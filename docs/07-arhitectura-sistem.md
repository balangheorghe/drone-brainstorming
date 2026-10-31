# 07 · Arhitectura unui sistem de predicție și avertizare pentru Iași

*Stare: 31.10.2026. Scop: detecție, urmărire, predicție, alertare. Fără bruiaj, interceptare sau neutralizare. Sistemul stochează totul în UTC.*

## Pe scurt

- **Trei niveluri de ambiție**, construite pe aceeași magistrală de date:
  - **A. Bot de fuziune OSINT** (2–6 săptămâni, cost aproape zero): citește sursele publice UA/MD/RO, ține un jurnal precis, calculează ETA și un scor, anunță *intern*.
  - **B. Rețea comunitară de senzori** (3–9 luni, mii de euro): A + noduri acustice, Remote ID, o cameră termală – pentru confirmare și localizare.
  - **C. Strat instituțional** (1–3 ani): B + senzori autorizați (radar), integrare cu ISU și aeroportul, finanțare publică.
- **Regula de aur:** sistemul civic **nu emite alerte publice de tip „adăpostiți-vă”** și nu anticipează public RO-Alert până nu are o precizie măsurată. Public: doar retransmiterea mesajelor oficiale și cronologii după incident.
- **Primul lucru de făcut:** arhivarea cu oră de primire a tuturor semnalelor, din ziua 1. Fără ea nu se poate calibra nimic.
- **Așteptări realiste (măsurate):** sursele publice moldovenești apar la ~ora RO-Alert (31.10: 16:57 vs. 17:04; 8.09: după). Doar semnalele ucrainene vin clar mai devreme (10–90+ min), dar sunt nespecifice. Valoarea sistemului e vigilența internă, jurnalul și confirmarea locală – nu „minute câștigate” față de RO-Alert pentru public.

## 1. Diagrama

```
 AMONTE (probabilitate)              LOCAL (confirmare)          OFICIAL (autoritate)
 +--------------------------+      +-----------------------+    +----------------------+
 | UA: alerts.in.ua (REST)  |      | Niv. B: noduri acustice|   | RO-Alert: telefon    |
 | UA: ukrainealarm webhook |      |  (GPS, ML pe nod)     |    |  Android dedicat     |
 | UA: @kpszsu (doar intern)|      | Remote ID (ESP32)     |    | MApN / ISU / Prefect.|
 | MD: presă RSS, MApN MD   |      | cameră termală (cue)  |    +----------+-----------+
 | ADS-B civil: LUKK, LRIA  |      | Niv. C: radar autoriz.|               |
 | Istoric: dataset GitHub  |      +-----------+-----------+               |
 +------------+-------------+                  |  doar detecții            |
              v                                v                           v
 +--------------------------------------------------------------------------------+
 |  Colectori Python  ->  ARHIVĂ BRUTĂ (text, published_at, received_at, hash)      |
 +-------------------------------------+------------------------------------------+
                                       v
       NLP (uk/ru/ro, toponime) -> ipoteze de traseu -> ETA + scor -> nivel intern
                                       v
                        OPERATOR (om în buclă) – jurnal de decizii
                     /                 |                         \
       grup închis (operatori,   retransmitere publică      cronologie publică
       parteneri, ISU pe bază    a mesajelor OFICIALE       după incident (24–48 h)
       de protocol)              (RO-Alert, MApN, ISU)
```

## 2. Ingestia (Nivel A)

