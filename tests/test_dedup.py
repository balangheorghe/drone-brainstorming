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


def test_dispatcher_drops_identical_internal_message_within_hour():
    st = Store(":memory:")
    d = Dispatcher(st, [], [])
    a = Message("internal", "oficial_intern", "[INTERN] OFICIAL · 17:05 EET. RO-Alert raportat pentru: Iași.")
    b = Message("internal", "oficial_intern", "[INTERN] OFICIAL · 17:35 EET. RO-Alert raportat pentru: Iași.")
    c = Message("internal", "oficial_intern", "[INTERN] OFICIAL · 17:36 EET. RO-Alert raportat pentru: Botoșani.")
    ids = [d.submit(x) for x in (a, b, c)]
    statuses = [st.get_outbox(i)["status"] for i in ids]
    assert statuses == ["queued", "duplicat", "queued"]
    start = Message("internal", "pornire", "[INTERN] veghe pornit · 17:40 EET · 10 surse active.")
    assert st.get_outbox(d.submit(start))["status"] == "queued"
    assert st.get_outbox(d.submit(start))["status"] == "queued"                      # pornirile au regula lor
    assert dedup_key("H-3 la 17:05 EEST") == dedup_key("H-7 la 9:41")
    off = Dispatcher(Store(":memory:"), [], [], dedup_min=0)
    assert [off.store.get_outbox(off.submit(x))["status"] for x in (a, b)] == ["queued", "queued"]
