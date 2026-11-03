"""Extragere simplă, pe reguli, din texte în ucraineană, rusă și română.

Nu e învățare automată: liste de cuvinte-cheie și localități. Orice decizie publică
trece oricum prin operator.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from . import geo

_LATIN_FIX = str.maketrans({"ş": "ș", "Ş": "Ș", "ţ": "ț", "Ţ": "Ț", "’": "'", "ʼ": "'", "`": "'"})


def _deaccent_latin(s: str) -> str:
    out = []
    for ch in s:
        if ch.isalpha() and "LATIN" in unicodedata.name(ch, ""):
            out.append(unicodedata.normalize("NFD", ch)[0])
        else:
            out.append(ch)
    return "".join(out)


def normalize(text: str) -> str:
    t = unicodedata.normalize("NFC", text or "").translate(_LATIN_FIX).lower()
    t = _deaccent_latin(t)
    return re.sub(r"\s+", " ", t).strip()


def detect_lang(text: str) -> str:
    cyr = sum(1 for c in text if "Ѐ" <= c <= "ӿ")
    lat = sum(1 for c in text if c.isascii() and c.isalpha())
    if cyr > lat:
        return "uk" if re.search(r"[іїєґ]", text.lower()) else "ru"
    return "ro"


def _rx(words: list[str]) -> re.Pattern:
    return re.compile(r"(?<!\w)(?:" + "|".join(words) + r")")


DRONE = _rx([
    r"бпла", r"безпілотн", r"беспилотн", r"дрон", r"шахед", r"шахід", r"герань", r"гербер",
    r"ударн\w* бпла", r"dron(?:a|e|ei|ele|elor)\b", r"drones?\b", r"uavs?\b", r"unmanned", r"мопед",
    r"aparat\w* de zbor fara pilot",
    r"aparat\w* fara pilot", r"tinta aeriana", r"tinte aeriene",
    r"obiect\w* zburator", r"shahed", r"geran",
])
MISSILE = _rx([r"ракет", r"балістик", r"баллистик", r"крилат", r"крылат", r"rachet"])
JET = _rx([r"реактивн", r"cu reactie", r"reactiv", r"jet\b", r"турбореактив"])
UA_ALERT_ON = _rx([r"повітрян\w* тривог", r"тривога", r"тривогу", r"воздушн\w* тревог", r"тревога"])
UA_ALERT_OFF = _rx([r"відбій", r"отбой"])
AIRSPACE = _rx([r"spatiul aerian", r"spatiului aerian", r"spatiu aerian", r"повітрян\w* простір", r"воздушн\w* пространств"])
RESTRICT = _rx([r"restrictionat", r"inchis", r"restrictii", r"обмежен", r"закрит", r"ограничен"])
REOPEN = _rx([r"redeschis", r"ridicat\w* restrict", r"відкрит", r"открыт"])
LOST = _rx([r"a disparut de pe radar", r"disparut de pe sistemele", r"a parasit spatiul aerian", r"a iesit din spatiul aerian"])
ROALERT = _rx([r"ro-alert", r"ro alert", r"roalert", r"alerta extrema", r"alerta aeriana"])
END = _rx([r"incetare\w* (?:a )?(?:starii de )?alert", r"alerta (?:aeriana )?a incetat", r"a incetat (?:starea de )?alert",
           r"alerta (?:aeriana )?(?:a fost )?(?:ridicata|incheiata)", r"starea de alerta aeriana .{0,30}(?:a fost ridicata|a incetat)",
           r"s-a incheiat alerta", r"alert(?:a|ei) (?:aeriana )?(?:s-a )?(?:incheiat|terminat)",
           r"alerta (?:aeriana |ro-alert )?(?:din|pentru|in) [^.]{0,40}?(?<!nu )(?:a incetat|a fost ridicata|s-a incheiat)"])
MOLDOVA = _rx([r"молдов", r"moldov", r"r\. moldova", r"republica moldova", r"придністров", r"приднестров", r"transnistr"])
ROMANIA = _rx([r"румун", r"румын", r"romani"])
DIRECTION = re.compile(
    r"(?<!\w)(?:курсом на|у напрямку|в напрямку|в направлении|направлением на|spre|in directia|cu directia|cu deplasare spre|towards|heading to|in the direction of)\s+([^\.,;:!\n]{0,60})"
)
ADMIN_CONT = re.compile(r",\s*((?:raionul|r\.|regiunea|районі?|район\w*|област\w*)\s+[^\.,;:!\n]{0,40})")
ORIGIN = re.compile(r"(?<!\w)(?:dinspre|з боку|со стороны|from)\s+([^\.,;:!\n]{0,60})")
# plecare spre Ucraina: drona se îndepărtează de România (ex. „a părăsit spațiul aerian pe la Otaci, revenind în Ucraina”)
TOWARD_UA = _rx([r"(?:spre|catre|inapoi (?:in|spre)|revenind (?:in|spre)|s-a intors (?:in|spre)|a revenit (?:in|spre)|"
                 r"in directia|cu directia|in spatiul aerian al) (?:spatiul aerian (?:al )?)?ucrain",
                 r"в (?:сторону|направлении) украин", r"вернул\w* в украин", r"повернул\w* (?:в|до) україн",
                 r"у напрямку україн", r"в напрямку україн"])
WESTWARD = _rx([r"на захід", r"західн\w* напрям", r"на запад", r"spre vest", r"directia vest", r"nord-vest", r"sud-vest",
                 r"північн\w*[ -]захід", r"північно-західн", r"південн\w*[ -]захід", r"південно-західн",
                 r"северо-запад", r"юго-запад", r"западн\w* направлен", r"westward", r"north-?west", r"south-?west"])

_VARIANT_RX: dict[str, re.Pattern] = {}


def _place_rx(p: geo.Place) -> re.Pattern:
    rx = _VARIANT_RX.get(p.key)
    if rx is None:
        parts = []
        for v in p.variants:
            if v.startswith("re:"):
                parts.append(r"(?<!\w)(?:" + v[3:] + ")")
            else:
                parts.append(r"(?<!\w)" + re.escape(normalize(v)))
        rx = re.compile("|".join(parts))
        _VARIANT_RX[p.key] = rx
    return rx


def find_places(norm_text: str, countries: tuple[str, ...] = ("UA", "MD", "RO")) -> list[geo.Place]:
    """Localitățile menționate, în ordinea primei apariții în text."""
    hits = []
    for p in geo.GAZETTEER:
        if p.country not in countries:
            continue
        m = _place_rx(p).search(norm_text)
        if m:
            hits.append((m.start(), p))
    hits.sort(key=lambda x: x[0])
    return [p for _, p in hits]


@dataclass
class Finding:
    lang: str
    drone: bool = False
    missile: bool = False
    jet: bool = False
    ua_alert_on: bool = False
    ua_alert_off: bool = False
    airspace_restricted: bool = False
    airspace_reopened: bool = False
    lost_or_left: bool = False
    roalert: bool = False
    end: bool = False
    mentions_moldova: bool = False
    mentions_romania: bool = False
    westward: bool = False
    toward_ua: bool = False
    places: list[geo.Place] = field(default_factory=list)
    direction_to: list[geo.Place] = field(default_factory=list)
    origin: list[geo.Place] = field(default_factory=list)

    @property
    def md_places(self) -> list[geo.Place]:
        return [p for p in self.places if p.country == "MD"]

    @property
    def ro_counties(self) -> list[geo.Place]:
        return [p for p in self.places if p.country == "RO"]

    @property
    def ua_places(self) -> list[geo.Place]:
        return [p for p in self.places if p.country == "UA"]


def analyze(text: str) -> Finding:
    n = normalize(text)
    f = Finding(lang=detect_lang(text))
    f.drone = bool(DRONE.search(n))
    f.missile = bool(MISSILE.search(n))
    f.jet = bool(JET.search(n))
    f.ua_alert_off = bool(UA_ALERT_OFF.search(n))
    f.ua_alert_on = bool(UA_ALERT_ON.search(n)) and not f.ua_alert_off
    air = bool(AIRSPACE.search(n))
    f.airspace_reopened = air and bool(REOPEN.search(n))
    f.airspace_restricted = air and bool(RESTRICT.search(n)) and not f.airspace_reopened
    f.lost_or_left = bool(LOST.search(n))
    f.roalert = bool(ROALERT.search(n))
    f.end = bool(END.search(n))
    f.mentions_moldova = bool(MOLDOVA.search(n))
    f.mentions_romania = bool(ROMANIA.search(n))
    f.westward = bool(WESTWARD.search(n))
    f.toward_ua = bool(TOWARD_UA.search(n)) and not f.mentions_romania
    f.places = find_places(n)
    for m in DIRECTION.finditer(n):
        tail = m.group(1)
        # „spre Sobari, raionul Soroca” / „на Подільськ, Одеська область”: includem precizarea administrativă
        ext = ADMIN_CONT.match(n, m.end())
        if ext:
            tail += " " + ext.group(1)
        f.direction_to += [p for p in find_places(tail) if p not in f.direction_to]
        if MOLDOVA.search(tail) or ROMANIA.search(tail):
            f.westward = True
    for m in ORIGIN.finditer(n):
        f.origin += [p for p in find_places(m.group(1)) if p not in f.origin]
    return f
