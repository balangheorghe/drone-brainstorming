"""NOTAM: restricții și închideri de spațiu aerian lângă Iași și Prut (LRBB/LRIA, LUUU/LUKK).

Doar informare. Un NOTAM descrie o zonă, un cod, limite și un interval orar; nu conține
identități de aeronave. Semnalele (rol „notam”) sunt CONTEXT pentru motor, nu o alertă
în sine: majoritatea sunt activări militare de rutină. Modulul nu publică nimic.

Surse (proveniența formatelor: tests/fixtures/notam_SURSE.txt):
- „romatsa_wfs” (implicit, fără cheie): GeoServer-ul public ROMATSA, WFS 1.0.0 → GeoJSON.
  Proprietăți: serie („C8116/2025”), dfrom, dto (ISO sau AAMMZZHHMM), mesaj (NOTAM ICAO
  complet, rânduri separate prin \\r), tip; geometrie Polygon [lon, lat] EPSG:4326
  (abpaul/romatsa-uav-zones, TechReckoning/Drones-Restricted-Zones-RO, cukierrro/Straznik).
  Acoperă doar FIR București (LRBB), inclusiv zonele temporare de la granița cu R. Moldova.
  Serverul are o cheie Diffie-Hellman slabă: OpenSSL modern refuză negocierea
  (DH_KEY_TOO_SMALL). Doar pentru ACEST host folosim cifruri fără DH („DEFAULT:!DH”, ca
  Dutzu05/DroneApp), iar la eșec „DEFAULT:@SECLEVEL=1” (ca Straznik). Certificatul se
  verifică întotdeauna.
- „faa_nms” (credențiale cerute la FAA): NOTAM Management Service. Token OAuth2
  client_credentials (POST /v1/auth/token, Basic), apoi
  GET /nmsapi/v1/notams?latitude=&longitude=&radius= cu antetul nmsResponseFormat: GEOJSON
  → {"status": "Success", "data": {"geojson": [Feature…]}} (dnickerson/flytab,
  koala73/worldmonitor). Singura sursă găsită care ar putea avea LUUU; NECONFIRMAT.
- „text”: o pagină cu NOTAM-uri ICAO ca text simplu sau tabel HTML (ex. lista ROMATSA
  getnotamlist, al cărei format e cunoscut doar din codul arhivat ROvACC).

Formatul ICAO (antet, Q) … G)) și sensul codurilor Q: tabelul avwx-engine
(avwx/static/notam.py, după FAA JO 7930.2 Anexa B) și NOTAM-uri reale LRBB / internaționale.
"""

from __future__ import annotations

import base64
import datetime as dt
import hashlib
import html
import json
import math
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser

from . import geo, http
from .collectors import Collector
from .models import Signal
from .timeutil import UTC, iso, parse_iso, to_local

ROMATSA_HOST = "flightplan.romatsa.ro"
ROMATSA_WFS_URL = ("https://flightplan.romatsa.ro/init/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature"
                   "&typeName=carto%3Arestrictii_notam_pt_uav&maxFeatures=5000&outputFormat=application%2Fjson")
# al doilea strat (Airspace Use Plan), același format; acoperirea față de primul nu e verificată
ROMATSA_AUP_URL = ("https://flightplan.romatsa.ro/init/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature"
                   "&typeName=opr:AUP&outputFormat=application/json")
NMS_HOST = "https://api-nms.aim.faa.gov"
TLS_CIPHERS = "DEFAULT:!DH"
TLS_CIPHERS_FALLBACK = "DEFAULT:@SECLEVEL=1"

NMS_HOWTO = (
    "Sursa NOTAM „faa_nms” (FAA NOTAM Management Service) cere credențiale, iar FAA_NMS_CLIENT_ID / "
    "FAA_NMS_CLIENT_SECRET lipsesc. Cum le obțineți: scrieți la notams@faa.gov și cereți acces la NMS-API "
    "pentru mediul de producție (api-nms.aim.faa.gov); primiți un client_id („KEY”) și un client_secret "
    "(„SECRET”). Puneți-le în .env: FAA_NMS_CLIENT_ID=… și FAA_NMS_CLIENT_SECRET=…, apoi reporniți. "
    "Atenție: nu e confirmat că FAA dă acces persoanelor din afara SUA, nici că NMS conține NOTAM-urile "
    "R. Moldova (LUUU). Până atunci folosiți sursa „romatsa_wfs” (fără cheie, doar România)."
)


class NotamCredentialsError(ValueError):
    """Credențiale lipsă sau respinse pentru o sursă NOTAM (mesajul spune ce e de făcut)."""


# ---------------------------------------------------------------------------
# Coduri Q (literele 2–3 = subiect, 4–5 = condiție), după avwx-engine (FAA JO 7930.2 Anexa B)
# ---------------------------------------------------------------------------

SUBJECT_RO = {
    "RT": "zonă restricționată temporar", "RR": "zonă restricționată", "RD": "zonă periculoasă",
    "RP": "zonă interzisă", "RA": "rezervare de spațiu aerian", "RM": "zonă de operațiuni militare",
    "RO": "survol", "AF": "FIR", "AU": "FIR superior", "AE": "zonă de control (CTA)",
    "AH": "zonă de control superioară", "AT": "zonă de control terminal (TMA)", "AC": "zonă de control (CTR)",
    "AZ": "zonă de trafic de aerodrom (ATZ)", "AS": "spațiu aerian", "AR": "rută ATS", "AN": "rută RNAV",
    "FA": "aerodrom", "WU": "aeronave fără pilot", "WM": "trageri (rachete, artilerie)", "WE": "exerciții",
    "GW": "operațiuni GNSS (zonal)", "GA": "operațiuni GNSS (aerodrom)",
}
CONDITION_RO = {
    "CA": "activată", "CS": "instituită", "CD": "dezactivată", "CN": "anulată", "CH": "modificată",
    "LC": "închis(ă)", "LW": "va avea loc", "LP": "interzis(ă)", "LT": "limitat(ă)", "LI": "închis IFR",
    "AS": "nefuncțional", "AU": "indisponibil", "AW": "retras complet", "AK": "revenit la normal",
    "LF": "interferențe", "XX": "",
}

RESTRICTION_SUBJECTS = frozenset({"RT", "RR", "RD", "RP", "RA", "RM", "RO"})
AIRSPACE_SUBJECTS = frozenset({"AF", "AU", "AE", "AH", "AT", "AC", "AZ", "AS", "AO", "AV"})
ROUTE_SUBJECTS = frozenset({"AR", "AN"})
GNSS_SUBJECTS = frozenset({"GW", "GA"})
UAS_SUBJECTS = frozenset({"WU"})          # Unmanned aircraft
FIRING_SUBJECTS = frozenset({"WM"})       # Missile, gun or rocket firing
END_CONDITIONS = frozenset({"CD", "CN", "AK", "CC", "AX"})  # dezactivat, anulat, revenit la normal…
AD_CLOSED_CONDITIONS = frozenset({"LC", "AU", "AW", "LI"})
GNSS_BAD_CONDITIONS = frozenset({"AS", "AU", "LF", "LD", "LS", "XX"})

CATEGORIES = ("spatiu_aerian_inchis", "restrictie_spatiu_aerian", "drone_uas", "aeroport_inchis",
              "ruta_inchisa", "gnss", "restrictie_ridicata")
CATEGORY_RO = {
    "spatiu_aerian_inchis": "spațiu aerian închis",
    "restrictie_spatiu_aerian": "restricție de spațiu aerian",
    "drone_uas": "zboruri UAS / drone",
    "aeroport_inchis": "aeroport închis",
    "ruta_inchisa": "rută ATS închisă",
    "gnss": "GNSS indisponibil / interferențe",
    "restrictie_ridicata": "restricție ridicată",
}
KINDS = ("nou", "inlocuire", "anulare", "retras")

# „UNAMNNED” apare așa în NOTAM-uri ROMATSA reale (F8008/26); „SUAS” = small UAS (M1128/26, RJTY)
UAS_RX = re.compile(r"\b(?:UNMANNED|UNAMNNED|S?UAS|UAVS?|RPAS|DRONES?|BVLOS)\b")
AIRSPACE_CLOSED_RX = re.compile(
    r"\b(?:AIRSPACE|FIR|CTR|TMA|CTA)\b[^.\n]{0,40}?\b(?:CLSD|CLOSED)\b"
    r"|\b(?:CLSD|CLOSED)\s+(?:FOR|TO)\s+ALL\s+(?:FLT|FLIGHTS|TFC|TRAFFIC|ACFT)\b")
