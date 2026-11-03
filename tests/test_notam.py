"""NOTAM: parser ICAO, clasificare, distanțe, colector (ROMATSA WFS, FAA NMS, text) pe server local.

Fixturile sunt înregistrări reale copiate verbatim (proveniența: fixtures/notam_SURSE.txt).
Exemplele LUUU sunt SINTETICE: nu s-a găsit niciun NOTAM moldovenesc verbatim.
"""

import copy
import datetime as dt
import gzip
import json
import pathlib
import ssl
import threading
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from veghe import geo, http
from veghe import notam as N
from veghe.timeutil import UTC

FIX = pathlib.Path(__file__).parent / "fixtures"
NOW = dt.datetime(2026, 8, 3, 12, 30, tzinfo=UTC)  # captura ROMATSA: 2026-08-03T12:26Z


def T(*a):
    return dt.datetime(*a, tzinfo=UTC)


def wfs():
    return json.loads((FIX / "notam_romatsa_wfs.json").read_text(encoding="utf-8"))


def text_list():
    return {n.id: n for n in N.parse_notam_text((FIX / "notam_text_list.txt").read_text(encoding="utf-8"))}


def mesaj(serie):
    return next(f["properties"]["mesaj"] for f in wfs()["features"] if f["properties"]["serie"] == serie)


# --- exemple verbatim din avwx-engine tests/current/test_notam.py și data/notam_parse_cases.json (MIT)
AVWX_PERM = """
A3475/22 NOTAMN
Q) LIMM/QFAXX/IV/NBO/A/000/999/4537N00843E005
A) LIMC B) 2205182200 C) PERM
E) REF AIP AD 2 LIMC 1-12 ITEM 20 'LOCAL TRAFFIC REGULATIONS'
BOX 2 'APRON' PARAGRAPH 2.1 'ORDERLY MOVEMENT OF AIRCRAFT ON
APRONS' INDENT 4 'SERVICES PROVIDED' POINT C) 'FOLLOW-ME ASSISTANCE
PROVIDED ON PILOT'S REQUEST AND MANDATORY IN CASE' ADD THE FOLLOWING
IN CASE:
"""
AVWX_AFTN = ("ORIGINAL NOTAM\r\n(A3230/26 NOTAMN\r\nQ)FAJA/QRACA/IV/NBO/AW/000/160/2546S02719E005\r\n"
             "A)FAXX B)2609160400 C)2612141600\r\nE)TEMPO DROP ZONE ESTABLISHED.\r\nF)SFC G)16000FT AMSL)")
AVWX_PAREN = ("A0001/26 NOTAMN\nQ) RJJJ/QRRCA/IV/BO/W/000/260/3500N13900E010\nA) RJJJ\n"
              "B) 2609300245 C) 2609300330\nE) AIRSPACE AR112H(F) ACT")
AVWX_CLSD = ("P4594/26 NOTAMN\nQ) UHMM/QRTCA/IV/BO/W/000/150/5629N16049E042\n"
             "A) UHMM B) 2608272300 C) 2608280800\nE) AIRSPACE CLSD WI AREA\nF) SFC  G) FL150")
AVWX_BADTIME = ("A1111/25 NOTAMR A1110/25 Q) ANYN/QKKKK/K/K/K/000/999/0032S16655E000 A) ANYN "
                "B) 2604018000 C) 2605018000 EST E) CHECKLIST YEAR=2025 0076 0080 0079")
AVWX_SUAS = ("M1128/26 NOTAMN \nQ) RJJJ/QWXXX/IV/NBO/A/000/999/3544N13920E005 \nA) RJTY \nB) 2609230518 \n"
             "C) 2610151450 \nE) USE CAUTION: SUAS OPERATIONS CONDUCTED 2NM SOUTH OF AFLD/354254N1392144E "
             "FROM SFC-UNK BETWEEN 0000Z-1450Z DAILY")
AVWX_TWY = ("F0910/26 NOTAMN\nQ)RJJJ/QMXLC/IV/M/A/000/999/3335N13027E005\n"
            "A)RJFF B)2609011400 C)2609272130\nD)01-14 19-23 26-27 1400/2130\n"
            "E)TWY A(FM K1 TO E8),ACFT STAND TXL K1 THRU K7,Y CLSD DUE TO MAINT")

# --- SINTETIC: format ICAO, conținut construit după știrile din 28–29 nov. 2025 (închidere 22:43–23:53 ora MD)
LUUU_CLOSED = """(A0123/25 NOTAMN
Q) LUUU/QAFLC/IV/NBO/E/000/999/4700N02850E999
A) LUUU B) 2511282043 C) 2511282153
E) AIRSPACE CLOSED DUE TO UAV ACTIVITY.
F) GND G) UNL)"""
LUUU_CANCEL = """(A0124/25 NOTAMC A0123/25
Q) LUUU/QAFAK/IV/NBO/E/000/999/4700N02850E999
A) LUUU B) 2511282130
E) AIRSPACE RESUMED NORMAL OPS.)"""
LUUU_NORTH_R = """(A0125/25 NOTAMR A0123/25
Q) LUUU/QRTCA/IV/BO/W/000/999/4800N02800E040
A) LUUU B) 2511282130 C) 2511290100 EST
E) TEMPORARY RESTRICTED AREA ACTIVATED IN THE NORTH OF CHISINAU FIR.
F) GND G) UNL)"""


# =========================================================================== parser
def test_parse_romatsa_c8116_verbatim():
    n = N.parse_icao_notam(mesaj("C8116/2025"))
    assert (n.id, n.type, n.ref, n.fir, n.qcode, n.subject, n.condition) == ("C8116/25", "N", None, "LRBB", "QRTCA", "RT", "CA")
    assert (n.series, n.number, n.year) == ("C", 8116, 2025)
    assert (n.traffic, n.purpose, n.scope, n.lower_fl, n.upper_fl, n.radius_nm) == ("IV", "BO", "W", 0, 130, 22)
    assert n.lat == pytest.approx(45 + 7 / 60) and n.lon == pytest.approx(29 + 13 / 60)
    assert n.locations == ["LRBB"]
    assert (n.start, n.end, n.estimated, n.permanent) == (T(2025, 7, 1, 5, 15), T(2025, 7, 31, 23, 59), False, False)
    assert n.text.startswith("TEMPORARY RESTRICTED AREA FOR VFR AND UNMANNED ACFT FLT\nWILL TAKE PLACE")
    assert n.text.endswith("EXPECT RADAR VECTORING") and n.text.count("\n") == 5
    assert (n.lower, n.upper) == ("GND", "FL130")


def test_parse_schedule_d():
    n = N.parse_icao_notam(mesaj("P2581/2026"))
    assert n.schedule == "DAILY 1630-0430" and n.upper == "FL065"
    assert n.text.startswith("TEMPORARY RESTRICTED AREA FOR IFR, VFR AND UNMANNED ACFT FLT")


def test_parse_tolerates_lowercase_crlf_and_spaces():
    ref = N.parse_icao_notam(mesaj("C8116/2025"))
    for variant in (mesaj("C8116/2025").lower(), mesaj("C8116/2025").replace("\r", "\r\n"),
                    "   " + mesaj("C8116/2025").replace(") ", ")   ")):
        n = N.parse_icao_notam(variant)
        assert (n.id, n.qcode, n.lat, n.start, n.end, n.upper) == (ref.id, ref.qcode, ref.lat, ref.start, ref.end, ref.upper)
        assert " ".join(n.text.split()) == " ".join(ref.text.split())


