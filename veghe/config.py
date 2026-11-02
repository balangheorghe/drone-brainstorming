"""Configurare: fișier TOML (fără secrete) + secrete din variabile de mediu."""

from __future__ import annotations

import logging
import os
import re
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


def read_env_file(path: str) -> dict[str, str]:
    """Citește un fișier .env simplu (CHEIE=valoare). Liniile goale și comentariile se ignoră;
    ghilimelele din jurul valorii și terminațiile Windows (\\r) se scot."""
    out: dict[str, str] = {}
    try:
        with open(path, encoding="utf-8-sig") as f:
            lines = f.read().splitlines()
    except OSError:
        return out
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if k.startswith("export "):
            k = k[7:].strip()
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        out[k] = v
    return out


def load(path: str, env: dict | None = None) -> Config:
    file_env: dict[str, str] = {}
    if env is None:
        # .env de lângă config.toml, citit automat (pornire manuală, WSL); variabilele de mediu au prioritate
        env = os.environ
        file_env = read_env_file(os.path.join(os.path.dirname(os.path.abspath(path)), ".env"))
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    secrets = {k: (env.get(v) or file_env.get(v, "")) for k, v in ENV_SECRETS.items()}
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
        where = "doar pe ntfy" if cfg.secret("ntfy_url") and cfg.secret("ntfy_topic") else "doar în jurnal (consolă)"
        warnings.append(f"TELEGRAM_BOT_TOKEN / TELEGRAM_INTERNAL_CHAT_ID lipsesc → mesajele interne merg {where}")
    if cfg.get("notify", "public_enabled", default=False) and not cfg.secret("telegram_public_chat_id"):
        warnings.append("public_enabled = true, dar TELEGRAM_PUBLIC_CHAT_ID lipsește → canalul public rămâne oprit")
    if cfg.secret("telegram_bot_token") and not cfg.operator_ids:
        warnings.append("TELEGRAM_OPERATOR_IDS gol (opțional) → comenzile /stare, /roalert, /aproba sunt dezactivate; "
                        "alertele interne se trimit oricum")
    for name in ("telegram_internal_chat_id", "telegram_public_chat_id"):
        v = cfg.secret(name)
        if v and not re.fullmatch(r"-?\d+", v):
            warnings.append(f"{name.upper()} = {v[:40]!r} nu e un număr (ex. -1001234567890); verificați .env "
                            f"(fără spații sau comentarii pe același rând)")
    for w in warnings:
        log.warning(w)
    return warnings