RESTRICTION_RX = re.compile(
    r"\b(?:RESTRICTED|PROHIBITED|DANGER|RESERVED)\s+AREAS?\b|\bTEMPORARY\s+FLIGHT\s+RESTRICTIONS?\b|\bTFR\b")
AD_CLOSED_RX = re.compile(r"\b(?:AD|AP|AIRPORT|AERODROME)\s+(?:[A-Z]+\s+)?(?:CLSD|CLOSED)\b")
_GNSS_WORD = r"\b(?:GNSS|GPS|GLONASS|GALILEO|SATELLITE\s+NAVIGATION)\b"
_GNSS_BAD = r"\b(?:INTERFERENCE|JAMMING|SPOOFING|OUTAGES?|UNRELIABLE|DEGRADED|DEGRADATION|DISRUPTIONS?)\b"
# GNSS_RX: interferențe / bruiaj / pană GNSS (semnal de context real). „NOT AVBL”/„U/S” singure NU ajung:
# „RNAV (GNSS) RWY 08 APCH NOT AVBL” e o procedură de apropiere suspendată (de rutină), nu o problemă GNSS.
GNSS_RX = re.compile(_GNSS_WORD + r".{0,120}?" + _GNSS_BAD + r"|\b(?:INTERFERENCE|JAMMING|SPOOFING)\b.{0,60}?\b(?:GNSS|GPS)\b",
                     re.S)
# GNSS_ANY_RX: și indisponibilitatea; doar pentru NOTAM-urile cu subiect GNSS (GW/GA)
GNSS_ANY_RX = re.compile(_GNSS_WORD + r".{0,120}?(?:" + _GNSS_BAD + r"|\b(?:UNAVBL|NOT\s+AVBL|U/S)(?![A-Z]))"
                         r"|\b(?:INTERFERENCE|JAMMING|SPOOFING)\b.{0,60}?\b(?:GNSS|GPS)\b", re.S)


# ---------------------------------------------------------------------------
# Structura
# ---------------------------------------------------------------------------

_ID_RX = re.compile(r"([A-Z])(\d{4})/(\d{2})")


@dataclass
class Notam:
    """Un NOTAM ICAO. Orele sunt în UTC; distanțele nu se păstrează aici (vezi distances())."""

    id: str | None                      # „P2580/26”
    type: str = "N"                     # N nou · R înlocuiește · C anulează
    ref: str | None = None              # NOTAM-ul înlocuit / anulat
    fir: str | None = None
    qcode: str | None = None            # „QRTCA”
    traffic: str | None = None          # I, V, IV
    purpose: str | None = None          # N, B, O, M, K (combinate: „BO”, „NBO”)
    scope: str | None = None            # A aerodrom, E rută, W avertizare (combinate: „AW”)
    lower_fl: int | None = None         # din linia Q (nivel de zbor; 000 = sol)
    upper_fl: int | None = None         # 999 = nelimitat
    lat: float | None = None            # centrul zonei (linia Q), grade zecimale
    lon: float | None = None
    radius_nm: int | None = None        # 999 = tot FIR-ul
    locations: list[str] = field(default_factory=list)   # A)
    start: dt.datetime | None = None    # B)
    end: dt.datetime | None = None      # C); None dacă PERM sau lipsește
    estimated: bool = False             # C) …EST
    permanent: bool = False             # C) PERM
    schedule: str | None = None         # D)
    text: str = ""                      # E)
    lower: str | None = None            # F)
    upper: str | None = None            # G)
    issued: dt.datetime | None = None   # doar unele surse (FAA NMS)
    cancelled_at: dt.datetime | None = None  # FAA NMS: cancelationDate
    polygons: list[list[tuple[float, float]]] = field(default_factory=list)  # inele (lat, lon) din sursă
    raw: str = ""

    @property
    def subject(self) -> str | None:
        return self.qcode[1:3] if self.qcode else None

    @property
    def condition(self) -> str | None:
        return self.qcode[3:5] if self.qcode else None

    @property
    def series(self) -> str | None:
        m = _ID_RX.fullmatch(self.id or "")
        return m.group(1) if m else None

    @property
    def number(self) -> int | None:
        m = _ID_RX.fullmatch(self.id or "")
        return int(m.group(2)) if m else None

    @property
    def year(self) -> int | None:
        m = _ID_RX.fullmatch(self.id or "")
        return 2000 + int(m.group(3)) if m else None

    @property
    def fir_wide(self) -> bool:
        return self.radius_nm is not None and self.radius_nm >= 999


_LOC_RX = re.compile(r"[A-Z][A-Z0-9]{2,3}")


def nof_scope(n: Notam) -> str:
    """Prefixul de naționalitate (2 litere) al FIR-ului din linia Q, altfel al primei locații din A):
    „LR” România, „LU” R. Moldova, „UK” Ucraina. Numerele NOTAM („A0123/25”) sunt unice doar pentru
    biroul NOTAM care le emite, deci o sursă cu mai multe țări (FAA NMS) poate avea același număr de
    două ori; prefixul le desparte. „” dacă nu există nicio locație."""
    for code in (n.fir, *n.locations):
        if code and _LOC_RX.fullmatch(code):
            return code[:2]
    return ""


def notam_key(n: Notam, nid: str | None = None) -> str:
    """Cheia unică a unui NOTAM (sau a NOTAM-ului nid din același birou): „LU:A0123/25”."""
    return f"{nof_scope(n)}:{nid or n.id}"


# ---------------------------------------------------------------------------
# Parser ICAO
# ---------------------------------------------------------------------------

_TAG_RX = re.compile(r"<\s*/?\s*[A-Za-z!][^<>]*>")
_BR_RX = re.compile(r"<\s*br\s*/?\s*>", re.I)
# antet: „(P2580/26 NOTAMN”, „A4460/24 NOTAMR A2844/24”, „G0105/26 NOTAMC G0552/25”.
# „(?:\(\s*)?” și nu „\(?\s*”: altfel fiecare poziție dintr-un șir lung de spații îl rescanează (timp pătratic).
_HDR_RX = re.compile(r"(?:\(\s*)?\b([A-Z])\s?(\d{1,4})\s?/\s?(\d{2})\s*NOTAM\s?([NRC])\b"
                     r"(?:\s+([A-Z])\s?(\d{1,4})\s?/\s?(\d{2})\b)?")
# cheile Q) A) … G); nu și „(F)” din „AR112H(F)” sau „REF(B)”
_KEY_RX = re.compile(r"(?<![A-Z0-9(])([QABCDEFG])\)\s*")
# FAA adaugă la final „CREATED: 13 MAR 2026 05:26 SOURCE: UUUUYNYX” (doar de la începutul unui șir de spații)
_TRAILER_RX = re.compile(r"(?<!\s)\s+CREATED:\s*\d{1,2}\s+[A-Z]{3}\s+\d{4}\b.*$", re.S)
_LIMIT_RX = re.compile(r"(?:GND|SFC|UNL|SURFACE|MSL|FL\s?\d|\d)")
_QCOORD_RX = re.compile(r"(\d{2})(\d{2})([NS])(\d{3})(\d{2})([EW])(\d{3})?")
_TEXT_COORD_RX = re.compile(r"(?<!\d)(\d{2})(\d{2})(\d{2}(?:\.\d+)?)\s?([NS])[\s-]{0,3}(\d{3})(\d{2})(\d{2}(?:\.\d+)?)\s?([EW])")


def _clean(raw: str) -> str:
    """Text → majuscule, rânduri cu \\n, fără etichete HTML/entități/spații de lățime zero."""
    s = raw if isinstance(raw, str) else ""
    if "<" in s:
        s = _TAG_RX.sub(" ", _BR_RX.sub("\n", s))
    s = html.unescape(s).replace("​", "").replace("﻿", "").replace("\xa0", " ")
    return s.replace("\r\n", "\n").replace("\r", "\n").upper()


def _strip_paren(v: str) -> str:
    """Scoate paranteza finală a NOTAM-ului „(… G) FL240)” dacă e în plus."""
    v = v.strip()
    if v.endswith(")") and v.count(")") > v.count("("):
        v = v[:-1].rstrip()
    return v


def _tidy(text: str) -> str:
    lines = [" ".join(line.split()) for line in text.split("\n")]
    return _strip_paren("\n".join(line for line in lines if line))


def _ymdhm(s: str | None) -> dt.datetime | None:
    m = re.fullmatch(r"(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})", (s or "").strip())
    if not m:
        return None
    y, mo, d, h, mi = map(int, m.groups())
    if h > 24 or mi > 59 or (h == 24 and mi):
        return None
    try:
        t = dt.datetime(2000 + y, mo, d, tzinfo=UTC)
    except ValueError:  # ex. „2604018000” (oră imposibilă) sau 31 februarie
        return None
    return t + dt.timedelta(hours=h, minutes=mi)


