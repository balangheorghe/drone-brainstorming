"""Test complet: server HTTP local care imită toate sursele și API-ul Telegram.

Verifică: configurarea din TOML + variabile de mediu, cererile reale (antete, autentificare),
parsarea, motorul, coada, trimiterea pe Telegram, comenzile operatorului (inclusiv refuzul
celor neautorizați), aprobarea unui mesaj public, comanda check-sources și pagina de stare.
"""

import datetime as dt
import json
import pathlib
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from veghe.app import App
from veghe.config import load
from veghe.store import Store
from veghe.timeutil import UTC

FIX = pathlib.Path(__file__).parent / "fixtures"
TOKEN = "123:TESTTOKEN"


MIL_AC = [{"hex": "4b1234", "flight": "SECRET1", "t": "F16", "dbFlags": 1, "alt_baro": 20000,
           "lat": 47.5, "lon": 28.0, "seen": 1}]


def notam_wfs():
    """Un NOTAM ROMATSA real (F8021/26, zbor UAS lângă Prut), cu validitatea mutată în jurul orei curente."""
    now = dt.datetime.now(UTC).replace(second=0, microsecond=0)
    b, c = now - dt.timedelta(hours=1), now + dt.timedelta(hours=8)
    mesaj = ("(F9021/26 NOTAMN\rQ) LRBB/QWULW/IV/BO /W /000/020/4629N02802E024\r"
             f"A) LRBB B) {b:%y%m%d%H%M} C) {c:%y%m%d%H%M}\rE) NAVIGATION WARNING.\r"
             "   UNMANNED ACFT FLT WILL TAKE PLACE INTO THE FLW AREA:\r"
             "   460705N0275910E-460630N0280656E-462535N0281533E-463840N0281446E\r"
             "   464732N0280949E-465039N0280627E-465145N0275759E-462845N0280343E\r"
             "   460705N0275910E\r   EXCEPT CHISINAU FIR\rF) GND G) 2000FT AMSL)\r")
    ring = [[27.986112, 46.118056], [28.2575, 46.43], [28.24, 46.85], [27.96, 46.86], [27.986112, 46.118056]]
    return {"type": "FeatureCollection", "totalFeatures": 1, "numberMatched": 1, "numberReturned": 1, "features": [
        {"type": "Feature", "id": "restrictii_notam_pt_uav.1", "geometry": {"type": "Polygon", "coordinates": [ring]},
         "geometry_name": "the_geom", "properties": {"serie": "F9021/2026", "dfrom": b.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                                     "dto": c.strftime("%Y-%m-%dT%H:%M:%SZ"), "mesaj": mesaj, "tip": "O"}}]}


class Upstream:
    def __init__(self):
        self.sent = []
        self.headers = {}
        self.updates = []
        self.getchat = None  # (cod, corp) pentru a simula un grup greșit; implicit: supergrup privat
        self.ntfy = []
        now = dt.datetime.now(UTC)
        self.t1 = (now - dt.timedelta(minutes=4)).isoformat(timespec="seconds")
        self.t2 = (now - dt.timedelta(minutes=2)).isoformat(timespec="seconds")
        self.rfc = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    def route(self, method, path, body, headers):
        self.headers[path.split("?")[0]] = headers
        if path == "/ain/v1/alerts/active.json":
            data = json.loads((FIX / "alerts_in_ua_active.json").read_text(encoding="utf-8"))
            return 200, "application/json", json.dumps(data, ensure_ascii=False)
        if path == "/ua/api/v3/alerts/status":
            return 200, "application/json", (FIX / "ukrainealarm_status.json").read_text()
        if path == "/ua/api/v3/alerts":
            return 200, "application/json", (FIX / "ukrainealarm_alerts.json").read_text(encoding="utf-8")
        if path == "/tme/kpszsu":
            html = (FIX / "tme_kpszsu.html").read_text(encoding="utf-8")
            html = html.replace("2026-10-31T14:10:00+00:00", self.t1).replace("2026-10-31T14:20:00+00:00", self.t2)
            return 200, "text/html; charset=utf-8", html
        if path == "/rss/md":
            xml = (FIX / "feed_atom.xml").read_text(encoding="utf-8").replace("2026-10-31T15:10:00Z", self.t2)
            return 200, "application/atom+xml", xml
        if path == "/rss/ro":
            xml = (FIX / "feed_rss.xml").read_text(encoding="utf-8").replace("Sat, 31 Oct 2026 15:05:00 GMT", self.rfc)
            return 200, "application/rss+xml", xml
        if path.startswith("/adsb/v2/point/"):
            d = json.loads((FIX / "adsb_point.json").read_text())
            d["now"] = d["ctime"] = int(time.time() * 1000)  # instantaneu proaspăt (altfel „date vechi”)
            if path.startswith("/adsb/v2/point/47.1/27.6/"):  # zona militară din testele de mai jos
                d["ac"] = MIL_AC
            return 200, "application/json", json.dumps(d)
        if path == "/notam/wfs":
            return 200, "application/json", json.dumps(notam_wfs())
        if path == "/broken":
            return 200, "text/html", "<html>nu e RSS</html>"
        if path == f"/tg/bot{TOKEN}/sendMessage":
            self.sent.append(json.loads(body))
            return 200, "application/json", json.dumps({"ok": True, "result": {"message_id": len(self.sent)}})
        if path.startswith("/ntfy/"):
            self.ntfy.append(body.decode("utf-8"))
            return 200, "application/json", "{}"
        if path == f"/tg/bot{TOKEN}/getChat":
            if self.getchat:
                return self.getchat[0], "application/json", self.getchat[1]
            cid = json.loads(body)["chat_id"]
            return 200, "application/json", json.dumps({"ok": True, "result": {"id": int(cid), "type": "supergroup",
                                                                                 "title": "veghe"}})
        if path == f"/tg/bot{TOKEN}/getUpdates":
            res, self.updates = self.updates, []
            return 200, "application/json", json.dumps({"ok": True, "result": res})
        return 404, "text/plain", "nu"


