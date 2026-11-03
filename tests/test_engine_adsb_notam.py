"""Regulile motorului pentru ADS-B (analiză civilă, militari) și NOTAM, cu meta construită
exact în forma întoarsă de veghe.adsb_analysis / veghe.adsb_military / veghe.notam."""

import datetime as dt
import json
import pathlib

from veghe import adsb_military as AM
from veghe.engine import Engine, EngineConfig
from veghe.models import Signal
from veghe.store import Store
from veghe.timeutil import UTC, iso

import pytest

from veghe import timeutil

T0 = dt.datetime(2026, 11, 3, 15, 0, tzinfo=UTC)


@pytest.fixture(autouse=True)
def _clock(monkeypatch):
    """Repornirea citește ceasul real (timeutil.now); aici e fixat lângă T0, ca testele să nu depindă de data rulării."""
    monkeypatch.setattr(timeutil, "now", lambda: T0 + dt.timedelta(minutes=5))


def eng(store=None):
    return Engine(EngineConfig(watch_oblasts=["Одеська область"], watch_raions=["Подільський район"]), store)


def adsb_meta(point="LRIA Iași", **kw):
    m = {"point": point, "civil_airborne": 5, "civil_total": 6, "civil_gps_lost": 0, "civil_mlat": 0, "civil_unplaced": 0,
         "gnss": {"n": 6, "degraded": 0, "lost": 0, "ratio": 0.0, "level": "normal", "interference": False,
                  "changed": False, "since": None, "scope": None, "baseline_ready": True},
         "emergencies": [], "holding": 0, "holding_recent": 0, "turnbacks": 0, "maneuver_aircraft": 0,
         "maneuver_alert": False, "maneuvers": [],
         "coverage": {"ok": True, "reason": "ok", "data_age_s": 1.0, "median_seen_pos_s": 1.0},
         "drop": {"real": False, "suspected_outage": False, "zero_streak": 0, "baseline": 5.0, "control_ok": True},
         "is_control": False}
    for k, v in kw.items():
        if isinstance(v, dict) and isinstance(m.get(k), dict):
            m[k] = {**m[k], **v}
        else:
            m[k] = v
    return m


def sig(meta, t=T0, role="adsb", text="x"):
    return Signal(source="adsb", role=role, text=text, received_at=t, meta=meta)


def vigilance(e, t=T0):
    e.process(Signal(source="alerts_in_ua", role="ua_alert_state", text="", received_at=t,
                     meta={"active": [{"title": "Подільський район", "type": "raion", "oblast": "Одеська область"}]}), t)


# ------------------------------------------------------------------ ADS-B civil
def test_emergency_is_always_announced_once_without_identity():
    e = eng()
    em = {"code": "7700", "meaning": "urgență generală (adesea medicală)", "dist_km": 22.0, "bearing": "NE",
          "alt_ft": 24000, "category": "A3", "new": True}
    msgs = e.process(sig(adsb_meta(emergencies=[em])), T0)
    assert len(msgs) == 1 and "URGENȚĂ 7700" in msgs[0].text and "~22 km NE de LRIA Iași" in msgs[0].text
    assert msgs[0].channel == "internal"
    # aceeași urgență (new=False) sau alt anunț în 10 min: nimic
    assert e.process(sig(adsb_meta(emergencies=[{**em, "new": False}]), T0 + dt.timedelta(minutes=1)), T0) == []
    assert e.process(sig(adsb_meta(emergencies=[em]), T0 + dt.timedelta(minutes=5)), T0 + dt.timedelta(minutes=5)) == []


def test_gnss_needs_baseline_then_announces_start_and_end():
    e = eng()
    on = {"n": 9, "degraded": 4, "lost": 2, "ratio": 0.33, "level": "ridicat", "interference": True, "changed": True,
          "scope": "local"}
    assert e.process(sig(adsb_meta(gnss={**on, "baseline_ready": False})), T0) == []   # primele 3 zile: doar învățăm
    msgs = e.process(sig(adsb_meta(gnss=on)), T0 + dt.timedelta(minutes=40))
    assert len(msgs) == 1 and "4 din 9 aeronave civile" in msgs[0].text and "Posibil bruiaj GNSS local" in msgs[0].text
    off = {"n": 9, "degraded": 0, "lost": 0, "ratio": 0.0, "level": "normal", "interference": False, "changed": True}
    msgs = e.process(sig(adsb_meta(gnss=off)), T0 + dt.timedelta(minutes=60))
    assert len(msgs) == 1 and "a revenit la normal" in msgs[0].text
    # încheiere fără început anunțat: nimic
    assert e.process(sig(adsb_meta(gnss=off)), T0 + dt.timedelta(minutes=70)) == []


