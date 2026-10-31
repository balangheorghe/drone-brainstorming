"""Cereri HTTP minimale (doar biblioteca standard)."""

from __future__ import annotations

import gzip
import json
import urllib.error
import urllib.request
from dataclasses import dataclass

DEFAULT_UA = "veghe/0.1 (avertizare civila drone Iasi; +https://github.com/balangheorghe/drone-brainstorming)"


class HttpError(Exception):
    def __init__(self, status: int, msg: str = "", retry_after: float | None = None):
        super().__init__(f"HTTP {status} {msg}".strip())
        self.status = status
        self.retry_after = retry_after


@dataclass
class Response:
    status: int
    headers: dict
    body: bytes

    def json(self):
        return json.loads(self.body.decode("utf-8"))

    def text(self) -> str:
        ctype = self.headers.get("content-type", "")
        enc = "utf-8"
        if "charset=" in ctype:
            enc = ctype.split("charset=")[-1].split(";")[0].strip() or "utf-8"
        return self.body.decode(enc, errors="replace")


def request(url: str, *, method: str = "GET", headers: dict | None = None, data: bytes | None = None,
            timeout: float = 15, user_agent: str = DEFAULT_UA, max_bytes: int = 5_000_000) -> Response:
    h = {"User-Agent": user_agent, "Accept-Encoding": "gzip"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(max_bytes + 1)
            hdrs = {k.lower(): v for k, v in r.headers.items()}
            status = r.status
    except urllib.error.HTTPError as e:
        hdrs = {k.lower(): v for k, v in (e.headers or {}).items()}
        if e.code == 304:
            return Response(304, hdrs, b"")
        ra = hdrs.get("retry-after")
        try:
            ra_s = float(ra) if ra else None
        except ValueError:
            ra_s = None
        try:
            detail = e.read(300).decode("utf-8", "replace")
        except Exception:
            detail = ""
        raise HttpError(e.code, detail, ra_s) from None
    if len(body) > max_bytes:
        raise HttpError(0, f"raspuns prea mare (> {max_bytes} B)")
    if hdrs.get("content-encoding") == "gzip":
        body = gzip.decompress(body)
    return Response(status, hdrs, body)