@pytest.mark.parametrize("nid,typ,ref,fir,qcode,end,est,perm", [
    ("A4460/24", "R", "A2844/24", "OIIX", "QAFXX", T(2025, 2, 9, 20, 30), True, False),   # EST lipit, pe un rând
    ("G0105/26", "R", "G0552/25", "URRV", "QGWXX", T(2026, 9, 24, 12, 59), True, False),  # „ EST” cu spațiu
    ("A1484/26", "R", "A8778/25", "UUWV", "QFALC", T(2026, 12, 26, 20, 59), False, False),
    ("A5862/25", "N", None, "LTAA", "QARLC", T(2026, 12, 31, 23, 59), False, False),
    ("J0249/26", "N", None, "SBBS", "QRRCH", None, False, True),                          # PERM
    ("A1136/25", "N", None, "PAZA", "QXXXX", T(2026, 9, 11, 23, 59), False, False),       # Q cu câmpuri goale
    ("B1216/26", "R", "B1215/26", "MMFR", "QRDCA", T(2026, 9, 15, 15, 0), False, False),  # Q fără coordonate
    ("P2580/26", "N", None, "LRBB", "QRTCA", T(2026, 8, 31, 23, 59), False, False),       # E pe mai multe rânduri
])
def test_parse_real_samples(nid, typ, ref, fir, qcode, end, est, perm):
    n = text_list()[nid]
    assert (n.type, n.ref, n.fir, n.qcode, n.end, n.estimated, n.permanent) == (typ, ref, fir, qcode, end, est, perm)
    assert n.text and not n.text.endswith(")") and "CREATED:" not in n.text


def test_parse_real_sample_details():
    ns = text_list()
    assert len(ns) == 8
    assert ns["A4460/24"].fir_wide and "MOLDOVA (LUUU)" in ns["A4460/24"].text and ns["A4460/24"].text.endswith("FROM GND TO UNL")
    assert ns["A1484/26"].text == "AD CLSD DUE TO MISSILE ALERT."             # fără „CREATED: … SOURCE: …”
    assert "A) AWY W/UW75 CLSD TO TFC" in " ".join(ns["A5862/25"].text.split())  # „A)” din E nu taie textul
    assert (ns["J0249/26"].lower, ns["J0249/26"].upper) == ("FL240", "UNL")
    assert ns["A1136/25"].traffic is None and ns["A1136/25"].lat is None and ns["A1136/25"].locations == ["PAZA"]
    assert ns["B1216/26"].lat is None and ns["B1216/26"].lower_fl == 0
    assert ns["P2580/26"].text.count("\n") == 6


def test_parse_avwx_edge_cases():
    n = N.parse_icao_notam(AVWX_PERM)
    assert n.permanent and n.end is None and n.start == T(2022, 5, 18, 22, 0)
    assert "POINT C) 'FOLLOW-ME ASSISTANCE" in n.text  # „C)” din E nu e cheie
    n = N.parse_icao_notam(AVWX_AFTN)  # mesaj AFTN, chei fără spațiu
    assert (n.id, n.fir, n.locations, n.text, n.lower, n.upper) == ("A3230/26", "FAJA", ["FAXX"], "TEMPO DROP ZONE ESTABLISHED.",
                                                                  "SFC", "16000FT AMSL")
    assert n.lat == pytest.approx(-(25 + 46 / 60))
    n = N.parse_icao_notam(AVWX_PAREN)
    assert n.text == "AIRSPACE AR112H(F) ACT" and n.lower is None
    n = N.parse_icao_notam(AVWX_CLSD)
    assert (n.lower, n.upper, n.text) == ("SFC", "FL150", "AIRSPACE CLSD WI AREA")
    n = N.parse_icao_notam(AVWX_BADTIME)  # ore imposibile: restul se citește
    assert (n.id, n.type, n.ref, n.fir, n.start, n.end, n.estimated) == ("A1111/25", "R", "A1110/25", "ANYN", None, None, True)
    n = N.parse_icao_notam(AVWX_TWY)
    assert n.schedule == "01-14 19-23 26-27 1400/2130" and n.start == T(2026, 9, 1, 14, 0)


@pytest.mark.parametrize("garbage", ["", "   ", "hello world", "<html><body>Mentenanță</body></html>", "Q) ???",
                                     "E) doar text", "{\"type\": \"FeatureCollection\"}", None, 123, b"(A1234/26 NOTAMN"])
def test_parse_garbage_is_none(garbage):
    assert N.parse_icao_notam(garbage) is None


def test_parse_minimal_and_synthetic_luuu():
    n = N.parse_icao_notam("(A1234/26 NOTAMC A1200/26")
    assert (n.id, n.type, n.ref, n.text, n.qcode) == ("A1234/26", "C", "A1200/26", "", None)
    n = N.parse_icao_notam(LUUU_CLOSED)  # SINTETIC
    assert (n.fir, n.qcode, n.locations, n.fir_wide, n.start, n.end) == ("LUUU", "QAFLC", ["LUUU"], True,
                                                                         T(2025, 11, 28, 20, 43), T(2025, 11, 28, 21, 53))
    c = N.parse_icao_notam(LUUU_CANCEL)
    assert (c.type, c.ref, c.end, c.text) == ("C", "A0123/25", None, "AIRSPACE RESUMED NORMAL OPS.")


def test_parse_notam_text_comments_and_html_table():
    assert list(text_list()) == ["P2580/26", "A4460/24", "G0105/26", "A1484/26", "A5862/25", "J0249/26", "A1136/25", "B1216/26"]
    assert N.parse_notam_text("# doar un comentariu\n\n") == [] and N.parse_notam_text(None) == []
    # CONSTRUIT după selectorul ROvACC (div#content table TR; TD0 număr, TD1 locație, TD2 text cu <br>) – nu e o captură
    page = ("<html><body><div id='content'><table><tr><th>Nr</th><th>AD</th><th>NOTAM</th></tr>"
            "<tr><td>A1234/26</td><td>LRIA</td><td>Q) LRBB/QFALC/IV/NBO/A/000/999/4711N02737E005<br>"
            "A) LRIA B) 2611021800 C) 2611022200<br>E) AD CLSD.</td></tr>"
            "<tr><td>P2580/26</td><td>LRBB</td><td>" + mesaj("P2580/2026").replace("\r", "<br>") + "</td></tr>"
            "</table></div></body></html>")
    ns = N.parse_notam_text(page)
    assert [(n.id, n.qcode, n.locations) for n in ns] == [("A1234/26", "QFALC", ["LRIA"]), ("P2580/26", "QRTCA", ["LRBB"])]
    assert N.classify(ns[0]) == "aeroport_inchis" and ns[0].end == T(2026, 11, 2, 22, 0)


