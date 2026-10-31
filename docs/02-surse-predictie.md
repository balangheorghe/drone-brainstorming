# 02 · Surse de date pentru predicție și avertizare timpurie

*Stare: 31.10.2026. Ore: RO, MD și UA au același fus orar (EEST = UTC+3 până la 25.10.2026, EET = UTC+2 după). Seturile de date sunt în UTC.*

## Pe scurt

- **Minutele de avertizare pentru Iași vin din amonte**: Ucraina (alerte aeriene, Forțele Aeriene) → R. Moldova (detecții, restricții de spațiu aerian) → România (RO-Alert, MApN).
- **Am măsurat** (vezi §1): în toate cele 3 incidente din 2026 cu traseu terestru prin sudul Ucrainei / R. Moldova, alerta aeriană ucraineană pentru regiunea Odesa era deja activă, pornită cu **8–94 de minute** înainte. În cele 2 cazuri venite de pe mare (Sulina), nu era.
- **Dar alerta din Odesa singură nu e un predictor**: în 2026 a sunat de **1.979 de ori**, în 293 din 304 zile, și e activă **~9,5% din timp**. E un *filtru* (când tace, riscul pe ruta prin Moldova e mic), nu un declanșator.
- **Semnalul cel mai specific e moldovenesc**: detecția anunțată de Armata Națională și restricția de spațiu aerian pe zone (nord/centru). Nu știm încă cu ce întârziere ajung public (vezi §3.4).
- **Ruta nordică (reg. Vinnița → nordul R. Moldova → Botoșani, sau direct spre Botoșani/Suceava)** are alt semnal din amonte: alertele din Vinnytsia și Chernivtsi. A doua dronă din 31.10 a venit exact pe aici (intrată în MD dinspre reg. Vinnița la 17:50, ieșită spre Botoșani la 18:12). În octombrie 2026 aceste alerte au explodat: Chernivtsi **103** (față de ~13/lună în prima jumătate a anului), Vinnytsia **225** (față de ~30/lună).

## 1. Ce arată datele măsurate

