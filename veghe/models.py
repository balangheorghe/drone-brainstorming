"""Structuri de date comune."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from dataclasses import dataclass, field
from enum import IntEnum

from .nlp import normalize

# Rolul unei surse determină ce reguli i se aplică.
ROLES = {
    "ua_alert_state",   # starea alertelor UA (API) – vigilență
    "ua_alerts",        # canal Telegram cu alerte UA (ex. air_alert_ua) – vigilență
    "ua_direction",     # Forțele Aeriene UA / monitorizare – direcții (DOAR INTERN)
    "ua_official",      # administrații regionale UA (OVA/RVA) – context (DOAR INTERN)
    "md_official",      # MA al R. Moldova / Moldpres – detecții, restricții
    "md_news",          # presa din R. Moldova
    "ro_official_news", # MApN / presa din România (RO-Alert, încetare)
    "adsb",             # trafic aerian civil (doar numărători)
    "manual",           # înregistrări ale operatorului (ex. RO-Alert primit)
}

# Rolurile din care se poate construi un mesaj PUBLIC (retransmitere oficială).
PUBLIC_SOURCE_ROLES = {"ro_official_news", "manual"}


class Level(IntEnum):
    FOND = 0
    VIGILENTA = 1
    DIRECTIE = 2
    MOLDOVA = 3
    APROPIERE = 4
    OFICIAL = 5
    INCHEIAT = 6


LEVEL_RO = {
    Level.FOND: "fond",
    Level.VIGILENTA: "vigilență",
    Level.DIRECTIE: "direcție",
    Level.MOLDOVA: "Moldova",
    Level.APROPIERE: "apropiere",
    Level.OFICIAL: "oficial",
    Level.INCHEIAT: "încheiat",
}


@dataclass
class Signal:
    source: str
    role: str
    text: str
    received_at: dt.datetime
    published_at: dt.datetime | None = None
    url: str = ""
    ext_id: str = ""
    meta: dict = field(default_factory=dict)

    def key(self) -> str:
        if self.ext_id:
            base = f"{self.source}|{self.ext_id}"
        else:
            base = f"{self.source}|{normalize(self.text)}|{json.dumps(self.meta, sort_keys=True, ensure_ascii=False)}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()[:32]

    @property
    def when(self) -> dt.datetime:
        return self.published_at or self.received_at


@dataclass
class Message:
    """Un mesaj produs de motor. channel: 'internal' sau 'public'."""

    channel: str
    kind: str
    text: str
    level: Level = Level.FOND
    hypothesis: int | None = None
    origin_role: str = ""