@pytest.fixture()
def upstream():
    up = Upstream()

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _do(self, method):
            n = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(n) if n else b""
            code, ctype, text = up.route(method, self.path, body, dict(self.headers))
            data = text.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            self._do("GET")

        def do_POST(self):
            self._do("POST")

    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    up.base = f"http://127.0.0.1:{srv.server_address[1]}"
    yield up
    srv.shutdown()


def cycle(app):
    """Un ciclu complet: pornește sursele, așteaptă răspunsurile, le procesează."""
    app.run_cycle()
    app.drain()
    app.run_cycle()


def write_config(tmp_path, base, extra=""):
    cfg = f"""
[general]
db_path = "{tmp_path / 'veghe.db'}"
http_timeout = 5
status_bind = "127.0.0.1"
status_port = 0
[watch]
ua_oblasts = ["Одеська область", "Вінницька область", "Чернівецька область"]
ua_raions = ["Подільський район", "Ізмаїльський район"]
[sources.alerts_in_ua]
enabled = true
url = "{base}/ain/v1/alerts/active.json"
[sources.ukrainealarm]
enabled = true
base_url = "{base}/ua/api/v3"
[[sources.telegram]]
channel = "kpszsu"
role = "ua_direction"
base_url = "{base}/tme/"
[[sources.rss]]
name = "md"
url = "{base}/rss/md"
role = "md_news"
[[sources.rss]]
name = "ro"
url = "{base}/rss/ro"
role = "ro_official_news"
[sources.adsb]
enabled = true
url_template = "{base}/adsb/v2/point/{{lat}}/{{lon}}/{{radius}}"
points = [{{ name = "LUKK", lat = 46.93, lon = 28.93, radius_nm = 40 }}]
[notify]
telegram_api = "{base}/tg"
public_enabled = true
auto_publish_official = false
telegram_min_interval = 0
{extra}
"""
    p = tmp_path / "config.toml"
    p.write_text(cfg, encoding="utf-8")
    return p


@pytest.fixture()
def env(monkeypatch):
    for k, v in {"ALERTS_IN_UA_TOKEN": "ain-secret", "UKRAINEALARM_TOKEN": "ua-secret", "TELEGRAM_BOT_TOKEN": TOKEN,
                 "TELEGRAM_INTERNAL_CHAT_ID": "-1001", "TELEGRAM_PUBLIC_CHAT_ID": "-2002",
                 "TELEGRAM_OPERATOR_IDS": "42"}.items():
        monkeypatch.setenv(k, v)
    for k in ("VEGHE_STATUS_PORT", "VEGHE_STATUS_BIND", "NTFY_URL", "NTFY_TOPIC", "NTFY_TOKEN"):
        monkeypatch.delenv(k, raising=False)  # portul/adresa din config, nu din mediul dezvoltatorului