def test_maneuvers_need_vigilance_unless_three_aircraft():
    e = eng()
    man = [{"kind": "asteptare", "dist_km": 28.0, "bearing": "N", "alt_ft": 9000},
           {"kind": "intoarcere", "dist_km": 35.0, "bearing": "E", "alt_ft": 35000}]
    m = adsb_meta(holding_recent=1, turnbacks=1, maneuver_aircraft=2, maneuver_alert=True, maneuvers=man)
    assert e.process(sig(m), T0) == []                                  # fără vigilență: 2 aeronave nu ajung
    vigilance(e)
    msgs = e.process(sig(m), T0 + dt.timedelta(minutes=1))
    assert len(msgs) == 1 and "1 aeronave civile în așteptare și 1 întoarceri" in msgs[0].text
    assert "așteptare ~28 km N, ~9000 ft" in msgs[0].text
    # în 20 min nu se repetă, decât dacă cresc cu ≥ 2
    assert e.process(sig(m), T0 + dt.timedelta(minutes=5)) == []
    m4 = adsb_meta(holding_recent=3, turnbacks=1, maneuver_aircraft=4, maneuver_alert=True, maneuvers=man)
    assert len(e.process(sig(m4), T0 + dt.timedelta(minutes=6))) == 1
    e2 = eng()
    m3 = adsb_meta(holding_recent=3, maneuver_aircraft=3, maneuver_alert=True, maneuvers=man)
    assert len(e2.process(sig(m3), T0)) == 1                             # ≥ 3 aeronave: chiar și fără vigilență


def test_real_drop_and_detour_announced_only_during_vigilance():
    e = eng()
    vigilance(e)
    drop = adsb_meta(civil_airborne=0, drop={"real": True, "baseline": 6.0})
    msgs = e.process(sig(drop), T0)
    assert len(msgs) == 1 and "de la ~6 la 0" in msgs[0].text
    # ocolire: trafic mult sub fond (nu zero) în 3 citiri la rând
    e2 = eng()
    vigilance(e2)
    low = adsb_meta(civil_airborne=1, drop={"real": False, "baseline": 8.0, "control_ok": True})
    assert e2.process(sig(low), T0) == [] and e2.process(sig(low), T0) == []
    msgs = e2.process(sig(low), T0)
    assert len(msgs) == 1 and "Trafic civil mult redus" in msgs[0].text and "ocolire" in msgs[0].text
    assert "ocolit" in e2._adsb_note()
    # fără vigilență: doar eveniment, fără mesaj
    e3 = eng()
    for _ in range(3):
        assert e3.process(sig(low), T0) == []
    assert e3.adsb_reduced["LRIA Iași"]


def test_outage_never_alerts_and_control_area_is_silent():
    e = eng()
    vigilance(e)
    out = adsb_meta(civil_airborne=0, coverage={"ok": False, "reason": "date_vechi"},
                    drop={"real": False, "suspected_outage": True, "baseline": 6.0})
    for _ in range(4):
        assert e.process(sig(out), T0) == []
    ctrl = adsb_meta(point="control", is_control=True, civil_airborne=0, drop={"real": True},
                     emergencies=[{"code": "7700", "new": True, "dist_km": 1.0, "bearing": "N"}])
    assert e.process(sig(ctrl), T0) == []


def test_samples_stored_only_with_good_coverage(tmp_path):
    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    e.process(sig(adsb_meta(civil_airborne=3, civil_gps_lost=1)), T0)
    e.process(sig(adsb_meta(coverage={"ok": False, "reason": "fara_db"})), T0 + dt.timedelta(minutes=1))
    rows = st.adsb_samples("LRIA Iași", T0 - dt.timedelta(hours=1))
    assert [r["civil_airborne"] for r in rows] == [4]                 # în aer + fără GPS; „fara_db” nu se păstrează
    p90, days = st.adsb_gnss_baseline("LRIA Iași", T0 + dt.timedelta(minutes=2))
    assert p90 == 0.0 and days == 0.0