def _fmt_id(letter: str, num: str, yy: str) -> str:
    return f"{letter}{int(num):04d}/{yy}"


def _coord(dd, mm, hemi, ddd, mm2, hemi2) -> tuple[float, float] | None:
    if int(mm) >= 60 or int(mm2) >= 60:
        return None
    lat = int(dd) + int(mm) / 60
    lon = int(ddd) + int(mm2) / 60
    lat, lon = (-lat if hemi == "S" else lat), (-lon if hemi2 == "W" else lon)
    return (lat, lon) if -90 <= lat <= 90 and -180 <= lon <= 180 else None


def _parse_q(v: str) -> dict:
    """„LRBB/QRTCA/IV/BO /W /000/240/4517N02814E019” (câmpuri goale tolerate)."""
    parts = [p.strip() for p in v.split("\n")[0].split("/")]
    out: dict = {}
    if parts and re.fullmatch(r"[A-Z0-9]{3,4}", parts[0]):
        out["fir"] = parts[0]
    if len(parts) > 1 and re.fullmatch(r"Q[A-Z]{4}", parts[1]):
        out["qcode"] = parts[1]
    for i, key in ((2, "traffic"), (3, "purpose"), (4, "scope")):
        if len(parts) > i and re.fullmatch(r"[A-Z]{1,3}", parts[i]):
            out[key] = parts[i]
    for i, key in ((5, "lower_fl"), (6, "upper_fl")):
        if len(parts) > i and re.fullmatch(r"\d{3}", parts[i]):
            out[key] = int(parts[i])
    if len(parts) > 7:
        m = _QCOORD_RX.fullmatch(parts[7].replace(" ", ""))
        if m:
            c = _coord(*m.groups()[:6])
            if c:
                out["lat"], out["lon"] = c
                if m.group(7):
                    out["radius_nm"] = int(m.group(7))
    return out


def _locations(v: str) -> list[str]:
    out = []
    for tok in re.split(r"[\s,/]+", v.strip()):
        if re.fullmatch(r"[A-Z]{3,4}", tok) and tok != "PART":
            out.append(tok)
        elif tok:
            break  # „LTBB LGGG PART 1 OF 2” → [LTBB, LGGG]
    return out


def parse_icao_notam(raw: str) -> Notam | None:
    """Un NOTAM ICAO (cu sau fără paranteze, pe mai multe rânduri sau pe unul singur).

    Întoarce None dacă textul nu are nici antet („A1234/26 NOTAMN”) nici linie Q validă."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    s = _TRAILER_RX.sub("", _clean(raw)).strip()
    hm = _HDR_RX.search(s)
    keys = [(m.group(1), m.start(), m.end()) for m in _KEY_RX.finditer(s, hm.end() if hm else 0)]
    e_key = next((k for k in keys if k[0] == "E"), None)
    end_head = e_key[1] if e_key else len(s)
    head = [k for k in keys if k[1] < end_head]
    vals: dict[str, str] = {}
    for i, (k, _st, en) in enumerate(head):
        nxt = head[i + 1][1] if i + 1 < len(head) else end_head
        vals.setdefault(k, s[en:nxt].strip())
    if e_key:
        # după E) contează doar F) și G) urmate de o limită (E poate conține „A)”, „C)” ca liste)
        tail = [k for k in keys if k[1] > e_key[1] and k[0] in "FG" and _LIMIT_RX.match(s, k[2])]
        f = next((k for k in reversed(tail) if k[0] == "F"), None)
        g = next((k for k in reversed(tail) if k[0] == "G" and (f is None or k[1] > f[1])), None)
        stops = [k[1] for k in (f, g) if k]
        vals["E"] = s[e_key[2]:min(stops) if stops else len(s)]
        if f:
            vals["F"] = s[f[2]:g[1] if g else len(s)]
        if g:
            vals["G"] = s[g[2]:]
    q = _parse_q(vals["Q"]) if "Q" in vals else {}
    if hm is None and "qcode" not in q:
        return None
    n = Notam(id=_fmt_id(*hm.group(1, 2, 3)) if hm else None, raw=raw)
    if hm:
        n.type = hm.group(4)
        if hm.group(5):
            n.ref = _fmt_id(*hm.group(5, 6, 7))
    for k, v in q.items():
        setattr(n, k, v)
    n.locations = _locations(vals.get("A", ""))
    m = re.match(r"(\d{10})", vals.get("B", ""))
    n.start = _ymdhm(m.group(1)) if m else None
    cv = vals.get("C", "")
    if re.match(r"PERM\b", cv):
        n.permanent = True
    else:
        m = re.match(r"(\d{10})\s*(EST)?", cv)
        if m:
            n.end, n.estimated = _ymdhm(m.group(1)), bool(m.group(2))
    n.schedule = (scrub_text(" ".join(vals["D"].split())) or None) if "D" in vals else None
    n.text = _tidy(vals.get("E", ""))
    for key, attr in (("F", "lower"), ("G", "upper")):
        if key in vals:
            v = _strip_paren(vals[key].split("\n")[0])
            setattr(n, attr, " ".join(v.split()) or None)
    return n


class _TableParser(HTMLParser):
    """Rânduri și celule dintr-un tabel HTML; <br> → rând nou."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows: list[list[list[str]]] = []
        self._row: list | None = None
        self._cell: list | None = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row, self._cell = [], None
            self.rows.append(self._row)
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []
            self._row.append(self._cell)
        elif tag == "br" and self._cell is not None:
            self._cell.append("\n")

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self._cell = None
        elif tag == "tr":
            self._row = self._cell = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def _split_plain(s: str) -> list[Notam]:
    s = "\n".join(line for line in _clean(s).split("\n") if not line.lstrip().startswith("#"))
    starts = [m.start() for m in _HDR_RX.finditer(s)]
    if not starts:  # NOTAM-uri fără antet: le despărțim după linia Q
        starts = [m.start() for m in re.finditer(r"(?<![A-Z0-9(])Q\)\s*[A-Z0-9]{3,4}\s*/", s)]
    out = []
    for a, b in zip(starts, starts[1:] + [len(s)]):
        n = parse_icao_notam(s[a:b])
        if n is not None:
            out.append(n)
    return out


def parse_notam_text(text: str) -> list[Notam]:
    """Listă de NOTAM-uri ICAO lipite ca text (rândurile cu # sunt comentarii) sau un tabel HTML.

    Tabel: după selectorul ROvACC pentru lista ROMATSA (rânduri <tr>, celulele: număr, locație,
    text NOTAM cu <br>). Dacă celula de text nu are antet, numărul se ia din altă celulă."""
    if not isinstance(text, str) or not text.strip():
        return []
    if not re.search(r"<\s*t[dr]\b", text, re.I):
        return _split_plain(text)
    p = _TableParser()
    p.feed(text)
    out = []
    for row in p.rows:
        cells = ["".join(c).strip() for c in row]
        found = _split_plain("\n".join(cells))
        if len(found) == 1 and found[0].id is None:
            num = next((c.strip().upper() for c in cells if _ID_RX.fullmatch(c.strip().upper())), None)
            found[0].id = num
        out += found
    return out


# ---------------------------------------------------------------------------
# Surse structurate: ROMATSA WFS, FAA NMS
# ---------------------------------------------------------------------------

def _safe(fn, item):
    try:
        return fn(item)
    except (TypeError, ValueError, KeyError, AttributeError, IndexError):
        return None  # un element stricat nu oprește restul


def _serie_id(serie) -> str | None:
    m = re.fullmatch(r"\s*([A-Z])\s?(\d{1,4})/(\d{2}|\d{4})\s*", str(serie or "").upper())
    return _fmt_id(m.group(1), m.group(2), m.group(3)[-2:]) if m else None


def _time_any(v) -> dt.datetime | None:
    """ROMATSA: dfrom/dto vin ca ISO8601 sau ca AAMMZZHHMM (abpaul/romatsa-uav-zones)."""
    if not isinstance(v, str) or not v.strip():
        return None
    v = v.strip()
    return _ymdhm(v) if re.fullmatch(r"\d{10}", v) else parse_iso(v)