def test_full_cycle(tmp_path, upstream, env):
    app = App(load(str(write_config(tmp_path, upstream.base))))
    assert len(app.collectors) == 6
    cycle(app)

    # autentificare corectă la sursele ucrainene
    def hdr(path, name):
        return {k.lower(): v for k, v in upstream.headers[path].items()}[name]

    assert hdr("/ain/v1/alerts/active.json", "authorization") == "Bearer ain-secret"
    assert hdr("/ua/api/v3/alerts", "authorization") == "ua-secret"

    # toate sursele au răspuns
    health = {r["source"]: r for r in app.store.health()}
    assert len(health) == 6 and all(r["error_count"] == 0 for r in health.values())

    internal = [m["text"] for m in upstream.sent if m["chat_id"] == "-1001"]
    assert any("VIGILENȚĂ" in t and "Подільський район" in t for t in internal)
    assert any("DIRECȚIE" in t for t in internal)
    assert any("OFICIAL" in t and "Iași" in t for t in internal)
    assert any("Mesaj public în așteptare" in t for t in internal)
    # nimic public înainte de aprobare
    assert not [m for m in upstream.sent if m["chat_id"] == "-2002"]

    pending = app.store.outbox("pending_approval")
    assert len(pending) == 1
    oid = pending[0]["id"]

    # al doilea ciclu: nimic nou (deduplicare), nicio retrimitere
    n_before = len(upstream.sent)
    cycle(app)
    assert len(upstream.sent) == n_before

    # un neautorizat încearcă să aprobe → ignorat; operatorul 42 aprobă → se publică
    upstream.updates = [
        {"update_id": 10, "message": {"text": f"/aproba {oid}", "from": {"id": 99}, "chat": {"id": -1001}}},
        {"update_id": 11, "message": {"text": "/stare", "from": {"id": 42}, "chat": {"id": -1001}}},
        {"update_id": 12, "message": {"text": f"/aproba {oid}", "from": {"id": 42}, "chat": {"id": -1001}}},
    ]
    assert app.commands.poll_once(long_poll=0) == 2
    replies = [m["text"] for m in upstream.sent[n_before:]]
    assert any(r.startswith("Nivel:") for r in replies)
    assert any("aprobat" in r for r in replies)
    app.dispatcher.flush()
    public = [m["text"] for m in upstream.sent if m["chat_id"] == "-2002"]
    assert len(public) == 1 and public[0].startswith("[NEOFICIAL] RETRANSMITERE")
    assert app.store.kv_get("tg_offset") == "13"

    # înregistrarea manuală a unui RO-Alert (adevărul de referință pentru raport)
    reply = app.handle_command("/roalert", ["Iași", "17:04"], 42)
    assert "Înregistrat" in reply

    # pagina de stare
    st = app.status()
    assert st["nivel"] in {"direcție", "vigilență", "oficial", "Moldova", "apropiere"}
    assert app.healthy()


def test_broken_source_backs_off_and_others_continue(tmp_path, upstream, env):
    extra = ""
    p = write_config(tmp_path, upstream.base, extra)
    text = p.read_text(encoding="utf-8").replace(f'url = "{upstream.base}/rss/md"', f'url = "{upstream.base}/broken"')
    p.write_text(text, encoding="utf-8")
    app = App(load(str(p)))
    cycle(app)
    health = {r["source"]: r for r in app.store.health()}
    assert health["rss:md"]["error_count"] == 1 and "nu e un flux RSS" in health["rss:md"]["last_error"]
    assert health["telegram:kpszsu"]["error_count"] == 0
    assert app.next_due["rss:md"] > app.next_due["telegram:kpszsu"]  # pauză mai lungă după eroare


def test_check_sources_command(tmp_path, upstream, env, capsys):
    from veghe.__main__ import main

    p = write_config(tmp_path, upstream.base)
    rc = main(["--config", str(p), "check-sources"])
    out = capsys.readouterr().out
    assert rc == 0 and "6/6 surse au răspuns corect" in out
    assert "Подільський район" in out and "civil_airborne" in out


def test_status_http_endpoint(tmp_path, upstream, env):
    app = App(load(str(write_config(tmp_path, upstream.base))))
    cycle(app)
    srv = app.start_status_server()
    port = srv.server_address[1]
    body = urllib.request.urlopen(f"http://127.0.0.1:{port}/status", timeout=5).read().decode()
    assert json.loads(body)["nivel"]
    assert urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=5).status == 200
    srv.shutdown()