# ------------------------------------------------------------------ militari
MIL = {"now": 1793728800000, "ac": [
    {"hex": "4b1234", "flight": "SECRET1", "r": "16-0001", "t": "F16", "dbFlags": 1, "alt_baro": 20000,
     "lat": 47.5, "lon": 28.0, "seen": 1},
    {"hex": "4b1235", "flight": "SECRET2", "t": "E3TF", "dbFlags": 1, "alt_baro": 30000, "lat": 46.5, "lon": 27.0, "seen": 1},
    {"hex": "4b1236", "flight": "SECRET3", "t": "C130", "dbFlags": 1, "alt_baro": "ground", "lat": 47.1, "lon": 27.6},
    {"hex": "4b1237", "flight": "FAR", "t": "F16", "dbFlags": 1, "alt_baro": 20000, "lat": 52.0, "lon": 21.0, "seen": 1},
    {"hex": "abc123", "flight": "ROT123", "t": "A320", "dbFlags": 0, "alt_baro": 35000, "lat": 47.0, "lon": 27.5},
]}


def test_military_summary_groups_without_identities():
    s = AM.summary(MIL, "Iași 150 NM", 47.1, 27.6, 150)
    assert s["n"] == 2 and s["grupuri"] == {"avion de luptă": 1, "avion radar/recunoaștere": 1}
    dump = json.dumps(s)
    for ident in ("4b1234", "SECRET1", "16-0001", "F16", "E3TF", "abc123", "ROT123"):
        assert ident not in dump
    assert all(d["dist_km"] % 10 == 0 for d in s["detalii"])
    assert AM.group_of({"category": "A7"}) == AM.ELICOPTER and AM.group_of({"t": "XXXX"}) == AM.ALTUL
    assert AM.group_of({"desc": "LOCKHEED MARTIN F-35A Lightning II"}) == AM.LUPTA


def test_military_message_on_fighters_only_rate_limited_internal():
    e = eng()
    s = AM.summary(MIL, "Iași 150 NM", 47.1, 27.6, 150)
    msgs = e.process(sig(s, role="adsb_militar"), T0)
    assert len(msgs) == 1 and msgs[0].channel == "internal" and "NU REDISTRIBUIȚI" in msgs[0].text
    assert "1 × avion de luptă" in msgs[0].text and "SECRET" not in msgs[0].text and "4b12" not in msgs[0].text
    assert e.process(sig(s, role="adsb_militar"), T0 + dt.timedelta(minutes=1)) == []    # același număr
    only_awacs = {**s, "grupuri": {"avion radar/recunoaștere": 1}, "n": 1}
    assert e.process(sig(only_awacs, role="adsb_militar"), T0 + dt.timedelta(minutes=30)) == []  # doar context
    assert e.status(T0 + dt.timedelta(minutes=30))["militar"]["trigger"] == 0
    # pâlpâire: o absență scurtă nu face din reapariție un mesaj nou
    assert e.process(sig(s, role="adsb_militar"), T0 + dt.timedelta(minutes=31)) == []
    for k in range(10):                                                                   # absență susținută ≥ 20 min
        e.process(sig(only_awacs, role="adsb_militar"), T0 + dt.timedelta(minutes=32 + 3 * k))
    msgs = e.process(sig(s, role="adsb_militar"), T0 + dt.timedelta(minutes=63))
    assert len(msgs) == 1
    # date indisponibile: starea veche nu mai e folosită
    e.process(sig({"ok": False}, role="adsb_militar"), T0 + dt.timedelta(minutes=64))
    assert e.military is None and e.status(T0 + dt.timedelta(minutes=64))["militar"] is None


def test_military_flicker_does_not_spam():
    e = eng()
    s = AM.summary(MIL, "Iași 150 NM", 47.1, 27.6, 150)
    two = {**s, "grupuri": {"avion de luptă": 2}, "n": 2}
    none = {**s, "grupuri": {}, "n": 0}
    sent = 0
    for k in range(11):                                   # 2 avioane apar și dispar la fiecare 2 min, 20 min
        sent += len(e.process(sig(two if k % 2 == 0 else none, role="adsb_militar"), T0 + dt.timedelta(minutes=2 * k)))
    assert sent == 1


