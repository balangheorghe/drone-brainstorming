"""Motorul de reguli: transformă semnalele în stări și mesaje.

Niveluri (docs/07): VIGILENȚĂ (alertă UA în zonele urmărite) → DIRECȚIE (mesaj UA despre
drone spre Moldova/zonele de graniță) → MOLDOVA (detecție anunțată în R. Moldova) →
APROPIERE (poziție la ≤ approach_km de Iași, spre vest). Separat: OFICIAL (RO-Alert raportat).

Reguli de siguranță „prin construcție”:
- mesajele PUBLICE se creează doar din semnale cu rol în PUBLIC_SOURCE_ROLES
  (presă/comunicate românești sau operatorul), doar ca retransmitere sau încetare, și
  dintr-un șablon fix (fără textul articolului);
- conținutul canalelor ucrainene nu ajunge niciodată într-un mesaj public;
- semnalele prea vechi se arhivează, dar nu declanșează nimic.
"""

from __future__ import annotations

import datetime as dt
import logging
import re
import statistics
import urllib.parse
from dataclasses import dataclass, field

from . import geo
from .models import LEVEL_RO, PUBLIC_SOURCE_ROLES, Level, Message, Signal
from .nlp import analyze, normalize
from .timeutil import hhmm

log = logging.getLogger("veghe.engine")

NEW_DRONE_MARKERS = ("a doua drona", "o noua drona", "o alta drona", "inca o drona", "другий", "ще один", "второй", "еще один")
# Locuri din UA relevante (vestul reg. Odesa, Vinnytsia de lângă MD, Cernăuți)
UA_WATCH_KEYS = {"podilsk", "rozdilna", "izmail", "reni", "bolhrad", "bilhorod", "vylkove", "mohyliv",
                 "tulchyn", "chernivtsi", "novodnistrovsk", "vinnytsia"}
PRUT_EDGE_KEYS = {"ungheni", "sculeni", "zagarancea", "lipcani", "giurgiulesti", "leova", "cahul", "briceni"}
NEWS_ROLES = {"md_news", "md_official", "ro_official_news"}

# Canalul air_alert_ua: „🔴 16:12 Повітряна тривога в Подільський район.” / „🟢 Відбій тривоги в …”
TG_ON = re.compile(r"(?:повітрян\w* тривог\w*|тривога ще триває)\s+(?:в|у)\s+([^\.\n#!]+)")
TG_OFF = re.compile(r"відбій\s+(?:повітрян\w* )?тривог\w*\s+(?:в|у)\s+([^\.\n#!]+)")


@dataclass
class EngineConfig:
    watch_oblasts: list[str]
    watch_raions: list[str]
    watch_counties: list[str] = field(default_factory=lambda: ["Iași", "Botoșani", "Suceava", "Neamț", "Vaslui", "Bacău"])
    max_age_min: float = 30
    max_age_news_min: float = 60
    ttl_min: float = 45
    approach_km: float = 120
    vigilance_quiet_min: float = 20
    official_repeat_min: float = 60
    tg_alert_ttl_min: float = 90
    state_stale_min: float = 10
    target: geo.Place = geo.IASI


@dataclass
class Hypothesis:
    id: int
    created: dt.datetime
    updated: dt.datetime
    level: Level
    place: geo.Place | None = None
    origin: list[geo.Place] = field(default_factory=list)
    jet: bool = False
    official: bool = False
    from_new_marker: bool = False
    notified: Level = Level.FOND
    last_msg_at: dt.datetime | None = None
    last_msg_place: str = ""
    sources: list[str] = field(default_factory=list)
    closed: bool = False


def _domain(url: str) -> str:
    try:
        host = urllib.parse.urlparse(url).hostname or ""
    except ValueError:
        host = ""
    return host.removeprefix("www.")


