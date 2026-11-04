"""Orchestrare: programează colectorii, trece semnalele prin motor, trimite mesajele."""

from __future__ import annotations

import datetime as dt
import json
import logging
import os
import re
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import collectors as C
from . import geo
from . import http
from .config import Config, ConfigError, num
from .engine import Engine, EngineConfig
from .iso_helpers import manual_roalert_signal
from .models import Message, Signal
from .notify import ConsoleSender, Dispatcher, NtfySender, TelegramCommands, TelegramSender, describe_error, parse_hhmm
from .store import Store
from .timeutil import hhmm, iso, now

log = logging.getLogger("veghe")

# Ce roluri poate primi fiecare tip de sursă (un canal Telegram nu poate genera mesaje publice).
# instantanee ADS-B: nu se arhivează ca semnale (doar agregate în adsb_samples / adsb_gnss)
EPHEMERAL_ROLES = ("adsb", "adsb_militar")
TELEGRAM_ROLES = {"ua_alerts", "ua_direction", "ua_official", "md_official", "md_news"}
RSS_ROLES = {"md_official", "md_news", "ro_official_news"}
DOWN_AFTER_ERRORS = 3


def _str_list(v, name: str) -> list[str]:
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        raise ConfigError(f"{name} trebuie să fie o listă de texte, ex. [\"Iași\"]")
    return v


