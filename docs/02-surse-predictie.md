# 02 · Surse de date pentru predicție și avertizare timpurie

*Stare: 31.10.2026. Ore: RO, MD și UA au același fus orar (EEST = UTC+3 până la 25.10.2026, EET = UTC+2 după). Seturile de date sunt în UTC.*

## Pe scurt (ce am măsurat)

1. **Alerta ucraineană pe raioane e un filtru bun, nu o alarmă.** La **toate cele 8** detecții anunțate de R. Moldova în 2026 pentru care avem date oficiale pe raioane, alerta aeriană era deja activă în regiunea ucraineană de unde venea drona, pornită cu **12–424 de minute** înainte (de obicei 30–110). Dar alerta e activă **~19% din timp** în regiunea Odesa și **~22%** dacă adăugăm Vinnytsia și Chernivtsi. Folosită ca „stare de vigilență”, reduce de ~5 ori timpul de pândă fără să rateze cazurile observate.
2. **Sursele publice moldovenești vin prea târziu ca să bată RO-Alert.** Pe 31.10, drona a fost detectată la 16:24, dar primul articol moldovenesc a apărut la **16:57**, cu ~7 minute înaintea RO-Alert-ului de la 17:04. Pe 8.09, **niciun** articol moldovenesc nu a apărut înainte de RO-Alert.
3. **RO-Alert e declanșat pe canale oficiale, nepublice, între instituții.** Pe 8.09, după orele publicate, RO-Alert (16:30) a plecat chiar înaintea detecției radar românești (16:33) – inferență din ore rotunjite; IGSU a vorbit de o dronă „în spațiul aerian al R. Moldova… spre Iași”. Pe 12.09, alerta din Botoșani a pornit de la o semnalare a centrelor de operații aeriene din Ucraina și R. Moldova. Deci autoritățile primesc deja datele din amonte.
4. **Singurele semnale publice care vin clar înaintea RO-Alert sunt ucrainene**: alerte pe raioane și mesaje de monitorizare de tipul „drone cu reacție … curs nord-vest” (8.09, la 16:09–16:11, cu ~20 de minute înainte). Sunt nespecifice și nu se republică.
5. **Ruta nordică (reg. Vinnița / Cernăuți → nordul R. Moldova → Botoșani)** e la fel de importantă ca ruta prin Transnistria: a doua dronă din 31.10 și cea din 23.10 au venit din reg. Vinnița; cele din 12.09 și 16.10 au intrat prin Soroca; cea din 24.09 a venit din reg. Cernăuți spre Solca.

**Ce înseamnă:** un sistem civil nu va da, cu surse publice, „40 de minute de avertizare” înaintea RO-Alert. Poate da: o stare de vigilență cu 20–90 de minute înainte (probabilistă, cu multe alarme false), un jurnal precis, confirmare locală și argumente pentru autorități.

## 1. Date măsurate

