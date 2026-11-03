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
    assert [t.key for t in e.targets] == ["iasi", "suceava"]
    assert {"Чернівецький район", "Вижницький район"} <= set(e.cfg.watch_raions)
    cols = app.build_collectors(cfg)
    adsb = next(c for c in cols if isinstance(c, C.Adsb))
    assert any(p["name"] == "LRSV Suceava" and abs(p["lat"] - 47.688) < 0.01 for p in adsb.points)
    notam = next(c for c in cols if isinstance(c, NotamCollector))
    assert "LRSV" in notam.locations
    assert "LRSV" in NotamCollector().locations   # și implicit, fără config


def test_unknown_target_is_a_config_error():
    import pytest

    from veghe.config import ConfigError

    with pytest.raises(ConfigError):
        app._targets(["atlantida"])
    assert [p.key for p in app._targets(["Iași", "Suceava"])] == ["iasi", "suceava"]


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
