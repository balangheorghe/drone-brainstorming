# 10 · Senzorii acustici: cum arată și unde pot fi puși

*Stare: 31.10.2026. Cifrele vin din presă și de la producători, nu din teste independente. „Estimare” = aproximare proprie. Documentul dă zone, nu locuri exacte: **locațiile reale ale senzorilor nu se publică**.*

## Pe scurt

- **Trei forme:** (a) un telefon Android vechi la fereastră; (b) o cutie mică pe un stâlp sau pe acoperiș, cu microfon sub burete și un mic calculator; (c) o „antenă de sunet” (reflector parabolic) sau un panou cu multe microfoane pe un turn de 10–12 m.
- **Unde:** cât mai sus (minimum 6 m, ideal 10–12 m), cu cer liber spre direcția dronelor, departe de drumuri, căi ferate, ventilatoare și pereți mari; pe dealuri, nu în văi; la 2–3 km unul de altul pe o linie, sau minimum 3–4 noduri dispuse în triunghi/patrulater pentru localizare.
- **Pentru Iași:** trei inele – linia Prutului (Bivolari → Gorban, plus nordul Botoșaniului), culoarul dintre Prut și oraș (Golăiești–Ungheni–Țuțora, Popricani, valea Jijiei) și dealurile din jurul orașului (Breazu, Copou, Repedea, Bucium, Galata/Cetățuia) plus zona aeroportului.
- **Atenție:** nimic în fâșia de 20 m de la frontieră; în zona de 30 km, întrebați în scris Poliția de Frontieră. Fără înregistrare audio brută (GDPR).

## 1. Cum arată

### (a) Telefon la fereastră – modelul Drone Rada (Lituania)

```
   fereastră
  ┌──────────┐
  │  ┌────┐  │   telefon Android vechi, în picioare,
  │  │ 📱 │  │   aplicația ascultă continuu
  │  └─┬──┘  │
  └────┼─────┘
       └── încărcător în priză
```

