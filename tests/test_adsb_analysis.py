"""Teste pentru veghe.adsb_analysis: politici (militari, confidențialitate, fără identități),
GNSS cu histerezis, urgențe persistente, așteptări/întoarceri din traiectorii sintetice,
pană de date vs scădere reală, ambele formate (re-api jv2 și aircraft.json), expirarea stării.

Fixturi: adsb_v2_sample_adsbone.json e mostra jv2 verbatim din README-ul ADSB One
(github.com/airplanes-live/api-archive); adsb_reapi_mix.json și adsb_aircraft_json_*.json urmează
câmpurile din readsb README-json.md / json_out.c (aeronava fără GPS e sintetică: deducție din sursă).
Traiectoriile sunt generate din mostra verbatim, cu poziții schimbate.
"""

import copy
import datetime as dt
import json
import math
import pathlib

import pytest

from veghe import adsb_analysis as A
from veghe import collectors as C
from veghe import geo
from veghe.timeutil import UTC

FIX = pathlib.Path(__file__).parent / "fixtures"
LRIA = (geo.LRIA.lat, geo.LRIA.lon)
LUKK = (geo.LUKK.lat, geo.LUKK.lon)
T0 = dt.datetime(2026, 11, 1, 18, 0, tzinfo=UTC)


def load(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


SAMPLE = load("adsb_v2_sample_adsbone.json")["ac"][0]  # mostra verbatim (ADSB One)
MIX = load("adsb_reapi_mix.json")
T_MIX = dt.datetime.fromtimestamp(MIX["now"] / 1000, UTC) + dt.timedelta(seconds=2)


def plane(hex_, la, lo, **kw):
    """Aeronavă în formatul mostrei verbatim; r/t prezente (readsb rulează cu --db-file).
    Un câmp cu valoarea None în kw e eliminat (ex. lat=None pentru o aeronavă fără GPS)."""
    ac = copy.deepcopy(SAMPLE)
    ac.update(hex=hex_, flight=f"TST{hex_[:4].upper()} ", r=f"YR-{hex_[-3:].upper()}", t="A320",
              category="A3", lat=round(la, 6), lon=round(lo, 6), seen_pos=1.0, seen=0.5, squawk="2000")
    for k, v in kw.items():
        if v is None:
            ac.pop(k, None)
        else:
            ac[k] = v
    return ac


def snap(acs, t):
    ms = int(t.timestamp() * 1000)
    return {"ac": acs, "msg": "No error", "now": ms, "total": len(acs), "ctime": ms, "ptime": 0}


def fresh(data, t):
    """Același răspuns jv2, „recitit” la momentul t (now/ctime noi): o observație nouă."""
    ms = int(t.timestamp() * 1000)
    return dict(data, now=ms, ctime=ms)


def feed(an, area, center, radius, data, t, **meta):
    m = A.snapshot_meta(data)
    m.update(meta)
    return an.update(area, center[0], center[1], radius, A.aircraft_list(data), t, m)


def offset(center, east_nm, north_nm):
    lat = center[0] + north_nm / 60.0
    return lat, center[1] + east_nm / (60.0 * math.cos(math.radians(center[0])))


def hexes(n, prefix="b"):
    return [f"{prefix}{i:03d}fa" for i in range(n)]


# ------------------------------------------------------------------ generatoare de traiectorii
def racetrack_xy(s, v=230.0, leg_s=60.0, turn_s=60.0):
    """Așteptare standard cu viraje la dreapta: picior 1 min, viraj 180° în 1 min (3°/s)."""
    a = v * leg_s / 3600.0
    r = v * turn_s / 3600.0 / math.pi
    s = s % (2 * (leg_s + turn_s))
    if s < leg_s:
        return 0.0, v * s / 3600.0
    s -= leg_s
    if s < turn_s:
        th = math.pi * s / turn_s
        return r - r * math.cos(th), a + r * math.sin(th)
    s -= turn_s
    if s < leg_s:
        return 2 * r, a - v * s / 3600.0
    th = math.pi * (s - leg_s) / turn_s
    return r + r * math.cos(th), -r * math.sin(th)


def rotate(x, y, hdg):
    h = math.radians(hdg)
    return x * math.cos(h) + y * math.sin(h), -x * math.sin(h) + y * math.cos(h)


def holding_positions(fix, minutes, *, inbound=90.0, v=230.0, enter_s=300, phase=17.0, drift=(0.0015, 0.0005)):
    """Apropiere în linie dreaptă spre punctul de așteptare (enter_s), apoi bucle; eșantion la 60 s."""
    out = []
    for i in range(minutes + 1):
        s = i * 60.0
        if s < enter_s:
            x, y = rotate(0.0, -v * (enter_s - s) / 3600.0, inbound)
        else:
            x, y = rotate(*racetrack_xy(s - enter_s + phase, v), inbound)
            x0, y0 = rotate(*racetrack_xy(phase, v), inbound)
            x, y = x - x0 + drift[0] * (s - enter_s), y - y0 + drift[1] * (s - enter_s)
        out.append(offset(fix, x, y))
    return out


def fly(start, hdg, gs, minutes, turns=()):
    """Integrare la 1 s; turns = [(început_s, sfârșit_s, rată °/s)]; eșantion la 60 s."""
    x = y = 0.0
    out = [offset(start, 0, 0)]
    for s in range(1, minutes * 60 + 1):
        hdg = (hdg + sum(r for a, b, r in turns if a <= s - 1 < b)) % 360
        x += gs / 3600.0 * math.sin(math.radians(hdg))
        y += gs / 3600.0 * math.cos(math.radians(hdg))
        if s % 60 == 0:
            out.append(offset(start, x, y))
    return out


def run_track(an, area, center, positions, mk, t0=T0, step=60):
    res = []
    for i, (lat, lon) in enumerate(positions):
        t = t0 + dt.timedelta(seconds=i * step)
        res.append(feed(an, area, center, 30, snap(mk(lat, lon), t), t))
    return res


# ------------------------------------------------------------------ formate și politici
def test_verbatim_sample_parses():
    data = load("adsb_v2_sample_adsbone.json")
    acs = A.aircraft_list(data)
    assert len(acs) == 1 and acs[0]["type"] == "adsb_icao"
    m = A.snapshot_meta(data)
    assert m["format"] == "jv2" and m["server_filtered"] is True and m["messages"] is None
    assert m["data_now"] == pytest.approx(1675633671.226, abs=1e-3)


def test_aircraft_list_both_formats_drop_military():
    assert [a["hex"] for a in A.aircraft_list(MIX)].count("43c6f2") == 0
    assert len(A.aircraft_list(MIX)) == 13
    local = load("adsb_aircraft_json_local.json")
    assert "43c71a" not in [a["hex"] for a in A.aircraft_list(local)]
    assert len(A.aircraft_list(local)) == 7
    m = A.snapshot_meta(local)
    assert m["format"] == "aircraft_json" and m["server_filtered"] is False
    assert m["messages"] == 48210337 and m["data_now"] == pytest.approx(1793546700.1, abs=1e-3)
    # re-api fără jv2: {"now": s, "aircraft", "resultCount"} – filtrat deja de server
    m2 = A.snapshot_meta({"now": 1793546700.5, "aircraft": [], "resultCount": 0, "ptime": 0.1})
    assert m2["format"] == "reapi" and m2["server_filtered"] is True
    assert A.aircraft_list({"msg": "No error"}) == [] and A.aircraft_list(None) == []
    # dbFlags ilizibil: exclus prudent
    assert A.aircraft_list({"ac": [{"hex": "4a0abc", "dbFlags": "x"}]}) == []


@pytest.mark.parametrize("name", ["adsb_point.json", "adsb_reapi_mix.json"])
def test_counts_parity_with_count_aircraft(name):
    data = load(name)
    t = dt.datetime.fromtimestamp(data["now"] / 1000, UTC) + dt.timedelta(seconds=2)
    r = feed(A.AdsbAnalyzer(), "LRIA Iași", LRIA, 30, data, t)
    legacy = C.count_aircraft(data)
    assert r["point"] == "LRIA Iași"
    assert r["civil_airborne"] == legacy["civil_airborne"] and r["civil_total"] == legacy["civil_total"]


def test_mix_fixture_full_result():
    an = A.AdsbAnalyzer()
    r = feed(an, "LRIA Iași", LRIA, 30, MIX, T_MIX)
    assert (r["civil_total"], r["civil_airborne"], r["civil_gps_lost"], r["civil_mlat"]) == (13, 10, 1, 1)
    g = r["gnss"]
    # eligibile: ROT711, RYR, WZZ (degradat), THY (fără GPS), DLH, C172 → 6; PIA/LADD/MLAT/v0/elicopter/sol: nu
    assert (g["n"], g["degraded"], g["lost"]) == (6, 2, 1)
    assert g["ratio"] == pytest.approx(round(1 / 6, 3)) and g["level"] == "ridicat"
    assert g["interference"] is False  # o singură evaluare
    assert r["emergencies"] == []  # o singură apariție
    assert r["coverage"] == {"ok": True, "reason": "ok", "data_age_s": 2.0, "median_seen_pos_s": 1.3}
    json.dumps(r)  # serializabil


def test_military_excluded_from_everything():
    an = A.AdsbAnalyzer()
    mil = [plane(h, *offset(LRIA, 5, i), dbFlags=1, squawk="7700", emergency="general", nac_p=3, nic=2)
           for i, h in enumerate(hexes(5, "c"))]
    for k in range(3):
        t = T0 + dt.timedelta(seconds=30 * k)
        r = feed(an, "LRIA", LRIA, 30, snap(mil, t), t)
        assert (r["civil_total"], r["civil_airborne"]) == (0, 0)
        assert r["emergencies"] == [] and r["gnss"]["n"] == 0
    assert an.state_size()["LRIA"] == {"tracks": 0, "gnss": 0, "emergencies": 0, "dedup": 0, "recent": 0}
    # amestec: militarul cu 7700 nu apare, civilul cu 7700 da
    an = A.AdsbAnalyzer()
    for k in range(2):
        t = T_MIX + dt.timedelta(seconds=30 * k)
        r = feed(an, "LRIA Iași", LRIA, 30, fresh(MIX, t), t)
    assert [e["code"] for e in r["emergencies"]] == ["7700"]
    assert r["emergencies"][0]["category"] == "A3"


def test_privacy_flagged_counted_but_not_analysed():
    an = A.AdsbAnalyzer()
    pia = plane("d1a0fa", *offset(LRIA, -8, 3), dbFlags=4, squawk="7600", emergency="nordo", nac_p=3, nic=2)
    ladd = plane("d1a1fa", *offset(LRIA, 8, -3), dbFlags=8, squawk="7700", emergency="general", nac_p=4)
    track = holding_positions(offset(LRIA, 0, 15), 16)
    for i, pos in enumerate(track):
        t = T0 + dt.timedelta(seconds=60 * i)
        hold = plane("d1a2fa", *pos, dbFlags=12, alt_baro=9000, gs=230.0)  # PIA+LADD, în așteptare
        r = feed(an, "LRIA", LRIA, 30, snap([pia, ladd, hold], t), t)
        assert r["civil_total"] == 3 and r["civil_airborne"] == 3  # în numărătorile agregate: da
        assert r["emergencies"] == [] and r["gnss"]["n"] == 0  # în analizele pe aeronavă: nu
        assert r["holding"] == 0 and r["holding_recent"] == 0
    assert an.state_size()["LRIA"]["tracks"] == 0


# ------------------------------------------------------------------ GNSS
def gnss_fleet(n_good, n_bad=0, n_lost=0):
    acs = [plane(h, *offset(LRIA, i * 2 - 10, 5), nac_p=10, nic=8, alt_baro=35000, gs=450.0)
           for i, h in enumerate(hexes(n_good, "e"))]
    acs += [plane(h, *offset(LRIA, i * 2 - 10, -5), nac_p=4, nic=5, alt_baro=35000, gs=450.0)
            for i, h in enumerate(hexes(n_bad, "d"))]
    acs += [plane(h, 0, 0, lat=None, lon=None, nic=None, rc=None, seen_pos=None, alt_baro=36000, gs=440.0,
                  gpsOkBefore=T0.timestamp() - 120, gpsOkLat=47.3, gpsOkLon=27.9,
                  lastPosition={"lat": 47.31, "lon": 27.95, "nic": 8, "rc": 186, "seen_pos": 70.0})
            for h in hexes(n_lost, "f")]
    return acs


def test_gnss_hysteresis_on_off():
    an = A.AdsbAnalyzer()
    jam = gnss_fleet(5, 3)  # N = 8, B = 3 → (3−1)/8 = 0.25
    clean = gnss_fleet(5) + [plane(h, *offset(LRIA, 0, -5), nac_p=10, nic=8) for h in hexes(3, "d")]
    r1 = feed(an, "LRIA", LRIA, 30, snap(jam, T0), T0)
    assert r1["gnss"]["ratio"] == 0.25 and r1["gnss"]["interference"] is False
    t = T0 + dt.timedelta(seconds=10)  # prea devreme: nu contează a doua oară
    assert feed(an, "LRIA", LRIA, 30, snap(jam, t), t)["gnss"]["interference"] is False
    t_on = T0 + dt.timedelta(seconds=40)
    r = feed(an, "LRIA", LRIA, 30, snap(jam, t_on), t_on)
    assert r["gnss"]["interference"] is True and r["gnss"]["changed"] is True and r["gnss"]["since"]
    changes, off_at = [], None
    for k in range(1, 40):  # aeronave curate, la 30 s
        t = t_on + dt.timedelta(seconds=30 * k)
        g = feed(an, "LRIA", LRIA, 30, snap(clean, t), t)["gnss"]
        if g["changed"]:
            changes.append((k, g["interference"]))
        if not g["interference"] and off_at is None:
            off_at = (t - t_on).total_seconds()
    assert changes == [(changes[0][0], False)]  # o singură ieșire
    # fereastra de 10 min se golește, apoi 3 evaluări curate; cel puțin 10 min în stare
    assert 600 + 60 <= off_at <= 600 + 150


def test_gnss_single_bad_or_low_ratio_never_enters():
    an = A.AdsbAnalyzer()
    for k in range(10):  # un singur avion degradat: (1−1)/N = 0 (formula gpsjam)
        t = T0 + dt.timedelta(seconds=30 * k)
        g = feed(an, "LRIA", LRIA, 30, snap(gnss_fleet(7, 1), t), t)["gnss"]
        assert g["ratio"] == 0 and g["interference"] is False and g["level"] == "normal"
    an = A.AdsbAnalyzer()
    for k in range(10):  # 2 din 20: (2−1)/20 = 5 % → banda „mediu”, sub pragul de 10 %
        t = T0 + dt.timedelta(seconds=30 * k)
        g = feed(an, "LRIA", LRIA, 30, snap(gnss_fleet(18, 2), t), t)["gnss"]
        assert g["level"] == "mediu" and g["interference"] is False
    an = A.AdsbAnalyzer()
    for k in range(10):  # sub 4 aeronave eligibile: insuficient
        t = T0 + dt.timedelta(seconds=30 * k)
        g = feed(an, "LRIA", LRIA, 30, snap(gnss_fleet(1, 2), t), t)["gnss"]
        assert g["level"] == "insuficient" and g["interference"] is False


def test_gnss_lost_enters_immediately_and_baseline_raises_threshold():
    an = A.AdsbAnalyzer()
    g = feed(an, "LRIA", LRIA, 30, snap(gnss_fleet(4, 0, 2), T0), T0)["gnss"]
    assert g["lost"] == 2 and g["interference"] is True and g["changed"] is True
    an = A.AdsbAnalyzer()
    an.set_gnss_baseline("LRIA", 0.20)  # fond ridicat (ex. Marea Neagră): prag = 0.30
    for k in range(5):
        t = T0 + dt.timedelta(seconds=30 * k)
        g = feed(an, "LRIA", LRIA, 30, snap(gnss_fleet(5, 3), t), t)["gnss"]
        assert g["ratio"] == 0.25 and g["interference"] is False


def test_gnss_scope_local_vs_regional():
    for ctl_bad, scope in ((0, "local"), (4, "regional")):
        an = A.AdsbAnalyzer(control_area="control")
        for k in range(3):
            t = T0 + dt.timedelta(seconds=30 * k)
            ctl = [plane(h, 46.6, 24.6 + i * 0.1, nac_p=10, nic=8) for i, h in enumerate(hexes(10, "a"))]
            ctl += [plane(h, 46.5, 24.6 + i * 0.1, nac_p=3, nic=3) for i, h in enumerate(hexes(ctl_bad, "c"))]
            assert feed(an, "control", (46.6, 24.6), 120, snap(ctl, t), t)["gnss"]["scope"] is None
            g = feed(an, "LRIA", LRIA, 30, snap(gnss_fleet(5, 3), t), t)["gnss"]
        assert g["interference"] is True and g["scope"] == scope


# ------------------------------------------------------------------ urgențe
def test_emergency_needs_two_snapshots():
    an = A.AdsbAnalyzer()
    em = plane("ab7fca", *offset(LRIA, 9, 9), squawk="7700", emergency="general", alt_baro=24350)
    other = plane("ab70ca", *offset(LRIA, -5, 0))

    def at(sec, acs):
        t = T0 + dt.timedelta(seconds=sec)
        return feed(an, "LRIA", LRIA, 30, snap(acs, t), t)["emergencies"]

    assert at(0, [em, other]) == []  # 1 instantaneu: nimic
    assert at(10, [em, other]) == []  # al doilea prea devreme (< 25 s)
    e = at(35, [em, other])
    assert len(e) == 1 and e[0]["new"] is True
    assert e[0]["code"] == "7700" and e[0]["meaning"].startswith("urgență generală")
    assert e[0]["bearing"] == "NE" and 20 <= e[0]["dist_km"] <= 26 and e[0]["alt_ft"] == 24000
    assert at(65, [em, other])[0]["new"] is False  # deja anunțat
    assert at(95, [other]) == []  # lipsă 1
    assert at(125, [other]) == []  # lipsă 2 → încheiat
    assert at(155, [em, other]) == []
    again = at(185, [em, other])
    assert len(again) == 1 and again[0]["new"] is False  # deduplicare 30 min


def test_emergency_7500_needs_three_or_unlawful_and_ground_ignored():
    an = A.AdsbAnalyzer()
    hij = plane("ab75ca", *offset(LRIA, 0, 10), squawk="7500", emergency="none")
    gnd = plane("ab76ca", *LRIA, squawk="7700", alt_baro="ground", gs=5.0)
    out = []
    for k in range(3):
        t = T0 + dt.timedelta(seconds=30 * k)
        out.append([e["code"] for e in feed(an, "LRIA", LRIA, 30, snap([hij, gnd], t), t)["emergencies"]])
    assert out == [[], [], ["7500"]]
    an = A.AdsbAnalyzer()
    hij2 = dict(hij, emergency="unlawful")
    out = []
    for k in range(2):
        t = T0 + dt.timedelta(seconds=30 * k)
        out.append([e["code"] for e in feed(an, "LRIA", LRIA, 30, snap([hij2], t), t)["emergencies"]])
    assert out == [[], ["7500"]]
    # starea ADS-B fără squawk 7x00 (ex. minfuel) e raportată cu numele ei
    an = A.AdsbAnalyzer()
    mf = plane("ab77ca", *offset(LRIA, 3, 3), emergency="minfuel")
    for k in range(2):
        t = T0 + dt.timedelta(seconds=30 * k)
        e = feed(an, "LRIA", LRIA, 30, snap([mf], t), t)["emergencies"]
    assert [x["code"] for x in e] == ["minfuel"]


# ------------------------------------------------------------------ manevre
def airliner(hex_, alt=9000, gs=230.0, **kw):
    return lambda lat, lon: [plane(hex_, lat, lon, alt_baro=alt, gs=gs, **kw)]


def test_holding_racetrack_detected():
    an = A.AdsbAnalyzer()
    res = run_track(an, "LRIA", LRIA, holding_positions(offset(LRIA, 0, 15), 18), airliner("aa01fb"))
    first = next(i for i, r in enumerate(res) if r["holding"])
    # intrare în așteptare la minutul 5; detecție în 8–12 min (cercetare): bucla apare în fereastra de
    # 8 min după ~6 min, apoi trebuie să persiste încă 4 min (holding_confirm_s)
    assert 5 + 9 <= first <= 5 + 12
    assert res[-1]["holding"] == 1 and res[-1]["holding_recent"] == 1 and res[-1]["turnbacks"] == 0
    m = res[-1]["maneuvers"]
    assert m[0]["kind"] == "asteptare" and m[0]["bearing"] in ("N", "NE", "NV") and m[0]["alt_ft"] == 9000
    assert res[-1]["maneuver_alert"] is False  # o singură aeronavă


def test_two_holdings_raise_maneuver_alert():
    an = A.AdsbAnalyzer()
    a = holding_positions(offset(LUKK, -20, 0), 18, inbound=270, phase=41)
    b = holding_positions(offset(LUKK, 0, -18), 18, inbound=0, phase=5, v=210)
    for i in range(19):
        t = T0 + dt.timedelta(minutes=i)
        acs = [plane("aa02fb", *a[i], alt_baro=8000, gs=230.0), plane("aa03fb", *b[i], alt_baro=11000, gs=210.0)]
        r = feed(an, "LUKK", LUKK, 30, snap(acs, t), t)
    assert r["holding"] == 2 and r["maneuver_alert"] is True


def test_turnback_detected_once():
    an = A.AdsbAnalyzer()
    pos = fly(offset(LUKK, -100, 0), 90.0, 450.0, 22, turns=[(480, 630, 1.2)])
    res = run_track(an, "LUKK", LUKK, pos, airliner("aa04fb", alt=35000, gs=450.0))
    first = next(i for i, r in enumerate(res) if r["turnbacks"])
    # viraj la minutul 8 (2,5 min); detecție când ambele segmente sunt drepte și opuse
    assert 8 + 3 <= first <= 8 + 9
    assert all(r["holding"] == 0 for r in res)
    assert res[-1]["turnbacks"] == 1 and res[-1]["maneuvers"][0]["kind"] == "intoarcere"


@pytest.mark.parametrize("turns", [[], [(600, 660, 1.5)], [(300, 330, 1.0), (700, 760, -1.0)]])
def test_straight_and_gentle_turns_not_flagged(turns):
    an = A.AdsbAnalyzer()
    pos = fly(offset(LRIA, -60, -20), 60.0, 440.0, 20, turns=turns)
    res = run_track(an, "LRIA", LRIA, pos, airliner("aa05fb", alt=33000, gs=440.0))
    assert all(r["holding"] == 0 and r["turnbacks"] == 0 and r["holding_recent"] == 0 for r in res)


@pytest.mark.parametrize("kw", [
    {"category": "A1", "gs": 230.0},  # aviație ușoară
    {"category": "A7", "gs": 230.0},  # elicopter
    {"category": "B6", "gs": 230.0},  # UAV declarat
    {"category": None, "gs": 150.0},  # fără categorie și lent
    {"category": "A3", "gs": 130.0},  # lent
    {"category": "A3", "alt_baro": 2500},  # jos
    {"type": "mlat", "mlat": ["lat", "lon", "gs", "track"]},  # poziție MLAT
    {"seen_pos": 45.0},  # poziție veche
])
def test_ga_helicopter_slow_low_not_flagged(kw):
    an = A.AdsbAnalyzer()
    base = {"alt_baro": 9000, "gs": 230.0}
    base.update(kw)
    res = run_track(an, "LRIA", LRIA, holding_positions(offset(LRIA, 0, 12), 18),
                    lambda lat, lon: [plane("aa06fb", lat, lon, **base)])
    assert all(r["holding"] == 0 and r["holding_recent"] == 0 for r in res)


def test_reversal_near_airport_low_is_approach_not_turnback():
    def run(alt):
        an = A.AdsbAnalyzer()
        pos = fly(offset(LRIA, -30, -6), 90.0, 250.0, 20, turns=[(420, 570, 1.2)])
        return run_track(an, "LRIA", LRIA, pos, airliner("aa07fb", alt=alt, gs=250.0))
    assert all(r["turnbacks"] == 0 for r in run(6000))  # la < 20 NM de LRIA și sub 10 000 ft
    assert run(12000)[-1]["turnbacks"] == 1


# ------------------------------------------------------------------ acoperire / scădere reală
CTL = (46.6, 24.6)


def poll(an, i, area_n, ctl_n, *, area_age=0.0, area_meta=None, lost=False):
    t = T0 + dt.timedelta(minutes=i)
    ctl = [plane(h, CTL[0], CTL[1] + j * 0.05) for j, h in enumerate(hexes(ctl_n, "c"))]
    feed(an, "control", CTL, 120, snap(ctl, t), t)
    area = [plane(h, *offset(LRIA, j, j)) for j, h in enumerate(hexes(area_n, "a"))]
    if lost:
        area = [plane(h, 0, 0, lat=None, lon=None, nic=None, rc=None, seen_pos=None, gpsOkBefore=t.timestamp() - 60,
                      gpsOkLat=47.2, gpsOkLon=27.7) for h in hexes(5, "f")]
    data = snap(area, t - dt.timedelta(seconds=area_age))
    if area_meta is not None:
        return an.update("LRIA", LRIA[0], LRIA[1], 30, [], t, area_meta)
    return feed(an, "LRIA", LRIA, 30, data, t)


def warm(an):
    for i in range(20):
        r = poll(an, i, 5, 20)
        assert r["coverage"]["ok"] is True and r["drop"]["real"] is False
    return 20


def test_real_drop_confirmed_by_control():
    an = A.AdsbAnalyzer(control_area="control")
    i = warm(an)
    r1, r2, r3 = (poll(an, i + k, 0, 20) for k in range(3))
    assert r2["drop"]["real"] is False and r2["drop"]["zero_streak"] == 2
    assert r3["drop"] == {"real": True, "suspected_outage": False, "zero_streak": 3, "baseline": 5.0, "control_ok": True}
    assert r3["coverage"]["ok"] is True


def test_outage_when_control_also_collapses():
    an = A.AdsbAnalyzer(control_area="control")
    i = warm(an)
    rs = [poll(an, i + k, 0, 0) for k in range(3)]
    assert rs[-1]["coverage"] == {"ok": False, "reason": "control_scazut", "data_age_s": 0.0, "median_seen_pos_s": None}
    assert rs[-1]["drop"]["real"] is False and rs[-1]["drop"]["suspected_outage"] is True


def test_outage_stale_data_and_failed_source():
    an = A.AdsbAnalyzer(control_area="control")
    i = warm(an)
    rs = [poll(an, i + k, 0, 20, area_age=120) for k in range(3)]
    assert rs[-1]["coverage"]["reason"] == "date_vechi" and rs[-1]["drop"]["suspected_outage"] is True
    assert rs[-1]["drop"]["real"] is False
    an = A.AdsbAnalyzer(control_area="control")
    i = warm(an)
    rs = [poll(an, i + k, 0, 20, area_meta={"ok": False}) for k in range(3)]
    assert rs[-1]["coverage"]["reason"] == "sursa_indisponibila" and rs[-1]["drop"]["real"] is False


def test_gps_lost_aircraft_are_not_a_traffic_drop():
    an = A.AdsbAnalyzer(control_area="control")
    i = warm(an)
    rs = [poll(an, i + k, 0, 20, lost=True) for k in range(3)]
    r = rs[-1]
    assert r["civil_airborne"] == 0 and r["civil_gps_lost"] == 5  # semantica veche: 0 „în aer”
    assert r["drop"]["zero_streak"] == 0 and r["drop"]["real"] is False
    assert r["gnss"]["lost"] == 5 and r["gnss"]["interference"] is True


def test_local_receiver_messages_stall():
    an = A.AdsbAnalyzer()
    local = load("adsb_aircraft_json_local.json")
    t = dt.datetime.fromtimestamp(local["now"], UTC)
    reasons = []
    for k in range(4):
        tk = t + dt.timedelta(seconds=30 * k)
        d = dict(local, now=tk.timestamp())  # fișierul se rescrie, dar contorul nu crește
        reasons.append(feed(an, "LRIA", LRIA, 30, d, tk)["coverage"]["reason"])
    assert reasons == ["ok", "ok", "receptor_fara_mesaje", "receptor_fara_mesaje"]
    d = dict(local, now=(t + dt.timedelta(seconds=150)).timestamp(), messages=local["messages"] + 900)
    assert feed(an, "LRIA", LRIA, 30, d, t + dt.timedelta(seconds=150))["coverage"]["reason"] == "ok"


def test_seed_counts_gives_immediate_baseline():
    an = A.AdsbAnalyzer()
    an.seed_counts("LRIA", [(T0 - dt.timedelta(minutes=90 - k * 5), 4) for k in range(15)])
    rs = [an.update("LRIA", *LRIA, 30, [], T0 + dt.timedelta(minutes=k), {"data_now": (T0 + dt.timedelta(minutes=k)).timestamp()})
          for k in range(3)]
    assert rs[-1]["drop"]["baseline"] == 4.0 and rs[-1]["drop"]["real"] is True and rs[-1]["drop"]["control_ok"] is None


# ------------------------------------------------------------------ format local (aircraft.json)
def test_local_aircraft_json_filtered_by_distance():
    local = load("adsb_aircraft_json_local.json")
    t = dt.datetime.fromtimestamp(local["now"], UTC) + dt.timedelta(seconds=1)
    r = feed(A.AdsbAnalyzer(), "LRIA Iași", LRIA, 30, local, t)
    # în cerc: ATR în aer, A318 la sol, A20N fără GPS (plasat după lastPosition recent);
    # afară: Chișinău, Bacău; neplasabile: Mode S fără poziție, lastPosition de 3 zile; militarul: exclus
    assert (r["civil_total"], r["civil_airborne"], r["civil_gps_lost"], r["civil_unplaced"]) == (3, 1, 1, 2)
    r = feed(A.AdsbAnalyzer(), "LUKK", LUKK, 30, local, t)
    assert (r["civil_total"], r["civil_airborne"]) == (1, 1)


def test_same_aircraft_in_both_formats():
    acs = [a for a in MIX["ac"]]
    local = {"now": MIX["now"] / 1000, "messages": 1000, "aircraft": acs}
    r1 = feed(A.AdsbAnalyzer(), "LRIA", LRIA, 30, MIX, T_MIX)
    r2 = feed(A.AdsbAnalyzer(), "LRIA", LRIA, 30, local, T_MIX)
    assert r2["civil_total"] == r1["civil_total"] - 1 and r2["civil_unplaced"] == 1  # Mode S fără poziție
    assert r2["civil_airborne"] == r1["civil_airborne"] and r2["gnss"] == r1["gnss"]


def test_without_db_no_per_aircraft_analysis():
    nodb = load("adsb_aircraft_json_nodb.json")
    an = A.AdsbAnalyzer()
    for k in range(3):
        t = dt.datetime.fromtimestamp(nodb["now"], UTC) + dt.timedelta(seconds=30 * k)
        d = dict(nodb, now=t.timestamp(), messages=nodb["messages"] + k)
        r = feed(an, "LRIA", LRIA, 30, d, t)
        assert r["coverage"]["reason"] == "fara_db" and r["coverage"]["ok"] is False
        assert r["emergencies"] == [] and r["gnss"]["n"] == 0
    assert an.state_size()["LRIA"]["gnss"] == 0 and an.state_size()["LRIA"]["emergencies"] == 0


# ------------------------------------------------------------------ memorie și identități
def test_state_expires_after_minutes():
    an = A.AdsbAnalyzer()
    res = run_track(an, "LRIA", LRIA, holding_positions(offset(LRIA, 0, 15), 18), airliner("aa08fb"))
    assert res[-1]["holding"] == 1
    em = plane("ab7fca", *offset(LRIA, 5, 5), squawk="7700")
    for k in range(2):
        t = T0 + dt.timedelta(minutes=18, seconds=30 * (k + 1))
        feed(an, "LRIA", LRIA, 30, snap([em], t), t)
    s = an.state_size()["LRIA"]
    assert s["tracks"] >= 1 and s["gnss"] >= 1 and s["dedup"] == 1 and s["recent"] == 1
    end = T0 + dt.timedelta(minutes=19)
    for m in (6, 11, 21, 31):
        an.prune(end + dt.timedelta(minutes=m))
        s = an.state_size()["LRIA"]
        if m >= 6:
            assert s["tracks"] == 0 and s["emergencies"] == 0
        if m >= 11:
            assert s["gnss"] == 0
        if m >= 21:
            assert s["recent"] == 0
    assert s == {"tracks": 0, "gnss": 0, "emergencies": 0, "dedup": 0, "recent": 0}


def test_no_identities_in_output_or_memory():
    an = A.AdsbAnalyzer(control_area="control")
    results = []
    local = load("adsb_aircraft_json_local.json")
    for k in range(3):
        t = T_MIX + dt.timedelta(seconds=30 * k)
        results.append(feed(an, "LRIA Iași", LRIA, 30, fresh(MIX, t), t))
        results.append(feed(an, "LUKK", LUKK, 60, dict(local, now=t.timestamp(), messages=k), t))
    results += run_track(an, "LUKK", LUKK, fly(offset(LUKK, -100, 0), 90.0, 450.0, 20, turns=[(480, 630, 1.2)]),
                         airliner("aa09fb", alt=35000, gs=450.0), t0=T_MIX + dt.timedelta(minutes=5))
    blob = json.dumps(results, ensure_ascii=False)
    assert any(r["emergencies"] for r in results) and any(r["turnbacks"] for r in results)
    memory = repr(an.__dict__)
    idents = set()
    for ac in MIX["ac"] + local["aircraft"]:
        idents |= {ac["hex"], ac.get("r"), (ac.get("flight") or "").strip()} - {None, ""}
    idents |= {"aa09fb", "TSTAA09", "YR-AFB"}
    for s in idents:
        assert s not in blob, s
        assert s not in memory, s


# ------------------------------------------------------------------ regresii (revizie)
def nodb(acs):
    """Aceleași aeronave, ca de la un readsb fără --db-file (fără r/t/dbFlags)."""
    out = []
    for ac in acs:
        ac = dict(ac)
        for k in ("r", "t", "dbFlags"):
            ac.pop(k, None)
        out.append(ac)
    return out


@pytest.mark.parametrize("body", [{}, {"msg": "Error: rate limited"}, None, [], "x", {"ac": "x"},
                                  {"ac": [], "msg": "No error"},  # fără `now`
                                  {"ac": [], "now": "abc"}, {"aircraft": None, "now": 1793546700.1}])
def test_snapshot_meta_body_without_aircraft_or_now_is_a_failure(body):
    m = A.snapshot_meta(body)
    assert m["ok"] is False
    an = A.AdsbAnalyzer(control_area="control")
    i = warm(an)
    for k in range(4):
        t = T0 + dt.timedelta(minutes=i + k)
        r = an.update("LRIA", *LRIA, 30, A.aircraft_list(body), t, A.snapshot_meta(body))
    assert r["coverage"]["reason"] == "sursa_indisponibila" and r["drop"]["real"] is False
    assert r["civil_total"] == 0 and r["drop"]["zero_streak"] == 0


def test_aircraft_list_without_messages_or_resultcount_is_filtered_locally():
    local = load("adsb_aircraft_json_local.json")
    no_msgs = {k: v for k, v in local.items() if k != "messages"}
    m = A.snapshot_meta(no_msgs)
    assert m["ok"] is True and m["format"] == "aircraft_json" and m["server_filtered"] is False
    t = dt.datetime.fromtimestamp(local["now"], UTC) + dt.timedelta(seconds=1)
    r = feed(A.AdsbAnalyzer(), "LRIA Iași", LRIA, 30, no_msgs, t)
    assert (r["civil_total"], r["civil_unplaced"]) == (3, 2)  # Chișinău și Bacău rămân afară


def test_unhealthy_polls_do_not_count_towards_real_drop():
    an = A.AdsbAnalyzer(control_area="control")
    i = warm(an)
    for k in range(3):  # 3 cereri eșuate
        r = poll(an, i + k, 0, 20, area_meta={"ok": False})
        assert r["drop"]["real"] is False and r["drop"]["zero_streak"] == 0
    assert r["drop"]["suspected_outage"] is True
    rs = [poll(an, i + 3 + k, 0, 20) for k in range(3)]  # apoi citiri bune, cu 0
    assert [x["drop"]["zero_streak"] for x in rs] == [1, 2, 3]
    assert [x["drop"]["real"] for x in rs] == [False, False, True]


def test_real_drop_needs_confirmed_control_when_configured():
    an = A.AdsbAnalyzer(control_area="control")
    i = warm(an)
    for k in range(8):  # zona de control nu mai răspunde; zona țintă dă 0, proaspăt
        t = T0 + dt.timedelta(minutes=i + k)
        an.update("control", *CTL, 120, [], t, {"ok": False})
        r = feed(an, "LRIA", LRIA, 30, snap([], t), t)
        if k >= 5:  # ultima citire bună a zonei de control e mai veche de 5 min: necunoscut ≠ normal
            assert r["drop"]["control_ok"] is None and r["coverage"]["ok"] is True
            assert r["drop"]["real"] is False and r["drop"]["suspected_outage"] is True
    assert r["drop"]["zero_streak"] == 8


def test_repeated_or_stale_snapshot_never_self_confirms():
    em = plane("ab7fca", *offset(LRIA, 9, 9), squawk="7700", emergency="general")
    acs = gnss_fleet(5, 3) + [em]
    frozen = snap(acs, T0)
    an = A.AdsbAnalyzer()
    for k in range(4):  # același instantaneu (cache înghețat), recitit la 30 s
        t = T0 + dt.timedelta(seconds=30 * k)
        r = feed(an, "LRIA", LRIA, 30, frozen, t)
        assert r["emergencies"] == [] and r["gnss"]["interference"] is False
        assert r["coverage"]["reason"] == ("ok" if k == 0 else "date_vechi")
    t = T0 + dt.timedelta(seconds=150)  # o citire nouă: a doua observație independentă
    r = feed(an, "LRIA", LRIA, 30, snap(acs, t), t)
    assert [e["code"] for e in r["emergencies"]] == ["7700"] and r["gnss"]["interference"] is True
    an = A.AdsbAnalyzer()
    for k in range(4):  # date vechi de 60 s (> 45 s), chiar dacă `now` avansează
        t = T0 + dt.timedelta(seconds=30 * k)
        r = feed(an, "LRIA", LRIA, 30, snap(acs, t - dt.timedelta(seconds=60)), t)
        assert r["emergencies"] == [] and r["gnss"]["interference"] is False
        assert r["coverage"]["reason"] == "date_vechi"
    assert an.state_size()["LRIA"]["emergencies"] == 0 and an.state_size()["LRIA"]["gnss"] == 0


def test_gnss_no_false_all_clear_when_area_empties():
    an = A.AdsbAnalyzer()
    for k in range(2):
        t = T0 + dt.timedelta(seconds=30 * k)
        g = feed(an, "LRIA", LRIA, 30, snap(gnss_fleet(5, 3), t), t)["gnss"]
    assert g["interference"] is True
    off = None
    for m in range(1, 50):  # spațiul aerian se golește (ex. închidere): instantanee proaspete, goale
        t = T0 + dt.timedelta(seconds=30, minutes=m)
        g = feed(an, "LRIA", LRIA, 30, snap([], t), t)["gnss"]
        if g["changed"]:
            assert off is None and g["interference"] is False and g["level"] == "insuficient"
            off = m
    # fereastra de 10 min păstrează aeronavele văzute; apoi 30 min fără dovezi → închidere, nu „normal”
    assert 10 + 30 <= off <= 10 + 32


def test_gnss_stale_exit_also_while_source_down():
    an = A.AdsbAnalyzer()
    g = feed(an, "LRIA", LRIA, 30, snap(gnss_fleet(4, 0, 2), T0), T0)["gnss"]
    assert g["interference"] is True
    changes = []
    for m in range(1, 40):
        t = T0 + dt.timedelta(minutes=m)
        g = an.update("LRIA", *LRIA, 30, [], t, {"ok": False})["gnss"]
        if g["changed"]:
            changes.append((m, g["interference"]))
    assert changes == [(30, False)]


def test_db_guard_is_sticky_and_unknown_blocks_analysis():
    em = plane("ab7fca", *offset(LRIA, 9, 9), squawk="7700", emergency="general")
    two = nodb([em, plane("ab70ca", *offset(LRIA, -5, 0))])
    three = two + nodb([plane("ab71ca", *offset(LRIA, 0, -5))])
    an = A.AdsbAnalyzer()
    for k in range(3):  # pornire cu < 3 aeronave fără r/t/dbFlags: necunoscut → fără analiză pe aeronavă
        t = T0 + dt.timedelta(seconds=30 * k)
        r = feed(an, "LRIA", LRIA, 30, snap(two, t), t)
        assert r["emergencies"] == [] and r["coverage"]["reason"] == "ok"
    assert an.state_size()["LRIA"] == {"tracks": 0, "gnss": 0, "emergencies": 0, "dedup": 0, "recent": 0}
    seq = [three, two, two, [em] + two[1:]]  # ultimul: `em` cu r/t (din plane()), restul fără
    reasons = []
    for k, acs in enumerate(seq):
        t = T0 + dt.timedelta(seconds=100 + 30 * k)
        reasons.append(feed(an, "LRIA", LRIA, 30, snap(acs, t), t)["coverage"]["reason"])
    # ≥ 3 fără DB → „fara_db”, rămâne așa și cu 2 aeronave; o aeronavă cu r/t confirmă din nou DB-ul
    assert reasons == ["fara_db", "fara_db", "fara_db", "ok"]


def test_update_drops_military_even_without_aircraft_list():
    an = A.AdsbAnalyzer()
    mil = [plane(h, *offset(LRIA, 5, i), dbFlags=f, squawk="7700", emergency="general", nac_p=3, nic=2)
           for i, (h, f) in enumerate(zip(hexes(4, "c"), (1, "1", 3, 9.0)))]
    for k in range(3):
        t = T0 + dt.timedelta(seconds=30 * k)
        r = an.update("LRIA", *LRIA, 30, mil, t, A.snapshot_meta(snap(mil, t)))
        assert (r["civil_total"], r["civil_airborne"], r["emergencies"], r["gnss"]["n"]) == (0, 0, [], 0)
    assert an.state_size()["LRIA"] == {"tracks": 0, "gnss": 0, "emergencies": 0, "dedup": 0, "recent": 0}


def test_mlat_position_on_adsb_icao_excluded_from_gnss():
    def run(src):
        an = A.AdsbAnalyzer()
        acs = gnss_fleet(5) + [plane("ab72ca", *offset(LRIA, 3, 3), nac_p=3, nic=2, mlat=src)]
        return feed(an, "LRIA", LRIA, 30, snap(acs, T0), T0)
    r = run(["lat", "lon", "nic", "rc"])  # poziție MLAT: nic/rc nu vin de la aeronavă
    assert r["gnss"]["n"] == 5 and r["gnss"]["degraded"] == 0 and r["civil_mlat"] == 1
    r = run([])
    assert r["gnss"]["n"] == 6 and r["gnss"]["degraded"] == 1 and r["civil_mlat"] == 0


def test_out_of_range_coordinates_are_not_placed():
    # lat 407.178 / lon 387.621 cad (modulo 360) exact peste LRIA: fără verificarea domeniului,
    # haversine le-ar plasa în zonă; trebuie să rămână neplasabile
    base = {"hex": "ab89ca", "r": "X", "type": "adsb_icao", "alt_baro": 30000, "gs": 450.0, "seen": 0.5}
    acs = [dict(base, lat=407.178, lon=27.621, seen_pos=1.0),
           dict(base, hex="ab8aca", lat=47.178, lon=387.621, seen_pos=1.0),
           dict(base, hex="ab8bca", lastPosition={"lat": -132.822, "lon": 27.621, "seen_pos": 70.0},
                gpsOkBefore=T0.timestamp() - 60, gpsOkLat=407.178, gpsOkLon=27.621)]
    local = {"now": T0.timestamp(), "messages": 1, "aircraft": acs}
    r = feed(A.AdsbAnalyzer(), "LRIA", LRIA, 30, local, T0)
    assert (r["civil_total"], r["civil_unplaced"]) == (0, 3)


def test_json_separate_ground_not_airborne():
    acs = [plane("ab73ca", *LRIA, alt_baro=525, ground=True, gs=5.0),
           plane("ab74ca", *offset(LRIA, 5, 5), alt_baro=9000, ground=False)]
    r = feed(A.AdsbAnalyzer(), "LRIA", LRIA, 30, snap(acs, T0), T0)
    assert (r["civil_total"], r["civil_airborne"]) == (2, 1)


def test_maneuver_alert_counts_distinct_aircraft():
    an = A.AdsbAnalyzer()
    start = offset(LRIA, -40, 10)
    out = fly(start, 90.0, 230.0, 17, turns=[(540, 600, 3.0)])  # 9 min E, viraj 180°, 7 min V
    last = out[-1]
    fix = offset(last, -230 * 60 / 3600.0, 0)
    out += holding_positions(fix, 16, inbound=270.0, enter_s=60)[1:]  # apoi intră în așteptare
    res = run_track(an, "LRIA", LRIA, out, airliner("aa0afb", alt=12000, gs=230.0))
    both = [r for r in res if r["holding_recent"] and r["turnbacks"]]
    assert both, "traiectoria trebuie să producă și întoarcere, și așteptare"
    assert all(r["maneuver_aircraft"] == 1 and r["maneuver_alert"] is False for r in both)


HOSTILE = [
    '{"hex":"ab80ca","dbFlags":Infinity,"alt_baro":9000,"lat":47.2,"lon":27.6}',
    '{"hex":"ab81ca","dbFlags":NaN,"alt_baro":9000,"lat":47.2,"lon":27.6}',
    '{"hex":"ab82ca","r":"X","alt_baro":9000,"lat":1' + "0" * 400 + ',"lon":27.6,"gs":450}',
    '{"hex":"ab83ca","r":"X","alt_baro":9000,"lat":999,"lon":-500,"gs":450,"seen_pos":1}',
    '{"hex":"ab84ca","r":"X","type":"adsb_icao","alt_baro":30000,"gs":450,"lat":47.2,"lon":27.6,'
    '"mlat":5,"tisb":{"a":1},"version":2,"nac_p":3,"nic":2,"seen_pos":1}',
    '{"hex":"ab85ca","r":"X","alt_baro":30000,"gs":450,"lat":47.2,"lon":27.6,"emergency":["general"],'
    '"squawk":7700,"category":5}',
    '{"hex":123,"r":"X","alt_baro":[1],"gs":"fast","lat":"47","lon":null,"seen":"x","seen_pos":-1}',
    '{"hex":"ab86ca","r":"X","alt_baro":30000,"gs":450,"lastPosition":"x","gpsOkBefore":"y",'
    '"gpsOkLat":95,"gpsOkLon":27}',
    '{"hex":"ab87ca","r":"X","alt_baro":30000,"gs":450,"lastPosition":{"lat":1e400,"lon":27,"seen_pos":5}}',
    '{"hex":"ab88ca","r":"X","alt_baro":1e400,"gs":-1e400,"lat":47.2,"lon":27.6,"track":NaN}',
]


@pytest.mark.parametrize("text", HOSTILE)
@pytest.mark.parametrize("wrap", ["ac", "aircraft"])
def test_hostile_aircraft_never_crash(text, wrap):
    body = json.loads('{"%s":[%s, 42, "x", null],"now":%s}'
                      % (wrap, text, int(T0.timestamp() * (1000 if wrap == "ac" else 1))))
    an = A.AdsbAnalyzer(control_area="control")
    for k in range(3):
        t = T0 + dt.timedelta(seconds=30 * k)
        body["now"] = int(t.timestamp() * (1000 if wrap == "ac" else 1))
        r = an.update("LRIA", *LRIA, 30, A.aircraft_list(body), t, A.snapshot_meta(body))
        json.dumps(r, allow_nan=False)
    for bad in (None, 42, "x", {"a": 1}):
        an.update("LRIA", *LRIA, 30, bad, T0 + dt.timedelta(minutes=5), {"ok": True})


def test_seed_counts_accepts_store_rows_and_naive_times():
    import os
    import time
    from veghe.timeutil import iso

    rows = [(iso(T0 - dt.timedelta(minutes=90 - k * 5)), 4) for k in range(15)]  # ca store.adsb_samples
    rows += [("garbage", 9), (None, 9), (iso(T0), None), (1,), "x", (iso(T0 - dt.timedelta(minutes=30)), -1)]
    old_tz = os.environ.get("TZ")
    try:  # un fus orar local ≠ UTC: un datetime fără fus trebuie tratat ca UTC, ca în update()
        os.environ["TZ"] = "America/New_York"  # UTC−5: .timestamp() pe un datetime naiv ar fi +5 h
        time.tzset()
        for seed in (rows, [(dt.datetime.fromisoformat(s).replace(tzinfo=None), n) for s, n in rows[:15]]):
            an = A.AdsbAnalyzer()
            an.update("LRIA", *LRIA, 30, [], T0 - dt.timedelta(minutes=1),
                      {"data_now": (T0 - dt.timedelta(minutes=1)).timestamp()})
            an.seed_counts("LRIA", seed)  # după un update: ordinea în timp e refăcută
            ts = [s[0] for s in an._areas["LRIA"].counts]
            assert ts == sorted(ts) and len(ts) == 16
            rs = [an.update("LRIA", *LRIA, 30, [], (T0 + dt.timedelta(minutes=k)).replace(tzinfo=None),
                            {"data_now": (T0 + dt.timedelta(minutes=k)).timestamp()}) for k in range(3)]
            assert rs[-1]["drop"]["baseline"] == 4.0 and rs[-1]["drop"]["real"] is True
        # prune() cu un datetime fără fus = UTC (ca update())
        an = A.AdsbAnalyzer()
        em = plane("ab7fca", *offset(LRIA, 5, 5), squawk="7700")
        for k in range(2):
            t = T0 + dt.timedelta(seconds=30 * k)
            feed(an, "LRIA", LRIA, 30, snap([em], t), t)
        an.prune((T0 + dt.timedelta(minutes=2)).replace(tzinfo=None))
        assert an.state_size()["LRIA"]["emergencies"] == 1  # încă în TTL (5 min), nu decalat cu +5 h
    finally:
        if old_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = old_tz
        time.tzset()


# ------------------------------------------------------------------ eligibilitate (anti-vacuitate)
@pytest.mark.parametrize("kw,expect", [
    ({}, (1, 0)),  # referință: o aeronavă bună
    ({"nic": 0, "nac_p": 10}, (1, 0)),  # NIC 0 = necunoscut, acceptat cu NACp ≥ 10
    ({"nic": 0, "nac_p": 9}, (1, 1)),  # NIC 0 cu NACp 9: degradat
    ({"nac_p": 7}, (1, 1)),
    ({"nic": 6}, (1, 1)),
    ({"seen_pos": 45.0}, (0, 0)),  # poziție veche: nu se clasifică
    ({"category": "C1"}, (0, 0)),  # vehicul de sol
    ({"version": 0}, (0, 0)),  # v0: nac_p dedus din codul de tip
    ({"seen": 40.0}, (0, 0)),  # niciun mesaj de 40 s: în afara analizelor pe aeronavă
])
def test_gnss_eligibility_and_classification(kw, expect):
    acs = [plane("ab90ca", *offset(LRIA, 4, 4), alt_baro=30000, gs=450.0, **kw)]
    g = feed(A.AdsbAnalyzer(), "LRIA", LRIA, 30, snap(acs, T0), T0)["gnss"]
    assert (g["n"], g["degraded"]) == expect


@pytest.mark.parametrize("alt,expect", [(36000, 1), (1000, 0)])
def test_gnss_lost_needs_altitude(alt, expect):
    acs = gnss_fleet(0, 0, 1)
    acs[0]["alt_baro"] = alt
    g = feed(A.AdsbAnalyzer(), "LRIA", LRIA, 30, snap(acs, T0), T0)["gnss"]
    assert g["lost"] == expect


def test_emergency_ignored_when_aircraft_not_seen_recently():
    an = A.AdsbAnalyzer()
    em = plane("ab91ca", *offset(LRIA, 9, 9), squawk="7700", emergency="general", seen=40.0)
    for k in range(4):
        t = T0 + dt.timedelta(seconds=30 * k)
        assert feed(an, "LRIA", LRIA, 30, snap([em], t), t)["emergencies"] == []


def test_old_positions_flag_coverage():
    acs = [plane(h, *offset(LRIA, i, i), seen_pos=40.0) for i, h in enumerate(hexes(5, "a"))]
    r = feed(A.AdsbAnalyzer(), "LRIA", LRIA, 30, snap(acs, T0), T0)
    assert r["coverage"]["reason"] == "pozitii_vechi" and r["coverage"]["median_seen_pos_s"] == 40.0


def test_baseline_excludes_last_ten_minutes():
    an = A.AdsbAnalyzer()
    seed = [(T0 - dt.timedelta(minutes=110 - 7 * k), 5) for k in range(12)]  # 2 h … 33 min înainte
    seed += [(T0 - dt.timedelta(seconds=30 * k), 0) for k in range(1, 19)]  # ultimele 9 min: 0
    an.seed_counts("LRIA", seed)
    r = an.update("LRIA", *LRIA, 30, [], T0, {"data_now": T0.timestamp()})
    assert r["drop"]["baseline"] == 5.0


def test_track_points_use_data_time():
    # datele au 30 s (sub pragul de 45 s): momentul poziției = now din date − seen_pos, nu ceasul local
    an = A.AdsbAnalyzer()
    ac = plane("ab92ca", *offset(LRIA, 4, 4), alt_baro=12000, gs=230.0, seen_pos=2.0)
    feed(an, "LRIA", LRIA, 30, snap([ac], T0 - dt.timedelta(seconds=30)), T0)
    (tr,) = an._areas["LRIA"].tracks.values()
    assert tr.pts[-1][0] == pytest.approx(T0.timestamp() - 32.0, abs=1e-3)


def orbit(center, gs, rate, minutes):
    """Cerc continuu (rate °/s), eșantion la 60 s."""
    return fly(offset(center, 0, 0), 0.0, gs, minutes, turns=[(0, minutes * 60, rate)])


def test_large_orbit_not_turnback():
    # orbită lentă (0,5 °/s, rază ~14 NM): direcția se inversează, dar segmentele nu sunt drepte
    an = A.AdsbAnalyzer()
    res = run_track(an, "LRIA", LRIA, orbit(offset(LRIA, -14, 0), 450.0, 0.5, 25),
                    airliner("ab93ca", alt=35000, gs=450.0))
    assert all(r["turnbacks"] == 0 and r["holding"] == 0 for r in res)


def test_long_racetrack_too_large_for_holding():
    # bucle cu picioare de 3 min la 450 kt (~22 NM): D/L ≈ 0, dar rază față de centroid > 10 NM
    pos = []
    for i in range(25):
        x, y = racetrack_xy(i * 60.0 + 7.0, v=450.0, leg_s=180.0, turn_s=60.0)
        pos.append(offset(offset(LRIA, 0, -10), x, y))
    res = run_track(A.AdsbAnalyzer(), "LRIA", LRIA, pos, airliner("ab94ca", alt=30000, gs=450.0))
    assert all(r["holding"] == 0 and r["holding_recent"] == 0 for r in res)
    res = run_track(A.AdsbAnalyzer(loiter_max_radius_nm=30.0), "LRIA", LRIA, pos,
                    airliner("ab94ca", alt=30000, gs=450.0))
    assert any(r["holding"] for r in res)  # aceeași traiectorie, fără limita de rază: ar fi „așteptare”