# =========================================================================== clasificare
@pytest.mark.parametrize("src,expected", [
    (lambda: N.parse_icao_notam(mesaj("P2580/2026")), "restrictie_spatiu_aerian"),
    (lambda: N.parse_icao_notam(mesaj("F8021/2026")), "drone_uas"),            # QWULW
    (lambda: N.parse_icao_notam(mesaj("F8008/2026")), "restrictie_spatiu_aerian"),  # QRRCA „UNAMNNED”
    (lambda: N.parse_icao_notam(mesaj("P2397/2026")), "restrictie_spatiu_aerian"),  # QRDCA trageri
    (lambda: N.parse_icao_notam(mesaj("M4430/2026")), None),                   # QWELW zboruri militare: rutină
    (lambda: text_list()["G0105/26"], "gnss"),
    (lambda: text_list()["A1136/25"], "gnss"),                                  # QXXXX + „GNSS INTERFERENCE”
    (lambda: text_list()["A1484/26"], "aeroport_inchis"),
    (lambda: text_list()["A5862/25"], "ruta_inchisa"),
    (lambda: text_list()["A4460/24"], None),                                    # avertizare de securitate, nu restricție
    (lambda: text_list()["B1216/26"], "restrictie_spatiu_aerian"),
    (lambda: N.parse_icao_notam(AVWX_CLSD), "spatiu_aerian_inchis"),
    (lambda: N.parse_icao_notam(AVWX_SUAS), "drone_uas"),
    (lambda: N.parse_icao_notam(AVWX_PERM), None),                              # QFAXX reguli de platformă
    (lambda: N.parse_icao_notam(AVWX_TWY), None),                               # cale de rulare închisă
    (lambda: N.parse_icao_notam(LUUU_CLOSED), "spatiu_aerian_inchis"),
    (lambda: N.parse_icao_notam(LUUU_CANCEL), "restrictie_ridicata"),
    (lambda: N.parse_icao_notam(LUUU_NORTH_R), "restrictie_spatiu_aerian"),
])
def test_classify(src, expected):
    assert N.classify(src()) == expected


def test_is_uas():
    assert N.is_uas(N.parse_icao_notam(mesaj("P2580/2026")))       # „UNMANNED ACFT”
    assert N.is_uas(N.parse_icao_notam(mesaj("F8008/2026")))       # „UNAMNNED”
    assert N.is_uas(N.parse_icao_notam(AVWX_SUAS))
    assert not N.is_uas(N.parse_icao_notam(mesaj("P2738/2026")))


# =========================================================================== distanțe
def test_distances_polygon_and_prut():
    ns = {n.id: n for n in N.parse_romatsa_wfs(wfs())}
    d_t, d_p = N.distances(ns["P2580/26"])  # zonă la granița cu R. Moldova (Galați)
    assert 170 < d_t < 195 and d_p < 3
    d_t, d_p = N.distances(ns["F8021/26"])  # UAS lângă Prut, la sud de Iași
    assert 35 < d_t < 50 and d_p == 0.0
    assert N.distances(ns["P2397/26"])[0] < 15
    # aceeași zonă din coordonatele din E) (fără poligonul sursei) dă practic același rezultat
    n = N.parse_icao_notam(mesaj("P2580/2026"))
    assert abs(N.distances(n)[0] - N.distances(ns["P2580/26"])[0]) < 5


def test_distance_polygon_straddling_prut_is_zero():
    ring = [(46.80, 27.95), (46.80, 28.20), (46.70, 28.20), (46.70, 27.95)]  # traversează Prutul între Prisăcani și Leova
    assert not any(N._in_ring(p[0], p[1], ring) for p in geo.PRUT_LINE)  # niciun vârf al Prutului în interior
    n = N.Notam(id="X0001/26", polygons=[ring])
    assert N.distances(n)[1] == 0.0
    n = N.Notam(id="X0002/26", polygons=[[(47.3, 27.5), (47.3, 27.7), (47.0, 27.7), (47.0, 27.5)]])  # conține Iașiul
    assert N.distances(n)[0] == 0.0


def test_distance_circle_firwide_and_unknown():
    n = N.Notam(id="X0003/26", lat=47.05, lon=27.5333, radius_nm=2)
    d = geo.haversine_km(47.05, 27.5333, geo.IASI.lat, geo.IASI.lon) - 2 * 1.852
    assert N.distances(n)[0] == pytest.approx(d, abs=0.1)
    luuu = N.parse_icao_notam(LUUU_CLOSED)
    d_t, d_p = N.distances(luuu)
    assert d_p == 0.0 and 0 < d_t < 25  # Iași – Prut
    assert N.distances(N.Notam(id="X", fir="LRBB", radius_nm=999, lat=46.0, lon=25.0)) == (0.0, 0.0)
    assert N.distances(text_list()["A4460/24"]) == (None, None)  # FIR străin pe tot cuprinsul
    assert N.distances(text_list()["B1216/26"]) == (None, None)  # fără niciun reper


def test_is_near():
    assert N.is_near(10, None) and N.is_near(None, 5) and N.is_near(100, 5)
    assert not N.is_near(180, 0.3)  # granița de la Galați: lângă Prut, dar departe de Iași
    assert not N.is_near(None, None) and not N.is_near(70, 40)


# =========================================================================== text pentru mesaje
def test_scrub_and_summary():
    assert N.scrub_contacts("CTC OPS +40 700 000 000 OR TEL 0700 000 000, OPS(AT)EXAMPLE.ORG, a@b.ro, 310-555-0100") == \
        "CTC OPS [tel] OR [tel], [email], [email], [tel]"
    assert N.scrub_contacts("451745N0284737E-451314N0293944E FL110-FL450 1630-0430") == \
        "451745N0284737E-451314N0293944E FL110-FL450 1630-0430"  # coordonatele și orele rămân
    n = text_list()["A1136/25"]
    assert "907-269-1930" not in N.summary(n, "nou", "gnss", None, None)
    s = N.summary(N.parse_icao_notam(mesaj("P2580/2026")), "nou", "restrictie_spatiu_aerian", 180.0, 0.3)
    assert s.startswith("NOTAM P2580/26 · restricție de spațiu aerian (QRTCA), menționează drone/UAS · LRBB · ~180 km de Iași")
    assert "01.08 03:00 EEST – 01.09 02:59 EEST" in s and "GND–FL240" in s and "[coord.]" in s


# =========================================================================== colector (fără rețea)
def ids(sigs, kind=None):
    return sorted(s.meta["id"] for s in sigs if kind is None or s.meta["kind"] == kind)


def test_process_romatsa_relevance_and_meta():
    c = N.NotamCollector()
    sigs = c.process(N.parse_romatsa_wfs(wfs()), 11, NOW)
    # C8116/25 expirat; F8015, F8008, P2263 prea departe; M4430 (QWELW) irelevant
    assert ids(sigs) == ["F8021/26", "P2397/26", "P2578/26", "P2580/26", "P2581/26", "P2738/26"]
    by = {s.meta["id"]: s for s in sigs}
    for s in sigs:
        assert s.role == "notam" and s.source == "notam:romatsa" and s.ext_id == f"LR:{s.meta['id']}|nou"
        assert s.meta["key"] == f"LR:{s.meta['id']}" and s.meta["area"] == "polygon"
        assert s.published_at <= NOW
        json.dumps(s.meta)  # serializabil
        assert set(s.meta) >= {"id", "kind", "replaces", "fir", "qcode", "category", "lat", "lon", "radius_nm", "lower_fl",
                               "upper_fl", "start", "end", "estimated", "locations", "text", "dist_iasi_km", "dist_prut_km",
                               "near", "ends", "continua", "uas", "key", "ends_key", "area"}
    assert {k for k, s in by.items() if s.meta["near"]} == {"F8021/26", "P2397/26", "P2738/26"}
    assert by["F8021/26"].meta["category"] == "drone_uas" and by["P2580/26"].meta["uas"] is True
    assert by["P2580/26"].published_at == T(2026, 8, 1) and by["P2580/26"].meta["start"] == "2026-08-01T00:00:00+00:00"
    assert by["P2397/26"].published_at == NOW  # începe pe 5 august: „publicat” = când l-am văzut
    # a doua citire: aceleași chei (arhiva deduplică), nimic retras
    again = c.process(N.parse_romatsa_wfs(wfs()), 11, NOW + dt.timedelta(minutes=15))
    assert sorted(s.key() for s in again) == sorted(s.key() for s in sigs)


