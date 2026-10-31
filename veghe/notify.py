"""Livrarea mesajelor: coadă (outbox) în SQLite, trimitere pe Telegram / ntfy / consolă,
comenzile operatorului pe Telegram.

Politica publică (verificată aici, nu doar în motor):
- un mesaj public trebuie să fie 'retransmitere' sau 'incetare' și să provină dintr-un rol
  din PUBLIC_SOURCE_ROLES; altfel PublicPolicyError;
- implicit, mesajele publice așteaptă aprobarea unui operator (/aproba N) și expiră;
- publicarea automată e permisă doar pentru înregistrările operatorului (rol 'manual');
- dacă publicul e oprit, mesajul se păstrează doar în arhivă.

Livrare: fiecare destinatar (Telegram, ntfy) e urmărit separat; un mesaj e „trimis” doar
când toți destinatarii reali l-au primit. Consola e doar jurnal și nu contează.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import threading
import time

from . import http
from .models import PUBLIC_SOURCE_ROLES, Message
from .timeutil import iso, now, parse_iso

log = logging.getLogger("veghe.notify")

PUBLIC_KINDS = {"retransmitere", "incetare"}
TG_MAX = 4000
PENDING_TTL = dt.timedelta(minutes=30)
MAX_ATTEMPTS = 8


class PublicPolicyError(Exception):
    pass


class ConsoleSender:
    name = "console"
    min_interval = 0.0
    optional = True  # doar jurnal: nu decide dacă mesajul a ajuns

    def send(self, text: str):
        log.info("MESAJ: %s", text)


class TelegramSender:
    optional = False

    def __init__(self, token: str, chat_id: str, api_base: str = "https://api.telegram.org", min_interval: float = 3.1):
        self.name = f"telegram:{chat_id}"
        self.token, self.chat_id, self.api = token, str(chat_id), api_base.rstrip("/")
        self.min_interval = min_interval  # ~20 mesaje/min într-un grup

    def send(self, text: str):
        body = json.dumps({"chat_id": self.chat_id, "text": text[:TG_MAX], "disable_web_page_preview": True}).encode()
        r = http.request(f"{self.api}/bot{self.token}/sendMessage", method="POST", data=body,
                         headers={"Content-Type": "application/json"}, timeout=20)
        if not r.json().get("ok"):
            raise RuntimeError("Telegram a refuzat mesajul")

    def check_private(self) -> str | None:
        """Întoarce un motiv de refuz dacă chatul NU e un grup privat."""
        r = http.request(f"{self.api}/bot{self.token}/getChat", method="POST",
                         data=json.dumps({"chat_id": self.chat_id}).encode(),
                         headers={"Content-Type": "application/json"}, timeout=20)
        res = r.json().get("result") or {}
        if res.get("type") == "private":
            return None  # chat 1:1 cu un operator; @username e al persoanei, nu un nume public de grup
        if res.get("type") == "channel":
            return "chatul intern e un CANAL (public sau nu); folosiți un grup privat"
        if res.get("username"):
            return f"chatul intern are nume public (@{res['username']}); folosiți un grup privat"
        return None


class NtfySender:
    optional = False

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
                 auto_publish_official: bool = False, max_attempts: int = MAX_ATTEMPTS):
        self.store = store
        self.senders = {"internal": internal, "public": public}
        self.public_enabled = public_enabled and bool(public)
        self.auto_publish = auto_publish_official
        self.max_attempts = max_attempts
        self._last_sent: dict[str, float] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ intrare
    def submit(self, msg: Message) -> int:
        if msg.channel == "internal":
            return self.store.enqueue("internal", msg.kind, msg.text, "queued", msg.origin_role)
        if msg.channel != "public":
            raise ValueError(f"canal necunoscut: {msg.channel}")
        if msg.kind not in PUBLIC_KINDS or msg.origin_role not in PUBLIC_SOURCE_ROLES:
            raise PublicPolicyError(f"mesaj public interzis: tip={msg.kind} rol={msg.origin_role}")
        if not self.public_enabled:
            return self.store.enqueue("public", msg.kind, msg.text, "disabled", msg.origin_role)
        # Publicare automată doar pentru RO-Alert-uri înregistrate de operator; presa → mereu aprobare.
        auto = self.auto_publish and msg.origin_role == "manual" and msg.kind == "retransmitere"
        status = "queued" if auto else "pending_approval"
        oid = self.store.enqueue("public", msg.kind, msg.text, status, msg.origin_role)
        if status == "pending_approval":
            self.store.enqueue("internal", "aprobare", f"[INTERN] Mesaj public în așteptare #{oid} "
                               f"(expiră în {PENDING_TTL.seconds // 60} min). Aprobați cu /aproba {oid} sau "
                               f"respingeți cu /respinge {oid}.\n—\n{msg.text}", "queued")
        return oid

    def approve(self, oid: int, by: str) -> str:
        self.expire_pending()
        row = self.store.get_outbox(oid)
        if row is None or row["channel"] != "public":
            return f"Nu există mesajul public #{oid}."
        # compare-and-set: nu aprobăm un mesaj care tocmai a expirat sau a fost respins
        ok = self.store.cas_outbox(oid, "pending_approval", "AND created_at > ?", (iso(now() - PENDING_TTL),),
                                   status="queued", approved_by=by)
        if not ok:
            row = self.store.get_outbox(oid)
            return f"Mesajul #{oid} are starea „{row['status']}”, nu poate fi aprobat."
        return f"Mesajul #{oid} a fost aprobat și pus la trimis."

    def reject(self, oid: int, by: str) -> str:
        if not self.store.cas_outbox(oid, "pending_approval", status="rejected", approved_by=by):
            return f"Mesajul #{oid} nu e în așteptare."
        return f"Mesajul #{oid} a fost respins."

    def expire_pending(self) -> int:
        n = 0
        for row in self.store.outbox("pending_approval", limit=200):
            created = parse_iso(row["created_at"])
            if created and now() - created > PENDING_TTL:
                n += self.store.cas_outbox(row["id"], "pending_approval", status="expired")
        return n

    # ------------------------------------------------------------------ trimitere
    def flush(self) -> int:
        """Trimite ce e în coadă și e scadent. Întoarce numărul de mesaje complet livrate."""
        sent = 0
        t = now()
        with self._lock:
            self.expire_pending()
            for row in self.store.outbox_due(t, limit=50):
                if row["channel"] == "public" and not self.public_enabled:
                    self.store.set_outbox(row["id"], status="disabled")
                    continue
                senders = self.senders.get(row["channel"]) or []
                delivered = set(filter(None, (row["delivered"] or "").split(",")))
                first_try = not row["attempts"]
                errors, retry_after, ambiguous = [], None, False
                for s in senders:
                    if s.name in delivered or (getattr(s, "optional", False) and not first_try):
                        continue
                    wait = s.min_interval - (time.monotonic() - self._last_sent.get(s.name, 0))
                    if wait > 0:
                        time.sleep(min(wait, 5))
                    try:
                        s.send(row["text"])
                        self._last_sent[s.name] = time.monotonic()
                        if not getattr(s, "optional", False):
                            delivered.add(s.name)
                    except Exception as e:  # noqa: BLE001 - orice eroare de rețea
                        code = f" {e.status}" if isinstance(e, http.HttpError) else ""
                        errors.append(f"{s.name}: {type(e).__name__}{code}")
                        if isinstance(e, http.HttpError) and e.retry_after:
                            retry_after = max(retry_after or 0, e.retry_after)
                        # fără răspuns de la server (timeout etc.): mesajul poate să fi plecat deja
                        if not isinstance(e, http.HttpError):
                            ambiguous = True
                required = {s.name for s in senders if not getattr(s, "optional", False)}
                attempts = (row["attempts"] or 0) + 1
                fields = {"attempts": attempts, "delivered": ",".join(sorted(delivered)), "error": "; ".join(errors)[:500] or None}
                if required <= delivered:
                    self.store.set_outbox(row["id"], status="sent", sent_at=iso(now()), **fields)
                    sent += 1
                elif row["channel"] == "public" and ambiguous:
                    # nu reîncercăm automat un mesaj public care poate fi deja publicat (ar apărea de două ori)
                    self.store.set_outbox(row["id"], status="unknown", **fields)
                    self.store.enqueue("internal", "esec", f"[INTERN] Mesajul public #{row['id']} are stare NECUNOSCUTĂ "
                                       f"(fără răspuns de la Telegram). Verificați canalul public; NU s-a reîncercat automat.",
                                       "queued")
                elif attempts >= self.max_attempts:
                    self.store.set_outbox(row["id"], status="failed", **fields)
                    log.error("mesajul #%s nu a putut fi livrat: %s", row["id"], errors)
                    if row["channel"] == "public":
                        self.store.enqueue("internal", "esec", f"[INTERN] Mesajul public #{row['id']} NU a putut fi "
                                           f"trimis după {attempts} încercări ({'; '.join(errors)}).", "queued")
                else:
                    delay = max(retry_after or 0, min(15 * 2 ** (attempts - 1), 600))
                    fields["next_attempt_at"] = iso(now() + dt.timedelta(seconds=delay))
                    self.store.set_outbox(row["id"], **fields)
                    log.warning("livrare parțială/eșuată #%s (%s); reîncercare în %.0f s", row["id"], errors, delay)
        return sent


class TelegramCommands:
    """Comenzi de la operatori, prin getUpdates (long polling).

    Acceptă doar: utilizatori din `operators`, scriind în grupul intern sau în chat privat cu botul.
    Comenzile mai vechi de MAX_AGE (bot oprit între timp) sunt ignorate.
    """

    MAX_AGE = dt.timedelta(minutes=10)

    def __init__(self, token: str, operators: set[int], handler, api_base: str = "https://api.telegram.org",
                 store=None, internal_chat_id: str | None = None):
        self.token, self.api = token, api_base.rstrip("/")
        self.operators = operators
        self.handler = handler  # handler(cmd, args, user_id, sent_at) -> str
        self.store = store
        self.internal_chat = str(internal_chat_id) if internal_chat_id else None
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
            if not (str(chat) == self.internal_chat or chat == uid):
                log.warning("comandă ignorată: chat %s nu e grupul intern sau un chat privat", chat)
                continue
            sent_at = dt.datetime.fromtimestamp(msg["date"], dt.timezone.utc) if msg.get("date") else now()
            if now() - sent_at > self.MAX_AGE:
                log.warning("comandă veche ignorată: %s (%s)", text, sent_at)
                continue
            parts = text.split()
            cmd = parts[0].split("@")[0].lower()
            try:
                reply = self.handler(cmd, parts[1:], uid, sent_at)
            except Exception as e:  # noqa: BLE001
                reply = f"Eroare: {type(e).__name__}"
            if reply:
                self._call("sendMessage", {"chat_id": chat, "text": reply[:TG_MAX], "disable_web_page_preview": True})
            handled += 1
        if self.store:
            self.store.kv_set("tg_offset", str(self.offset))
        return handled


def parse_hhmm(s: str, ref: dt.datetime) -> dt.datetime:
    """'17:04' → momentul de azi (ora României) în UTC; dacă e în viitor, e de ieri."""
    from .timeutil import to_local

    h, m = (int(x) for x in s.split(":"))
    if not (0 <= h < 24 and 0 <= m < 60):
        raise ValueError("oră invalidă")
    loc = to_local(ref).replace(hour=h, minute=m, second=0, microsecond=0)
    if loc > to_local(ref) + dt.timedelta(minutes=5):
        loc -= dt.timedelta(days=1)
    return loc.astimezone(dt.timezone.utc)