Sursa: setul public [Vadimkin/ukrainian-air-raid-sirens-dataset](https://github.com/Vadimkin/ukrainian-air-raid-sirens-dataset) (licență MIT, actualizat zilnic, ore UTC). Conține alertele oficiale (la nivel de raion din dec. 2025, până la 07.09.2026 în copia de azi) și alertele colectate din canalul eTryvoga (la nivel de regiune, până la 31.10.2026 03:24 UTC). Pentru că eTryvoga e un canal Telegram, marcajul de timp e chiar momentul publicării: exact ce ar „vedea” un sistem automat.

Scriptul care reproduce tot: [`analysis/ua_alerts_analysis.py`](../analysis/ua_alerts_analysis.py); rezultatul complet: [`analysis/rezultate.md`](../analysis/rezultate.md).

### 1.1 Alertele ucrainene în jurul incidentelor din 2026

| Incident (oră locală) | Traseu | Alertă UA activă în momentul incidentului? | Cu cât a pornit înainte |
|---|---|---|---|
| 29.05, Galați, impact (~01:50) | sud, spre Dunăre (traseu exact nepublicat) | **DA** – raioanele Izmail, Bilhorod-Dnistrovskyi, Bolhrad | **~94 min** |
| 16.08, intrare în RO dinspre MD (04:44) | reg. Odesa → R. Moldova → Galați | **DA** – reg. Odesa (Izmail, Bilhorod-Dnistrovskyi, Bolhrad) | **~58–59 min** |
| 08.09, detecție MD, drona spre Iași (16:20) | reg. Odesa → Transnistria → Ungheni → Iași | **DA** – reg. Odesa | **~8 min** (pornită la 16:12) |
| 15.10, Sulina, contact radar (01:34) | Marea Neagră | nu (doar Mykolaiv) | – |
| 17.10, Sulina, intrare (~17:59) | Marea Neagră | nu (ultima alertă Odesa se încheiase cu ~2 h înainte) | – |
| 21.10, Tulcea, RO-Alert (~03:30) | Delta | nu în acel minut (alertă Odesa 02:53–03:02, apoi din nou la 03:38) | parțial |
| 31.10, drona 1, detecție MD (16:24) | reg. Odesa → Rîbnița → Telenești → Călărași | *datele apar în set abia mâine* | – |
| 31.10, drona 2, intrare în MD (17:50) | reg. Vinnița → Soroca → Edineț → Botoșani | *idem* | – |

**Ce înseamnă:** pentru ruta *terestră* prin Moldova, alerta din Odesa a fost o condiție necesară în toate cazurile observate (3/3). Pentru ruta *maritimă* nu ajută. Eșantionul e mic; scriptul trebuie rulat la fiecare incident nou.

### 1.2 Cât de des sună alerta (rate de bază 2026, 1 ian. – 31 oct.)

| Regiune UA | Alerte | Zile cu alertă | % din timp cu alertă activă |
|---|---|---|---|
| Odesa | 1.979 | 293 | 9,5% |
| Mykolaiv | 2.565 | 298 | 14,9% |
| Vinnytsia | 584 | 188 | 3,6% |
| Chernivtsi | 218 | 98 | 4,9% |
| oricare: Odesa, Vinnytsia, Chernivtsi | – | – | 15,8% (25,8% în octombrie) |

La nivel de raion (date oficiale, până la 7 sept.): raioanele din sud (Izmail, Bilhorod-Dnistrovskyi, Bolhrad) au alertă activă ~11,6% din timp; cele din nord, lângă Transnistria (Podilsk, Rozdilna), ~5,9%.

**Calcul de alarme false:** 1.979 de alerte Odesa față de 2 RO-Alert-uri de dronă la Iași în același an. Un mesaj public la fiecare alertă din Odesa ar fi greșit în >99,9% din cazuri. De aceea, nivelul „alertă UA activă” rămâne **intern** (stare de vigilență a sistemului), nu mesaj public.

### 1.3 Tendință: alertele se mută spre vest

| Lună 2026 | Odesa | Vinnytsia | Chernivtsi |
|---|---|---|---|
| ian.–iun. (medie) | ~146 | ~31 | ~13 |
| iul. | 288 | 25 | 5 |
| aug. | 320 | 37 | 4 |
| sept. | 283 | 114 | 31 |
| oct. | 209 | 225 | 103 |

Creșterea din Vinnytsia și Chernivtsi în septembrie–octombrie se potrivește cu incidentele noi din nordul României (Solca, Suceava, 24.09; alertele din Botoșani/Suceava). Pentru Iași contează și această rută, nu doar cea prin Moldova.

## 2. Cinematică: cât timp avem

| Tip | Viteză (surse) | Observații |
|---|---|---|
| Gerbera (momeală) | ≤150–160 km/h | zbor foarte jos raportat |
| Shahed-136 / Geran-2 (piston) | ~150–185 km/h croazieră | cifra uzuală ~185 km/h maxim |
| Geran-3 (reacție) | 300–370 km/h (HUR, sept. 2025) | estimarea timpurie de 550–600 km/h a fost revizuită |
| „Geran cu reacție” (8.09 și 17.10.2026) | **~400–470 km/h implicit** din orele publice | estimare proprie, eroare mare; MApN a confirmat „cu reacție” pe 17.10 |

**Regula de proiectare:** ETA se dă mereu ca interval, cu **450 km/h** pentru limita de jos (cazul cu reacție observat în 2026) și **150 km/h** pentru limita de sus.

**ETA până la Iași** (minute; distanță în linie dreaptă, deci limită inferioară):

| Punct | km | 150 km/h | 185 km/h | 370 km/h | 450 km/h |
|---|---|---|---|---|---|
| Vinnytsia | 240 | 96 | 78 | 39 | 32 |
| Izmail | 222 | 89 | 72 | 36 | 30 |
| Chernivtsi | 177 | 71 | 57 | 29 | 24 |
| Podilsk | 159 | 64 | 52 | 26 | 21 |
| Rîbnița | 125 | 50 | 41 | 20 | 17 |
| Chișinău | 97 | 39 | 31 | 16 | 13 |
| Țibirica (ultimul punct, 31.10) | 64 | 26 | 21 | 10 | 9 |
| Ungheni (Prut) | 16 | 6 | 5 | 3 | 2 |

## 3. Sursele, una câte una

### 3.1 Ucraina – alerte oficiale (T-90…T-10 min, nespecifice)

| Sursă | Ce dă | Acces | Note |
|---|---|---|---|
| **alerts.in.ua API** | alerte active pe regiune, raion, hromadă | token (formular pe site sau api@alerts.in.ua); client Python oficial `alerts-in-ua` (PyPI); limite de ~8–12 cereri/min per IP raportate în documentație (de reverificat) | proiect independent; cel mai simplu de integrat |
| **api.ukrainealarm.com** (aplicația oficială „Повітряна тривога”) | alerte pe regiuni, plus **webhook** | token la cerere | webhook = latență minimă; istoricul păstrat e scurt (raportat 168 h, neconfirmat) → arhivați voi |
| **Vadimkin/ukrainian-air-raid-sirens-dataset** (GitHub) | istoric complet 2022–azi, CSV | liber (MIT), actualizat zilnic | pentru calibrare și backtest (folosit în §1) |
| NEPTUN / mapa.ua / war-monitor | hărți cu traiectorii estimate | termeni neconfirmați | doar confirmare umană |

Regiuni de urmărit: **Odesa** (Podilsk, Rozdilna – nordul, spre Transnistria; Izmail, Bilhorod-Dnistrovskyi, Bolhrad – sudul), **Vinnytsia** (Mohyliv-Podilskyi, la granița cu MD), **Chernivtsi** (ruta spre Botoșani/Suceava).

### 3.2 Ucraina – Forțele Aeriene și canale de monitorizare (direcție, dar cu restricții)

- **@kpszsu** (Telegram, canalul oficial al Forțelor Aeriene): mesaje de tipul „БпЛА … курсом на …” (dronă cu cursul spre…) și bilanțul de dimineață. De la ~mai 2026 publică mai puține detalii. Există canale false care îl imită: fixați **ID-ul numeric** al canalului, nu numele.
- **Canale de voluntari** (de ex. @war_monitor, ~960 mii abonați): rapide, dar anonime, neauditate, uneori greșite; unele pot fi manipulate.
- **Atenție legală:** în Ucraina, publicarea în timp real a mișcărilor țintelor e incriminată (art. 114-2 CP UA). **Folosiți-le doar intern, ca semnal; nu le republicați.**
- Ingestie: previzualizarea publică `t.me/s/<canal>` (fără cont, unele canale o dezactivează) sau un client MTProto (Telethon, cont dedicat). Conformitatea cu termenii Telegram trebuie verificată (vezi [05-cadru-legal](05-cadru-legal.md)).

### 3.3 R. Moldova (T-40…T-10 min, cel mai specific semnal)

- **Ministerul Apărării / Armata Națională**: comunicate despre detecții („Serviciul Operații Aeriene monitorizează…”), mai ales pe Facebook, preluate rapid de presă (ZdG, TV8, Pro TV Chișinău, Moldpres, Ziar.md, NordNews).
- **Restricțiile de spațiu aerian pe zone** (nord/centru) sunt anunțate cu oră exactă; se văd și indirect, în ADS-B (zborurile civile de la Chișinău se opresc).
- **Volum:** R. Moldova a raportat **65 de încălcări** ale spațiului aerian în 2026 (17 doar în octombrie). Doar 2 au dus la RO-Alert la Iași. Deci și acest semnal trebuie combinat cu direcția (spre vest / spre Prut).
- Moldova **nu are încă alertare publică prin cell broadcast** (MD-ALERT e planificat pentru 2027).

### 3.4 Problema nerezolvată: *când* devin publice semnalele moldovenești

Orele din comunicate sunt orele *evenimentelor* (16:24 detecția, 16:46 restricția). Momentul în care textul ajunge online poate fi mult mai târziu: pe 31.10, actualizarea ZdG despre „dispariția de pe radar” (16:54) pare publicată pe la ~17:10, **după** RO-Alert-ul de la 17:04. Până nu măsurăm asta, „~40 de minute avans” e o limită teoretică. **Prima sarcină a oricărui sistem: să arhiveze cu oră de primire fiecare mesaj, din prima zi.**

### 3.5 România (T-5…0, confirmare)

- **RO-Alert**: cell broadcast, emis de autorități (IGSU/ISU/DSU, cu suport tehnic STS). Nu am găsit un feed public; soluția practică e un telefon Android dedicat care jurnalizează mesajele.
- **MApN**: comunicate pe mapn.ro / english.mapn.ro, preluate de Agerpres.
- **ISU Iași, Prefectura Iași, DSU**: pagini oficiale de social media (vezi [08-plan-actiune](08-plan-actiune.md) pentru verificarea lor ca surse).
- **ADS-B, trafic civil**: avioane în așteptare sau deviate la Iași (LRIA), oprirea zborurilor la Chișinău (LUKK). Surse: adsb.lol (fără limită de rată deocamdată, ODbL), OpenSky (credite zilnice), ADS-B Exchange (contra cost). **Nu urmăriți și nu publicați mișcări de aeronave militare.**

### 3.6 Context de „zi de atac” (H-ore)

- Bilanțurile @kpszsu (câte drone, câte cu reacție) și analizele lunare ISIS / CSIS dau nivelul general de activitate.
- **Ora din zi:** ambele incidente de la Iași au fost **după-amiaza (16:20–17:05)**, nu noaptea. Pe Dunăre domină noaptea și dimineața devreme. Sistemul trebuie să meargă 24/7.
- **Meteo** (Open-Meteo, gratuit pentru uz necomercial): vânt și plafon de nori pe rută, ca factor secundar.

## 4. Stiva de predicție recomandată

| Treaptă | Semnal | Ce face sistemul | Public? |
|---|---|---|---|
| **H** (ore) | zi/noapte de atac masiv în sudul/vestul UA | crește vigilența | nu |
| **T-90…T-10** | alertă activă în Odesa / Vinnytsia / Chernivtsi (Mohyliv-Podilskyi) | stare „vigilență” – filtru (activă ~10–26% din timp) | nu |
| **T-60…T-15** | @kpszsu: „curs spre” Podilsk / Rozdilna / Izmail / Moldova | ipoteză de traseu, ETA | nu (restricție legală UA) |
| **T-40…T-10** | MD: detecție + restricție de spațiu aerian + direcție vest | ipoteză confirmată, ETA, scor | intern; public doar după calibrare (vezi [07-arhitectura](07-arhitectura-sistem.md)) |
| **T-10…0** | RO-Alert / MApN / anomalii la LRIA / senzori locali | confirmare, retransmitere oficială | **da, doar retransmiterea mesajelor oficiale** |

**Regulă:** sistemul civic nu anticipează public RO-Alert până nu are o precizie măsurată pe date proprii. Până atunci, valoarea lui e: vigilență internă, jurnal precis, cronologii publicate după incident și date pentru autorități.
