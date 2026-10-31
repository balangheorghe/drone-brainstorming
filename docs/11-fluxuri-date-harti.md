# 11 · Fluxuri de date și hărți de agregat

*Stare: 31.10.2026. Catalogul complet, cu 141 de surse (acces, cost, licență, actualizare, precauții), e în [12-catalog-surse](12-catalog-surse.md). Aici: ce să legați întâi și cum. „Neconfirmat” = n-am putut citi documentația la sursă (multe domenii au fost blocate din sesiune).*

## Pe scurt

- **Pre-avertizare (nespecifică, internă):** API-urile ucrainene de alertă (alerts.in.ua, ukrainealarm) + canalele Telegram oficiale ale Forțelor Aeriene și ale administrațiilor regionale Odesa, Cernăuți, Vinnița și raionului Izmail.
- **Confirmare:** army.md și Moldpres (R. Moldova), MApN, DSU, presa; RO-Alert doar printr-un telefon-receptor (nu are feed public).
- **Indicator de spațiu aerian:** traficul aerian civil (ADS-B) peste R. Moldova și la Iași – oprirea zborurilor se vede în timp real, fără să aștepți presa. **De testat** pe date istorice dacă apare mai devreme decât știrile.
- **Context:** vânt și inversiuni termice, fulgere, incendii din satelit, căderi de internet, știri la 15 minute.
- **Hărți de bază:** limite administrative RO/MD/UA, relief, OSM (stâlpi, castele de apă, drumuri zgomotoase), zonele UAS ROMATSA, acoperire mobilă, populație.
- **Afișare și livrare:** Grafana (intern), MapLibre/uMap (public, cu întârziere), TAK (echipă), Node-RED (colectare), ntfy/Telegram/Pushover (notificări), Meshtastic (rezervă fără internet).

## Ce arată măsurătorile (de ținut minte când citiți catalogul)

Pe 31.10, R. Moldova a restricționat spațiul aerian în nord la 16:46 și în centru la 16:52, dar primul articol a apărut la 16:57, iar RO-Alert la 17:04. Pe 8.09, nimic public din Moldova înainte de RO-Alert (vezi [02](02-surse-predictie.md) §1.4). Deci, pe surse publice:
- doar alertele ucrainene vin clar mai devreme (dar sunt nespecifice);
- presa moldovenească vine la ~ora RO-Alert;
- **ADS-B ar putea arăta închiderea spațiului aerian moldovenesc cu ~10 minute înaintea presei** (16:46 → 16:57) – ipoteză de verificat cu date istorice (OpenSky, adsb.lol), nu fapt.

## 1. Primele 12 surse de legat (în ordine)

| # | Sursă | Ce dă | Cum | Cost |
|---|---|---|---|---|
| 1 | **alerts.in.ua** | alerte pe regiune / raion / hromadă | REST `api.alerts.in.ua/v1`, client Python `alerts-in-ua`; token la cerere (descrieți scopul cu cuvintele voastre) | gratuit (neconfirmat) |
| 2 | **api.ukrainealarm.com** (aplicația oficială) | idem, redundanță | `/api/v3/alerts`, `/alerts/status`, `/regions`; cheie la cerere; interogați `/status` și cereți `/alerts` doar la schimbări | gratuit (neconfirmat) |
| 3 | **t.me/air_alert_ua** | canalul aplicației „Повітряна тривога” – toate alertele, **fără cheie** | RSSHub găzduit propriu (`/telegram/channel/air_alert_ua`) sau Telethon | gratuit |
| 4 | **@kpszsu**, **@warningodesa** | direcții ale grupurilor de drone | idem | gratuit – **doar intern** |
| 5 | **Odesa OVA** (`t.me/odeskaODA`), **Cernăuți OVA** (`t.me/chernivetskaODA`), **Izmail RDA** (`t.me/IzmailRDA`), Vinnița OVA (link de pe vin.gov.ua) | anunțuri oficiale regionale, inclusiv raioanele de lângă MD | idem; verificați periodic handle-urile (se schimbă odată cu șefii administrațiilor) | gratuit |
| 6 | **army.md** + **Moldpres** (RSS observat la `w.moldpres.md/config/rss.php?lang=eng`) | detecții, restricții și redeschideri de spațiu aerian în MD | scraping army.md; RSS Moldpres | gratuit |
| 7 | **Presa MD** (Unimedia, ZdG, Realitatea.md, IPN, TV8, NordNews pentru nord) + agregatorul **news.yam.md** | prima publicare (16:57 pe 31.10) | RSS unde există; altfel scraping politicos | gratuit |
| 8 | **ADS-B civil** – OpenSky (din 18.03.2026 doar OAuth2), adsb.lol, adsb.fi, airplanes.live | oprirea zborurilor la Chișinău, avioane în așteptare/deviate la Iași (LRIA) și Suceava (LRSV) | REST; un bbox ~25,5–30,5°E × 44,8–48,6°N = 1 credit/cerere la OpenSky | gratuit, necomercial |
| 9 | **Receptor ADS-B propriu în Iași** (docker-adsb-ultrafeeder) | independență de agregatori + credite suplimentare (OpenSky 8.000/zi pentru feederi) | RTL-SDR + Raspberry Pi | ~100–150 € (estimare) |
| 10 | **MApN** (comunicate, Facebook, preluări Agerpres), **DSU** (aplicație, canal WhatsApp, fiipregatit.ro) | confirmarea oficială românească | manual / prin presă (Facebook nu are API de citire) | gratuit |
| 11 | **Telefon-receptor RO-Alert** în Iași (ideal și în Botoșani, Suceava) | adevărul de referință | jurnal manual sau testarea unei aplicații care citește notificarea de sistem | un telefon vechi |
| 12 | **Open-Meteo** | vânt la 850/700 hPa, nori, istoric ERA5 | REST fără cheie; necomercial < 10.000 apeluri/zi; CC BY 4.0 | gratuit |