def test_process_withdrawn_outage_and_reissue():
    c = N.NotamCollector()
    c.process(N.parse_romatsa_wfs(wfs()), 11, NOW)
    t1 = NOW + dt.timedelta(minutes=15)
    # pană: răspuns gol sau mult mai mic → nimic „retras”
    assert c.process([], 0, t1) == []
    few = [n for n in N.parse_romatsa_wfs(wfs()) if n.id == "P2580/26"]
    assert ids(c.process(few, 1, t1), "retras") == []
    # P2738/26 (valabil până la 17:40) dispare dintr-un răspuns normal → „retras”
    rest = [n for n in N.parse_romatsa_wfs(wfs()) if n.id != "P2738/26"]
    sigs = c.process(rest, 10, t1)
    gone = [s for s in sigs if s.meta["kind"] == "retras"]
    assert ids(gone) == ["P2738/26"] and gone[0].ext_id == "LR:P2738/26|retras" and gone[0].meta["ends"] == "P2738/26"
    assert gone[0].meta["ends_key"] == "LR:P2738/26"
    assert gone[0].published_at == t1 and "retras înainte de expirare" in gone[0].text
    # reemitere sub alt număr, același conținut → „continua”
    later = NOW + dt.timedelta(days=1)
    data = wfs()
    f = next(x for x in data["features"] if x["properties"]["serie"] == "P2580/2026")
    f2 = copy.deepcopy(f)
    f2["properties"]["mesaj"] = f2["properties"]["mesaj"].replace("P2580/26", "P2799/26")
    data["features"].append(f2)
    sigs = c.process(N.parse_romatsa_wfs(data), 12, later)
    by = {s.meta["id"]: s for s in sigs}
    assert by["P2799/26"].meta["continua"] == "P2580/26" and by["P2580/26"].meta["continua"] is None


def test_process_luuu_replace_and_cancel_synthetic():
    c = N.NotamCollector(name="test", source="text", urls=["http://x/"])
    now = T(2025, 11, 28, 21, 0)
    s = c.process([N.parse_icao_notam(LUUU_CLOSED)], 1, now)  # SINTETIC
    assert len(s) == 1 and s[0].meta["category"] == "spatiu_aerian_inchis" and s[0].meta["near"]
    assert s[0].meta["fir_wide"] and s[0].meta["dist_prut_km"] == 0.0
    # NOTAMR: restricția din nord înlocuiește închiderea → nu apare „retras” pentru A0123/25
    s = c.process([N.parse_icao_notam(LUUU_NORTH_R)], 1, now + dt.timedelta(minutes=35))
    assert [(x.meta["kind"], x.meta["ends"], x.meta["replaces"], x.meta["ends_key"]) for x in s] == \
        [("inlocuire", "A0123/25", "A0123/25", "LU:A0123/25")]
    assert s[0].meta["estimated"] and "(înlocuiește A0123/25)" in s[0].text
    # NOTAMC: anulează A0125/25? Nu – anulează A0123/25, deja urmărit → categoria lui
    c2 = N.NotamCollector(name="t2", source="text", urls=["http://x/"])
    c2.process([N.parse_icao_notam(LUUU_CLOSED)], 1, now)
    s = c2.process([N.parse_icao_notam(LUUU_CANCEL)], 1, now + dt.timedelta(minutes=30))
    assert [(x.meta["kind"], x.meta["ends"], x.meta["category"], x.ext_id) for x in s] == \
        [("anulare", "A0123/25", "spatiu_aerian_inchis", "LU:A0124/25|anulare")]


def test_collector_options_validated():
    with pytest.raises(ValueError, match="sursă NOTAM necunoscută"):
        N.NotamCollector(source="ead")
    with pytest.raises(ValueError, match="categorii NOTAM necunoscute"):
        N.NotamCollector(categories=["toate"])
    with pytest.raises(ValueError, match="cel puțin un URL"):
        N.NotamCollector(source="text")
    with pytest.raises(N.NotamCredentialsError) as e:
        N.NotamCollector(source="faa_nms", client_id="id")
    assert "notams@faa.gov" in str(e.value) and "FAA_NMS_CLIENT_ID" in str(e.value)
    c = N.NotamCollector(interval=10, timeout=3, user_agent="ua-test")
    assert c.interval == 300 and c.timeout == 3 and c.user_agent == "ua-test" and c.urls == [N.ROMATSA_WFS_URL]
    assert N.NotamCollector().interval == 900
    only = N.NotamCollector(categories=["drone_uas"])
    assert ids(only.process(N.parse_romatsa_wfs(wfs()), 11, NOW)) == ["F8021/26"]


# =========================================================================== server HTTP local
class Fake:
    def __init__(self):
        self.routes = {}
        self.requests = []

    def hits(self, path):
        return [r for r in self.requests if r["path"].split("?")[0] == path]


@pytest.fixture()
def server():
    fake = Fake()

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _do(self, method):
            n = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(n) if n else b""
            fake.requests.append({"method": method, "path": self.path, "body": body,
                                  "headers": {k.lower(): v for k, v in self.headers.items()}})
            code, ctype, data, extra = fake.routes.get(self.path.split("?")[0], (404, "text/plain", b"nu", {}))
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            for k, v in extra.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            self._do("GET")

        def do_POST(self):
            self._do("POST")

    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    fake.base = f"http://127.0.0.1:{srv.server_address[1]}"
    yield fake
    srv.shutdown()


def route(fake, path, data, ctype="application/json", code=200, gz=False, **extra):
    body = data if isinstance(data, bytes) else (data if isinstance(data, str) else json.dumps(data)).encode("utf-8")
    hdrs = dict(extra)
    if gz:
        body, hdrs["Content-Encoding"] = gzip.compress(body), "gzip"
    fake.routes[path] = (code, ctype, body, hdrs)


def test_romatsa_over_http_gzip(server):
    route(server, "/geoserver/ows", wfs(), gz=True)
    c = N.NotamCollector(urls=[server.base + "/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature"], timeout=5)
    sigs = c.poll(NOW)
    assert ids(sigs) == ["F8021/26", "P2397/26", "P2578/26", "P2580/26", "P2581/26", "P2738/26"]
    req = server.hits("/geoserver/ows")[0]
    assert req["headers"]["accept"] == "application/json" and "gzip" in req["headers"]["accept-encoding"]
    assert c.last_raw == 11 and c.last_skipped == 0 and c.last_date  # antetul Date pentru verificarea ceasului


@pytest.mark.parametrize("payload,ctype,code,err,match", [
    (b"service unavailable", "text/plain", 503, http.HttpError, "503"),
    (b"<!doctype html><html><body>Mentenanta</body></html>", "text/html", 200, ValueError, "HTML/XML"),
    (b"{not json", "application/json", 200, ValueError, "nu e JSON"),
    (b'{"type": "Feature"}', "application/json", 200, ValueError, "FeatureCollection"),
    ((FIX / "notam_wfs_exception.xml").read_bytes(), "text/xml", 200, ValueError, "GeoServer: Feature type carto:strat_inexistent"),
])
def test_romatsa_errors(server, payload, ctype, code, err, match):
    route(server, "/ows", payload, ctype=ctype, code=code)
    c = N.NotamCollector(urls=[server.base + "/ows"], timeout=5)
    with pytest.raises(err, match=match):
        c.poll(NOW)