def test_source_down_and_recovery_are_announced(tmp_path, upstream, env):
    p = write_config(tmp_path, upstream.base)
    p.write_text(p.read_text(encoding="utf-8").replace(f'url = "{upstream.base}/rss/md"', f'url = "{upstream.base}/broken"'),
                 encoding="utf-8")
    app = App(load(str(p)))
    for _ in range(3):
        app.next_due["rss:md"] = 0
        cycle(app)
    texts = [m["text"] for m in upstream.sent]
    assert sum("SURSĂ CĂZUTĂ" in t and "rss:md" in t for t in texts) == 1  # o singură dată
    # sursa își revine
    md = next(c for c in app.collectors if c.name == "rss:md")
    md.url = f"{upstream.base}/rss/md"
    app.next_due["rss:md"] = 0
    cycle(app)
    assert any("Sursa rss:md a revenit" in m["text"] for m in upstream.sent)


def test_first_poll_does_not_act_on_undated_items(tmp_path, upstream, env):
    from veghe.models import Signal

    app = App(load(str(write_config(tmp_path, upstream.base))))
    s = Signal("rss:md", "md_news", "O dronă în raionul Telenești, Republica Moldova", dt.datetime.now(UTC))
    assert app.ingest([s], dt.datetime.now(UTC), warmup=True) == 0  # fără dată, la pornire: doar arhivat
    s2 = Signal("rss:md", "md_news", "O dronă în raionul Soroca, Republica Moldova", dt.datetime.now(UTC))
    assert app.ingest([s2], dt.datetime.now(UTC), warmup=False) > 0


def test_stuck_download_is_reported_as_source_down(tmp_path, upstream, env):
    app = App(load(str(write_config(tmp_path, upstream.base))))
    gate = threading.Event()
    md = next(c for c in app.collectors if c.name == "rss:md")
    md.poll = lambda t: gate.wait(30) and []
    app.run_cycle()
    app.started["rss:md"] -= 10_000  # simulăm o descărcare blocată de mult timp
    app.run_cycle()
    gate.set()
    assert "rss:md" in app.status()["surse_blocate"] or any(
        "SURSĂ CĂZUTĂ" in r["text"] and "rss:md" in r["text"] for r in app.store.outbox(limit=100))
    assert any("SURSĂ CĂZUTĂ" in r["text"] and "rss:md" in r["text"] for r in app.store.outbox(limit=100))


def test_untrusted_internal_group_disables_group_commands(tmp_path, upstream, env, monkeypatch):
    from veghe import notify

    monkeypatch.setattr(notify.TelegramSender, "check_private", lambda self: "chatul intern are nume public (@x)")
    app = App(load(str(write_config(tmp_path, upstream.base))), verify_private=True)
    assert [s.name for s in app.dispatcher.senders["internal"]] == ["console"]
    assert app.commands.internal_chat is None  # comenzile merg doar în chat privat cu botul


def test_zero_intervention_mode(tmp_path, upstream, monkeypatch):
    """Fără operatori, fără canal public: alertele interne (inclusiv OFICIAL din presă) vin singure,
    nimic nu așteaptă aprobare și nu e nevoie de nicio comandă."""
    for k, v in {"ALERTS_IN_UA_TOKEN": "ain-secret", "UKRAINEALARM_TOKEN": "ua-secret", "TELEGRAM_BOT_TOKEN": TOKEN,
                 "TELEGRAM_INTERNAL_CHAT_ID": "-1001"}.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setenv("TELEGRAM_PUBLIC_CHAT_ID", "-2002")  # chiar cu un canal public setat, flagul îl ține oprit
    monkeypatch.delenv("TELEGRAM_OPERATOR_IDS", raising=False)
    p = write_config(tmp_path, upstream.base)
    p.write_text(p.read_text(encoding="utf-8").replace("public_enabled = true", "public_enabled = false"), encoding="utf-8")
    app = App(load(str(p)))
    assert app.commands is None
    cycle(app)
    internal = [m["text"] for m in upstream.sent if m["chat_id"] == "-1001"]
    assert any("VIGILENȚĂ" in t for t in internal)
    assert any("OFICIAL" in t and "Iași" in t for t in internal)
    assert not any("așteptare" in t or "/aproba" in t for t in internal)
    assert not app.store.outbox("pending_approval")
    assert {m["chat_id"] for m in upstream.sent} == {"-1001"}


def test_check_sources_sends_test_message_to_internal_group(tmp_path, upstream, env, capsys):
    from veghe.__main__ import main

    rc = main(["--config", str(write_config(tmp_path, upstream.base)), "check-sources"])
    out = capsys.readouterr().out
    assert rc == 0 and "✓ telegram intern -1001" in out
    sent = [m for m in upstream.sent if m["chat_id"] == "-1001"]
    assert len(sent) == 1 and "test de livrare" in sent[0]["text"]
    assert not [m for m in upstream.sent if m["chat_id"] == "-2002"]   # nimic în canalul public


