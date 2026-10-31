"""Teste de regresie pentru problemele găsite la revizuirea de cod (o problemă = cel puțin un test)."""

import datetime as dt
import json
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from veghe import collectors as C
from veghe import http
from veghe.__main__ import run_replay
from veghe.app import build_collectors
from veghe.config import Config, ConfigError, validate
from veghe.engine import Engine, EngineConfig
from veghe.models import Message, Signal
from veghe.nlp import analyze
from veghe.notify import Dispatcher, TelegramCommands, TelegramSender
from veghe.store import Store
from veghe.timeutil import UTC, iso, now

T0 = dt.datetime(2026, 10, 31, 15, 0, tzinfo=UTC)


def eng(**kw):
    cfg = EngineConfig(watch_oblasts=["Одеська область", "Вінницька область"],
                       watch_raions=["Подільський район", "Могилів-Подільський район"], **kw)
    return Engine(cfg, Store(":memory:"))


def sig(role, text, t, **kw):
    return Signal(source=kw.pop("source", "x"), role=role, text=text, received_at=t, published_at=kw.pop("pub", t), **kw)


# ---------------------------------------------------------------- livrare
class FlakySender:
    optional = False
    min_interval = 0

    def __init__(self, fails):
        self.name, self.fails, self.got = "flaky", fails, []

    def send(self, text):
        if self.fails > 0:
            self.fails -= 1
            raise OSError("rețea")
        self.got.append(text)


class OkConsole:
    name, optional, min_interval = "console", True, 0

    def send(self, text):
        pass


def test_internal_message_is_retried_until_telegram_gets_it():
    st = Store(":memory:")
    tg = FlakySender(fails=1)
    d = Dispatcher(st, [OkConsole(), tg], [])
    oid = d.submit(Message("internal", "x", "salut"))
    assert d.flush() == 0 and st.get_outbox(oid)["status"] == "queued"  # consola nu contează
    st.set_outbox(oid, next_attempt_at=iso(now() - dt.timedelta(seconds=1)))
    assert d.flush() == 1 and tg.got == ["salut"] and st.get_outbox(oid)["status"] == "sent"


class HttpFailSender(FlakySender):
    def send(self, text):
        raise http.HttpError(500, "eroare server")


def test_public_failure_backs_off_then_notifies_operators():
    st = Store(":memory:")
    d = Dispatcher(st, [OkConsole()], [HttpFailSender(0)], public_enabled=True, max_attempts=3)
    oid = d.submit(Message("public", "retransmitere", "[NEOFICIAL] x", origin_role="ro_official_news"))
    d.approve(oid, "42")
    for _ in range(3):
        d.flush()
        assert st.get_outbox(oid)["next_attempt_at"] or st.get_outbox(oid)["status"] == "failed"
        st.set_outbox(oid, next_attempt_at=iso(now() - dt.timedelta(seconds=1)))
    assert st.get_outbox(oid)["status"] == "failed"
    assert any("NU a putut fi trimis" in r["text"] for r in st.outbox("queued"))


def test_public_send_without_reply_is_not_retried_automatically():
    # fără răspuns de la server (timeout): mesajul poate fi deja publicat → nu-l retrimitem singuri
    st = Store(":memory:")
    d = Dispatcher(st, [OkConsole()], [FlakySender(fails=1)], public_enabled=True)
    oid = d.submit(Message("public", "retransmitere", "[NEOFICIAL] x", origin_role="ro_official_news"))
    d.approve(oid, "42")
    d.flush()
    assert st.get_outbox(oid)["status"] == "unknown"
    assert any("NECUNOSCUTĂ" in r["text"] for r in st.outbox("queued"))


def test_new_messages_are_not_starved_by_rows_waiting_for_retry():
    st = Store(":memory:")
    tg = FlakySender(fails=0)
    d = Dispatcher(st, [tg], [])
    for i in range(60):
        oid = d.submit(Message("internal", "x", f"vechi {i}"))
        st.set_outbox(oid, attempts=1, next_attempt_at=iso(now() + dt.timedelta(minutes=10)))
    d.submit(Message("internal", "apropiere", "URGENT"))
    d.flush()
    assert tg.got == ["URGENT"]


def test_approve_cannot_resurrect_an_expired_message():
    st = Store(":memory:")
    d = Dispatcher(st, [], [object()], public_enabled=True)
    oid = d.submit(Message("public", "retransmitere", "[NEOFICIAL] x", origin_role="ro_official_news"))
    st.set_outbox(oid, created_at=iso(now() - dt.timedelta(minutes=31)))  # expirat, dar încă „pending” în DB
    assert "nu poate fi aprobat" in d.approve(oid, "42")
    assert st.get_outbox(oid)["status"] == "expired"


