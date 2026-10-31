# 06 · Rețele civile de detecție și lecții din alte țări

*Stare: 31.10.2026. Unde scrie „neconfirmat”, n-am găsit o sursă verificabilă în această sesiune.*

## Pe scurt

1. **Rețelele care funcționează sunt integrate cu statul.** Sky Fortress (Ucraina) e o rețea acustică ieftină, dar valoarea vine din densitate, fuziune centrală și legătura directă cu cine reacționează. Datele nu sunt publice.
2. **Există deja un precedent civic în UE:** Drone Rada (Lituania, iunie 2026) – telefoane Android vechi la fereastră, ascultă motoarele de tip Shahed, voluntari verificați, cod deschis.
3. **Raportarea cetățenească (ePPO) merge doar cu identitate verificată, agregare centrală și fără output public.**
4. **Alertarea publică rămâne oficială.** Modelul israelian (zone mici, pre-alertă, încetare explicită) e reperul de cerut autorităților, nu de imitat de un ONG.
5. **Țările baltice și Polonia au descoperit aceleași goluri:** drone nedetectate până la impact, alerte târzii pe arii mari, nevoia de senzori ficși la graniță.

## 1. Ucraina

### Sky Fortress (Небесна фортеця) – rețea acustică
- Rețea de senzori acustici ieftini (inițial telefoane pe stâlpi), cu procesare locală a sunetului și transmitere către un sistem central care estimează traiectoria și o trimite grupurilor mobile de foc.
- Scară: **~9.500 de telefoane/senzori** ([ITC.ua](https://itc.ua/en/news/in-ukraine-9-500-phones-detect-shaheds-by-sound-and-transmit-air-defense-data)); alte surse spun peste 10.000. Cost raportat: câteva sute de USD pe nod (detalii și verificare în [03-senzori](03-senzori-echipamente.md)).
- Lituania a ales tehnologia acustică ucraineană pentru 2026 ([Euromaidan Press, 29.07.2025](https://euromaidanpress.com/2025/07/29/lithuania-to-deploy-ukrainian-drone-detection-system-by-2026-after-russian-airspace-violations/); [Ukrainska Pravda](https://www.pravda.com.ua/eng/news/2025/07/29/7523876)).
- **Lecția:** nodul ieftin nu e suficient; contează rețeaua densă, calibrarea pe teren și cine primește datele.

### ePPO – raportare cetățenească
- Lansată în octombrie 2022 (anunț al serviciului de informații militare HUR): utilizatorul alege tipul țintei, îndreaptă telefonul spre ea și apasă un buton; aplicația trimite poziția și direcția ([Mezha, 2022](https://mezha.media/en/2022/10/14/eppo-a-mobile-application-for-informing-about-cruise-missiles-and-kamikaze-drones)).
- Autentificare (raportată prin Diia), agregare centrală, niciun output public.
- Cifre de utilizare pentru 2026: neconfirmate.
- **Lecția:** multe rapoarte slabe devin o estimare de traiectorie doar dacă sunt agregate, filtrate și legate de identitate. Fără asta, aplicația devine o țintă pentru trolli.

### Canalele de monitorizare
- Rapide și detaliate, dar anonime, uneori greșite, uneori manipulate. În Ucraina, publicarea în timp real a mișcărilor țintelor și a apărării antiaeriene e incriminată (art. 114-2 CP UA).
- **Lecția pentru Iași:** folosiți-le intern; publicați doar agregat și cu întârziere.

## 2. Lituania: Drone Rada (exemplul cel mai apropiat de ce s-ar putea face la Iași)

- Lansată pe **19.06.2026** de un start-up împreună cu activiști ([LRT](https://www.lrt.lt/en/news-in-english/19/2965205/lithuanian-startup-launches-open-source-network-to-detect-shahed-type-drones); [Tom's Hardware](https://www.tomshardware.com/tech-industry/drones/acoustic-mapping-app-uses-thousands-of-networked-old-android-phones-to-hunt-shahed-drones-crowd-sourced-microphone-network-spots-small-low-rcs-military-targets)).
- Cum funcționează: voluntari **verificați** pun un telefon Android nefolosit, conectat la priză, lângă fereastră. Aplicația analizează continuu sunetul ambiental după semnăturile de joasă frecvență ale motoarelor de tip Shahed. Detecțiile alimentează o hartă în timp real.
- Țintă: 10.000 de participanți (obiectiv, nu cifră atinsă). Se discută montarea senzorilor pe turnurile operatorilor de telefonie.
- Probleme ridicate public: dacă aplicația înregistrează continuu sunetul (viața privată).
- Separat, Lituania a testat un sistem de detecție în jurul orașului Kaunas pe 25–26 mai 2026 ([Intellinews](https://www.intellinews.com/lithuania-tests-shahed-like-drone-detection-system-444797/)).

**De reținut pentru Iași:** modelul e replicabil, dar trebuie ales de la început cine vede harta (public vs. autorități), cum se verifică voluntarii și cum se garantează că nu se stochează audio.

## 3. Polonia, 9–10 septembrie 2025

- Radarele poloneze și aliate au urmărit **11–20 de obiecte**; premierul Tusk a vorbit de **cel puțin 19 drone**, multe venite dinspre Belarus. Incursiunea a durat ~7 ore (23:30–06:30). Cel puțin 3 (probabil 4) au fost doborâte de F-16 poloneze și F-35 olandeze; o casă a fost distrusă de resturi, fără victime ([Ukrainska Pravda](https://www.pravda.com.ua/eng/news/2025/09/10/7530122); [Notes from Poland](https://notesfrompoland.com/2025/09/10/poland-shoots-down-russian-drones-that-entered-its-airspace-in-unprecedented-violation/)).
- O parte erau momeli Gerbera. Polonia a invocat articolul 4 NATO; a urmat operațiunea Eastern Sentry.
- **Lecții:** saturația cu momeli ieftine cere detecție stratificată și clasificare rapidă; aeroporturile se închid preventiv (exact ca Iașul pe 8.09.2026).

## 4. Țările baltice, 2026

- Din martie 2026, drone ucrainene deviate (prin război electronic rusesc, după oficialii baltici și NATO) au căzut în Lituania, Letonia și Estonia: prima pe 23.03 în Lituania; un coș de fum lovit la centrala Auvere (Estonia). Pe 19.05, un avion NATO a doborât o dronă deasupra Estoniei; pe 20.05, aeroportul din Vilnius a fost închis după o dronă urmărită dinspre Belarus ([Wikipedia](https://en.wikipedia.org/wiki/2026_Ukrainian_drone_incursions_into_the_Baltic_states); [OSW](https://www.osw.waw.pl/en/publikacje/analyses/2026-03-25/baltic-states-respond-to-incidents-involving-ukrainian-drones)).
- **Cel puțin 15 incidente în 2026** până la 21 mai, față de 9 în tot 2025 ([Novaya Gazeta Europe](https://novayagazeta.eu/articles/2026/05/21/at-least-24-drone-incidents-recorded-in-the-baltic-states-since-start-of-2025-en-news)).
- Unele drone **n-au fost detectate până la impact**; o analiză oficială letonă a găsit lipsuri în avertizarea timpurie și în detecție.
- Răspunsuri: Estonia a pornit pe 30.05 primii senzori ficși de detecție pe granița cu Rusia ([Euromaidan Press](https://euromaidanpress.com/?p=408888)); Letonia planifică acoperire anti-dronă automatizată pe granița de est ([The Defense Post, 22.07.2026](https://thedefensepost.com/2026/07/22/latvia-automated-anti-drone-border/)).
- **Lecția:** chiar și state NATO cu radare moderne au nevoie de un strat de senzori ficși, ieftini, la graniță. Pentru Iași, granița e Prutul.

## 5. Israel: modelul de alertare publică (de cerut autorităților)

- Țara e împărțită în **~1.600 de zone de alertă (poligoane)**, micșorate în timp pentru precizie ([Breaking Defense, feb. 2025](https://breakingdefense.com/2025/02/smaller-polygons-and-cell-alerts-how-israels-home-front-command-honed-its-civilian-alert-system/)).
- **Pre-alerte** în 2025: mesaje cu câteva secunde (lângă graniță) până la ~2 minute înainte de sirene, prin aplicație, platforma de mesaje, portalul național și Telegram. Avertisment explicit: o pre-alertă poate să nu fie urmată de sirenă, iar sirena poate veni fără pre-alertă ([JNS](https://www.jns.org/analysis/the-purpose-is-to-provide-additional-preparation-time)).
- **Ce să cereți DSU/IGSU:** alertă pe zone mai mici decât județul; pre-alertă în două trepte; mesaj explicit de încetare; o hartă publică a zonelor. Mesajul RO-Alert din 31.10.2026 nu avea nici zonă, nici durată.

## 6. R. Moldova: radarele de care depinde avertizarea Iașului

- Primul radar Thales Ground Master 200 a sosit în decembrie 2023 (rază ~250 km, ~14 mil. €). Ministrul Apărării a spus public că nu oferă protecție completă ([Radio Moldova](https://radiomoldova.md/c/en/13/41)).
- Al doilea radar, pentru drone, finanțat prin Facilitatea Europeană pentru Pace (~20 mil. €), era programat pentru prima jumătate a lui 2026 ([IPN](https://ipn.md/en/second-drone-detection-radar-will-be-operational-in-2026-confirms-7965_1111052.html)). Intrarea în funcțiune: **neconfirmată**.
- Alertare publică prin cell broadcast (MD-ALERT, ~5 mil. €): licitație în pregătire în aug. 2026, operațională estimat în 2027.
- **Schimbul de date oficial există:** pe 12.09.2026, RO-Alert-ul din Botoșani a pornit de la o semnalare a centrelor de operații aeriene din Ucraina și R. Moldova ([Mediafax](https://www.mediafax.ro/social/ro-alert-in-botosani-sambata-dupa-amiaza-o-drona-s-a-prabusit-intr-o-localitate-din-judetul-suceava-formand-un-crater-23806064)), iar pe 8.09 RO-Alert a plecat înaintea detecției radar românești. Detaliile protocolului nu sunt publice.
- **Implicație:** calitatea avertizării pentru Iași depinde direct de radarele moldovenești și de canalul militar MD → RO, nu de presa moldovenească (care publică abia la ~ora RO-Alert).

## 7. Rețele comunitare care au funcționat (modele de organizare)

| Rețea | Ce face | Ce se poate copia | Ce NU se copiază |
|---|---|---|---|
| **Blitzortung** | localizează fulgere prin TDOA, cu senzori de voluntari sincronizați GPS | arhitectura: noduri ieftine + timp GPS + procesare centrală; acces complet la date doar pentru contribuitori | – |
| **ADS-B (OpenSky, ADS-B Exchange)** | receptoare de voluntari, multilaterație | stimulente pentru voluntari (acces la date) | publicarea în timp real a tot ce se vede |
| **Sensor.Community, uRADMonitor (RO)** | calitatea aerului, kituri DIY | ușurința montajului, flag-uri de calitate | datele complet publice |
| **Drone Rada (LT)** | acustic, telefoane vechi | totul – e cel mai apropiat model | – |

## 8. Inițiative din România

- **Spectrum Hive** (Suceava, echipa conf. dr. Alexandru Lavric, Universitatea „Ștefan cel Mare”): start-up pentru analiza spectrului radio și **detecția RF a dronelor** ([IEEE](https://events.vtools.ieee.org/m/570554)). Componenta acustică nu e confirmată. Partener regional natural pentru un pilot.
- Universitatea Politehnica București: cercetare pe localizarea surselor radio pentru detecția dronelor (teze de doctorat, SDR).
- Canale civice dedicate (Telegram/Facebook) în Galați, Tulcea sau Iași: **n-am găsit** niciunul documentat.
- Firme românești cu produse de detecție (Optoelectronica 2001/Skylock, Qognifly, OVES): vezi [04-produse-programe](04-produse-programe.md).

## 9. Cum se evită alarmele false și dezinformarea

**Separarea rolurilor:** rețeaua civică detectează și agregă; statul alertează. Rețeaua nu trimite niciodată „adăpostiți-vă”.

**Scor de încredere** (exemplu):

| Factor | Efect |
|---|---|
| Coroborare: câte noduri / surse independente | crește încrederea |
| Plauzibilitate cinematică (viteză 40–130 m/s, direcție coerentă) | elimină avioane (ADS-B), drone legale (Remote ID), motociclete |
| Context din amonte (alertă UA, detecție MD) | crește prioritatea |
| Rapoarte cetățenești | ponderate după reputație și identitate verificată |
| Vechimea semnalului | scade încrederea |

**Surse frecvente de confuzie:** acustic – mopede, drujbe, motocoase, tractoare, ultraușoare, paramotoare; vizual noaptea – planete, sateliți Starlink, lampioane, baloane; RF – drone civile legale.

**Dezinformare:** capturi false „RO-Alert”, canale Telegram clonate (nume aproape identice), valuri coordonate de „rapoarte”. Contramăsuri: surse fixate prin ID, mesaje postate doar de bot, educarea publicului („RO-Alert vine ca mesaj de sistem pe telefon, nu ca imagine”), detecția valurilor anormale de conturi noi.

**Oboseala alertelor:** alerte precise geografic, încetare explicită, cronologie publică după incident (ar fi lămurit discrepanțele de oră de la 8.09: 16:30 / 16:37 / 16:47).