def test_check_sources_reports_wrong_internal_group(tmp_path, upstream, env, capsys):
    from veghe.__main__ import main

    upstream.getchat = (400, json.dumps({"ok": False, "error_code": 400, "description": "Bad Request: chat not found"}))
    rc = main(["--config", str(write_config(tmp_path, upstream.base)), "check-sources"])
    out = capsys.readouterr().out
    assert rc == 1 and "✗ telegram intern -1001" in out and "chat not found" in out
    assert "6/6 surse au răspuns corect" in out                       # sursele merg; livrarea nu
    assert not upstream.sent


def test_check_sources_refuses_public_group(tmp_path, upstream, env, capsys):
    from veghe.__main__ import main

    upstream.getchat = (200, json.dumps({"ok": True, "result": {"id": -1001, "type": "supergroup", "username": "public"}}))
    rc = main(["--config", str(write_config(tmp_path, upstream.base)), "check-sources"])
    out = capsys.readouterr().out
    assert rc == 1 and "nume public" in out and not upstream.sent


def test_check_sources_without_telegram_fails(tmp_path, upstream, env, monkeypatch, capsys):
    from veghe.__main__ import main

    monkeypatch.delenv("TELEGRAM_INTERNAL_CHAT_ID")
    rc = main(["--config", str(write_config(tmp_path, upstream.base)), "check-sources"])
    out = capsys.readouterr().out
    assert rc == 1 and "✗ telegram intern: TELEGRAM_BOT_TOKEN / TELEGRAM_INTERNAL_CHAT_ID lipsesc" in out


def test_wrong_internal_group_is_logged_as_critical(tmp_path, upstream, env, caplog):
    from veghe.app import build_dispatcher

    upstream.getchat = (403, json.dumps({"ok": False, "error_code": 403, "description": "Forbidden: bot was kicked"}))
    cfg = load(str(write_config(tmp_path, upstream.base)))
    with caplog.at_level("CRITICAL", logger="veghe"):
        build_dispatcher(cfg, Store(":memory:"), verify_private=True)
    assert any("INACCESIBIL" in r.message and "bot was kicked" in r.message for r in caplog.records)


def test_status_port_in_use_does_not_stop_the_service(tmp_path, upstream, env):
    import socket as so

    busy = so.socket()
    busy.bind(("127.0.0.1", 0))
    busy.listen(1)
    port = busy.getsockname()[1]
    p = write_config(tmp_path, upstream.base)
    p.write_text(p.read_text(encoding="utf-8").replace("status_port = 0", f"status_port = {port}"), encoding="utf-8")
    app = App(load(str(p)))
    try:
        assert app.start_status_server() is None
    finally:
        busy.close()


def test_run_forever_announces_start_in_internal_group(tmp_path, upstream, env, monkeypatch):
    monkeypatch.delenv("VEGHE_STATUS_PORT", raising=False)
    monkeypatch.delenv("VEGHE_STATUS_BIND", raising=False)
    app = App(load(str(write_config(tmp_path, upstream.base))))
    th = threading.Thread(target=app.run_forever, kwargs={"cycle_seconds": 0.2}, daemon=True)
    th.start()
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and not any("veghe pornit" in m["text"] for m in upstream.sent):
        time.sleep(0.1)
    app.stop.set()
    th.join(10)
    starts = [m for m in upstream.sent if "veghe pornit" in m["text"]]
    assert len(starts) == 1 and starts[0]["chat_id"] == "-1001" and not th.is_alive()


def test_check_sources_prints_each_warning_once(tmp_path, upstream, env, monkeypatch, capsys):
    from veghe.__main__ import main

    monkeypatch.delenv("TELEGRAM_OPERATOR_IDS")
    main(["--config", str(write_config(tmp_path, upstream.base)), "check-sources"])
    cap = capsys.readouterr()
    assert cap.out.count("TELEGRAM_OPERATOR_IDS gol") == 1 and "TELEGRAM_OPERATOR_IDS" not in cap.err