def test_military_note_has_no_positions_and_expires():
    e = eng()
    e.process(sig(AM.summary(MIL, "Iași 150 NM", 47.1, 27.6, 150), role="adsb_militar"), T0)
    note = e._adsb_note(T0 + dt.timedelta(minutes=1))
    assert "NU REDISTRIBUIȚI" in note and "1 × avion de luptă" in note and "km" not in note
    assert "militar" not in e._adsb_note(T0 + dt.timedelta(minutes=10))


# ------------------------------------------------------------------ NOTAM
def notam_meta(**kw):
    m = {"id": "F8021/26", "key": "LR:F8021/26", "kind": "nou", "replaces": None, "fir": "LRBB", "qcode": "QRTCA",
         "category": "spatiu_aerian_inchis", "uas": False, "near": True, "locations": ["LRBB"],
         "start": iso(T0 - dt.timedelta(hours=1)), "end": iso(T0 + dt.timedelta(hours=8)), "estimated": False,
         "dist_iasi_km": 42.8, "dist_prut_km": 0.0, "ends": None, "ends_key": None, "continua": None}
    m.update(kw)
    return m


def nsig(meta, t=T0, text=None):
    return Signal(source="notam:romatsa", role="notam", received_at=t, published_at=t, ext_id=f"{meta['key']}|{meta['kind']}",
                  text=text or f"NOTAM {meta['id']} · spațiu aerian închis ({meta.get('qcode')}) · LRBB", meta=meta)


def test_notam_near_closure_announced_routine_ones_only_in_status():
    e = eng()
    msgs = e.process(nsig(notam_meta()), T0)
    assert len(msgs) == 1 and msgs[0].text.startswith("[INTERN] NOTAM") and "F8021/26" in msgs[0].text
    assert "nu confirmă o dronă" in msgs[0].text
    routine = [
        notam_meta(id="F9001/26", key="LR:F9001/26", category="drone_uas", uas=True, qcode="QWULW"),       # zboruri UAS planificate
        notam_meta(id="P2397/26", key="LR:P2397/26", category="restrictie_spatiu_aerian", qcode="QRDCA"),  # activare militară
        notam_meta(id="P2578/26", key="LR:P2578/26", category="restrictie_spatiu_aerian", uas=True, qcode="QRTCA",
                   near=False, end=iso(T0 + dt.timedelta(days=28))),                                       # zona lunară de la graniță
        notam_meta(id="G1/26", key="LR:G1/26", category="gnss", qcode="QGWXX"),                            # avertizare GNSS
    ]
    sent = []
    for k, r in enumerate(routine):
        sent += e.process(nsig(r), T0 + dt.timedelta(minutes=20 + k))
    assert {"F9001/26", "P2397/26", "G1/26"} <= {n["id"] for n in e.status(T0)["notam_active"]}   # vizibile în /stare
    sent += [x for k in range(1, 60) for x in e.tick(T0 + dt.timedelta(hours=k))]
    assert not [x for x in sent if "F9001" in x.text or "P2397" in x.text or "P2578" in x.text or "G1/26" in x.text]


def test_notam_moldova_restriction_is_announced():
    e = eng()
    md = notam_meta(id="A0200/26", key="LU:A0200/26", fir="LUUU", category="restrictie_spatiu_aerian", near=False,
                    qcode="QRTCA", locations=["LUUU"])
    assert len(e.process(nsig(md), T0)) == 1


def test_notam_moldova_closure_is_attention_and_merged_within_10_min():
    e = eng()
    e.process(nsig(notam_meta()), T0)
    md = notam_meta(id="A0123/26", key="LU:A0123/26", fir="LUUU", category="spatiu_aerian_inchis", near=False,
                    uas=False, qcode="QAFLC", locations=["LUUU"])
    assert e.process(nsig(md, text="NOTAM A0123/26 · spațiu aerian închis · LUUU"), T0 + dt.timedelta(minutes=2)) == []
    msgs = e.tick(T0 + dt.timedelta(minutes=11))
    assert len(msgs) == 1 and "ATENȚIE" in msgs[0].text and "NOTAM R. Moldova: spațiu aerian închis" in msgs[0].text
    assert "NOTAM activ" in e._adsb_note()


