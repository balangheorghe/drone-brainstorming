"""Construirea semnalului „RO-Alert înregistrat de operator” (folosit de Telegram și CLI)."""

from __future__ import annotations

import datetime as dt

from .models import Signal
from .timeutil import iso, now


def manual_roalert_signal(county: str, at: dt.datetime, who: str) -> Signal:
    return Signal(source=who, role="manual", received_at=now(), published_at=at,
                  text=f"RO-Alert (dronă, spațiu aerian) primit în județul {county[:40]} – înregistrat de operator",
                  ext_id=f"roalert|{county[:40]}|{iso(at)}")