def test_check_sources_reports_unwritable_database(tmp_path, upstream, env, capsys):
    from veghe.__main__ import main

    (tmp_path / "fisier").write_text("x")
    p = write_config(tmp_path, upstream.base)
    p.write_text(p.read_text(encoding="utf-8").replace(f'db_path = "{tmp_path / "veghe.db"}"',
                                                       f'db_path = "{tmp_path / "fisier" / "veghe.db"}"'), encoding="utf-8")
    rc = main(["--config", str(p), "check-sources"])
    out = capsys.readouterr().out
    assert rc == 1 and "✗ baza de date" in out and "chown" in out


def test_check_sources_ntfy_only_is_not_reported_as_log_only(tmp_path, upstream, env, monkeypatch, capsys):
    from veghe.__main__ import main

    monkeypatch.delenv("TELEGRAM_INTERNAL_CHAT_ID")
    monkeypatch.setenv("NTFY_URL", f"{upstream.base}/ntfy")
    monkeypatch.setenv("NTFY_TOPIC", "veghe-test")
    rc = main(["--config", str(write_config(tmp_path, upstream.base)), "check-sources"])
    out = capsys.readouterr().out
    assert rc == 0 and "neconfigurat (alertele merg doar pe ntfy)" in out and "doar în jurnal" not in out
    assert len(upstream.ntfy) == 1 and "test de livrare" in upstream.ntfy[0]


def test_rate_limit_at_startup_is_not_critical(tmp_path, upstream, env, caplog):
    from veghe.app import build_dispatcher

    upstream.getchat = (429, json.dumps({"ok": False, "error_code": 429, "description": "Too Many Requests: retry after 5"}))
    cfg = load(str(write_config(tmp_path, upstream.base)))
    with caplog.at_level("WARNING", logger="veghe"):
        build_dispatcher(cfg, Store(":memory:"), verify_private=True)
    assert not any(r.levelname == "CRITICAL" for r in caplog.records)
    assert any("nu am putut verifica" in r.message for r in caplog.records)


def test_restarts_while_telegram_is_down_send_a_single_start_message(tmp_path, upstream, env):
    app = App(load(str(write_config(tmp_path, upstream.base))))
    for _ in range(3):  # trei porniri anterioare, nelivrate
        app.store.enqueue("internal", "pornire", "[INTERN] veghe pornit · vechi", "queued")
    th = threading.Thread(target=app.run_forever, kwargs={"cycle_seconds": 0.2}, daemon=True)
    th.start()
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and not any("veghe pornit" in m["text"] for m in upstream.sent):
        time.sleep(0.1)
    time.sleep(0.5)
    app.stop.set()
    th.join(10)
    starts = [m["text"] for m in upstream.sent if "veghe pornit" in m["text"]]
    assert len(starts) == 1 and "3 porniri anterioare nelivrate" in starts[0]


def test_check_sources_explains_filtered_feed_and_clock_skew(tmp_path, upstream, env, monkeypatch, capsys):
    import veghe.__main__ as M

    p = write_config(tmp_path, upstream.base)
    p.write_text(p.read_text(encoding="utf-8").replace('role = "md_news"', 'role = "md_news"\nkeywords = ["inexistent"]'),
                 encoding="utf-8")
    real_now = M.now
    monkeypatch.setattr(M, "now", lambda: real_now() - dt.timedelta(minutes=40))   # ceas în urmă (WSL după somn)
    M.main(["--config", str(p), "check-sources"])
    out = capsys.readouterr().out
    assert "rss:md" in out and "în flux; restul nu conțin cuvintele-cheie" in out
    assert "e cu ~40 min în urmă față de surse" in out



NEW_SOURCES = """
[[sources.notam]]
name = "romatsa"
source = "romatsa_wfs"
urls = ["{base}/notam/wfs"]
interval = 300
"""


def test_notam_and_military_reach_internal_group_only(tmp_path, upstream, env):
    extra = NEW_SOURCES.format(base=upstream.base) + (
        '\n[sources.adsb.military]\nname = "Iași 150 NM"\nlat = 47.1\nlon = 27.6\nradius_nm = 150\n')
    p = write_config(tmp_path, upstream.base, extra)
    txt = p.read_text(encoding="utf-8").replace("[sources.adsb]\n", "[sources.adsb]\nmin_request_gap_s = 0\n")
    p.write_text(txt, encoding="utf-8")
    app = App(load(str(p)))
    assert [c for c in app.collectors if c.name == "adsb"][0].military
    assert "notam:romatsa" in [c.name for c in app.collectors]
    cycle(app)
    internal = [m["text"] for m in upstream.sent if m["chat_id"] == "-1001"]
    assert any(t.startswith("[INTERN] NOTAM") and "F9021/26" in t for t in internal)
    mil = [t for t in internal if "ADS-B MILITAR" in t]
    assert len(mil) == 1 and "avion de luptă" in mil[0] and "SECRET1" not in mil[0] and "4b1234" not in mil[0]
    public = [m for m in upstream.sent if m["chat_id"] == "-2002"]
    assert not any("NOTAM" in m["text"] or "MILITAR" in m["text"] for m in public)
    # instantaneele ADS-B (civile și militare) nu se arhivează ca semnale; NOTAM-ul da
    roles = {r["role"] for r in app.store.recent_signals(200)}
    assert "notam" in roles and "adsb" not in roles and "adsb_militar" not in roles
    assert "NOTAM active: 1" in app.status_text(dt.datetime.now(UTC))
    assert app.store.adsb_samples("LUKK", dt.datetime.now(UTC) - dt.timedelta(hours=1))