def build_collectors(cfg: Config) -> list[C.Collector]:
    kw = {"timeout": num(cfg.get("general", "http_timeout", default=15), "general.http_timeout"),
          "user_agent": cfg.get("general", "user_agent", default=http.DEFAULT_UA)}
    oblasts = _str_list(cfg.get("watch", "ua_oblasts", default=[]), "watch.ua_oblasts")
    raions = _str_list(cfg.get("watch", "ua_raions", default=[]), "watch.ua_raions")
    out: list[C.Collector] = []
    s = cfg.get("sources", default={}) or {}
    for key in ("telegram", "rss"):
        lst = s.get(key, [])
        if not isinstance(lst, list) or not all(isinstance(x, dict) for x in lst):
            raise ConfigError(f"[[sources.{key}]] trebuie să fie o listă de tabele (folosiți paranteze duble)")
    for t in s.get("telegram", []):
        if not t.get("channel"):
            raise ConfigError("[[sources.telegram]] fără „channel”")
    for r in s.get("rss", []):
        if not r.get("name") or not r.get("url"):
            raise ConfigError("[[sources.rss]] are nevoie de „name” și „url”")
    a = s.get("alerts_in_ua", {})
    if a.get("enabled") and cfg.secret("alerts_in_ua_token"):
        out.append(C.AlertsInUA(cfg.secret("alerts_in_ua_token"), a.get("url", "https://api.alerts.in.ua/v1/alerts/active.json"),
                                oblasts, raions, interval=max(10, num(a.get("interval", 20), "alerts_in_ua.interval")), **kw))
    u = s.get("ukrainealarm", {})
    if u.get("enabled") and cfg.secret("ukrainealarm_token"):
        out.append(C.UkraineAlarm(cfg.secret("ukrainealarm_token"), u.get("base_url", "https://api.ukrainealarm.com/api/v3"),
                                  oblasts + raions, interval=max(30, num(u.get("interval", 60), "ukrainealarm.interval")), **kw))
    for t in s.get("telegram", []) or []:
        if not t.get("enabled", True):
            continue
        role = t.get("role", "ua_official")
        if role not in TELEGRAM_ROLES:
            raise ConfigError(f"telegram:{t.get('channel')}: rol nepermis „{role}” (permise: {sorted(TELEGRAM_ROLES)})")
        out.append(C.TelegramWeb(t["channel"], role, t.get("base_url", "https://t.me/s/"),
                                 interval=max(30, num(t.get("interval", 60), "telegram.interval")), **kw))
        out[-1].probation = bool(t.get("probation", False))
    for r in s.get("rss", []) or []:
        if not r.get("enabled", True):
            continue
        role = r.get("role", "md_news")
        if role not in RSS_ROLES:
            raise ConfigError(f"rss:{r.get('name')}: rol nepermis „{role}” (permise: {sorted(RSS_ROLES)})")
        out.append(C.Feed(r["name"], r["url"], role, r.get("keywords"),
                          interval=max(60, num(r.get("interval", 120), "rss.interval")), **kw))
        out[-1].probation = bool(r.get("probation", False))
    ad = s.get("adsb", {})
    if ad.get("enabled"):
        mil = ad.get("military")
        if isinstance(mil, dict) and not mil.get("enabled", True):
            mil = None
        if mil is not None:
            if not (isinstance(mil, dict) and {"lat", "lon"} <= set(mil)):
                raise ConfigError("sources.adsb.military trebuie să aibă lat și lon (și opțional radius_nm, name)")
            mil = {"name": str(mil.get("name", "militar")), "lat": num(mil["lat"], "adsb.military.lat"),
                   "lon": num(mil["lon"], "adsb.military.lon"),
                   "radius_nm": num(mil.get("radius_nm", 150), "adsb.military.radius_nm")}
        pts = ad.get("points", [])
        names = []
        for i, pt in enumerate(pts if isinstance(pts, list) else []):
            if not isinstance(pt, dict) or not {"name", "lat", "lon"} <= set(pt):
                raise ConfigError(f"sources.adsb.points[{i}] trebuie să aibă name, lat, lon")
            num(pt["lat"], f"adsb.points[{i}].lat"), num(pt["lon"], f"adsb.points[{i}].lon")
            num(pt.get("radius_nm", 30), f"adsb.points[{i}].radius_nm")
            names.append(pt["name"])
        if len(names) != len(set(names)):
            raise ConfigError("sources.adsb.points: nume duplicate")
        cp = ad.get("control_point", "")
        if cp and cp not in names:
            raise ConfigError(f"sources.adsb.control_point = {cp!r} nu e numele niciunei zone din points ({names})")
        try:
            out.append(C.Adsb(ad.get("url_template", "https://api.adsb.lol/v2/point/{lat}/{lon}/{radius}"),
                              ad.get("points", []), interval=max(30, num(ad.get("interval", 60), "adsb.interval")),
                              fallback_templates=_str_list(ad.get("fallback_templates", []), "adsb.fallback_templates"),
                              api_key=cfg.secret("adsblol_api_key"), local_url=ad.get("local_url", ""),
                              local_points=_str_list(ad.get("local_points", []), "adsb.local_points"),
                              control_point=ad.get("control_point", ""), military=mil,
                              analysis=ad.get("analysis") or {},
                              min_request_gap_s=num(ad.get("min_request_gap_s", 1.1), "adsb.min_request_gap_s"), **kw))
        except TypeError as e:  # cheie necunoscută în [sources.adsb.analysis]
            raise ConfigError(f"sources.adsb.analysis: {e}") from None
    from . import notam as N

    for n in s.get("notam", []) or []:
        if not isinstance(n, dict) or not n.get("enabled", True):
            continue
        opts = {k: n[k] for k in ("urls", "watch_firs", "locations", "categories", "nms_host", "tls_ciphers") if k in n}
        for k in ("max_dist_km", "max_prut_km", "near_km", "near_prut_km", "near_prut_max_km", "nms_radius_nm"):
            if k in n:
                opts[k] = num(n[k], f"notam.{k}")
        if "nms_center" in n:
            opts["nms_center"] = tuple(n["nms_center"])
        try:
            out.append(N.NotamCollector(n.get("name", "romatsa"), n.get("source", "romatsa_wfs"),
                                        client_id=cfg.secret("faa_nms_client_id"),
                                        client_secret=cfg.secret("faa_nms_client_secret"),
                                        interval=num(n.get("interval", 900), "notam.interval"), **opts, **kw))
        except N.NotamCredentialsError as e:
            log.warning("notam:%s dezactivat: %s", n.get("name", "faa"), e)
        except (ValueError, TypeError) as e:
            raise ConfigError(f"notam:{n.get('name')}: {e}") from None
    names = [c.name for c in out]
    if len(names) != len(set(names)):
        raise ConfigError(f"surse cu același nume: {sorted({n for n in names if names.count(n) > 1})}")
    return out


