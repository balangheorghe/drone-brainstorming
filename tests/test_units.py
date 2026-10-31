"""Teste unitare: geografie, analiza textului, parsere (pe fixturi în formatele confirmate)."""

import datetime as dt
import json
import pathlib

import pytest

from veghe import collectors as C
from veghe import geo
from veghe.nlp import analyze, normalize
from veghe.timeutil import UTC, _ro_offset, hhmm

FIX = pathlib.Path(__file__).parent / "fixtures"


# ------------------------------------------------------------------ geografie
def test_gazetteer_in_region_and_unique():
    keys = [p.key for p in geo.GAZETTEER]
    assert len(keys) == len(set(keys))
    for p in geo.GAZETTEER:
        assert 44.0 <= p.lat <= 50.0 and 25.0 <= p.lon <= 32.5, p
        assert p.country in {"UA", "MD", "RO"}


@pytest.mark.parametrize("a,b,km", [("iasi", "chisinau", 97), ("iasi", "ungheni", 16), ("iasi", "tibirica", 63),
                                    ("iasi", "podilsk", 159), ("iasi", "izmail", 222)])
def test_distances_match_docs(a, b, km):
    # distanțele din docs/01–02 (calculate independent)
    assert abs(geo.dist(geo.BY_KEY[a], geo.BY_KEY[b]) - km) <= 3


def test_eta_interval():
    assert geo.eta_minutes(97) == (13, 39)
    assert geo.eta_minutes(0) == (0, 0)


def test_prut_distance_sane():
    assert geo.dist_to_prut_km(geo.BY_KEY["ungheni"]) < 5
    assert 35 < geo.dist_to_prut_km(geo.BY_KEY["chisinau"]) < 90
    assert geo.dist_to_prut_km(geo.BY_KEY["tiraspol"]) > geo.dist_to_prut_km(geo.BY_KEY["chisinau"])


def test_dst_fallback_rule():
    assert _ro_offset(dt.datetime(2026, 9, 8, 13, 0, tzinfo=UTC)) == dt.timedelta(hours=3)
    assert _ro_offset(dt.datetime(2026, 10, 31, 14, 0, tzinfo=UTC)) == dt.timedelta(hours=2)
    assert _ro_offset(dt.datetime(2026, 10, 25, 0, 59, tzinfo=UTC)) == dt.timedelta(hours=3)
    assert _ro_offset(dt.datetime(2026, 10, 25, 1, 0, tzinfo=UTC)) == dt.timedelta(hours=2)
    assert hhmm(dt.datetime(2026, 10, 31, 15, 4, tzinfo=UTC)) == "17:04 EET"


# ------------------------------------------------------------------ text
def test_normalize_diacritics():
    assert normalize("Țibirica, Şerban  ŞI Iaşi") == "tibirica, serban si iasi"
    assert normalize("Ізмаїл") == "ізмаїл"  # chirilicul nu se atinge


@pytest.mark.parametrize("text,drone,missile,places,direction", [
    ("Група ударних БпЛА на півночі Одещини курсом на Подільськ", True, False, ["odesa", "podilsk"], ["podilsk"]),
    ("Ракета на Одесу!", False, True, ["odesa"], []),
    ("Ударные БПЛА в направлении Измаила", True, False, ["izmail"], ["izmail"]),
    ("UPDATE/ Drona a dispărut de pe sistemele de monitorizare radar, în raionul Călărași, lângă Țibirica", True, False,
     ["calarasi", "tibirica"], []),
    ("O dronă dinspre Mihailovka (regiunea Vinnița) spre Sobari, raionul Soroca", True, False, ["vinnytsia", "soroca"], ["soroca"]),
    ("Prețul pâinii crește din noiembrie", False, False, [], []),
])
def test_analyze(text, drone, missile, places, direction):
    f = analyze(text)
    assert f.drone == drone and f.missile == missile
    assert [p.key for p in f.places] == places
    assert [p.key for p in f.direction_to] == direction