def test_notam_cancel_expiry_and_future_start():
    e = eng()
    e.process(nsig(notam_meta()), T0)
    cancel = notam_meta(id="F8030/26", key="LR:F8030/26", kind="anulare", ends="F8021/26", ends_key="LR:F8021/26")
    msgs = e.process(nsig(cancel), T0 + dt.timedelta(minutes=5))
    assert any("NOTAM ANULAT" in m.text and "F8021/26" in m.text for m in msgs)
    assert e.status(T0)["notam_active"] == []
    # expirare a unui NOTAM anunțat
    e2 = eng()
    e2.process(nsig(notam_meta(end=iso(T0 + dt.timedelta(minutes=30)))), T0)
    msgs = e2.tick(T0 + dt.timedelta(minutes=31))
    assert any("NOTAM ÎNCHEIAT" in m.text for m in msgs)
    # NOTAM programat peste 10 h: anunțat abia când devine iminent (≤ 6 h)
    e3 = eng()
    fut = notam_meta(start=iso(T0 + dt.timedelta(hours=10)), end=iso(T0 + dt.timedelta(hours=14)))
    assert e3.process(nsig(fut), T0) == []
    assert e3.tick(T0 + dt.timedelta(hours=3)) == []
    msgs = e3.tick(T0 + dt.timedelta(hours=4, minutes=1))
    assert len(msgs) == 1 and "F8021/26" in msgs[0].text


def test_notam_reissue_not_reannounced_and_restored_after_restart(tmp_path):
    e = eng()
    e.process(nsig(notam_meta()), T0)
    again = notam_meta(id="F8100/26", key="LR:F8100/26", continua="F8021/26")
    assert e.process(nsig(again), T0 + dt.timedelta(minutes=30)) == []
    # prima pornire după actualizare (fără listă salvată): arhiva e considerată deja anunțată
    st = Store(str(tmp_path / "v.db"))
    st.add_signal(nsig(notam_meta()))
    e2 = eng(st)
    assert [n["id"] for n in e2.status(T0)["notam_active"]] == ["F8021/26"]
    assert e2.tick(T0 + dt.timedelta(minutes=20)) == []             # nu se reanunță
    assert any("ÎNCHEIAT" in m.text for m in e2.tick(T0 + dt.timedelta(hours=9)))   # încheierea, da


def test_notam_state_survives_restart(tmp_path):
    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    a = notam_meta()
    s_a = nsig(a)
    st.add_signal(s_a)
    assert len(e.process(s_a, T0)) == 1                              # A anunțat
    b = notam_meta(id="F8022/26", key="LR:F8022/26")
    s_b = nsig(b)
    st.add_signal(s_b)
    assert e.process(s_b, T0 + dt.timedelta(minutes=2)) == []        # B în așteptare (limita de 10 min)
    fut = notam_meta(id="F8023/26", key="LR:F8023/26", start=iso(T0 + dt.timedelta(hours=10)),
                     end=iso(T0 + dt.timedelta(hours=14)))
    s_f = nsig(fut)
    st.add_signal(s_f)
    assert e.process(s_f, T0 + dt.timedelta(minutes=3)) == []        # programat peste 10 h
    e2 = eng(st)                                                     # repornire înainte de trimiterea lui B
    msgs = e2.tick(T0 + dt.timedelta(minutes=15))
    assert len(msgs) == 1 and "F8022/26" in msgs[0].text and "F8021/26" not in msgs[0].text
    msgs = e2.tick(T0 + dt.timedelta(hours=4, minutes=5))
    assert len(msgs) == 1 and "F8023/26" in msgs[0].text            # programatul, când devine iminent
    cancel = notam_meta(id="F8030/26", key="LR:F8030/26", kind="anulare", ends="F8021/26", ends_key="LR:F8021/26")
    assert any("ANULAT" in m.text for m in e2.process(nsig(cancel), T0 + dt.timedelta(hours=5)))


