"""Motorul de reguli: transformă semnalele în stări și mesaje.

Niveluri (docs/07): VIGILENȚĂ (alertă UA în zonele urmărite) → DIRECȚIE (mesaj UA despre
drone spre Moldova/zonele de graniță) → MOLDOVA (detecție anunțată în R. Moldova) →
APROPIERE (poziție la ≤ approach_km de Iași, spre vest). Separat: OFICIAL (RO-Alert raportat).

Reguli de siguranță „prin construcție”:
- mesajele PUBLICE se creează doar din semnale cu rol în PUBLIC_SOURCE_ROLES
  (presă/comunicate românești sau operatorul), doar ca retransmitere sau încetare, și
  dintr-un șablon fix (fără textul articolului);
- conținutul canalelor ucrainene nu ajunge niciodată într-un mesaj public;
- semnalele prea vechi se arhivează, dar nu declanșează nimic.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import re
import statistics
import urllib.parse
from dataclasses import dataclass, field

from . import geo
from .models import LEVEL_RO, PUBLIC_SOURCE_ROLES, Level, Message, Signal
from .nlp import analyze, normalize
from .timeutil import hhmm, iso, parse_iso

log = logging.getLogger("veghe.engine")

def _maneuver_text(x: dict) -> str:
    kind = "așteptare" if x.get("kind") == "asteptare" else "întoarcere"
    alt = f", ~{x['alt_ft']} ft" if x.get("alt_ft") is not None else ""
    return f"{kind} ~{x['dist_km']:.0f} km {x.get('bearing') or ''}".rstrip() + alt


NOTAM_CAT_RO = {
    "spatiu_aerian_inchis": "spațiu aerian închis",
    "restrictie_spatiu_aerian": "restricție de spațiu aerian",
    "drone_uas": "zboruri UAS / drone",
    "aeroport_inchis": "aeroport închis",
    "ruta_inchisa": "rută ATS închisă",
    "gnss": "GNSS indisponibil / interferențe",
    "restrictie_ridicata": "restricție ridicată",
}

NEW_DRONE_MARKERS = ("a doua drona", "o noua drona", "o alta drona", "inca o drona", "другий", "ще один", "второй", "еще один")
# Locuri din UA relevante (vestul reg. Odesa, Vinnytsia de lângă MD, Cernăuți)
UA_WATCH_KEYS = {"podilsk", "rozdilna", "izmail", "reni", "bolhrad", "bilhorod", "vylkove", "mohyliv",
                 "tulchyn", "chernivtsi", "novodnistrovsk", "vinnytsia"}
PRUT_EDGE_KEYS = {"ungheni", "sculeni", "zagarancea", "lipcani", "giurgiulesti", "leova", "cahul", "briceni"}
NEWS_ROLES = {"md_news", "md_official", "ro_official_news"}

# Canalul air_alert_ua: „🔴 16:12 Повітряна тривога в Подільський район.” / „🟢 Відбій тривоги в …”
TG_ON = re.compile(r"(?:повітрян\w* тривог\w*|тривога ще триває)\s+(?:в|у)\s+([^\.\n#!]+)")
TG_OFF = re.compile(r"відбій\s+(?:повітрян\w* )?тривог\w*\s+(?:в|у)\s+([^\.\n#!]+)")


@dataclass
class EngineConfig:
    watch_oblasts: list[str]
    watch_raions: list[str]
    watch_counties: list[str] = field(default_factory=lambda: ["Iași", "Botoșani", "Suceava", "Neamț", "Vaslui", "Bacău"])
    max_age_min: float = 30
    max_age_news_min: float = 60
    ttl_min: float = 45
    approach_km: float = 120
    vigilance_quiet_min: float = 20
    official_repeat_min: float = 60
    tg_alert_ttl_min: float = 90
    state_stale_min: float = 10
    target: geo.Place = geo.IASI


@dataclass
class Hypothesis:
    id: int
    created: dt.datetime
    updated: dt.datetime
    level: Level
    place: geo.Place | None = None
    origin: list[geo.Place] = field(default_factory=list)
    jet: bool = False
    official: bool = False
    from_new_marker: bool = False
    notified: Level = Level.FOND
    last_msg_at: dt.datetime | None = None
    last_msg_place: str = ""
    sources: list[str] = field(default_factory=list)
    closed: bool = False


def _domain(url: str) -> str:
    try:
        host = urllib.parse.urlparse(url).hostname or ""
    except ValueError:
        host = ""
    return host.removeprefix("www.")


class Engine:
    def __init__(self, cfg: EngineConfig, store=None):
        self.cfg = cfg
        self.store = store
        self.ua_state: dict[str, list[dict]] = {}
        self.ua_state_alive: dict[str, dt.datetime] = {}
        self.ua_tg_state: dict[str, dt.datetime] = {}
        self.vigilance_since: dt.datetime | None = None
        self.vigilance_msg_at: dt.datetime | None = None
        self.vigilance_titles: set[str] = set()
        self.hyps: list[Hypothesis] = []
        self._next_id = int(store.kv_get("next_hypothesis_id", "1")) if store else 1
        self.last_official: dict[str, dt.datetime] = {}
        self.last_end: dict[str, dt.datetime] = {}
        # momentul (după data semnalului) ultimei alerte / încetări pe județ – contra știrilor întârziate
        self.alerted_at: dict[str, dt.datetime] = {}
        self.ended_at: dict[str, dt.datetime] = {}
        self.adsb_anomaly: dict[str, bool] = {}
        # ADS-B (doar agregate pe zonă; nimic despre aeronave individuale)
        self.adsb_view: dict[str, dict] = {}
        self.adsb_reduced: dict[str, bool] = {}
        self.adsb_low_streak: dict[str, int] = {}
        self.adsb_outage: dict[str, bool] = {}
        self.adsb_last_msg: dict[tuple, dt.datetime] = {}
        self.adsb_gnss_sent: dict[str, list[dt.datetime]] = {}
        self.adsb_gnss_started: set[str] = set()
        self.adsb_maneuver_sent_n: dict[str, int] = {}
        self.military: dict | None = None
        self.military_at: dt.datetime | None = None
        self.military_announced = 0
        self.military_msg_at: dt.datetime | None = None
        self.military_zero_since: dt.datetime | None = None
        self.adsb_ok_streak: dict[tuple, int] = {}
        # NOTAM (context oficial; nu ridică singur nivelul)
        self.notam_active: dict[str, dict] = {}
        self.notam_pending: list[dict] = []
        self.notam_last_msg: dt.datetime | None = None
        self.clock_skew_warned = False
        self._watch_titles = list(cfg.watch_oblasts) + list(cfg.watch_raions)
        self._watch_norm = {normalize(t): t for t in self._watch_titles}
        if store is not None:
            self._restore_notams()

    # ------------------------------------------------------------------ utilitare
    def _event(self, level, hyp, kind, text, now):
        if self.store:
            self.store.add_event(level, hyp, kind, text, now)

    def _new_hyp(self, now, level, from_new_marker=False) -> Hypothesis:
        h = Hypothesis(id=self._next_id, created=now, updated=now, level=level, from_new_marker=from_new_marker)
        self._next_id += 1
        if self.store:
            self.store.kv_set("next_hypothesis_id", str(self._next_id))
        self.hyps.append(h)
        return h

    def open_hyps(self) -> list[Hypothesis]:
        return [h for h in self.hyps if not h.closed]

    def _eta_text(self, p: geo.Place) -> str:
        d_t = geo.dist(p, self.cfg.target)
        a, b = geo.eta_minutes(d_t)
        if p.country == "RO":
            return f"{p.name}: {d_t:.0f} km de {self.cfg.target.name}"
        d_p = geo.dist_to_prut_km(p)
        pa, pb = geo.eta_minutes(d_p)
        return (f"{p.name}: ~{d_t:.0f} km de {self.cfg.target.name}. ETA Prut {pa}–{pb} min, "
                f"{self.cfg.target.name} {a}–{b} min (linie dreaptă, 450/150 km/h)")

    def _fresh(self, point: str, now) -> bool:
        """Starea ADS-B a zonei e folosită în note doar dacă e recentă (≤ 5 min)."""
        t = (self.adsb_view.get(point) or {}).get("la_ok")  # ultima citire cu date bune
        return now is None or (t is not None and now - t <= dt.timedelta(minutes=5))

    def _adsb_note(self, now=None) -> str:
        notes = []
        pts = [k for k, v in self.adsb_anomaly.items() if v and self._fresh(k, now)]
        if pts:
            notes.append(f"ADS-B: trafic civil oprit în jurul {', '.join(pts)}.")
        red = [k for k, v in self.adsb_reduced.items() if v and not self.adsb_anomaly.get(k) and self._fresh(k, now)]
        if red:
            notes.append(f"ADS-B: trafic civil mult redus (posibil ocolit) în jurul {', '.join(red)}.")
        gn = [k for k in sorted(self.adsb_gnss_started) if self._fresh(k, now)]
        if gn:
            notes.append(f"GNSS degradat în jurul {', '.join(gn)}.")
        man = [f"{k} ({v.get('manevre', 0)})" for k, v in self.adsb_view.items()
               if v.get("manevre", 0) >= 2 and self._fresh(k, now)]
        if man:
            notes.append(f"Avioane civile în așteptare/întoarse: {', '.join(man)}.")
        mil_fresh = self.military and (now is None or (self.military_at and now - self.military_at <= dt.timedelta(minutes=5)))
        if mil_fresh and self.military.get("trigger", 0):
            # doar numere, fără poziții; marcajul permite înlocuirea notei în arhivă după livrare
            notes.append(f"ADS-B militar (NU REDISTRIBUIȚI): {self.military.get('numere')} (detalii în /stare).")
        closed = [m for m in self.notam_active.values()
                  if m.get("category") in ("spatiu_aerian_inchis", "drone_uas") and (m.get("near") or m.get("fir") == "LUUU")
                  and (now is None or not parse_iso(m.get("start")) or parse_iso(m.get("start")) <= now)]
        if closed:
            notes.append("NOTAM activ: " + "; ".join(f"{m.get('id')} {NOTAM_CAT_RO.get(m.get('category'), m.get('category'))}"
                                                    for m in closed[:3]) + ".")
        return (" " + " ".join(notes)) if notes else ""

    @staticmethod
    def _excerpt(text: str, n: int = 220) -> str:
        t = " ".join(text.split())
        return t if len(t) <= n else t[: n - 1] + "…"

    # ------------------------------------------------------------------ vigilență
    def source_alive(self, source: str, now: dt.datetime):
        """Apelat la fiecare citire reușită a unei surse de stare (chiar dacă starea nu s-a schimbat)."""
        self.ua_state_alive[source] = now

    def _active_titles(self, now) -> set[str]:
        stale = dt.timedelta(minutes=self.cfg.state_stale_min)
        titles = {a["title"] for src, lst in self.ua_state.items()
                  if now - self.ua_state_alive.get(src, now) <= stale for a in lst}
        ttl = dt.timedelta(minutes=self.cfg.tg_alert_ttl_min)
        titles |= {t for t, at in self.ua_tg_state.items() if now - at <= ttl}
        return titles

    def _drone_threat(self) -> bool:
        return any("drones" in a.get("threats", []) for lst in self.ua_state.values() for a in lst)

    def _update_vigilance(self, now) -> list[Message]:
        active = self._active_titles(now)
        msgs = []
        if active and self.vigilance_since is None:
            self.vigilance_since = now
            self._event(Level.VIGILENTA, None, "vigilenta_start", ", ".join(sorted(active)), now)
        if not active and self.vigilance_since is not None:
            self._event(Level.FOND, None, "vigilenta_stop", "", now)
            self.vigilance_since = None
            self.vigilance_titles = set()
            return msgs
        new = active - self.vigilance_titles
        quiet = dt.timedelta(minutes=self.cfg.vigilance_quiet_min)
        if active and new and (self.vigilance_msg_at is None or now - self.vigilance_msg_at >= quiet):
            pts = [geo.BY_KEY[k] for k in {geo.UA_AREA_POINT.get(t) for t in active} if k in geo.BY_KEY]
            near = min(pts, key=lambda p: geo.dist(p, self.cfg.target)) if pts else None
            eta = ""
            if near:
                a, b = geo.eta_minutes(geo.dist(near, self.cfg.target))
                eta = f" Dacă o dronă ar veni de acolo spre {self.cfg.target.name}: ~{a}–{b} min (linie dreaptă)."
            threat = " Tip amenințare raportat: drone." if self._drone_threat() else ""
            text = (f"[INTERN] VIGILENȚĂ · {hhmm(now)}. Alertă aeriană activă în: {', '.join(sorted(active))}.{threat}{eta}"
                    f"{self._adsb_note(now)} Stare internă, nespecifică (filtrul e activ ~20% din timp). Nicio acțiune publică.")
            msgs.append(Message("internal", "vigilenta", text, Level.VIGILENTA))
            self.vigilance_msg_at = now
        self.vigilance_titles = set(active)
        return msgs

    def _tg_alert(self, sig: Signal, now) -> list[Message]:
        # pe linii: normalize() ar transforma rândurile noi în spații și ar lipi rândul următor de localitate
        n = "\n".join(normalize(line) for line in sig.text.splitlines())
        for rx, on in ((TG_OFF, False), (TG_ON, True)):
            for m in rx.finditer(n):
                for loc in re.split(r",| та | і ", m.group(1)):
                    title = self._watch_norm.get(loc.strip(" .:;"))
                    if not title:
                        continue
                    if on:
                        self.ua_tg_state[title] = sig.when
                    else:
                        self.ua_tg_state.pop(title, None)
        return self._update_vigilance(now)

    # ------------------------------------------------------------------ ipoteze
    def _match_hyp(self, place: geo.Place | None, now, new_marker: bool) -> Hypothesis | None:
        best = None
        for h in self.open_hyps():
            # „a doua / o altă dronă”: doar la o ipoteză deschisă tot de un astfel de mesaj, recent
            if new_marker and not (h.from_new_marker and now - h.created <= dt.timedelta(minutes=20)):
                continue
            if place is not None and h.place is not None:
                hours = max((now - h.updated).total_seconds() / 3600, 0.05)
                if geo.dist(place, h.place) > geo.V_JET_KMH * hours + 80:
                    continue
            if best is None or h.updated > best.updated:
                best = h
        return best

    def _hyp_message(self, h: Hypothesis, kind: str, sig: Signal, now) -> list[Message]:
        place_key = h.place.key if h.place else ""
        changed = h.level > h.notified or place_key != h.last_msg_place
        recent = h.last_msg_at is not None and now - h.last_msg_at < dt.timedelta(minutes=3)
        if not changed or (recent and h.level <= h.notified):
            return []
        pos = self._eta_text(h.place) if h.place else "poziție nepublicată"
        jet = " (posibil cu reacție)" if h.jet else ""
        src = f"{sig.source} {sig.url}".strip()
        off = " RO-Alert deja raportat." if h.official else ""
        if kind == "directie":
            text = (f"[INTERN – NU REDISTRIBUIȚI] DIRECȚIE · {hhmm(now)} · H-{h.id}. Sursă UA: drone{jet} spre zona de graniță. "
                    f"{pos}. Text: «{self._excerpt(sig.text)}» ({src}){self._adsb_note(now)}")
        elif kind == "moldova":
            text = (f"[INTERN] ATENȚIE · {hhmm(now)} · H-{h.id}. R. Moldova: dronă{jet} semnalată. {pos}. "
                    f"«{self._excerpt(sig.text)}» ({src}).{off}{self._adsb_note(now)} Un RO-Alert poate urma.")
        else:  # apropiere
            text = (f"[INTERN] APROPIERE · {hhmm(now)} · H-{h.id}. Dronă{jet} aproape de Prut / {self.cfg.target.name}. {pos}. "
                    f"«{self._excerpt(sig.text)}» ({src}).{off}{self._adsb_note(now)} "
                    f"Dacă nu există încă RO-Alert, contactați ISU conform protocolului.")
        h.notified = max(h.notified, h.level)
        h.last_msg_at = now
        h.last_msg_place = place_key
        return [Message("internal", kind, text, h.level, h.id, sig.role)]

    def _ua_direction(self, sig, f, now) -> list[Message]:
        if not (f.drone or f.jet) or (f.missile and not f.drone):
            return []
        cand = [p for p in f.direction_to if p.country in ("MD", "RO") or p.key in UA_WATCH_KEYS]
        cand += [p for p in f.places if p.key in UA_WATCH_KEYS or p.country in ("MD", "RO")]
        border_regions = {geo.ODESA, geo.VINN, geo.CHERN}
        westward_near = f.westward and any(p.region in border_regions for p in f.places)
        relevant = bool(cand) or f.mentions_moldova or (f.mentions_romania and f.westward) or westward_near
        if not relevant:
            return []
        place = cand[0] if cand else None
        new_marker = any(m in normalize(sig.text) for m in NEW_DRONE_MARKERS)
        h = self._match_hyp(place, now, new_marker) or self._new_hyp(now, Level.DIRECTIE, new_marker)
        h.level = max(h.level, Level.DIRECTIE)
        h.updated, h.jet = now, h.jet or f.jet
        if place:
            h.place = place
        h.sources.append(sig.source)
        self._event(h.level, h.id, "directie", self._excerpt(sig.text, 300), now)
        return self._hyp_message(h, "directie", sig, now)

    def _approach(self, h: Hypothesis, f) -> bool:
        if f.mentions_romania and (f.westward or f.lost_or_left):
            return True
        if h.place is None:
            return False
        if h.place.key in PRUT_EDGE_KEYS:
            return True
        west = h.place.lon < 28.65 or f.westward or any(p.country == "RO" for p in f.direction_to)
        return geo.dist(h.place, self.cfg.target) <= self.cfg.approach_km and west

    def _moldova(self, sig, f, now) -> list[Message]:
        if not f.drone:
            return []
        if not (f.mentions_moldova or f.md_places or f.airspace_restricted or sig.role == "md_official"):
            return []
        md = f.md_places
        dir_md = [p for p in f.direction_to if p.country in ("MD", "RO")]
        place = None
        if f.lost_or_left and md:
            place = md[-1]
        elif md or dir_md:
            place = min(md + dir_md, key=lambda p: geo.dist(p, self.cfg.target))
        new_marker = any(m in normalize(sig.text) for m in NEW_DRONE_MARKERS)
        h = self._match_hyp(place, now, new_marker) or self._new_hyp(now, Level.MOLDOVA, new_marker)
        h.level = max(h.level, Level.MOLDOVA)
        h.updated, h.jet = now, h.jet or f.jet
        if place:
            h.place = place
        h.origin += [p for p in f.origin if p not in h.origin]
        h.sources.append(sig.source)
        approach = self._approach(h, f)
        if approach:
            h.level = max(h.level, Level.APROPIERE)
        kind = "apropiere" if approach else "moldova"
        self._event(h.level, h.id, kind, self._excerpt(sig.text, 300), now)
        return self._hyp_message(h, kind, sig, now)

    # ------------------------------------------------------------------ oficial (RO)
    def _official(self, sig, f, now) -> list[Message]:
        if sig.role not in PUBLIC_SOURCE_ROLES:
            return []
        watch = {normalize(c) for c in self.cfg.watch_counties}
        county_places = [p for p in f.ro_counties if normalize(p.name) in watch]
        counties = [p.name for p in county_places]
        if not counties:
            return []
        repeat = dt.timedelta(minutes=self.cfg.official_repeat_min)
        link = f" {sig.url}" if sig.url else ""
        src = "operator (RO-Alert primit)" if sig.role == "manual" else (_domain(sig.url) or sig.source)
        title = self._excerpt(sig.text, 180)
        n = normalize(sig.text)
        when = sig.when
        if f.end and re.search(r"(?<!\w)(?:nou|noua|un nou|adapost|incursiune)", n):
            # titlu amestecat („a încetat în X, dar RO-Alert nou în Y”): doar intern, decide operatorul
            self._event(Level.OFICIAL, None, "amestecat", title, now)
            return [Message("internal", "verificare",
                            f"[INTERN] DE VERIFICAT · {hhmm(now)}. Titlu cu încetare ȘI alertă nouă ({', '.join(counties)}): "
                            f"«{title}»{link}. Nu s-a pregătit niciun mesaj public.", Level.OFICIAL, origin_role=sig.role)]
        if f.end:
            fresh = [c for c in counties if (c not in self.last_end or now - self.last_end[c] > repeat)
                     and not (c in self.alerted_at and when < self.alerted_at[c])]  # încetare mai veche decât alerta
            if not fresh:
                return []
            for c in fresh:
                self.last_end[c] = now
                self.ended_at[c] = max(self.ended_at.get(c, when), when)
                self.last_official.pop(c, None)  # o alertă nouă după încetare va fi luată în seamă
            self._event(Level.INCHEIAT, None, "incetare", title, now)
            return [
                Message("internal", "incetare_intern",
                        f"[INTERN] ÎNCETARE raportată · {hhmm(now)} · {', '.join(fresh)}: «{title}»{link}", Level.INCHEIAT,
                        origin_role=sig.role),
                Message("public", "incetare",
                        f"[NEOFICIAL] ÎNCETARE · {hhmm(now)}. Se relatează încetarea alertei pentru: {', '.join(fresh)}. "
                        f"Sursa: {src}{link}. Nu atingeți eventualele fragmente; anunțați-le la 112.",
                        Level.INCHEIAT, origin_role=sig.role),
            ]
        aerial = f.drone or "spatiu aerian" in n or "spatiul aerian" in n or "obiecte" in n
        if not (f.roalert and aerial):
            return []
        fresh = [c for c in counties if (c not in self.last_official or now - self.last_official[c] > repeat)
                 and not (c in self.ended_at and when <= self.ended_at[c])]  # știre întârziată despre o alertă încheiată
        if not fresh:
            return []
        for c in fresh:
            self.last_official[c] = now
            self.alerted_at[c] = max(self.alerted_at.get(c, when), when)
            self.last_end.pop(c, None)
        near = [p for p in county_places if p.name in fresh]
        for h in self.open_hyps():
            close = h.place is None or any(geo.dist(h.place, p) <= 200 for p in near)
            if h.level >= Level.MOLDOVA and close and now - h.updated <= dt.timedelta(minutes=90):
                h.official = True
        self._event(Level.OFICIAL, None, "oficial", title, now)
        return [
            Message("internal", "oficial_intern",
                    f"[INTERN] OFICIAL · {hhmm(now)}. RO-Alert raportat pentru: {', '.join(fresh)} ({sig.source}). "
                    f"«{title}»{link}", Level.OFICIAL, origin_role=sig.role),
            Message("public", "retransmitere",
                    f"[NEOFICIAL] RETRANSMITERE · {hhmm(now)}. Se relatează un mesaj RO-Alert pentru: {', '.join(fresh)}. "
                    f"Sursa: {src}{link}. Urmați doar instrucțiunile oficiale RO-Alert / ISU. "
                    f"Observațiile se raportează la 112.", Level.OFICIAL, origin_role=sig.role),
        ]

    # ------------------------------------------------------------------ ADS-B
    def _adsb(self, sig, now) -> list[Message]:
        m = sig.meta or {}
        if "coverage" not in m:
            return self._adsb_legacy(sig, now)
        point = m.get("point", "?")
        cov = m.get("coverage") or {}
        eff = int(m.get("civil_airborne", 0) or 0) + int(m.get("civil_gps_lost", 0) or 0)
        g = m.get("gnss") or {}
        prev_ok = (self.adsb_view.get(point) or {}).get("la_ok")
        self.adsb_view[point] = {"trafic": eff, "acoperire": cov.get("reason", "ok"),
                                 "gnss": g.get("level"), "manevre": int(m.get("maneuver_aircraft", 0) or 0),
                                 "control": bool(m.get("is_control")), "sursa": m.get("sursa_date"), "la": now,
                                 "la_ok": now if cov.get("ok") else prev_ok}
        if cov.get("ok") and self.store:
            self.store.add_adsb_sample(now, point, eff, int(m.get("civil_total", 0) or 0))
            if int(g.get("n", 0) or 0) >= 4:
                self.store.add_adsb_gnss(now, point, g.get("n", 0), g.get("degraded", 0), g.get("lost", 0), g.get("ratio", 0.0))
        if m.get("is_control"):
            return []  # zona de control (departe de Prut) servește doar la comparație
        msgs = (self._adsb_drop(point, m, eff, now) + self._adsb_emergencies(point, m, now)
                + self._adsb_gnss(point, g, now) + self._adsb_maneuvers(point, m, now))
        self._save_aviation(now)  # scrie doar dacă starea de păstrat s-a schimbat
        return msgs

    def _active(self) -> bool:
        return bool(self.vigilance_since) or any(h.level >= Level.DIRECTIE for h in self.open_hyps())

    def _quiet(self, key: tuple, now, minutes: float) -> bool:
        last = self.adsb_last_msg.get(key)
        return bool(last and now - last < dt.timedelta(minutes=minutes))

    def _adsb_drop(self, point, m, eff, now) -> list[Message]:
        """Scădere la zero și ocolire (trafic mult redus), cu histerezis: o citire proastă (date lipsă)
        nu schimbă starea, iar ieșirea cere 3 citiri bune clar peste prag."""
        d = m.get("drop") or {}
        cov = m.get("coverage") or {}
        msgs = []
        out = bool(d.get("suspected_outage"))
        if out and not self.adsb_outage.get(point):
            self._event(Level.FOND, None, "adsb_date_indisponibile", f"{point}: {cov.get('reason')}", now)
        self.adsb_outage[point] = out
        if not cov.get("ok"):
            return msgs  # date lipsă/vechi: nici intrare, nici ieșire
        base = d.get("baseline")
        ok_streak = self.adsb_ok_streak
        # --- scădere la 0 (confirmată de analizor cu zona de control)
        if d.get("real"):
            ok_streak[(point, "zero")] = 0
            if not self.adsb_anomaly.get(point):
                self.adsb_anomaly[point] = True
                self._event(Level.FOND, None, "adsb_anomalie", f"{point}: de la ~{base} la 0", now)
                if self._active() and not self._quiet((point, "zero"), now, 30):
                    self.adsb_last_msg[(point, "zero")] = now
                    msgs.append(Message("internal", "adsb",
                                        f"[INTERN] ADS-B · {hhmm(now)}. Traficul civil din jurul {point} a scăzut de la "
                                        f"~{base:g} la 0 aeronave în aer (zona de control normală, date proaspete de la "
                                        f"agregator; o pană a receptoarelor locale ar arăta la fel). Posibilă închidere de "
                                        f"spațiu aerian (de confirmat cu NOTAM). Nicio acțiune publică.", Level.FOND))
        elif self.adsb_anomaly.get(point):
            clear = isinstance(base, (int, float)) and eff > 0.5 * base
            n = ok_streak[(point, "zero")] = (ok_streak.get((point, "zero"), 0) + 1) if clear else 0
            if n >= 3:
                self.adsb_anomaly[point] = False
                ok_streak[(point, "zero")] = 0
                self.adsb_last_msg[(point, "redus")] = now  # o revenire parțială nu e o „ocolire” nouă
        # --- ocolire: trafic mult sub fondul recent, dar nu zero (zero = logica de mai sus)
        low = bool(isinstance(base, (int, float)) and base >= 4 and 0 < eff <= 0.3 * base
                   and not self.adsb_anomaly.get(point) and d.get("control_ok") is not False)
        if low:
            ok_streak[(point, "redus")] = 0
            streak = self.adsb_low_streak[point] = self.adsb_low_streak.get(point, 0) + 1
            if streak >= 3 and not self.adsb_reduced.get(point):
                self.adsb_reduced[point] = True
                self._event(Level.FOND, None, "adsb_trafic_redus", f"{point}: {eff} față de ~{base:g}", now)
                if self._active() and not self._quiet((point, "redus"), now, 30):
                    self.adsb_last_msg[(point, "redus")] = now
                    msgs.append(Message("internal", "adsb",
                                        f"[INTERN] ADS-B · {hhmm(now)}. Trafic civil mult redus în jurul {point}: {eff} "
                                        f"aeronave în aer față de ~{base:g} în ultimele ore (zona de control normală). "
                                        f"Posibilă ocolire a zonei sau restricție de spațiu aerian; de confirmat (NOTAM). "
                                        f"Nicio acțiune publică.", Level.FOND))
        else:
            self.adsb_low_streak[point] = 0
            if self.adsb_reduced.get(point):
                clear = not isinstance(base, (int, float)) or eff > 0.5 * base
                n = ok_streak[(point, "redus")] = ok_streak.get((point, "redus"), 0) + 1 if clear else 0
                if n >= 3:
                    self.adsb_reduced[point] = False
                    ok_streak[(point, "redus")] = 0
        return msgs

    def _adsb_emergencies(self, point, m, now) -> list[Message]:
        msgs = []
        for e in m.get("emergencies") or []:
            if not isinstance(e, dict) or not e.get("new"):
                continue
            key = (point, "urgenta", e.get("code"))
            if self._quiet(key, now, 10):
                continue
            self.adsb_last_msg[key] = now
            where = (f"la ~{e['dist_km']:.0f} km {e.get('bearing') or ''} de {point}".replace("  ", " ")
                     if e.get("dist_km") is not None else f"în zona {point}")
            alt = f", ~{e['alt_ft']} ft" if e.get("alt_ft") is not None else ""
            extra = " Cod 7500 confirmat în mai multe citiri; poate fi și o eroare de transponder." if e.get("code") == "7500" else ""
            self._event(Level.FOND, None, "adsb_urgenta", f"{point}: {e.get('code')}", now)
            msgs.append(Message("internal", "adsb_urgenta",
                                f"[INTERN] ADS-B · URGENȚĂ {e.get('code')} · {hhmm(now)}. O aeronavă civilă transmite "
                                f"{e.get('code')} ({e.get('meaning', '')}) {where}{alt}, categorie {e.get('category') or '?'}. "
                                f"Informativ: codul nu are neapărat legătură cu dronele; aeronava nu e identificată.{extra} "
                                f"Nicio acțiune publică.", Level.FOND))
        return msgs

    def _adsb_gnss(self, point, g, now) -> list[Message]:
        if not g.get("changed"):
            return []
        if g.get("interference"):
            self._event(Level.FOND, None, "gnss_degradat", f"{point}: {g.get('degraded')}/{g.get('n')}", now)
            if not g.get("baseline_ready"):
                return []  # primele 3 zile: doar învățăm fondul zonei (Marea Neagră are bruiaj frecvent)
            sent = [t for t in self.adsb_gnss_sent.get(point, []) if now - t < dt.timedelta(hours=24)]
            if len(sent) >= 4 or self._quiet((point, "gnss"), now, 30):
                return []
            self.adsb_gnss_sent[point] = sent + [now]
            self.adsb_last_msg[(point, "gnss")] = now
            self.adsb_gnss_started.add(point)
            scope = {"local": ("normală", "Posibil bruiaj GNSS local"),
                     "regional": ("afectată și ea", "Posibil bruiaj GNSS regional")}.get(
                         g.get("scope"), ("fără date", "Posibil bruiaj GNSS (întindere necunoscută)"))
            return [Message("internal", "gnss",
                            f"[INTERN] GNSS · {hhmm(now)}. Zona {point}: {g.get('degraded')} din {g.get('n')} aeronave civile "
                            f"cu precizie GPS degradată (NACp<8/NIC<7), dintre care {g.get('lost', 0)} fără poziție GPS. "
                            f"Zona de control: {scope[0]}. {scope[1]}; de confirmat. Nicio acțiune publică.", Level.FOND)]
        self._event(Level.FOND, None, "gnss_normal", f"{point}: {g.get('level')}", now)
        if point not in self.adsb_gnss_started:
            return []
        self.adsb_gnss_started.discard(point)
        if g.get("level") == "insuficient":
            text = (f"[INTERN] GNSS · {hhmm(now)}. Zona {point}: precizia GPS nu mai poate fi evaluată (prea puține "
                    f"aeronave sau date lipsă); starea de interferență s-a închis.")
        else:
            text = f"[INTERN] GNSS · {hhmm(now)}. Zona {point}: precizia GPS a revenit la normal ({g.get('degraded')}/{g.get('n')})."
        return [Message("internal", "gnss", text, Level.FOND)]

    def _adsb_maneuvers(self, point, m, now) -> list[Message]:
        """Anunț la apariție; din nou doar dacă numărul crește cu ≥ 2, sau un memento după 60 min."""
        n = int(m.get("maneuver_aircraft", 0) or 0)
        if n == 0:
            self.adsb_maneuver_sent_n[point] = 0
        if not ((m.get("maneuver_alert") and self._active()) or n >= 3):
            return []
        sent_n = self.adsb_maneuver_sent_n.get(point, 0)
        if n < max(sent_n, 2) + 2 and self._quiet((point, "manevre"), now, 60):
            return []
        self.adsb_last_msg[(point, "manevre")] = now
        self.adsb_maneuver_sent_n[point] = n
        det = "; ".join(_maneuver_text(x) for x in (m.get("maneuvers") or [])[:4]
                        if isinstance(x, dict) and x.get("dist_km") is not None)
        self._event(Level.FOND, None, "adsb_manevre", f"{point}: {n} aeronave", now)
        return [Message("internal", "adsb",
                        f"[INTERN] ADS-B · {hhmm(now)}. {point}: {m.get('holding_recent', 0)} aeronave civile în așteptare "
                        f"și {m.get('turnbacks', 0)} întoarceri de pe rută în ultimele 20 min"
                        f"{f' ({det})' if det else ''}. Posibilă restricție de spațiu aerian; de confirmat (NOTAM). "
                        f"Nicio acțiune publică.", Level.FOND)]

    # ------------------------------------------------------------------ aeronave militare (doar rezumat, doar intern)
    def _adsb_military(self, sig, now) -> list[Message]:
        """Un mesaj la apariția avioanelor de luptă/dronelor; din nou doar dacă numărul crește cu ≥ 2
        sau după 20 min fără ele. Starea nu se folosește dacă e mai veche de 5 min."""
        from . import adsb_military as AM

        s = sig.meta or {}
        if not s.get("ok"):
            self.military = None  # date indisponibile: nu repetăm o stare veche
            return []
        trig = sum(n for g, n in (s.get("grupuri") or {}).items() if g in AM.TRIGGER)
        self.military = {"n": s.get("n", 0), "grupuri": s.get("grupuri", {}), "trigger": trig,
                         "descriere": AM.describe(s), "numere": AM.describe(s, positions=False), "zona": s.get("area")}
        self.military_at = now
        if trig == 0:
            if self.military_zero_since is None:
                self.military_zero_since = now
            if now - self.military_zero_since >= dt.timedelta(minutes=20) and self.military_announced:
                self.military_announced = 0  # absență susținută: următoarea apariție e din nou „nouă”
                self._save_aviation(now)
            return []
        self.military_zero_since = None
        recent = self.military_msg_at and now - self.military_msg_at < dt.timedelta(minutes=20)
        if trig <= self.military_announced or (recent and trig < self.military_announced + 2):
            return []
        self.military_announced = trig
        self.military_msg_at = now
        self._event(Level.FOND, None, "adsb_militar", "", now)  # doar momentul; conținutul nu se arhivează
        self._save_aviation(now)
        radius = s.get("radius_nm")
        zone = f"în raza de {radius:g} NM ({radius * 1.852:.0f} km) de Iași" if isinstance(radius, (int, float)) else "în zona urmărită"
        return [Message("internal", "adsb_militar",
                        f"[INTERN – NU REDISTRIBUIȚI] ADS-B MILITAR · {hhmm(now)}. Aeronave militare vizibile în datele "
                        f"publice {zone}: {AM.describe(s)}. Poate indica o reacție a apărării aeriene. Absența lor nu "
                        f"înseamnă nimic (zboară des fără ADS-B). Nu publicați pozițiile.", Level.FOND)]

    # ------------------------------------------------------------------ stare de aviație după repornire (doar ore și numere)
    def _save_aviation(self, now):
        if not self.store:
            return
        st = {"military_announced": self.military_announced,
              "military_msg_at": iso(self.military_msg_at) if self.military_msg_at else None,
              "last_msg": {"|".join(map(str, k)): iso(v) for k, v in self.adsb_last_msg.items()
                           if now - v < dt.timedelta(hours=2)},
              "anomaly": {k: v for k, v in self.adsb_anomaly.items() if v},
              "reduced": {k: v for k, v in self.adsb_reduced.items() if v},
              "gnss_started": sorted(self.adsb_gnss_started), "maneuver_sent_n": self.adsb_maneuver_sent_n,
              "gnss_sent": {k: [iso(t) for t in v if now - t < dt.timedelta(hours=24)] for k, v in self.adsb_gnss_sent.items()}}
        blob = json.dumps(st, ensure_ascii=False, sort_keys=True)
        if blob == getattr(self, "_aviation_saved", None) and now - getattr(self, "_aviation_saved_at", now) < dt.timedelta(minutes=30):
            return
        self._aviation_saved, self._aviation_saved_at = blob, now
        self.store.kv_set("stare_aviatie", json.dumps({**st, "la": iso(now)}, ensure_ascii=False))

    def _restore_aviation(self, t):
        try:
            st = json.loads(self.store.kv_get("stare_aviatie", "") or "{}")
        except ValueError:
            return
        at = parse_iso(st.get("la"))
        if not at:
            return
        if t - at <= dt.timedelta(hours=24):  # limita de 4 mesaje GNSS/zi rămâne valabilă după repornire
            for k, v in (st.get("gnss_sent") or {}).items():
                self.adsb_gnss_sent[k] = [x for x in (parse_iso(i) for i in v) if x]
        if t - at > dt.timedelta(hours=2):
            return
        self.military_announced = int(st.get("military_announced") or 0)
        self.military_msg_at = parse_iso(st.get("military_msg_at"))
        for k, v in (st.get("last_msg") or {}).items():
            parts = k.split("|")
            if parse_iso(v):
                self.adsb_last_msg[tuple(parts)] = parse_iso(v)
        self.adsb_anomaly.update(st.get("anomaly") or {})
        self.adsb_reduced.update(st.get("reduced") or {})
        self.adsb_gnss_started.update(st.get("gnss_started") or [])
        self.adsb_maneuver_sent_n.update(st.get("maneuver_sent_n") or {})

    # ------------------------------------------------------------------ NOTAM (context oficial)
    def _announced_keys(self) -> dict | None:
        try:
            v = self.store.kv_get("notam_anuntate") if self.store else None
            return json.loads(v) if v is not None else None
        except ValueError:
            return {}

    def _save_announced(self):
        if self.store:
            keys = {k: m.get("end") or "" for k, m in self.notam_active.items() if m.get("_anuntat")}
            self.store.kv_set("notam_anuntate", json.dumps(keys))

    def _restore_notams(self):
        """După repornire: NOTAM-urile active din arhivă, cu marcajul „anunțat” păstrat în kv.
        Cele neanunțate rămân eligibile (ex. programate, sau în așteptare la oprire)."""
        from .timeutil import now as _now

        t = _now()
        self._restore_aviation(t)
        try:
            rows = self.store.signals_by_role("notam", t - dt.timedelta(days=21))
        except Exception:  # noqa: BLE001 - arhivă veche sau indisponibilă
            return
        announced = self._announced_keys()
        for r in rows:
            try:
                m = json.loads(r["meta"] or "{}")
            except ValueError:
                continue
            if not isinstance(m, dict):
                continue
            m["_text"] = r["text"]
            key = m.get("key") or m.get("id")
            # prima pornire după actualizare (fără listă salvată): le considerăm anunțate, fără rafală
            m["_anuntat"] = True if announced is None else key in announced
            self._notam_apply(m)
        self._notam_expire(t, announce=False)
        self._save_announced()

    def _predecessor(self, m: dict) -> dict | None:
        cont = m.get("continua")
        if not cont:
            return None
        scope = (m.get("key") or "").split(":")[0]
        for v in self.notam_active.values():
            if v.get("id") == cont and (v.get("key") or "").split(":")[0] == scope:
                return v
        return None

    def _notam_apply(self, m: dict) -> dict | None:
        ended = self.notam_active.pop(m["ends_key"], None) if m.get("ends_key") else None
        if m.get("ends_key"):
            self.notam_pending = [p for p in self.notam_pending if (p.get("key") or p.get("id")) != m["ends_key"]]
        key = m.get("key") or m.get("id")
        if m.get("kind") in ("nou", "inlocuire") and key:
            pred = self._predecessor(m) or ended
            start, pend = parse_iso(m.get("start")), parse_iso((pred or {}).get("end"))
            adjacent = not start or not pend or start <= pend + dt.timedelta(hours=1)
            inherits = bool(pred and pred.get("_anuntat") and m.get("continua") and adjacent)
            if "_anuntat" not in m:
                # o reemitere (același conținut) a unui NOTAM deja anunțat, lipită de el în timp, nu e o noutate
                m["_anuntat"] = inherits
            if inherits:
                pred["_succesor"] = key  # predecesorul expiră fără „ÎNCHEIAT”: restricția continuă
            self.notam_active[key] = m
        return ended

    def _notam_eligible(self, m: dict, now: dt.datetime) -> str | None:
        """„acum”, „viitor” (va fi eligibil) sau None."""
        if m.get("kind") not in ("nou", "inlocuire") or m.get("_anuntat"):
            return None
        cat, fir, locs = m.get("category"), m.get("fir"), set(m.get("locations") or [])
        if not (m.get("near") or fir == "LUUU"):
            return None
        if not (cat in ("spatiu_aerian_inchis", "drone_uas", "gnss")
                or (cat == "aeroport_inchis" and locs & {"LRIA", "LUKK", "LUBL"})
                or (cat == "restrictie_spatiu_aerian" and (m.get("uas") or fir == "LUUU"))):
            return None
        start, end = parse_iso(m.get("start")), parse_iso(m.get("end"))
        if end and end <= now:
            return None
        if start and start > now + dt.timedelta(hours=6):
            return "viitor"
        return "acum"

    def _notam(self, sig, now) -> list[Message]:
        m = dict(sig.meta or {})
        m["_text"] = sig.text
        m.pop("_anuntat", None)
        kind = m.get("kind")
        ended = self._notam_apply(m)
        msgs = []
        if kind in ("anulare", "retras") and ended and ended.get("_anuntat"):
            how = ("anulat" if kind == "anulare" else
                   "nu mai apare în lista sursei înainte de expirare (anulat sau retras; de verificat)")
            msgs.append(Message("internal", "notam_sfarsit",
                                f"[INTERN] NOTAM {'ANULAT' if kind == 'anulare' else 'RETRAS'} · {hhmm(now)} · "
                                f"{ended.get('id')} ({NOTAM_CAT_RO.get(ended.get('category'), ended.get('category'))}) {how}.",
                                Level.FOND))
        if kind in ("nou", "inlocuire"):
            self._event(Level.FOND, None, "notam", f"{m.get('id')} {m.get('category')} {m.get('fir')}", now)
            if self._notam_eligible(m, now) == "acum":
                self.notam_pending.append(m)
        msgs += self._notam_flush(now)
        self._save_announced()
        return msgs

    def _notam_flush(self, now) -> list[Message]:
        if not self.notam_pending:
            return []
        if self.notam_last_msg and now - self.notam_last_msg < dt.timedelta(minutes=10):
            return []
        # doar cele încă active (nu anulate/înlocuite/expirate cât au așteptat)
        items = [m for m in self.notam_pending
                 if self.notam_active.get(m.get("key") or m.get("id")) is m
                 and not (parse_iso(m.get("end")) and parse_iso(m.get("end")) <= now) and not m.get("_anuntat")]
        self.notam_pending = []
        if not items:
            return []
        self.notam_last_msg = now
        for m in items:
            m["_anuntat"] = True
        self._save_announced()
        md = [m for m in items if m.get("category") == "spatiu_aerian_inchis" and m.get("fir") == "LUUU"]
        body = items[0]["_text"] if len(items) == 1 else "\n• " + "\n• ".join(m["_text"] for m in items)
        if md:
            head = (f"[INTERN] ATENȚIE · {hhmm(now)} · NOTAM R. Moldova: spațiu aerian închis. De obicei înseamnă "
                    f"drone detectate în R. Moldova; urmăriți sursele MD. ")
        else:
            head = f"[INTERN] NOTAM · {hhmm(now)} · " + (f"{len(items)} NOTAM noi lângă Iași/Prut: " if len(items) > 1 else "")
        return [Message("internal", "notam", f"{head}{body}\nContext oficial, nu confirmă o dronă. Nicio acțiune publică.",
                        Level.FOND)]

    def _notam_expire(self, now, announce: bool = True) -> list[Message]:
        msgs = []
        changed = False
        for k, m in list(self.notam_active.items()):
            end = parse_iso(m.get("end"))
            grace = dt.timedelta(minutes=30) if m.get("estimated") else dt.timedelta(0)
            if end and end + grace < now:
                del self.notam_active[k]
                changed = True
                succ = m.get("_succesor") in self.notam_active
                if announce and m.get("_anuntat") and not m.get("estimated") and not succ:
                    msgs.append(Message("internal", "notam_sfarsit",
                                        f"[INTERN] NOTAM ÎNCHEIAT · {hhmm(now)} · {m.get('id')} "
                                        f"({NOTAM_CAT_RO.get(m.get('category'), m.get('category'))}) a expirat.", Level.FOND))
            elif announce and self._notam_eligible(m, now) == "acum" and not any(p is m for p in self.notam_pending):
                self.notam_pending.append(m)  # NOTAM programat care a devenit iminent (sau rămas după repornire)
        if changed:
            self._save_announced()
        return msgs

    def _adsb_legacy(self, sig, now) -> list[Message]:
        m = sig.meta
        point = m.get("point", "?")
        if self.store:
            self.store.add_adsb_sample(now, point, m.get("civil_airborne", 0), m.get("civil_total", 0))
            hist = self.store.adsb_samples(point, now - dt.timedelta(hours=2))
        else:
            hist = []
        vals = [r["civil_airborne"] for r in hist]
        if len(vals) < 20:
            return []
        recent, base = vals[-3:], vals[:-10]
        baseline = statistics.median(base) if base else 0
        anomaly = baseline >= 2 and max(recent) == 0
        was = self.adsb_anomaly.get(point, False)
        self.adsb_anomaly[point] = anomaly
        if anomaly and not was:
            self._event(Level.FOND, None, "adsb_anomalie", f"{point}: de la ~{baseline:g} la 0", now)
            if self.vigilance_since or any(h.level >= Level.DIRECTIE for h in self.open_hyps()):
                return [Message("internal", "adsb",
                                f"[INTERN] ADS-B · {hhmm(now)}. Traficul civil din jurul {point} a scăzut de la ~{baseline:g} la 0 "
                                f"aeronave în aer. Posibilă închidere de spațiu aerian (de confirmat; poate fi și altă cauză).",
                                Level.FOND)]
        return []

    # ------------------------------------------------------------------ intrare
    def process(self, sig: Signal, now: dt.datetime) -> list[Message]:
        if sig.role == "adsb":
            return self._adsb(sig, now)
        if sig.role == "adsb_militar":
            return self._adsb_military(sig, now)
        if sig.role == "notam":
            # înaintea filtrului de vârstă: validitatea se judecă după B)/C) din meta, nu după data publicării
            return self._notam(sig, now)
        if sig.role == "ua_alert_state":
            self.ua_state[sig.source] = list(sig.meta.get("active") or [])
            self.ua_state_alive[sig.source] = now
            return self._update_vigilance(now)
        pub = sig.published_at
        if pub and pub > now + dt.timedelta(minutes=2):
            if not self.clock_skew_warned:
                log.warning("sursa %s are ora în viitor (%s); verificați ceasul serverului (NTP)", sig.source, pub)
                self.clock_skew_warned = True
            pub = now
        limit = self.cfg.max_age_news_min if sig.role in NEWS_ROLES else self.cfg.max_age_min
        if pub and now - pub > dt.timedelta(minutes=limit):
            return []  # arhivat, dar prea vechi ca să declanșeze ceva
        if sig.role == "ua_alerts":
            return self._tg_alert(sig, now)
        f = analyze(sig.text)
        if sig.role in ("ua_direction", "ua_official"):
            return self._ua_direction(sig, f, now)
        if sig.role in ("md_official", "md_news"):
            return self._moldova(sig, f, now)
        if sig.role in PUBLIC_SOURCE_ROLES:
            return self._official(sig, f, now)
        return []

    def tick(self, now: dt.datetime) -> list[Message]:
        ttl = dt.timedelta(minutes=self.cfg.ttl_min)
        for h in self.open_hyps():
            if now - h.updated > ttl:
                h.closed = True
                self._event(h.level, h.id, "ipoteza_inchisa", f"fără semnale noi de {self.cfg.ttl_min:g} min", now)
        self.hyps = [h for h in self.hyps if not h.closed or now - h.updated < dt.timedelta(hours=6)]
        return self._notam_expire(now) + self._notam_flush(now) + self._update_vigilance(now)

    def status(self, now: dt.datetime) -> dict:
        lvl = max([h.level for h in self.open_hyps()] + [Level.VIGILENTA if self.vigilance_since else Level.FOND])
        stale = dt.timedelta(minutes=self.cfg.state_stale_min)
        return {
            "nivel": LEVEL_RO[Level(lvl)],
            "vigilenta_din": hhmm(self.vigilance_since) if self.vigilance_since else None,
            "alerte_ua_active": sorted(self._active_titles(now)),
            "surse_stare_invechite": sorted(s for s, t in self.ua_state_alive.items() if now - t > stale),
            "ipoteze": [{"id": h.id, "nivel": LEVEL_RO[h.level], "oficial": h.official,
                         "pozitie": h.place.name if h.place else None,
                         "actualizat": hhmm(h.updated), "reactie": h.jet} for h in self.open_hyps()],
            "adsb_anomalii": [k for k, v in self.adsb_anomaly.items() if v],
            "adsb_trafic_redus": [k for k, v in self.adsb_reduced.items() if v],
            "adsb_gnss_degradat": sorted(self.adsb_gnss_started),
            "adsb_zone": {k: {**v, "la": hhmm(v["la"]) if v.get("la") else None,
                              "la_ok": hhmm(v["la_ok"]) if v.get("la_ok") else "niciodată",
                              "vechi": not v.get("la_ok") or now - v["la_ok"] > dt.timedelta(minutes=5)}
                          for k, v in self.adsb_view.items()},
            "militar": ({**self.military, "la": hhmm(self.military_at)}
                        if self.military and self.military_at and now - self.military_at <= dt.timedelta(minutes=5) else None),
            "notam_active": [{"id": m.get("id"), "categorie": NOTAM_CAT_RO.get(m.get("category"), m.get("category")),
                              "fir": m.get("fir"), "pana_la": hhmm(parse_iso(m["end"])) if m.get("end") else "permanent",
                              "aproape": bool(m.get("near"))} for m in self.notam_active.values()],
        }