def test_adsb_collector_fallback_order_and_api_key(monkeypatch):
    from veghe import collectors as C

    a = C.Adsb("https://api.adsb.lol/v2/point/{lat}/{lon}/{radius}",
               [{"name": "LRIA", "lat": 47.1, "lon": 27.6, "radius_nm": 30},
                {"name": "control", "lat": 46.6, "lon": 24.6, "radius_nm": 120}],
               fallback_templates=["https://api.airplanes.live/v2/point/{lat}/{lon}/{radius}"], api_key="k",
               control_point="control", min_request_gap_s=0)
    calls = []

    def fake_get(url, headers=None):
        calls.append((url, dict(headers or {})))
        if "adsb.lol" in url and "/47.1/" in url:
            raise OSError("jos")
        from veghe import http
        return http.Response(200, {}, json.dumps({"now": int(time.time() * 1000), "ac": []}).encode())

    a._get = fake_get
    sigs = a.poll(dt.datetime.now(UTC))
    assert [s.meta["point"] for s in sigs] == ["control", "LRIA"]           # zona de control prima
    assert calls[0][0].startswith("https://api.adsb.lol/v2/point/46.6/24.6/120") and calls[0][1]["X-API-Key"] == "k"
    assert calls[2][0].startswith("https://api.airplanes.live") and "X-API-Key" not in calls[2][1]
    assert all(s.meta["coverage"]["ok"] for s in sigs)
    a._get = lambda url, headers=None: (_ for _ in ()).throw(OSError("totul e jos"))
    with pytest.raises(OSError):
        a.poll(dt.datetime.now(UTC))


def test_adsb_unusable_answer_uses_fallback_and_blind_source_raises():
    from veghe import collectors as C
    from veghe import http

    a = C.Adsb("https://api.adsb.lol/v2/point/{lat}/{lon}/{radius}", [{"name": "LRIA", "lat": 47.1, "lon": 27.6}],
               fallback_templates=["https://api.airplanes.live/v2/point/{lat}/{lon}/{radius}"], min_request_gap_s=0,
               api_key="k", military={"lat": 47.1, "lon": 27.6})
    fresh = json.dumps({"now": int(time.time() * 1000), "ac": []}).encode()
    calls = []

    def get(url, headers=None):
        calls.append((url, dict(headers or {})))
        if "adsb.lol" in url:
            return http.Response(200, {}, b'{"error": "API key required"}')     # 200, dar fără date
        return http.Response(200, {}, fresh)

    a._get = get
    sigs = a.poll(dt.datetime.now(UTC))
    civil = [s for s in sigs if s.role == "adsb"][0]
    assert civil.meta["coverage"]["ok"] and civil.meta["sursa_date"] == "rezervă 1"
    assert "/47.1/27.6/150" in calls[-1][0]                     # zona militară implicit 150 NM, nu 30
    assert all("X-API-Key" not in h for u, h in calls if "airplanes.live" in u)
    a._get = lambda url, headers=None: http.Response(200, {}, b'{"error": "x"}')
    with pytest.raises(C.AdsbNoData):
        a.poll(dt.datetime.now(UTC))
    a2 = C.Adsb("https://adsb.lol.example.net/{lat}/{lon}/{radius}", [{"name": "p", "lat": 1, "lon": 2}], api_key="k",
                min_request_gap_s=0)
    seen = []
    a2._get = lambda url, headers=None: seen.append(dict(headers or {})) or http.Response(200, {}, fresh)
    a2.poll(dt.datetime.now(UTC))
    assert "X-API-Key" not in seen[0]                            # cheia doar spre adsb.lol real