def _rings(geom) -> list[list[tuple[float, float]]]:
    """Inelele exterioare (lat, lon) dintr-o geometrie GeoJSON [lon, lat]."""
    if not isinstance(geom, dict):
        return []
    t, c = geom.get("type"), geom.get("coordinates")
    if t == "GeometryCollection":
        return [r for g in geom.get("geometries") or [] for r in _rings(g)]
    polys = [c] if t == "Polygon" else c if t == "MultiPolygon" else []
    out = []
    for poly in polys or []:
        try:
            ring = [(float(p[1]), float(p[0])) for p in poly[0]]
        except (TypeError, ValueError, IndexError, KeyError):
            continue
        ring = [p for p in ring if -90 <= p[0] <= 90 and -180 <= p[1] <= 180]
        if len(ring) >= 3:
            out.append(ring)
    return out


def _point(geom) -> tuple[float, float] | None:
    if not isinstance(geom, dict):
        return None
    if geom.get("type") == "GeometryCollection":
        for g in geom.get("geometries") or []:
            p = _point(g)
            if p:
                return p
        return None
    if geom.get("type") == "Point":
        try:
            lon, lat = float(geom["coordinates"][0]), float(geom["coordinates"][1])
        except (TypeError, ValueError, IndexError, KeyError):
            return None
        return (lat, lon) if -90 <= lat <= 90 and -180 <= lon <= 180 else None
    return None


def _romatsa_feature(f: dict) -> Notam | None:
    p = f.get("properties") or {}
    n = parse_icao_notam(p.get("mesaj")) if isinstance(p.get("mesaj"), str) else None
    if n is None:
        return None  # fără textul NOTAM nu avem cod Q, deci nici clasificare
    n.id = n.id or _serie_id(p.get("serie"))
    if n.start is None:
        n.start = _time_any(p.get("dfrom"))
    if n.end is None and not n.permanent:
        n.end = _time_any(p.get("dto"))
    n.polygons = _rings(f.get("geometry"))
    return n


def parse_romatsa_wfs(data) -> list[Notam]:
    """FeatureCollection de la GeoServer-ul ROMATSA. Feature-urile stricate se sar."""
    if not isinstance(data, dict) or data.get("type") != "FeatureCollection" or not isinstance(data.get("features"), list):
        raise ValueError("răspunsul ROMATSA nu e un FeatureCollection GeoJSON (URL sau strat greșit?)")
    return [n for n in (_safe(_romatsa_feature, f) for f in data["features"]) if n is not None]


def _nms_feature(f: dict) -> Notam | None:
    core = f["properties"]["coreNOTAMData"]
    nd = core["notam"]
    icao = next((t.get("formattedText") for t in core.get("notamTranslation") or []
                 if isinstance(t, dict) and t.get("type") == "ICAO" and isinstance(t.get("formattedText"), str)), None)
    n = parse_icao_notam(icao) if icao else None
    n = n or Notam(id=None)
    number = str(nd.get("number") or "").strip().upper()
    if re.fullmatch(r"[A-Z]\d{1,4}/\d{2}", number):
        nid = _serie_id(number)
    else:  # numerotare FAA internă („6/1966”, locația „FDC”)
        nid = f"{str(nd.get('location') or '').strip().upper()} {number}".strip() if number else None
    n.id = n.id or nid
    if not n.id:
        return None
    typ = str(nd.get("type") or "").upper()
    if typ in ("N", "R", "C"):
        n.type = typ
    n.fir = str(nd.get("affectedFir") or "").strip().upper() or n.fir
    q = str(nd.get("selectionCode") or "").strip().upper()
    if re.fullmatch(r"Q[A-Z]{4}", q):
        n.qcode = q
    for key in ("traffic", "purpose", "scope"):
        v = str(nd.get(key) or "").strip().upper()  # NMS lasă spații: „BO ”, „W ”
        if v:
            setattr(n, key, v)
    for key, attr in (("minimumFl", "lower_fl"), ("maximumFl", "upper_fl")):
        v = str(nd.get(key) or "").strip()
        if v.isdigit():
            setattr(n, attr, int(v))
    loc = str(nd.get("icaoLocation") or nd.get("location") or "").strip().upper()
    if loc and not n.locations:
        n.locations = [loc]
    n.start = parse_iso(nd.get("effectiveStart")) or n.start
    end = str(nd.get("effectiveEnd") or "").strip()
    if end.upper() == "PERM":
        n.permanent, n.end = True, None
    elif end:
        n.end = parse_iso(end) or n.end
    if str(nd.get("estimated") or "").lower() == "true":
        n.estimated = True
    n.schedule = scrub_text(str(nd.get("schedule") or "").strip()) or n.schedule
    if isinstance(nd.get("text"), str) and nd["text"].strip() and not n.text:
        n.text = _tidy(_clean(nd["text"]))
    n.lower = str(nd.get("lowerLimit") or "").strip().upper() or n.lower
    n.upper = str(nd.get("upperLimit") or "").strip().upper() or n.upper
    if n.lat is None:  # punctul GeoJSON e mai precis decât „coordinates” (rotunjit la minut)
        c = _point(f.get("geometry"))
        if c is None:
            m = _QCOORD_RX.fullmatch(str(nd.get("coordinates") or "").replace(" ", ""))
            c = _coord(*m.groups()[:6]) if m else None
        if c:
            n.lat, n.lon = c
    r = str(nd.get("radius") or "").strip()
    if n.radius_nm is None and re.fullmatch(r"\d+(?:\.\d+)?", r):
        n.radius_nm = int(round(float(r)))
    n.issued = parse_iso(nd.get("issued"))
    n.cancelled_at = parse_iso(nd.get("cancelationDate"))
    n.polygons = _rings(f.get("geometry"))
    if n.ref is None and n.type in ("R", "C"):
        m = re.search(r"NOTAM[RC]\s+([A-Z]?\s?\d{1,4}/\d{2,4})", n.text)
        if m:
            n.ref = _serie_id(m.group(1)) or m.group(1).replace(" ", "")
    return n


def parse_nms(data) -> list[Notam]:
    """FAA NMS: {"status": "Success", "data": {"geojson": [Feature…]}} sau direct lista de Feature.

    Câmpurile din properties.coreNOTAMData.notam: number, type, issued, affectedFir, selectionCode,
    traffic, purpose, scope, minimumFl, maximumFl, icaoLocation, effectiveStart, effectiveEnd
    (poate fi „PERM”), estimated, schedule, text (doar E), lowerLimit, upperLimit, coordinates,
    radius, cancelationDate (koala73/worldmonitor tests/fixtures/nms-notam-geojson.json)."""
    return [n for n in (_safe(_nms_feature, f) for f in _nms_features(data)) if n is not None]


def _nms_features(data) -> list:
    """Lista de Feature dintr-un răspuns NMS (ValueError dacă lipsește sau statusul nu e Success)."""
    feats = data
    if isinstance(data, dict):
        if "status" in data and data.get("status") != "Success":
            raise ValueError(f"FAA NMS: răspuns fără date (status {str(data.get('status'))[:40]!r})")
        if "data" in data:
            inner = data.get("data")
            feats = inner.get("geojson") if isinstance(inner, dict) else None
        else:
            feats = data.get("items")
    if not isinstance(feats, list):
        raise ValueError("FAA NMS: lipsește lista data.geojson")
    return feats


# ---------------------------------------------------------------------------
# Clasificare
# ---------------------------------------------------------------------------

def is_uas(n: Notam) -> bool:
    """NOTAM legat de drone/UAS: cod Q „WU” sau cuvinte-cheie în E)."""
    return n.subject in UAS_SUBJECTS or bool(UAS_RX.search(n.text or ""))


