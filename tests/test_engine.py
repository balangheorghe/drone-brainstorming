"""Scenarii reale (8.09 și 31.10.2026) reluate prin motor + politica mesajelor publice."""

import datetime as dt
import pathlib
import re

import pytest

from veghe.__main__ import run_replay
from veghe.models import Message
from veghe.notify import Dispatcher, PublicPolicyError
from veghe.store import Store
from veghe.timeutil import parse_iso

SC = pathlib.Path(__file__).parent / "scenarios"
CYR = re.compile(r"[Ѐ-ӿ]")


def replay(name):
    return run_replay((SC / name).read_text(encoding="utf-8").splitlines())


def kinds(res, channel=None):
    return [m.kind for _, m in res if channel is None or m.channel == channel]


def first(res, kind):
    return next(t for t, m in res if m.kind == kind)


def test_scenario_2026_10_31():
    res = replay("2026-10-31.jsonl")
    internal = kinds(res, "internal")
    assert internal[0] == "vigilenta"
    assert internal.index("moldova") < internal.index("apropiere") < internal.index("oficial_intern")
    # prima atenție internă (16:57) vine înainte de primul RO-Alert relatat (17:05)
    assert first(res, "moldova") == parse_iso("2026-10-31T16:57:00+02:00")
    assert first(res, "moldova") < first(res, "retransmitere")
    # cele două drone = ipoteze diferite; „o altă dronă” la 5 min după „a doua” = aceeași
    hyps = {m.hypothesis for _, m in res if m.hypothesis}
    assert hyps == {1, 2}
    # câte o retransmitere publică per județ
    pub = [m for _, m in res if m.channel == "public"]
    assert [m.kind for m in pub] == ["retransmitere"] * 3
    for county in ("Iași", "Neamț", "Botoșani"):
        assert any(county in m.text for m in pub)


def test_scenario_2026_09_08():
    res = replay("2026-09-08.jsonl")
    internal = kinds(res, "internal")
    assert internal[:2] == ["directie", "vigilenta"]  # semnalele UA (16:09, 16:12) vin primele
    assert first(res, "directie") < first(res, "retransmitere")
    pub = [m for _, m in res if m.channel == "public"]
    assert [m.kind for m in pub] == ["retransmitere", "retransmitere", "incetare"]


@pytest.mark.parametrize("name", ["2026-09-08.jsonl", "2026-10-31.jsonl"])
def test_public_messages_never_contain_ukrainian_channel_content(name):
    for _, m in replay(name):
        if m.channel == "public":
            assert m.origin_role in {"ro_official_news", "manual"}
            assert not CYR.search(m.text), m.text
            assert m.text.startswith("[NEOFICIAL]")
        else:
            assert m.text.startswith("[INTERN")


def test_stale_signals_do_not_trigger():
    lines = ['{"t": "2026-10-31T18:00:00+02:00", "published_at": "2026-10-31T16:57:00+02:00", "source": "rss:x", '
             '"role": "md_news", "text": "O dronă în raionul Telenești, spațiul aerian al Republicii Moldova restricționat"}']
    assert run_replay(lines) == []


def test_unrelated_and_missile_messages_ignored():
    lines = ['{"t": "2026-10-31T16:00:00+02:00", "source": "telegram:kpszsu", "role": "ua_direction", "text": "Ракета на Одесу!"}',
             '{"t": "2026-10-31T16:01:00+02:00", "source": "telegram:kpszsu", "role": "ua_direction", "text": "БпЛА на Харківщині курсом на Полтаву"}',
             '{"t": "2026-10-31T16:02:00+02:00", "source": "rss:x", "role": "ro_official_news", "text": "Prețul pâinii crește în Iași"}']
    assert run_replay(lines) == []


def test_dispatcher_enforces_public_policy():
    st = Store(":memory:")
    d = Dispatcher(st, internal=[], public=[object()], public_enabled=True)
    with pytest.raises(PublicPolicyError):
        d.submit(Message("public", "directie", "x", origin_role="ua_direction"))
    with pytest.raises(PublicPolicyError):
        d.submit(Message("public", "retransmitere", "x", origin_role="ua_official"))
    with pytest.raises(PublicPolicyError):
        d.submit(Message("public", "vigilenta", "x", origin_role="ro_official_news"))
    oid = d.submit(Message("public", "retransmitere", "[NEOFICIAL] ok", origin_role="ro_official_news"))
    assert st.get_outbox(oid)["status"] == "pending_approval"
    assert "/aproba" in st.outbox("queued")[0]["text"]  # operatorul e anunțat intern
    assert "aprobat" in d.approve(oid, "42") and st.get_outbox(oid)["status"] == "queued"
    assert "nu poate" in d.approve(oid, "42")


def test_public_disabled_by_default_keeps_message_archived_only():
    st = Store(":memory:")
    d = Dispatcher(st, internal=[], public=[], public_enabled=True)  # fără destinatar public → oprit
    oid = d.submit(Message("public", "retransmitere", "[NEOFICIAL] ok", origin_role="ro_official_news"))
    assert st.get_outbox(oid)["status"] == "disabled"