def test_romatsa_malformed_features_do_not_crash(server):
    data = wfs()
    data["features"] += [None, {}, "x", {"properties": None}, {"properties": {"mesaj": 123}},
                         {"properties": {"mesaj": "nimic util", "serie": "Z1/2026"}},
                         {"properties": {"mesaj": mesaj("P2738/2026").replace("P2738", "P2999")}, "geometry": {"type": "Polygon",
                                                                                                             "coordinates": "rupt"}}]
    route(server, "/ows", data)
    c = N.NotamCollector(urls=[server.base + "/ows"], timeout=5)
    sigs = c.poll(NOW)
    assert "P2999/26" in ids(sigs) and "P2738/26" in ids(sigs)  # fără geometrie: cercul din linia Q
    assert c.last_raw == 18 and c.last_skipped == 6


def test_text_source_over_http(server):
    route(server, "/notams.txt", (FIX / "notam_text_list.txt").read_text(encoding="utf-8"), ctype="text/plain; charset=utf-8")
    c = N.NotamCollector(name="lista", source="text", urls=server.base + "/notams.txt", timeout=5)
    sigs = c.poll(NOW)
    assert [s.ext_id for s in sigs] == ["LR:P2580/26|nou"] and sigs[0].source == "notam:lista"


# --- FAA NMS: format după dnickerson/flytab (token) și koala73/worldmonitor (date); LUUU = SINTETIC
LUUU_NMS = {"type": "Feature", "properties": {"coreNOTAMData": {"notamEvent": {"scenario": "982"}, "notam": {
    "id": "NMS_ID_0000000000000001", "series": "A", "number": "A0123/25", "year": "2025", "type": "N",
    "issued": "2025-11-28T20:40:00.000Z", "affectedFir": "LUUU", "selectionCode": "QAFLC", "traffic": "IV",
    "purpose": "NBO", "scope": "E ", "minimumFl": "000", "maximumFl": "999", "location": "LUUU",
    "effectiveStart": "2025-11-28T20:43:00.000Z", "effectiveEnd": "2025-11-28T21:53:00.000Z",
    "text": "AIRSPACE CLOSED DUE TO UAV ACTIVITY.", "classification": "INTL", "accountId": "LUKKYNYX",
    "lastUpdated": "2025-11-28T20:41:00.000Z", "icaoLocation": "LUUU", "lowerLimit": "GND", "upperLimit": "UNL",
    "coordinates": "4700N02850E", "radius": "999"}}},
    "geometry": {"type": "GeometryCollection", "geometries": [{"type": "Point", "coordinates": [28.833333, 47.0]}]}}
TOKEN = {"refresh_token_expires_in": "0", "token_type": "BearerToken values", "issued_at": "1752851243984",
         "client_id": "cid", "access_token": "TOK123", "scope": "", "expires_in": "1799", "status": "approved"}


def test_nms_parse_fixture():
    ns = {n.id: n for n in N.parse_nms(json.loads((FIX / "notam_nms_geojson.json").read_text(encoding="utf-8")))}
    assert set(ns) == {"J3386/26", "A0634/26", "A3651/26", "FDC 6/1966"}
    n = ns["J3386/26"]
    assert (n.type, n.fir, n.qcode, n.purpose, n.scope, n.upper_fl, n.radius_nm, n.lower, n.upper) == \
        ("R", "EGTT", "QRDCS", "BO", "AW", 999, 2, "SFC", "600FT AMSL")
    assert n.lat == pytest.approx(54.509167) and n.issued == T(2026, 9, 24, 11, 42) and not n.text.endswith(")")
    assert N.classify(n) == "restrictie_spatiu_aerian" and N.is_uas(n)
    assert ns["A3651/26"].permanent and ns["A3651/26"].end is None and N.classify(ns["A3651/26"]) is None  # QFALT
    assert N.classify(ns["A0634/26"]) == "aeroport_inchis" and ns["A0634/26"].text.endswith("BCST ON ATIS.")
    assert ns["FDC 6/1966"].type == "C"
    with pytest.raises(ValueError, match="status"):
        N.parse_nms({"status": "Error", "data": None})
    with pytest.raises(ValueError, match="geojson"):
        N.parse_nms({"status": "Success", "data": {}})


def test_nms_over_http(server):
    data = json.loads((FIX / "notam_nms_geojson.json").read_text(encoding="utf-8"))
    data["data"]["geojson"] += [LUUU_NMS, {"type": "Feature", "properties": {}}, None]
    route(server, "/v1/auth/token", TOKEN)
    route(server, "/nmsapi/v1/notams", data)
    c = N.NotamCollector(name="faa", source="faa_nms", client_id="cid", client_secret="sec", nms_host=server.base,
                         locations=["LSZH"], timeout=5)
    now = T(2025, 11, 28, 21, 0)
    sigs = c.poll(now)
    # EGNV, OERK, FDC: în afara zonei; LSZH (urmărit aici) începe în viitor, deci se păstrează
    assert sorted(s.ext_id for s in sigs) == ["LS:A0634/26|nou", "LU:A0123/25|nou"]
    s = next(x for x in sigs if x.meta["id"] == "A0123/25")
    assert s.meta["category"] == "spatiu_aerian_inchis" and s.meta["near"] and s.published_at == T(2025, 11, 28, 20, 40)
    tok = server.hits("/v1/auth/token")[0]
    assert tok["method"] == "POST" and tok["body"] == b"grant_type=client_credentials"
    assert tok["headers"]["authorization"] == "Basic Y2lkOnNlYw=="  # base64("cid:sec")
    get = server.hits("/nmsapi/v1/notams")[0]
    assert get["headers"]["authorization"] == "Bearer TOK123" and get["headers"]["nmsresponseformat"] == "GEOJSON"
    assert "latitude=47.0500" in get["path"] and "longitude=28.2000" in get["path"] and "radius=100" in get["path"]
    later = c.poll(T(2026, 10, 26, 23, 0))  # tokenul e refolosit; închiderea LUUU a expirat (nu e „retras”)
    assert len(server.hits("/v1/auth/token")) == 1 and ids(later) == ["A0634/26"]


def test_nms_auth_rejected(server):
    route(server, "/v1/auth/token", {"ErrorCode": "invalid_client"}, code=401)
    c = N.NotamCollector(name="faa", source="faa_nms", client_id="cid", client_secret="gresit", nms_host=server.base, timeout=5)
    with pytest.raises(N.NotamCredentialsError, match="HTTP 401") as e:
        c.poll(NOW)
    assert "gresit" not in str(e.value)  # secretul nu apare în mesaje


# =========================================================================== TLS
def test_tls_context_keeps_verification():
    for ciphers in (N.TLS_CIPHERS, N.TLS_CIPHERS_FALLBACK, "", "SIR-INVALID"):
        ctx = N.make_tls_context(ciphers)
        assert ctx.check_hostname and ctx.verify_mode == ssl.CERT_REQUIRED
    # fără schimb de chei DHE cu certificat (rămân doar suitele DHE-PSK, oferite numai cu un PSK configurat)
    kx = [c.get("kea") for c in N.make_tls_context(N.TLS_CIPHERS).get_ciphers()]
    assert kx and "kx-dhe" not in kx and "kx-dhe" in [c.get("kea") for c in ssl.create_default_context().get_ciphers()]