| # | Sursă | Conector | Rol |
|---|---|---|---|
| 1 | alerts.in.ua | REST cu token, polling ~10–15 s (sub limita de rată) | vigilență (UA) |
| 2 | ukrainealarm API | webhook cu token | vigilență, redundanță |
| 3 | @kpszsu, @warningodesa | `t.me/s/<canal>` (previzualizare publică activă) sau Telethon cu cont dedicat; **ID numeric fixat** | direcție – **doar intern** |
| 4 | army.md („Informează!”), presă MD (Unimedia, ZdG, Realitatea.md, TV8, IPN, Newsmaker), agregatorul news.yam.md | RSS unde există / scraping la 30–60 s | detecții și restricții MD (publicate la ~ora RO-Alert) |
| 5 | MApN, Agerpres, ISU Iași, Prefectura Iași | RSS / scraping | confirmare oficială |
| 6 | RO-Alert | telefon Android dedicat. Atenție: alertele de urgență ajung doar la aplicația de sistem pentru cell broadcast, nu la aplicații obișnuite. De testat: o aplicație care citește *notificarea* afișată de sistem (NotificationListenerService), `adb logcat` pe un telefon conectat la un Raspberry Pi, sau confirmare manuală a operatorului | adevărul de referință pentru KPI |
| 7 | ADS-B civil (adsb.lol, OpenSky) | REST, geofence LUKK + LRIA | anomalii de trafic (oprire, așteptare, deviere) |
| 8 | Istoric UA (GitHub, zilnic) | descărcare CSV | calibrare, backtest |
| 9 | Meteo (Open-Meteo) | REST | factor secundar; vânt pentru senzorii acustici |

Lista extinsă de surse (canale OVA, `t.me/air_alert_ua` fără cheie, RSSHub, adsb.fi, NOTAM, meteo, hărți de bază): [11-fluxuri-date-harti](11-fluxuri-date-harti.md).

**Ce NU se ingerează:** poziții de aeronave militare, rapoarte cetățenești automate (doar prin operator), surse fără identitate verificabilă.

## 3. NLP și toponime

1. Detectarea limbii (uk / ru / ro) și normalizare (ș/ş, ț/ţ, transliterare chirilică).
2. Cuvinte-cheie: *БпЛА, шахед, реактивн-, курсом на, у напрямку* (uk); *БПЛА, герань, в направлении* (ru); *dronă, țintă aeriană, spațiu aerian restricționat, a dispărut de pe radar, RO-Alert, încetarea alertei* (ro).
3. Gazetteer cu variante uk/ru/ro/en: raioanele din reg. Odesa (Podilsk, Rozdilna, Bilhorod-Dnistrovskyi/Cetatea Albă, Izmail, Bolhrad, Berezivka), Vinnytsia (Mohyliv-Podilskyi), Chernivtsi; raioanele din R. Moldova de pe rutele observate (Rîbnița, Telenești, Călărași, Ungheni, Rîșcani, Orhei, Strășeni, Nisporeni, nordul); localitățile de pe Prut din județele Iași și Botoșani.
4. Extragere: *(tip, număr, loc, direcție, oră, sursă, încetare)*. Toponimele nerezolvate (de ex. „Semionovca”, „Slavianorebca”) se marchează și nu intră în calculul ETA.

## 4. Ipoteze de traseu și stări

| Stare | Când | Public? |
|---|---|---|
| S0 Fond | implicit | – |
| S1 Vigilență | alertă activă în Odesa / Vinnytsia / Chernivtsi | nu |
| S2 Direcție UA | @kpszsu sau surse UA: „curs spre” Moldova / Podilsk / Izmail / Mohyliv-Podilskyi | nu |
| S3 Moldova | detecție anunțată de MD sau restricție de spațiu aerian (o sursă oficială sau două de presă) – publicate de obicei la ~ora RO-Alert | nu (intern) |
| S4 Apropiere | ultima poziție MD în jumătatea vestică, curs spre Prut, ETA Iași ≤ 30 min; sau anomalie la LRIA | nu (intern; grup închis) |
| S5 Oficial | RO-Alert înregistrat sau comunicat MApN | **da: retransmitere** |
| S6 Încheiat | încetare oficială sau decădere | **da: încetare + cronologie** |

Mai multe ipoteze pot exista simultan (pe 3.10.2026, Moldova a raportat 5–6 zboruri în ~15 minute). Un eveniment nou se atașează unei ipoteze doar dacă distanța e compatibilă cu viteza maximă (450 km/h) și timpul scurs.

## 5. ETA și scor

