"""Fără mesaje repetate: VIGILENȚĂ pe episod, ipoteze doar la apropiere reală, surse intermitente,
filtrul de dubluri din livrare și continuitatea după repornire."""

import datetime as dt

from veghe.engine import Engine, EngineConfig
from veghe.models import Message, Signal
from veghe.notify import Dispatcher, dedup_key
from veghe.store import Store
from veghe.timeutil import UTC

T0 = dt.datetime(2026, 11, 3, 20, 0, tzinfo=UTC)
CFG = dict(watch_oblasts=["Одеська область"], watch_raions=["Подільський район", "Ізмаїльський район"])


def eng(store=None):
    return Engine(EngineConfig(**CFG), store)


def state(e, t, *titles):
    act = [{"title": x, "type": "raion", "oblast": "Одеська область"} for x in titles]
    return e.process(Signal(source="alerts_in_ua", role="ua_alert_state", text="", received_at=t, meta={"active": act}), t)


def m(minutes):
    return T0 + dt.timedelta(minutes=minutes)


def test_flickering_alert_gives_one_vigilance_per_episode():
    e = eng()
    sent = []
    for k in range(0, 120, 5):                          # alerta pornește și se oprește la 5 min, 2 ore
        sent += state(e, m(k), "Ізмаїльський район") if (k // 5) % 2 == 0 else state(e, m(k))
        sent += e.tick(m(k))
    assert len([x for x in sent if x.kind == "vigilenta"]) == 1
    # după 30 min fără alerte episodul se încheie; o alertă nouă e un episod nou
    for k in range(120, 160, 5):
        state(e, m(k))
        e.tick(m(k))
    assert e.vigilance_since is None
    assert len([x for x in state(e, m(161), "Ізмаїльський район") if x.kind == "vigilenta"]) == 1


def test_vigilance_update_only_when_alert_moves_much_closer():
    e = eng()
    assert len(state(e, m(0), "Подільський район")) == 1                         # ~159 km de Iași
    assert state(e, m(25), "Подільський район", "Ізмаїльський район") == []       # Izmail e mai departe (~222 km)
    e2 = eng()
    assert len(state(e2, m(0), "Ізмаїльський район")) == 1
    msgs = state(e2, m(30), "Ізмаїльський район", "Подільський район")            # Podilsk: mult mai aproape
    assert len(msgs) == 1 and "mai aproape de Iași" in msgs[0].text
    assert state(e2, m(35), "Подільський район") == []


def test_vigilance_continues_after_restart(tmp_path):
    from veghe.timeutil import now as real_now

    t = real_now()
    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    assert len(state(e, t, "Ізмаїльський район")) == 1
    e2 = eng(st)                                                    # repornire în timpul alertei
    assert e2.tick(t + dt.timedelta(minutes=2)) == []
    assert state(e2, t + dt.timedelta(minutes=3), "Ізмаїльський район") == []


def direction(e, t, text):
    return e.process(Signal(source="telegram:kpszsu", role="ua_direction", text=text, received_at=t, published_at=t), t)


def test_same_drone_reported_by_several_posts_is_announced_once():
    e = eng()
    first = direction(e, m(0), "БпЛА на Одещині курсом на Ізмаїл")
    assert len(first) == 1
    # alte postări despre același grup, localități apropiate sau aceeași: fără mesaje noi
    assert direction(e, m(4), "БпЛА на Одещині курсом на Рені") == []
    assert direction(e, m(15), "БпЛА на Одещині курсом на Ізмаїл") == []
    assert direction(e, m(30), "Група БпЛА курсом на Ізмаїл") == []


def test_hypothesis_update_when_drone_gets_much_closer():
    e = eng()
    assert len(direction(e, m(0), "БпЛА на Одещині курсом на Ізмаїл")) == 1
    msgs = direction(e, m(12), "БпЛА курсом на Подільськ")                         # mult mai aproape de Iași
    assert len(msgs) == 1


def test_dispatcher_drops_identical_internal_message_within_minutes():
    st = Store(":memory:")
    d = Dispatcher(st, [], [])
    a = Message("internal", "sursa_cazuta", "[INTERN] SURSĂ CĂZUTĂ · 17:05 EET. rss:x nu răspunde (URLError, 3 erori la rând).")
    b = Message("internal", "sursa_cazuta", "[INTERN] SURSĂ CĂZUTĂ · 17:08 EET. rss:x nu răspunde (URLError, 3 erori la rând).")
    c = Message("internal", "sursa_cazuta", "[INTERN] SURSĂ CĂZUTĂ · 17:09 EET. rss:y nu răspunde (URLError, 3 erori la rând).")
    statuses = [st.get_outbox(d.submit(x))["status"] for x in (a, b, c)]
    assert statuses == ["queued", "duplicat", "queued"]
    start = Message("internal", "pornire", "[INTERN] veghe pornit · 17:40 EET · 10 surse active.")
    assert [st.get_outbox(d.submit(start))["status"] for _ in range(2)] == ["queued", "queued"]
    # RO-Alert nou după o încetare: același text, dar alertă nouă → trece mereu
    ro = Message("internal", "oficial_intern", "[INTERN] OFICIAL · 17:05 EET. RO-Alert raportat pentru: Iași (operator).")
    assert [st.get_outbox(d.submit(ro))["status"] for _ in range(2)] == ["queued", "queued"]
    assert dedup_key("H-3 la 17:05 EEST") != dedup_key("H-7 la 9:41")       # ipoteze diferite = mesaje diferite
    off = Dispatcher(Store(":memory:"), [], [], dedup_min=0)
    assert [off.store.get_outbox(off.submit(x))["status"] for x in (a, b)] == ["queued", "queued"]


def test_duplicate_is_sent_if_original_fails():
    class Down:
        name, min_interval, optional = "telegram:-1", 0, False

        def send(self, text):
            raise OSError("jos")

    st = Store(":memory:")
    d = Dispatcher(st, [Down()], [], max_attempts=1)
    a = Message("internal", "sursa_cazuta", "[INTERN] SURSĂ CĂZUTĂ · 17:05 EET. rss:x nu răspunde.")
    i1 = d.submit(a)
    i2 = d.submit(a)
    assert st.get_outbox(i2)["status"] == "duplicat"
    d.flush()                                                     # originalul eșuează definitiv
    assert st.get_outbox(i1)["status"] == "failed" and st.get_outbox(i2)["status"] == "queued"


def md(e, t, text):
    return e.process(Signal(source="rss:md", role="md_news", text=text, received_at=t, published_at=t), t)


def test_closer_position_inside_pause_is_sent_later_not_lost():
    e = eng()
    assert len(md(e, m(0), "O dronă a intrat în R. Moldova, a fost observată la Nisporeni, spre vest")) == 1
    assert md(e, m(4), "Drona a fost observată deasupra orașului Ungheni") != [] or \
        any("Ungheni" in x.text for x in e.tick(m(10)))
    e2 = eng()
    md(e2, m(0), "Dronă semnalată în R. Moldova, poziție necunoscută")
    msgs = md(e2, m(6), "Drona survolează raionul Soroca")       # prima poziție: imediat
    assert len(msgs) == 1 and "Soroca" in msgs[0].text


def test_second_drone_phrasings_create_new_hypothesis():
    e = eng()
    assert len(md(e, m(0), "Dronă semnalată în R. Moldova la Edineț, spre vest")) == 1
    msgs = md(e, m(3), "Încă un UAV a fost observat lângă Ocnița")
    assert len(msgs) == 1 and "H-2" in msgs[0].text
    for text in ("Un nou aparat de zbor fără pilot a intrat în spațiul aerian, în raionul Soroca",
                 "Ще одна група БпЛА зайшла в повітряний простір Молдови біля Сорок",
                 "Another drone entered Moldovan airspace near Soroca"):
        e2 = eng()
        md(e2, m(0), "Dronă semnalată în R. Moldova la Edineț, spre vest")
        msgs = md(e2, m(3), text)
        assert len(msgs) == 1 and "H-2" in msgs[0].text, text


def test_lost_from_radar_is_reported_once():
    e = eng()
    md(e, m(0), "Dronă semnalată în R. Moldova la Telenești, spre vest")
    msgs = md(e, m(6), "UPDATE: Drona a dispărut de pe radar lângă Țibirica")
    assert len(msgs) == 1
    assert md(e, m(8), "Drona a dispărut de pe radar lângă Țibirica, confirmă MApN") == []


def test_merged_report_after_long_silence_is_sent():
    e = eng()
    md(e, m(0), "Dronă la Ungheni, spre vest")
    assert md(e, m(30), "Dronă semnalată la Soroca") != []                 # ultimul mesaj e vechi, alt loc


def test_hypotheses_and_official_state_survive_restart(tmp_path):
    from veghe.timeutil import now as real_now

    t = real_now()
    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    assert len(direction(e, t, "БпЛА на Одещині курсом на Ізмаїл")) == 1
    ro = Signal(source="rss:ro", role="ro_official_news", received_at=t, published_at=t,
                text="RO-Alert în județul Iași: posibilă incursiune de drone", url="https://x.ro/a")
    assert any(x.kind == "oficial_intern" for x in e.process(ro, t))
    e2 = eng(st)
    assert direction(e2, t + dt.timedelta(minutes=5), "Група БпЛА курсом на Ізмаїл") == []
    ro2 = Signal(source="rss:ro2", role="ro_official_news", received_at=t + dt.timedelta(minutes=6),
                 published_at=t + dt.timedelta(minutes=6), url="https://y.ro/b",
                 text="RO-Alert în județul Iași după o incursiune de drone")
    assert not any(x.kind == "oficial_intern" for x in e2.process(ro2, t + dt.timedelta(minutes=6)))


def test_long_vigilance_survives_restart(tmp_path):
    from veghe.timeutil import now as real_now

    t = real_now() - dt.timedelta(minutes=75)
    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    for k in range(0, 76, 3):
        state(e, t + dt.timedelta(minutes=k), "Ізмаїльський район")
    e2 = eng(st)
    now2 = t + dt.timedelta(minutes=76)
    assert e2.tick(now2) == []
    assert state(e2, now2 + dt.timedelta(minutes=1), "Ізмаїльський район") == []
