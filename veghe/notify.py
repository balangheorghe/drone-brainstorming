"""Livrarea mesajelor: coadă (outbox) în SQLite, trimitere pe Telegram / ntfy / consolă,
comenzile operatorului pe Telegram.

Politica publică (verificată aici, nu doar în motor):
- un mesaj public trebuie să fie 'retransmitere' sau 'incetare' și să provină dintr-un rol
  din PUBLIC_SOURCE_ROLES; altfel PublicPolicyError;
- implicit, mesajele publice așteaptă aprobarea unui operator (/aproba N);
- dacă publicul e dezactivat, mesajul se păstrează doar în arhivă.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import threading
import time

from . import http
from .models import PUBLIC_SOURCE_ROLES, Message
from .timeutil import iso, now

log = logging.getLogger("veghe.notify")

PUBLIC_KINDS = {"retransmitere", "incetare"}
TG_MAX = 4000


class PublicPolicyError(Exception):
    pass


class ConsoleSender:
    name = "console"
    min_interval = 0.0

    def send(self, text: str):
        log.info("MESAJ: %s", text)


class TelegramSender:
    def __init__(self, token: str, chat_id: str, api_base: str = "https://api.telegram.org", min_interval: float = 3.1):
        self.name = f"telegram:{chat_id}"
        self.token, self.chat_id, self.api = token, str(chat_id), api_base.rstrip("/")
        self.min_interval = min_interval  # ~20 mesaje/min într-un grup

    def send(self, text: str):
        body = json.dumps({"chat_id": self.chat_id, "text": text[:TG_MAX], "disable_web_page_preview": True}).encode()
        r = http.request(f"{self.api}/bot{self.token}/sendMessage", method="POST", data=body,
                         headers={"Content-Type": "application/json"}, timeout=20)
        if not r.json().get("ok"):
            raise RuntimeError(f"Telegram a refuzat mesajul: {r.body[:200]!r}")


class NtfySender:
    def __init__(self, url: str, topic: str, token: str = ""):
        self.name = f"ntfy:{topic}"
        self.url = url.rstrip("/") + "/" + topic
        self.token = token
        self.min_interval = 1.0

    def send(self, text: str):
        headers = {"Title": "veghe", "Tags": "warning"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        http.request(self.url, method="POST", data=text.encode("utf-8"), headers=headers, timeout=20)


class Dispatcher:
    def __init__(self, store, internal: list, public: list, *, public_enabled: bool = False,
                 auto_publish_official: bool = False, max_attempts: int = 5):
        self.store = store
        self.senders = {"internal": internal, "public": public}
        self.public_enabled = public_enabled and bool(public)
        self.auto_publish = auto_publish_official
        self.max_attempts = max_attempts
        self._last_sent: dict[str, float] = {}
        self._lock = threading.Lock()

    def submit(self, msg: Message) -> int:
        if msg.channel == "internal":
            return self.store.enqueue("internal", msg.kind, msg.text, "queued", msg.origin_role)
        if msg.channel != "public":
            raise ValueError(f"canal necunoscut: {msg.channel}")
        if msg.kind not in PUBLIC_KINDS or msg.origin_role not in PUBLIC_SOURCE_ROLES:
            raise PublicPolicyError(f"mesaj public interzis: tip={msg.kind} rol={msg.origin_role}")
        if not self.public_enabled:
            return self.store.enqueue("public", msg.kind, msg.text, "disabled", msg.origin_role)
        status = "queued" if self.auto_publish else "pending_approval"
        oid = self.store.enqueue("public", msg.kind, msg.text, status, msg.origin_role)
        if status == "pending_approval":
            self.store.enqueue("internal", "aprobare", f"[INTERN] Mesaj public în așteptare #{oid}. "
                               f"Aprobați cu /aproba {oid} sau respingeți cu /respinge {oid}.\n—\n{msg.text}", "queued")
        return oid

    def approve(self, oid: int, by: str) -> str:
        row = self.store.get_outbox(oid)
        if row is None or row["channel"] != "public":
            return f"Nu există mesajul public #{oid}."
        if row["status"] != "pending_approval":
            return f"Mesajul #{oid} are starea „{row['status']}”, nu poate fi aprobat."
        self.store.set_outbox(oid, status="queued", approved_by=by)
        return f"Mesajul #{oid} a fost aprobat și pus la trimis."

    def reject(self, oid: int, by: str) -> str:
        row = self.store.get_outbox(oid)
        if row is None or row["status"] != "pending_approval":
            return f"Mesajul #{oid} nu e în așteptare."
        self.store.set_outbox(oid, status="rejected", approved_by=by)
        return f"Mesajul #{oid} a fost respins."

    def flush(self) -> int:
        """Trimite ce e în coadă. Întoarce numărul de mesaje trimise."""
        sent = 0
        with self._lock:
            for row in self.store.outbox("queued", limit=50):
                senders = self.senders.get(row["channel"]) or []
                if row["channel"] == "public" and not self.public_enabled:
                    self.store.set_outbox(row["id"], status="disabled")
                    continue
                errors = []
                for s in senders:
                    wait = s.min_interval - (time.monotonic() - self._last_sent.get(s.name, 0))
                    if wait > 0:
                        time.sleep(min(wait, 5))
                    try:
                        s.send(row["text"])
                        self._last_sent[s.name] = time.monotonic()
                    except Exception as e:  # noqa: BLE001 - orice eroare de rețea
                        errors.append(f"{s.name}: {e}")
                attempts = (row["attempts"] or 0) + 1
                if errors and len(errors) == len(senders):
                    status = "failed" if attempts >= self.max_attempts else "queued"
                    self.store.set_outbox(row["id"], attempts=attempts, error="; ".join(errors)[:500], status=status)
                    log.warning("trimitere eșuată #%s: %s", row["id"], errors)
                    continue  # reîncercăm la ciclul următor
                self.store.set_outbox(row["id"], status="sent", sent_at=iso(now()), attempts=attempts,
                                      error="; ".join(errors)[:500] or None)
                sent += 1
        return sent


class TelegramCommands:
    """Comenzi de la operatori (doar ID-uri autorizate), prin getUpdates (long polling)."""

    def __init__(self, token: str, operators: set[int], handler, api_base: str = "https://api.telegram.org", store=None):
        self.token, self.api = token, api_base.rstrip("/")
        self.operators = operators
        self.handler = handler  # handler(cmd, args, user_id) -> str
        self.store = store
        self.offset = int(store.kv_get("tg_offset", "0")) if store else 0

    def _call(self, method: str, payload: dict, timeout: float = 35):
        r = http.request(f"{self.api}/bot{self.token}/{method}", method="POST", data=json.dumps(payload).encode(),
                         headers={"Content-Type": "application/json"}, timeout=timeout)
        return r.json()

    def poll_once(self, long_poll: int = 25) -> int:
        data = self._call("getUpdates", {"offset": self.offset, "timeout": long_poll, "allowed_updates": ["message"]},
                          timeout=long_poll + 10)
        handled = 0
        for upd in data.get("result") or []:
            self.offset = max(self.offset, int(upd["update_id"]) + 1)
            msg = upd.get("message") or {}
            text = (msg.get("text") or "").strip()
            uid = (msg.get("from") or {}).get("id")
            chat = (msg.get("chat") or {}).get("id")
            if not text.startswith("/") or uid not in self.operators:
                continue
            parts = text.split()
            cmd = parts[0].split("@")[0].lower()
            try:
                reply = self.handler(cmd, parts[1:], uid)
            except Exception as e:  # noqa: BLE001
                reply = f"Eroare: {e}"
            if reply:
                self._call("sendMessage", {"chat_id": chat, "text": reply[:TG_MAX], "disable_web_page_preview": True})
            handled += 1
        if self.store:
            self.store.kv_set("tg_offset", str(self.offset))
        return handled


def parse_hhmm(s: str, ref: dt.datetime) -> dt.datetime:
    """'17:04' → momentul de azi (ora României) în UTC."""
    from .timeutil import to_local

    h, m = (int(x) for x in s.split(":"))
    loc = to_local(ref).replace(hour=h, minute=m, second=0, microsecond=0)
    if loc > to_local(ref) + dt.timedelta(minutes=5):
        loc -= dt.timedelta(days=1)
    return loc.astimezone(dt.timezone.utc)