```
d        = distanța (haversine) de la ultima poziție la țintă (Prut, Iași, LRIA)
ETA_min  = 60 * d / 450      # cazul cu reacție observat în 2026 (8.09, 17.10)
ETA_max  = 60 * d / 150      # piston, croazieră prudentă

logit P  = logit(p0[stare])
         + b1 * alerta_UA_activă              (0/1)
         + b2 * curs_spre_Moldova_UA          (0/1)
         + b3 * restricție_spațiu_aerian_MD   (0/1)
         + b4 * max(0, cos(unghi curs - direcția spre Iași))
         + b5 * exp(-d_Prut / 30 km)
         + b6 * anomalie_ADS-B_civil          (0/1)
fiecare termen decade în timp: x * exp(-(t - t_obs) / tau),  tau ≈ 20–45 min
```

**Onestitate:** coeficienții sunt deocamdată inventați. Cu 2 evenimente la Iași nu se poate calibra nimic. Calibrarea se face pe **toate** încălcările spațiului aerian moldovenesc (65 în 2026) și pe toate RO-Alert-urile de dronă din NE și SE, legate de istoricul alertelor UA (vezi [02-surse-predictie](02-surse-predictie.md) §1). Până atunci, scorul doar **ordonează** ipotezele. Primul punct de sprijin măsurat: alerta UA pe raioane era activă la 8/8 detecții moldovenești, dar e activă ~20% din timp → raport de verosimilitate de ordinul 4–5 pentru termenul `alerta_UA_activă`.

**De ce nivelurile de pre-alertă rămân interne:** 65 de încălcări moldovenești → 2 RO-Alert-uri la Iași. Un „ATENȚIE” public la fiecare detecție moldovenească ar fi greșit în ~97% din cazuri; unul la fiecare alertă din Odesa, în >99,9%. Asta produce oboseală și neîncredere – exact opusul scopului.

## 6. Mesaje (șabloane)

Reguli: nume și design care **nu** seamănă cu RO-Alert sau cu o instituție; prefix „[NEOFICIAL]”; oră + sursă în fiecare mesaj; corecții publice; nicio instrucțiune care contrazice autoritățile; niciodată capturi de ecran RO-Alert.

> **[INTERN] VIGILENȚĂ · 16:12 EEST (8.09).** Alertă UA activă în reg. Odesa; monitorizare UA: drone cu reacție, curs nord-vest. ETA maxim spre Iași dacă intră în MD: ~20–60 min. Fără acțiune publică.

> **[INTERN] ATENȚIE · 16:58 EET (31.10).** Presa MD (16:57): dronă detectată la 16:24, restricție în nord la 16:46; poziție publicată: zona Telenești/Bănești. ETA Prut 7–21 min, Iași 9–28 min (estimare, linie dreaptă). Scor necalibrat. Verificați RO-Alert, pregătiți retransmiterea. *(În realitate, RO-Alert a venit la 17:04.)*

> **[NEOFICIAL] RETRANSMITERE · 17:04 EET.** Autoritățile au emis RO-Alert pentru [zona din mesaj]. Textul oficial: „[citat]”. Urmați doar instrucțiunile oficiale. Observațiile se raportează la 112.

> **[NEOFICIAL] ÎNCETARE · HH:MM.** Autoritățile au anunțat încetarea alertei (sursa, ora oficială). Nu atingeți fragmentele; anunțați-le la 112.

> **[NEOFICIAL] CRONOLOGIE · a doua zi.** Ce s-a știut și când: UA 16:12, MD 16:20, RO-Alert 16:30/16:37… (cu surse și discrepanțe).

## 7. Alarme false, om în buclă, securitate