def test_adsb_config_errors_are_clear(tmp_path, upstream, env):
    from veghe.config import ConfigError

    p = write_config(tmp_path, upstream.base, "\n[sources.adsb.military]\nlat = \"47.1\"\nlon = 27.6\n")
    with pytest.raises(ConfigError):
        App(load(str(p)))
    p = write_config(tmp_path, upstream.base)
    p.write_text(p.read_text(encoding="utf-8").replace("[sources.adsb]\n", '[sources.adsb]\ncontrol_point = "Control"\n'),
                 encoding="utf-8")
    with pytest.raises(ConfigError, match="control_point"):
        App(load(str(p)))


def test_clock_skew_checked_only_after_successful_read(tmp_path, upstream, env):
    app = App(load(str(write_config(tmp_path, upstream.base))))
    c = app.collectors[0]
    c.last_date = "Mon, 01 Jan 2024 00:00:00 GMT"              # antet vechi, de la o citire reușită de demult
    c.poll = lambda t: (_ for _ in ()).throw(OSError("jos"))
    app.next_due = {k: (0 if k == c.name else float("inf")) for k in app.next_due}
    app.run_cycle()
    app.drain()
    app.run_cycle()
    assert app.clock_skew_s is None


def test_adsb_blind_monitored_zones_raise_even_if_control_ok():
    from veghe import collectors as C
    from veghe import http

    a = C.Adsb("https://api.adsb.lol/v2/point/{lat}/{lon}/{radius}",
               [{"name": "control", "lat": 46.6, "lon": 24.6, "radius_nm": 120},
                {"name": "LRIA", "lat": 47.1, "lon": 27.6, "radius_nm": 30}], control_point="control", min_request_gap_s=0)
    fresh = json.dumps({"now": int(time.time() * 1000), "ac": [{"hex": "a1", "alt_baro": 30000, "lat": 46.6, "lon": 24.6}]}).encode()
    a._get = lambda url, headers=None: (http.Response(200, {}, fresh) if "/46.6/" in url
                                        else http.Response(200, {}, b'{"error": "x"}'))
    with pytest.raises(C.AdsbNoData):
        a.poll(dt.datetime.now(UTC))


def test_check_sources_hides_military_content(tmp_path, upstream, env, capsys):
    from veghe.__main__ import main

    p = write_config(tmp_path, upstream.base, '\n[sources.adsb.military]\nname = "Iași 150 NM"\nlat = 47.1\nlon = 27.6\nradius_nm = 150\n')
    p.write_text(p.read_text(encoding="utf-8").replace("[sources.adsb]\n", "[sources.adsb]\nmin_request_gap_s = 0\n"), encoding="utf-8")
    main(["--config", str(p), "check-sources"])
    out = capsys.readouterr()
    assert "militar: date OK, 1 aeronave" in out.out
    assert "avion de luptă" not in out.out + out.err and "km NE" not in out.out


def test_flapping_source_announced_once_per_two_hours(tmp_path, upstream, env):
    app = App(load(str(write_config(tmp_path, upstream.base))))
    c = app.collectors[0]
    t = dt.datetime.now(UTC)
    texts = []
    app._submit = lambda msgs: texts.extend(x.text for x in msgs)
    for k in range(3):                                            # cade, revine, cade din nou, de 3 ori
        app.errors[c.name] = 3
        app._source_down(c, OSError("jos"), t + dt.timedelta(minutes=20 * k))
        app.down.discard(c.name) if c.name not in app.down_announced else None
        if c.name in app.down:                                    # revenire, ca în run_cycle
            app.down.discard(c.name)
            if c.name in app.down_announced:
                app.down_announced.discard(c.name)
                texts.append("revenit")
    assert sum("SURSĂ CĂZUTĂ" in x for x in texts) == 1 and texts.count("revenit") == 1


def test_repeat_outage_after_flap_is_announced_if_it_lasts(tmp_path, upstream, env):
    app = App(load(str(write_config(tmp_path, upstream.base))))
    c = app.collectors[0]
    t = dt.datetime.now(UTC)
    texts = []
    app._submit = lambda msgs: texts.extend(x.text for x in msgs)
    app.errors[c.name] = 3
    app._source_down(c, OSError("jos"), t)                                  # anunțată
    app.down.discard(c.name)
    app.down_announced.discard(c.name)                                      # a revenit
    for k in range(0, 40, 5):                                               # cade din nou și ține
        app._source_down(c, OSError("jos"), t + dt.timedelta(minutes=30 + k))
    assert sum("SURSĂ CĂZUTĂ" in x for x in texts) == 2
