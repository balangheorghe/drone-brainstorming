"""Suceava ca a doua țintă: distanțe/ETA față de cea mai apropiată țintă, NOTAM lângă Suceava și LRSV,
zona ADS-B LRSV și raioanele din nordul Bucovinei în configurația de exemplu."""

import datetime as dt
import pathlib

from veghe import app, geo
from veghe import collectors as C
from veghe.config import load
from veghe.engine import Engine, EngineConfig
from veghe.models import Signal
from veghe.notam import NotamCollector
from veghe.timeutil import UTC, iso

T0 = dt.datetime(2026, 11, 3, 15, 0, tzinfo=UTC)
SUCEAVA = geo.BY_KEY["suceava"]
ROOT = pathlib.Path(__file__).resolve().parent.parent


def eng(targets=(geo.IASI, SUCEAVA)):
    return Engine(EngineConfig(watch_oblasts=["Чернівецька область"],
                               watch_raions=["Чернівецький район", "Вижницький район"], targets=list(targets)))


def alert_state(e, raion, t=T0):
    return e.process(Signal(source="alerts_in_ua", role="ua_alert_state", text="", received_at=t,
                            meta={"active": [{"title": raion, "type": "raion", "oblast": "Чернівецька область"}]}), t)


def md(e, text, t=T0):
    return e.process(Signal(source="rss:md", role="md_news", text=text, received_at=t, published_at=t), t)


def test_bucovina_alert_eta_is_toward_suceava():
    msgs = alert_state(eng(), "Вижницький район")
    assert len(msgs) == 1 and msgs[0].kind == "vigilenta"
    assert "spre Suceava" in msgs[0].text and "spre Iași" not in msgs[0].text
    # cu o singură țintă (vechiul comportament) ETA rămâne față de Iași
    only_iasi = alert_state(eng((geo.IASI,)), "Вижницький район")
    assert "spre Iași" in only_iasi[0].text


def test_northern_moldova_drone_is_approach_toward_suceava_with_iasi_distance_kept():
    text = "O dronă a fost observată în raionul Edineț, la Goleni, spre vest"
    msgs = md(eng(), text)
    assert len(msgs) == 1 and msgs[0].kind == "apropiere"
    assert "Prut / Suceava" in msgs[0].text and "km de Suceava" in msgs[0].text and "km de Iași)" in msgs[0].text
    # lângă Iași, tot Iașul e ținta afișată
    near = md(eng(), "O dronă a intrat în R. Moldova, a fost observată la Ungheni, spre vest")
    assert near and "Prut / Iași" in near[0].text and "Suceava" not in near[0].text


def test_ua_direction_near_chernivtsi_reports_suceava_distance():
    msgs = eng().process(Signal(source="tg:kpszsu", role="ua_direction", text="БпЛА на Чернівеччині, курсом на Сторожинець",
                                received_at=T0, published_at=T0), T0)
    assert len(msgs) == 1 and msgs[0].kind == "directie"
    assert "km de Suceava (~" in msgs[0].text and "km de Iași)" in msgs[0].text


def notam_meta(**kw):
    m = {"id": "F8100/26", "key": "LR:F8100/26", "kind": "nou", "replaces": None, "fir": "LRBB", "qcode": "QRTCA",
         "category": "spatiu_aerian_inchis", "uas": False, "near": False, "locations": ["LRBB"],
         "lat": 47.75, "lon": 26.1, "radius_nm": 5,
         "start": iso(T0 - dt.timedelta(hours=1)), "end": iso(T0 + dt.timedelta(hours=8)), "estimated": False,
         "dist_iasi_km": 135.0, "dist_prut_km": 80.0, "ends": None, "ends_key": None, "continua": None}
    m.update(kw)
    return m


def nsig(meta, t=T0):
    return Signal(source="notam:romatsa", role="notam", received_at=t, published_at=t,
                  ext_id=f"{meta['key']}|{meta['kind']}", text=f"NOTAM {meta['id']} · spațiu aerian închis · LRBB", meta=meta)


def test_notam_closure_near_suceava_announced_only_when_suceava_is_a_target():
    msgs = eng().process(nsig(notam_meta()), T0)
    assert len(msgs) == 1 and "F8100/26" in msgs[0].text
    assert eng((geo.IASI,)).process(nsig(notam_meta()), T0) == []
    # zonă mare (cerc Q de 150 NM): distanța nu spune nimic, rămâne doar în /stare
    assert eng().process(nsig(notam_meta(id="F8101/26", key="LR:F8101/26", radius_nm=150)), T0) == []
    # departe de ambele ținte (Maramureș)
    assert eng().process(nsig(notam_meta(id="F8102/26", key="LR:F8102/26", lat=47.66, lon=23.58)), T0) == []