def _targets(v) -> list:
    """[engine] targets = ["iasi", "suceava", …]: chei sau nume de localități din veghe.geo."""
    from .nlp import normalize

    out = []
    for k in _str_list(v, "engine.targets"):
        key = re.sub(r"[\s-]+", "_", normalize(k))  # „Piatra Neamț” → piatra_neamt
        p = (geo.TARGET_KEYS.get(key) or geo.BY_KEY.get(key)
             or next((x for x in geo.GAZETTEER if normalize(x.name) == normalize(k)), None))
        if p is None:
            raise ConfigError(f"engine.targets: localitate necunoscută „{k}”")
        out.append(p)
    return out or [geo.IASI]


def build_engine(cfg: Config, store) -> Engine:
    e = cfg.get("engine", default={}) or {}
    d = EngineConfig.__dataclass_fields__

    def g(k):
        return num(e.get(k, d[k].default), f"engine.{k}")

    ec = EngineConfig(
        watch_oblasts=cfg.get("watch", "ua_oblasts", default=[]),
        watch_raions=cfg.get("watch", "ua_raions", default=[]),
        watch_counties=_str_list(e.get("watch_counties", d["watch_counties"].default_factory()), "engine.watch_counties"),
        max_age_min=g("max_age_min"), max_age_news_min=g("max_age_news_min"), ttl_min=g("ttl_min"),
        approach_km=g("approach_km"), vigilance_quiet_min=g("vigilance_quiet_min"), vigilance_end_min=g("vigilance_end_min"),
        official_repeat_min=g("official_repeat_min"), tg_alert_ttl_min=g("tg_alert_ttl_min"),
        state_stale_min=g("state_stale_min"), news_echo_min=g("news_echo_min"),
        targets=_targets(e.get("targets", geo.NE_TARGETS)),
    )
    return Engine(ec, store)


def build_dispatcher(cfg: Config, store, verify_private: bool = False) -> tuple[Dispatcher, bool]:
    """Întoarce (dispatcher, grupul_intern_e_de_incredere)."""
    api = cfg.get("notify", "telegram_api", default="https://api.telegram.org")
    gap = num(cfg.get("notify", "telegram_min_interval", default=3.1), "notify.telegram_min_interval")
    internal: list = [ConsoleSender()]
    public: list = []
    tok = cfg.secret("telegram_bot_token")
    if tok and cfg.secret("telegram_internal_chat_id"):
        tg = TelegramSender(tok, cfg.secret("telegram_internal_chat_id"), api, gap)
        ok = True
        if verify_private and not cfg.get("notify", "allow_unverified_internal_chat", default=False):
            try:
                reason = tg.check_private()
            except http.HttpError as e:
                if 400 <= e.status < 500 and e.status != 429:  # răspuns clar: token/ID greșit, bot scos din grup
                    log.critical("Telegram intern INACCESIBIL (%s): alertele NU vor ajunge în grup. Verificați "
                                 "TELEGRAM_BOT_TOKEN, TELEGRAM_INTERNAL_CHAT_ID și că botul e membru.", describe_error(e))
                else:
                    log.warning("nu am putut verifica dacă grupul intern e privat (%s)", describe_error(e))
                reason = None
            except Exception as e:  # noqa: BLE001 - fără rețea la pornire: nu orbim operatorii
                log.warning("nu am putut verifica dacă grupul intern e privat (%s)", type(e).__name__)
                reason = None
            if reason:
                log.critical("REFUZ trimiterea pe Telegram intern: %s", reason)
                ok = False
        if ok:
            internal.append(tg)
        trusted = ok
    else:
        trusted = False
    ntfy_url = cfg.secret("ntfy_url")
    if ntfy_url and cfg.secret("ntfy_topic"):
        if "ntfy.sh" in ntfy_url and not cfg.secret("ntfy_token") and not cfg.get("notify", "allow_public_ntfy", default=False):
            log.critical("REFUZ ntfy: ntfy.sh fără NTFY_TOKEN e public (oricine știe topicul citește mesajele interne)")
        else:
            internal.append(NtfySender(ntfy_url, cfg.secret("ntfy_topic"), cfg.secret("ntfy_token")))
    if tok and cfg.secret("telegram_public_chat_id"):
        public.append(TelegramSender(tok, cfg.secret("telegram_public_chat_id"), api, gap))
    return Dispatcher(store, internal, public, public_enabled=bool(cfg.get("notify", "public_enabled", default=False)),
                      auto_publish_official=bool(cfg.get("notify", "auto_publish_official", default=False)),
                      dedup_min=num(cfg.get("notify", "dedup_min", default=10), "notify.dedup_min")), trusted