- **Regula celor două surse** (sau o sursă oficială) pentru S3; surse identificate prin ID, nu prin nume (există canale clonate).
- **Mod umbră 30–90 de zile:** sistemul rulează și măsoară, nu publică nimic în afară de retransmiteri.
- **Echipă realistă:** 24/7 cu voluntari nu e realist. Automatizați arhivarea și starea internă; omul intervine doar pentru mesajele publice. Retransmiterea RO-Alert poate avea întârziere de câteva minute fără pagubă: oamenii au primit deja mesajul pe telefon.
- **Securitate:** cont Telegram dedicat cu 2FA, secrete separate, backup zilnic, MQTT doar cu TLS și autentificare per nod (Nivel B). Dacă se integrează cu Aeroportul Iași, intră sub NIS2.
- **OPSEC:** nu se publică traiectorii UA, poziții de senzori, aeronave militare sau hărți de impact imediat după eveniment.

## 8. Stivă tehnică

| Nivel | Minimum (A) | Extins (B/C) |
|---|---|---|
| Colectori | Python (asyncio), `alerts-in-ua`, Telethon / `t.me/s`, feedparser | idem + MQTT de la noduri |
| Stocare | SQLite sau PostgreSQL | PostgreSQL + PostGIS + TimescaleDB |
| Fuziune | un serviciu Python cu reguli versionate în git | idem + TDOA/azimut pentru senzori |
| Interfață | bot Telegram (grup închis + canal public) | + Grafana intern, consolă operator |
| Găzduire | 1 VPS mic în UE (ordin de mărime 5–20 €/lună, verificați) + un telefon Android în Iași | 2 VPS la furnizori diferiți + rezervă locală |
| Edge | – | Raspberry Pi 5 / ESP32-S3, GPS PPS, router LTE |

## 9. Cele trei niveluri

| | A. Bot OSINT | B. Rețea comunitară | C. Instituțional |
|---|---|---|---|
| Durată | 2–6 săptămâni | 3–9 luni | 1–3 ani |
| Câștig | minute (din amonte), jurnal, cronologii | secunde–minute: confirmare, localizare, documentare | detecție 24/7 pe orice vreme |
| Cost | timp + VPS + telefon | ~300–600 €/nod acustic + carcasă/alimentare; < 100 €/nod Remote ID; câteva mii € pentru o cameră termală (vezi [03](03-senzori-echipamente.md)) | radar profesional: zeci–sute de mii €; sistem complet de aeroport (cu neutralizare): ~10 mil. € (presă) |
| Echipă | 1–2 dezvoltatori, 1 cititor uk/ru | + inginer audio/ML, electronist, DPO, universitate | + integrator, jurist, operațiuni (eventual la ISU) |
| Cerințe legale | disclaimer, fără date personale | DPIA dacă acoperă spațiul public, procesare pe nod, doar benzi radio permise, acord în zona de frontieră | licență ANCOM pentru radar, NIS2/CER, plan EASA de incident |

## 10. KPI (după modul umbră)

| KPI | Definiție |
|---|---|
| Avans față de RO-Alert | mediană și p10 pentru `t_RO-Alert − t_primul semnal S3` |
| Latență de ingestie | p50/p95 pentru `received_at − published_at` |
| Precizie S3/S4 | fracțiunea urmată de RO-Alert în NE în ≤ 90 min |
| Recall | fracțiunea de RO-Alert-uri din NE precedate de S3/S4 |
| Integritate | mesaje publice retrase pentru sursă falsă: țintă 0 |

Pragul pentru a face publică o treaptă de pre-alertă: se decide **după** aceste cifre, împreună cu ISU, nu înainte.

## 11. Partajarea cu autoritățile

- Observațiile cetățenilor merg la **112**. Fluxul OSINT **nu** merge la 112.
- Propuneți un **protocol scris** cu ISU Iași / Prefectura: ce se trimite (raport structurat, oră UTC, sursă, incertitudine), când (doar S4 sau detecții de senzori confirmate), pe ce canal (punct de contact dedicat), temei GDPR.
- Oferiți MApN jurnalele post-eveniment; nu trimiteți zgomot.
- Cereți autorităților: alertare pe zone mai mici decât județul, pre-alertă în două trepte, mesaj explicit de încetare (mesajul din 31.10 nu avea nici zonă, nici durată).