def test_notam_cancelled_while_pending_is_not_announced():
    e = eng()
    e.process(nsig(notam_meta()), T0)
    b = notam_meta(id="F8022/26", key="LR:F8022/26")
    assert e.process(nsig(b), T0 + dt.timedelta(minutes=1)) == []
    cancel = notam_meta(id="F8031/26", key="LR:F8031/26", kind="anulare", ends="F8022/26", ends_key="LR:F8022/26")
    e.process(nsig(cancel), T0 + dt.timedelta(minutes=2))
    assert e.tick(T0 + dt.timedelta(minutes=11)) == []


def test_notam_reissue_ends_quietly_and_rescheduled_one_is_announced():
    e = eng()
    p1 = notam_meta(id="P1/26", key="LR:P1/26", end=iso(T0 + dt.timedelta(hours=2)))
    e.process(nsig(p1), T0)                                          # anunțat
    p2 = notam_meta(id="P2/26", key="LR:P2/26", continua="P1/26", start=iso(T0 + dt.timedelta(hours=2)),
                    end=iso(T0 + dt.timedelta(days=30)))
    assert e.process(nsig(p2), T0 + dt.timedelta(minutes=30)) == []  # reemitere lipită: nu e o noutate
    assert e.tick(T0 + dt.timedelta(hours=2, minutes=1)) == []       # P1 expiră, dar continuă ca P2: fără ÎNCHEIAT
    # un NOTAM programat neanunțat, mutat mai devreme (același conținut): devine eligibil
    e2 = eng()
    f1 = notam_meta(id="F6001/26", key="LR:F6001/26", start=iso(T0 + dt.timedelta(hours=30)),
                    end=iso(T0 + dt.timedelta(hours=34)))
    assert e2.process(nsig(f1), T0) == []
    f2 = notam_meta(id="F6002/26", key="LR:F6002/26", kind="inlocuire", continua="F6001/26", ends="F6001/26",
                    ends_key="LR:F6001/26", start=iso(T0 + dt.timedelta(hours=4)), end=iso(T0 + dt.timedelta(hours=8)))
    msgs = e2.process(nsig(f2), T0 + dt.timedelta(minutes=1))
    assert len(msgs) == 1 and "F6002/26" in msgs[0].text


# ------------------------------------------------------------------ după verificarea integrării
def test_flapping_traffic_does_not_repeat_drop_or_detour_messages():
    e = eng()
    vigilance(e)
    low = adsb_meta(civil_airborne=1, drop={"real": False, "baseline": 8.0, "control_ok": True})
    zero = adsb_meta(civil_airborne=0, drop={"real": True, "baseline": 8.0, "control_ok": True})
    bad = adsb_meta(civil_airborne=0, coverage={"ok": False, "reason": "date_vechi"},
                    drop={"real": False, "suspected_outage": True, "baseline": 8.0})
    mid = adsb_meta(civil_airborne=3, drop={"real": False, "baseline": 8.0, "control_ok": True})
    seq = [low, low, low, bad, low, mid, low, low, low, bad, zero, bad, zero, low, low, low, mid, low, low, low]
    texts = []
    for k, m in enumerate(seq):
        texts += [x.text for x in e.process(sig(m), T0 + dt.timedelta(minutes=k))]
    assert sum("mult redus" in t for t in texts) == 1 and sum("la 0 aeronave" in t for t in texts) == 1


def test_maneuver_reminder_only_after_60_min():
    e = eng()
    m3 = adsb_meta(holding_recent=3, maneuver_aircraft=3, maneuver_alert=True)
    sent = [len(e.process(sig(m3), T0 + dt.timedelta(minutes=k))) for k in range(0, 70, 5)]
    assert sent[0] == 1 and sum(sent) == 2 and sent[12] == 1        # la 0 și la 60 min


def test_gnss_unknown_scope_wording():
    e = eng()
    on = {"n": 9, "degraded": 4, "lost": 0, "ratio": 0.33, "level": "ridicat", "interference": True, "changed": True,
          "scope": None}
    msgs = e.process(sig(adsb_meta(gnss=on)), T0)
    assert "întindere necunoscută" in msgs[0].text and "GNSS ;" not in msgs[0].text


