"""Timp: totul se stochează în UTC; afișarea e în ora României."""

from __future__ import annotations

import datetime as dt

UTC = dt.timezone.utc

try:  # imaginea Docker instalează tzdata; aici avem și o rezervă fără ea
    from zoneinfo import ZoneInfo

    _RO = ZoneInfo("Europe/Bucharest")
except Exception:  # pragma: no cover - doar când lipsește tzdata
    _RO = None

RO_TZ = _RO


def now() -> dt.datetime:
    return dt.datetime.now(UTC)


def _last_sunday(year: int, month: int) -> dt.date:
    d = dt.date(year, month + 1, 1) - dt.timedelta(days=1) if month < 12 else dt.date(year, 12, 31)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def _ro_offset(t: dt.datetime) -> dt.timedelta:
    """Regula UE: ora de vară de la ultima duminică din martie 01:00 UTC
    până la ultima duminică din octombrie 01:00 UTC."""
    start = dt.datetime.combine(_last_sunday(t.year, 3), dt.time(1), UTC)
    end = dt.datetime.combine(_last_sunday(t.year, 10), dt.time(1), UTC)
    return dt.timedelta(hours=3 if start <= t < end else 2)


def to_local(t: dt.datetime) -> dt.datetime:
    if t.tzinfo is None:
        t = t.replace(tzinfo=UTC)
    if _RO is not None:
        return t.astimezone(_RO)
    off = _ro_offset(t.astimezone(UTC))
    return t.astimezone(dt.timezone(off))


def hhmm(t: dt.datetime | None) -> str:
    if t is None:
        return "--:--"
    loc = to_local(t)
    name = "EEST" if loc.utcoffset() == dt.timedelta(hours=3) else "EET"
    return f"{loc:%H:%M} {name}"


def parse_iso(s: str | None) -> dt.datetime | None:
    if not s:
        return None
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        t = dt.datetime.fromisoformat(s)
    except ValueError:
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=UTC)
    return t.astimezone(UTC)


def iso(t: dt.datetime | None) -> str | None:
    return t.astimezone(UTC).isoformat() if t else None
