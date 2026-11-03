"""Colectori: fiecare citește o sursă și întoarce semnale. Nu iau decizii.

Formatele sunt preluate din surse verificabile (vezi comentariile de la fiecare parser);
fixturile din tests/fixtures urmează aceleași formate.
"""

from __future__ import annotations

import datetime as dt
import email.utils
import hashlib
import html
import html.entities
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

from . import http
from .models import Signal
from .nlp import normalize
from .timeutil import RO_TZ, iso, parse_iso, to_local


class Collector:
    def __init__(self, name: str, role: str, interval: float, *, timeout: float = 15, user_agent: str = http.DEFAULT_UA):
        self.name = name
        self.role = role
        self.interval = interval
        self.timeout = timeout
        self.user_agent = user_agent
        self.last_date = None

    def _get(self, url: str, headers: dict | None = None) -> http.Response:
        r = http.request(url, headers=headers, timeout=self.timeout, user_agent=self.user_agent)
        self.last_date = r.headers.get("date")  # pentru verificarea ceasului serverului
        return r

    def poll(self, now: dt.datetime) -> list[Signal]:  # pragma: no cover - interfață
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Ucraina – starea alertelor
# ---------------------------------------------------------------------------

def _state_signal(source: str, active: list[dict], now: dt.datetime) -> Signal:
    names = ", ".join(sorted({a["title"] for a in active})) or "nicio alertă în zonele urmărite"
    h = hashlib.sha256(json.dumps(sorted(active, key=lambda a: a["title"]), ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
    return Signal(source=source, role="ua_alert_state", text=f"Alerte active: {names}", received_at=now,
                  ext_id=f"{h}@{iso(now)}", meta={"active": active, "state_hash": h})


def parse_alerts_in_ua(data: dict, watch_oblasts: list[str], watch_raions: list[str]) -> list[dict]:
    """Format: răspunsul /v1/alerts/active.json, câmpurile din clientul oficial
    alerts-ua/alerts-in-ua-py (alert.py): location_title, location_type, location_oblast,
    location_raion, alert_type, alert_level, started_at, threats[{threat_type, level}]."""
    out = []
    for a in data.get("alerts") or []:
        if a.get("alert_type") != "air_raid" or a.get("finished_at"):
            continue
        title = a.get("location_title") or ""
        oblast = a.get("location_oblast") or ""
        raion = a.get("location_raion") or ""
        ltype = a.get("location_type") or ""
        watched = (
            title in watch_raions or raion in watch_raions
            or (ltype == "oblast" and title in watch_oblasts)
            or (not watch_raions and oblast in watch_oblasts)
        )
        if not watched:
            continue
        out.append({
            "title": title,
            "title_en": a.get("location_title_en") or "",
            "type": ltype,
            "oblast": oblast,
            "level": a.get("alert_level") or "",
            "threats": sorted({t.get("threat_type") for t in (a.get("threats") or []) if t.get("threat_type")}),
            "started_at": a.get("started_at"),
        })
    return out


class AlertsInUA(Collector):
    def __init__(self, token: str, url: str, watch_oblasts, watch_raions, **kw):
        super().__init__("alerts_in_ua", "ua_alert_state", kw.pop("interval", 20), **kw)
        self.token, self.url = token, url
        self.watch_oblasts, self.watch_raions = list(watch_oblasts), list(watch_raions)
        self._last_modified = None
        self._last_hash = None

    def poll(self, now):
        headers = {"Accept": "application/json", "Authorization": f"Bearer {self.token}"}
        if self._last_modified:
            headers["If-Modified-Since"] = self._last_modified
        r = self._get(self.url, headers)
        if r.status == 304:
            return []
        active = parse_alerts_in_ua(r.json(), self.watch_oblasts, self.watch_raions)
        self._last_modified = r.headers.get("last-modified")  # doar după o parsare reușită
        sig = _state_signal(self.name, active, now)
        if sig.meta["state_hash"] == self._last_hash:
            return []
        self._last_hash = sig.meta["state_hash"]
        return [sig]


def parse_ukrainealarm(regions: list, watch_titles: list[str]) -> list[dict]:
    """Format: GET /api/v3/alerts → listă AlertRegionModel (regionId, regionType, regionName,
    regionEngName, lastUpdate, activeAlerts[{regionId, regionType, type, lastUpdate}]),
    după UkraineAlarm-python/models (attribute_map) și integrarea Home Assistant."""
    out = []
    for reg in regions or []:
        name = reg.get("regionName") or ""
        if name not in watch_titles:
            continue
        types = sorted({a.get("type") for a in reg.get("activeAlerts") or [] if a.get("type")})
        if "AIR" not in types:
            continue
        out.append({"title": name, "title_en": reg.get("regionEngName") or "", "type": reg.get("regionType") or "",
                    "oblast": "", "level": "", "threats": [], "started_at": reg.get("lastUpdate")})
    return out


class UkraineAlarm(Collector):
    def __init__(self, token: str, base_url: str, watch_titles, **kw):
        super().__init__("ukrainealarm", "ua_alert_state", kw.pop("interval", 60), **kw)
        self.token, self.base = token, base_url.rstrip("/")
        self.watch = list(watch_titles)
        self._last_index = None
        self._last_hash = None

    def poll(self, now):
        headers = {"accept": "application/json", "authorization": self.token}
        idx = self._get(f"{self.base}/alerts/status", headers).json().get("lastActionIndex")
        if idx is not None and idx == self._last_index:
            return []
        regions = self._get(f"{self.base}/alerts", headers).json()
        self._last_index = idx
        sig = _state_signal(self.name, parse_ukrainealarm(regions, self.watch), now)
        if sig.meta["state_hash"] == self._last_hash:
            return []
        self._last_hash = sig.meta["state_hash"]
        return [sig]


# ---------------------------------------------------------------------------
# Telegram – previzualizarea publică t.me/s/<canal>
# ---------------------------------------------------------------------------

class _TmeParser(HTMLParser):
    """Selectoare după RSSHub (lib/routes/telegram/channel.ts):
    .tgme_widget_message[data-post], .tgme_widget_message_bubble > .tgme_widget_message_text,
    .tgme_widget_message_date[href] > time[datetime]. Textul din răspunsuri (reply) e ignorat."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.posts: list[dict] = []
        self._stack: list[set] = []  # clasele fiecărui element deschis
        self._cur: dict | None = None
        self._msg_depth = -1
        self._text_depth = -1
        self._reply_depth = -1
        self.seen_history = False

    VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr"}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set((a.get("class") or "").split())
        if tag == "br":
            if self._cur is not None and self._text_depth >= 0 and self._reply_depth < 0:
                self._cur["text"].append("\n")
            return
        if tag in self.VOID:
            return
        depth = len(self._stack)
        self._stack.append(classes)
        if "tgme_channel_history" in classes:
            self.seen_history = True
        if "tgme_widget_message" in classes and a.get("data-post"):
            self._cur = {"post": a["data-post"], "text": [], "datetime": None, "link": "",
                         "service": "service_message" in classes}
            self._msg_depth = depth
            self.posts.append(self._cur)
        if self._cur is None:
            return
        if "tgme_widget_message_reply" in classes:
            self._reply_depth = depth
        if "tgme_widget_message_text" in classes and self._reply_depth < 0 and self._text_depth < 0:
            self._text_depth = depth
        if "tgme_widget_message_date" in classes and a.get("href"):
            self._cur["link"] = a["href"]
        if tag == "time" and a.get("datetime") and self._cur["datetime"] is None:
            self._cur["datetime"] = a["datetime"]

    def handle_endtag(self, tag):
        if tag in self.VOID or not self._stack:
            return
        self._stack.pop()
        depth = len(self._stack)
        if depth == self._text_depth:
            self._text_depth = -1
        if depth == self._reply_depth:
            self._reply_depth = -1
        if depth == self._msg_depth:
            self._msg_depth = -1
            self._cur = None

    def handle_data(self, data):
        if self._cur is not None and self._text_depth >= 0 and self._reply_depth < 0:
            self._cur["text"].append(data)


def parse_tme(page: str) -> list[dict]:
    p = _TmeParser()
    p.feed(page)
    if not p.posts and not p.seen_history:
        # ca la RSSHub: fără mesaje și fără istoric = canal inexistent sau previzualizare dezactivată
        raise ValueError("pagina t.me/s nu conține mesaje publice (canal inexistent sau previzualizare dezactivată)")
    out = []
    for post in p.posts:
        text = re.sub(r"[ \t]+", " ", "".join(post["text"])).strip()[:4000]
        if not text or post.get("service"):
            continue
        out.append({"post": post["post"], "text": text, "published_at": parse_iso(post["datetime"]),
                    "link": post["link"] or f"https://t.me/{post['post']}"})
    return out


class TelegramWeb(Collector):
    def __init__(self, channel: str, role: str, base_url: str = "https://t.me/s/", **kw):
        super().__init__(f"telegram:{channel}", role, kw.pop("interval", 60), **kw)
        self.channel = channel
        self.url = base_url.rstrip("/") + "/" + channel

    def poll(self, now):
        posts = parse_tme(self._get(self.url).text())
        # cheia include un hash al textului: o postare editată (direcție nouă) e reevaluată
        return [Signal(source=self.name, role=self.role, text=p["text"], received_at=now,
                       published_at=p["published_at"], url=p["link"],
                       ext_id=f"{p['post']}#{hashlib.sha256(p['text'].encode()).hexdigest()[:8]}",
                       meta={"post": p["post"]}) for p in posts]


# ---------------------------------------------------------------------------
# RSS / Atom (presă, Google News, Moldpres)
# ---------------------------------------------------------------------------

_TAG_RX = re.compile(r"<[^<>]*>")


def _strip_html(s: str, cap: int = 20000) -> str:
    return re.sub(r"\s+", " ", html.unescape(_TAG_RX.sub(" ", (s or "")[:cap]))).strip()


def _as_ro_local(t: dt.datetime) -> dt.datetime:
    """Dată fără fus orar → ora României (presa locală), corect și în jurul schimbării orei."""
    if RO_TZ is not None:
        return t.replace(tzinfo=RO_TZ).astimezone(dt.timezone.utc)
    off1 = to_local((t - dt.timedelta(hours=2)).replace(tzinfo=dt.timezone.utc)).utcoffset()
    off = to_local((t - off1).replace(tzinfo=dt.timezone.utc)).utcoffset()
    return (t - off).replace(tzinfo=dt.timezone.utc)


_ZONES = {"UT": "+0000", "UTC": "+0000", "GMT": "+0000", "Z": "+0000", "CET": "+0100", "CEST": "+0200",
          "EET": "+0200", "EEST": "+0300", "MSK": "+0300"}


def _parse_date(s: str | None) -> dt.datetime | None:
    if not s:
        return None
    s = s.strip()
    iso_s = s[:-1] + "+00:00" if s.endswith("Z") else s
    try:
        t = dt.datetime.fromisoformat(iso_s)
    except ValueError:
        m = re.search(r"\s([A-Za-z]{1,4}|[+-]\d{4})$", s)
        zone = m.group(1) if m else None
        s2 = s[: m.start(1)] + _ZONES[zone.upper()] if zone and zone.upper() in _ZONES else s
        try:
            t = email.utils.parsedate_to_datetime(s2)
        except (TypeError, ValueError, IndexError):
            return None
        if t.tzinfo is None and zone:  # „-0000” = UTC (RFC 5322); alt nume de zonă necunoscut → UTC
            return t.replace(tzinfo=dt.timezone.utc)
    if t.tzinfo is None:
        return _as_ro_local(t)
    return t.astimezone(dt.timezone.utc)


_XML_ENT = {"amp", "lt", "gt", "quot", "apos"}


def _prolog_encoding(raw: bytes) -> str | None:
    m = re.match(rb"\s*<\?xml[^>]*encoding=[\"']([A-Za-z0-9._-]+)[\"']", raw)
    return m.group(1).decode("ascii") if m else None


def _fix_entities(raw: bytes) -> bytes:
    """Înlocuiește doar entitățile HTML necunoscute XML-ului (ex. &nbsp;) cu referințe numerice."""
    try:
        text = raw.decode(_prolog_encoding(raw) or "utf-8", "replace")
    except LookupError:
        text = raw.decode("utf-8", "replace")

    def rep(m):
        name = m.group(1)
        if name is None:
            return "&amp;"
        if name.startswith("#") or name in _XML_ENT:
            return m.group(0)
        ch = html.entities.html5.get(name + ";")
        return "".join(f"&#{ord(c)};" for c in ch) if ch else "&amp;" + name + ";"

    text = re.sub(r"&(?:(#\d+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]*);)?", rep, text)
    text = re.sub(r"^<\?xml[^>]*\?>", '<?xml version="1.0" encoding="utf-8"?>', text)
    return text.encode("utf-8")


def _first(children: dict, *names):
    # atenție: un element XML fără copii e „fals” în Python, deci nu folosim `or`
    for n in names:
        if children.get(n) is not None:
            return children[n]
    return None


def parse_feed(xml_text: str) -> list[dict]:
    """RSS 2.0 (<item>) și Atom (<entry>)."""
    raw = xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text
    try:
        root = ET.fromstring(raw)  # din octeți: ET respectă encoding-ul din prolog
    except ET.ParseError:
        # unele fluxuri folosesc entități HTML (&nbsp; etc.) nedeclarate în XML
        root = ET.fromstring(_fix_entities(raw))
    rtag = root.tag.split("}")[-1].lower()
    if rtag not in ("rss", "feed", "rdf"):
        raise ValueError(f"nu e un flux RSS/Atom (rădăcina <{rtag}>) – URL greșit sau pagină de blocare?")
    items = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag not in ("item", "entry"):
            continue
        f = {c.tag.split("}")[-1]: c for c in el}
        title = _strip_html((f.get("title").text if f.get("title") is not None else "") or "")
        link = ""
        links = [c for c in el if c.tag.split("}")[-1] == "link"]
        alt = [c for c in links if c.get("rel") in (None, "alternate")] or links
        if alt:
            link = (alt[0].text or alt[0].get("href") or "").strip()
        summary_el = _first(f, "description", "summary", "content")
        summary = _strip_html(summary_el.text if summary_el is not None else "")
        date_el = _first(f, "pubDate", "published", "updated", "date")
        guid_el = _first(f, "guid", "id")
        items.append({
            "title": title, "link": link, "summary": summary[:800],
            "published_at": _parse_date(date_el.text if date_el is not None else None),
            "guid": (guid_el.text if guid_el is not None else "") or link or title,
        })
    return items


def strip_publisher(title: str) -> str:
    """„Titlu - Publicație” → „Titlu” (doar ultimul segment, dacă e scurt)."""
    head, sep, tail = title.rpartition(" - ")
    return head.strip() if sep and head and len(tail) <= 40 else title


class Feed(Collector):
    def __init__(self, name: str, url: str, role: str, keywords: list[str] | None = None, **kw):
        super().__init__(f"rss:{name}", role, kw.pop("interval", 120), **kw)
        self.url = url
        self.keywords = [normalize(k) for k in (keywords or [])]
        # Google News pune numele publicației la final („… - Pro TV Chișinău”); îl scoatem
        # ca să nu fie citit drept localitate.
        self.strip_source = "news.google." in url

    def poll(self, now):
        r = self._get(self.url)
        body = r.body
        ctype = r.headers.get("content-type", "")
        if "charset=" in ctype and not _prolog_encoding(body):
            # encoding declarat doar în antetul HTTP: îl aplicăm noi
            cs = ctype.split("charset=")[-1].split(";")[0].strip().strip('"')
            try:
                text = body.decode(cs, "replace")
                body = re.sub(r"^\s*<\?xml[^>]*\?>", "", text).encode("utf-8")
            except LookupError:
                pass
        items = parse_feed(body)
        self.last_raw = len(items)  # pentru check-sources: câți itemi erau înainte de filtrul pe cuvinte-cheie
        out = []
        for it in items:
            title, summary = it["title"][:500], it["summary"]
            if self.strip_source:
                title = strip_publisher(title)
                summary = ""  # descrierea Google News repetă titlul și publicația
            text = title + (" — " + summary if summary and summary != title else "")
            if self.keywords and not any(k in normalize(text) for k in self.keywords):
                continue
            out.append(Signal(source=self.name, role=self.role, text=text, received_at=now,
                              published_at=it["published_at"], url=it["link"], ext_id=it["guid"]))
        return out


# ---------------------------------------------------------------------------
# ADS-B – doar trafic civil, doar numărători
# ---------------------------------------------------------------------------

def count_aircraft(data: dict) -> dict:
    """Format readsb „re-api” (folosit de adsb.lol /v2/point): {"ac": [...], "now", "total"}.
    Militar = dbFlags & 1 (README-json readsb). Aeronavele militare sunt ignorate complet:
    nu se numără, nu se păstrează, nu se afișează."""
    airborne = total = 0
    for ac in data.get("ac") or []:
        if int(ac.get("dbFlags") or 0) & 1:
            continue
        total += 1
        if ac.get("alt_baro") != "ground" and ac.get("lat") is not None:
            airborne += 1
    return {"civil_airborne": airborne, "civil_total": total}


class AdsbNoData(RuntimeError):
    """Nicio zonă civilă n-a primit date utilizabile (răspunsuri vechi, goale sau erori)."""


class Adsb(Collector):
    """Trafic aerian din ADS-B (agregator public și/sau receptor propriu).

    Civil: analiza din veghe.adsb_analysis (scădere reală vs. lipsă de date, interferență GNSS,
    așteptări, întoarceri, coduri de urgență) – fără identități de aeronave.
    Militar (opțional, `military`): doar un rezumat pe grupuri, rol „adsb_militar”, doar intern."""

    def __init__(self, url_template: str, points: list[dict], *, fallback_templates=(), api_key: str = "",
                 local_url: str = "", local_points=(), control_point: str = "", military: dict | None = None,
                 analysis: dict | None = None, min_request_gap_s: float = 1.1, **kw):
        from .adsb_analysis import AdsbAnalysisConfig, AdsbAnalyzer

        super().__init__("adsb", "adsb", kw.pop("interval", 60), **kw)
        self.url_template, self.points = url_template, list(points)
        self.fallback_templates = [t for t in (fallback_templates or []) if t]
        self.api_key = api_key
        self.local_url, self.local_points = local_url, set(local_points or [])
        self.control_point = control_point or None
        if military:
            military = {**military, "name": military.get("name", "militar"),
                        "radius_nm": float(military.get("radius_nm", 150))}
        self.military = military
        self.min_gap = float(min_request_gap_s)
        self._last_req: dict[str, float] = {}
        self.analyzer = AdsbAnalyzer(AdsbAnalysisConfig(**(analysis or {})), control_area=self.control_point)
        self.store = None
        self.gnss_ready: dict[str, bool] = {}
        self._gnss_baseline_at = float("-inf")
        self.stale_s = float((analysis or {}).get("stale_s", 45.0))
        self.last_errors: list[str] = []

    @property
    def max_poll_s(self) -> float:
        """Cât poate dura legitim o citire (zone × surse × 2×timeout + pauze); peste asta e „blocată”."""
        n = len(self.points) + (1 if self.military else 0)
        tries = 1 + len(self.fallback_templates) + (1 if self.local_url else 0)
        return n * (tries * 2 * self.timeout + self.min_gap) + 30

    # ---------------------------------------------------------------- fond din arhivă (doar agregate)
    def attach_store(self, store, now: dt.datetime):
        """După pornire: fondul de trafic din eșantioanele agregate ale ultimelor 2 ore."""
        self.store = store
        for p in self.points:
            rows = store.adsb_samples(p["name"], now - dt.timedelta(hours=2))
            self.analyzer.seed_counts(p["name"], [(r["ts"], r["civil_airborne"]) for r in rows])

    def _refresh_gnss_baseline(self, now: dt.datetime):
        import time

        if self.store is None or time.monotonic() - self._gnss_baseline_at < 3600:
            return
        self._gnss_baseline_at = time.monotonic()
        for p in self.points:
            p90, days = self.store.adsb_gnss_baseline(p["name"], now)
            self.analyzer.set_gnss_baseline(p["name"], p90)
            self.gnss_ready[p["name"]] = days >= 3  # mesajele GNSS pornesc după 3 zile de fond

    # ---------------------------------------------------------------- cereri
    def _fetch(self, template: str, p: dict) -> dict:
        import time
        from urllib.parse import urlsplit

        url = template.format(lat=p["lat"], lon=p["lon"], radius=int(p.get("radius_nm", 30)))
        host = urlsplit(url).netloc
        wait = self.min_gap - (time.monotonic() - self._last_req.get(host, float("-inf")))
        if wait > 0:
            time.sleep(min(wait, 5))
        headers = {"Accept": "application/json"}
        parts = urlsplit(url)
        hn = (parts.hostname or "").lower()
        if self.api_key and parts.scheme == "https" and (hn == "adsb.lol" or hn.endswith(".adsb.lol")):
            headers["X-API-Key"] = self.api_key  # doar spre adsb.lol, doar prin https
        try:
            return self._get(url, headers).json()
        finally:
            self._last_req[host] = time.monotonic()

    def _usable(self, data, now) -> bool:
        from .adsb_analysis import snapshot_meta

        m = snapshot_meta(data) if isinstance(data, dict) else {"ok": False}
        if not m.get("ok"):
            return False
        dn = m.get("data_now")
        return dn is None or now.timestamp() - dn <= self.stale_s

    def _snapshot(self, p: dict, now: dt.datetime, failed: set):
        """Prima sursă cu date utilizabile: receptor propriu (dacă e cazul), principală, rezerve.
        Sursele care au eșuat deja în această citire se încearcă ultimele. Întoarce (date, eticheta, eroare)."""
        cands = []
        if self.local_url and p["name"] in self.local_points:
            cands.append(("local", self.local_url))
        cands.append(("principal", self.url_template))
        cands += [(f"rezervă {i + 1}", t) for i, t in enumerate(self.fallback_templates)]
        cands.sort(key=lambda c: c[1] in failed)
        last, fallback = None, None
        for label, tpl in cands:
            try:
                data = self._fetch(tpl, p)
            except Exception as e:  # noqa: BLE001 - încercăm sursa următoare
                failed.add(tpl)
                last = e
                self.last_errors.append(f"{p['name']} · {label}: {type(e).__name__}: {str(e)[:120]}")
                continue
            if self._usable(data, now):
                return data, label, None
            failed.add(tpl)
            self.last_errors.append(f"{p['name']} · {label}: răspuns fără date proaspete")
            fallback = fallback or (data, label)
        if fallback:
            return fallback[0], fallback[1], None  # măcar un răspuns: analizorul îl va marca „date vechi”
        return None, None, last

    def poll(self, now):
        from . import adsb_military
        from .adsb_analysis import aircraft_list, snapshot_meta

        self._refresh_gnss_baseline(now)
        out, errors, failed = [], [], set()
        self.last_errors = []
        usable = 0
        # zona de control prima: altfel comparația folosește datele ciclului anterior
        for p in sorted(self.points, key=lambda x: x["name"] != self.control_point):
            data, label, err = self._snapshot(p, now, failed)
            if err is not None:
                errors.append(err)
            src = snapshot_meta(data) if data is not None else {"ok": False}
            r = self.analyzer.update(p["name"], p["lat"], p["lon"], int(p.get("radius_nm", 30)),
                                     aircraft_list(data) if data is not None else [], now, src)
            r["is_control"] = p["name"] == self.control_point
            r["sursa_date"] = label
            r.setdefault("gnss", {})["baseline_ready"] = self.gnss_ready.get(p["name"], False)
            cov = r.get("coverage") or {}
            if cov.get("ok") or cov.get("reason") not in ("sursa_indisponibila", "date_vechi"):
                usable += 1
            text = f"{p['name']}: {r.get('civil_airborne', 0)} civile în aer"
            if not cov.get("ok", True):
                text += f" (date: {cov.get('reason')})"
            out.append(Signal(source=self.name, role="adsb", text=text, received_at=now,
                              ext_id=f"{p['name']}@{iso(now)}", meta=r))
        if self.military:
            m = self.military
            data, _, err = self._snapshot(m, now, failed)
            s = {"area": m["name"], "radius_nm": m["radius_nm"], "ok": False, "n": 0, "grupuri": {}, "detalii": []}
            if err is None:
                try:
                    s = adsb_military.summary(data, m["name"], m["lat"], m["lon"], m["radius_nm"], now=now,
                                              stale_s=self.stale_s)
                except Exception as e:  # noqa: BLE001 - rezumatul militar nu are voie să strice citirea civilă
                    self.last_errors.append(f"militar: {type(e).__name__}: {e}")
            # și la eroare trimitem un semnal ok=False, ca motorul să nu folosească o stare veche
            out.append(Signal(source=self.name, role="adsb_militar", received_at=now,
                              text=f"Militar (ADS-B public), {m['name']}: "
                                   + (adsb_military.describe(s) if s.get("ok") else "date indisponibile"),
                              ext_id=f"militar@{iso(now)}", meta=s))
        if self.points and usable == 0:
            # nicio zonă civilă cu date utilizabile: sursa e „oarbă” → eroare (SURSĂ CĂZUTĂ după 3 citiri)
            if errors:
                raise errors[-1]
            raise AdsbNoData("niciun agregator ADS-B n-a dat date proaspete: " + "; ".join(self.last_errors[-3:]))
        return out