def test_military_content_not_kept_in_archive(tmp_path):
    from veghe.notify import ConsoleSender, Dispatcher

    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    d = Dispatcher(st, [ConsoleSender()], [])

    class Fake:
        name, min_interval, optional = "telegram:-1", 0, False

        def __init__(self):
            self.got = []

        def send(self, text):
            self.got.append(text)

    tg = Fake()
    d.senders["internal"].append(tg)
    for m in e.process(sig(AM.summary(MIL, "Iași 150 NM", 47.1, 27.6, 150), role="adsb_militar"), T0):
        d.submit(m)
    t1 = T0 + dt.timedelta(minutes=1)
    vig = e.process(Signal(source="alerts_in_ua", role="ua_alert_state", text="", received_at=t1,
                           meta={"active": [{"title": "Подільський район", "type": "raion", "oblast": "Одеська область"}]}), t1)
    assert any("ADS-B militar (NU REDISTRIBUIȚI)" in m.text for m in vig)     # nota apare în VIGILENȚĂ
    for m in vig:
        d.submit(m)
    d.flush()
    assert any("VIGILENȚĂ" in t and "ADS-B militar (NU REDISTRIBUIȚI): 1 × avion de luptă" in t for t in tg.got)
    assert any("avion de luptă" in t for t in tg.got)                       # livrat
    rows = [r["text"] for r in st.outbox(limit=50)]
    assert rows and not any("avion de luptă" in t or "km NE" in t for t in rows)   # dar nepăstrat
    assert not any("avion de luptă" in (r["text"] or "") for r in st.events_between(T0 - dt.timedelta(hours=1), T0 + dt.timedelta(hours=1)))


def test_aviation_announcements_not_repeated_after_restart(tmp_path):
    from veghe.timeutil import now as real_now

    t = real_now()                                                # starea salvată se restaurează doar dacă e recentă
    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    s = AM.summary(MIL, "Iași 150 NM", 47.1, 27.6, 150)
    assert len(e.process(sig(s, role="adsb_militar", t=t), t)) == 1
    em = {"code": "7700", "meaning": "urgență", "dist_km": 22.0, "bearing": "NE", "alt_ft": 24000, "category": "A3", "new": True}
    assert len(e.process(sig(adsb_meta(emergencies=[em]), t=t), t)) == 1
    e2 = eng(st)                                                  # repornire în mijlocul incidentului
    t2 = t + dt.timedelta(minutes=3)
    assert e2.military_announced == 1
    assert e2.process(sig(s, role="adsb_militar", t=t2), t2) == []
    assert e2.process(sig(adsb_meta(emergencies=[em]), t=t2), t2) == []      # aceeași urgență, în 10 min


# ------------------------------------------------------------------ a doua verificare a integrării
def test_note_uses_last_good_reading_only():
    e = eng()
    vigilance(e)
    e.process(sig(adsb_meta(civil_airborne=0, drop={"real": True, "baseline": 6.0})), T0)
    assert "trafic civil oprit" in e._adsb_note(T0 + dt.timedelta(minutes=1))
    bad = adsb_meta(civil_airborne=5, coverage={"ok": False, "reason": "control_scazut"})
    for k in range(1, 30):
        e.process(sig(bad), T0 + dt.timedelta(minutes=k))
    assert "trafic civil oprit" not in e._adsb_note(T0 + dt.timedelta(minutes=29))


def test_stray_aircraft_does_not_end_closure_or_trigger_detour():
    e = eng()
    vigilance(e)
    zero = adsb_meta(civil_airborne=0, drop={"real": True, "baseline": 8.0, "control_ok": True})
    stray = adsb_meta(civil_airborne=1, drop={"real": False, "baseline": 8.0, "control_ok": True})
    seq = [zero, zero, stray, zero, stray, stray, stray, zero, zero, zero]
    texts = [x.text for k, m in enumerate(seq) for x in e.process(sig(m), T0 + dt.timedelta(minutes=k))]
    assert len(texts) == 1 and "la 0 aeronave" in texts[0]


def test_cleared_state_saved_for_restart(tmp_path):
    from veghe.timeutil import now as real_now

    t = real_now()
    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    vigilance(e, t)
    e.process(sig(adsb_meta(civil_airborne=0, drop={"real": True, "baseline": 6.0}), t=t), t)
    for k in range(1, 5):
        e.process(sig(adsb_meta(civil_airborne=6, drop={"real": False, "baseline": 6.0}), t=t), t + dt.timedelta(minutes=k))
    assert not e.adsb_anomaly["LRIA Iași"]
    e2 = eng(st)
    assert not e2.adsb_anomaly.get("LRIA Iași")