- Un smartphone vechi, pe pervaz sau lipit de geam, conectat permanent la încărcător. Nimic montat afară. Voluntarii sunt verificați ([LRT](https://www.lrt.lt/en/news-in-english/19/2989283/civic-initiative-turns-old-phones-into-drone-detectors-as-lithuania-fixates-on-air-defence); [TVP World](https://tvpworld.com/94421075/lithuanian-start-up-uses-old-phones-as-drone-detectors)).
- Cost: ~0 dacă ai telefonul. Rețeaua avea ~250 de dispozitive vara aceasta; ținta e 10.000.
- **Limită:** geamul atenuează sunetul și telefonul „aude” doar o parte din cer – e varianta de masă, nu cea mai bună acustic.

### (b) Cutie pe stâlp sau acoperiș – modelul Sky Fortress (Ucraina) și variantele DIY

```
        ☁  cer liber
     ( burete + „blăniță” )  ← protecție de vânt
          │ microfon / matrice
     ┌────┴─────┐
     │ cutie    │  ← IP65, ~30×30×5 cm (Sky Fortress)
     │ calcul.  │     telefon Android sau Raspberry Pi / ESP32
     │ GPS, LTE │     + baterie de rezervă
     └────┬─────┘
          │ stâlp ~2 m sau pe acoperiș (mai bine ≥ 6 m)
   ═══════╧═══════
```

- **Sky Fortress:** la început, **un telefon și un microfon pe un stâlp de ~1,8–2 m** ([FlightGlobal](https://www.flightglobal.com/military-uavs/how-ukraine-turned-mobile-phone-microphones-into-an-air-defence-network/159997.article)); senzorul e descris ca o **cutie de ~30×30×5 cm cu un telefon Android** ([Janes](https://www.janes.com/osint-insights/defence-news/weapons/ukraine-conflict-ukrainian-air-defence-employs-passive-sensors-for-detection-and-tracking)), cu baterie de rezervă ([DVIDS](https://dvidshub.net/publication/issues/72169)). Cost raportat 300–500 USD. Distanța dintre senzori: ~4–5 km (o singură sursă).
- **Variante DIY:**
  - [Batear](https://github.com/batear-io/batear): placă ESP32-S3 + un microfon MEMS, alerte prin LoRa sau Ethernet; „sub 15 USD”, testat doar pe înregistrări.
  - Raspberry Pi + matrice ReSpeaker cu 4 microfoane ([Sych-Tech](https://github.com/Sych-Tech), voluntari ucraineni), apoi o carcasă proprie rezistentă la apă și vânt.
  - [miniDSP UMA-16](https://www.minidsp.com/products/usb-audio-interface/uma-16-microphone-array): placă plată de **13 × 19,5 × 2,5 cm** cu 16 microfoane în grilă (dă și direcția).
- **Protecția de vânt e obligatorie:** buretele reduce zgomotul vântului cu ~10–25 dB, o „blăniță” cu ~25 dB, un „blimp” cu blană până la ~50 dB ([Broadcast Bridge](https://www.thebroadcastbridge.com/content/entry/11777/essential-things-to-know-about-microphone-windscreens?cat_id=131)). Zgomotul de vânt e cel mai mare exact în banda joasă a motorului Shahed.
- **Alimentare solară:** exemple din bioacustică – Pi Zero 2 W cu panou de 2,5 W și o baterie 18650, sau un kit de 10 W ([Hackster](https://www.hackster.io/news/this-self-contained-system-gathers-outdoor-sounds-for-ecological-research-7d8cc9fd1f98)). Pentru iarna din Iași trebuie testat; mai sigur e curent de la clădirea gazdă + o baterie tampon.

### (c) Pilon cu reflector sau panou mare – Zvook (Ucraina), Squarehead (Norvegia)

```
          ___
        /     \     reflector parabolic ~0,5 m
       |   •   |    (microfonul în focar)
        \_____/
           │
     ┌─────┴─────┐  cutie cu electronica
     └─────┬─────┘
           │  turn de telecomunicații, 10–12 m
           │
    ═══════╧═══════
```

- **Zvook:** „antenă de satelit pentru sunet”, pe turnuri GSM la 10–12 m, acoperire ~200°, rază declarată ~5 km pentru drone, ~1,6% alarme false, ~500 USD/stație; are nevoie doar de curent ([Espreso](https://global.espreso.tv/zvook-project-ukrainian-know-how-for-detecting-air-targets); [United24](https://united24media.com/defense-tech/ukraines-zvook-acoustic-system-tests-mobile-detection-of-low-flying-missiles-and-drones-21587)). Diametrul de ~0,5 m vine dintr-o singură sursă.
- **Squarehead Discovair G2+:** un panou plat „cât o cutie de pizza”, **128 de microfoane** și o cameră, ~8 kg, 24–48 V, IP65; montat orizontal (360°) sau vertical (rază mai mare) ([Squarehead](https://www.sqhead.com/drone-detection)). Preț nepublic.

## 2. Reguli de amplasare

| Regulă | De ce | Sursă |
|---|---|---|
| **Înălțime ≥ 6 m, ideal 10–12 m** | mai puține reflexii de la sol și pereți; sunetul trece peste case și copaci. Standardul ISO 20906 pentru monitorizarea zgomotului de avioane cere ≥ 6 m; Zvook folosește 10–12 m | [Dublin Airport (ISO 20906)](https://www.dublinairport.com/docs/default-source/corporate/portable-noise-monitoring-terminals-report.pdf) |
| **≥ ~7,5 m de pereți mari, ≥ ~3 m de copaci și stâlpi** | reflexii care strică semnalul | [LAWA](https://www.lawa.org/media/35871) |
| **Departe de zgomot**: drumuri, cale ferată, ferme cu utilaje, industrie, ventilatoare/aer condiționat pe acoperiș | zgomotul de joasă frecvență acoperă motorul dronei. Măsurați fondul sonor 3+ nopți (banda 100–1000 Hz) înainte de a alege | derivat |
| **Pe creastă sau versant spre culoarul de zbor, nu în vale** | un deal între senzor și traseu face „umbră acustică” | derivat; [IOA](https://www.ioa.org.uk/system/files/proceedings/dc_waddington_yw_lam_the_effect_of_weather_conditions_on_the_propagation_of_sound.pdf) |
| **Țineți cont de meteo** | noaptea, inversiunile termice duc sunetul mai departe (+5–10 dB); contra vântului apar zone de umbră | [BBA](https://www.bba.ca/publications/acoustic-measurements-the-effects-of-weather-on-sound-propagation) |
| **Vegetația contează puțin** pentru propagare (~0,02 dB/m la frecvențe joase), mai mult ca zgomot de frunze | | [USDA](https://www.fs.usda.gov/t-d/programs/im/sound_measure/helo_appendix5.shtml) |
| **Distanța dintre noduri pe o linie: 2–3 km** (cu suprapunere, ca o dronă să fie auzită de ≥ 2 noduri); linia perpendiculară pe rută; două linii paralele dau și sensul | | derivat din raza declarată de 2–5 km |
| **Pentru localizare (TDOA): ≥ 3–4 noduri necoliniare**, care înconjoară zona; GPS cu PPS pentru oră exactă | pe o singură linie, localizarea e proastă | derivat |
| **O alertă e validă doar dacă ≥ 2 noduri aud simultan** | elimină alarmele locale (tractor, motocoasă) | așa face și Drone Rada |
| **Redundanță**: puneți mai multe noduri decât minimul | unele cad în timp (lecția ShotSpotter) | [KPTV](https://www.kptv.com/2023/04/24/what-gunshot-detection-would-mean-portland) |

## 3. Unde, concret, în jurul Iașului (zone, nu locuri)

### Inelul A – linia Prutului

- **Județul Iași, de la nord la sud** (ordine aproximativă): Bivolari (Soloneț), Trifești, Victoria (Sculeni), **Golăiești (Petrești)** – în dreptul Zagarancea, unde a intrat drona pe 8.09 –, Ungheni, Țuțora, Prisăcani (Măcărești), Grozești, Gorban (confluența Jijia–Prut). Costuleni: de verificat ([lista localităților de pe Prut](https://en.wikipedia.org/wiki/Category:Populated_places_on_the_Prut)).
- **Botoșani (ruta nordică, 24.09 și 31.10):** Rădăuți-Prut, Ripiceni, Ștefănești, Santa Mare.
- **Lungime:** nepublicată pe județ; în linie dreaptă, frontul Iașului are ordinul a ~80 km (estimare). La 2–3 km între noduri: **~28–41 de noduri** pentru o singură linie; la 5 km, ~17.
- **De evitat:** vama Sculeni (cozi de camioane), podurile și șantierul A8 de la Ungheni, calea ferată Iași–Ungheni. În luncă, montați deasupra cotei de inundație (Victoria și Țuțora au fost afectate în 2020).
- **Rol:** confirmă că o dronă a trecut Prutul și în ce punct. Pentru orașul Iași (~15–20 km de Prut) dă doar ~2–5 minute.

### Inelul B – culoarul dintre Prut și oraș

- Interiorul comunelor Golăiești, Ungheni și Țuțora; Popricani (~16,5 km N); valea Jijiei între Victoria și Gorban; culoarul spre nord-vest (Iași → Botoșani), unde radarul a pierdut drona pe 8.09.
- **Rol:** direcția de deplasare după trecerea Prutului; 3–4 noduri aici, în triunghi, pot localiza.

### Inelul C – orașul și aeroportul

- Dealurile Iașului: **Breazu** (unde drona a fost văzută pe 31.10, neconfirmat oficial), Copou (N), **Repedea** (~350 m, S) și Bucium (>300 m, SE), Galata și Cetățuia (S). Zona aeroportului (~5–8 km E de centru), pe clădiri înalte din jur, nu pe pistă.
- **Rol:** confirmare deasupra orașului; dealurile sunt bune și pentru camere termale îndreptate de senzorii acustici.

### Pilotul recomandat (3–5 noduri)

Nu începeți cu linia completă pe Prut. Începeți cu **3–5 noduri în estul orașului**, în triunghi pe axa Golăiești – Ungheni – Țuțora și pe un deal (Breazu sau Copou), pe clădiri publice sau ale unei universități:
- acoperă rutele documentate (8.09: Golăiești; 31.10: Breazu/Lețcani);
- permit localizarea (nu sunt pe o singură linie);
- strâng primele luni de sunete locale (tractoare, trenuri, avioane, furtuni) pentru antrenarea clasificatorului;
- sunt în afara fâșiei de frontieră.

## 4. Cine trebuie să-și dea acordul

| Loc | Pe cine întrebați |
|---|---|
| Primărie, școli, cămine culturale | primăria (pentru domeniul public poate fi nevoie de o hotărâre a consiliului local); conducerea școlii |
| Turle de biserici | parohia + Arhiepiscopia Iașilor |
| Castele de apă | operatorul regional de apă |
| Turnuri de telecomunicații | **proprietarul turnului** (de ex. Vantage Towers, Digi, Orange), nu neapărat operatorul. Din oct. 2025, Telekom Mobile a fost împărțit între Digi și Vodafone ([Digi](https://www.digi-communications.ro/en/see-file/DIGI_Press-release_-Closing-TKRM-Transaction.pdf)). Un ONG nu are drept legal de acces; e negociere |
| Catarge noi | urbanismul primăriei: dacă e nevoie de autorizație de construire (Legea 50/1991) |
| Curent | de la clădirea gazdă, cu acord scris (consumul e de câțiva wați); un racord separat nu merită |

**Frontiera de stat** ([OUG 105/2001](https://legeaz.net/oug-105-2001-frontiera-de-stat/art-7-dispozitii-generale-regimul-juridic-al-frontierei-de-stat); [HG 445/2002](https://www.politiadefrontiera.ro/files/docu/1475063994447-hg445.pdf)):
- **fâșia de protecție: 20 m** de la linia de frontieră; accesul acolo cere aprobarea Poliției de Frontieră → **nu montați nimic acolo**;
- **zona de frontieră: 30 km** în interior (include localitățile de pe Prut și, probabil, o parte din Iași) → cereți în scris punctul de vedere al ITPF Iași / sectorului local (Bivolari, Tomești etc.) pentru orice nod.

**GDPR:** autoritatea belgiană a considerat că vocea captată de senzorii de zgomot ai orașului Anvers e dată personală ([PwC Legal](https://www.pwclegal.be/en/news/voices-as-personal-data--belgian-dpa-challenges-antwerp-s-noise-.html)). Deci: clasificare pe dispozitiv, **fără audio brut stocat sau transmis**, doar evenimente (oră, scor, direcție); DPIA; informare scrisă pentru proprietar. Un filtru de frecvență nu e suficient – banda motorului se suprapune cu vocea.

## 5. Checklist pentru un loc

1. ☐ Înălțime ≥ 6 m (ideal 10–12 m), cer liber spre est / nord-est.
2. ☐ ≥ 7,5 m de pereți mari, ≥ 3 m de copaci; fără ventilatoare în apropiere.
3. ☐ Fond sonor măsurat 3+ nopți; departe de drumuri mari, cale ferată, ferme, industrie.
4. ☐ Creastă sau versant spre culoar, nu vale.
5. ☐ Protecție de vânt (burete + blăniță) și capac de ploaie; nodul raportează și vântul.
6. ☐ Vecinul cel mai apropiat la ≤ 2–3 km; pentru localizare, 3–4 noduri necoliniare.
7. ☐ GPS cu vedere la cer.
8. ☐ Curent permanent + baterie tampon; 4G bun (atenție la roaming pe rețele moldovenești lângă Prut) + semnal „heartbeat”.
9. ☐ Montaj discret, la înălțime, acces controlat.
10. ☐ Acord scris al proprietarului; verificat la urbanism.
11. ☐ În afara fâșiei de 20 m; consultare scrisă cu Poliția de Frontieră în zona de 30 km.
12. ☐ Procesare pe dispozitiv, fără audio brut; DPIA.
13. ☐ Locația doar în registrul intern, **nepublicată**.
