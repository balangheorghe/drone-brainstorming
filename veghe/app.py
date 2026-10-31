"""Orchestrare: programează colectorii, trece semnalele prin motor, trimite mesajele."""

from __future__ import annotations

import datetime as dt
import json
import logging
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import collectors as C
from . import http
from .config import Config
from .engine import Engine, EngineConfig
from .models import Signal
from .notify import ConsoleSender, Dispatcher, NtfySender, TelegramCommands, TelegramSender, parse_hhmm
from .store import Store
from .timeutil import hhmm, iso, now

log = logging.getLogger("veghe")


def build_collectors(cfg: Config) -> list[C.Collector]:
    kw = {"timeout": cfg.get("general", "http_timeout", default=15),
          "user_agent": cfg.get("general", "user_agent", default=http.DEFAULT_UA)}
    oblasts = cfg.get("watch", "ua_oblasts", default=[])
    raions = cfg.get("watch", "ua_raions", default=[])
    out: list[C.Collector] = []
    s = cfg.get("sources", default={}) or {}
    a = s.get("alerts_in_ua", {})
    if a.get("enabled") and cfg.secret("alerts_in_ua_token"):
        out.append(C.AlertsInUA(cfg.secret("alerts_in_ua_token"), a.get("url", "https://api.alerts.in.ua/v1/alerts/active.json"),
                                oblasts, raions, interval=max(10, a.get("interval", 20)), **kw))
    u = s.get("ukrainealarm", {})
    if u.get("enabled") and cfg.secret("ukrainealarm_token"):
        out.append(C.UkraineAlarm(cfg.secret("ukrainealarm_token"), u.get("base_url", "https://api.ukrainealarm.com/api/v3"),
                                  oblasts + raions, interval=max(30, u.get("interval", 60)), **kw))
    for t in s.get("telegram", []) or []:
        if t.get("enabled", True):
            out.append(C.TelegramWeb(t["channel"], t.get("role", "ua_official"), t.get("base_url", "https://t.me/s/"),
                                     interval=max(30, t.get("interval", 60)), **kw))
    for r in s.get("rss", []) or []:
        if r.get("enabled", True):
            out.append(C.Feed(r["name"], r["url"], r.get("role", "md_news"), r.get("keywords"),
                              interval=max(60, r.get("interval", 120)), **kw))
    ad = s.get("adsb", {})
    if ad.get("enabled"):
        out.append(C.Adsb(ad.get("url_template", "https://api.adsb.lol/v2/point/{lat}/{lon}/{radius}"),
                          ad.get("points", []), interval=max(30, ad.get("interval", 60)), **kw))
    return out


def build_engine(cfg: Config, store) -> Engine:
    e = cfg.get("engine", default={}) or {}
    ec = EngineConfig(
        watch_oblasts=cfg.get("watch", "ua_oblasts", default=[]),
        watch_raions=cfg.get("watch", "ua_raions", default=[]),
        watch_counties=e.get("watch_counties", EngineConfig.__dataclass_fields__["watch_counties"].default_factory()),
        max_age_min=e.get("max_age_min", 30), ttl_min=e.get("ttl_min", 45), approach_km=e.get("approach_km", 120),
        vigilance_quiet_min=e.get("vigilance_quiet_min", 20), official_repeat_min=e.get("official_repeat_min", 60),
    )
    return Engine(ec, store)


def build_dispatcher(cfg: Config, store) -> Dispatcher:
    api = cfg.get("notify", "telegram_api", default="https://api.telegram.org")
    internal: list = [ConsoleSender()]
    public: list = []
    tok = cfg.secret("telegram_bot_token")
    gap = float(cfg.get("notify", "telegram_min_interval", default=3.1))
    if tok and cfg.secret("telegram_internal_chat_id"):
        internal.append(TelegramSender(tok, cfg.secret("telegram_internal_chat_id"), api, gap))
    if cfg.secret("ntfy_url") and cfg.secret("ntfy_topic"):
        internal.append(NtfySender(cfg.secret("ntfy_url"), cfg.secret("ntfy_topic"), cfg.secret("ntfy_token")))
    if tok and cfg.secret("telegram_public_chat_id"):
        public.append(TelegramSender(tok, cfg.secret("telegram_public_chat_id"), api, gap))
    return Dispatcher(store, internal, public, public_enabled=bool(cfg.get("notify", "public_enabled", default=False)),
                      auto_publish_official=bool(cfg.get("notify", "auto_publish_official", default=False)))


