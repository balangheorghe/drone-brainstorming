"""Geografie: localități (gazetteer), distanțe, linia Prutului, ETA.

Coordonatele sunt APROXIMATIVE (±2–5 km), suficiente pentru ETA-uri orientative.
Variantele de nume sunt rădăcini (prefixe) potrivite la început de cuvânt, după
normalizare (litere mici, fără diacritice latine). O variantă care începe cu "re:"
este o expresie regulată.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

V_JET_KMH = 450.0  # limita de jos a ETA: drone cu reacție observate în 2026
V_SLOW_KMH = 150.0  # limita de sus: piston/momeală, croazieră prudentă


@dataclass(frozen=True)
class Place:
    key: str
    name: str  # numele afișat (română)
    country: str  # UA / MD / RO
    lat: float
    lon: float
    variants: tuple[str, ...] = field(default=(), compare=False)
    region: str = ""  # pentru UA: regiunea (oblast) în ucraineană


def _p(key, name, country, lat, lon, variants, region=""):
    return Place(key, name, country, lat, lon, tuple(variants), region)


ODESA = "Одеська область"
VINN = "Вінницька область"
CHERN = "Чернівецька область"
MYK = "Миколаївська область"

GAZETTEER: list[Place] = [
    # --- Ucraina ---
    _p("odesa", "Odesa", "UA", 46.482, 30.723, ["одес", "одещин", "odes"], ODESA),
    _p("izmail", "Izmail", "UA", 45.351, 28.837, ["ізмаї", "измаил", "izmail", "ismail"], ODESA),
    _p("reni", "Reni", "UA", 45.456, 28.283, ["re:рен[іи]\\b", "re:reni\\b"], ODESA),
    _p("kiliia", "Kiliia", "UA", 45.453, 29.264, ["кілі", "килия", "kiliia", "kilia"], ODESA),
    _p("vylkove", "Vîlcov", "UA", 45.402, 29.584, ["вилков", "vylkov", "vilkov", "vâlcov", "valcov"], ODESA),
    _p("bilhorod", "Bilhorod-Dnistrovskyi", "UA", 46.186, 30.344,
       ["білгород-дністров", "белгород-днестров", "bilhorod", "cetatea alba"], ODESA),
    _p("bolhrad", "Bolhrad", "UA", 45.677, 28.614, ["болград", "bolhrad", "bolgrad"], ODESA),
    _p("podilsk", "Podilsk", "UA", 47.748, 29.533, ["подільськ", "подольск", "podilsk", "podolsk", "котовськ", "котовск"], ODESA),
    _p("rozdilna", "Rozdilna", "UA", 46.848, 30.078, ["роздільн", "раздельн", "rozdilna"], ODESA),
    _p("berezivka", "Berezivka", "UA", 47.204, 30.913, ["березівк", "березовк", "berezivka"], ODESA),
    _p("mohyliv", "Mohyliv-Podilskyi", "UA", 48.447, 27.798,
       ["могилів-подільськ", "могилев-подольск", "могилів", "mohyliv", "moghiliov"], VINN),
    _p("vinnytsia", "Vinnytsia", "UA", 49.233, 28.468, ["вінниц", "вінничин", "вінниччин", "винниц", "винничин", "vinnyts", "vinita", "vinnita"], VINN),
    _p("tulchyn", "Tulcin", "UA", 48.676, 28.848, ["тульчин", "tulchyn"], VINN),
    _p("vyzhnytsia", "Vijnița", "UA", 48.250, 25.190, ["вижниц", "выжниц", "vijnita", "vyzhnyts"], CHERN),
    _p("storozhynets", "Storojineț", "UA", 48.161, 25.719, ["сторожин", "storojinet", "storozhyn"], CHERN),
    _p("hlyboka", "Hliboca", "UA", 48.081, 25.928, ["re:(?:на|до|біля|поблизу|у|в|районі|напрямку|напрямок|бік|повз|околиц\\w*|над|під|з|із|через)\\s+глибок(?:а|у|ої|ій|ою)(?!\\w)"
       "(?!\\s+(?:ноч|ніч|відстан|темряв|тиш|скорбот|стурбован|вдячн|пова|шан|модерніз|оборон|розвідк|глибин|криз))", "глибоцьк", "re:глыбок\\w*", "hliboca", "hlyboka"], CHERN),
    _p("chernivtsi", "Cernăuți", "UA", 48.292, 25.935, ["чернівц", "чернівец", "чернівеччин", "черновц", "черновиц", "буковин", "chernivts", "cernauti"], CHERN),
    _p("novodnistrovsk", "Novodnistrovsk", "UA", 48.58, 27.44, ["новодністровськ", "новоднестровск", "novodnistrovsk"], CHERN),
    _p("mykolaiv", "Mykolaiv", "UA", 46.975, 31.995, ["миколаї", "миколаїв", "николаев", "mykolaiv"], MYK),
    # --- R. Moldova ---
    _p("chisinau", "Chișinău", "MD", 47.011, 28.861, ["chisinau", "кишин"]),
    _p("balti", "Bălți", "MD", 47.762, 27.929, ["re:balti(?:ul|ului)?\\b", "бельц", "бєльц"]),
    _p("soroca", "Soroca", "MD", 48.156, 28.297, ["soroca", "сороцьк", "сорокск", "re:сорок(?:и|ах|ам)(?!\\w)"]),
    _p("otaci", "Otaci", "MD", 48.43, 27.79, ["otaci", "отач"]),
    _p("ocnita", "Ocnița", "MD", 48.385, 27.437, ["ocnit", "окниц"]),
    _p("edinet", "Edineț", "MD", 48.168, 27.305, ["edinet", "единц"]),
    _p("briceni", "Briceni", "MD", 48.362, 27.084, ["briceni", "бричан"]),
    _p("lipcani", "Lipcani", "MD", 48.265, 26.805, ["lipcani", "липкан"]),
    _p("donduseni", "Dondușeni", "MD", 48.223, 27.585, ["donduseni", "дондюшан"]),
    _p("drochia", "Drochia", "MD", 48.035, 27.813, ["drochia", "дрокия", "дрокія"]),
    _p("riscani", "Rîșcani", "MD", 47.957, 27.553, ["riscani", "rascani", "рышкан", "ришкан"]),
    _p("glodeni", "Glodeni", "MD", 47.771, 27.515, ["glodeni", "глоден"]),
    _p("falesti", "Fălești", "MD", 47.573, 27.709, ["falesti", "фалешт", "фэлешт"]),
    _p("singerei", "Sîngerei", "MD", 47.638, 28.142, ["singerei", "sangerei", "сынжере", "синжере"]),
    _p("floresti", "Florești", "MD", 47.891, 28.301, ["re:(?:raionul|r\\.)\\s*floresti", "флорешт"]),
    _p("ribnita", "Rîbnița", "MD", 47.768, 29.000, ["ribnita", "rabnita", "рыбниц", "рибниц"]),
    _p("dubasari", "Dubăsari", "MD", 47.266, 29.165, ["dubasari", "дубоссар", "дубосар"]),
    _p("orhei", "Orhei", "MD", 47.384, 28.822, ["orhei", "оргеев", "оргіїв"]),
    _p("telenesti", "Telenești", "MD", 47.499, 28.366, ["telenesti", "теленешт"]),
    _p("banesti", "Bănești (Telenești)", "MD", 47.53, 28.44, ["re:banesti\\b(?=.{0,40}telenesti)"]),
    _p("tibirica", "Țibirica", "MD", 47.37, 28.37, ["tibirica", "цибирик"]),
    _p("calarasi", "Călărași (MD)", "MD", 47.255, 28.308, ["re:(?:raionul|r\\.)\\s*calarasi", "кэлэраш", "калараш"]),
    _p("ungheni", "Ungheni", "MD", 47.208, 27.800, ["ungheni", "унген"]),
    _p("zagarancea", "Zagarancea", "MD", 47.24, 27.77, ["zagarancea", "загаранч"]),
    _p("sculeni", "Sculeni", "MD", 47.333, 27.600, ["sculeni", "скулень", "скулены"]),
    _p("nisporeni", "Nisporeni", "MD", 47.081, 28.178, ["nisporeni", "ниспорен"]),
    _p("straseni", "Strășeni", "MD", 47.143, 28.610, ["straseni", "страшен"]),
    _p("hincesti", "Hîncești", "MD", 46.829, 28.590, ["hincesti", "hancesti", "хынчешт", "хинчешт"]),
    _p("leova", "Leova", "MD", 46.479, 28.255, ["leova", "леов"]),
    _p("cimislia", "Cimișlia", "MD", 46.520, 28.784, ["cimislia", "чимишли"]),
    _p("causeni", "Căușeni", "MD", 46.638, 29.411, ["causeni", "каушан"]),
    _p("stefanvoda", "Ștefan Vodă", "MD", 46.513, 29.663, ["stefan voda", "штефан-вод", "штефан вод"]),
    _p("bender", "Bender (Tighina)", "MD", 46.831, 29.478, ["bender", "tighina", "бендер"]),
    _p("tiraspol", "Tiraspol", "MD", 46.840, 29.643, ["tiraspol", "тираспол"]),
    _p("cuciurgan", "Cuciurgan", "MD", 46.78, 29.97, ["cuciurgan", "кучурган"]),
    _p("aneniinoi", "Anenii Noi", "MD", 46.880, 29.231, ["anenii noi", "анений", "аненій"]),
    _p("criuleni", "Criuleni", "MD", 47.214, 29.161, ["criuleni", "криулян"]),
    _p("cahul", "Cahul", "MD", 45.907, 28.194, ["cahul", "кагул"]),
    _p("comrat", "Comrat", "MD", 46.300, 28.657, ["comrat", "комрат"]),
    _p("vulcanesti", "Vulcănești", "MD", 45.68, 28.40, ["vulcanesti", "вулканешт", "вулкэнешт"]),
    _p("taraclia", "Taraclia", "MD", 45.900, 28.669, ["taraclia", "таракли"]),
    _p("etulia", "Etulia", "MD", 45.534, 28.454, ["etulia", "етулі", "етули"]),
    _p("giurgiulesti", "Giurgiulești", "MD", 45.475, 28.198, ["giurgiulesti", "джурджулешт"]),
    # --- România ---
    _p("iasi", "Iași", "RO", 47.158, 27.601, ["iasi", "ясс"]),
    _p("botosani", "Botoșani", "RO", 47.748, 26.669, ["botosani", "ботошан"]),
    _p("suceava", "Suceava", "RO", 47.651, 26.255, ["suceava", "сучав"]),
    _p("radauti", "Rădăuți", "RO", 47.842, 25.919, ["radauti", "рэдэуц", "радівц"]),
    _p("siret", "Siret", "RO", 47.953, 26.064, ["re:(?:orasul |municipiul |la |din )siret\\b", "сирет"]),
    _p("dorohoi", "Dorohoi", "RO", 47.957, 26.397, ["dorohoi", "дорохой"]),
    _p("vaslui", "Vaslui", "RO", 46.640, 27.729, ["vaslui", "васлу"]),
    _p("neamt", "Neamț", "RO", 46.927, 26.370, ["neamt", "piatra-neamt", "piatra neamt"]),
    _p("bacau", "Bacău", "RO", 46.567, 26.914, ["bacau", "бакэу", "бакеу"]),
    _p("galati", "Galați", "RO", 45.435, 28.008, ["galati", "галац"]),
    _p("tulcea", "Tulcea", "RO", 45.180, 28.805, ["tulcea", "тулча"]),
]

BY_KEY = {p.key: p for p in GAZETTEER}

# Ținte și puncte de referință
IASI = BY_KEY["iasi"]
LRIA = Place("lria", "Aeroportul Iași (LRIA)", "RO", 47.178, 27.621)
LUKK = Place("lukk", "Aeroportul Chișinău (LUKK)", "MD", 46.928, 28.931)
LRSV = Place("lrsv", "Aeroportul Suceava (LRSV)", "RO", 47.688, 26.354)
LRBC = Place("lrbc", "Aeroportul Bacău (LRBC)", "RO", 46.522, 26.910)
# Ținte cu alt nume afișat decât în dicționar („neamt” e județul; ținta e municipiul Piatra Neamț)
PIATRA_NEAMT = Place("piatra_neamt", "Piatra Neamț", "RO", 46.927, 26.370)
TARGET_KEYS: dict[str, Place] = {"piatra_neamt": PIATRA_NEAMT, "neamt": PIATRA_NEAMT}
# Nord-Estul (cele 6 reședințe de județ); Iașul (prima) rămâne referința principală (EngineConfig.target)
NE_TARGETS = ["iasi", "suceava", "botosani", "piatra_neamt", "bacau", "vaslui"]

# Linia Prutului (aproximativă, nord → sud)
PRUT_LINE: list[tuple[float, float]] = [
    (48.265, 26.805),  # Lipcani / Rădăuți-Prut
    (47.860, 27.240),  # Costești–Stânca
    (47.540, 27.420),  # zona Bivolari
    (47.333, 27.600),  # Sculeni
    (47.208, 27.790),  # Ungheni
    (47.050, 27.900),  # Prisăcani
    (46.480, 28.245),  # Leova
    (45.900, 28.160),  # Cahul
    (45.475, 28.198),  # Giurgiulești
]

# Punct reprezentativ pentru o regiune/raion ucrainean (pentru ETA în starea de vigilență)
UA_AREA_POINT: dict[str, str] = {
    "Подільський район": "podilsk",
    "Роздільнянський район": "rozdilna",
    "Березівський район": "berezivka",
    "Ізмаїльський район": "izmail",
    "Болградський район": "bolhrad",
    "Білгород-Дністровський район": "bilhorod",
    "Одеський район": "odesa",
    ODESA: "podilsk",
    "Могилів-Подільський район": "mohyliv",
    "Тульчинський район": "tulchyn",
    "Вінницький район": "vinnytsia",
    VINN: "mohyliv",
    "Дністровський район": "novodnistrovsk",
    "Чернівецький район": "chernivtsi",
    "Вижницький район": "vyzhnytsia",
    CHERN: "chernivtsi",
}


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def dist(a: Place, b: Place) -> float:
    return haversine_km(a.lat, a.lon, b.lat, b.lon)


def _seg_dist_km(lat, lon, a, b) -> float:
    # proiecție echirectangulară locală (suficient pentru câteva sute de km)
    k = math.cos(math.radians(lat)) * 111.32
    ax, ay = (a[1] - lon) * k, (a[0] - lat) * 110.57
    bx, by = (b[1] - lon) * k, (b[0] - lat) * 110.57
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, -(ax * dx + ay * dy) / L2))
    px, py = ax + t * dx, ay + t * dy
    return math.hypot(px, py)


def dist_to_prut_km(p: Place) -> float:
    return min(_seg_dist_km(p.lat, p.lon, PRUT_LINE[i], PRUT_LINE[i + 1]) for i in range(len(PRUT_LINE) - 1))


def eta_minutes(d_km: float) -> tuple[int, int]:
    """Interval ETA (min) în linie dreaptă: [reacție 450 km/h, piston 150 km/h]."""
    return (round(60 * d_km / V_JET_KMH), round(60 * d_km / V_SLOW_KMH))