def test_request_with_context_plain_http(server):
    route(server, "/a", b"salut", ctype="text/plain", gz=True)
    route(server, "/b", b"nu acum", ctype="text/plain", code=503, **{"Retry-After": "120"})
    r = N.request_with_context(server.base + "/a", N.make_tls_context(), timeout=5)
    assert r.status == 200 and r.body == b"salut"
    with pytest.raises(http.HttpError) as e:
        N.request_with_context(server.base + "/b", None, timeout=5)
    assert e.value.status == 503 and e.value.retry_after == 120
    with pytest.raises(http.HttpError, match="prea mare"):
        route(server, "/c", b"x" * 5000, ctype="text/plain")
        N.request_with_context(server.base + "/c", None, timeout=5, max_bytes=1000)


def test_tls_only_for_romatsa_host_and_dh_fallback(monkeypatch):
    calls = []

    def fake(url, ctx, **kw):
        calls.append(ctx)
        if len(calls) == 1:
            raise urllib.error.URLError(ssl.SSLError(1, "[SSL: DH_KEY_TOO_SMALL] dh key too small"))
        return http.Response(200, {"date": "Mon, 03 Aug 2026 12:30:00 GMT"}, json.dumps(wfs()).encode())

    monkeypatch.setattr(N, "request_with_context", fake)
    c = N.NotamCollector(timeout=5)
    assert ids(c.poll(NOW))  # al doilea context (SECLEVEL=1) a mers
    assert len(calls) == 2 and calls[0] is not calls[1] and c._tls_relaxed
    assert all(x.verify_mode == ssl.CERT_REQUIRED for x in calls) and c.last_date
    # alt host https: nu trece pe aici (folosește http.request obișnuit)
    seen = []
    empty = b'{"status":"Success","data":{"geojson":[]}}'
    monkeypatch.setattr(N.http, "request", lambda url, **kw: seen.append(url) or http.Response(200, {}, empty))
    c2 = N.NotamCollector(name="faa", source="faa_nms", client_id="a", client_secret="b", nms_host="https://api-nms.aim.faa.gov")
    c2._token, c2._token_exp = "T", float("inf")
    assert c2.poll(NOW) == [] and seen and len(calls) == 2


# =========================================================================== regresii (revizie)
def nms_feature(number, fir, loc, qcode, text, start="2026-11-02T20:00:00.000Z", end="2026-11-03T02:00:00.000Z",
                typ="N", lat=47.0, lon=28.83, radius="999", **extra):
    """Feature NMS construit după câmpurile din worldmonitor (SINTETIC: conținutul, nu formatul)."""
    nd = {"id": f"NMS_ID_{number}", "number": number, "type": typ, "issued": start, "affectedFir": fir,
          "selectionCode": qcode, "traffic": "IV", "purpose": "NBO", "scope": "E ", "minimumFl": "000",
          "maximumFl": "999", "location": loc, "icaoLocation": loc, "effectiveStart": start, "effectiveEnd": end,
          "text": text, "classification": "INTL", "radius": radius}
    nd.update(extra)
    return {"type": "Feature", "properties": {"coreNOTAMData": {"notam": nd}},
            "geometry": {"type": "GeometryCollection", "geometries": [{"type": "Point", "coordinates": [lon, lat]}]}}


def test_same_number_in_two_countries_does_not_collide():
    # A0123/26 al LUUU (închidere) și A0123/26 al LRBB (zonă UAS lângă Prut): numere egale, birouri diferite
    data = {"status": "Success", "data": {"geojson": [
        nms_feature("A0123/26", "LUUU", "LUUU", "QAFLC", "AIRSPACE CLOSED DUE TO UAV ACTIVITY."),
        nms_feature("A0123/26", "LRBB", "LRBB", "QWULW", "UNMANNED ACFT FLT WILL TAKE PLACE.",
                    lat=47.1, lon=27.7, radius="005"),
    ]}}
    ns = N.parse_nms(data)
    assert sorted(N.notam_key(n) for n in ns) == ["LR:A0123/26", "LU:A0123/26"]
    c = N.NotamCollector(name="t", source="text", urls=["http://x/"])
    now = T(2026, 11, 2, 21, 0)
    sigs = c.process(ns, 2, now)
    assert sorted(s.ext_id for s in sigs) == ["LR:A0123/26|nou", "LU:A0123/26|nou"]
    assert len({s.key() for s in sigs}) == 2  # arhiva nu le mai deduplică una cu alta
    # NOTAMC al LRBB pentru A0123/26 nu încheie închiderea LUUU
    cancel = N.parse_icao_notam("(A0130/26 NOTAMC A0123/26\nQ) LRBB/QWUXX/IV/BO/W/000/010/4706N02742E005\n"
                                "A) LRBB B) 2611022110\nE) UAS FLT CNL)")
    sigs = c.process([ns[0], cancel], 2, now + dt.timedelta(minutes=15))
    anul = [s for s in sigs if s.meta["kind"] == "anulare"]
    assert [(s.meta["ends"], s.meta["ends_key"], s.meta["category"]) for s in anul] == [("A0123/26", "LR:A0123/26", "drone_uas")]
    assert "LU:A0123/26" in c._active and "LR:A0123/26" not in c._active
    assert N.nof_scope(N.Notam(id="X0001/26")) == "" and N.nof_scope(N.Notam(id="X", locations=["LRIA"])) == "LR"


