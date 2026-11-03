"""Arhiva SQLite: toate semnalele (cu ora de primire), deciziile, coada de mesaje,
starea surselor și eșantioanele ADS-B. Un singur fișier, ușor de copiat."""

from __future__ import annotations

import datetime as dt
import json
import os
import sqlite3
import threading

from .models import Signal
from .timeutil import iso, now, parse_iso

SCHEMA = """
CREATE TABLE IF NOT EXISTS signals (
  id INTEGER PRIMARY KEY,
  key TEXT UNIQUE NOT NULL,
  source TEXT NOT NULL,
  role TEXT NOT NULL,
  text TEXT NOT NULL,
  url TEXT,
  published_at TEXT,
  received_at TEXT NOT NULL,
  meta TEXT
);
CREATE INDEX IF NOT EXISTS ix_signals_received ON signals(received_at);
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY,
  ts TEXT NOT NULL,
  level INTEGER,
  hypothesis INTEGER,
  kind TEXT,
  text TEXT
);
CREATE TABLE IF NOT EXISTS outbox (
  id INTEGER PRIMARY KEY,
  created_at TEXT NOT NULL,
  channel TEXT NOT NULL,
  kind TEXT NOT NULL,
  text TEXT NOT NULL,
  status TEXT NOT NULL,
  origin_role TEXT,
  approved_by TEXT,
  sent_at TEXT,
  attempts INTEGER DEFAULT 0,
  error TEXT,
  delivered TEXT DEFAULT '',
  next_attempt_at TEXT
);
CREATE TABLE IF NOT EXISTS health (
  source TEXT PRIMARY KEY,
  last_ok TEXT,
  last_error TEXT,
  last_error_at TEXT,
  error_count INTEGER DEFAULT 0,
  last_count INTEGER DEFAULT 0,
  last_sample TEXT
);
CREATE TABLE IF NOT EXISTS adsb_samples (
  ts TEXT NOT NULL,
  point TEXT NOT NULL,
  civil_airborne INTEGER,
  civil_total INTEGER
);
CREATE INDEX IF NOT EXISTS ix_adsb_point_ts ON adsb_samples(point, ts);
CREATE TABLE IF NOT EXISTS adsb_gnss (
  ts TEXT NOT NULL,
  point TEXT NOT NULL,
  n INTEGER,
  degraded INTEGER,
  lost INTEGER,
  ratio REAL
);
CREATE INDEX IF NOT EXISTS ix_adsb_gnss_point_ts ON adsb_gnss(point, ts);
CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT);
CREATE INDEX IF NOT EXISTS ix_outbox_status ON outbox(status, id);
"""