def test_pending_public_messages_expire():
    st = Store(":memory:")
    d = Dispatcher(st, [], [object()], public_enabled=True)
    oid = d.submit(Message("public", "retransmitere", "[NEOFICIAL] x", origin_role="ro_official_news"))
    st.set_outbox(oid, created_at=iso(now() - dt.timedelta(minutes=31)))
    assert "nu poate fi aprobat" in d.approve(oid, "42")
    assert st.get_outbox(oid)["status"] == "expired"


def test_auto_publish_never_applies_to_press():
    st = Store(":memory:")
    d = Dispatcher(st, [], [object()], public_enabled=True, auto_publish_official=True)
    press = d.submit(Message("public", "retransmitere", "[NEOFICIAL] x", origin_role="ro_official_news"))
    manual = d.submit(Message("public", "retransmitere", "[NEOFICIAL] y", origin_role="manual"))
    assert st.get_outbox(press)["status"] == "pending_approval"
    assert st.get_outbox(manual)["status"] == "queued"


# ---------------------------------------------------------------- comenzi
class FakeCommands(TelegramCommands):
    def __init__(self, updates):
        super().__init__("t", {42}, lambda c, a, u, s: f"ok {c}", internal_chat_id="-100")
        self.updates, self.replies = updates, []

    def _call(self, method, payload, timeout=35):
        if method == "getUpdates":
            res, self.updates = self.updates, []
            return {"result": res}
        self.replies.append(payload)
        return {"ok": True}


def upd(i, text, uid, chat, age_s=0):
    return {"update_id": i, "message": {"text": text, "from": {"id": uid}, "chat": {"id": chat},
                                        "date": int(time.time()) - age_s}}


def test_commands_only_from_internal_group_or_private_chat_and_fresh():
    fc = FakeCommands([upd(1, "/ultimele", 42, -2002),   # canal/grup public → ignorat
                       upd(2, "/stare", 42, -100),        # grupul intern → ok
                       upd(3, "/stare", 42, 42),          # chat privat → ok
                       upd(4, "/stare", 7, -100),         # neautorizat → ignorat
                       upd(5, "/roalert Iași", 42, -100, age_s=3600)])  # veche → ignorată
    assert fc.poll_once(0) == 2
    assert {r["chat_id"] for r in fc.replies} == {-100, 42}


def test_check_private_refuses_channels_and_public_groups(monkeypatch):
    s = TelegramSender("t", "-100")
    for result, bad in [({"type": "channel"}, True), ({"type": "supergroup", "username": "x"}, True),
                        ({"type": "supergroup"}, False), ({"type": "private", "username": "ion_operator"}, False)]:
        monkeypatch.setattr(http, "request", lambda *a, r=result, **k: http.Response(200, {}, json.dumps({"result": r}).encode()))
        assert bool(s.check_private()) == bad


# ---------------------------------------------------------------- configurare
def test_config_rejects_same_internal_and_public_chat_and_bad_roles_and_types():
    with pytest.raises(ConfigError):
        validate(Config({}, {"telegram_internal_chat_id": "-1", "telegram_public_chat_id": "-1"}))
    with pytest.raises(ConfigError):
        build_collectors(Config({"sources": {"telegram": [{"channel": "x", "role": "ro_official_news"}]}}))
    with pytest.raises(ConfigError):
        build_collectors(Config({"sources": {"rss": [{"name": "x", "url": "u", "role": "ua_direction"}]}}))
    with pytest.raises(ConfigError):
        build_collectors(Config({"general": {"http_timeout": "15"}}))
    with pytest.raises(ConfigError):
        build_collectors(Config({"sources": {"telegram": {"channel": "x"}}}))  # tabel simplu, nu listă
    with pytest.raises(ConfigError):
        build_collectors(Config({"sources": {"rss": [{"name": "x"}]}}))  # fără url
    with pytest.raises(ConfigError):
        build_collectors(Config({"watch": {"ua_oblasts": "Одеська область"}}))  # text, nu listă


