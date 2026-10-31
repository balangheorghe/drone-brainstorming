"""Configurare: fișier TOML (fără secrete) + secrete din variabile de mediu."""

from __future__ import annotations

import logging
import os
import tomllib
from dataclasses import dataclass, field

log = logging.getLogger("veghe.config")

ENV_SECRETS = {
    "alerts_in_ua_token": "ALERTS_IN_UA_TOKEN",
    "ukrainealarm_token": "UKRAINEALARM_TOKEN",
    "telegram_bot_token": "TELEGRAM_BOT_TOKEN",
    "telegram_internal_chat_id": "TELEGRAM_INTERNAL_CHAT_ID",
    "telegram_public_chat_id": "TELEGRAM_PUBLIC_CHAT_ID",
    "telegram_operator_ids": "TELEGRAM_OPERATOR_IDS",
    "ntfy_url": "NTFY_URL",
    "ntfy_topic": "NTFY_TOPIC",
    "ntfy_token": "NTFY_TOKEN",
}


class ConfigError(Exception):
    pass


def num(value, name: str) -> float:
    """Valoare numerică din configurare, cu mesaj clar dacă e greșită (ex. "30" între ghilimele)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError(f"{name} trebuie să fie număr, nu {value!r}")
    if value < 0:
        raise ConfigError(f"{name} nu poate fi negativ")
    return value


@dataclass
class Config:
    raw: dict
    secrets: dict = field(default_factory=dict)

    def get(self, *path, default=None):
        cur = self.raw
        for p in path:
            if not isinstance(cur, dict) or p not in cur:
                return default
            cur = cur[p]
        return cur

    def secret(self, name: str) -> str:
        return (self.secrets.get(name) or "").strip()

    @property
    def operator_ids(self) -> set[int]:
        out = set()
        for x in self.secret("telegram_operator_ids").replace(";", ",").split(","):
            x = x.strip()
            if x.lstrip("-").isdigit():
                out.add(int(x))
        return out


def load(path: str, env: dict | None = None) -> Config:
    env = os.environ if env is None else env
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    secrets = {k: env.get(v, "") for k, v in ENV_SECRETS.items()}
    cfg = Config(raw, secrets)
    validate(cfg)
    return cfg


def validate(cfg: Config) -> list[str]:
    warnings = []
    internal, public = cfg.secret("telegram_internal_chat_id"), cfg.secret("telegram_public_chat_id")
    if internal and public and internal == public:
        raise ConfigError("TELEGRAM_INTERNAL_CHAT_ID și TELEGRAM_PUBLIC_CHAT_ID sunt identice – mesajele interne ar deveni publice")
    if cfg.get("notify", "auto_publish_official", default=False):
        warnings.append("auto_publish_official = true: se aplică doar RO-Alert-urilor înregistrate de operator; presa cere mereu aprobare")
    if cfg.get("sources", "alerts_in_ua", "enabled", default=False) and not cfg.secret("alerts_in_ua_token"):
        warnings.append("alerts_in_ua activat, dar ALERTS_IN_UA_TOKEN lipsește → sursa e dezactivată")
    if cfg.get("sources", "ukrainealarm", "enabled", default=False) and not cfg.secret("ukrainealarm_token"):
        warnings.append("ukrainealarm activat, dar UKRAINEALARM_TOKEN lipsește → sursa e dezactivată")
    if not cfg.secret("telegram_bot_token") or not cfg.secret("telegram_internal_chat_id"):
        warnings.append("TELEGRAM_BOT_TOKEN / TELEGRAM_INTERNAL_CHAT_ID lipsesc → mesajele interne merg doar în jurnal (consolă)")
    if cfg.get("notify", "public_enabled", default=False) and not cfg.secret("telegram_public_chat_id"):
        warnings.append("public_enabled = true, dar TELEGRAM_PUBLIC_CHAT_ID lipsește → canalul public rămâne oprit")
    if cfg.secret("telegram_bot_token") and not cfg.operator_ids:
        warnings.append("TELEGRAM_OPERATOR_IDS lipsește → nimeni nu poate da comenzi (/aproba, /roalert)")
    for w in warnings:
        log.warning(w)
    return warnings