def test_notam_suceava_airport_closure_is_announced():
    m = notam_meta(id="A2001/26", key="LR:A2001/26", category="aeroport_inchis", qcode="QFALC", locations=["LRSV"],
                   lat=None, lon=None, radius_nm=None)
    msgs = eng((geo.IASI,)).process(nsig(m), T0)
    assert len(msgs) == 1 and "A2001/26" in msgs[0].text


def test_example_config_monitors_suceava():
    cfg = load(str(ROOT / "config.example.toml"), env={})
    e = app.build_engine(cfg, None)
    assert [t.key for t in e.targets] == ["iasi", "suceava", "botosani", "piatra_neamt", "bacau", "vaslui"]
    assert [t.name for t in e.targets][3] == "Piatra Neamț"
    assert {"Чернівецький район", "Вижницький район"} <= set(e.cfg.watch_raions)
    cols = app.build_collectors(cfg)
    adsb = next(c for c in cols if isinstance(c, C.Adsb))
    assert any(p["name"] == "LRSV Suceava" and abs(p["lat"] - 47.688) < 0.01 for p in adsb.points)
    assert any(p["name"] == "LRBC Bacău" and abs(p["lat"] - 46.522) < 0.01 for p in adsb.points)
    notam = next(c for c in cols if isinstance(c, NotamCollector))
    assert {"LRSV", "LRBC"} <= notam.locations
    assert {"LRSV", "LRBC"} <= NotamCollector().locations   # și implicit, fără config
    # fără [engine] targets în config.toml (config vechi): tot Nord-Estul, din cod
    from veghe.config import Config
    assert len(app.build_engine(Config({}), None).targets) == 6


def test_unknown_target_is_a_config_error():
    import pytest

    from veghe.config import ConfigError

    with pytest.raises(ConfigError):
        app._targets(["atlantida"])
    assert [p.key for p in app._targets(["Iași", "Suceava"])] == ["iasi", "suceava"]
    assert [p.name for p in app._targets(["neamt", "Bacău"])] == ["Piatra Neamț", "Bacău"]


def test_notam_near_suceava_cancel_and_expiry_are_announced():
    e = eng()
    assert len(e.process(nsig(notam_meta()), T0)) == 1
    cancel = notam_meta(id="F8110/26", key="LR:F8110/26", kind="anulare", ends="F8100/26", ends_key="LR:F8100/26",
                        lat=None, lon=None, radius_nm=None)
    msgs = e.process(nsig(cancel), T0 + dt.timedelta(minutes=5))
    assert any("NOTAM ANULAT" in m.text and "F8100/26" in m.text for m in msgs)
    # expirare
    e2 = eng()
    e2.process(nsig(notam_meta(end=iso(T0 + dt.timedelta(hours=1)))), T0)
    out = [m for k in range(1, 4) for m in e2.tick(T0 + dt.timedelta(hours=k))]
    assert any("F8100/26" in m.text for m in out)


# ------------------------------------------------------------------ Nord-Est: regresii găsite la verificare
NE = app._targets(geo.NE_TARGETS)


def ne_eng(store=None):
    return Engine(EngineConfig(watch_oblasts=["Одеська область", "Вінницька область", "Чернівецька область"],
                               watch_raions=["Подільський район", "Березівський район", "Білгород-Дністровський район",
                                             "Чернівецький район", "Вижницький район"], targets=list(NE)), store)


def mins(m):
    return T0 + dt.timedelta(minutes=m)


def test_drone_leaving_moldova_toward_ukraine_is_not_approach():
    e = ne_eng()
    assert [x.kind for x in md(e, "O dronă a fost observată în raionul Soroca")] == ["moldova"]
    out = md(e, "Drona a părăsit spațiul aerian al R. Moldova pe la Otaci, revenind în Ucraina", mins(15))
    assert [x.kind for x in out] == ["moldova"] and "contactați ISU" not in out[0].text
    # „lansate spre Ucraina” fără „a părăsit”: tot o posibilă apropiere (Ocnița, ~91 km de Botoșani)
    e2 = ne_eng()
    out = md(e2, "Dronele lansate de Rusia spre Ucraina au intrat în spațiul aerian al R. Moldova la Ocnița")
    assert [x.kind for x in out] == ["apropiere"] and "Botoșani" in out[0].text


def test_ukrainian_position_does_not_become_approach_from_placeless_moldova_news():
    e = ne_eng()
    e.process(Signal(source="tg:kpszsu", role="ua_direction", text="БпЛА на Чернівеччині, курсом на захід",
                     received_at=T0, published_at=T0), T0)
    out = md(e, "O dronă a fost semnalată în spațiul aerian al R. Moldova", mins(5))
    assert all(x.kind != "apropiere" for x in out)