def classify(n: Notam) -> str | None:
    """Categoria NOTAM-ului sau None dacă nu e relevant (iluminat, obstacole, mijloace de
    navigație, proceduri, suprafețe de mișcare etc.). Ordinea contează: întâi codul Q, apoi textul."""
    subj, cond, text = n.subject, n.condition, n.text or ""
    uas_txt = bool(UAS_RX.search(text))
    if subj in AIRSPACE_SUBJECTS | RESTRICTION_SUBJECTS and cond in END_CONDITIONS:
        return "restrictie_ridicata"
    if subj == "FA":
        # „AH” = program de funcționare schimbat: „AD CLSD OUTSIDE THESE HR” e rutină, nu închidere
        if cond in AD_CLOSED_CONDITIONS or (cond != "AH" and AD_CLOSED_RX.search(text)):
            return "aeroport_inchis"
        return "drone_uas" if uas_txt else None
    if subj in ROUTE_SUBJECTS:
        return "ruta_inchisa" if cond in ("LC", "AU") or re.search(r"\b(?:CLSD|CLOSED)\b", text) else None
    if subj in AIRSPACE_SUBJECTS:
        if cond in ("LC", "LP") or AIRSPACE_CLOSED_RX.search(text):
            return "spatiu_aerian_inchis"
        # „LT” limitat la (ex. FIR limitat la zboruri de stat/urgență), „LI” închis IFR
        if cond in ("LT", "LI") or RESTRICTION_RX.search(text):
            return "restrictie_spatiu_aerian"
        return "drone_uas" if uas_txt else None
    if subj in UAS_SUBJECTS:
        return "drone_uas"
    if subj in RESTRICTION_SUBJECTS or subj in FIRING_SUBJECTS:
        return "spatiu_aerian_inchis" if AIRSPACE_CLOSED_RX.search(text) else "restrictie_spatiu_aerian"
    if subj in GNSS_SUBJECTS:
        return "gnss" if cond in GNSS_BAD_CONDITIONS or GNSS_ANY_RX.search(text) else None
    if GNSS_RX.search(text):  # alt subiect (ex. procedură, mijloc de navigație): doar interferențe/pană GNSS
        return "gnss"
    if uas_txt:
        return "drone_uas"
    if subj is None or subj in ("XX", "WX"):  # cod necunoscut / „alte avertizări”: după text
        if AIRSPACE_CLOSED_RX.search(text):
            return "spatiu_aerian_inchis"
        if AD_CLOSED_RX.search(text):
            return "aeroport_inchis"
        if RESTRICTION_RX.search(text):
            return "restrictie_spatiu_aerian"
    return None


# ---------------------------------------------------------------------------
# Distanțe (Iași, linia Prutului) – aceeași proiecție locală ca geo._seg_dist_km
# ---------------------------------------------------------------------------

_KX = math.cos(math.radians(46.5)) * 111.32
_KY = 110.57


def _xy(p):
    return p[1] * _KX, p[0] * _KY


def _edges(ring):
    pts = list(ring)
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts = pts[:-1]
    return [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]


def _in_ring(lat: float, lon: float, ring) -> bool:
    inside = False
    for (y1, x1), (y2, x2) in _edges(ring):
        if (y1 > lat) != (y2 > lat) and lon < x1 + (lat - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def _cross(a, b, c, d) -> bool:
    (ax, ay), (bx, by), (cx, cy), (dx_, dy_) = _xy(a), _xy(b), _xy(c), _xy(d)

    def orient(px, py, qx, qy, rx, ry):
        return (qx - px) * (ry - py) - (qy - py) * (rx - px)

    o1, o2 = orient(ax, ay, bx, by, cx, cy), orient(ax, ay, bx, by, dx_, dy_)
    o3, o4 = orient(cx, cy, dx_, dy_, ax, ay), orient(cx, cy, dx_, dy_, bx, by)
    return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)


def _point_line_km(lat, lon, line) -> float:
    return min(geo._seg_dist_km(lat, lon, line[i], line[i + 1]) for i in range(len(line) - 1))


def _point_ring_km(lat, lon, ring) -> float:
    if _in_ring(lat, lon, ring):
        return 0.0
    return min(geo._seg_dist_km(lat, lon, a, b) for a, b in _edges(ring))


def _ring_line_km(ring, line) -> float:
    """Distanța minimă poligon–linie frântă; 0 dacă linia intră în poligon sau îl traversează."""
    if any(_in_ring(p[0], p[1], ring) for p in line):
        return 0.0
    edges = _edges(ring)
    segs = list(zip(line, line[1:]))
    if any(_cross(a, b, c, d) for a, b in edges for c, d in segs):
        return 0.0
    return min(min(_point_line_km(p[0], p[1], line) for p in ring),
               min(geo._seg_dist_km(p[0], p[1], a, b) for p in line for a, b in edges))


def text_coords(text: str) -> list[tuple[float, float]]:
    """Coordonatele „453410N0280827E” (și „540733.1N 0094659.5W”) din E), în ordine."""
    out = []
    for m in _TEXT_COORD_RX.finditer(text or ""):
        dd, mm, ss, h1, ddd, mm2, ss2, h2 = m.groups()
        if int(mm) >= 60 or int(mm2) >= 60 or float(ss) >= 60 or float(ss2) >= 60:
            continue
        lat = int(dd) + int(mm) / 60 + float(ss) / 3600
        lon = int(ddd) + int(mm2) / 60 + float(ss2) / 3600
        lat, lon = (-lat if h1 == "S" else lat), (-lon if h2 == "W" else lon)
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            out.append((lat, lon))
    return out


# FIR-uri care se învecinează pe Prut (granița RO–MD) → un NOTAM pe tot FIR-ul atinge Prutul
FIR_COUNTRY = {"LRBB": "RO", "LUUU": "MD"}
# Un cerc Q mai mare de atât nu localizează nimic la scara „aproape” (60 km): distanța lui e doar o
# limită inferioară (cercul ICAO cuprinde toată zona), deci un astfel de NOTAM nu e marcat „near”.
# Euristică; NOTAM-urile LUUU pe tot FIR-ul au aria „fir”, nu „circle”.
COARSE_CIRCLE_NM = 100


def _geometry(n: Notam) -> tuple[str | None, list]:
    """(tipul ariei, inele): „polygon” (geometria sursei), „text” (≥ 3 coordonate din E)),
    „fir” (tot FIR-ul, doar LRBB/LUUU), „circle” (cercul din linia Q) sau None (fără reper)."""
    if n.polygons:
        return "polygon", n.polygons
    pts = text_coords(n.text)
    if len(pts) >= 3:
        return "text", [pts]
    if n.fir_wide or (n.lat is None and n.fir and n.fir in n.locations):
        return ("fir" if (n.fir or "") in FIR_COUNTRY else None), []
    if n.lat is None or n.lon is None:
        return None, []
    return "circle", []


def area_kind(n: Notam) -> str | None:
    """Cât de precisă e aria: „polygon”, „text”, „fir”, „circle” sau None (vezi distances())."""
    return _geometry(n)[0]


def distances(n: Notam, target: geo.Place = geo.IASI) -> tuple[float | None, float | None]:
    """(km până la țintă, km până la linia Prutului) pentru zona NOTAM-ului; 0 = în zonă.

    Ordinea preciziei: poligonul sursei → poligonul din coordonatele din E) (≥ 3 puncte) →
    cercul din linia Q (centru − rază). Rază 999 = tot FIR-ul: cunoscut doar pentru LRBB/LUUU.
    Fără niciun reper: (None, None)."""
    kind, rings = _geometry(n)
    if rings:
        d_t = min(_point_ring_km(target.lat, target.lon, r) for r in rings)
        d_p = min(_ring_line_km(r, geo.PRUT_LINE) for r in rings)
        return round(d_t, 1), round(d_p, 1)
    if kind == "fir":
        country = FIR_COUNTRY[n.fir]
        d_t = 0.0 if country == target.country else _point_line_km(target.lat, target.lon, geo.PRUT_LINE)
        return round(d_t, 1), 0.0
    if kind is None:
        return None, None
    r_km = (n.radius_nm or 0) * 1.852
    d_t = max(0.0, geo.haversine_km(n.lat, n.lon, target.lat, target.lon) - r_km)
    d_p = max(0.0, _point_line_km(n.lat, n.lon, geo.PRUT_LINE) - r_km)
    return round(d_t, 1), round(d_p, 1)


def is_near(d_target: float | None, d_prut: float | None, near_km: float = 60, near_prut_km: float = 15,
            near_prut_max_km: float = 120) -> bool:
    """Aproape: la ≤ near_km de Iași, sau la ≤ near_prut_km de Prut dar nu mai departe de
    near_prut_max_km de Iași (Prutul are ~400 km; capătul de la Galați nu e „aproape”)."""
    if d_target is not None and d_target <= near_km:
        return True
    return (d_prut is not None and d_prut <= near_prut_km
            and (d_target is None or d_target <= near_prut_max_km))


# ---------------------------------------------------------------------------
# Text pentru mesaje
# ---------------------------------------------------------------------------

# (?<![\w.+-]): începe doar la marginea unui cuvânt (altfel, timp pătratic pe un șir lung fără „@”)
_EMAIL_RX = re.compile(r"(?<![\w.+-])[\w.+-]+(?:@|\s?\(AT\)\s?)[\w-]+(?:\.[\w-]+)+", re.I)
_PHONE_RX = re.compile(r"\+\d[\d\s()./-]{6,}\d|\b(?:TEL|PHONE|PH|FAX|MOB(?:ILE)?|GSM)\b\.?:?\s*\+?\d[\d\s()./-]{5,}\d"
                       r"|\bCTC\b\.?:?\s*\+?\d(?:[\s()./-]{0,2}\d){8,}"   # „CTC 0232 271 590” (≥ 9 cifre, nu „CTC 0600-1800”)
                       r"|\b\d{3}[-.]\d{3}[-.]\d{4}\b|\b00\d{9,13}\b|\b0\d{8,11}\b", re.I)