Sursa: setul public [Vadimkin/ukrainian-air-raid-sirens-dataset](https://github.com/Vadimkin/ukrainian-air-raid-sirens-dataset) (licență MIT, actualizat zilnic, ore UTC):
- **date oficiale** – din dec. 2025 pe **raioane**; în copia de azi se opresc la 07.09.2026;
- **date de voluntari** (canalul eTryvoga) – doar pe **regiuni**, până la 31.10.2026; **subestimează mult** alertele pe raioane (Odesa, mar.–sept.: 471 h față de 984 h în datele oficiale).

Pentru utilizare în timp real, datele pe raioane vin din API-urile alerts.in.ua și ukrainealarm (§3.1).

Script: [`analysis/ua_alerts_analysis.py`](../analysis/ua_alerts_analysis.py) · rezultate complete: [`analysis/rezultate.md`](../analysis/rezultate.md) · lista evenimentelor: [09-evenimente-2026](09-evenimente-2026.md).

### 1.1 Detecțiile moldovenești și alertele ucrainene (date oficiale pe raioane)

| Detecție MD (oră locală) | Venită dinspre | Alertă activă acolo? | Pornită cu | Raioane în alertă |
|---|---|---|---|---|
| 30.03, 21:29 – Comarivka → Orhei | reg. Odesa | DA | 32 min | Podilsk, Rozdilna, Berezivka |
| 13.05, 16:00 – dinspre Mohyliv-Podilskyi | reg. Vinnytsia | DA | ~7 h | 5 raioane, inclusiv Mohyliv-Podilskyi |
| 16.08, 04:31 – Etulia → Galați | reg. Odesa | DA | 46 min | Izmail, Bilhorod-Dnistrovskyi, Bolhrad |
| 17.08, 17:37 – Cuciurgan → Tiraspol | reg. Odesa | DA | 12 min | Podilsk, Rozdilna, Berezivka, Odesa |
| 20.08, 03:16 – Etulia | reg. Odesa | DA | ~2,7 h | toată regiunea |
| 24.08, 05:55 – dinspre Vinogradovka → Cahul → Galați | reg. Odesa | DA | 91 min | toată regiunea |
| 26.08, 17:38 – Palanca | reg. Odesa | DA | 36 min | nordul regiunii + Odesa |
| 27.08, 03:56 – 5 drone (regiune presupusă) | reg. Odesa | DA | 112 min | toată regiunea |
| 08.09, 16:20 – spre Bender → Iași | reg. Odesa | DA (date voluntari) | 8 min | (regiune) |

După 7 septembrie avem doar date de voluntari, care ratează alertele pe raioane: ele arată alertă activă doar în 2 din 8 cazuri (inclusiv 8.09). Cazurile 31.10 vor apărea în set de mâine.

### 1.2 Cât timp e activă alerta (rate de bază, 1.01–7.09.2026, date oficiale)

*Atenție: în septembrie–octombrie alertele din Vinnytsia și Chernivtsi s-au triplat (§1.3), deci acum filtrul e activ mai des decât arată media de mai jos.*

| Regiune UA | % din timp cu alertă în oricare raion |
|---|---|
| Odesa | 19,4% |
| Vinnytsia | 4,9% |
| Chernivtsi | 1,7% |
| oricare din cele trei | 21,8% |

Pe raioane: sudul Odesei (Izmail, Bilhorod-Dnistrovskyi, Bolhrad) ~11,6%; nordul, lângă Transnistria (Podilsk, Rozdilna, Berezivka) ~5,9%; raioanele Vinnytsia ~3,5–4,3%; Chernivtsi ~1,2–1,7%.

**Calcul grosier:** dacă alerta e activă la (aproape) toate detecțiile, dar doar ~20% din timp, atunci starea „alertă activă” face ca o detecție să fie de ~4–5 ori mai probabilă decât în medie. E un filtru util, dar cu 65 de încălcări moldovenești pe an și doar 2 RO-Alert-uri la Iași, o alertă publică bazată pe el ar fi aproape mereu falsă. Rămâne **stare internă**.

### 1.3 Tendința (date de voluntari, doar regiuni)

| Lună 2026 | Odesa | Vinnytsia | Chernivtsi |
|---|---|---|---|
| ian.–iun. (medie) | ~146 | ~31 | ~13 |
| sept. | 283 | 114 | 31 |
| oct. | 209 | 225 | 103 |

Alertele din Vinnytsia și Chernivtsi au crescut puternic în septembrie–octombrie, odată cu incidentele noi din nordul R. Moldova, Botoșani și Suceava.

### 1.4 Când devin publice semnalele

| | 8.09 | 31.10 |
|---|---|---|
| Primul semnal public UA relevant | 16:09–16:11 (live-blog: „drone cu reacție … Buialyk (Odesa), curs nord-vest”); alertă Odesa 16:12 | de verificat mâine (set de date, @kpszsu) |
| Detecția MD (ora evenimentului) | 16:20 | 16:24 |
| Primul articol moldovenesc observat | 16:56 (update; nimic înainte de 16:30) | **16:57** (Unimedia; actualizare ZdG) |
| RO-Alert Iași | 16:30 (MApN) / ~16:36–16:37 | **17:04** |
| Avans al semnalului public MD față de RO-Alert | **≤ 0** | **~7 min** (0 dacă cerem și direcția spre vest) |

Sursă: căutări pe orele de publicare ([Unimedia](https://unimedia.info/ro/news/723c8ad7ae628873/ultima-ora-o-drona-a-intrat-neautorizat-in-spatiul-aerian-al-moldovei-a-zburat-dinspre-odesa.html), [24tv](https://24tv.ua/ataka-droniv-7-veresnya-2026-kudi-letyat-bpla-karta-trivog_n3137666), [Radio Iași](https://www.radioiasi.ro/stiri/regional/ro-alert-in-judetul-iasi-populatia-avertizata-cu-privire-la-posibilitatea-caderii-unor-obiecte-din-spatiul-aerian/)). Orele vin din fragmente de căutare și pot fi ore de actualizare.

## 2. Cinematică: cât timp avem

| Tip | Viteză (surse) | Observații |
|---|---|---|
| Gerbera (momeală) | ≤150–160 km/h | zbor foarte jos raportat |
| Shahed-136 / Geran-2 (piston) | ~150–185 km/h | |
| Geran cu reacție (Geran-3/4) | estimări publice ~300–400 km/h; declarat până la 550–600 | cifrele diferă mult între surse; Geran-5 ~600 km/h (surse secundare) |
| Incidentele din 2026 (8.09, 17.10) | **~400–470 km/h implicit** din orele publice | estimare proprie; MApN a confirmat „cu reacție” pe 17.10 |

**Regulă:** ETA se dă ca interval, cu **450 km/h** pentru limita de jos și **150 km/h** pentru cea de sus.

**ETA până la Iași** (minute; linie dreaptă, deci limită inferioară):

| Punct | km | 150 km/h | 185 km/h | 370 km/h | 450 km/h |
|---|---|---|---|---|---|
| Vinnytsia | 240 | 96 | 78 | 39 | 32 |
| Izmail | 222 | 89 | 72 | 36 | 30 |
| Chernivtsi | 177 | 71 | 57 | 29 | 24 |
| Podilsk | 159 | 64 | 52 | 26 | 21 |
| Rîbnița | 125 | 50 | 41 | 20 | 17 |
| Chișinău | 97 | 39 | 31 | 16 | 13 |
| Țibirica (ultimul punct, 31.10) | 63 | 25 | 20 | 10 | 8 |
| Ungheni (Prut) | 16 | 6 | 5 | 3 | 2 |

## 3. Sursele, una câte una

### 3.1 Ucraina – alerte oficiale (vigilență: 10 min – câteva ore, nespecific)

| Sursă | Ce dă | Acces | Note |
|---|---|---|---|
| **alerts.in.ua API** | alerte active pe regiune, raion, hromadă, oraș | token prin formularul [alerts.in.ua/api-request](https://alerts.in.ua/api-request); client Python oficial [`alerts-in-ua`](https://pypi.org/project/alerts-in-ua); limite per IP (~8–12 cereri/min, după surse terțe) | cel mai simplu de integrat |
| **api.ukrainealarm.com** (aplicația oficială „Повітряна тривога”) | alerte pe regiuni, plus **webhook** | token la cerere | latență minimă; istoricul păstrat e scurt (neconfirmat) → arhivați voi |
| **Setul de date de pe GitHub** | istoric 2022–azi, CSV | liber (MIT), zilnic | calibrare, backtest (§1); datele publice au zgomot (duplicate, fus orar) – curățați |

Raioane de urmărit: **Odesa** – Podilsk, Rozdilna, Berezivka (spre Transnistria), Izmail, Bilhorod-Dnistrovskyi, Bolhrad (sud); **Vinnytsia** – Mohyliv-Podilskyi, Tulchyn (spre nordul MD); **Chernivtsi** – Dnistrovskyi (spre Briceni/Botoșani).

### 3.2 Ucraina – Forțele Aeriene și canale de monitorizare (direcție, cu restricții)

- **@kpszsu** (Forțele Aeriene; previzualizare publică [t.me/s/kpszsu](https://t.me/s/kpszsu)) și **@warningodesa** ([t.me/s/warningodesa](https://t.me/s/warningodesa)): mesaje de tipul „БпЛА … курсом на …”. Fixați **ID-ul numeric** (există canale clonate). De la ~mai 2026, Forțele Aeriene publică mai puține detalii.
- Canale de voluntari: rapide, dar anonime și neauditate.
- **Atenție legală:** în Ucraina, publicarea în timp real a mișcărilor țintelor e incriminată (art. 114-2 CP UA). **Doar intern; nu republicați.**

### 3.3 R. Moldova (confirmare, dar publică abia la ~ora RO-Alert)

- **Ministerul Apărării**: [army.md](https://www.army.md/ro/comunicate-de-presa/informeaza-34) → „Comunicate de presă”, seria „Informează!”; și Facebook. Nu am găsit canal Telegram oficial sau RSS.
- **Presa** (Unimedia, ZdG, Realitatea.md, Newsmaker, TV8, IPN, Moldpres) și agregatorul **news.yam.md** (ID-uri secvențiale, utile pentru ordonarea în timp).
- Restricțiile de spațiu aerian pe zone sunt anunțate cu oră; nu am găsit NOTAM-uri pentru aceste incidente (serviciul AIM: aim.moldatsa.md).
- **Volum:** 65 de încălcări în 2026 (17 în octombrie) → doar 2 RO-Alert-uri la Iași. Semnalul trebuie combinat cu direcția.
- Moldova nu are încă alertare publică prin cell broadcast: **MD-ALERT** (~5 mil. €) e în pregătire, cu licitație anunțată în aug. 2026.

### 3.4 România (oficial)

- **RO-Alert**: cell broadcast emis de autorități (IGSU/ISU/DSU, suport tehnic STS). Nu am găsit un feed sau o arhivă publică. Pe Android, alertele de urgență ajung doar la aplicația de sistem pentru cell broadcast, nu la aplicații obișnuite – jurnalizarea automată trebuie testată (vezi [07](07-arhitectura-sistem.md)).
- **MApN** (mapn.ro, english.mapn.ro), **ISU Iași**, **Prefectura Iași**, **DSU**: comunicate oficiale; contul exact al fiecăruia e de verificat.
- **ADS-B civil**: avioane în așteptare sau deviate la Iași (LRIA) – pe 31.10, cursa Eindhoven–Iași a fost deviată la Suceava; oprirea zborurilor la Chișinău (LUKK). Surse: adsb.lol, OpenSky. **Nu urmăriți și nu publicați aeronave militare.**

### 3.5 Context

- Bilanțurile Forțelor Aeriene UA și analizele lunare (ISIS, CSIS) dau nivelul general de activitate.
- **Ora din zi:** incidentele de la Iași au fost **după-amiaza (16:09–18:44)**; pe Dunăre domină noaptea. 24/7 obligatoriu.
- **Lumina:** pe 31.10 apusul la Iași a fost la ~16:55; RO-Alert-ul de la 17:04 a fost după apus, iar a doua dronă a zburat practic noaptea.

## 4. Stiva de predicție, realist

| Treaptă | Semnal | Avans față de RO-Alert (observat) | Ce face sistemul | Public? |
|---|---|---|---|---|
| **Vigilență** | alertă UA activă în raioanele de lângă MD | 10 min – ore; activă ~20% din timp | stare internă, ETA maxime | nu |
| **Direcție** | mesaje UA „curs spre” MD / nord-vest | ~20 min (8.09) | ipoteză de traseu | nu (restricție UA) |
| **Confirmare MD** | articol / comunicat MD cu direcție vest | 0–7 min | confirmă ipoteza | intern |
| **Oficial** | RO-Alert, MApN, ISU | 0 | retransmitere | **da, doar retransmiterea** |
| **Local** | senzori proprii, anomalii la LRIA | după RO-Alert, de obicei | confirmare, localizare, documentare | date pentru autorități; cronologie după incident |

**Regulă:** sistemul civic nu anticipează public RO-Alert. Valoarea lui: vigilență pentru cine are nevoie (operatori, instituții, voluntari), jurnal precis, cronologii publice după incident, date locale pentru autorități și argumente pentru o alertare oficială mai precisă.