def test_bucovina_towns_alone_give_direction_and_adverb_glyboko_does_not():
    for text, place in (("БпЛА курсом на Вижницю", "Vijnița"), ("Шахед біля Глибокої", "Hliboca"),
                        ("БпЛА курсом на Сторожинець", "Storojineț")):
        out = ne_eng().process(Signal(source="tg:x", role="ua_direction", text=text, received_at=T0, published_at=T0), T0)
        assert [x.kind for x in out] == ["directie"] and place in out[0].text and "Suceava" in out[0].text
    deep = ne_eng().process(Signal(source="tg:x", role="ua_direction", text="Шахеди глибоко в тилу, курсом на захід",
                                   received_at=T0, published_at=T0), T0)
    assert all("Hliboca" not in x.text for x in deep)


def test_vigilance_deep_ukraine_areas_do_not_produce_updates_with_ne_targets():
    e = ne_eng()
    assert len(alert_state(e, "Березівський район")) == 1
    # Bilhorod (207 km de Vaslui, 236 de Iași) după Berezivka: nu e „mai aproape”
    st = {"active": [{"title": "Березівський район", "type": "raion", "oblast": "Одеська область"},
                     {"title": "Білгород-Дністровський район", "type": "raion", "oblast": "Одеська область"}]}
    assert e.process(Signal(source="alerts_in_ua", role="ua_alert_state", text="", received_at=mins(30), meta=st), mins(30)) == []
    # Vinnytsia (212 km de Botoșani) după Podilsk: nu e o „direcție nouă”
    e2 = ne_eng()
    alert_state(e2, "Подільський район")
    st = {"active": [{"title": "Подільський район", "type": "raion", "oblast": "Одеська область"},
                     {"title": "Вінницька область", "type": "oblast", "oblast": "Вінницька область"}]}
    out = e2.process(Signal(source="alerts_in_ua", role="ua_alert_state", text="", received_at=mins(30), meta=st), mins(30))
    assert all("direcție nouă" not in x.text for x in out)


def test_restart_after_target_list_change_does_not_resend_as_closer(tmp_path):
    from veghe.store import Store

    st = Store(str(tmp_path / "v.db"))
    old = Engine(EngineConfig(watch_oblasts=[], watch_raions=[], targets=[geo.IASI]), st)   # versiunea veche: doar Iași
    text = "O dronă a fost observată în raionul Edineț, la Goleni, spre vest"
    assert [x.kind for x in md(old, text, T0)] == ["apropiere"]       # 114 km de Iași
    new = ne_eng(st)
    new._restore_hyps(mins(20))
    # aceeași poziție, repostată: 67 km de Botoșani nu e „mai aproape” decât 114 km de Iași
    assert md(new, text, mins(20)) == []


def test_notam_near_bacau_names_the_city_survives_restart_and_shows_in_status(tmp_path):
    from veghe import timeutil
    from veghe.store import Store

    st = Store(str(tmp_path / "v.db"))
    e = ne_eng(st)
    m = notam_meta(id="F8200/26", key="LR:F8200/26", lat=46.6, lon=26.95, radius_nm=3)   # ~4 km de Bacău
    s = nsig(m)
    st.add_signal(s)
    out = e.process(s, T0)
    assert len(out) == 1 and "lângă Bacău (~" in out[0].text
    assert e.status(T0)["notam_active"][0]["aproape"] and "Bacău" in e.status(T0)["tinte"]
    orig = timeutil.now
    timeutil.now = lambda: mins(30)
    try:
        e2 = ne_eng(st)                                                # repornire: near_tinta se recalculează
    finally:
        timeutil.now = orig
    cancel = notam_meta(id="F8201/26", key="LR:F8201/26", kind="anulare", ends="F8200/26", ends_key="LR:F8200/26",
                        lat=None, lon=None, radius_nm=None)
    assert any("NOTAM ANULAT" in x.text and "F8200/26" in x.text for x in e2.process(nsig(cancel), mins(40)))


def test_target_names_with_diacritics_and_status_text():
    assert [p.name for p in app._targets(["Piatra Neamț", "piatra-neamt", "Neamț"])] == ["Piatra Neamț"] * 3


def test_vigilance_restart_after_target_list_change_is_silent(tmp_path):
    from veghe.store import Store

    st = Store(str(tmp_path / "v.db"))
    old = Engine(EngineConfig(watch_oblasts=[], watch_raions=["Чернівецький район"], targets=[geo.IASI]), st)
    assert len(alert_state(old, "Чернівецький район")) == 1          # 177 km de Iași
    new = ne_eng(st)
    new._restore_vigilance(mins(25))
    # aceeași alertă, după pauză: 75 km de Suceava nu înseamnă „s-a extins mai aproape”
    assert alert_state(new, "Чернівецький район", mins(25)) == []