# ---------------------------------------------------------------- text
@pytest.mark.parametrize("text,key,present", [
    ("Drone rusești au încălcat spațiul aerian al statelor baltice", "balti", False),
    ("Marea Baltică", "balti", False),
    ("drona s-a îndreptat spre Bălți", "balti", True),
    ("deasupra Bălțiului", "balti", True),
    ("sirenele din Nisporeni", "reni", False),
    ("Ударні БпЛА на півдні Вінниччини", "vinnytsia", True),
    ("БпЛА у Чернівецькій області", "chernivtsi", True),
])
def test_place_variants(text, key, present):
    assert (key in [p.key for p in analyze(text).places]) == present


@pytest.mark.parametrize("text", ["Dronele au pătruns în raionul Soroca", "Two drones violated Moldova airspace",
                                  "UAV detected near Soroca", "мопеди на Одещину"])
def test_drone_word_forms(text):
    assert analyze(text).drone


def test_southwest_is_westward():
    assert analyze("Група БпЛА на півночі Одещини курсом на південний захід").westward


@pytest.mark.parametrize("text", ["Alerta aeriană a încetat în județul Iași", "RO-Alert: Încetare alertă aeriană în județul Iași",
                                  "Alerta a fost ridicată în județul Iași"])
def test_end_phrasings_are_end_not_new_alert(text):
    lines = [json.dumps({"t": "2026-10-31T17:00:00+02:00", "source": "rss:x", "role": "ro_official_news", "text": text})]
    kinds = [m.kind for _, m in run_replay(lines)]
    assert "incetare" in kinds and "retransmitere" not in kinds


# ---------------------------------------------------------------- motor
def test_second_alert_after_end_in_same_hour_is_not_dropped():
    e = eng()
    k = []
    for i, txt in enumerate(["RO-Alert în județul Iași: posibilă incursiune de drone",
                             "Alerta a încetat în județul Iași",
                             "RO-Alert în județul Iași: o nouă dronă, posibilă cădere de obiecte",
                             "Alerta a încetat în județul Iași"]):
        k += [m.kind for m in e.process(sig("ro_official_news", txt, T0 + dt.timedelta(minutes=15 * i)), T0 + dt.timedelta(minutes=15 * i))
              if m.channel == "public"]
    assert k == ["retransmitere", "incetare", "retransmitere", "incetare"]


def test_late_alert_article_after_end_does_not_reopen():
    e = eng()
    out = []
    for t_min, pub_min, txt in [(0, 0, "RO-Alert în județul Iași: posibilă incursiune de drone"),
                                (21, 21, "Alerta a încetat în județul Iași"),
                                (30, 5, "RO-Alert în județul Iași: posibilă incursiune de drone (articol întârziat)"),
                                (40, 22, "Alerta a încetat în județul Iași (alt articol)")]:
        t = T0 + dt.timedelta(minutes=t_min)
        out += [m.kind for m in e.process(sig("ro_official_news", txt, t, pub=T0 + dt.timedelta(minutes=pub_min)), t)
                if m.channel == "public"]
    assert out == ["retransmitere", "incetare"]


def test_mixed_end_and_new_alert_headline_goes_to_operator_only():
    e = eng()
    msgs = e.process(sig("ro_official_news", "Alerta a încetat în Vaslui, dar RO-Alert nou pentru drone în județul Iași", T0), T0)
    assert [m.channel for m in msgs] == ["internal"] and msgs[0].kind == "verificare"


def test_multiline_air_alert_post():
    e = eng()
    txt = "🔴 17:00 Повітряна тривога в Одеська область\nСлідкуйте за подальшими повідомленнями.\n#Одеська_область"
    e.process(sig("ua_alerts", txt, T0, source="telegram:air_alert_ua"), T0)
    assert "Одеська область" in e._active_titles(T0)


def test_public_text_is_a_fixed_template_without_the_headline():
    e = eng()
    s = sig("ro_official_news", "RO-Alert în județul Iași: drona venea dinspre Izmail, a zis canalul X", T0,
            url="https://www.hotnews.ro/articol")
    pub = [m for m in e.process(s, T0) if m.channel == "public"][0]
    assert "Izmail" not in pub.text and "hotnews.ro" in pub.text and "Iași" in pub.text