class App:
    def __init__(self, cfg: Config, *, store: Store | None = None, verify_private: bool = False):
        self.cfg = cfg
        self.store = store or Store(cfg.get("general", "db_path", default="data/veghe.db"))
        self.collectors = build_collectors(cfg)
        self.engine = build_engine(cfg, self.store)
        self.dispatcher, internal_trusted = build_dispatcher(cfg, self.store, verify_private)
        self.next_due: dict[str, float] = {c.name: 0.0 for c in self.collectors}
        self.errors: dict[str, int] = {c.name: 0 for c in self.collectors}
        self.polled_ok: set[str] = set()
        self.down: set[str] = set()
        self.down_msg_at: dict[str, dt.datetime] = {}
        self.down_since: dict[str, dt.datetime] = {}
        self.down_announced: set[str] = set()
        self._restore_down()
        self.running: dict[str, Future] = {}
        self.started: dict[str, float] = {}
        self.stuck: set[str] = set()
        self.clock_skew_s: float | None = None
        self.boot = time.monotonic()
        self.last_cycle: dt.datetime | None = None
        self._last_kv = 0.0
        self._last_prune = float("-inf")
        self.flush_in_cycle = True  # în run_forever, livrarea are firul ei
        self.stop = threading.Event()
        # câte un fir per sursă (+rezervă): o sursă blocată nu le poate opri pe celelalte
        for c in self.collectors:
            if isinstance(c, C.Adsb):
                c.attach_store(self.store, now())  # fondul de trafic după repornire (doar agregate)
        self._pool = ThreadPoolExecutor(max_workers=len(self.collectors) + 2, thread_name_prefix="colector")
        self._lock = threading.RLock()
        self.commands = None
        if cfg.secret("telegram_bot_token") and cfg.operator_ids:
            self.commands = TelegramCommands(cfg.secret("telegram_bot_token"), cfg.operator_ids, self.handle_command,
                                             cfg.get("notify", "telegram_api", default="https://api.telegram.org"),
                                             self.store,
                                             # dacă grupul intern nu e privat, comenzile merg doar în chat privat
                                             cfg.secret("telegram_internal_chat_id") if internal_trusted else None)

    # ------------------------------------------------------------------ ciclu
    def _poll(self, c: C.Collector, t: dt.datetime):
        try:
            return c.poll(t), None
        except Exception as e:  # noqa: BLE001 - o sursă căzută nu oprește bucla
            return [], e

    def _submit(self, msgs: list[Message]):
        for m in msgs:
            self.dispatcher.submit(m)

    def ingest(self, sigs: list[Signal], t: dt.datetime, warmup: bool = False) -> int:
        """Arhivează semnalele noi și le trece prin motor. Întoarce câte mesaje au rezultat.

        warmup = prima citire a unei surse după pornire: arhivăm tot, dar acționăm doar pe
        semnalele cu dată (cele fără dată ar putea fi știri vechi)."""
        n = 0
        with self._lock:
            for s in sorted(sigs, key=lambda x: x.when):
                if s.role not in EPHEMERAL_ROLES and not self.store.add_signal(s):
                    continue  # deja văzut
                if warmup and s.role not in ("ua_alert_state", *EPHEMERAL_ROLES) and s.published_at is None:
                    continue
                msgs = self.engine.process(s, t)
                self._submit(msgs)
                n += len(msgs)
        return n

    def _save_down(self):
        st = {n: {"msg_at": iso(self.down_msg_at[n]) if n in self.down_msg_at else None,
                  "since": iso(self.down_since[n]) if n in self.down_since else None,
                  "announced": n in self.down_announced} for n in set(self.down_msg_at) | self.down}
        self.store.kv_set("stare_surse", json.dumps(st))

    def _restore_down(self):
        """După repornire: o sursă anunțată căzută rămâne „căzută” (fără un nou anunț; „a revenit” la revenire)."""
        from .timeutil import parse_iso

        try:
            st = json.loads(self.store.kv_get("stare_surse", "") or "{}")
        except ValueError:
            return
        t = now()
        for n, d in st.items() if isinstance(st, dict) else []:
            if n not in self.errors or not isinstance(d, dict):
                continue
            at = parse_iso(d.get("msg_at"))
            if at and t - at < dt.timedelta(hours=2):
                self.down_msg_at[n] = at
            if d.get("announced"):
                self.down.add(n)
                self.down_announced.add(n)
                self.down_since[n] = parse_iso(d.get("since")) or t

    def _source_down(self, c, err, t):
        if self.errors[c.name] < DOWN_AFTER_ERRORS:
            return
        if getattr(c, "probation", False) and c.name not in self.polled_ok:
            # sursă nouă, încă neconfirmată: nu alarmăm grupul (check-sources o arată cu ✗)
            if c.name not in self.down:
                self.down.add(c.name)
                log.warning("sursa nouă %s nu răspunde (%s); verificați-o cu check-sources", c.name, type(err).__name__)
            return
        if c.name in self.down:
            # o cădere neanunțată (sursă intermitentă) care durează: o anunțăm după 15 min
            if c.name in self.down_announced or t - self.down_since.get(c.name, t) < dt.timedelta(minutes=15):
                return
        else:
            self.down.add(c.name)
            self.down_since[c.name] = t
            last = self.down_msg_at.get(c.name)
            if last and t - last < dt.timedelta(hours=2):
                log.warning("sursa %s din nou căzută (anunțată deja la %s; mesaj doar dacă durează 15 min)", c.name, hhmm(last))
                return  # sursă intermitentă: nu repetăm „căzută / a revenit” la fiecare pâlpâire
        self.down_msg_at[c.name] = t
        self.down_announced.add(c.name)
        self._save_down()
        self._submit([Message("internal", "sursa_cazuta",
                              f"[INTERN] SURSĂ CĂZUTĂ · {hhmm(t)}. {c.name} nu răspunde ({type(err).__name__}, "
                              f"{self.errors[c.name]} erori la rând). Avertizarea pe această cale e oarbă până revine.")])

    def run_cycle(self, t: dt.datetime | None = None) -> int:
        t = t or now()
        mono = time.monotonic()
        produced = 0
        # 1) culegem ce s-a terminat (fără să așteptăm sursele lente)
        for name, fut in list(self.running.items()):
            c = next(x for x in self.collectors if x.name == name)
            if not fut.done():
                # descărcare blocată: o tratăm ca eroare (o singură dată), ca operatorii să afle
                if name not in self.stuck and mono - self.started[name] > getattr(c, "max_poll_s", 3 * c.timeout + 30):
                    self.stuck.add(name)
                    self.errors[name] = max(self.errors[name] + 1, DOWN_AFTER_ERRORS)
                    self.store.health_error(name, "blocată: descărcarea nu s-a terminat")
                    with self._lock:
                        self._source_down(c, TimeoutError("blocată"), t)
                continue
            del self.running[name]
            self.stuck.discard(name)
            sigs, err = fut.result()
            if err is None:
                self.errors[name] = 0
                self.next_due[name] = mono + c.interval
                self._check_clock(c)  # doar după o citire reușită (altfel antetul Date e vechi)
                sample = next((s.text for s in sigs if s.role != "adsb_militar"), "")[:200]
                self.store.health_ok(name, len(sigs), sample)
                if c.role == "ua_alert_state":
                    with self._lock:
                        self.engine.source_alive(name, t)
                warm = name not in self.polled_ok
                self.polled_ok.add(name)
                produced += self.ingest(sigs, t, warmup=warm)
                if name in self.down:
                    self.down.discard(name)
                    if name in self.down_announced:
                        self.down_announced.discard(name)
                        self._save_down()
                        self._submit([Message("internal", "sursa_revenita", f"[INTERN] Sursa {name} a revenit · {hhmm(t)}.")])
            else:
                self.errors[name] += 1
                backoff = min(c.interval * (2 ** min(self.errors[name], 5)), 900)
                if isinstance(err, C.AdsbNoData):
                    backoff = min(backoff, max(2 * c.interval, 120))  # agregator „înghețat”: reîncercăm des
                if isinstance(err, http.HttpError) and err.retry_after:
                    backoff = max(backoff, err.retry_after)
                self.next_due[name] = mono + backoff
                self.store.health_error(name, f"{type(err).__name__}: {err}"[:300])
                log.warning("sursa %s: %s (următoarea încercare în %.0f s)", name, type(err).__name__, backoff)
                with self._lock:
                    self._source_down(c, err, t)
        # 2) pornim sursele scadente care nu rulează deja
        for c in self.collectors:
            if c.name not in self.running and self.next_due[c.name] <= mono:
                self.running[c.name] = self._pool.submit(self._poll, c, t)
                self.started[c.name] = mono
        # 3) reguli dependente de timp
        with self._lock:
            msgs = self.engine.tick(t)
            self._submit(msgs)
            produced += len(msgs)
        if self.flush_in_cycle:
            self.dispatcher.flush()
        self.last_cycle = t
        if mono - self._last_kv > 60:
            self.store.kv_set("last_cycle", iso(t))
            self._last_kv = mono
        if mono - self._last_prune > 86400:
            self.store.prune()
            self._last_prune = mono
        return produced

    def _check_clock(self, c):
        """Compară ceasul serverului cu antetul HTTP Date al sursei (ex. un ceas care o ia înainte)."""
        d = getattr(c, "last_date", None)
        if not d:
            return
        try:
            import email.utils

            src = email.utils.parsedate_to_datetime(d)
        except (TypeError, ValueError):
            return
        skew = (now() - src).total_seconds()
        if self.clock_skew_s is None or abs(skew) < abs(self.clock_skew_s):
            self.clock_skew_s = skew  # cea mai mică diferență observată (latența o umflă)
        if abs(skew) > 120 and not getattr(self, "_skew_warned", False):
            self._skew_warned = True
            log.critical("ceasul serverului diferă cu %.0f s de sursa %s; porniți NTP", skew, c.name)
            self._submit([Message("internal", "ceas", f"[INTERN] Ceasul serverului diferă cu ~{skew:.0f} s de surse. "
                                                      f"Mesajele pot fi ignorate ca „vechi”. Porniți sincronizarea NTP.")])

    def drain(self, timeout: float = 10.0):
        """Așteaptă colectorii porniți (folosit în teste)."""
        end = time.monotonic() + timeout
        while self.running and time.monotonic() < end:
            if all(f.done() for f in self.running.values()):
                break
            time.sleep(0.02)

    # ------------------------------------------------------------------ comenzi operator
    def handle_command(self, cmd: str, args: list[str], uid, sent_at: dt.datetime | None = None) -> str:
        t = sent_at or now()
        if cmd in ("/start", "/ajutor", "/help"):
            return ("Comenzi: /stare · /ultimele [n] · /coada · /aproba N · /respinge N · "
                    "/roalert <județ> [hh:mm] (înregistrează un RO-Alert primit)")
        if cmd == "/stare":
            return self.status_text(now())
        if cmd == "/ultimele":
            n = int(args[0]) if args and args[0].isdigit() else 5
            rows = self.store.recent_signals(min(n, 20))
            return "\n".join(f"{r['received_at'][11:16]}Z {r['source']}: {r['text'][:120]}" for r in rows) or "Nimic încă."
        if cmd == "/coada":
            self.dispatcher.expire_pending()
            rows = self.store.outbox("pending_approval", limit=10, newest_first=True)
            return "\n".join(f"#{r['id']} {r['kind']}: {r['text'][:150]}" for r in rows) or "Nimic în așteptare."
        if cmd == "/aproba" and args and args[0].isdigit():
            return self.dispatcher.approve(int(args[0]), str(uid))
        if cmd == "/respinge" and args and args[0].isdigit():
            return self.dispatcher.reject(int(args[0]), str(uid))
        if cmd == "/roalert" and args:
            at = t  # implicit: momentul în care operatorul a trimis comanda
            county = " ".join(a for a in args if ":" not in a)[:40]
            hm = [a for a in args if ":" in a]
            if hm:
                at = parse_hhmm(hm[0], t)
            self.log_roalert(county, at, f"operator:{uid}")
            return f"Înregistrat: RO-Alert în județul {county} la {hhmm(at)}."
        return "Comandă necunoscută. /ajutor"

    def log_roalert(self, county: str, at: dt.datetime, who: str):
        self.ingest([manual_roalert_signal(county, at, who)], now())

    # ------------------------------------------------------------------ stare
    def status(self, t: dt.datetime | None = None) -> dict:
        t = t or now()
        with self._lock:
            st = self.engine.status(t)
        st["ultimul_ciclu"] = hhmm(self.last_cycle) if self.last_cycle else None
        st["surse"] = [{"sursa": r["source"], "ultima_ok": r["last_ok"], "erori_consecutive": r["error_count"],
                        "ultima_eroare": r["last_error"]} for r in self.store.health()]
        st["in_asteptare"] = len(self.store.outbox("pending_approval"))
        st["livrari_interne_esuate_24h"] = self.store.failed_outbox_count("internal")
        st["surse_blocate"] = sorted(self.stuck)
        st["decalaj_ceas_s"] = round(self.clock_skew_s) if self.clock_skew_s is not None else None
        return st

    def status_text(self, t) -> str:
        st = self.status(t)
        bad = [s["sursa"] for s in st["surse"] if s["erori_consecutive"]]
        lines = [f"Nivel: {st['nivel']} · ultimul ciclu {st['ultimul_ciclu'] or 'încă niciunul'}",
                 f"Alerte UA urmărite: {', '.join(st['alerte_ua_active']) or 'niciuna'}"
                 + (f" (episodul VIGILENȚĂ se încheie la {st['vigilenta_se_incheie']} dacă nu reapar)"
                    if st.get("vigilenta_se_incheie") and st['ultimul_ciclu'] else ""),
                 f"Ipoteze: {len(st['ipoteze'])} · mesaje publice în așteptare: {st['in_asteptare']}",
                 f"Orașe urmărite: {', '.join(st.get('tinte') or []) or 'Iași'}",
                 f"Surse cu erori: {', '.join(bad) or 'niciuna'}"]
        if st["livrari_interne_esuate_24h"]:
            lines.append(f"ATENȚIE: {st['livrari_interne_esuate_24h']} mesaje interne nelivrate în 24 h (vezi `outbox`)")
        if st["surse_blocate"]:
            lines.append(f"Surse blocate: {', '.join(st['surse_blocate'])}")
        if st["decalaj_ceas_s"] is not None and abs(st["decalaj_ceas_s"]) > 120:
            lines.append(f"Ceas decalat cu ~{st['decalaj_ceas_s']} s față de surse")
        if st["surse_stare_invechite"]:
            lines.append(f"Stare UA învechită: {', '.join(st['surse_stare_invechite'])}")
        for h in st["ipoteze"]:
            lines.append(f"H-{h['id']} {h['nivel']}{' (oficial)' if h['oficial'] else ''} · {h['pozitie'] or '?'} · {h['actualizat']}")
        zones = {k: v for k, v in (st.get("adsb_zone") or {}).items() if not v.get("control")}
        if zones:
            lines.append("ADS-B: " + "; ".join(
                f"{k} {v['trafic']} în aer" + (f", date: {v['acoperire']}" if v["acoperire"] != "ok" else "")
                + (f", sursa: {v['sursa']}" if v.get("sursa") not in (None, "principal") else "")
                + (f", date bune din {v['la_ok']}" if v.get("vechi") else "")
                + (f", GNSS {v['gnss']}" if v.get("gnss") not in (None, "normal", "insuficient") else "")
                + (f", {v['manevre']} în așteptare/întoarse" if v.get("manevre") else "") for k, v in zones.items()))
        if st.get("militar"):
            lines.append(f"Militar (ADS-B public, doar intern) la {st['militar']['la']}: {st['militar']['descriere']}")
        if st.get("notam_active"):
            near = [n for n in st["notam_active"] if n["aproape"] or n["fir"] == "LUUU"]
            lines.append(f"NOTAM active: {len(st['notam_active'])} ({len(near)} lângă orașele urmărite / Prut sau în R. Moldova)"
                         + ("".join(f"\n  · {n['id']} {n['categorie']} până la {n['pana_la']}" for n in near[:5])))
        return "\n".join(lines)

    def healthy(self) -> bool:
        return self.last_cycle is not None and now() - self.last_cycle < dt.timedelta(minutes=3)

    # ------------------------------------------------------------------ fire auxiliare
    def _commands_loop(self):
        while not self.stop.is_set():
            try:
                self.commands.poll_once()
            except Exception as e:  # noqa: BLE001
                log.warning("comenzi Telegram: %s", type(e).__name__)
                self.stop.wait(15)

    def _dispatch_loop(self):
        while not self.stop.is_set():
            try:
                self.dispatcher.flush()
            except Exception:  # noqa: BLE001
                log.exception("eroare la trimiterea mesajelor")
            self.stop.wait(1.0)

    def _watchdog(self):
        """Dacă bucla principală se blochează, ieșim; Docker/systemd repornesc procesul."""
        while not self.stop.wait(30):
            never = self.last_cycle is None and time.monotonic() - self.boot > 300
            if never or (self.last_cycle and now() - self.last_cycle > dt.timedelta(minutes=5)):
                log.critical("bucla principală e blocată de peste 5 minute; ies pentru repornire")
                os._exit(3)

    def start_status_server(self):
        app = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                if self.path == "/health":
                    ok = app.healthy()
                    body, code = (b"ok" if ok else b"stale"), (200 if ok else 503)
                    ctype = "text/plain"
                elif self.path == "/status":
                    body, code, ctype = json.dumps(app.status(), ensure_ascii=False, indent=1).encode(), 200, "application/json"
                else:
                    body, code, ctype = b"veghe: /health /status", 404, "text/plain"
                self.send_response(code)
                self.send_header("Content-Type", f"{ctype}; charset=utf-8")
                self.end_headers()
                self.wfile.write(body)

        # în Docker se leagă la 0.0.0.0 (VEGHE_STATUS_BIND), iar compose publică portul doar pe 127.0.0.1
        bind = os.environ.get("VEGHE_STATUS_BIND") or self.cfg.get("general", "status_bind", default="127.0.0.1")
        port = int(os.environ.get("VEGHE_STATUS_PORT") or self.cfg.get("general", "status_port", default=8080))
        try:
            srv = ThreadingHTTPServer((bind, port), H)
        except OSError as e:  # portul ocupat nu are voie să oprească alertele
            log.error("pagina de stare NU a pornit pe %s:%s (%s); alertele continuă. Schimbați status_port în config.toml.",
                      bind, port, e)
            return None
        threading.Thread(target=srv.serve_forever, daemon=True, name="status").start()
        log.info("pagina de stare: http://%s:%s/status", bind, srv.server_address[1])
        return srv

    def run_forever(self, cycle_seconds: float = 2.0):
        log.info("veghe pornit: %d surse active", len(self.collectors))
        for c in self.collectors:
            log.info("  sursa %s (rol %s, la %ss)", c.name, c.role, c.interval)
        self.flush_in_cycle = False
        # confirmă livrarea la fiecare pornire (și după repornirile automate); un singur mesaj de pornire
        # în așteptare, chiar dacă au fost mai multe reporniri cât Telegram era indisponibil
        old = self.store.supersede_queued("pornire")
        extra = f" ({old} porniri anterioare nelivrate)" if old else ""
        self._submit([Message("internal", "pornire", f"[INTERN] veghe pornit · {hhmm(now())} · {len(self.collectors)} "
                              f"surse active. Alertele vor veni în acest grup.{extra}")])
        srv = self.start_status_server()
        threading.Thread(target=self._dispatch_loop, daemon=True, name="livrare").start()
        threading.Thread(target=self._watchdog, daemon=True, name="watchdog").start()
        if self.commands:
            threading.Thread(target=self._commands_loop, daemon=True, name="comenzi").start()
        try:
            while not self.stop.is_set():
                try:
                    self.run_cycle()
                except Exception:  # noqa: BLE001
                    log.exception("eroare în ciclu")
                self.stop.wait(cycle_seconds)
        finally:
            if srv:
                srv.shutdown()
            self._pool.shutdown(wait=False, cancel_futures=True)
            log.info("veghe oprit")
