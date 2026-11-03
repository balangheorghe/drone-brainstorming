"""Aeronave MILITARE vizibile în datele ADS-B publice – doar un rezumat, doar intern.

Ce face: din răspunsul unui agregator (adsb.lol /v2/point etc.) numără aeronavele marcate militare
(readsb dbFlags & 1) aflate în aer în zona cerută și le grupează pe categorii generale
(avion de luptă, dronă, avion radar/recunoaștere, avion-cisternă, transport, elicopter).

Ce NU face: nu păstrează și nu întoarce identități (hex, indicativ, înmatriculare, tip exact),
nu urmărește traiectorii, nu stochează nimic. Distanța e rotunjită la 10 km, direcția pe 8 puncte.

De ce doar intern: datele sunt publice, dar republicarea pozițiilor aeronavelor militare în timpul
unei operațiuni poate ajuta adversarul și poate avea consecințe legale. Avioanele de poliție aeriană
zboară des fără ADS-B: absența lor nu înseamnă nimic. Rezumatul se livrează pe canalele interne, dar nu
se păstrează: în arhivă (outbox) textul e înlocuit după livrare, iar în jurnal apare redactat.
"""

from __future__ import annotations

import re

from . import geo
from .adsb_analysis import _bearing, _num, _on_ground, _pos, _ts, compass_ro, is_military, is_private, snapshot_meta

LUPTA = "avion de luptă"
DRONA = "dronă"
RADAR = "avion radar/recunoaștere"
CISTERNA = "avion-cisternă"
TRANSPORT = "avion de transport"
ELICOPTER = "elicopter"
ALTUL = "altă aeronavă militară"

# Grupurile care declanșează un mesaj; celelalte (AWACS, cisterne, transport) sunt frecvente
# deasupra României și apar doar ca context.
TRIGGER = (LUPTA, DRONA)

# Coduri de tip ICAO (Doc 8643) sigure + cuvinte din descrierea bazei de date (câmpul `desc`).
_TYPES = {
    DRONA: {"Q4", "Q9", "MQ9", "RQ4", "TB2", "HRON"},
    LUPTA: {"F16", "F15", "F35", "F18H", "F18S", "EUFI", "RFAL", "MG29", "SU27", "SU30", "TOR", "F4"},
    RADAR: {"E3TF", "E3CF", "E6", "E737", "R135", "P8", "U2", "E2", "E8"},
    CISTERNA: {"K35R", "K35E"},
    TRANSPORT: {"C17", "C130", "C30J", "C5M", "A400", "C27J", "C295", "CN35", "C160"},
}
_DESC = [
    (DRONA, re.compile(r"GLOBAL HAWK|REAPER|PREDATOR|TRITON|BAYRAKTAR|HERON|\bMQ-?9|\bRQ-?4", re.I)),
    (LUPTA, re.compile(r"\bF-?(?:16|15|35)[A-Z]?\b|F/A-?18|HORNET|TYPHOON|EUROFIGHTER|RAFALE|GRIPEN|MIG-?29|SU-?27|SU-?30|TORNADO|FIGHTING FALCON", re.I)),
    (RADAR, re.compile(r"SENTRY|AWACS|WEDGETAIL|RIVET JOINT|RC-?135|POSEIDON|\bP-?8\b|\bE-?3\b|\bE-?7\b|ARTEMIS|SENTINEL", re.I)),
    (CISTERNA, re.compile(r"KC-?135|KC-?46|KC-?10\b|MRTT|TANKER|STRATOTANKER", re.I)),
    (TRANSPORT, re.compile(r"HERCULES|GLOBEMASTER|\bATLAS\b|SPARTAN|C-?295|C-?27|CASA|GALAXY|TRANSALL", re.I)),
    (ELICOPTER, re.compile(r"HELICOPTER|BLACK HAWK|CHINOOK|PUMA|IAR-?330|SEAHAWK|NH-?90|AW-?101|COUGAR", re.I)),
]


def group_of(ac: dict) -> str:
    t = str(ac.get("t") or "").upper().strip()
    for g, codes in _TYPES.items():
        if t in codes:
            return g
    desc = str(ac.get("desc") or "")
    for g, rx in _DESC:
        if desc and rx.search(desc):
            return g
    if str(ac.get("category") or "").upper() == "A7":
        return ELICOPTER
    return ALTUL


def summary(data: dict, area: str, center_lat: float, center_lon: float, radius_nm: float,
            max_seen_s: float = 60.0, now=None, stale_s: float = 45.0) -> dict:
    """Rezumatul aeronavelor militare în aer în zonă. Fără identități.
    Cu `now`: un instantaneu mai vechi de `stale_s` secunde e tratat ca indisponibil (ok=False)."""
    meta = snapshot_meta(data) if isinstance(data, dict) else {"ok": False}
    out = {"area": area, "radius_nm": radius_nm, "ok": bool(meta.get("ok")), "n": 0, "grupuri": {}, "detalii": []}
    if out["ok"] and now is not None and meta.get("data_now") is not None:
        t = _ts(now)
        if t is not None and t - meta["data_now"] > stale_s:
            out["ok"] = False
    if not out["ok"]:
        return out
    lst = data.get("ac")
    if lst is None:
        lst = data.get("aircraft")
    center = (center_lat, center_lon)
    for ac in lst if isinstance(lst, list) else []:
        if not isinstance(ac, dict) or not is_military(ac) or _on_ground(ac):
            continue
        seen = _num(ac.get("seen"))
        if seen is not None and seen > max_seen_s:
            continue
        p = _pos(ac)
        if p is None:
            continue  # fără poziție nu știm dacă e în zonă (contact Mode-S fără poziție)
        if geo.haversine_km(center[0], center[1], p[0], p[1]) > radius_nm * 1.852 + 1:
            continue  # aircraft.json local: filtrăm pe distanță la noi
        g = group_of(ac)
        out["n"] += 1
        out["grupuri"][g] = out["grupuri"].get(g, 0) + 1
        d = {"grup": g, "dist_km": None, "directie": None}
        if not is_private(ac):  # PIA/LADD: doar numărate, fără distanță/direcție
            d["dist_km"] = int(round(geo.haversine_km(center[0], center[1], p[0], p[1]) / 10.0) * 10)
            d["directie"] = compass_ro(_bearing(center, p))
        out["detalii"].append(d)
    out["detalii"].sort(key=lambda d: (d["grup"] not in TRIGGER, d["dist_km"] if d["dist_km"] is not None else 1e9))
    out["detalii"] = out["detalii"][:8]
    return out


def describe(s: dict, center_name: str = "Iași", positions: bool = True) -> str:
    """Text scurt: „2 × avion de luptă (~40 km NE de Iași), 1 × avion radar/recunoaștere (~120 km S de Iași)”.
    positions=False: doar numere (pentru notele din alte mesaje)."""
    parts = []
    for g, n in sorted(s.get("grupuri", {}).items(), key=lambda kv: (kv[0] not in TRIGGER, -kv[1])):
        near = [d for d in s.get("detalii", []) if d["grup"] == g and d["dist_km"] is not None] if positions else []
        where = f" (~{near[0]['dist_km']} km {near[0]['directie']} de {center_name})" if near else ""
        parts.append(f"{n} × {g}{where}")
    return ", ".join(parts) if parts else "niciuna"