@pytest.mark.parametrize("err,retries", [
    (urllib.error.URLError(ssl.SSLError(1, "[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure")), True),
    (urllib.error.URLError(ssl.SSLError(1, "[SSL: NO_CIPHERS_AVAILABLE] no ciphers available")), True),
    (ssl.SSLError(1, "[SSL: DH_KEY_TOO_SMALL] dh key too small"), True),
    (urllib.error.URLError(ssl.SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed")), False),
    (urllib.error.URLError(ConnectionRefusedError(111, "Connection refused")), False),
])
def test_tls_fallback_on_any_handshake_failure_but_not_cert(monkeypatch, err, retries):
    # cu „DEFAULT:!DH” nu se oferă DHE, deci un server doar-DHE dă „handshake failure”, nu DH_KEY_TOO_SMALL
    calls = []

    def fake(url, ctx, **kw):
        calls.append(ctx)
        if len(calls) == 1 or not retries:
            raise err
        return http.Response(200, {}, json.dumps(wfs()).encode())

    monkeypatch.setattr(N, "request_with_context", fake)
    c = N.NotamCollector(timeout=5)
    if retries:
        assert ids(c.poll(NOW)) and len(calls) == 2 and c._tls_relaxed
        assert all(x.verify_mode == ssl.CERT_REQUIRED and x.check_hostname for x in calls)
    else:
        with pytest.raises(type(err)):
            c.poll(NOW)
        assert len(calls) == 1 and not c._tls_relaxed


def test_tls_fallback_only_once(monkeypatch):
    calls = []

    def fake(url, ctx, **kw):
        calls.append(ctx)
        raise urllib.error.URLError(ssl.SSLError(1, "[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure"))

    monkeypatch.setattr(N, "request_with_context", fake)
    c = N.NotamCollector(timeout=5)
    for _ in range(3):
        with pytest.raises(urllib.error.URLError):
            c.poll(NOW)
    assert len(calls) == 4  # 2 la prima citire (normal + rezervă), apoi doar contextul de rezervă


@pytest.mark.parametrize("fn", [
    lambda: N.parse_notam_text("x" + " " * 200_000 + "x"),
    lambda: N.parse_icao_notam("(A1234/26 NOTAMN\nQ) LRBB/QRTCA/IV/BO/W/000/240/4517N02814E019\nE) " + " " * 200_000 + "X"),
    lambda: N.scrub_contacts("A" * 200_000),
    lambda: N.scrub_text("A" * 200_000 + " " + "1 " * 50_000),
    lambda: N.excerpt("YR" * 100_000),
])
def test_regex_linear_time_on_huge_input(fn):
    import time
    t0 = time.perf_counter()
    fn()
    assert time.perf_counter() - t0 < 1.5  # înainte: ~8 s pentru 40 000 de spații, ~23 s pentru 40 000 de litere


def test_regex_fixes_keep_semantics():
    assert N.parse_notam_text("   (A0001/26 NOTAMN\nQ) LRBB/QRTCA/IV/BO/W/000/240/4517N02814E019\nE) X)")[0].id == "A0001/26"
    n = N.parse_icao_notam("A1484/26 NOTAMR A8778/25  Q) UUWV/QFALC/IV/NBO/A/000/999/5039N03635E005  A) UUOB "
                           "B) 2603130525 C) 2612262059  E) AD CLSD.   CREATED: 13 MAR 2026 05:26  SOURCE: UUUUYNYX")
    assert n.text == "AD CLSD."
    assert N.scrub_contacts("OPS@EXAMPLE.ORG, X.Y+Z@A.RO") == "[email], [email]"


@pytest.mark.parametrize("raw,expected", [
    # procedură de apropiere suspendată (subiect PI): rutină la LRIA, nu GNSS
    ("(A0500/26 NOTAMN\nQ) LRBB/QPIAU/I/NBO/A/000/999/4711N02737E005\nA) LRIA B) 2611010000 C) 2611302359\n"
     "E) RNAV (GNSS) RWY 08 APCH NOT AVBL DUE TO MAINT.)", None),
    ("(A0501/26 NOTAMN\nQ) LRBB/QPIAU/I/NBO/A/000/999/4711N02737E005\nA) LRIA B) 2611010000 C) 2611302359\n"
     "E) RNAV (GNSS) RWY 08 APCH NOT AVBL DUE TO GNSS INTERFERENCE.)", "gnss"),
    ("(A0502/26 NOTAMN\nQ) LRBB/QGWAU/I/NBO/E/000/999/4700N02800E050\nA) LRBB B) 2611010000 C) 2611302359\n"
     "E) GNSS SIGNAL NOT AVBL IN THE FLW AREA.)", "gnss"),
    # FA + AH (program schimbat): „AD CLSD OUTSIDE THESE HR” e rutină
    ("(A0503/26 NOTAMN\nQ) LRBB/QFAAH/IV/NBO/A/000/999/4711N02737E005\nA) LRIA B) 2611010000 C) 2611302359\n"
     "E) AD HR OF SER MON-FRI 0500-1900. AD CLSD OUTSIDE THESE HR.)", None),
    ("(A0504/26 NOTAMN\nQ) LRBB/QFALC/IV/NBO/A/000/999/4711N02737E005\nA) LRIA B) 2611010000 C) 2611010300\n"
     "E) AD CLSD.)", "aeroport_inchis"),
    # FIR limitat la zboruri de stat (cod Q „LT”): restricție, nu „irelevant” (SINTETIC)
    ("(A0505/26 NOTAMN\nQ) LUUU/QAFLT/IV/NBO/E/000/999/4700N02850E999\nA) LUUU B) 2611012000 C) 2611012200\n"
     "E) FLT IN CHISINAU FIR LIMITED TO STATE, SAR AND EMERG ACFT.)", "restrictie_spatiu_aerian"),
])
def test_classify_regressions(raw, expected):
    assert N.classify(N.parse_icao_notam(raw)) == expected


@pytest.mark.parametrize("keep", ["LRTRA82G", "EGD494B", "W/UW75", "AR112H(F)", "451745N0284737E-451314N0293944E",
                                  "FL240", "U-TURN", "AD-HOC", "EN-ROUTE", "CO-ORD", "RE-OPEN", "D-ATIS", "L-BAND",
                                  "MOLDAVIAN BORDER - UKRAINIAN BORDER", "CALL SIGNS AND FREQ", "QRTCS", "SQUAWK 7700"])
def test_scrub_identities_keeps_codes(keep):
    assert N.scrub_text(keep) == keep


@pytest.mark.parametrize("text,gone", [
    ("FLT CHECK BY ACFT YR-ABC WILL TAKE PLACE", "YR-ABC"),
    ("HEL ER-AXV AND D-EABC OPS", "ER-AXV"),
    ("PJE FM ACFT YR-1234", "YR-1234"),
    ("CALLSIGN ROT123 ON 118.105", "ROT123"),
    ("FLT INSPECTION ACFT C/S YRCAA", "YRCAA"),
    ("ACFT CS ROF99 WILL", "ROF99"),
    ("ICAO 24-BIT ADDRESS 4A1234 IN USE", "4A1234"),
    ("MODE S CODE: 50852C", "50852C"),
])
def test_scrub_identities_removes_aircraft(text, gone):
    out = N.scrub_text(text)
    assert gone not in out and "[aeronavă]" in out


def test_identities_never_reach_signal_or_meta():
    raw = ("(F8099/26 NOTAMN\nQ) LRBB/QWULW/IV/BO/W/000/020/4710N02740E005\nA) LRBB B) 2608030000 C) 2608032359\n"
           "E) UNMANNED ACFT FLT. FLT CHECK BY ACFT YR-ABC CALLSIGN ROT123. ICAO ADDRESS 4A1234. CTC 0232 271 590.\n"
           "F) GND G) 2000FT AMSL)")
    sigs = N.NotamCollector().process([N.parse_icao_notam(raw)], 1, NOW)
    assert len(sigs) == 1
    blob = sigs[0].text + json.dumps(sigs[0].meta, ensure_ascii=False)
    for secret in ("YR-ABC", "ROT123", "4A1234", "0232 271 590"):
        assert secret not in blob


@pytest.mark.parametrize("text,expected", [
    ("PPR CTC 0232 271 590", "PPR [tel]"),
    ("PPR CTC 0232271590 OR 0040212083100", "PPR [tel] OR [tel]"),
    ("GSM 0722 123 456", "[tel]"),                           # ca „TEL …”: cuvântul-cheie dispare și el
    ("CTC 0600-1800", "CTC 0600-1800"),                     # ore, nu telefon
    ("B) 2608010000 C) 2608312359", "B) 2608010000 C) 2608312359"),
    ("451745N0284737E FL110-FL450 DAILY 1630-0430", "451745N0284737E FL110-FL450 DAILY 1630-0430"),
])
def test_phone_scrub(text, expected):
    assert N.scrub_contacts(text) == expected


def test_parse_nms_bad_shapes_raise_valueerror():
    for bad in ({"status": "Success", "data": []}, {"status": "Success", "data": "x"}, {"items": None}, "x", None, 5):
        with pytest.raises(ValueError):
            N.parse_nms(bad)
    assert N.parse_nms({"items": []}) == [] and N.parse_nms([]) == []


def test_coarse_circle_is_never_near():
    big = N.Notam(id="A0001/26", fir="UKOV", qcode="QRTCA", lat=46.5, lon=30.7, radius_nm=300, text="TEMPORARY RESTRICTED AREA",
                  start=T(2026, 8, 1), end=T(2026, 9, 1))
    small = N.Notam(id="A0002/26", fir="LRBB", qcode="QRTCA", lat=47.1, lon=27.7, radius_nm=5, text="TEMPORARY RESTRICTED AREA",
                    start=T(2026, 8, 1), end=T(2026, 9, 1))
    assert N.distances(big) == (0.0, 0.0)  # limita inferioară: cercul cuprinde Iașiul
    assert N.area_kind(big) == "circle" and N.area_kind(N.parse_icao_notam(LUUU_CLOSED)) == "fir"
    by = {s.meta["id"]: s.meta for s in N.NotamCollector().process([big, small], 2, NOW)}
    assert by["A0001/26"]["near"] is False and by["A0002/26"]["near"] is True
    assert by["A0001/26"]["area"] == "circle"


def test_text_coords_hemispheres_seconds_and_bad_minutes():
    pts = N.text_coords("540733.1N 0094659.5W-453410N0280827E 123456S0123456W 456010N0280000E 450060N0280000E")
    assert pts[0] == pytest.approx((54 + 7 / 60 + 33.1 / 3600, -(9 + 46 / 60 + 59.5 / 3600)))
    assert pts[1] == pytest.approx((45 + 34 / 60 + 10 / 3600, 28 + 8 / 60 + 27 / 3600))
    assert pts[2] == pytest.approx((-(12 + 34 / 60 + 56 / 3600), -(12 + 34 / 60 + 56 / 3600)))
    assert len(pts) == 3  # minute 60 și secunde 60: respinse
    assert N._coord("45", "60", "N", "028", "00", "E") is None and N._coord("45", "00", "N", "028", "60", "E") is None
    j = text_list()["J0249/26"]  # „2040S04938W”: emisfera sudică și vestică
    assert j.lat == pytest.approx(-(20 + 40 / 60)) and j.lon == pytest.approx(-(49 + 38 / 60)) and j.radius_nm == 70


def test_rings_are_lat_lon_from_geojson_lon_lat():
    n = N.parse_romatsa_wfs(wfs())[0]  # C8116/25: primul vârf GeoJSON [28.79357276, 45.29593932]
    assert n.polygons[0][0] == pytest.approx((45.29593932, 28.79357276))


def test_retras_grace_and_health_threshold():
    c = N.NotamCollector()
    c.process(N.parse_romatsa_wfs(wfs()), 11, NOW)
    rest = [n for n in N.parse_romatsa_wfs(wfs()) if n.id not in ("P2738/26", "F8021/26")]
    # P2738/26 se termină la 17:40: dispariția cu < 10 min înainte nu e „retras”; F8021/26 (până la 23:59) e
    sigs = c.process(rest, 9, T(2026, 8, 3, 17, 35))
    assert ids(sigs, "retras") == ["F8021/26"]
    # pragul de sănătate: 5 din 11 (< 50%) = pană, nimic retras
    c2 = N.NotamCollector()
    c2.process(N.parse_romatsa_wfs(wfs()), 11, NOW)
    few = [n for n in N.parse_romatsa_wfs(wfs()) if n.id in ("P2578/26", "P2580/26")]
    assert ids(c2.process(few, 5, NOW + dt.timedelta(minutes=15)), "retras") == []
    assert ids(c2.process(few, 6, NOW + dt.timedelta(minutes=30)), "retras") != []  # 6 ≥ 50% din 5: sănătos


def test_cancel_in_partial_read_is_not_later_retras():
    c = N.NotamCollector(name="t", source="text", urls=["http://x/"])
    now = T(2025, 11, 28, 21, 0)
    c.process([N.parse_icao_notam(LUUU_CLOSED)], 10, now)
    # citire parțială (1 din 10) care aduce anularea → „anulare”
    s = c.process([N.parse_icao_notam(LUUU_CANCEL)], 1, now + dt.timedelta(minutes=10))
    assert [x.meta["kind"] for x in s] == ["anulare"]
    # citire normală fără nimic: A0123/25 nu mai e urmărit, deci nu apare „retras”
    assert c.process([], 10, now + dt.timedelta(minutes=20)) == []


def test_nms_cancelation_date_path():
    f = nms_feature("A0123/26", "LUUU", "LUUU", "QAFLC", "AIRSPACE CLOSED DUE TO UAV ACTIVITY.")
    c = N.NotamCollector(name="t", source="text", urls=["http://x/"])
    now = T(2026, 11, 2, 21, 0)
    assert ids(c.process(N.parse_nms([f]), 1, now), "nou") == ["A0123/26"]
    f2 = copy.deepcopy(f)
    f2["properties"]["coreNOTAMData"]["notam"]["cancelationDate"] = "2026-11-02T21:10:00.000Z"
    n = N.parse_nms([f2])[0]
    assert n.cancelled_at == T(2026, 11, 2, 21, 10)
    s = c.process([n], 1, now + dt.timedelta(minutes=5))  # anularea e în viitor: încă activ
    assert [x.meta["kind"] for x in s] == ["nou"]
    s = c.process([n], 1, now + dt.timedelta(minutes=15))
    assert [(x.meta["kind"], x.meta["ends"], x.meta["ends_key"], x.ext_id) for x in s] == \
        [("anulare", "A0123/26", "LU:A0123/26", "LU:A0123/26|anulare")]
    assert c.process([], 1, now + dt.timedelta(minutes=30)) == []  # nu și „retras”


def test_categories_filter_and_cancellations():
    only = N.NotamCollector(name="t", source="text", urls=["http://x/"], categories=["drone_uas"])
    now = T(2025, 11, 28, 21, 0)
    assert only.process([N.parse_icao_notam(LUUU_CLOSED)], 1, now) == []  # spațiu închis: nu e în filtru
    # anularea unui NOTAM neurmărit, de altă categorie (restrictie_ridicata), nu trece de filtru
    assert only.process([N.parse_icao_notam(LUUU_CANCEL)], 1, now + dt.timedelta(minutes=30)) == []
    every = N.NotamCollector(name="t", source="text", urls=["http://x/"])
    s = every.process([N.parse_icao_notam(LUUU_CANCEL)], 1, now + dt.timedelta(minutes=30))
    assert [(x.meta["kind"], x.meta["category"]) for x in s] == [("anulare", "restrictie_ridicata")]


def test_request_with_context_total_deadline_binds():
    import socket
    import time

    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)

    def drip():
        conn, _ = srv.accept()
        conn.recv(4096)
        conn.sendall(b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\n")
        try:
            for _ in range(10):  # un octet la 0,9 s: fiecare citire < timeout, dar totalul depășește 2 × timeout
                conn.sendall(b"x")
                time.sleep(0.9)
        except OSError:
            pass
        conn.close()

    threading.Thread(target=drip, daemon=True).start()
    t0 = time.monotonic()
    with pytest.raises(http.HttpError):
        N.request_with_context(f"http://127.0.0.1:{srv.getsockname()[1]}/", None, timeout=1)
    assert time.monotonic() - t0 < 2.5  # fără termenul pe socket: ~2,7 s
    srv.close()