class Engine:
    def __init__(self, cfg: EngineConfig, store=None):
        self.cfg = cfg
        self.store = store
        self.ua_state: dict[str, list[dict]] = {}
        self.ua_state_alive: dict[str, dt.datetime] = {}
        self.ua_tg_state: dict[str, dt.datetime] = {}
        self.vigilance_since: dt.datetime | None = None
        self.vigilance_msg_at: dt.datetime | None = None
        self.vigilance_titles: set[str] = set()
        self.hyps: list[Hypothesis] = []
        self._next_id = int(store.kv_get("next_hypothesis_id", "1")) if store else 1
        self.last_official: dict[str, dt.datetime] = {}
        self.last_end: dict[str, dt.datetime] = {}
        self.adsb_anomaly: dict[str, bool] = {}
        self.clock_skew_warned = False
        self._watch_titles = list(cfg.watch_oblasts) + list(cfg.watch_raions)
        self._watch_norm = {normalize(t): t for t in self._watch_titles}

    # ------------------------------------------------------------------ utilitare
    def _event(self, level, hyp, kind, text, now):
        if self.store:
            self.store.add_event(level, hyp, kind, text, now)

    def _new_hyp(self, now, level, from_new_marker=False) -> Hypothesis:
        h = Hypothesis(id=self._next_id, created=now, updated=now, level=level, from_new_marker=from_new_marker)
        self._next_id += 1
        if self.store:
            self.store.kv_set("next_hypothesis_id", str(self._next_id))
        self.hyps.append(h)
        return h

    def open_hyps(self) -> list[Hypothesis]:
        return [h for h in self.hyps if not h.closed]

    def _eta_text(self, p: geo.Place) -> str:
        d_t = geo.dist(p, self.cfg.target)
        a, b = geo.eta_minutes(d_t)
        if p.country == "RO":
            return f"{p.name}: {d_t:.0f} km de {self.cfg.target.name}"
        d_p = geo.dist_to_prut_km(p)
        pa, pb = geo.eta_minutes(d_p)
        return (f"{p.name}: ~{d_t:.0f} km de {self.cfg.target.name}. ETA Prut {pa}–{pb} min, "
                f"{self.cfg.target.name} {a}–{b} min (linie dreaptă, 450/150 km/h)")

    def _adsb_note(self) -> str:
        pts = [k for k, v in self.adsb_anomaly.items() if v]
        return f" ADS-B: trafic civil oprit în jurul {', '.join(pts)}." if pts else ""

    @staticmethod
    def _excerpt(text: str, n: int = 220) -> str:
        t = " ".join(text.split())
        return t if len(t) <= n else t[: n - 1] + "…"

    # ------------------------------------------------------------------ vigilență
    def source_alive(self, source: str, now: dt.datetime):
        """Apelat la fiecare citire reușită a unei surse de stare (chiar dacă starea nu s-a schimbat)."""
        self.ua_state_alive[source] = now

    def _active_titles(self, now) -> set[str]:
        stale = dt.timedelta(minutes=self.cfg.state_stale_min)
        titles = {a["title"] for src, lst in self.ua_state.items()
                  if now - self.ua_state_alive.get(src, now) <= stale for a in lst}
        ttl = dt.timedelta(minutes=self.cfg.tg_alert_ttl_min)
        titles |= {t for t, at in self.ua_tg_state.items() if now - at <= ttl}
        return titles

    def _drone_threat(self) -> bool:
        return any("drones" in a.get("threats", []) for lst in self.ua_state.values() for a in lst)

    def _update_vigilance(self, now) -> list[Message]:
        active = self._active_titles(now)
        msgs = []
        if active and self.vigilance_since is None:
            self.vigilance_since = now
            self._event(Level.VIGILENTA, None, "vigilenta_start", ", ".join(sorted(active)), now)
        if not active and self.vigilance_since is not None:
            self._event(Level.FOND, None, "vigilenta_stop", "", now)
            self.vigilance_since = None
            self.vigilance_titles = set()
            return msgs
        new = active - self.vigilance_titles
        quiet = dt.timedelta(minutes=self.cfg.vigilance_quiet_min)
        if active and new and (self.vigilance_msg_at is None or now - self.vigilance_msg_at >= quiet):
            pts = [geo.BY_KEY[k] for k in {geo.UA_AREA_POINT.get(t) for t in active} if k in geo.BY_KEY]
            near = min(pts, key=lambda p: geo.dist(p, self.cfg.target)) if pts else None
            eta = ""
            if near:
                a, b = geo.eta_minutes(geo.dist(near, self.cfg.target))
                eta = f" Dacă o dronă ar veni de acolo spre {self.cfg.target.name}: ~{a}–{b} min (linie dreaptă)."
            threat = " Tip amenințare raportat: drone." if self._drone_threat() else ""
            text = (f"[INTERN] VIGILENȚĂ · {hhmm(now)}. Alertă aeriană activă în: {', '.join(sorted(active))}.{threat}{eta}"
                    f"{self._adsb_note()} Stare internă, nespecifică (filtrul e activ ~20% din timp). Nicio acțiune publică.")
            msgs.append(Message("internal", "vigilenta", text, Level.VIGILENTA))
            self.vigilance_msg_at = now
        self.vigilance_titles = set(active)
        return msgs

    def _tg_alert(self, sig: Signal, now) -> list[Message]:
        n = normalize(sig.text)
        for rx, on in ((TG_OFF, False), (TG_ON, True)):
            for m in rx.finditer(n):
                for loc in re.split(r",| та | і ", m.group(1)):
                    title = self._watch_norm.get(loc.strip(" .:;"))
                    if not title:
                        continue
                    if on:
                        self.ua_tg_state[title] = sig.when
                    else:
                        self.ua_tg_state.pop(title, None)
        return self._update_vigilance(now)

    # ------------------------------------------------------------------ ipoteze
    def _match_hyp(self, place: geo.Place | None, now, new_marker: bool) -> Hypothesis | None:
        best = None
        for h in self.open_hyps():
            # „a doua / o altă dronă”: doar la o ipoteză deschisă tot de un astfel de mesaj, recent
            if new_marker and not (h.from_new_marker and now - h.created <= dt.timedelta(minutes=20)):
                continue
            if place is not None and h.place is not None:
                hours = max((now - h.updated).total_seconds() / 3600, 0.05)
                if geo.dist(place, h.place) > geo.V_JET_KMH * hours + 80:
                    continue
            if best is None or h.updated > best.updated:
                best = h
        return best

    def _hyp_message(self, h: Hypothesis, kind: str, sig: Signal, now) -> list[Message]:
        place_key = h.place.key if h.place else ""
        changed = h.level > h.notified or place_key != h.last_msg_place
        recent = h.last_msg_at is not None and now - h.last_msg_at < dt.timedelta(minutes=3)
        if not changed or (recent and h.level <= h.notified):
            return []
        pos = self._eta_text(h.place) if h.place else "poziție nepublicată"
        jet = " (posibil cu reacție)" if h.jet else ""
        src = f"{sig.source} {sig.url}".strip()
        off = " RO-Alert deja raportat." if h.official else ""
        if kind == "directie":
            text = (f"[INTERN – NU REDISTRIBUIȚI] DIRECȚIE · {hhmm(now)} · H-{h.id}. Sursă UA: drone{jet} spre zona de graniță. "
                    f"{pos}. Text: «{self._excerpt(sig.text)}» ({src}){self._adsb_note()}")
        elif kind == "moldova":
            text = (f"[INTERN] ATENȚIE · {hhmm(now)} · H-{h.id}. R. Moldova: dronă{jet} semnalată. {pos}. "
                    f"«{self._excerpt(sig.text)}» ({src}).{off}{self._adsb_note()} Verificați RO-Alert; pregătiți retransmiterea.")
        else:  # apropiere
            text = (f"[INTERN] APROPIERE · {hhmm(now)} · H-{h.id}. Dronă{jet} aproape de Prut / {self.cfg.target.name}. {pos}. "
                    f"«{self._excerpt(sig.text)}» ({src}).{off}{self._adsb_note()} "
                    f"Dacă nu există încă RO-Alert, contactați ISU conform protocolului.")
        h.notified = max(h.notified, h.level)
        h.last_msg_at = now
        h.last_msg_place = place_key
        return [Message("internal", kind, text, h.level, h.id, sig.role)]

    def _ua_direction(self, sig, f, now) -> list[Message]:
        if not (f.drone or f.jet) or (f.missile and not f.drone):
            return []
        cand = [p for p in f.direction_to if p.country in ("MD", "RO") or p.key in UA_WATCH_KEYS]
        cand += [p for p in f.places if p.key in UA_WATCH_KEYS or p.country in ("MD", "RO")]
        border_regions = {geo.ODESA, geo.VINN, geo.CHERN}
        westward_near = f.westward and any(p.region in border_regions for p in f.places)
        relevant = bool(cand) or f.mentions_moldova or (f.mentions_romania and f.westward) or westward_near
        if not relevant:
            return []
        place = cand[0] if cand else None
        new_marker = any(m in normalize(sig.text) for m in NEW_DRONE_MARKERS)
        h = self._match_hyp(place, now, new_marker) or self._new_hyp(now, Level.DIRECTIE, new_marker)
        h.level = max(h.level, Level.DIRECTIE)
        h.updated, h.jet = now, h.jet or f.jet
        if place:
            h.place = place
        h.sources.append(sig.source)
        self._event(h.level, h.id, "directie", self._excerpt(sig.text, 300), now)
        return self._hyp_message(h, "directie", sig, now)

    def _approach(self, h: Hypothesis, f) -> bool:
        if f.mentions_romania and (f.westward or f.lost_or_left):
            return True
        if h.place is None:
            return False
        if h.place.key in PRUT_EDGE_KEYS:
            return True
        west = h.place.lon < 28.65 or f.westward or any(p.country == "RO" for p in f.direction_to)
        return geo.dist(h.place, self.cfg.target) <= self.cfg.approach_km and west

    def _moldova(self, sig, f, now) -> list[Message]:
        if not f.drone:
            return []
        if not (f.mentions_moldova or f.md_places or f.airspace_restricted or sig.role == "md_official"):
            return []
        md = f.md_places
        dir_md = [p for p in f.direction_to if p.country in ("MD", "RO")]
        place = None
        if f.lost_or_left and md:
            place = md[-1]
        elif md or dir_md:
            place = min(md + dir_md, key=lambda p: geo.dist(p, self.cfg.target))
        new_marker = any(m in normalize(sig.text) for m in NEW_DRONE_MARKERS)
        h = self._match_hyp(place, now, new_marker) or self._new_hyp(now, Level.MOLDOVA, new_marker)
        h.level = max(h.level, Level.MOLDOVA)
        h.updated, h.jet = now, h.jet or f.jet
        if place:
            h.place = place
        h.origin += [p for p in f.origin if p not in h.origin]
        h.sources.append(sig.source)
        approach = self._approach(h, f)
        if approach:
            h.level = max(h.level, Level.APROPIERE)
        kind = "apropiere" if approach else "moldova"
        self._event(h.level, h.id, kind, self._excerpt(sig.text, 300), now)
        return self._hyp_message(h, kind, sig, now)

    # ------------------------------------------------------------------ oficial (RO)
    def _official(self, sig, f, now) -> list[Message]:
        if sig.role not in PUBLIC_SOURCE_ROLES:
            return []
        watch = {normalize(c) for c in self.cfg.watch_counties}
        county_places = [p for p in f.ro_counties if normalize(p.name) in watch]
        counties = [p.name for p in county_places]
        if not counties:
            return []
        repeat = dt.timedelta(minutes=self.cfg.official_repeat_min)
        link = f" {sig.url}" if sig.url else ""
        src = "operator (RO-Alert primit)" if sig.role == "manual" else (_domain(sig.url) or sig.source)
        title = self._excerpt(sig.text, 180)
        n = normalize(sig.text)
        if f.end:
            fresh = [c for c in counties if c not in self.last_end or now - self.last_end[c] > repeat]
            if not fresh:
                return []
            for c in fresh:
                self.last_end[c] = now
                self.last_official.pop(c, None)  # o alertă nouă după încetare va fi luată în seamă
            self._event(Level.INCHEIAT, None, "incetare", title, now)
            return [
                Message("internal", "incetare_intern",
                        f"[INTERN] ÎNCETARE raportată · {hhmm(now)} · {', '.join(fresh)}: «{title}»{link}", Level.INCHEIAT,
                        origin_role=sig.role),
                Message("public", "incetare",
                        f"[NEOFICIAL] ÎNCETARE · {hhmm(now)}. Se relatează încetarea alertei pentru: {', '.join(fresh)}. "
                        f"Sursa: {src}{link}. Nu atingeți eventualele fragmente; anunțați-le la 112.",
                        Level.INCHEIAT, origin_role=sig.role),
            ]
        aerial = f.drone or "spatiu aerian" in n or "spatiul aerian" in n or "obiecte" in n
        if not (f.roalert and aerial):
            return []
        fresh = [c for c in counties if c not in self.last_official or now - self.last_official[c] > repeat]
        if not fresh:
            return []
        for c in fresh:
            self.last_official[c] = now
            self.last_end.pop(c, None)
        near = [p for p in county_places if p.name in fresh]
        for h in self.open_hyps():
            close = h.place is None or any(geo.dist(h.place, p) <= 200 for p in near)
            if h.level >= Level.MOLDOVA and close and now - h.updated <= dt.timedelta(minutes=90):
                h.official = True
        self._event(Level.OFICIAL, None, "oficial", title, now)
        return [
            Message("internal", "oficial_intern",
                    f"[INTERN] OFICIAL · {hhmm(now)}. RO-Alert raportat pentru: {', '.join(fresh)} ({sig.source}). "
                    f"«{title}»{link}", Level.OFICIAL, origin_role=sig.role),
            Message("public", "retransmitere",
                    f"[NEOFICIAL] RETRANSMITERE · {hhmm(now)}. Se relatează un mesaj RO-Alert pentru: {', '.join(fresh)}. "
                    f"Sursa: {src}{link}. Urmați doar instrucțiunile oficiale RO-Alert / ISU. "
                    f"Observațiile se raportează la 112.", Level.OFICIAL, origin_role=sig.role),
        ]

    # ------------------------------------------------------------------ ADS-B
    def _adsb(self, sig, now) -> list[Message]:
        m = sig.meta
        point = m.get("point", "?")
        if self.store:
            self.store.add_adsb_sample(now, point, m.get("civil_airborne", 0), m.get("civil_total", 0))
            hist = self.store.adsb_samples(point, now - dt.timedelta(hours=2))
        else:
            hist = []
        vals = [r["civil_airborne"] for r in hist]
        if len(vals) < 20:
            return []
        recent, base = vals[-3:], vals[:-10]
        baseline = statistics.median(base) if base else 0
        anomaly = baseline >= 2 and max(recent) == 0
        was = self.adsb_anomaly.get(point, False)
        self.adsb_anomaly[point] = anomaly
        if anomaly and not was:
            self._event(Level.FOND, None, "adsb_anomalie", f"{point}: de la ~{baseline:g} la 0", now)
            if self.vigilance_since or any(h.level >= Level.DIRECTIE for h in self.open_hyps()):
                return [Message("internal", "adsb",
                                f"[INTERN] ADS-B · {hhmm(now)}. Traficul civil din jurul {point} a scăzut de la ~{baseline:g} la 0 "
                                f"aeronave în aer. Posibilă închidere de spațiu aerian (de confirmat; poate fi și altă cauză).",
                                Level.FOND)]
        return []

    # ------------------------------------------------------------------ intrare
    def process(self, sig: Signal, now: dt.datetime) -> list[Message]:
        if sig.role == "adsb":
            return self._adsb(sig, now)
        if sig.role == "ua_alert_state":
            self.ua_state[sig.source] = list(sig.meta.get("active") or [])
            self.ua_state_alive[sig.source] = now
            return self._update_vigilance(now)
        pub = sig.published_at
        if pub and pub > now + dt.timedelta(minutes=2):
            if not self.clock_skew_warned:
                log.warning("sursa %s are ora în viitor (%s); verificați ceasul serverului (NTP)", sig.source, pub)
                self.clock_skew_warned = True
            pub = now
        limit = self.cfg.max_age_news_min if sig.role in NEWS_ROLES else self.cfg.max_age_min
        if pub and now - pub > dt.timedelta(minutes=limit):
            return []  # arhivat, dar prea vechi ca să declanșeze ceva
        if sig.role == "ua_alerts":
            return self._tg_alert(sig, now)
        f = analyze(sig.text)
        if sig.role in ("ua_direction", "ua_official"):
            return self._ua_direction(sig, f, now)
        if sig.role in ("md_official", "md_news"):
            return self._moldova(sig, f, now)
        if sig.role in PUBLIC_SOURCE_ROLES:
            return self._official(sig, f, now)
        return []

    def tick(self, now: dt.datetime) -> list[Message]:
        ttl = dt.timedelta(minutes=self.cfg.ttl_min)
        for h in self.open_hyps():
            if now - h.updated > ttl:
                h.closed = True
                self._event(h.level, h.id, "ipoteza_inchisa", f"fără semnale noi de {self.cfg.ttl_min:g} min", now)
        self.hyps = [h for h in self.hyps if not h.closed or now - h.updated < dt.timedelta(hours=6)]
        return self._update_vigilance(now)

    def status(self, now: dt.datetime) -> dict:
        lvl = max([h.level for h in self.open_hyps()] + [Level.VIGILENTA if self.vigilance_since else Level.FOND])
        stale = dt.timedelta(minutes=self.cfg.state_stale_min)
        return {
            "nivel": LEVEL_RO[Level(lvl)],
            "vigilenta_din": hhmm(self.vigilance_since) if self.vigilance_since else None,
            "alerte_ua_active": sorted(self._active_titles(now)),
            "surse_stare_invechite": sorted(s for s, t in self.ua_state_alive.items() if now - t > stale),
            "ipoteze": [{"id": h.id, "nivel": LEVEL_RO[h.level], "oficial": h.official,
                         "pozitie": h.place.name if h.place else None,
                         "actualizat": hhmm(h.updated), "reactie": h.jet} for h in self.open_hyps()],
            "adsb_anomalii": [k for k, v in self.adsb_anomaly.items() if v],
        }