def test_air_alert_ua_exact_location_matching():
    e = eng()
    tg = lambda txt, t: e.process(sig("ua_alerts", txt, t, source="telegram:air_alert_ua"), t)
    tg("🔴 16:00 Повітряна тривога в Одеська територіальна громада.", T0)
    assert e._active_titles(T0) == set()  # alerta orașului Odesa nu activează regiunea
    tg("🔴 16:01 Повітряна тривога в Могилів-Подільський район.", T0)
    assert e._active_titles(T0) == {"Могилів-Подільський район"}  # nu și „Подільський район”
    tg("🔴 16:02 Повітряна тривога в Одеська область.", T0)
    tg("🟢 16:03 Відбій тривоги в Одеський район.", T0)
    assert "Одеська область" in e._active_titles(T0)  # încetarea unui raion nu oprește regiunea
    tg("🟢 16:04 Відбій тривоги в Одеська область.", T0)
    assert "Одеська область" not in e._active_titles(T0)


def test_stale_alert_state_source_is_ignored():
    e = eng(state_stale_min=10)
    e.process(Signal("alerts_in_ua", "ua_alert_state", "x", T0, meta={"active": [{"title": "Подільський район"}]}), T0)
    assert e._active_titles(T0) == {"Подільський район"}
    assert e._active_titles(T0 + dt.timedelta(minutes=11)) == set()
    e.source_alive("alerts_in_ua", T0 + dt.timedelta(minutes=11))
    assert e._active_titles(T0 + dt.timedelta(minutes=11)) == {"Подільський район"}


def test_future_timestamps_are_treated_as_now():
    e = eng()
    s = sig("md_news", "O dronă a intrat în raionul Telenești, Republica Moldova", T0, pub=T0 + dt.timedelta(hours=3))
    assert e.process(s, T0)  # nu e aruncat ca „prea vechi” și nici nu blochează ceva


def test_official_flag_only_for_nearby_hypotheses_and_kind_from_geometry():
    e = eng()
    e.process(sig("md_news", "O dronă în raionul Cahul, Republica Moldova", T0), T0)  # sud, departe de Botoșani
    e.process(sig("ro_official_news", "RO-Alert în județul Botoșani: posibilă incursiune de drone", T0), T0)
    h = e.open_hyps()[0]
    assert h.official is False


def test_second_drone_marker_never_merges_into_first():
    e = eng()
    e.process(sig("md_news", "O dronă în raionul Telenești, Republica Moldova", T0), T0)
    t = T0 + dt.timedelta(minutes=5)
    e.process(sig("md_news", "A doua dronă a intrat în raionul Soroca, Republica Moldova", t), t)
    assert len(e.open_hyps()) == 2


# ---------------------------------------------------------------- formate
def test_atom_prefers_alternate_link_and_entities_with_escaped_html():
    atom = ('<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Drona</title>'
            '<link rel="replies" href="https://x/comments"/><link rel="alternate" href="https://x/articol"/>'
            '<updated>2026-10-31T15:00:00Z</updated></entry></feed>')
    assert C.parse_feed(atom)[0]["link"] == "https://x/articol"
    rss = ('<rss><channel><item><title>A&nbsp;B</title>'
           '<description>&lt;p&gt;dronă &amp; spațiu aerian&lt;/p&gt;</description></item></channel></rss>')
    it = C.parse_feed(rss)[0]
    assert it["title"] == "A B" and it["summary"] == "dronă & spațiu aerian"


def test_feed_encoding_from_prolog_and_naive_dates_are_local_time():
    xml = ('<?xml version="1.0" encoding="windows-1251"?><rss><channel><item><title>Дрон</title>'
           '<pubDate>2026-10-31T17:04:00</pubDate></item></channel></rss>').encode("cp1251")
    it = C.parse_feed(xml)[0]
    assert it["title"] == "Дрон"
    assert it["published_at"] == dt.datetime(2026, 10, 31, 15, 4, tzinfo=UTC)  # 17:04 EET = 15:04 UTC
    assert C._parse_date("Sat, 31 Oct 2026 17:04:00 EET") == dt.datetime(2026, 10, 31, 15, 4, tzinfo=UTC)
    assert C._parse_date("Sat, 31 Oct 2026 15:00:00 -0000") == dt.datetime(2026, 10, 31, 15, 0, tzinfo=UTC)
    assert C._parse_date("Sat, 31 Oct 2026 16:00:00 CET") == dt.datetime(2026, 10, 31, 15, 0, tzinfo=UTC)
    # în jurul schimbării orei (ora României, fără fus în text)
    assert C._parse_date("2026-03-29T01:30:00") == dt.datetime(2026, 3, 28, 23, 30, tzinfo=UTC)
    assert C._parse_date("2026-10-25T02:30:00") == dt.datetime(2026, 10, 24, 23, 30, tzinfo=UTC)


