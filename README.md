# Detecția dronelor și avertizare timpurie pentru Iași

*Brainstorming documentat · 31 octombrie 2026 · după incursiunile din 8 septembrie și 31 octombrie*

## Concluziile, pe scurt

1. **Minutele de avertizare vin din amonte, nu din senzori locali.** Lanțul real: alertă aeriană în Ucraina → detecție anunțată de Armata R. Moldova → RO-Alert. Pe 8 septembrie: alertă Odesa 16:12 → detecție MD 16:20 → RO-Alert ~16:37 → drona intră în România la 16:37. Pe 31 octombrie: detecție MD 16:24 → RO-Alert Iași 17:04 (+40 min).
2. **Am măsurat pe date reale:** în toate cele 3 incidente din 2026 cu traseu terestru prin sudul Ucrainei / R. Moldova, alerta ucraineană pentru regiunea Odesa era deja activă (pornită cu 8–94 min înainte). **Dar** alerta din Odesa sună aproape zilnic (1.979 de alerte în 2026, ~9,5% din timp) – e un filtru de vigilență, nu un motiv de alarmă publică.
3. **Senzorii locali dau secunde–minute:** o rețea acustică (2–5 km rază) dă ~40–100 s pentru o dronă cu piston și ~15–40 s pentru una cu reacție. Rolul lor: confirmare, localizare, documentare – nu avertizare.
4. **Legal, un civil sau un ONG poate:** asculta surse publice, face detecție pasivă (acustic, optic spre cer, Remote ID, ADS-B), publica cronologii și raporta la 112. **Nu poate:** bruia, folosi radar fără licență ANCOM, intercepta comunicații sau emite alerte care imită RO-Alert.
5. **Start recomandat:** un bot OSINT care arhivează cu oră exactă toate semnalele UA/MD/RO din prima zi (cost aproape zero), apoi un pilot cu 3–5 noduri acustice împreună cu o universitate, apoi lobby pentru senzori instituționali pe Prut (SAFE, EDDI, Eastern Flank Watch).

## Ce s-a întâmplat

| | 8 septembrie 2026 | 31 octombrie 2026 |
|---|---|---|
| Drone | 1 (cu reacție, după fragmente) | 2 (tipul nedeclarat oficial) |
| Ruta | reg. Odesa → Transnistria → Chișinău → Ungheni → Iași → înapoi în MD | (1) reg. Odesa → Rîbnița → Telenești → Călărași; (2) reg. Vinnița → Soroca → Edineț → spre Botoșani |
| Primul semnal public | alertă UA Odesa 16:12; detecție MD 16:20 | detecție MD 16:24; a doua dronă 17:50 |
| RO-Alert | Iași ~16:37, apoi încă 4 județe | Iași 17:04, Neamț 17:27, Vaslui 17:53, Botoșani 18:10, Bacău 18:15, Suceava 18:44 |
| Aeronave | 2 F-18 spaniole | 4 F-16 + 1 elicopter |
| Aeroportul Iași | zboruri suspendate | spațiu aerian închis temporar, o cursă deviată la Suceava |
| Final | prăbușită în MD (Mihăilenii Vechi) | fără prăbușiri raportate |

Detalii și surse: [docs/01-incidente.md](docs/01-incidente.md).

## Ce echipament, pentru cine

| Cine | Ce | Cost orientativ |
|---|---|---|
| Cetățean | RO-Alert activ; aplicația OpenDroneID sau un receptor ESP32 pentru Remote ID; raportare la 112 | 0–100 € |
| ONG / universitate | bot OSINT (Nivel A); 3–5 noduri acustice cu GPS și LTE (Nivel B); receptoare Remote ID | 0 € → ~300–600 €/nod |
| Primărie / Consiliu Județean / Aeroport | camere termale îndreptate de senzori; radar autorizat ANCOM; plan de incident EASA; protocol cu ISU/MApN | zeci de mii → milioane € |

Detalii: [docs/03-senzori-echipamente.md](docs/03-senzori-echipamente.md), [docs/04-produse-programe.md](docs/04-produse-programe.md).

## Sursele care contează

| Treaptă | Sursă | Avans tipic |
|---|---|---|
| Vigilență | alerte UA pe regiuni/raioane: Odesa, Vinnytsia, Chernivtsi (alerts.in.ua, ukrainealarm) | 10–90 min, foarte nespecific |
| Direcție | Forțele Aeriene UA (@kpszsu) – **doar intern**, nu republicați | 15–60 min |
| Confirmare din amonte | Armata Națională a R. Moldova: detecții și restricții de spațiu aerian; presa MD | 10–40 min (de măsurat cu ce întârziere apar online) |
| Oficial | RO-Alert, MApN, ISU Iași, Prefectura | 0 |
| Istoric / calibrare | setul public de alerte UA (GitHub, zilnic); jurnalul propriu | – |

Detalii: [docs/02-surse-predictie.md](docs/02-surse-predictie.md).

## Documente

| Fișier | Conținut |
|---|---|
| [01-incidente](docs/01-incidente.md) | cronologiile 8.09 și 31.10, ferestrele de avertizare, alte incidente 2026 |
| [02-surse-predictie](docs/02-surse-predictie.md) | date măsurate (alerte UA vs. incidente), rate de bază, ETA, toate sursele |
| [03-senzori-echipamente](docs/03-senzori-echipamente.md) | acustic, RF, radar, optic/termic; liste de materiale; ce e realist |
| [04-produse-programe](docs/04-produse-programe.md) | produse comerciale, firme românești, SAFE / EDDI / Eastern Flank Watch |
| [05-cadru-legal](docs/05-cadru-legal.md) | ce e permis, cui, cu ce autorizații |
| [06-retele-civile-lectii](docs/06-retele-civile-lectii.md) | Sky Fortress, Drone Rada, ePPO, Polonia, țările baltice, Israel, R. Moldova |
| [07-arhitectura-sistem](docs/07-arhitectura-sistem.md) | arhitectura pe 3 niveluri, modelul de scor, mesaje, KPI |
| [08-plan-actiune](docs/08-plan-actiune.md) | primii pași, întrebări pentru autorități, ce să nu faceți |
| [analysis/](analysis/) | scriptul care leagă incidentele de alertele ucrainene + rezultate |

## Limitări

- Majoritatea surselor de presă au fost consultate prin rezumate de căutare, nu citite integral. Unde relatările diferă, sunt puse una lângă alta.
- Orele din comunicate sunt orele *evenimentelor*; momentul în care devin publice e încă nemăsurat.
- Cifrele de performanță ale produselor sunt declarații ale producătorilor.
- Secțiunea juridică nu e consultanță juridică.
- Documentul se limitează la detecție și alertare: fără metode de bruiaj, interceptare sau neutralizare.