# Identități de aeronave (politica: nimic despre aeronave individuale în mesaje sau în arhivă).
# Înmatriculări cu prefix de naționalitate din listă (nu un prefix generic: „U-TURN”, „AD-HOC”, „EN-ROUTE”).
_REG_PREFIXES = ("YR", "ER", "UR", "SP", "HA", "LZ", "OM", "OK", "OE", "YU", "LY", "YL", "ES", "EW", "RA", "TC",
                 "SX", "4L", "4K", "4X", "4O", "9A", "9H", "S5", "Z3", "E7", "ZA", "5B", "EK", "HB", "PH", "OO", "OY",
                 "LN", "SE", "OH", "EC", "CS", "EI", "LX", "D", "G", "F", "I")
_REG_RX = re.compile(r"(?<![A-Z0-9/-])(?!D-ATIS\b|D-VOLMET\b)(?:" + "|".join(_REG_PREFIXES)
                     + r")-(?:[A-Z]{3,4}|\d{3,5}[A-Z]{0,2})(?![A-Z0-9/-])", re.I)
# „CS” = call sign în abrevierile ICAO; cuvintele uzuale de după („CALL SIGNS AND FREQ”) rămân
_CALLSIGN_RX = re.compile(r"\b(CALL\s?SIGNS?|C/S|CS)(\s*[:.]?\s*)(?!(?:AND|OR|OF|ARE|IS|WILL|TO|FOR|THE|WITH|IN|ON)\b)"
                          r"[A-Z0-9]{2,8}\b", re.I)
_HEX_RX = re.compile(r"\b(ICAO\s+(?:24[\s-]?BIT\s+)?(?:ADDRESS|ADDR|CODE)|MODE[\s-]?S\s+(?:ADDRESS|ADDR|CODE)|HEX(?:\s+CODE)?)"
                     r"(\s*[:.]?\s*)[0-9A-F]{6}\b", re.I)


def scrub_contacts(s: str) -> str:
    """Scoate adresele de e-mail și numerele de telefon din textul unui NOTAM."""
    return _PHONE_RX.sub("[tel]", _EMAIL_RX.sub("[email]", s or ""))


def scrub_identities(s: str) -> str:
    """Scoate identitățile de aeronave din textul unui NOTAM: înmatriculări (YR-ABC, ER-AXV, D-EABC),
    indicative („CALLSIGN ROT123”) și adrese ICAO de 24 de biți („ICAO ADDRESS 4A1234”)."""
    s = _HEX_RX.sub(lambda m: f"{m.group(1)}{m.group(2)}[aeronavă]", s or "")
    s = _CALLSIGN_RX.sub(lambda m: f"{m.group(1)}{m.group(2)}[aeronavă]", s)
    return _REG_RX.sub("[aeronavă]", s)


def scrub_text(s: str) -> str:
    """Textul E) pentru mesaje și arhivă: fără contacte și fără identități de aeronave."""
    return scrub_contacts(scrub_identities(s))


def _local(t: dt.datetime) -> str:
    loc = to_local(t)
    zone = "EEST" if loc.utcoffset() == dt.timedelta(hours=3) else "EET"
    return f"{loc:%d.%m %H:%M} {zone}"


def validity_ro(n: Notam) -> str:
    start = _local(n.start) if n.start else "?"
    if n.permanent:
        end = "permanent"
    elif n.end:
        end = _local(n.end) + (" (estimat)" if n.estimated else "")
    else:
        end = "nedefinit"
    sched = f", program {n.schedule}" if n.schedule else ""
    return f"{start} – {end}{sched}"


_COORD_RUN_RX = re.compile(r"(?:\d{6}(?:\.\d+)?\s?[NS][\s-]{0,3}\d{7}(?:\.\d+)?\s?[EW][\s-]*)+")


def excerpt(text: str, n: int = 200) -> str:
    """Primele ~n caractere din E), fără contacte și identități de aeronave; șirurile de
    coordonate devin „[coord.]”."""
    t = scrub_text(" ".join((text or "").split()))
    t = _COORD_RUN_RX.sub("[coord.] ", t).replace(" [coord.] [coord.]", " [coord.]").strip()
    return t if len(t) <= n else t[: n - 1] + "…"


def summary(n: Notam, kind: str, category: str, d_target: float | None, d_prut: float | None,
            ends: str | None = None) -> str:
    """Rezumatul scurt din Signal.text (română): ce, unde, când, limite, extras din E)."""
    head = {"nou": "", "inlocuire": f" (înlocuiește {n.ref or '?'})", "anulare": f" (anulează {ends or n.ref or '?'})",
            "retras": " (retras înainte de expirare)"}[kind]
    what = CATEGORY_RO.get(category, category)
    if n.qcode:
        what += f" ({n.qcode})"
    if category != "drone_uas" and is_uas(n):
        what += ", menționează drone/UAS"
    where = ", ".join(n.locations or ([n.fir] if n.fir else [])) or "?"
    dists = []
    if d_target is not None:
        dists.append(f"~{d_target:.0f} km de Iași")
    if d_prut is not None:
        dists.append(f"{d_prut:.0f} km de Prut")
    if dists:
        where += " · " + ", ".join(dists)
    parts = [f"NOTAM {n.id}{head}", what, where, validity_ro(n)]
    if n.lower or n.upper:
        parts.append(f"{n.lower or '?'}–{n.upper or '?'}")
    if n.text:
        parts.append(f"«{excerpt(n.text)}»")
    return " · ".join(parts)


def content_hash(n: Notam) -> str:
    """Amprenta conținutului (E, cod Q, limite, program, geometrie rotunjită): aceeași pentru
    reemiterea lunară a unei zone sub alt număr (ex. P2580/26 → luna următoare)."""
    geom = n.polygons[0] if n.polygons else ([(n.lat, n.lon)] if n.lat is not None else [])
    pts = ";".join(f"{a:.2f},{b:.2f}" for a, b in geom[:400])
    base = "|".join([n.qcode or "", " ".join((n.text or "").split()), n.lower or "", n.upper or "", n.schedule or "", pts])
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]


def notam_meta(n: Notam, kind: str, category: str, d_target: float | None, d_prut: float | None, near: bool) -> dict:
    """Meta JSON pentru Signal (fără identități de aeronave; datele în ISO UTC sau null).

    „id” e numărul afișat („A0123/25”); „key” e cheia unică („LU:A0123/25”, vezi notam_key)."""
    return {
        "id": n.id, "key": notam_key(n), "kind": kind, "replaces": n.ref, "fir": n.fir, "qcode": n.qcode,
        "category": category,
        "uas": is_uas(n),
        "lat": round(n.lat, 4) if n.lat is not None else None,
        "lon": round(n.lon, 4) if n.lon is not None else None,
        "radius_nm": n.radius_nm, "fir_wide": n.fir_wide,
        "lower_fl": n.lower_fl, "upper_fl": n.upper_fl, "lower": n.lower, "upper": n.upper,
        "start": iso(n.start), "end": iso(n.end), "estimated": n.estimated, "permanent": n.permanent,
        "schedule": n.schedule, "locations": list(n.locations), "issued": iso(n.issued),
        # tăiat la 4000 înainte de curățare (limitează timpul), apoi la 2000: un contact care trece de
        # 2000 e oricum întreg în fereastra de 4000, deci nu rămâne pe jumătate
        "text": scrub_text((n.text or "")[:4000])[:2000], "text_hash": content_hash(n),
        "dist_iasi_km": d_target, "dist_prut_km": d_prut, "near": near, "area": area_kind(n),
    }


# ---------------------------------------------------------------------------
# HTTP cu context TLS propriu (http.request nu primește context)
# ---------------------------------------------------------------------------

def make_tls_context(ciphers: str = TLS_CIPHERS) -> ssl.SSLContext:
    """Context TLS cu verificarea certificatului și a numelui PĂSTRATE; doar cifrurile se schimbă."""
    ctx = ssl.create_default_context()
    if ciphers:
        try:
            ctx.set_ciphers(ciphers)
        except ssl.SSLError:
            pass  # unele build-uri OpenSSL nu acceptă șirul: rămân cifrurile implicite
    return ctx


