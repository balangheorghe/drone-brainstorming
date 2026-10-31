#!/usr/bin/env python3
"""Analiza alertelor aeriene ucrainene din regiunile vecine R. Moldova / României.

Ce face:
  1. Descarcă setul public de date Vadimkin/ukrainian-air-raid-sirens-dataset
     (licență MIT; ore în UTC; actualizat zilnic):
       - official_data_en.csv  (alerte oficiale, pe oblast/raion/hromadă)
       - volunteer_data_en.csv (canalul eTryvoga, doar pe oblast)
  2. Calculează ratele de bază pentru 2026: câte alerte și ce procent din timp
     e activă alerta în Odesa, Mykolaiv, Vinnytsia, Chernivtsi.
  3. Pentru fiecare incident din INCIDENTS, arată ce alerte ucrainene erau
     active sau porniseră în cele 3 ore dinainte (avans în minute).

Rulare:  python3 analysis/ua_alerts_analysis.py [--data-dir DIR]
Numai biblioteca standard Python 3.9+.
"""
import argparse
import csv
import datetime as dt
import os
import urllib.request

BASE = "https://raw.githubusercontent.com/Vadimkin/ukrainian-air-raid-sirens-dataset/main/datasets/"
FILES = ["official_data_en.csv", "volunteer_data_en.csv"]
UTC = dt.timezone.utc

REGIONS = ["Odeska oblast", "Mykolaivska oblast", "Vinnytska oblast", "Chernivetska oblast"]

# Incidente 2026 cu oră cunoscută (ora în UTC). Adăugați aici evenimente noi.
# Ora locală: EEST = UTC+3 până la 25.10.2026; EET = UTC+2 după.
INCIDENTS = [
    ("29.05.2026 Galați, impact pe bloc (~01:50 EEST)", "2026-05-28T22:50"),
    ("16.08.2026 intrare în RO dinspre MD (04:44 EEST)", "2026-08-16T01:44"),
    ("08.09.2026 detecție MD, drona spre Iași (16:20 EEST)", "2026-09-08T13:20"),
    ("15.10.2026 Sulina, contact radar (01:34 EEST)", "2026-10-14T22:34"),
    ("17.10.2026 Sulina, intrare (~17:59 EEST)", "2026-10-17T14:59"),
    ("21.10.2026 Tulcea, RO-Alert (~03:30 EEST)", "2026-10-21T00:30"),
    ("31.10.2026 drona 1, detecție MD, spre Iași (16:24 EET)", "2026-10-31T14:24"),
    ("31.10.2026 drona 2, intrare în MD dinspre Vinnița (17:50 EET)", "2026-10-31T15:50"),
]


def parse(ts):
    return dt.datetime.fromisoformat(ts)


def download(data_dir):
    os.makedirs(data_dir, exist_ok=True)
    for name in FILES:
        path = os.path.join(data_dir, name)
        if not os.path.exists(path):
            print(f"descarc {name} ...")
            urllib.request.urlretrieve(BASE + name, path)


def load(data_dir):
    off = list(csv.DictReader(open(os.path.join(data_dir, FILES[0]), encoding="utf-8")))
    vol = list(csv.DictReader(open(os.path.join(data_dir, FILES[1]), encoding="utf-8")))
    for r in vol:
        r["oblast"] = r["region"]
        r["raion"] = ""
    return off, vol


def union_hours(rows, t0, t1):
    """Ore în care cel puțin o alertă din `rows` e activă în intervalul [t0, t1]."""
    iv = sorted((max(parse(r["started_at"]), t0), min(parse(r["finished_at"]), t1)) for r in rows)
    iv = [x for x in iv if x[1] > x[0]]
    total, cur = dt.timedelta(), None
    for s, f in iv:
        if cur is None:
            cur = [s, f]
        elif s <= cur[1]:
            cur[1] = max(cur[1], f)
        else:
            total += cur[1] - cur[0]
            cur = [s, f]
    if cur:
        total += cur[1] - cur[0]
    return total.total_seconds() / 3600


def base_rates(vol):
    t0 = dt.datetime(2026, 1, 1, tzinfo=UTC)
    t1 = max(parse(r["started_at"]) for r in vol)
    span = (t1 - t0).total_seconds() / 3600
    print(f"\n## Rate de bază 2026 (date voluntari eTryvoga, {t0.date()} → {t1:%Y-%m-%d %H:%M} UTC)\n")
    print("| Regiune | Alerte | Zile cu alertă | % din timp cu alertă activă |")
    print("|---|---|---|---|")
    for reg in REGIONS:
        rows = [r for r in vol if r["region"] == reg and parse(r["started_at"]) >= t0]
        days = len({r["started_at"][:10] for r in rows})
        print(f"| {reg} | {len(rows)} | {days} | {100 * union_hours(rows, t0, t1) / span:.1f}% |")
    for group in (REGIONS[:1], [REGIONS[0], REGIONS[2], REGIONS[3]], REGIONS):
        rows = [r for r in vol if r["region"] in group and parse(r["started_at"]) >= t0]
        print(f"| oricare din {', '.join(g.split()[0] for g in group)} | – | – | {100 * union_hours(rows, t0, t1) / span:.1f}% |")


def incident_table(off, vol):
    off_end = max(parse(r["started_at"]) for r in off)
    vol_end = max(parse(r["started_at"]) for r in vol)
    print("\n## Alerte ucrainene în jurul incidentelor\n")
    print("Avans = minute între pornirea alertei UA și momentul incidentului (pozitiv = alerta a fost înainte).\n")
    for name, t in INCIDENTS:
        T = dt.datetime.fromisoformat(t).replace(tzinfo=UTC)
        print(f"### {name} — {T:%Y-%m-%d %H:%M} UTC\n")
        if T > vol_end:
            print(f"_Date indisponibile încă (setul de voluntari se oprește la {vol_end:%Y-%m-%d %H:%M} UTC). Rulați din nou mâine._\n")
            continue
        print("| Sursă | Regiune / raion | Start UTC | Sfârșit UTC | Avans (min) | Activă la momentul T |")
        print("|---|---|---|---|---|---|")
        sets = [("voluntari", vol)] + ([("oficial", off)] if T <= off_end else [])
        for label, rows in sets:
            for r in rows:
                if r["oblast"] not in REGIONS:
                    continue
                s, f = parse(r["started_at"]), parse(r["finished_at"])
                if T - dt.timedelta(hours=3) <= s <= T + dt.timedelta(minutes=30) or s <= T <= f:
                    where = r["oblast"] + (f" / {r['raion']}" if r.get("raion") else "")
                    print(f"| {label} | {where} | {s:%H:%M} | {f:%H:%M} | {(T - s).total_seconds() / 60:+.0f} | {'DA' if s <= T <= f else 'nu'} |")
        print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=os.path.join(os.path.dirname(__file__), "data"))
    a = ap.parse_args()
    download(a.data_dir)
    off, vol = load(a.data_dir)
    base_rates(vol)
    incident_table(off, vol)


if __name__ == "__main__":
    main()
