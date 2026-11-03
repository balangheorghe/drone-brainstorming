"""Linia de comandă: python -m veghe <comandă>

  run             pornește serviciul (implicit)
  check-sources   citește fiecare sursă o dată și arată ce a înțeles (validarea live)
  replay FIȘIER   trece un scenariu JSONL prin motor (fără rețea, fără trimitere)
  report          cronologie pe un interval: primul semnal pe fiecare nivel vs. RO-Alert
  roalert JUDEȚ [--at HH:MM]   opțional: notează ora exactă a unui RO-Alert (altfel se ia din presă)
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
from .config import ConfigError, load, validate
from .models import LEVEL_RO, Level, Signal
from .store import Store
from .timeutil import hhmm, now, parse_iso, to_local


def cmd_run(args):
    from .app import App

    app = App(load(args.config), verify_private=True)
    for s in (signal.SIGTERM, signal.SIGINT):
        signal.signal(s, lambda *_: app.stop.set())
    app.run_forever()


def cmd_check_sources(args):
    from .app import build_collectors

    logging.getLogger("veghe.config").setLevel(logging.ERROR)  # avertismentele apar o singură dată, ca ATENȚIE
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
        note = ""
        raw = getattr(c, "last_raw", None)
        if c.role == "notam":
            note = f" (din {raw} NOTAM-uri în sursă; restul nu privesc zona sau nu sunt restricții)" if raw is not None else ""
        elif raw is not None and raw != len(sigs):
            note = f" (din {raw} în flux; restul nu conțin cuvintele-cheie)"
        elif raw == 0 and "when:" in getattr(c, "url", ""):
            note = " (fluxul caută doar știrile recente; gol când nu e nimic nou)"
        print(f"✓ {c.name:28s} {len(sigs):3d} elemente · cel mai nou: {hhmm(newest) if newest else '-'}{note}")
        for s in sigs[-3:]:
            extra = ""
            if s.role == "ua_alert_state":
                extra = f" {json.dumps(s.meta, ensure_ascii=False)[:160]}"
            elif s.role == "adsb":
                g = s.meta.get("gnss") or {}
                extra = (f" {json.dumps({'civil_airborne': s.meta.get('civil_airborne'), 'acoperire': (s.meta.get('coverage') or {}).get('reason'), 'gnss': g.get('level')}, ensure_ascii=False)}")
            print(f"      · {s.text[:140]}{extra}")
    print(f"\n{ok}/{len(cols)} surse au răspuns corect.")
    skew = clock_skew(cols)
    if skew is not None and abs(skew) > 120:
        print(f"\nATENȚIE: ceasul acestui calculator e cu ~{abs(skew) / 60:.0f} min {'înainte' if skew > 0 else 'în urmă'} "
              f"față de surse. Sincronizați ora (WSL: „wsl --shutdown” în PowerShell, apoi redeschideți Ubuntu; "
              f"server: sudo timedatectl set-ntp true).")
    print("\nArhiva și livrarea alertelor:")
    db_ok = check_database(cfg)
    delivery_ok = check_delivery(cfg, t)
    return 0 if ok == len(cols) and delivery_ok and db_ok else 1


def clock_skew(cols) -> float | None:
    """Diferența (secunde) dintre ceasul local și antetul HTTP Date al surselor; cea mai mică în valoare absolută."""
    import email.utils

    t = now()
    skews = []
    for c in cols:
        d = getattr(c, "last_date", None)
        if not d:
            continue
        try:
            skews.append((t - email.utils.parsedate_to_datetime(d)).total_seconds())
        except (TypeError, ValueError):
            continue
    return min(skews, key=abs) if skews else None


def check_database(cfg) -> bool:
    """Serviciul trebuie să poată scrie arhiva; altfel pornește și cade la nesfârșit."""
    db = cfg.get("general", "db_path", default="data/veghe.db")
    try:
        Store(db).close()
    except Exception as e:  # noqa: BLE001
        print(f"✗ baza de date {db}: {type(e).__name__}: {e} → directorul trebuie să fie al utilizatorului "
              f"serviciului (Docker: sudo chown 10001:10001 data; systemd: sudo chown veghe:veghe data)")
        return False
    print(f"✓ baza de date {db}: se poate scrie")
    return True


def check_delivery(cfg, t) -> bool:
    """Trimite un mesaj de test în grupul intern (și pe ntfy, dacă e configurat). Fără asta, un ID
    de grup greșit ar însemna alerte care nu ajung nicăieri, fără ca cineva să afle."""
    from .app import build_dispatcher
    from .notify import NtfySender, TelegramSender, describe_error

    text = (f"[INTERN] veghe {__version__} · test de livrare (check-sources) · {hhmm(t)}. "
            f"Dacă vedeți acest mesaj, alertele vor ajunge aici.")
    tok, chat = cfg.secret("telegram_bot_token"), cfg.secret("telegram_internal_chat_id")
    api = cfg.get("notify", "telegram_api", default="https://api.telegram.org")
    dispatcher, _ = build_dispatcher(cfg, Store(":memory:"))
    ntfy = [s for s in dispatcher.senders["internal"] if isinstance(s, NtfySender)]
    good = True
    if tok and chat:
        tg = TelegramSender(tok, chat, api, 0)
        try:
            reason = None if cfg.get("notify", "allow_unverified_internal_chat", default=False) else tg.check_private()
            if reason:
                print(f"✗ telegram intern {chat}: {reason} (nu s-a trimis nimic)")
                good = False
            else:
                tg.send(text)
                print(f"✓ telegram intern {chat}: mesaj de test trimis – verificați că a apărut în grupul privat")
        except Exception as e:  # noqa: BLE001
            print(f"✗ telegram intern {chat}: {describe_error(e)}")
            good = False
    elif ntfy:
        print("- telegram intern: neconfigurat (alertele merg doar pe ntfy)")
    else:
        print("✗ telegram intern: TELEGRAM_BOT_TOKEN / TELEGRAM_INTERNAL_CHAT_ID lipsesc → alertele apar doar în jurnal")
        good = False
    for s in ntfy:
        try:
            s.send(text)
            print(f"✓ {s.name}: mesaj de test trimis")
        except Exception as e:  # noqa: BLE001
            print(f"✗ {s.name}: {describe_error(e, telegram=False)}")
            good = False
    return good


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


# evenimentele care înseamnă „am aflat ceva” (fără cele de întreținere: oprirea vigilenței, ADS-B, închideri)
SIGNAL_KINDS = {"vigilenta_start", "directie", "moldova", "apropiere", "oficial"}


def cmd_report(args):
    from .config import num

    cfg = load(args.config)
    st = Store(cfg.get("general", "db_path", default="data/veghe.db"))
    t1 = parse_iso(args.to) if args.to else now()
    t0 = parse_iso(args.since) if args.since else t1 - dt.timedelta(hours=24)
    evs = st.events_between(t0, t1)
    first: dict[int, dt.datetime] = {}
    for e in evs:
        if e["kind"] in SIGNAL_KINDS:
            first.setdefault(int(e["level"] or 0), parse_iso(e["ts"]))
    end = next((parse_iso(e["ts"]) for e in evs if e["kind"] == "incetare"), None)
    manual = st.manual_between(t0, t1)
    if manual:
        ro = min(parse_iso(r["published_at"]) or parse_iso(r["received_at"]) for r in manual)
        ro_label = "înregistrat de operator"
    else:
        max_age = num(cfg.get("engine", "max_age_news_min", default=60), "engine.max_age_news_min")
        ro, ro_label = roalert_from_events(st, evs, max_age)

    def when(x):
        return hhmm(x) if to_local(x).date() == to_local(t0).date() else f"{to_local(x):%d.%m} {hhmm(x)}"

    print(f"Interval {hhmm(t0)} – {hhmm(t1)} ({to_local(t0):%d.%m})")
    for lv in sorted(first):
        lead = f" · avans față de RO-Alert: {(ro - first[lv]).total_seconds() / 60:+.0f} min" if ro else ""
        print(f"  primul semnal „{LEVEL_RO[Level(lv)]}”: {when(first[lv])}{lead}")
    print(f"  RO-Alert ({ro_label}): {when(ro)}" if ro else "  RO-Alert: negăsit (nici în presă, nici înregistrat)")
    if end:
        print(f"  încetare raportată: {when(end)}")
    print(f"  evenimente: {len(evs)}")


def roalert_from_events(st: Store, evs, max_age_min: float) -> tuple[dt.datetime | None, str]:
    """Ora RO-Alert fără nicio înregistrare manuală: pentru fiecare mesaj OFICIAL, găsim știrea
    (sau înregistrarea) care l-a produs – același titlu, primită înainte de mesaj, nu mai veche
    decât acceptă motorul – și luăm ora ei de publicare. Întoarce (ora, eticheta)."""
    from .engine import Engine

    offs = [(parse_iso(e["ts"]), e["text"]) for e in evs if e["kind"] == "oficial"]
    if not offs:
        return None, ""
    age = dt.timedelta(minutes=max_age_min)
    rows = [r for r in st.signals_between(min(t for t, _ in offs) - age - dt.timedelta(minutes=5), max(t for t, _ in offs))
            if r["role"] in ("ro_official_news", "manual")]
    best: tuple[dt.datetime, str] | None = None
    for ts, title in offs:
        match = [r for r in rows if Engine._excerpt(r["text"], 180) == title and parse_iso(r["received_at"]) <= ts
                 and (parse_iso(r["published_at"]) or parse_iso(r["received_at"])) >= ts - age]
        if not match:
            cand = (ts, "ora la care serviciul a aflat")
        else:
            r = max(match, key=lambda x: x["received_at"])  # cea care a declanșat mesajul
            if r["role"] == "manual":
                cand = (parse_iso(r["published_at"]) or parse_iso(r["received_at"]), "înregistrat de operator")
            elif r["published_at"]:
                cand = (parse_iso(r["published_at"]), "din presă, ora publicării; alerta reală a fost cu câteva minute mai devreme")
            else:
                cand = (parse_iso(r["received_at"]), "ora la care serviciul a aflat din presă")
        if best is None or cand[0] < best[0]:
            best = cand
    return best


def cmd_roalert(args):
    """Doar arhivează (pentru raport). Serviciul care rulează nu e anunțat: pentru asta folosiți
    /roalert pe Telegram. Așa nu se creează mesaje duble sau trimiteri în paralel."""
    from .iso_helpers import manual_roalert_signal
    from .notify import parse_hhmm

    cfg = load(args.config)
    st = Store(cfg.get("general", "db_path", default="data/veghe.db"))
    at = parse_hhmm(args.at, now()) if args.at else now()
    st.add_signal(manual_roalert_signal(args.county, at, "operator:cli"))
    print(f"Arhivat RO-Alert {args.county} la {hhmm(at)} (doar pentru raport; serviciul pornit nu e anunțat).")


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
    level = "INFO"
    try:
        import tomllib

        with open(args.config, "rb") as f:
            level = str(tomllib.load(f).get("general", {}).get("log_level", "INFO")).upper()
    except (OSError, ValueError):
        pass
    logging.basicConfig(level=getattr(logging, level, logging.INFO), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cmd = args.cmd or "run"
    try:
        return _dispatch(cmd, args)
    except ConfigError as e:
        print(f"Configurare greșită: {e}", file=sys.stderr)
        return 2
    except FileNotFoundError as e:
        if e.filename and str(e.filename).endswith(".toml"):
            print(f"Lipsește fișierul de configurare {e.filename} (copiați config.example.toml în config.toml).",
                  file=sys.stderr)
            return 2
        raise


def _dispatch(cmd, args):
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