def request_with_context(url: str, context: ssl.SSLContext | None, *, method: str = "GET", headers: dict | None = None,
                         data: bytes | None = None, timeout: float = 15, user_agent: str = http.DEFAULT_UA,
                         max_bytes: int = 5_000_000) -> http.Response:
    """Ca http.request, dar cu un context TLS dat (opener separat, fără install_opener)."""
    h = {"User-Agent": user_agent, "Accept-Encoding": "gzip"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=context))
    deadline = time.monotonic() + 2 * timeout
    try:
        with opener.open(req, timeout=timeout) as r:
            chunks, size = [], 0
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise http.HttpError(0, f"timp total depășit ({2 * timeout:.0f} s)")
                sock = getattr(getattr(getattr(r, "fp", None), "raw", None), "_sock", None)
                if sock is not None:  # ca în http.request: o citire nu poate depăși termenul total
                    sock.settimeout(max(0.1, min(timeout, remaining)))
                try:
                    chunk = r.read1(65536)
                except (TimeoutError, OSError) as e:
                    raise http.HttpError(0, f"citire întreruptă ({type(e).__name__})") from None
                if not chunk:
                    break
                chunks.append(chunk)
                size += len(chunk)
                if size > max_bytes:
                    raise http.HttpError(0, f"raspuns prea mare (> {max_bytes} B)")
            body = b"".join(chunks)
            hdrs = {k.lower(): v for k, v in r.headers.items()}
            status = r.status
    except urllib.error.HTTPError as e:
        hdrs = {k.lower(): v for k, v in (e.headers or {}).items()}
        try:
            ra = float(hdrs["retry-after"]) if hdrs.get("retry-after") else None
        except ValueError:
            ra = None
        try:
            detail = e.read(300).decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            detail = ""
        raise http.HttpError(e.code, detail, ra) from None
    if hdrs.get("content-encoding") == "gzip":
        body = http._gunzip_limited(body, max_bytes)
    return http.Response(status, hdrs, body)


def _tls_handshake_failed(e: BaseException) -> bool:
    """Negocierea TLS a eșuat din alt motiv decât certificatul (care nu se relaxează niciodată).

    Cu primul context („DEFAULT:!DH”) nu se oferă DHE, deci DH_KEY_TOO_SMALL nu poate apărea: dacă
    serverul are doar suite DHE, eroarea e „handshake failure” / „no shared cipher”. Orice astfel de
    SSLError (direct sau în URLError.reason) declanșează contextul de rezervă."""
    err = e.reason if isinstance(e, urllib.error.URLError) else e
    if isinstance(err, ssl.SSLCertVerificationError):
        return False
    return isinstance(err, ssl.SSLError) or "DH_KEY_TOO_SMALL" in str(err)


def _json_body(r: http.Response, what: str):
    body = r.body.lstrip()
    if body[:1] == b"<":
        txt = body[:4000].decode("utf-8", "replace")
        if "ServiceException" in txt:
            m = re.search(r"<ServiceException\b[^>]*>(.*?)</ServiceException>", txt, re.S)  # nu …Report
            msg = " ".join(html.unescape(m.group(1)).split())[:200] if m else "?"
            raise ValueError(f"{what}: eroare WFS de la GeoServer: {msg}")
        raise ValueError(f"{what}: a venit HTML/XML în loc de JSON (mentenanță, blocare sau URL greșit)")
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise ValueError(f"{what}: răspunsul nu e JSON valid") from None


# ---------------------------------------------------------------------------
# Colectorul
# ---------------------------------------------------------------------------

