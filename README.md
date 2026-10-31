# Detecția dronelor și avertizare timpurie pentru Iași

*Brainstorming documentat · 31 octombrie 2026 · după incursiunile din 8 septembrie și 31 octombrie*

## Concluziile, pe scurt

1. **Avertizarea reală pentru Iași vine din amonte, dar pe canale oficiale, nepublice.** RO-Alert a plecat practic odată cu primele știri moldovenești (31.10: primul articol MD la 16:57, RO-Alert la 17:04) sau înaintea lor (8.09: niciun articol MD înainte de RO-Alert). Pe 12.09, alerta din Botoșani a pornit explicit de la o semnalare a centrelor de operații aeriene din Ucraina și R. Moldova. Cu surse publice, un sistem civil **nu va bate RO-Alert-ul** pentru public.
2. **Singurul semnal public timpuriu e ucrainean și e nespecific.** Cu datele oficiale pe raioane, alerta aeriană din regiunea ucraineană de plecare era activă la **toate cele 8** detecții moldovenești analizate (pornită cu 12 min – 7 h înainte). Dar e activă ~20% din timp (medie ian.–sept.; în octombrie, mai des): bun ca **stare de vigilență internă** (reduce de ~5 ori timpul de pândă), nu ca alarmă publică.
3. **Senzorii locali dau secunde–minute:** o rețea acustică (2–5 km rază) dă ~30–80 s pentru o dronă cu piston și ~10–25 s pentru una cu reacție (care au fost cel puțin 2 din cazurile din 2026). Rolul lor: confirmare, localizare, documentare, date pentru autorități.
4. **Legal, un civil sau un ONG poate:** asculta surse publice, face detecție pasivă (acustic, optic spre cer, Remote ID, ADS-B), publica cronologii și raporta la 112. **Nu poate:** bruia, folosi radar fără licență ANCOM, intercepta comunicații sau emite alerte care imită RO-Alert.
5. **Start recomandat:** un bot care arhivează cu oră exactă toate semnalele UA/MD/RO (cost aproape zero) și dă vigilență internă + cronologii publice; un pilot cu 3–5 noduri acustice împreună cu o universitate; apoi presiune pe autorități pentru alerte pe zone mai mici, cu durată și încetare explicită, și pentru senzori instituționali pe Prut (SAFE, EDDI, Eastern Flank Watch).

## Ce s-a întâmplat

| | 8 septembrie 2026 | 31 octombrie 2026 |
|---|---|---|
| Drone | 1 (cu reacție, după fragmente) | 2 (tipul nedeclarat oficial) |
| Ruta | reg. Odesa → Transnistria → Chișinău → Ungheni → Iași → înapoi în MD | (1) reg. Odesa → Rîbnița → Telenești → Călărași; (2) reg. Vinnița → Soroca → Edineț → spre Botoșani |
| Primul semnal public | UA: 16:09–16:12 (alertă Odesa, „curs nord-vest”); primul articol MD: după RO-Alert | primul articol MD: 16:57 (detecția MD fusese la 16:24); a doua dronă: 17:50 |
| RO-Alert | Iași 16:30–16:37, apoi încă 4 județe | Iași 17:04, Neamț 17:27, Vaslui 17:53, Botoșani 18:10, Bacău 18:15, Suceava 18:44 |
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
| Vigilență | alerte UA pe raioane: Odesa, Vinnytsia, Chernivtsi (alerts.in.ua, ukrainealarm) | 10 min – ore; activă ~20% din timp |
| Direcție | Forțele Aeriene UA (@kpszsu), @warningodesa – **doar intern**, nu republicați | ~20 min (8.09) |
| Confirmare din amonte | Armata Națională a R. Moldova (army.md), presa MD | **0–7 min** (publicare la ~ora RO-Alert) |
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
| [09-evenimente-2026](docs/09-evenimente-2026.md) | anexă: incidentele din RO și MD, ian.–oct. 2026, cu ore |
| [10-senzori-acustici-amplasare](docs/10-senzori-acustici-amplasare.md) | cum arată senzorii acustici, reguli de amplasare, zone în jurul Iașului, acorduri necesare |
| [analysis/](analysis/) | scriptul care leagă detecțiile moldovenești și incidentele de alertele ucrainene + [rezultate](analysis/rezultate.md) |

## Limitări

- Majoritatea surselor de presă au fost consultate prin rezumate de căutare, nu citite integral. Unde relatările diferă, sunt puse una lângă alta.
- Orele din comunicate sunt orele *evenimentelor*; orele de publicare le-am măsurat doar pentru 8.09 și 31.10, din fragmente de căutare.
- Datele ucrainene oficiale pe raioane se opresc (în copia publică de azi) la 7.09.2026; după aceea avem doar date de voluntari, care subestimează.
- Cifrele de performanță ale produselor sunt declarații ale producătorilor.
- Secțiunea juridică nu e consultanță juridică.
- Documentul se limitează la detecție și alertare: fără metode de bruiaj, interceptare sau neutralizare.