def test_feed_charset_only_in_http_header():
    class F(C.Feed):
        def _get(self, url, headers=None):
            body = "<rss><channel><item><title>RO-Alert în judeţul Iaşi: dronă</title></item></channel></rss>"
            return http.Response(200, {"content-type": "application/rss+xml; charset=iso-8859-2"}, body.encode("iso-8859-2"))

    sigs = F("x", "http://h/rss", "ro_official_news").poll(T0)
    assert sigs[0].text == "RO-Alert în judeţul Iaşi: dronă"  # ISO-8859-2 are doar ş/ţ cu sedilă


def test_tme_service_messages_skipped_and_edits_get_new_key():
    page = ('<section class="tgme_channel_history">'
            '<div class="tgme_widget_message service_message" data-post="c/1"><div class="tgme_widget_message_bubble">'
            '<div class="tgme_widget_message_text">Channel photo updated</div></div></div>'
            '<div class="tgme_widget_message" data-post="c/2"><div class="tgme_widget_message_bubble">'
            '<div class="tgme_widget_message_text">БпЛА курсом на Подільськ</div></div></div></section>')
    assert [p["post"] for p in C.parse_tme(page)] == ["c/2"]

    class T(C.TelegramWeb):
        def __init__(self, html):
            super().__init__("c", "ua_direction")
            self.html = html

        def _get(self, url, headers=None):
            return http.Response(200, {}, self.html.encode())

    k1 = T(page).poll(T0)[0].key()
    k2 = T(page.replace("Подільськ", "Подільськ та Молдову")).poll(T0)[0].key()
    assert k1 != k2


def test_alerts_in_ua_keeps_last_modified_only_after_successful_parse():
    class A(C.AlertsInUA):
        def __init__(self, bodies):
            super().__init__("t", "u", ["Одеська область"], ["Подільський район"])
            self.bodies, self.sent = bodies, []

        def _get(self, url, headers=None):
            self.sent.append(dict(headers or {}))
            return http.Response(200, {"last-modified": "X"}, self.bodies.pop(0))

    a = A([b"<html>eroare</html>", json.dumps({"alerts": []}).encode()])
    with pytest.raises(ValueError):
        a.poll(T0)
    a.poll(T0)
    assert "If-Modified-Since" not in a.sent[1]


def test_adsb_radius_is_integer_in_url():
    a = C.Adsb("http://h/{lat}/{lon}/{radius}", [{"name": "p", "lat": 1, "lon": 2, "radius_nm": 40.0}])
    urls = []
    a._get = lambda url, headers=None: urls.append(url) or http.Response(200, {}, b'{"ac": []}')
    a.poll(T0)
    assert urls == ["http://h/1/2/40"]


# ---------------------------------------------------------------- robustețe
def test_strip_html_is_linear_on_hostile_input():
    t = time.monotonic()
    C._strip_html("<" * 200_000)
    assert time.monotonic() - t < 2


def test_http_total_deadline_against_trickling_server():
    class Slow(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            try:
                for _ in range(40):
                    self.wfile.write(b"x" * 70000)
                    self.wfile.flush()
                    time.sleep(0.3)
            except (BrokenPipeError, ConnectionResetError, socket.error):
                pass

    srv = ThreadingHTTPServer(("127.0.0.1", 0), Slow)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    t = time.monotonic()
    with pytest.raises(http.HttpError):
        http.request(f"http://127.0.0.1:{srv.server_address[1]}/", timeout=1, max_bytes=50_000_000)
    assert time.monotonic() - t < 4
    srv.shutdown()


def test_report_finds_roalert_logged_hours_later(tmp_path, capsys):
    from veghe.__main__ import main
    from veghe.iso_helpers import manual_roalert_signal

    db = tmp_path / "v.db"
    (tmp_path / "c.toml").write_text(f'[general]\ndb_path = "{db}"\n', encoding="utf-8")
    st = Store(str(db))
    st.add_event(3, 1, "moldova", "x", T0)                       # 15:00 UTC
    s = manual_roalert_signal("Iași", T0 + dt.timedelta(minutes=8), "operator:42")
    s.received_at = T0 + dt.timedelta(hours=5)                   # înregistrat abia seara
    st.add_signal(s)
    main(["--config", str(tmp_path / "c.toml"), "report", "--since", iso(T0 - dt.timedelta(minutes=30)),
          "--to", iso(T0 + dt.timedelta(minutes=60))])
    out = capsys.readouterr().out
    assert "neînregistrat" not in out and "+8 min" in out
