"""Linia de comandă: python -m veghe <comandă>

  run             pornește serviciul (implicit)
  check-sources   citește fiecare sursă o dată și arată ce a înțeles (validarea live)
  replay FIȘIER   trece un scenariu JSONL prin motor (fără rețea, fără trimitere)
  report          cronologie pe un interval: primul semnal pe fiecare nivel vs. RO-Alert
  roalert JUDEȚ [--at HH:MM]   înregistrează un RO-Alert primit (adevărul de referință)
  outbox | aproba N | respinge N   coada de mesaje publice
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import signal
import sys

from . import __version__
from .config import load, validate
from .models import LEVEL_RO, Level, Signal
from .store import Store
from .timeutil import hhmm, now, parse_iso, to_local


def _app(args):
    from .app import App

    return App(load(args.config))


def cmd_run(args):
    app = _app(args)
    for s in (signal.SIGTERM, signal.SIGINT):
        signal.signal(s, lambda *_: app.stop.set())
    app.run_forever()


def cmd_check_sources(args):
    from .app import build_collectors

    cfg = load(args.config)
    warnings = validate(cfg)
    t = now()
    cols = build_collectors(cfg)
    print(f"veghe {__version__} · verificare surse · {hhmm(t)}\n")
    for w in warnings:
        print(f"ATENȚIE: {w}")
    ok = 0
    for c in cols:
        try:
            sigs = c.poll(t)
        except Exception as e:  # noqa: BLE001
            print(f"✗ {c.name:28s} EROARE {type(e).__name__}: {e}")
            continue
        ok += 1
        newest = max((s.published_at for s in sigs if s.published_at), default=None)
        print(f"✓ {c.name:28s} {len(sigs):3d} elemente · cel mai nou: {hhmm(newest) if newest else '-'}")
        for s in sigs[-3:]:
            extra = f" {json.dumps(s.meta, ensure_ascii=False)[:160]}" if s.role in ("ua_alert_state", "adsb") else ""
            print(f"      · {s.text[:140]}{extra}")
    print(f"\n{ok}/{len(cols)} surse au răspuns corect.")
    return 0 if ok == len(cols) else 1


def run_replay(lines, engine=None, store=None):
    """Trece semnalele prin motor cu ceasul simulat; întoarce [(timp, Message)]."""
    from .app import build_engine
    from .config import Config

    if engine is None:
        store = store or Store(":memory:")
        cfg = Config({"watch": {"ua_oblasts": ["Одеська область", "Вінницька область", "Чернівецька область"],
                                "ua_raions": ["Подільський район", "Роздільнянський район", "Ізмаїльський район",
                                              "Могилів-Подільський район", "Дністровський район"]}})
        engine = build_engine(cfg, store)
    out = []
    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        d = json.loads(raw)
        t = parse_iso(d["t"])
        s = Signal(source=d["source"], role=d["role"], text=d.get("text", ""), received_at=t,
                   published_at=parse_iso(d.get("published_at")) or t, url=d.get("url", ""), meta=d.get("meta", {}))
        if store is not None and s.role != "adsb":
            store.add_signal(s)
        for m in engine.tick(t) + engine.process(s, t):
            out.append((t, m))
    return out


def cmd_replay(args):
    with open(args.file, encoding="utf-8") as f:
        res = run_replay(f.readlines())
    for t, m in res:
        print(f"{hhmm(t)} [{m.channel}/{m.kind}] {m.text}\n")
    print(f"{len(res)} mesaje ({sum(1 for _, m in res if m.channel == 'public')} publice, care ar aștepta aprobare).")


def cmd_report(args):
    cfg = load(args.config)
    st = Store(cfg.get("general", "db_path", default="data/veghe.db"))
    t1 = parse_iso(args.to) if args.to else now()
    t0 = parse_iso(args.since) if args.since else t1 - dt.timedelta(hours=24)
    evs = st.events_between(t0, t1)
    sigs = [r for r in st.signals_between(t0, t1) if r["role"] == "manual"]
    first: dict[int, dt.datetime] = {}
    for e in evs:
        lv = int(e["level"] or 0)
        first.setdefault(lv, parse_iso(e["ts"]))
    ro = min((parse_iso(r["published_at"]) or parse_iso(r["received_at"]) for r in sigs), default=None)
    print(f"Interval {hhmm(t0)} – {hhmm(t1)} ({to_local(t0):%d.%m})")
    for lv in sorted(first):
        lead = f" · avans față de RO-Alert: {(ro - first[lv]).total_seconds() / 60:+.0f} min" if ro else ""
        print(f"  primul semnal „{LEVEL_RO[Level(lv)]}”: {hhmm(first[lv])}{lead}")
    print(f"  RO-Alert (înregistrat de operator): {hhmm(ro) if ro else 'neînregistrat'}")
    print(f"  evenimente: {len(evs)}")


def cmd_roalert(args):
    from .notify import parse_hhmm

    app = _app(args)
    at = parse_hhmm(args.at, now()) if args.at else now()
    app.log_roalert(args.county, at, "operator:cli")
    app.dispatcher.flush()
    print(f"Înregistrat RO-Alert {args.county} la {hhmm(at)}.")


def cmd_outbox(args):
    from .notify import Dispatcher

    st = Store(load(args.config).get("general", "db_path", default="data/veghe.db"))
    if args.cmd == "outbox":
        for r in st.outbox(limit=30):
            print(f"#{r['id']} {r['channel']}/{r['kind']} [{r['status']}] {r['text'][:120]}")
        return
    d = Dispatcher(st, [], [])
    print(d.approve(args.id, "cli") if args.cmd == "aproba" else d.reject(args.id, "cli"))


def main(argv=None):
    p = argparse.ArgumentParser(prog="veghe", description="avertizare timpurie OSINT pentru drone (Iași)")
    p.add_argument("--config", default="config.toml")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("run")
    sub.add_parser("check-sources")
    r = sub.add_parser("replay")
    r.add_argument("file")
    rp = sub.add_parser("report")
    rp.add_argument("--since", help="ISO, ex. 2026-10-31T14:00:00Z")
    rp.add_argument("--to")
    ra = sub.add_parser("roalert")
    ra.add_argument("county")
    ra.add_argument("--at", help="HH:MM, ora României")
    sub.add_parser("outbox")
    for name in ("aproba", "respinge"):
        x = sub.add_parser(name)
        x.add_argument("id", type=int)
    args = p.parse_args(argv)
    cfg_level = "INFO"
    logging.basicConfig(level=cfg_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cmd = args.cmd or "run"
    if cmd == "run":
        return cmd_run(args)
    if cmd == "check-sources":
        return cmd_check_sources(args)
    if cmd == "replay":
        return cmd_replay(args)
    if cmd == "report":
        return cmd_report(args)
    if cmd == "roalert":
        return cmd_roalert(args)
    return cmd_outbox(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