class NotamCollector(Collector):
    """NOTAM-uri relevante pentru Iași / Prut, ca semnale cu rolul „notam”.

    Întoarce, la fiecare citire, toate NOTAM-urile active (sau viitoare) clasificate și aflate
    în zona urmărită; ext_id = „<cheie>|<tip>” (ex. „LU:A0123/25|nou”, vezi notam_key) fără oră,
    deci arhiva le deduplică și motorul vede fiecare NOTAM o singură dată. Cheia are prefixul
    țării: același număr poate exista la două birouri NOTAM (LRBB și LUUU). Tipuri: nou, inlocuire (NOTAMR), anulare (NOTAMC sau
    cancelationDate), retras (a dispărut din sursă înainte de C)). Starea (ce s-a văzut) e doar
    în memorie; nu conține nimic despre aeronave."""

    SOURCES = ("romatsa_wfs", "faa_nms", "text")
    MIN_INTERVAL = {"romatsa_wfs": 300, "faa_nms": 180, "text": 60}  # FAA: o interogare la 3 min

    def __init__(self, name: str = "romatsa", source: str = "romatsa_wfs", urls: list[str] | str | None = None, *,
                 watch_firs=("LUUU",), locations=("LRIA", "LRSV", "LRBC", "LUKK", "LUBL"),
                 max_dist_km: float = 200, max_prut_km: float = 60, near_km: float = 60, near_prut_km: float = 15,
                 near_prut_max_km: float = 120,
                 categories=None, client_id: str = "", client_secret: str = "", nms_host: str = NMS_HOST,
                 nms_center: tuple[float, float] = (47.05, 28.2), nms_radius_nm: float = 100,
                 tls_ciphers: str = TLS_CIPHERS, tls_hosts=(ROMATSA_HOST,), max_bytes: int = 8_000_000, **kw):
        if source not in self.SOURCES:
            raise ValueError(f"sursă NOTAM necunoscută „{source}” (permise: {', '.join(self.SOURCES)})")
        interval = max(float(kw.pop("interval", 900)), self.MIN_INTERVAL[source])
        super().__init__(f"notam:{name}", "notam", interval, **kw)
        self.source = source
        self.urls = [urls] if isinstance(urls, str) else list(urls or [])
        if source == "romatsa_wfs" and not self.urls:
            self.urls = [ROMATSA_WFS_URL]
        if source == "text" and not self.urls:
            raise ValueError("sursa NOTAM „text” are nevoie de cel puțin un URL")
        if source == "faa_nms" and not (client_id and client_secret):
            raise NotamCredentialsError(NMS_HOWTO)
        bad = set(categories or ()) - set(CATEGORIES)
        if bad:
            raise ValueError(f"categorii NOTAM necunoscute: {sorted(bad)} (permise: {', '.join(CATEGORIES)})")
        self.watch_firs = {str(x).upper() for x in watch_firs or ()}
        self.locations = {str(x).upper() for x in locations or ()}
        self.max_dist_km, self.max_prut_km = float(max_dist_km), float(max_prut_km)
        self.near_km, self.near_prut_km, self.near_prut_max_km = float(near_km), float(near_prut_km), float(near_prut_max_km)
        self.categories = set(categories or ())
        self.client_id, self.client_secret = client_id, client_secret
        self.nms_host = nms_host.rstrip("/")
        self.nms_center, self.nms_radius_nm = nms_center, nms_radius_nm
        self.tls_ciphers = tls_ciphers
        self.tls_hosts = {h.lower() for h in tls_hosts or ()}
        self.max_bytes = max_bytes
        self.last_raw = 0       # câte înregistrări avea sursa (înainte de filtre) – pentru check-sources
        self.last_skipped = 0   # câte nu s-au putut citi
        self._active: dict[str, dict] = {}
        self._prev_total = 0
        self._hash_ids: dict[str, dict[str, list]] = {}  # amprentă → {id: [prima, ultima apariție]}
        self._token: str | None = None
        self._token_exp = 0.0
        self._tls_ctx: ssl.SSLContext | None = None
        self._tls_relaxed = False

    # ------------------------------------------------------------------ rețea
    def _fetch(self, url: str, headers: dict | None = None, *, method: str = "GET", data: bytes | None = None) -> http.Response:
        host = (urllib.parse.urlsplit(url).hostname or "").lower()
        if url.lower().startswith("https:") and self.tls_ciphers and host in self.tls_hosts:
            r = self._fetch_tls(url, headers, method, data)
        else:
            r = http.request(url, method=method, headers=headers, data=data, timeout=self.timeout,
                             user_agent=self.user_agent, max_bytes=self.max_bytes)
        self.last_date = r.headers.get("date")  # pentru verificarea ceasului (app._check_clock)
        return r

    def _fetch_tls(self, url, headers, method, data) -> http.Response:
        kw = {"method": method, "headers": headers, "data": data, "timeout": self.timeout,
              "user_agent": self.user_agent, "max_bytes": self.max_bytes}
        if self._tls_ctx is None:
            self._tls_ctx = make_tls_context(self.tls_ciphers)
        try:
            return request_with_context(url, self._tls_ctx, **kw)
        except (urllib.error.URLError, ssl.SSLError) as e:
            if self._tls_relaxed or not _tls_handshake_failed(e):
                raise
        # O singură dată pe proces: „DEFAULT:@SECLEVEL=1” (ca Straznik). Certificatul și numele se verifică
        # în continuare. Și o eroare TLS trecătoare (ex. SSLEOFError) duce aici – acceptabil, tot verificat.
        self._tls_ctx, self._tls_relaxed = make_tls_context(TLS_CIPHERS_FALLBACK), True
        return request_with_context(url, self._tls_ctx, **kw)

    def _nms_token(self) -> str:
        if self._token and time.monotonic() < self._token_exp:
            return self._token
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("ascii")
        try:
            r = self._fetch(f"{self.nms_host}/v1/auth/token",
                            {"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded",
                             "Accept": "application/json"},
                            method="POST", data=b"grant_type=client_credentials")
        except http.HttpError as e:
            if e.status in (401, 403):
                raise NotamCredentialsError(
                    f"FAA NMS a respins credențialele (HTTP {e.status}): verificați FAA_NMS_CLIENT_ID / "
                    f"FAA_NMS_CLIENT_SECRET și mediul (producție api-nms.aim.faa.gov vs. staging).") from None
            raise
        body = _json_body(r, "FAA NMS (token)")
        tok = body.get("access_token") if isinstance(body, dict) else None
        if not isinstance(tok, str) or not tok:
            raise ValueError("FAA NMS: răspunsul la cererea de token nu conține access_token")
        try:
            ttl = float(body.get("expires_in") or 1799)  # „1799” (șir) = 30 min
        except (TypeError, ValueError):
            ttl = 1799.0
        self._token, self._token_exp = tok, time.monotonic() + max(60.0, ttl - 60)
        return tok

    def _read(self) -> tuple[list[Notam], int]:
        """(NOTAM-uri citite, câte înregistrări avea sursa)."""
        out: list[Notam] = []
        total = 0
        if self.source == "romatsa_wfs":
            for url in self.urls:
                data = _json_body(self._fetch(url, {"Accept": "application/json"}), "ROMATSA WFS")
                ns = parse_romatsa_wfs(data)
                total += len(data["features"])
                out += ns
        elif self.source == "faa_nms":
            tok = self._nms_token()
            lat, lon = self.nms_center
            q = urllib.parse.urlencode({"latitude": f"{lat:.4f}", "longitude": f"{lon:.4f}",
                                        "radius": int(self.nms_radius_nm)})
            try:
                r = self._fetch(f"{self.nms_host}/nmsapi/v1/notams?{q}",
                                {"Authorization": f"Bearer {tok}", "nmsResponseFormat": "GEOJSON",
                                 "Accept": "application/json"})
            except http.HttpError as e:
                if e.status == 401:
                    self._token = None  # token expirat mai devreme: data viitoare se cere altul
                raise
            data = _json_body(r, "FAA NMS")
            out = parse_nms(data)
            total = len(_nms_features(data))
        else:
            for url in self.urls:
                ns = parse_notam_text(self._fetch(url, {"Accept": "text/plain, text/html;q=0.9, */*;q=0.5"}).text())
                total += len(ns)
                out += ns
        uniq: dict[str, Notam] = {}
        for n in out:  # aceeași zonă poate apărea în două straturi: păstrăm varianta cu geometrie
            if not n.id:
                continue
            k = notam_key(n)  # cu prefixul țării: „A0123/25” al LRBB ≠ „A0123/25” al LUUU
            if k not in uniq or (n.polygons and not uniq[k].polygons):
                uniq[k] = n
        self.last_raw, self.last_skipped = total, max(0, total - len(out))
        return list(uniq.values()), total

    # ------------------------------------------------------------------ filtre
    def _in_area(self, n: Notam, d_t, d_p) -> bool:
        return ((n.fir or "") in self.watch_firs or any(loc in self.locations for loc in n.locations)
                or (d_t is not None and d_t <= self.max_dist_km) or (d_p is not None and d_p <= self.max_prut_km))

    def _near(self, n: Notam, d_t, d_p) -> bool:
        if area_kind(n) == "circle" and (n.radius_nm or 0) > COARSE_CIRCLE_NM:
            return False  # cerc Q prea mare: distanța e doar o limită inferioară
        return is_near(d_t, d_p, self.near_km, self.near_prut_km, self.near_prut_max_km)

    def _signal(self, n: Notam, kind: str, cat: str, d_t, d_p, now: dt.datetime, ends=None, ends_key=None,
                cont=None) -> Signal:
        meta = notam_meta(n, kind, cat, d_t, d_p, self._near(n, d_t, d_p))
        meta.update({"ends": ends, "ends_key": ends_key, "continua": cont, "source_type": self.source})
        pub = now if kind == "retras" else (n.issued or n.start)
        if pub is None or pub > now:
            pub = now  # NOTAM cu început în viitor: „publicat” = când l-am văzut (orele exacte sunt în meta)
        return Signal(source=self.name, role="notam", text=summary(n, kind, cat, d_t, d_p, ends),
                      received_at=now, published_at=pub, url=self.urls[0] if self.urls else self.nms_host,
                      ext_id=f"{notam_key(n)}|{kind}", meta=meta)

    def _continues(self, n: Notam, key: str, now: dt.datetime) -> str | None:
        """Numărul unui NOTAM văzut mai devreme cu același conținut (reemitere sub alt număr)."""
        seen = self._hash_ids.setdefault(content_hash(n), {})
        first = seen.setdefault(key, [now, now, n.id])[0]
        seen[key][1] = now
        earlier = [(t[0], t[2]) for k, t in seen.items() if k != key and t[0] < first]
        return max(earlier)[1] if earlier else None

    def process(self, notams: list[Notam], total: int, now: dt.datetime) -> list[Signal]:
        """Filtrează și transformă NOTAM-urile citite în semnale (separat de rețea, pentru teste)."""
        out: list[Signal] = []
        current: dict[str, dict] = {}
        ended: set[str] = set()
        for n in notams:
            if not n.id:
                continue  # fără număr nu are cheie (nici deduplicare, nici anulare)
            key = notam_key(n)
            cancelled = n.type == "C" or (n.cancelled_at is not None and n.cancelled_at <= now)
            if not cancelled and n.end is not None and n.end <= now:
                continue  # expirat
            cat = classify(n)
            d_t, d_p = distances(n)
            if cancelled:
                target_id = n.ref if n.type == "C" else n.id
                target = notam_key(n, target_id) if target_id else None
                tracked = self._active.get(target) if target else None
                if tracked:
                    cat = tracked["cat"]
                    if d_t is None and d_p is None:
                        d_t, d_p = tracked["d_t"], tracked["d_p"]
                if cat is None or not (tracked or self._in_area(n, d_t, d_p)):
                    continue
                if not tracked and self.categories and cat not in self.categories:
                    continue
                if target:
                    ended.add(target)
                out.append(self._signal(n, "anulare", cat, d_t, d_p, now, ends=target_id, ends_key=target))
                continue
            if cat is None or (self.categories and cat not in self.categories) or not self._in_area(n, d_t, d_p):
                continue
            replaced = notam_key(n, n.ref) if n.type == "R" and n.ref else None
            if replaced:
                ended.add(replaced)
            current[key] = {"n": n, "cat": cat, "d_t": d_t, "d_p": d_p}
            out.append(self._signal(n, "inlocuire" if n.type == "R" else "nou", cat, d_t, d_p, now,
                                    ends=n.ref if replaced else None, ends_key=replaced,
                                    cont=self._continues(n, key, now)))
        # dispărute înainte de C): „retras”. Un răspuns gol sau mult mai mic = pană, nu retragere.
        healthy = total > 0 and total >= 0.5 * self._prev_total
        if healthy:
            grace = now + dt.timedelta(minutes=10)
            for k, info in self._active.items():
                n = info["n"]
                if k in current or k in ended or (n.end is not None and n.end <= grace):
                    continue
                out.append(self._signal(n, "retras", info["cat"], info["d_t"], info["d_p"], now, ends=n.id, ends_key=k))
            self._active = current
        else:
            self._active.update(current)
            for k in ended:  # anulate/înlocuite într-o citire parțială: nu mai sunt urmărite (altfel „retras” fals)
                if k not in current:
                    self._active.pop(k, None)
        if total > 0:
            self._prev_total = total
        cutoff = now - dt.timedelta(days=3)
        for h in list(self._hash_ids):
            self._hash_ids[h] = {i: t for i, t in self._hash_ids[h].items() if t[1] >= cutoff}
            if not self._hash_ids[h]:
                del self._hash_ids[h]
        return out

    def poll(self, now: dt.datetime) -> list[Signal]:
        notams, total = self._read()
        return self.process(notams, total, now)