def test_gnss_daily_cap_survives_restart(tmp_path):
    from veghe.timeutil import now as real_now

    t = real_now()
    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    on = {"n": 9, "degraded": 4, "lost": 0, "ratio": 0.33, "level": "ridicat", "interference": True, "changed": True, "scope": "local"}
    off = {"n": 9, "degraded": 0, "lost": 0, "ratio": 0.0, "level": "normal", "interference": False, "changed": True}
    sent = 0
    for k in range(4):
        sent += len([m for m in e.process(sig(adsb_meta(gnss=on), t=t), t + dt.timedelta(minutes=40 * k)) if "precizie GPS degradată" in m.text])
        e.process(sig(adsb_meta(gnss=off), t=t), t + dt.timedelta(minutes=40 * k + 10))
    assert sent == 4
    e2 = eng(st)
    assert e2.process(sig(adsb_meta(gnss=on), t=t), t + dt.timedelta(minutes=200)) == []


def test_maneuver_not_resent_right_after_restart(tmp_path):
    from veghe.timeutil import now as real_now

    t = real_now()
    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    m3 = adsb_meta(holding_recent=3, maneuver_aircraft=3, maneuver_alert=True)
    assert len(e.process(sig(m3, t=t), t)) == 1
    e2 = eng(st)
    e2.process(sig(adsb_meta(), t=t), t + dt.timedelta(minutes=5))          # după repornire analizorul începe de la 0
    assert e2.process(sig(m3, t=t), t + dt.timedelta(minutes=12)) == []


def test_daily_notam_series_each_gets_its_end():
    e = eng()
    d1 = notam_meta(id="F5001/26", key="LR:F5001/26", end=iso(T0 + dt.timedelta(hours=1)))
    e.process(nsig(d1), T0)
    d2 = notam_meta(id="F5002/26", key="LR:F5002/26", continua="F5001/26", start=iso(T0 + dt.timedelta(hours=17)),
                    end=iso(T0 + dt.timedelta(hours=25)))
    e.process(nsig(d2), T0 + dt.timedelta(minutes=5))
    assert any("ÎNCHEIAT" in m.text and "F5001/26" in m.text for m in e.tick(T0 + dt.timedelta(hours=1, minutes=1)))


def test_failed_military_row_says_not_delivered_and_raw_file_is_clean(tmp_path):
    from veghe.notify import Dispatcher

    class Down:
        name, min_interval, optional = "telegram:-1", 0, False

        def send(self, text):
            raise OSError("jos")

    class Up(Down):
        name = "telegram:-2"

        def send(self, text):
            pass

    st = Store(str(tmp_path / "v.db"))
    e = eng(st)
    s = AM.summary(MIL, "Iași 150 NM", 47.1, 27.6, 150)
    d = Dispatcher(st, [Down()], [], max_attempts=1)
    for m in e.process(sig(s, role="adsb_militar"), T0):
        d.submit(m)
    d.flush()
    assert st.outbox(limit=5)[0]["text"].startswith("[ADS-B militar – nelivrat")
    d2 = Dispatcher(st, [Up()], [])
    e2 = eng()
    for m in e2.process(sig(s, role="adsb_militar"), T0):
        d2.submit(m)
    d2.flush()
    raw = b"".join(pathlib.Path(str(tmp_path / f)).read_bytes() for f in ("v.db", "v.db-wal") if (tmp_path / f).exists())
    assert "avion de luptă".encode() not in raw and b"km NE" not in raw


def test_prune_redacts_old_format_notes(tmp_path):
    st = Store(str(tmp_path / "v.db"))
    oid = st.enqueue("internal", "vigilenta", "[INTERN] VIGILENȚĂ. ADS-B militar (doar intern): 1 × avion de luptă (~50 km NE de Iași). Nicio acțiune.", "sent")
    st.add_event(0, None, "adsb_militar", "avion de luptă: 1", T0)
    st.prune()
    assert "avion de luptă" not in st.get_outbox(oid)["text"]
    assert all(r["text"] == "" for r in st.events_between(T0 - dt.timedelta(hours=1), T0 + dt.timedelta(hours=1)))