**Model de arhitectură gata făcut:** [Alert_Server](https://github.com/sergeiown/Alert_Server) (MIT) – un server Node.js care unifică alerts.in.ua, UkraineAlarm și Neptun și publică pe WebSocket.

## 2. Spațiu aerian și aviație (context, confirmare)

- **NOTAM:** EUROCONTROL EAD Basic (gratuit, manual, „nu pentru uz operațional”) pentru LRIA, LRSV, LRBC, FIR București și FIR Chișinău; ICAO API Data Service (doar 100 de apeluri gratuite); suplimentele AIP ale MoldATSA (aim.moldatsa.md).
- **EUROCONTROL NOP – portalul public:** știri despre restricții în rețeaua europeană.
- **EASA CZIB** (buletinul pentru zona de conflict Ucraina, valabil până la 31.01.2027) și **Safe Airspace** (Moldova la nivelul 2).
- **Zonele UAS ROMATSA** (flightplan.romatsa.ro/init/drones): hartă + fișiere `.shp/.json/.xlsx`; **OpenAIP** pentru CTR/TMA (neoficial).
- **GPSJam.org** și harta FR24 de bruiaj GPS: context zilnic despre războiul electronic în zona Mării Negre și a Moldovei.
- **AIS maritim** (pentru Galați–Tulcea–Sulina): aisstream.io (WebSocket, cheie gratuită, max. 3 conexiuni).

## 3. Context și verificare

| Sursă | La ce folosește | Notă |
|---|---|---|
| **Univ. Wyoming – sondaje aerologice** | inversiuni termice (schimbă raza senzorilor acustici) | text, zilnic |
| **ANM** (radar, avertizări) · **MeteoAlarm** (CAP RO, pistă) | ploaie, furtuni – alarme false acustice | API ANM neconfirmat |
| **Blitzortung** | tunete = alarme false | doar vizual; fără API public |
| **NASA FIRMS** (VIIRS) | incendii/impacturi după eveniment (Odesa, Izmail, MD, Delta) | ~3 h întârziere; MAP_KEY gratuit; toamna, multe arderi agricole |
| **Copernicus Data Space** (Sentinel-1/2) | verificarea locului unei prăbușiri, după zile | cont gratuit |
| **IODA**, **Cloudflare Radar** | căderi de internet regionale (lovituri asupra rețelei) | Cloudflare: CC BY-NC |
| **GDELT DOC/GEO 2.0**, **Google News RSS** | „semnal de știri” la 5–15 min | fără cheie |
| **Harta interactivă Europa Liberă Moldova**, Wikipedia (lista violărilor de spațiu aerian), [09-evenimente-2026](09-evenimente-2026.md) | istoric de incidente | verificați fiecare rând cu comunicatele |
| **Kaggle „Massive Missile Attacks on Ukraine”**, **ISIS** (analize lunare Shahed), UA AirDefense Tracker, setul de alerte de pe GitHub | tipare, calibrare | **atenție:** Forțele Aeriene UA nu mai publică numărul de rachete din 10.08.2026, iar numărul de Shahed nu mai apare consecvent din ~mai 2026 → folosiți alertele ca proxy |
| **ACLED** (API doar la nivelul Research), **UCDP** | analiză istorică | termeni restrictivi |

## 4. Hărți de bază și amplasare

- **Limite administrative:** geoBoundaries (RO/MD/UA, aceeași schemă; verificați licența fiecărui fișier); **HDX COD-AB** pentru raioanele și hromadele Ucrainei; limitele UAT de pe geo-spatial.org (cu cod SIRUTA) sau ANCPI INSPIRE pentru România; geodata.gov.md pentru Moldova. **Evitați GADM** pe o pagină publică (interzice redistribuirea).
- **Muncă manuală obligatorie:** corespondența dintre ID-urile de regiune din alerts.in.ua/ukrainealarm și codurile COD-AB – n-am găsit o tabelă oficială.
- **Relief:** Copernicus DEM GLO-30 (gratuit pe AWS, fără cont) – analize de vizibilitate pentru senzori și camere, culoare joase (Prut, Jijia, Bahlui).
- **OpenStreetMap:** extrase Geofabrik procesate local; Overpass doar ocazional (< 100 cereri/zi). Etichete utile: `man_made=mast|tower|water_tower` (montaj), `highway=primary`, `railway=rail`, `aeroway=aerodrome`, `landuse=industrial` (zgomot).
- **Acoperire mobilă:** ANCOM [aisemnal.ro](https://aisemnal.ro) (hartă, fără date descărcabile), OpenCelliD (CC BY-SA, cu token).
- **Populație:** GHSL GHS-POP (100 m, CC BY 4.0), INS TEMPO / RPL2021 pe UAT.

## 5. Afișare și livrare

| Rol | Unealtă | Notă |
|---|---|---|
| Colectare și normalizare | **Node-RED** (Apache-2.0) | n8n e gratuit doar pentru uz intern |
| Tablou intern | **Grafana** (panou Geomap) | doar cu autentificare, în spatele unui reverse proxy |
| Pagină publică | **MapLibre / Leaflet + PMTiles**, sau **uMap** | doar date agregate și întârziate |
| Analiză | **QGIS** (amplasare), **Kepler.gl** (istoric) | offline |
| Echipă de teren | **OpenTAKServer** + ATAK/iTAK/WinTAK | TLS + certificate client; pozițiile voluntarilor = date personale |
| Sediu | **Home Assistant** (integrare „Ukraine Alarm”) | lumini/sirenă internă, nu publică |
| Notificări | **ntfy** găzduit propriu (principal), **Telegram Bot** (rezervă; ~20 mesaje/min într-un grup), **Pushover** (coordonatori), signal-cli | fiecare mesaj: „NEOFICIAL – urmați RO-Alert/ISU” |
| Fără internet | **Meshtastic EU_868** (869,4–869,65 MHz, 10% duty cycle) | schimbați cheia implicită; fără uplink MQTT public |

**Ritm de interogare sugerat:** API-uri UA la 15–30 s (sau webhook); Telegram la 30–60 s; presa MD la 1 min; ADS-B la ~20–30 s; GDELT la 15 min; Google News la 5–10 min; Open-Meteo la 30–60 min; FIRMS la 1–3 h.

## 6. Ce NU folosiți și NU publicați

- **Poziții și traiectorii în timp real** ale dronelor sau ale apărării antiaeriene ucrainene, locuri de impact (art. 114-2 CP al Ucrainei; ajută țintirea). Public: doar agregat și cu întârziere.
- **Hărțile neoficiale de urmărire a Shahed-urilor** (NEPTUN, monitor, mapa.ua etc.): erori de minute, surse netransparente, termeni neclari. Cel mult indiciu intern; niciodată declanșator automat sau afișare publică.
- **Aeronave militare** (endpoint-uri „mil”, F-16 ridicate, AWACS, realimentare): excludeți-le la ingestie.
- **Interceptarea radio** (scanere pe frecvențe ATC sau militare): risc penal.
- **Surse ruse sau pro-ruse și canale anonime**: dezinformare; R. Moldova a dezmințit public falsuri de pe Telegram.
- **„RO-Alert” redistribuit pe WhatsApp**: IGSU a semnalat mesaje false în numele său.
- **Locațiile senzorilor proprii și hărți de infrastructură critică** suprapuse peste rutele dronelor.
- **Date personale** (fotografii cu oameni, adrese, coordonate exacte ale fragmentelor din rapoartele cetățenilor): doar la nivel de localitate, cu întârziere.
- **Licențe:** adsb.fi, airplanes.live și Open-Meteo gratuit = necomercial; Cloudflare Radar = CC BY-NC; NewsAPI gratuit interzis în producție; cheia de test Windy dă date aleatoare; Blitzortung nu dă date brute; scraping-ul Facebook/Google încalcă termenii; ODbL (OSM, adsb.lol istoric) și CC BY-SA (OpenCelliD) cer share-alike pentru baze derivate.

## 7. Ce a rămas neconfirmat

- Termenii și limitele oficiale alerts.in.ua și ukrainealarm (domeniile de documentație au fost blocate din sesiune).
- Canalele Telegram ale Vinnița OVA, Mykolaiv OVA și ale raioanelor Podilsk și Mohyliv-Podilskyi.
- Un canal Telegram oficial al Ministerului Apărării al R. Moldova; tabela de zboruri a aeroportului Chișinău; un portal NOTAM public MoldATSA.
- Canale oficiale Telegram/WhatsApp ale ISU Iași, Botoșani, Suceava (doar DSU are un canal WhatsApp anunțat).
- RSS-ul MApN și al presei din Iași (căutați `<link rel="alternate" type="application/rss+xml">` în sursa paginilor).
