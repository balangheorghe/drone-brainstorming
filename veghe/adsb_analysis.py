"""Analiza ADS-B, doar pentru traficul CIVIL: numărători pe zonă, degradarea preciziei GNSS,
așteptări (holding) și întoarceri de pe rută, coduri de urgență (7500/7600/7700) și deosebirea
unei scăderi reale de trafic de o pană de date / de acoperire.

Modulul nu ia decizii de mesaj și nu publică nimic: întoarce, pe zonă, un dicționar agregat
(JSON) pe care motorul îl poate transforma în mesaje INTERNE.

Politici (verificate de tests/test_adsb_analysis.py):
- aeronavele militare (dbFlags & 1) sunt eliminate înaintea oricărui alt pas: nu se numără,
  nu se analizează, nu se păstrează, nu se afișează;
- aeronavele cu indicatori de confidențialitate (PIA = dbFlags & 4, LADD = dbFlags & 8) intră
  doar în numărătorile agregate, niciodată în analizele pe aeronavă;
- rezultatul nu conține identități (hex, indicativ, înmatriculare, tip): doar numărători, coduri,
  distanțe/direcții și altitudini rotunjite;
- starea pe aeronavă stă doar în memorie, sub o cheie BLAKE2s cu cheie aleatoare per proces
  (nu adresa hex în clar), și expiră în câteva minute; nimic nu se scrie pe disc.

Formate (sursa readsb, ramura dev, citită la 2026-11-02):
- re-api „jv2” (adsb.lol /v2/point, airplanes.live /v2/point, adsb.fi /v3, readsb local cu
  --net-api-port interogat cu `?circle=lat,lon,nm&jv2`):
  {"ac": [...], "msg", "now": ms, "total", "ctime", "ptime"}; `total` = aeronavele din ACEST
  răspuns, nu din rețea – https://github.com/wiedehopf/readsb/blob/dev/api.c (ramura jamesv2);
  adsb.lol trece răspunsul neschimbat:
  https://github.com/adsblol/api/blob/main/src/adsb_api/utils/reapi.py
- re-api fără jv2: {"now": s, "aircraft": [...], "resultCount", "ptime"} (același api.c);
- aircraft.json local (readsb/tar1090): {"now": s, "messages": total de la pornire, "aircraft": [...]}
  – https://github.com/wiedehopf/readsb/blob/dev/README-json.md
Câmpuri pe aeronavă (README-json.md; json_out.c, sprintAircraftObject):
  hex; type (adsb_icao, mlat, mode_s, …); alt_baro (ft sau "ground"; cu --json-separate-ground e
  numeric + "ground": true/false); gs (kt); lat/lon/nic/rc/seen_pos (doar cu poziție validă);
  altfel lastPosition{lat, lon, nic, rc, seen_pos} (poate avea până la 14 zile); squawk ("%04x");
  emergency (none/general/lifeguard/minfuel/nordo/unlawful/downed/reserved); category ("A3");
  version (0/1/2); nac_p; mlat[]/tisb[] (câmpurile derivate din MLAT/TIS-B); seen; r/t și dbFlags
  (doar cu --db-file; dbFlags doar dacă e nenul); gpsOkBefore/gpsOkLat/gpsOkLon („experimental,
  subject to change”: GPS pierdut sau puternic degradat; emis independent de lat/lon – json_out.c,
  nogps(): ≥ 17 mesaje DF17 fără poziție sau cu NACp ≤ 2, la gs > 50 kt, în aer, în cel mult
  15 min de la ultima poziție ADS-B cu NACp ≥ 4 – https://github.com/wiedehopf/readsb/blob/dev/track.c).

Reguli (praguri în AdsbAnalysisConfig; toate sunt propuneri de inginerie de reglat pe istoricul
agregat, nu standarde publicate):
- GNSS: o aeronavă e PIERDUTĂ dacă are gpsOkBefore; DEGRADATĂ dacă NACp < 8 sau NIC < 7 (cu excepția
  NIC 0 „necunoscut” cu NACp ≥ 10) – pragurile 14 CFR 91.227(c) (NACp < 0,05 NM, NIC < 0,2 NM), regula
  „gev-nic-nacp-v2” din github.com/glebprokopchuk/gps-jamming-daily (jam.mjs); doar poziții ADS-B
  v1/v2 proprii (nu MLAT/TIS-B: readsb raportează nic/rc ale poziției, oricare i-ar fi sursa, iar la
  v0 nac_p e dedus din codul de tip). Scorul pe zonă e cel al gpsjam.org: (rele − 1)/(bune + rele),
  benzi 2 % și 10 % (din extrase ale FAQ gpsjam.org; site-ul nu a putut fi citit direct).
- Așteptare: pe 8 min, drum ≥ 12 NM, deplasare netă / drum ≤ 0,35, rază în jurul centroidului ≤ 10 NM,
  adevărat în două evaluări la ≥ 4 min distanță. La eșantionare de 60 s direcția virajului dintre două
  puncte e ambiguă, deci se folosește geometria pozițiilor, nu suma schimbărilor de direcție.
- Întoarcere: direcția deplasării în [t−12, t−6] min diferă cu ≥ 150° de cea din [t−4, t] min, ambele
  segmente drepte (D/L ≥ 0,8) și ≥ 5 NM, la ≥ 10 000 ft sau la > 20 NM de LRIA/LUKK.
- Urgență: squawk 7500/7600/7700 sau câmpul emergency, confirmat în ≥ 2 instantanee la ≥ 25 s distanță
  (7500: ≥ 3, sau emergency == "unlawful"); readsb cere deja de două ori același squawk, dar
  agregatoarele amestecă mulți receptori.
- Acoperire: `total` nu ajută; se folosesc vechimea lui `now`, seen_pos median, contorul `messages` al
  receptorului local și o zonă de control largă. Un instantaneu vechi (> 45 s) sau repetat (`now` care
  nu avansează) nu e o observație nouă: analizele pe aeronavă nu rulează pe el (altfel o urgență sau o
  „lovitură” GNSS s-ar confirma singură). Scădere reală = 0 aeronave în 3 citiri SĂNĂTOASE consecutive,
  cu zona de control confirmată normală (când e configurată).

ADS-B vede doar aeronave cu transponder. Dronele nu apar aici: tot ce produce modulul e context.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import math
import os
import re
import statistics
from collections import deque
from dataclasses import dataclass, field, replace

from . import geo
from .timeutil import UTC, parse_iso

NM_KM = 1.852
MIL, PIA, LADD = 1, 4, 8  # biții dbFlags (README-json.md)

# Squawk-uri de urgență și starea ADS-B „emergency” (README-json.md; mode_s.c: general = 7700,
# nordo = 7600, unlawful = 7500). „reserved” și „none” nu sunt urgențe.
EMERG_SQUAWKS = ("7500", "7600", "7700")
EMERG_STATUS = {"general": "7700", "nordo": "7600", "unlawful": "7500",
                "lifeguard": "lifeguard", "minfuel": "minfuel", "downed": "downed"}
EMERG_MEANING_RO = {
    "7700": "urgență generală (adesea medicală)",
    "7600": "pierderea legăturii radio",
    "7500": "interferență ilicită",
    "lifeguard": "zbor sanitar prioritar",
    "minfuel": "combustibil minim",
    "downed": "aterizare forțată / aeronavă căzută",
}
COMPASS_RO = ("N", "NE", "E", "SE", "S", "SV", "V", "NV")
_CATEGORY_RX = re.compile(r"^[A-D][0-7]$")

GOOD, BAD, LOST = "bun", "degradat", "pierdut"


@dataclass
class AdsbAnalysisConfig:
    """Praguri. Valorile implicite vin din cercetarea ADS-B (docs + sursa readsb); toate se pot
    suprascrie din constructor: AdsbAnalyzer(gnss_min_n=5, control_area="control")."""

    # --- general / politică
    control_area: str | None = None  # numele zonei largi de control (actualizați-o PRIMA la fiecare ciclu)
    max_seen_s: float = 30.0  # aeronavă fără mesaj de > 30 s: ignorată la analizele pe aeronavă
    state_ttl_s: float = 300.0  # starea pe aeronavă dispare după 5 min fără apariții
    max_tracked: int = 2000  # plafon de memorie pe zonă
    last_position_max_age_s: float = 900.0  # lastPosition folosit la plasare (aircraft.json) doar ≤ 15 min
    db_guard_min_aircraft: int = 3  # ≥ 3 aeronave fără r/t/dbFlags = readsb fără --db-file
    airports: tuple = ((geo.LRIA.lat, geo.LRIA.lon), (geo.LUKK.lat, geo.LUKK.lon))
    alt_round_ft: int = 1000  # altitudinile din rezultat se rotunjesc (nu identifică aeronava)

    # --- GNSS (gpsjam + regula NACp/NIC)
    gnss_window_s: float = 600.0  # fereastra glisantă: aeronave distincte în ultimele 10 min, starea cea mai rea
    gnss_min_n: int = 4  # sub 4 aeronave eligibile nu se calculează procentul
    gnss_nacp_min: int = 8  # NACp < 8 (EPU ≥ 0,05 NM) = degradat
    gnss_nic_min: int = 7  # NIC < 7 (Rc ≥ 0,2 NM) = degradat
    gnss_nic0_nacp_ok: int = 10  # NIC 0 (necunoscut) e acceptat dacă NACp ≥ 10
    gnss_min_alt_ft: float = 2000.0
    gnss_min_gs_kt: float = 100.0
    gnss_max_seen_pos_s: float = 30.0
    gnss_medium_ratio: float = 0.02  # banda gpsjam „galben”: 2–10 %
    gnss_enter_ratio: float = 0.10  # banda gpsjam „roșu”: > 10 %
    gnss_exit_ratio: float = 0.02
    gnss_baseline_margin: float = 0.10  # pragul de intrare = max(0,10; p90 de fond + 0,10)
    gnss_enter_evals: int = 2  # evaluări consecutive (la ≥ 25 s) necesare pentru intrare
    gnss_exit_evals: int = 3  # evaluări „curate” consecutive necesare pentru ieșire
    gnss_min_eval_gap_s: float = 25.0
    gnss_min_on_s: float = 600.0  # cel puțin 10 min în starea „interferență”
    gnss_lost_enter: int = 2  # ≥ 2 aeronave cu gpsOkBefore = intrare imediată (readsb filtrează deja)
    # fără date suficiente (< gnss_min_n eligibile, de ex. spațiu aerian golit) starea NU se închide ca
    # „revenită la normal”; se închide doar după 30 min fără nicio evaluare concludentă (level „insuficient”)
    gnss_stale_exit_s: float = 1800.0

    # --- urgențe
    emerg_confirm: int = 2  # instantanee cu același cod
    emerg_confirm_7500: int = 3  # 7500 doar cu 3 instantanee sau cu emergency == "unlawful"
    emerg_min_gap_s: float = 25.0
    emerg_end_missing: int = 2  # evenimentul se încheie după 2 instantanee fără cod
    emerg_dedup_s: float = 1800.0  # aceeași aeronavă, același cod: nu e „nou” timp de 30 min

    # --- manevre (așteptare / întoarcere)
    track_keep_s: float = 780.0  # istoricul de poziții: 13 min (întoarcerea are nevoie de 12)
    man_max_seen_pos_s: float = 20.0
    man_min_gs_kt: float = 140.0
    man_min_gs_nocat_kt: float = 160.0  # fără categorie: viteză mai mare (exclude aviația ușoară)
    man_min_alt_ft: float = 3000.0
    loiter_window_s: float = 480.0
    loiter_min_points: int = 6
    loiter_min_span_s: float = 300.0
    loiter_min_path_nm: float = 12.0
    loiter_max_ratio: float = 0.35  # deplasare netă / drum parcurs
    loiter_max_radius_nm: float = 10.0
    holding_confirm_s: float = 240.0  # „buclă” în două evaluări la ≥ 4 min
    turnback_before_s: tuple = (720.0, 360.0)  # segmentul „înainte”: [t−12, t−6] min
    turnback_after_s: float = 240.0  # segmentul „după”: [t−4, t] min
    turnback_min_points: int = 3
    # fiecare segment trebuie să acopere ≥ 75 % din fereastra lui (ca loiter_min_span_s): altfel o urmă
    # abia începută, în viraj continuu (arc DME, orbită), are un segment „înainte” de 2 min care pare drept
    turnback_min_cover: float = 0.75
    turnback_min_deg: float = 150.0
    turnback_min_leg_nm: float = 5.0
    turnback_min_straight: float = 0.8
    turnback_min_alt_ft: float = 10000.0
    turnback_airport_nm: float = 20.0  # sub 10 000 ft, aproape de aeroport = manevră de apropiere
    maneuver_window_s: float = 1200.0  # „recent” = ultimele 20 min
    maneuver_alert_min: int = 2  # ≥ 2 aeronave (așteptare și/sau întoarcere)

    # --- acoperire / scădere reală
    stale_s: float = 45.0  # `now` din răspuns mai vechi de 45 s = date vechi
    max_median_seen_pos_s: float = 30.0
    messages_stall_polls: int = 2  # receptor local: contorul `messages` neschimbat de 2 ori la rând
    control_max_age_s: float = 300.0  # date de control mai vechi sunt ignorate
    drop_zero_polls: int = 3
    drop_min_baseline: float = 2.0
    control_min_fraction: float = 0.5
    baseline_s: float = 7200.0  # fondul: mediana ultimelor 2 h…
    baseline_exclude_recent_s: float = 600.0  # …fără ultimele 10 min
    baseline_min_samples: int = 10


# ---------------------------------------------------------------------------
# utilitare (fără stare)
# ---------------------------------------------------------------------------

def _num(v) -> float | None:
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    try:
        f = float(v)
    except OverflowError:  # întreg JSON uriaș
        return None
    return f if math.isfinite(f) else None


def _int(v) -> int | None:
    return v if isinstance(v, int) and not isinstance(v, bool) else None


def _ts(v) -> float | None:
    """datetime (fără fus = UTC, ca în update()), epoch sau text ISO (cum îl întoarce store) → epoch s."""
    if isinstance(v, dt.datetime):
        return (v if v.tzinfo else v.replace(tzinfo=UTC)).timestamp()
    if isinstance(v, str):
        p = parse_iso(v)
        return p.timestamp() if p else None
    return _num(v)


def _flags(ac: dict) -> int | None:
    v = ac.get("dbFlags")
    if v is None:
        return 0
    try:
        return int(v)
    except (TypeError, ValueError, OverflowError):  # json.loads acceptă Infinity/NaN
        return None  # necunoscut


def is_military(ac: dict) -> bool:
    """dbFlags & 1. Un dbFlags ilizibil e tratat ca militar (excludere prudentă)."""
    f = _flags(ac)
    return f is None or bool(f & MIL)


def is_private(ac: dict) -> bool:
    """PIA (dbFlags & 4) sau LADD (dbFlags & 8)."""
    return bool((_flags(ac) or 0) & (PIA | LADD))


def aircraft_list(data: dict) -> list[dict]:
    """Lista de aeronave CIVILE dintr-un răspuns re-api ({"ac": [...]}) sau aircraft.json /
    re-api fără jv2 ({"aircraft": [...]}). Militarii sunt eliminați aici, înaintea oricărui alt pas."""
    if not isinstance(data, dict):
        return []
    lst = data.get("ac")
    if lst is None:
        lst = data.get("aircraft")
    if not isinstance(lst, list):
        return []
    return [a for a in lst if isinstance(a, dict) and not is_military(a)]


def snapshot_meta(data: dict, *, server_filtered: bool | None = None) -> dict:
    """Metadatele instantaneului pentru AdsbAnalyzer.update(source_meta=...).

    - ok: False dacă răspunsul nu are o listă de aeronave ("ac"/"aircraft") sau un `now` utilizabil
      (atunci format = None și update() îl tratează ca sursă indisponibilă, nu ca trafic zero);
    - data_now: momentul datelor (s epoch); jv2 dă ms, aircraft.json dă s;
    - messages: contorul global al receptorului local (doar aircraft.json);
    - server_filtered: True când serverul a filtrat deja pe cerc (re-api, implicit), False pentru
      aircraft.json (atunci filtrăm noi după distanța față de centrul zonei)."""
    data = data if isinstance(data, dict) else {}
    now_v = _num(data.get("now"))
    data_now = None if now_v is None or now_v <= 0 else (now_v / 1000.0 if now_v > 1e11 else now_v)
    if isinstance(data.get("ac"), list):
        fmt = "jv2"
    elif isinstance(data.get("aircraft"), list) and "resultCount" not in data:
        # aircraft.json (readsb/tar1090); fără „resultCount” nu e un răspuns re-api filtrat pe cerc,
        # deci filtrăm noi pe distanță (prudent: un cerc al serverului rămâne în rază oricum)
        fmt = "aircraft_json"
    elif isinstance(data.get("aircraft"), list):
        fmt = "reapi"
    else:
        fmt = None
    # Un corp fără listă de aeronave ({}, {"msg": "..."}, pagină de eroare) sau fără `now` utilizabil
    # NU e „trafic zero”: e o cerere eșuată (altfel motorul ar vedea o scădere falsă la 0).
    # Toate formatele verificate în api.c / json_out.c au `now`.
    ok = fmt is not None and data_now is not None
    msgs = _int(data.get("messages")) if fmt == "aircraft_json" else None
    sf = (fmt != "aircraft_json") if server_filtered is None else bool(server_filtered)
    return {"ok": ok, "format": fmt, "data_now": data_now, "messages": msgs, "server_filtered": sf}


def _on_ground(ac: dict) -> bool:
    return ac.get("alt_baro") == "ground" or ac.get("ground") is True


def _latlon(lat, lon) -> tuple[float, float] | None:
    lat, lon = _num(lat), _num(lon)
    if lat is None or lon is None or not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        return None  # în afara domeniului: haversine ar ieși din domeniul asin/sqrt
    return lat, lon


def _pos(ac: dict) -> tuple[float, float] | None:
    return _latlon(ac.get("lat"), ac.get("lon"))


def _place(ac: dict, max_last_age: float) -> tuple[float, float] | None:
    """Poziția pentru plasare (zonă, distanță, direcție): lat/lon, altfel lastPosition recent,
    altfel ultima poziție GPS bună (gpsOkLat/gpsOkLon)."""
    p = _pos(ac)
    if p:
        return p
    lp = ac.get("lastPosition")
    if isinstance(lp, dict):
        age = _num(lp.get("seen_pos"))
        q = _pos(lp)
        if q and age is not None and age <= max_last_age:
            return q
    return _latlon(ac.get("gpsOkLat"), ac.get("gpsOkLon"))


def _src_list(ac: dict, key: str) -> list | None:
    """mlat[] / tisb[] (mereu liste în readsb); None dacă valoarea e malformată."""
    v = ac.get(key)
    if v is None:
        return []
    return v if isinstance(v, list) else None


def _mlat_pos(ac: dict) -> bool:
    m = _src_list(ac, "mlat")
    return m is not None and "lat" in m


def _adsb_position(ac: dict) -> bool:
    """Poziție transmisă de aeronavă prin ADS-B (adresă ICAO), nu calculată prin MLAT/TIS-B."""
    if ac.get("type") != "adsb_icao" or _pos(ac) is None:
        return False
    mlat, tisb = _src_list(ac, "mlat"), _src_list(ac, "tisb")
    if mlat is None or tisb is None:
        return False  # sursa poziției nu poate fi stabilită
    return "lat" not in mlat and "lat" not in tisb


def _nm(a: tuple[float, float], b: tuple[float, float]) -> float:
    return geo.haversine_km(a[0], a[1], b[0], b[1]) / NM_KM


def _bearing(a: tuple[float, float], b: tuple[float, float]) -> float:
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dl = math.radians(b[1] - a[1])
    x = math.sin(dl) * math.cos(p2)
    y = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360.0) % 360.0


def compass_ro(deg: float) -> str:
    return COMPASS_RO[int(((deg % 360.0) + 22.5) // 45.0) % 8]


def _angle_diff(a: float, b: float) -> float:
    return abs((b - a + 180.0) % 360.0 - 180.0)


def emergency_code(ac: dict) -> str | None:
    sq = ac.get("squawk")
    if isinstance(sq, str) and sq in EMERG_SQUAWKS:
        return sq
    em = ac.get("emergency")
    return EMERG_STATUS.get(em) if isinstance(em, str) else None


# ---------------------------------------------------------------------------
# stare în memorie
# ---------------------------------------------------------------------------

@dataclass
class _Track:
    seen: float
    pts: deque = field(default_factory=deque)  # (t_poziție, lat, lon, alt_ft)
    loiter_since: float | None = None
    holding: bool = False
    turnback_at: float | None = None


@dataclass
class _GnssState:
    on: bool = False
    since: float | None = None
    hits: int = 0
    hit_t: float | None = None
    clears: int = 0
    clear_t: float | None = None
    evidence_t: float | None = None  # ultima evaluare concludentă cât timp starea e activă
    baseline: float | None = None
    last: dict | None = None


@dataclass
class _Area:
    name: str
    lat: float | None = None
    lon: float | None = None
    radius_nm: float | None = None
    last_t: float | None = None
    tracks: dict = field(default_factory=dict)  # cheie → _Track
    gnss_ac: dict = field(default_factory=dict)  # cheie → {"seen", "bad", "lost"}
    gnss: _GnssState = field(default_factory=_GnssState)
    emerg: dict = field(default_factory=dict)  # cheie → stare urgență
    emerg_done: dict = field(default_factory=dict)  # cheie|cod → ultima apariție confirmată
    holding_recent: dict = field(default_factory=dict)  # cheie → (t, detaliu agregat)
    turnback_recent: dict = field(default_factory=dict)  # cheie → (t, detaliu agregat)
    counts: deque = field(default_factory=deque)  # (t, aeronave în aer) – doar agregat
    last_count: int | None = None
    zero_streak: int = 0  # citiri SĂNĂTOASE consecutive cu 0 aeronave în aer
    raw_zero_streak: int = 0  # citiri consecutive cu 0 aeronave, oricare ar fi starea datelor
    last_messages: int | None = None
    msg_stall: int = 0
    last_data_now: float | None = None  # pentru instantanee repetate (cache înghețat)
    db_state: bool | None = None  # True: readsb are --db-file (r/t/dbFlags văzute); False: lipsă; None: necunoscut


class AdsbAnalyzer:
    """Analizor în memorie, pe zone numite. Nu persistă nimic; un singur fir de execuție."""

    def __init__(self, cfg: AdsbAnalysisConfig | None = None, **overrides):
        self.cfg = replace(cfg or AdsbAnalysisConfig(), **overrides)
        self._secret = os.urandom(16)
        self._areas: dict[str, _Area] = {}

    # ------------------------------------------------------------------ utilitare
    def _key(self, hex_addr: str) -> str:
        return hashlib.blake2s(hex_addr.strip().lower().encode(), key=self._secret, digest_size=12).hexdigest()

    def _area(self, name: str) -> _Area:
        a = self._areas.get(name)
        if a is None:
            a = self._areas[name] = _Area(name)
        return a

    def _detail(self, center, p, alt) -> dict:
        r = self.cfg.alt_round_ft
        out = {"dist_km": None, "bearing": None,
               "alt_ft": int(round(alt / r) * r) if alt is not None else None}
        if p is not None and center[0] is not None:
            out["dist_km"] = float(round(geo.haversine_km(center[0], center[1], p[0], p[1])))
            out["bearing"] = compass_ro(_bearing(center, p))
        return out

    def set_gnss_baseline(self, area_name: str, p90_ratio: float | None):
        """Fondul GNSS al zonei (p90 al raportului pe 7 zile, calculat de motor din agregatele
        stocate). Pragul de intrare devine max(gnss_enter_ratio, p90 + gnss_baseline_margin)."""
        self._area(area_name).gnss.baseline = p90_ratio

    def seed_counts(self, area_name: str, samples):
        """Preîncarcă fondul de trafic (după repornire) din eșantioane agregate (t, aeronave în aer),
        de ex. din store.adsb_samples(); doar numere, fără identități.
        t: datetime (fără fus = UTC), epoch s sau text ISO (coloana `ts` din store); rândurile
        ilizibile sunt ignorate."""
        a = self._area(area_name)
        for s in samples or []:
            try:
                t, n = s[0], s[1]
            except (TypeError, IndexError, KeyError):
                continue
            ts, nv = _ts(t), _num(n)
            if ts is None or nv is None or nv < 0:
                continue
            a.counts.append((ts, int(nv)))
        a.counts = deque(sorted(a.counts, key=lambda s: s[0]))  # prune presupune ordinea în timp

    def _baseline(self, a: _Area, t: float) -> float | None:
        c = self.cfg
        vals = [n for ts, n in a.counts if t - c.baseline_s <= ts <= t - c.baseline_exclude_recent_s]
        return float(statistics.median(vals)) if len(vals) >= c.baseline_min_samples else None

    def state_size(self) -> dict:
        """Dimensiunea stării din memorie (diagnostic/teste): doar numărători."""
        return {n: {"tracks": len(a.tracks), "gnss": len(a.gnss_ac), "emergencies": len(a.emerg),
                    "dedup": len(a.emerg_done), "recent": len(a.holding_recent) + len(a.turnback_recent)}
                for n, a in self._areas.items()}

    def prune(self, now: dt.datetime):
        """Șterge starea expirată din toate zonele (apelat automat la fiecare update).
        Un datetime fără fus e UTC (ca în update())."""
        self._prune_all(_ts(now))

    def _prune_all(self, t: float):
        c = self.cfg
        for a in self._areas.values():
            for k in [k for k, tr in a.tracks.items() if t - tr.seen > c.state_ttl_s]:
                del a.tracks[k]
            if len(a.tracks) > c.max_tracked:
                for k in sorted(a.tracks, key=lambda k: a.tracks[k].seen)[: len(a.tracks) - c.max_tracked]:
                    del a.tracks[k]
            for k in [k for k, e in a.gnss_ac.items() if t - e["seen"] > c.gnss_window_s]:
                del a.gnss_ac[k]
            for k in [k for k, e in a.emerg.items() if t - e["seen"] > c.state_ttl_s]:
                del a.emerg[k]
            for k in [k for k, v in a.emerg_done.items() if t - v > c.emerg_dedup_s]:
                del a.emerg_done[k]
            for d in (a.holding_recent, a.turnback_recent):
                for k in [k for k, v in d.items() if t - v[0] > c.maneuver_window_s]:
                    del d[k]
            while a.counts and t - a.counts[0][0] > c.baseline_s:
                a.counts.popleft()

    # ------------------------------------------------------------------ intrare
    def update(self, area_name: str, center_lat: float, center_lon: float, radius_nm: float,
               aircraft: list[dict], now: dt.datetime, source_meta: dict | None = None) -> dict:
        """Analizează un instantaneu pentru o zonă și întoarce un dicționar JSON (fără identități).

        aircraft: lista din aircraft_list() (militarii sunt eliminați oricum și aici).
        source_meta: de la snapshot_meta(); {"ok": False} = cererea a eșuat (lista e ignorată).
        now: datetime (fără fus = UTC).
        Cheile "point", "civil_airborne", "civil_total" au semantica din collectors.count_aircraft
        (pentru fondul existent din motor); singura diferență: cu --json-separate-ground, o aeronavă cu
        "ground": true nu e numărată „în aer”.
        Analizele pe aeronavă (GNSS, urgențe, manevre) rulează doar pe date proaspete și nerepetate,
        și doar după ce zona a văzut dovada că readsb are baza de date (r/t/dbFlags)."""
        c = self.cfg
        t = _ts(now)
        sm = source_meta if isinstance(source_meta, dict) else {}
        server_filtered = sm.get("server_filtered", True) is not False
        source_ok = sm.get("ok", True) is not False
        a = self._area(area_name)
        a.lat, a.lon, a.radius_nm = center_lat, center_lon, radius_nm
        center = (center_lat, center_lon)

        data_now = _num(sm.get("data_now")) if source_ok else None
        data_age = None if data_now is None else t - data_now
        age_shift = min(max(data_age or 0.0, 0.0), 3600.0)  # seen/seen_pos sunt relative la `now` din date
        # date vechi sau același instantaneu de două ori (cache înghețat): nu sunt observații noi;
        # altfel o urgență sau o „lovitură” GNSS s-ar confirma singură din aceeași citire repetată
        stale = data_age is not None and data_age > c.stale_s
        repeated = data_now is not None and a.last_data_now is not None and data_now <= a.last_data_now
        if data_now is not None:
            a.last_data_now = data_now if a.last_data_now is None else max(a.last_data_now, data_now)

        # 1) militarii afară, înainte de orice
        acs = aircraft if isinstance(aircraft, (list, tuple)) and source_ok else []
        civ = [ac for ac in acs if isinstance(ac, dict) and not is_military(ac)]

        # 2) plasare în zonă (doar dacă serverul n-a filtrat deja pe cerc)
        in_area: list[tuple[dict, tuple | None]] = []
        unplaced = 0
        for ac in civ:
            p = _place(ac, c.last_position_max_age_s)
            if not server_filtered:
                if p is None:
                    unplaced += 1
                    continue
                if _nm(center, p) > radius_nm:
                    continue
            in_area.append((ac, p))

        # 3) numărători agregate (paritate cu collectors.count_aircraft când lipsește cheia „ground”;
        #    cu --json-separate-ground, alt_baro e numeric și „ground”: true marchează solul)
        total = len(in_area)
        airborne = sum(1 for ac, _ in in_area if not _on_ground(ac) and ac.get("lat") is not None)
        gps_lost = sum(1 for ac, _ in in_area
                       if not _on_ground(ac) and ac.get("lat") is None and "gpsOkBefore" in ac)
        mlat = sum(1 for ac, _ in in_area if ac.get("lat") is not None and _mlat_pos(ac))
        sp_vals = [v for ac, _ in in_area if (v := _num(ac.get("seen_pos"))) is not None]
        med_sp = statistics.median(sp_vals) if sp_vals else None

        # readsb fără --db-file: nu putem exclude militarii → nicio analiză pe aeronavă. Starea e
        # persistentă pe zonă: confirmată de orice r/t/dbFlags, „lipsă” după ≥ 3 aeronave fără ele;
        # cât timp e necunoscută (ex. < 3 aeronave la pornire) analiza pe aeronavă nu rulează.
        if any(k in ac for ac in civ for k in ("r", "t", "dbFlags")):
            a.db_state = True
        elif len(civ) >= c.db_guard_min_aircraft:
            a.db_state = False
        db_missing = a.db_state is False
        analyse = source_ok and a.db_state is True and not stale and not repeated

        # 4) setul pentru analizele pe aeronavă: fără confidențiale, fără mesaje vechi
        per_ac: list[tuple[str, dict, tuple | None]] = []
        if analyse:
            for ac, p in in_area:
                hx = ac.get("hex")
                if not isinstance(hx, str) or not hx.strip() or is_private(ac):
                    continue
                seen = _num(ac.get("seen"))
                if seen is not None and seen > c.max_seen_s:
                    continue
                per_ac.append((self._key(hx), ac, p))

        gnss = self._gnss(a, per_ac, t, analyse)
        emergencies = self._emergencies(a, per_ac, t, center) if analyse else []
        if analyse:
            self._track(a, per_ac, t, age_shift, center)
        holding_now = sum(1 for tr in a.tracks.values() if tr.holding and tr.seen == t)
        W = c.maneuver_window_s
        hold_keys = {k for k, v in a.holding_recent.items() if t - v[0] <= W}
        turn_keys = {k for k, v in a.turnback_recent.items() if t - v[0] <= W}
        hold_recent = [a.holding_recent[k][1] for k in hold_keys]
        turn_recent = [a.turnback_recent[k][1] for k in turn_keys]
        # aeronave DISTINCTE: una care se întoarce și apoi intră în așteptare contează o singură dată
        man_aircraft = len(hold_keys | turn_keys)
        maneuvers = ([{"kind": "asteptare", **d} for d in hold_recent]
                     + [{"kind": "intoarcere", **d} for d in turn_recent])

        # 5) acoperire și scădere reală
        stalled = False
        msgs = _int(sm.get("messages"))
        if msgs is not None:
            if a.last_messages is not None and msgs == a.last_messages:
                a.msg_stall += 1
            else:
                a.msg_stall = 0
            a.last_messages = msgs
            stalled = a.msg_stall >= c.messages_stall_polls

        control_ok = None
        ctl = self._areas.get(c.control_area) if c.control_area and c.control_area != area_name else None
        if ctl is not None and ctl.last_count is not None and ctl.last_t is not None \
                and t - ctl.last_t <= c.control_max_age_s:
            cb = self._baseline(ctl, t)
            if cb is not None and cb >= c.drop_min_baseline:
                control_ok = ctl.last_count >= c.control_min_fraction * cb

        if not source_ok:
            reason = "sursa_indisponibila"
        elif db_missing:
            reason = "fara_db"
        elif stale or repeated:
            reason = "date_vechi"
        elif stalled:
            reason = "receptor_fara_mesaje"
        elif med_sp is not None and med_sp > c.max_median_seen_pos_s:
            reason = "pozitii_vechi"
        elif control_ok is False:
            reason = "control_scazut"
        else:
            reason = "ok"
        cov_ok = reason == "ok"

        eff = airborne + gps_lost  # aeronavele fără GPS nu sunt o „scădere de trafic”
        # scădere reală: 0 aeronave în N citiri SĂNĂTOASE consecutive (o citire nesănătoasă resetează),
        # altfel 3 cereri eșuate + o singură citire bună cu 0 ar părea „scădere reală”
        a.zero_streak = a.zero_streak + 1 if (cov_ok and eff == 0) else 0
        a.raw_zero_streak = a.raw_zero_streak + 1 if eff == 0 else 0
        base = self._baseline(a, t)
        base_ok = base is not None and base >= c.drop_min_baseline
        # cu o zonă de control configurată, scăderea e „reală” doar dacă zona de control e confirmată
        # normală (date proaspete + fond); necunoscut ≠ normal
        control_needed = bool(c.control_area) and c.control_area != area_name
        real = (cov_ok and base_ok and a.zero_streak >= c.drop_zero_polls
                and (control_ok is True or not control_needed))
        suspected = not real and base_ok and a.raw_zero_streak >= c.drop_zero_polls
        if cov_ok:  # fondul se construiește doar din date sănătoase
            a.counts.append((t, eff))
        a.last_count = eff if cov_ok else a.last_count
        a.last_t = t if cov_ok else a.last_t

        self._prune_all(t)
        return {
            "point": area_name,
            "civil_airborne": airborne,
            "civil_total": total,
            "civil_gps_lost": gps_lost,
            "civil_mlat": mlat,
            "civil_unplaced": unplaced,
            "gnss": gnss,
            "emergencies": emergencies,
            "holding": holding_now,
            "holding_recent": len(hold_recent),
            "turnbacks": len(turn_recent),
            "maneuver_aircraft": man_aircraft,
            "maneuver_alert": man_aircraft >= c.maneuver_alert_min,
            "maneuvers": maneuvers,
            "coverage": {"ok": cov_ok, "reason": reason,
                         "data_age_s": None if data_age is None else round(data_age, 1),
                         "median_seen_pos_s": None if med_sp is None else round(med_sp, 1)},
            "drop": {"real": real, "suspected_outage": suspected,
                     "zero_streak": a.zero_streak, "baseline": base, "control_ok": control_ok},
        }

    # ------------------------------------------------------------------ GNSS
    def _gnss_class(self, ac: dict) -> str | None:
        c = self.cfg
        if _on_ground(ac):
            return None
        cat = ac.get("category")
        if isinstance(cat, str) and cat.startswith("C"):
            return None  # vehicule/obstacole de sol
        alt, gs = _num(ac.get("alt_baro")), _num(ac.get("gs"))
        if "gpsOkBefore" in ac:  # detectorul readsb (gs > 50 kt, în aer, ≥ 17 mesaje)
            if (alt is None or alt >= c.gnss_min_alt_ft) and (gs is None or gs >= c.gnss_min_gs_kt):
                return LOST
            return None
        if alt is None or alt < c.gnss_min_alt_ft or gs is None or gs < c.gnss_min_gs_kt:
            return None
        if not _adsb_position(ac) or _int(ac.get("version")) not in (1, 2):
            return None
        sp = _num(ac.get("seen_pos"))
        nacp, nic = _int(ac.get("nac_p")), _int(ac.get("nic"))
        if sp is None or sp > c.gnss_max_seen_pos_s or nacp is None or nic is None:
            return None
        nic_ok = nic >= c.gnss_nic_min or (nic == 0 and nacp >= c.gnss_nic0_nacp_ok)
        return GOOD if nacp >= c.gnss_nacp_min and nic_ok else BAD

    def _gnss_stale_exit(self, st: _GnssState, t: float) -> bool:
        """Starea activă fără nicio evaluare concludentă de gnss_stale_exit_s: se închide (fără a
        pretinde că precizia „a revenit la normal”: rezultatul are level „insuficient”)."""
        if st.on and st.evidence_t is not None and t - st.evidence_t >= self.cfg.gnss_stale_exit_s:
            st.on, st.since, st.evidence_t = False, None, None
            st.clears, st.clear_t, st.hits, st.hit_t = 0, None, 0, None
            return True
        return False

    def _gnss(self, a: _Area, per_ac, t: float, analyse: bool) -> dict:
        c, st = self.cfg, a.gnss
        if not analyse:
            changed = self._gnss_stale_exit(st, t)
            return {"n": 0, "degraded": 0, "lost": 0, "ratio": 0.0, "level": "insuficient",
                    "interference": st.on, "changed": changed, "since": _iso(st.since if st.on else None),
                    "scope": None}
        for key, ac, _ in per_ac:
            cls = self._gnss_class(ac)
            if cls is None:
                continue
            e = a.gnss_ac.setdefault(key, {"seen": t, "bad": None, "lost": None})
            e["seen"] = t
            if cls == BAD:
                e["bad"] = t
            elif cls == LOST:
                e["lost"] = t
        W = c.gnss_window_s
        good = bad = lost = 0
        for e in a.gnss_ac.values():
            if t - e["seen"] > W:
                continue
            if e["lost"] is not None and t - e["lost"] <= W:
                lost += 1
            elif e["bad"] is not None and t - e["bad"] <= W:
                bad += 1
            else:
                good += 1
        n, b = good + bad + lost, bad + lost
        ratio = max(0, b - 1) / n if n >= c.gnss_min_n else 0.0  # formula gpsjam (−1 contra fals-pozitivelor)
        if n < c.gnss_min_n:
            level = "insuficient"
        elif ratio > c.gnss_enter_ratio:
            level = "ridicat"
        elif ratio >= c.gnss_medium_ratio:
            level = "mediu"
        else:
            level = "normal"

        thr = c.gnss_enter_ratio
        if st.baseline is not None:
            thr = max(thr, st.baseline + c.gnss_baseline_margin)
        hit = n >= c.gnss_min_n and b >= 2 and ratio >= thr
        lost_hit = lost >= c.gnss_lost_enter
        changed = False
        if not st.on:
            st.clears, st.clear_t = 0, None
            if hit and (st.hit_t is None or t - st.hit_t >= c.gnss_min_eval_gap_s):
                st.hits += 1
                st.hit_t = t
            elif not hit:
                st.hits, st.hit_t = 0, None
            if lost_hit or st.hits >= c.gnss_enter_evals:
                st.on, st.since, st.evidence_t, changed = True, t, t, True
                st.hits, st.hit_t = 0, None
        elif n < c.gnss_min_n and not lost_hit:
            # prea puține aeronave eligibile: nicio dovadă că precizia a revenit (de ex. spațiul aerian
            # s-a golit). Nu se numără ca evaluare „curată”; doar expirarea de mai jos închide starea.
            changed = self._gnss_stale_exit(st, t)
        else:
            st.evidence_t = t
            clear = (ratio < c.gnss_exit_ratio or b <= 1) and not lost_hit
            if clear and (st.clear_t is None or t - st.clear_t >= c.gnss_min_eval_gap_s):
                st.clears += 1
                st.clear_t = t
            elif not clear:
                st.clears, st.clear_t = 0, None
            since = st.since if st.since is not None else t
            if st.clears >= c.gnss_exit_evals and t - since >= c.gnss_min_on_s:
                st.on, changed = False, True
                st.clears, st.clear_t, st.evidence_t = 0, None, None

        scope = None
        if c.control_area and c.control_area != a.name:
            ctl = self._areas.get(c.control_area)
            last = ctl.gnss.last if ctl else None
            if last and last["n"] >= c.gnss_min_n and t - last["t"] <= c.control_max_age_s:
                scope = "local" if last["ratio"] < c.gnss_exit_ratio else "regional"
            else:
                scope = "necunoscut"
        out = {"n": n, "degraded": b, "lost": lost, "ratio": round(ratio, 3), "level": level,
               "interference": st.on, "changed": changed, "since": _iso(st.since if st.on else None),
               "scope": scope}
        st.last = {"t": t, "n": n, "ratio": ratio}
        return out

    # ------------------------------------------------------------------ urgențe
    def _emergencies(self, a: _Area, per_ac, t: float, center) -> list[dict]:
        c = self.cfg
        present = set()
        for key, ac, p in per_ac:
            code = emergency_code(ac)
            if code is None or _on_ground(ac):
                continue
            present.add(key)
            e = a.emerg.get(key)
            if e is None or e["code"] != code:
                e = a.emerg[key] = {"code": code, "count": 1, "last": t, "seen": t, "missing": 0,
                                    "confirmed": False, "new": False, "unlawful": False}
            elif t - e["last"] >= c.emerg_min_gap_s:
                e["count"] += 1
                e["last"] = t
            e["seen"], e["missing"], e["new"] = t, 0, False
            e["unlawful"] = e["unlawful"] or ac.get("emergency") == "unlawful"
            cat = ac.get("category")
            e["detail"] = {**self._detail(center, p, _num(ac.get("alt_baro"))),
                           "category": cat if isinstance(cat, str) and _CATEGORY_RX.match(cat) else None}
            need = c.emerg_confirm_7500 if code == "7500" and not e["unlawful"] else c.emerg_confirm
            dk = f"{key}|{code}"
            if not e["confirmed"] and e["count"] >= need:
                e["confirmed"] = True
                prev = a.emerg_done.get(dk)
                e["new"] = prev is None or t - prev > c.emerg_dedup_s
            if e["confirmed"]:
                a.emerg_done[dk] = t
        for key in [k for k in a.emerg if k not in present]:
            e = a.emerg[key]
            e["missing"] += 1
            if e["missing"] >= c.emerg_end_missing:
                del a.emerg[key]
        out = [{"code": e["code"], "meaning": EMERG_MEANING_RO[e["code"]], **e["detail"], "new": e["new"]}
               for e in a.emerg.values() if e["confirmed"] and e["missing"] == 0]
        return sorted(out, key=lambda x: (x["code"], x["dist_km"] if x["dist_km"] is not None else 1e9))

    # ------------------------------------------------------------------ manevre
    def _man_eligible(self, ac: dict) -> bool:
        c = self.cfg
        if _on_ground(ac) or not _adsb_position(ac):
            return False
        sp, alt, gs = _num(ac.get("seen_pos")), _num(ac.get("alt_baro")), _num(ac.get("gs"))
        if sp is None or sp > c.man_max_seen_pos_s or alt is None or alt < c.man_min_alt_ft or gs is None:
            return False
        cat = ac.get("category")
        if isinstance(cat, str) and cat:
            if cat in ("A1", "A7") or cat[0] in "BCD":  # ușoare, elicoptere, planoare/UAV, sol
                return False
            return gs >= c.man_min_gs_kt
        return gs >= c.man_min_gs_nocat_kt

    def _track(self, a: _Area, per_ac, t: float, age_shift: float, center):
        c = self.cfg
        for key, ac, _ in per_ac:
            ok = self._man_eligible(ac)
            tr = a.tracks.get(key)
            if tr is None:
                if not ok:
                    continue
                tr = a.tracks[key] = _Track(seen=t)
            tr.seen = t
            if ok:
                pt = t - age_shift - (_num(ac.get("seen_pos")) or 0.0)
                if not tr.pts or pt > tr.pts[-1][0] + 1.0:  # deduplicare după timpul poziției
                    tr.pts.append((pt, float(ac["lat"]), float(ac["lon"]), _num(ac.get("alt_baro"))))
            while tr.pts and t - tr.pts[0][0] > c.track_keep_s:
                tr.pts.popleft()
        for key, tr in a.tracks.items():
            if tr.seen != t or not tr.pts:
                continue
            last = tr.pts[-1]
            if self._loiter(tr, t):
                if tr.loiter_since is None:
                    tr.loiter_since = t
                tr.holding = t - tr.loiter_since >= c.holding_confirm_s
            else:
                tr.loiter_since, tr.holding = None, False
            if tr.holding:
                a.holding_recent[key] = (t, self._detail(center, (last[1], last[2]), last[3]))
            elif (tr.turnback_at is None or t - tr.turnback_at > c.maneuver_window_s) and self._turnback(tr, t):
                tr.turnback_at = t
                a.turnback_recent[key] = (t, self._detail(center, (last[1], last[2]), last[3]))

    @staticmethod
    def _seg(pts) -> tuple[float, float, float]:
        """(drum L, deplasare netă D, direcția deplasării) în NM/grade."""
        L = sum(_nm(pts[i][1:3], pts[i + 1][1:3]) for i in range(len(pts) - 1))
        return L, _nm(pts[0][1:3], pts[-1][1:3]), _bearing(pts[0][1:3], pts[-1][1:3])

    def _loiter(self, tr: _Track, t: float) -> bool:
        c = self.cfg
        w = [q for q in tr.pts if t - q[0] <= c.loiter_window_s]
        if len(w) < c.loiter_min_points or w[-1][0] - w[0][0] < c.loiter_min_span_s:
            return False
        L, D, _ = self._seg(w)
        if L < c.loiter_min_path_nm or D / L > c.loiter_max_ratio:
            return False
        cen = (sum(q[1] for q in w) / len(w), sum(q[2] for q in w) / len(w))
        return max(_nm(cen, q[1:3]) for q in w) <= c.loiter_max_radius_nm

    def _turnback(self, tr: _Track, t: float) -> bool:
        c = self.cfg
        b0, b1 = c.turnback_before_s
        s1 = [q for q in tr.pts if t - b0 <= q[0] <= t - b1]
        s2 = [q for q in tr.pts if q[0] >= t - c.turnback_after_s]
        if len(s1) < c.turnback_min_points or len(s2) < c.turnback_min_points:
            return False
        if (s1[-1][0] - s1[0][0] < c.turnback_min_cover * (b0 - b1)
                or s2[-1][0] - s2[0][0] < c.turnback_min_cover * c.turnback_after_s):
            return False
        L1, D1, h1 = self._seg(s1)
        L2, D2, h2 = self._seg(s2)
        if min(D1, D2) < c.turnback_min_leg_nm:
            return False
        if D1 / L1 < c.turnback_min_straight or D2 / L2 < c.turnback_min_straight:
            return False
        if _angle_diff(h1, h2) < c.turnback_min_deg:
            return False
        # se judecă locul virajului (între cele două segmente), nu ultima poziție: un viraj de
        # apropiere sub 10 000 ft lângă LRIA/LUKK rămâne exclus și după ce aeronava s-a depărtat
        turn = [q for q in tr.pts if s1[-1][0] <= q[0] <= s2[0][0]]
        if all(q[3] is not None and q[3] >= c.turnback_min_alt_ft for q in turn):
            return True
        return all(_nm(q[1:3], ap) > c.turnback_airport_nm for q in turn for ap in c.airports)


def _iso(ts: float | None) -> str | None:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat() if ts is not None else None
