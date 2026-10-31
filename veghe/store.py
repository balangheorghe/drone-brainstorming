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
  error TEXT
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
  civil_total INTEGER,
  excluded_military INTEGER
);
CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT);
"""


class Store:
    def __init__(self, path: str):
        if path != ":memory:":
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self._lock = threading.RLock()
        self._db = sqlite3.connect(path, check_same_thread=False, timeout=30)
        self._db.row_factory = sqlite3.Row
        with self._lock:
            self._db.execute("PRAGMA journal_mode=WAL")
            self._db.executescript(SCHEMA)
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

    def outbox(self, status: str | None = None, limit: int = 50) -> list[sqlite3.Row]:
        with self._lock:
            if status:
                return list(self._db.execute("SELECT * FROM outbox WHERE status=? ORDER BY id LIMIT ?", (status, limit)))
            return list(self._db.execute("SELECT * FROM outbox ORDER BY id DESC LIMIT ?", (limit,)))

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
    def add_adsb_sample(self, ts: dt.datetime, point: str, airborne: int, total: int, military: int):
        with self._lock:
            self._db.execute("INSERT INTO adsb_samples VALUES (?,?,?,?,?)", (iso(ts), point, airborne, total, military))
            self._db.commit()

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
