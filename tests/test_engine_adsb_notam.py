"""Regulile motorului pentru ADS-B (analiză civilă, militari) și NOTAM, cu meta construită
exact în forma întoarsă de veghe.adsb_analysis / veghe.adsb_military / veghe.notam."""

import datetime as dt
import json

from veghe import adsb_military as AM
from veghe.engine import Engine, EngineConfig
from veghe.models import Signal
from veghe.store import Store
from veghe.timeutil import UTC, iso

T0 = dt.datetime(2026, 11, 3, 15, 0, tzinfo=UTC)


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
    assert e.status(T0)["militar"]["trigger"] == 0
    msgs = e.process(sig(s, role="adsb_militar"), T0 + dt.timedelta(minutes=31))         # reapar după zero
    assert len(msgs) == 1


# ------------------------------------------------------------------ NOTAM
def notam_meta(**kw):
    m = {"id": "F8021/26", "key": "LR:F8021/26", "kind": "nou", "replaces": None, "fir": "LRBB", "qcode": "QWULW",
         "category": "drone_uas", "uas": True, "near": True, "locations": ["LRBB"],
         "start": iso(T0 - dt.timedelta(hours=1)), "end": iso(T0 + dt.timedelta(hours=8)), "estimated": False,
         "dist_iasi_km": 42.8, "dist_prut_km": 0.0, "ends": None, "ends_key": None, "continua": None}
    m.update(kw)
    return m


def nsig(meta, t=T0, text=None):
    return Signal(source="notam:romatsa", role="notam", received_at=t, published_at=t, ext_id=f"{meta['key']}|{meta['kind']}",
                  text=text or f"NOTAM {meta['id']} · zboruri UAS / drone ({meta.get('qcode')}) · LRBB", meta=meta)


def test_notam_near_uas_announced_far_routine_archived():
    e = eng()
    msgs = e.process(nsig(notam_meta()), T0)
    assert len(msgs) == 1 and msgs[0].text.startswith("[INTERN] NOTAM") and "F8021/26" in msgs[0].text
    assert "nu confirmă o dronă" in msgs[0].text
    far = notam_meta(id="P1/26", key="LR:P1/26", near=False, category="restrictie_spatiu_aerian", uas=False, qcode="QRTCA")
    assert e.process(nsig(far), T0 + dt.timedelta(minutes=20)) == []
    assert {n["id"] for n in e.status(T0)["notam_active"]} == {"F8021/26", "P1/26"}


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
    st = Store(str(tmp_path / "v.db"))
    s1 = nsig(notam_meta())
    st.add_signal(s1)
    e2 = eng(st)                                                    # repornire: starea vine din arhivă
    assert [n["id"] for n in e2.status(T0)["notam_active"]] == ["F8021/26"]
    assert e2.tick(T0 + dt.timedelta(minutes=20)) == []             # nu se reanunță
    assert e2.tick(T0 + dt.timedelta(hours=9)) == []                # nici încheierea (n-am anunțat-o noi)