def test_analyze_flags():
    assert analyze("Реактивні БпЛА ... курсом на північний захід").westward
    assert analyze("Реактивні БпЛА ... курсом на північний захід").jet
    assert analyze("🟢 16:50 Відбій тривоги в Подільський район.").ua_alert_off
    assert analyze("🔴 16:12 Повітряна тривога в Подільський район.").ua_alert_on
    f = analyze("RO-Alert în nordul județului Iași: posibilă incursiune de drone")
    assert f.roalert and f.drone and [p.key for p in f.ro_counties] == ["iasi"]
    assert analyze("Alerta a încetat în județul Iași").end
    assert analyze("Spațiul aerian din nordul Republicii Moldova a fost restricționat").airspace_restricted
    assert analyze("Spațiul aerian a fost redeschis").airspace_reopened


def test_ambiguous_names_need_context():
    # Călărași (MD) și Florești (MD) doar cu „raionul”; altfel pot fi județul/comuna din RO
    assert "calarasi" not in [p.key for p in analyze("Ploaie în județul Călărași").places]
    assert "calarasi" in [p.key for p in analyze("drona în raionul Călărași").places]
    assert "reni" not in [p.key for p in analyze("renină și altele").places]


# ------------------------------------------------------------------ parsere
def test_parse_alerts_in_ua_official_fixture():
    data = json.loads((FIX / "alerts_in_ua_active.json").read_text(encoding="utf-8"))
    act = C.parse_alerts_in_ua(data, ["Одеська область", "Вінницька область"], ["Подільський район", "Ізмаїльський район"])
    titles = [a["title"] for a in act]
    assert titles == ["Подільський район"]  # Izmail e terminată; Odesa raion = artilerie; restul în afara zonei
    assert act[0]["threats"] == ["drones"] and act[0]["level"] == "yellow"


def test_parse_ukrainealarm():
    data = json.loads((FIX / "ukrainealarm_alerts.json").read_text(encoding="utf-8"))
    act = C.parse_ukrainealarm(data, ["Одеська область", "Подільський район", "Чернівецька область"])
    assert sorted(a["title"] for a in act) == ["Одеська область", "Подільський район"]  # Cernăuți = ARTILLERY


def test_parse_tme():
    posts = C.parse_tme((FIX / "tme_kpszsu.html").read_text(encoding="utf-8"))
    assert [p["post"] for p in posts] == ["kpszsu/30001", "kpszsu/30002"]  # 30003 e doar foto, fără text
    assert posts[0]["text"].startswith("Група ударних БпЛА на півночі Одещини курсом на Подільськ.")
    assert "\n" in posts[0]["text"] and "Будьте уважні" in posts[0]["text"]
    assert "ВІДПОВІДЬ" not in posts[1]["text"]  # textul din reply e ignorat
    assert posts[1]["published_at"] == dt.datetime(2026, 10, 31, 14, 20, tzinfo=UTC)
    assert posts[0]["link"] == "https://t.me/kpszsu/30001"


def test_parse_feeds():
    rss = C.parse_feed((FIX / "feed_rss.xml").read_text(encoding="utf-8"))
    assert len(rss) == 2 and rss[0]["published_at"] == dt.datetime(2026, 10, 31, 15, 5, tzinfo=UTC)
    assert "RO-Alert" in rss[0]["title"] and rss[0]["guid"] == "CBMi1"
    atom = C.parse_feed((FIX / "feed_atom.xml").read_text(encoding="utf-8"))
    assert atom[0]["link"] == "https://www.zdg.md/stiri/update-drona" and "16:54" in atom[0]["summary"]
    assert C.strip_publisher("RO-Alert în Iași - Pro TV Chișinău") == "RO-Alert în Iași"
    assert C.strip_publisher("Iași - Chișinău, drumul închis pentru câteva ore din cauza lucrărilor") \
        == "Iași - Chișinău, drumul închis pentru câteva ore din cauza lucrărilor"


def test_parsers_fail_loudly_on_wrong_pages():
    with pytest.raises(ValueError):
        C.parse_feed("<html><body>captcha</body></html>")
    with pytest.raises(ValueError):
        C.parse_tme("<html><body><div class='tgme_page'>Channel not found</div></body></html>")
    # canal existent dar gol: fără eroare
    assert C.parse_tme("<section class='tgme_channel_history js-message_history'></section>") == []
    # entități HTML nedeclarate în XML
    assert C.parse_feed("<rss><channel><item><title>A&nbsp;B</title></item></channel></rss>")[0]["title"] == "A B"


def test_count_aircraft_excludes_military():
    c = C.count_aircraft(json.loads((FIX / "adsb_point.json").read_text()))
    assert c == {"civil_airborne": 1, "civil_total": 3, "excluded_military": 1}