class Store:
    def __init__(self, path: str):
        if path != ":memory:":
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self._lock = threading.RLock()
        self._db = sqlite3.connect(path, check_same_thread=False, timeout=30)
        if path != ":memory:":
            try:
                os.chmod(path, 0o600)  # arhiva conține texte interne: doar pentru utilizatorul serviciului
            except OSError:
                pass
        self._db.row_factory = sqlite3.Row
        with self._lock:
            self._db.execute("PRAGMA journal_mode=WAL")
            self._db.execute("PRAGMA secure_delete=ON")  # textele înlocuite nu rămân în paginile libere
            self._db.executescript(SCHEMA)
            for col in ("delivered TEXT DEFAULT ''", "next_attempt_at TEXT"):  # migrare pentru baze mai vechi
                try:
                    self._db.execute(f"ALTER TABLE outbox ADD COLUMN {col}")
                except sqlite3.OperationalError:
                    pass
            self._db.commit()

    def close(self):
        with self._lock:
            self._db.close()

    # --- semnale ---
    def add_signal(self, s: Signal) -> bool:
        """Salvează semnalul; întoarce False dacă era deja (deduplicare)."""
        with self._lock:
            try:
                self._db.execute(
                    "INSERT INTO signals(key,source,role,text,url,published_at,received_at,meta) VALUES (?,?,?,?,?,?,?,?)",
                    (s.key(), s.source, s.role, s.text, s.url, iso(s.published_at), iso(s.received_at),
                     json.dumps(s.meta, ensure_ascii=False)),
                )
                self._db.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def signals_between(self, t0: dt.datetime, t1: dt.datetime) -> list[sqlite3.Row]:
        with self._lock:
            return list(self._db.execute(
                "SELECT * FROM signals WHERE received_at >= ? AND received_at <= ? ORDER BY received_at",
                (iso(t0), iso(t1))))

    def manual_between(self, t0: dt.datetime, t1: dt.datetime) -> list[sqlite3.Row]:
        """Înregistrările operatorului după ora ALERTEI (published_at), nu după ora înregistrării."""
        with self._lock:
            return list(self._db.execute(
                "SELECT * FROM signals WHERE role='manual' AND COALESCE(published_at, received_at) BETWEEN ? AND ? "
                "ORDER BY COALESCE(published_at, received_at)", (iso(t0), iso(t1))))

    def recent_signals(self, n: int = 10) -> list[sqlite3.Row]:
        with self._lock:
            return list(self._db.execute("SELECT * FROM signals ORDER BY id DESC LIMIT ?", (n,)))

    # --- evenimente (decizii ale motorului) ---
    def add_event(self, level: int, hypothesis: int | None, kind: str, text: str, ts: dt.datetime | None = None):
        with self._lock:
            self._db.execute("INSERT INTO events(ts,level,hypothesis,kind,text) VALUES (?,?,?,?,?)",
                             (iso(ts or now()), int(level), hypothesis, kind, text))
            self._db.commit()

    def events_between(self, t0: dt.datetime, t1: dt.datetime) -> list[sqlite3.Row]:
        with self._lock:
            return list(self._db.execute("SELECT * FROM events WHERE ts >= ? AND ts <= ? ORDER BY ts", (iso(t0), iso(t1))))

    # --- coada de mesaje ---
    def enqueue(self, channel: str, kind: str, text: str, status: str, origin_role: str = "") -> int:
        with self._lock:
            cur = self._db.execute(
                "INSERT INTO outbox(created_at,channel,kind,text,status,origin_role) VALUES (?,?,?,?,?,?)",
                (iso(now()), channel, kind, text, status, origin_role))
            self._db.commit()
            return int(cur.lastrowid)

    def outbox(self, status: str | None = None, limit: int = 50, newest_first: bool = False) -> list[sqlite3.Row]:
        order = "DESC" if newest_first else "ASC"
        with self._lock:
            if status:
                return list(self._db.execute(f"SELECT * FROM outbox WHERE status=? ORDER BY id {order} LIMIT ?", (status, limit)))
            return list(self._db.execute("SELECT * FROM outbox ORDER BY id DESC LIMIT ?", (limit,)))

    def outbox_due(self, at: dt.datetime, limit: int = 50) -> list[sqlite3.Row]:
        """Mesajele de trimis acum (filtrul pe next_attempt_at e ÎNAINTE de LIMIT, ca rândurile
        în reîncercare să nu blocheze mesajele noi)."""
        with self._lock:
            return list(self._db.execute(
                "SELECT * FROM outbox WHERE status='queued' AND (next_attempt_at IS NULL OR next_attempt_at <= ?) "
                "ORDER BY id LIMIT ?", (iso(at), limit)))

    def cas_outbox(self, oid: int, expect_status: str, extra_where: str = "", extra_args: tuple = (), **fields) -> int:
        """Actualizare condiționată (compare-and-set); întoarce numărul de rânduri modificate."""
        cols = ", ".join(f"{k}=?" for k in fields)
        with self._lock:
            cur = self._db.execute(f"UPDATE outbox SET {cols} WHERE id=? AND status=? {extra_where}",
                                   (*fields.values(), oid, expect_status, *extra_args))
            self._db.commit()
            return cur.rowcount

    def supersede_queued(self, kind: str) -> int:
        """Retrage mesajele interne încă netrimise de un anumit tip (ex. „veghe pornit” de la
        reporniri cât Telegram era indisponibil), ca să nu sosească toate deodată."""
        with self._lock:
            cur = self._db.execute("UPDATE outbox SET status='superseded' WHERE kind=? AND status='queued' "
                                   "AND channel='internal'", (kind,))
            self._db.commit()
            return cur.rowcount

    def failed_outbox_count(self, channel: str = "internal", since: dt.datetime | None = None) -> int:
        with self._lock:
            return self._db.execute("SELECT COUNT(*) FROM outbox WHERE channel=? AND status='failed' AND created_at >= ?",
                                    (channel, iso(since or now() - dt.timedelta(hours=24)))).fetchone()[0]

    def get_outbox(self, oid: int) -> sqlite3.Row | None:
        with self._lock:
            return self._db.execute("SELECT * FROM outbox WHERE id=?", (oid,)).fetchone()

    def set_outbox(self, oid: int, **fields):
        cols = ", ".join(f"{k}=?" for k in fields)
        with self._lock:
            self._db.execute(f"UPDATE outbox SET {cols} WHERE id=?", (*fields.values(), oid))
            self._db.commit()

    # --- starea surselor ---
    def health_ok(self, source: str, count: int, sample: str = ""):
        with self._lock:
            self._db.execute(
                "INSERT INTO health(source,last_ok,last_count,last_sample,error_count) VALUES (?,?,?,?,0) "
                "ON CONFLICT(source) DO UPDATE SET last_ok=excluded.last_ok, last_count=excluded.last_count, "
                "last_sample=excluded.last_sample, error_count=0",
                (source, iso(now()), count, sample[:300]))
            self._db.commit()

    def health_error(self, source: str, error: str):
        with self._lock:
            self._db.execute(
                "INSERT INTO health(source,last_error,last_error_at,error_count) VALUES (?,?,?,1) "
                "ON CONFLICT(source) DO UPDATE SET last_error=excluded.last_error, "
                "last_error_at=excluded.last_error_at, error_count=health.error_count+1",
                (source, error[:600], iso(now())))
            self._db.commit()

    def health(self) -> list[sqlite3.Row]:
        with self._lock:
            return list(self._db.execute("SELECT * FROM health ORDER BY source"))

    # --- ADS-B ---
    def add_adsb_sample(self, ts: dt.datetime, point: str, airborne: int, total: int):
        # doar trafic civil; aeronavele militare nu se numără și nu se păstrează
        with self._lock:
            self._db.execute("INSERT INTO adsb_samples(ts,point,civil_airborne,civil_total) VALUES (?,?,?,?)",
                             (iso(ts), point, airborne, total))
            self._db.commit()

    def prune(self, keep_adsb_days: int = 7):
        with self._lock:
            cut = iso(now() - dt.timedelta(days=keep_adsb_days))
            self._db.execute("DELETE FROM adsb_samples WHERE ts < ?", (cut,))
            self._db.execute("DELETE FROM adsb_gnss WHERE ts < ?", (cut,))
            # rezumatele militare nu se păstrează (de obicei sunt deja înlocuite la livrare)
            self._db.execute("UPDATE outbox SET text='[ADS-B militar – conținutul nu se păstrează]' "
                             "WHERE kind='adsb_militar' AND status!='queued' AND text NOT LIKE '[ADS-B militar%'")
            self._db.execute("UPDATE events SET text='' WHERE kind='adsb_militar' AND text!=''")
            rows = list(self._db.execute("SELECT id, kind, text FROM outbox WHERE status!='queued' AND text LIKE '%ADS-B militar (%'"))
            self._db.commit()
        if rows:
            from .notify import redact_military

            for r in rows:
                self.set_outbox(r["id"], text=redact_military(r["text"], r["kind"], ""))
        self.checkpoint()

    def checkpoint(self):
        with self._lock:
            try:
                self._db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            except sqlite3.OperationalError:
                pass

    def add_adsb_gnss(self, ts: dt.datetime, point: str, n: int, degraded: int, lost: int, ratio: float):
        # doar agregate pe zonă (câte aeronave, câte cu GPS degradat); nicio identitate
        with self._lock:
            self._db.execute("INSERT INTO adsb_gnss(ts,point,n,degraded,lost,ratio) VALUES (?,?,?,?,?,?)",
                             (iso(ts), point, int(n), int(degraded), int(lost), float(ratio)))
            self._db.commit()

    def adsb_gnss_baseline(self, point: str, at: dt.datetime, days: int = 7, min_n: int = 4) -> tuple[float | None, float]:
        """(p90 al raportului GNSS degradat pe ultimele `days` zile, câte zile acoperă eșantioanele)."""
        with self._lock:
            rows = list(self._db.execute("SELECT ts, ratio FROM adsb_gnss WHERE point=? AND ts>=? AND n>=? ORDER BY ts",
                                         (point, iso(at - dt.timedelta(days=days)), min_n)))
        if not rows:
            return None, 0.0
        vals = sorted(r["ratio"] for r in rows)
        p90 = vals[min(len(vals) - 1, int(0.9 * (len(vals) - 1) + 0.5))]
        span = (parse_iso(rows[-1]["ts"]) - parse_iso(rows[0]["ts"])).total_seconds() / 86400
        return p90, span

    def signals_by_role(self, role: str, since: dt.datetime) -> list[sqlite3.Row]:
        with self._lock:
            return list(self._db.execute("SELECT * FROM signals WHERE role=? AND received_at>=? ORDER BY received_at, id",
                                         (role, iso(since))))

    def adsb_samples(self, point: str, since: dt.datetime) -> list[sqlite3.Row]:
        with self._lock:
            return list(self._db.execute(
                "SELECT * FROM adsb_samples WHERE point=? AND ts>=? ORDER BY ts", (point, iso(since))))

    # --- chei simple ---
    def kv_get(self, k: str, default: str | None = None) -> str | None:
        with self._lock:
            r = self._db.execute("SELECT v FROM kv WHERE k=?", (k,)).fetchone()
            return r["v"] if r else default

    def kv_set(self, k: str, v: str):
        with self._lock:
            self._db.execute("INSERT INTO kv VALUES (?,?) ON CONFLICT(k) DO UPDATE SET v=excluded.v", (k, v))
            self._db.commit()


def row_time(r, col: str) -> dt.datetime | None:
    return parse_iso(r[col])
