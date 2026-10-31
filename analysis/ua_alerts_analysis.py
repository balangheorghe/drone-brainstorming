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


# Detecții anunțate de R. Moldova în 2026 (ora în UTC) + regiunea UA de unde a venit drona.
# Surse: comunicatele MA RM citate în presă (vezi docs/01-incidente.md, docs/09-evenimente-2026.md).
MD_DETECTIONS = [
    ("30.03 Comarivka → Orhei", "2026-03-30T18:29", "Odeska oblast"),
    ("13.05 dinspre Mohyliv-Podilskyi", "2026-05-13T13:00", "Vinnytska oblast"),
    ("16.08 Etulia → Galați", "2026-08-16T01:31", "Odeska oblast"),
    ("17.08 Cuciurgan → Tiraspol", "2026-08-17T14:37", "Odeska oblast"),
    ("20.08 Etulia", "2026-08-20T00:16", "Odeska oblast"),
    ("24.08 dinspre Vinogradovka → Cahul → Galați", "2026-08-24T02:55", "Odeska oblast"),
    ("26.08 Palanca", "2026-08-26T14:38", "Odeska oblast"),
    ("27.08 5 drone, noaptea (regiune presupusă)", "2026-08-27T00:56", "Odeska oblast"),
    ("08.09 → Bender → Iași", "2026-09-08T13:20", "Odeska oblast"),
    ("12.09 Vasilcău (Soroca) → Botoșani", "2026-09-12T12:26", "Vinnytska oblast"),
    ("24.09 dinspre Chelimenți (Cernăuți) → Solca", "2026-09-24T03:14", "Chernivetska oblast"),
    ("30.09 Bender (regiune presupusă)", "2026-09-30T02:43", "Odeska oblast"),
    ("30.09 Lunga (Dubăsari), cu reacție", "2026-09-30T07:26", "Odeska oblast"),
    ("03.10 5 drone, dimineața (regiune presupusă)", "2026-10-03T04:45", "Odeska oblast"),
    ("16.10 Sobari (Soroca)", "2026-10-16T13:22", "Vinnytska oblast"),
    ("23.10 dinspre Verhnia Slobidka (Vinnița)", "2026-10-23T10:59", "Vinnytska oblast"),
    ("31.10 drona 1, dinspre Semionovca", "2026-10-31T14:24", "Odeska oblast"),
    ("31.10 drona 2, dinspre Mihailovka (Vinnița)", "2026-10-31T15:50", "Vinnytska oblast"),
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


def base_rates(off, vol):
    """Procentul din timp în care e activă cel puțin o alertă, pe regiuni.

    Sursa principală: datele OFICIALE (din dec. 2025 alertele sunt pe raioane; o regiune
    contează ca „în alertă” dacă oricare raion al ei e în alertă). Datele de voluntari
    sunt doar la nivel de regiune și SUBESTIMEAZĂ mult alertele pe raioane.
    """
    t0 = dt.datetime(2026, 1, 1, tzinfo=UTC)
    off_end = max(parse(r["started_at"]) for r in off)
    vol_end = max(parse(r["started_at"]) for r in vol)
    print(f"\n## Rate de bază 2026\n")
    print(f"Oficial (raioane): {t0.date()} → {off_end:%Y-%m-%d %H:%M} UTC. "
          f"Voluntari (doar regiune, subestimează): {t0.date()} → {vol_end:%Y-%m-%d %H:%M} UTC.\n")
    print("| Regiune | % timp în alertă – oficial (oricare raion) | % timp – voluntari | Alerte voluntari |")
    print("|---|---|---|---|")
    so = (off_end - t0).total_seconds() / 3600
    sv = (vol_end - t0).total_seconds() / 3600
    for reg in REGIONS:
        ro = [r for r in off if r["oblast"] == reg and parse(r["started_at"]) >= t0]
        rv = [r for r in vol if r["region"] == reg and parse(r["started_at"]) >= t0]
        print(f"| {reg} | {100 * union_hours(ro, t0, off_end) / so:.1f}% | {100 * union_hours(rv, t0, vol_end) / sv:.1f}% | {len(rv)} |")
    for group in ([REGIONS[0], REGIONS[2], REGIONS[3]], REGIONS):
        ro = [r for r in off if r["oblast"] in group and parse(r["started_at"]) >= t0]
        rv = [r for r in vol if r["region"] in group and parse(r["started_at"]) >= t0]
        name = "oricare din " + ", ".join(g.split()[0] for g in group)
        print(f"| {name} | {100 * union_hours(ro, t0, off_end) / so:.1f}% | {100 * union_hours(rv, t0, vol_end) / sv:.1f}% | – |")
    print("\n### Pe raioane (oficial)\n")
    print("| Raion | % timp în alertă |")
    print("|---|---|")
    raions = sorted({(r["oblast"], r["raion"]) for r in off if r["oblast"] in REGIONS[:1] + REGIONS[2:] and r["raion"]})
    for ob, ra in raions:
        rows = [r for r in off if r["oblast"] == ob and r["raion"] == ra and parse(r["started_at"]) >= t0]
        print(f"| {ob} / {ra} | {100 * union_hours(rows, t0, off_end) / so:.1f}% |")


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


def md_gate_table(off, vol):
    """Pentru fiecare detecție MD: era activă alerta UA în regiunea de plecare?

    Folosește datele oficiale pe raioane când acoperă momentul; altfel datele de
    voluntari (marcate, pentru că subestimează)."""
    off_end = max(parse(r["started_at"]) for r in off)
    vol_end = max(parse(r["started_at"]) for r in vol)
    print("\n## Detecții R. Moldova vs. alerte UA în regiunea de plecare\n")
    print("| Detecție MD | UTC | Regiune UA | Sursa datelor | Alertă activă? | Pornită cu (min) | Raioane în alertă |")
    print("|---|---|---|---|---|---|---|")
    stats = {"oficial": [0, 0], "voluntari": [0, 0]}
    for name, t, src in MD_DETECTIONS:
        T = dt.datetime.fromisoformat(t).replace(tzinfo=UTC)
        if T <= off_end:
            label, rows = "oficial", [r for r in off if r["oblast"] == src]
        elif T <= vol_end:
            label, rows = "voluntari", [r for r in vol if r["region"] == src]
        else:
            print(f"| {name} | {T:%Y-%m-%d %H:%M} | {src} | – | _date indisponibile încă_ | – | – |")
            continue
        act = [r for r in rows if parse(r["started_at"]) <= T <= parse(r["finished_at"])]
        lead = max(((T - parse(r["started_at"])).total_seconds() / 60 for r in act), default=None)
        raions = ", ".join(sorted({r["raion"].replace(" raion", "") for r in act if r.get("raion")})) or ("(regiune)" if act else "")
        stats[label][0] += bool(act)
        stats[label][1] += 1
        print(f"| {name} | {T:%Y-%m-%d %H:%M} | {src} | {label} | {'DA' if act else 'nu'} | "
              f"{'' if lead is None else f'{lead:.0f}'} | {raions} |")
    print()
    for k, (h, n) in stats.items():
        if n:
            print(f"- **{k}:** alertă activă în regiunea de plecare la {h}/{n} detecții.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=os.path.join(os.path.dirname(__file__), "data"))
    a = ap.parse_args()
    download(a.data_dir)
    off, vol = load(a.data_dir)
    base_rates(off, vol)
    md_gate_table(off, vol)
    incident_table(off, vol)


if __name__ == "__main__":
    main()