class App:
    def __init__(self, cfg: Config, *, store: Store | None = None):
        self.cfg = cfg
        self.store = store or Store(cfg.get("general", "db_path", default="data/veghe.db"))
        self.collectors = build_collectors(cfg)
        self.engine = build_engine(cfg, self.store)
        self.dispatcher = build_dispatcher(cfg, self.store)
        self.next_due: dict[str, float] = {c.name: 0.0 for c in self.collectors}
        self.errors: dict[str, int] = {c.name: 0 for c in self.collectors}
        self.last_cycle: dt.datetime | None = None
        self.stop = threading.Event()
        self._pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="colector")
        self._lock = threading.Lock()
        self.commands = None
        if cfg.secret("telegram_bot_token") and cfg.operator_ids:
            self.commands = TelegramCommands(cfg.secret("telegram_bot_token"), cfg.operator_ids, self.handle_command,
                                             cfg.get("notify", "telegram_api", default="https://api.telegram.org"), self.store)

    # ------------------------------------------------------------------ ciclu
    def _poll(self, c: C.Collector, t: dt.datetime):
        try:
            sigs = c.poll(t)
            sample = sigs[0].text[:200] if sigs else ""
            self.store.health_ok(c.name, len(sigs), sample)
            return c, sigs, None
        except Exception as e:  # noqa: BLE001 - o sursă căzută nu oprește bucla
            return c, [], e

    def ingest(self, sigs: list[Signal], t: dt.datetime) -> int:
        """Arhivează semnalele noi și le trece prin motor. Întoarce câte mesaje au rezultat."""
        n = 0
        with self._lock:
            for s in sorted(sigs, key=lambda x: x.when):
                if s.role != "adsb" and not self.store.add_signal(s):
                    continue  # deja văzut
                for m in self.engine.process(s, t):
                    self.dispatcher.submit(m)
                    n += 1
        return n

    def run_cycle(self, t: dt.datetime | None = None) -> int:
        t = t or now()
        mono = time.monotonic()
        due = [c for c in self.collectors if self.next_due[c.name] <= mono]
        futures = [self._pool.submit(self._poll, c, t) for c in due]
        produced = 0
        for f in futures:
            c, sigs, err = f.result()
            if err is None:
                self.errors[c.name] = 0
                self.next_due[c.name] = mono + c.interval
                produced += self.ingest(sigs, t)
            else:
                self.errors[c.name] += 1
                backoff = min(c.interval * (2 ** min(self.errors[c.name], 5)), 900)
                if isinstance(err, http.HttpError) and err.retry_after:
                    backoff = max(backoff, err.retry_after)
                self.next_due[c.name] = mono + backoff
                self.store.health_error(c.name, f"{type(err).__name__}: {err}")
                log.warning("sursa %s: %s (următoarea încercare în %.0f s)", c.name, err, backoff)
        with self._lock:
            for m in self.engine.tick(t):
                self.dispatcher.submit(m)
                produced += 1
        self.dispatcher.flush()
        self.last_cycle = t
        self.store.kv_set("last_cycle", iso(t))
        return produced

    # ------------------------------------------------------------------ comenzi operator
    def handle_command(self, cmd: str, args: list[str], uid) -> str:
        t = now()
        if cmd in ("/start", "/ajutor", "/help"):
            return ("Comenzi: /stare · /ultimele [n] · /coada · /aproba N · /respinge N · "
                    "/roalert <județ> [hh:mm] (înregistrează un RO-Alert primit)")
        if cmd == "/stare":
            return self.status_text(t)
        if cmd == "/ultimele":
            n = int(args[0]) if args and args[0].isdigit() else 5
            rows = self.store.recent_signals(min(n, 20))
            return "\n".join(f"{r['received_at'][11:16]}Z {r['source']}: {r['text'][:120]}" for r in rows) or "Nimic încă."
        if cmd == "/coada":
            rows = self.store.outbox("pending_approval")
            return "\n".join(f"#{r['id']} {r['kind']}: {r['text'][:150]}" for r in rows) or "Nimic în așteptare."
        if cmd == "/aproba" and args and args[0].isdigit():
            return self.dispatcher.approve(int(args[0]), str(uid))
        if cmd == "/respinge" and args and args[0].isdigit():
            return self.dispatcher.reject(int(args[0]), str(uid))
        if cmd == "/roalert" and args:
            at = t
            county = " ".join(a for a in args if ":" not in a)
            hm = [a for a in args if ":" in a]
            if hm:
                at = parse_hhmm(hm[0], t)
            self.log_roalert(county, at, f"operator:{uid}")
            return f"Înregistrat: RO-Alert în județul {county} la {hhmm(at)}."
        return "Comandă necunoscută. /ajutor"

    def log_roalert(self, county: str, at: dt.datetime, who: str):
        s = Signal(source=who, role="manual", received_at=now(), published_at=at,
                   text=f"RO-Alert (dronă, spațiu aerian) primit în județul {county} – înregistrat de operator",
                   ext_id=f"roalert|{county}|{iso(at)}")
        self.ingest([s], now())

    # ------------------------------------------------------------------ stare
    def status(self, t: dt.datetime | None = None) -> dict:
        t = t or now()
        st = self.engine.status(t)
        st["ultimul_ciclu"] = hhmm(self.last_cycle) if self.last_cycle else None
        st["surse"] = [{"sursa": r["source"], "ultima_ok": r["last_ok"], "erori_consecutive": r["error_count"],
                        "ultima_eroare": r["last_error"]} for r in self.store.health()]
        st["in_asteptare"] = len(self.store.outbox("pending_approval"))
        return st

    def status_text(self, t) -> str:
        st = self.status(t)
        bad = [s["sursa"] for s in st["surse"] if s["erori_consecutive"]]
        lines = [f"Nivel: {st['nivel']} · ultimul ciclu {st['ultimul_ciclu']}",
                 f"Alerte UA urmărite: {', '.join(st['alerte_ua_active']) or 'niciuna'}",
                 f"Ipoteze: {len(st['ipoteze'])} · mesaje publice în așteptare: {st['in_asteptare']}",
                 f"Surse cu erori: {', '.join(bad) or 'niciuna'}"]
        for h in st["ipoteze"]:
            lines.append(f"H-{h['id']} {h['nivel']} · {h['pozitie'] or '?'} · {h['actualizat']}")
        return "\n".join(lines)

    def healthy(self) -> bool:
        return self.last_cycle is not None and now() - self.last_cycle < dt.timedelta(minutes=3)

    # ------------------------------------------------------------------ fire auxiliare
    def _commands_loop(self):
        while not self.stop.is_set():
            try:
                self.commands.poll_once()
            except Exception as e:  # noqa: BLE001
                log.warning("comenzi Telegram: %s", e)
                self.stop.wait(15)

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
        port = int(self.cfg.get("general", "status_port", default=8080))
        srv = ThreadingHTTPServer((bind, port), H)
        threading.Thread(target=srv.serve_forever, daemon=True, name="status").start()
        log.info("pagina de stare: http://%s:%s/status", bind, port)
        return srv

    def run_forever(self, cycle_seconds: float = 2.0):
        log.info("veghe pornit: %d surse active", len(self.collectors))
        for c in self.collectors:
            log.info("  sursa %s (rol %s, la %ss)", c.name, c.role, c.interval)
        srv = self.start_status_server()
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
            srv.shutdown()
            self._pool.shutdown(wait=False)
            log.info("veghe oprit")
