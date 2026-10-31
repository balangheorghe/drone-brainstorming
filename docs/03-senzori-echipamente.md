# 03 · Senzori și echipamente: ce funcționează, cât costă, cine poate folosi

*Stare: 31.10.2026. Doar detecție și urmărire. „Declarat” = cifră de la producător/dezvoltator, nu test independent. Prețurile se schimbă: verificați înainte de cumpărare.*

## Pe scurt

1. **Senzorii locali dau secunde–minute, nu zeci de minute.** Un Geran-2 (~180 km/h) parcurge un km în ~20 s; o dronă cu reacție (~450 km/h) în ~8 s. Un senzor acustic cu raza de 2–5 km dă ~40–100 s (piston) sau ~16–40 s (reacție). Avertizarea reală vine din amonte ([02](02-surse-predictie.md)).
2. **Acusticul e singura modalitate ieftină, dovedită la scară mare și accesibilă civililor** (Sky Fortress în Ucraina, Drone Rada în Lituania). **Necunoscută importantă:** cât de bine aude dronele cu reacție, care au fost probabil 2 din 3 cazuri de referință în 2026.
3. **RF pasiv nu funcționează contra Shahed pentru un civil.** E însă excelent și ieftin (< 100 €) pentru dronele civile mici care emit Remote ID.
4. **Radarul potrivit pentru ținte de 0,01–0,1 m²** e echipament profesional (zeci–sute de mii de euro) și cere licență ANCOM.
5. **Camerele termale** sunt bune pentru confirmare, dacă altcineva le spune unde să se uite.

## 1. Ținta

| Parametru | Valoare | Sursă |
|---|---|---|
| Viteză Geran-2 (piston) | ~180 km/h croazieră, ~185–190 max | [drone-warfare](https://drone-warfare.com/research/shahed-136/) |
| Viteză Geran-3 (reacție) | 300–370 km/h (HUR); ~400–470 implicit în incidentele din 2026 | [CSIS](https://missilethreat.csis.org/missile/shahed-238/); [02](02-surse-predictie.md) |
| Altitudine | de la zeci de metri (faza de atac) la 1–4 km | variabil, ales tactic |
| Secțiune radar (RCS) | 0,01–0,1 m² (estimări open-source) | [drone-warfare](https://drone-warfare.com/counter-uas/countering-the-shahed-136/) |
| Sunet | motor în 2 timpi, 4 cilindri (MD-550); energia sub ~3 kHz, „ca o motocoasă foarte zgomotoasă” | [studiu](https://computingonline.net/computing/article/view/4023/1244) |
| Emisii radio | GNSS doar recepționează; unele variante au modem 3G/LTE cu SIM sau modem mesh | [TWZ](https://www.twz.com/shahed-136-with-cellular-modem-found-in-ukraine-what-it-means); [RFE/RL via Migflug](https://migflug.com/afterburner/geran-4-teardown-rfe-rl-foreign-components-2026/) |

**Cât timp câștigi cu o rază de detecție dată:**

| Rază | Geran-2 (180 km/h) | reacție 370 km/h | reacție 450 km/h |
|---|---|---|---|
| 1 km | 20 s | 10 s | 8 s |
| 5 km | 100 s | 49 s | 40 s |
| 30 km | 10 min | 4,9 min | 4 min |
| 100 km | 33 min | 16 min | 13 min |

## 2. Modalitățile

### 2.1 Acustic – prioritatea nr. 1 pentru civili și ONG-uri

**Ce se știe:**
- **Sky Fortress (Ucraina):** ~9.500 (sau peste 10.000) de senzori; cost raportat de la ~300 USD (componente comerciale, [raport SHIELD 2024](https://www.missiledefenseadvocacy.org/wp-content/uploads/2024/07/Team-6-Acoustic-Lily-Pads-Final-Report.pdf)) la ~400–1.000 USD pe nod ([Odessa Journal](https://odessa-journal.com/ukrainian-engineers-have-created-a-network-of-nearly-10000-acoustic-sensors-to-track-russian-drones)). Armata SUA a publicat în 2026 un raport despre lecțiile acestei rețele ([„Listening to the Sky”](https://api.army.mil/e2/c/downloads/2026/04/30/af450e75/no-26-1115-listening-to-the-sky-acoustic-drone-detection-in-ukraine-mar-26.pdf)).
- **Raza față de Shahed:** tipic 2–3 km, până la ~5 km (declarat; [drone-warfare](https://drone-warfare.com/counter-uas/acoustic-detection/), [Baltic Defense Initiative](https://balticdefenseinitiative.com/programs/acoustic-sensor-network/)); 5–8 km doar „în deșert liniștit” – nerelevant pentru Iași.
- **Drone Rada (Lituania, iunie 2026):** telefoane Android vechi la fereastră ([LRT](https://www.lrt.lt/en/news-in-english/19/2989283/civic-initiative-turns-old-phones-into-drone-detectors-as-lithuania-fixates-on-air-defence)). Detalii în [06](06-retele-civile-lectii.md).

**Arhitecturi:**
- *Un microfon:* spune doar „există/nu există”, fără direcție.
- *Matrice de microfoane (beamforming):* dă azimutul. Ex. miniDSP UMA-16, ReSpeaker.
- *Rețea TDOA:* nodurile trebuie sincronizate cu GPS (PPS); o eroare de 1 ms strică localizarea. Nodul trimite doar detecția cu marcaj de timp, nu audio brut.
- *Clasificare ML pe nod:* nu există un set public dedicat Shahed. Seturi utile: [DADS](https://huggingface.co/datasets/geronimobasso/drone-audio-detection-samples) (MIT), [DroneAudioDataset](https://github.com/saraalemadi/DroneAudioDataset). Proiecte: [Sych-Tech](https://github.com/Sych-Tech) (voluntari ucraineni, RPi + ReSpeaker), [Batear](https://github.com/batear-io/batear) (ESP32-S3 + MEMS, ~15 USD, testat doar pe înregistrări; README-ul folosește 915 MHz, care **nu** e bandă UE). 16 kHz eșantionare ajunge.

**Limite:** vânt peste ~5 m/s, ploaie, inversiuni termice (zone de umbră acustică); alarme false de la tractoare, drujbe, mopede, ultraușoare, furtuni. **Dronele cu reacție:** au alt spectru (turbină mică) – eficiența rețelelor acustice contra lor nu e documentată public (vezi §6).

### 2.2 RF pasiv

- **Contra Shahed:** practic nu. GNSS nu emite; doar variantele cu modem emit, iar traficul celular e vizibil doar operatorilor (un civil nu are voie să-l intercepteze). Nici senzorul profesional Skyperion nu vede variantele exclusiv GNSS/INS ([Janes](https://www.janes.com/osint-insights/defence-news/c4isr/metis-aerospaces-skyperion-lightweight-rf-sensor-previously-tested-in-ukraine)).
- **Contra dronelor civile mici:** foarte bun. În UE, Remote ID direct e obligatoriu pentru clasele C1–C3 și categoria specifică ([EASA](https://www.easa.europa.eu/en/document-library/general-publications/remote-identification-will-become-mandatory-drones-across)); C0 și dronele vechi fără marcaj de clasă nu emit. Receptoare deschise: [OpenDroneID](https://github.com/opendroneid) (Android), [orecchino-esp32](https://github.com/isaacbentley/orecchino-esp32), [WiFi-RemoteID](https://github.com/lukeswitz/WiFi-RemoteID), [ESP32Marauder](https://github.com/justcallmekoko/ESP32Marauder/wiki/Remote-ID). Raza reală: ~100–500 m în testele amatorilor; producătorii declară 5–15 km.
- **Util la aeroport:** separă dronele legale de restul și reduce alarmele false.

### 2.3 Radar activ

- Pentru ținte de 0,01–0,1 m²: radare profesionale. Exemple: Echodyne EchoGuard (sub ~50.000 USD/unitate, drone mici la ~1 km) și EchoShield (~3 km, ~160.000 USD după CEO, [Defense News](https://www.defensenews.com/industry/2026/07/02/in-red-hot-counter-drone-market-echodyne-ceo-sees-radar-demand-boom/)); Robin Radar IRIS cu mod de 12 km pentru Shahed (declarat, [Defense Mirror](https://defensemirror.com/news/40436)). Mai multe în [04](04-produse-programe.md).
- **Licență ANCOM obligatorie** pentru emisie; banda de 24 GHz scutită de licență vizează radarele auto cu rază scurtă ([Decizia ANCOM 311/2016](https://legeaz.net/monitorul-oficial-228-2016/decizie-ancom-311-2016-frecvente-radio-exceptate-regim-licentiere)).
- Radar marin refolosit sau FMCW DIY: **nicio dovadă** de eficiență contra Shahed. Nu investiți în asta.

### 2.4 Radar pasiv (KrakenSDR)

- Nu emite, deci nu cere licență. Folosește emițătoarele FM/DVB-T existente.
- Rezultate academice cu echipamente profesionale: drone de 0,5–1 m la ~1 km cu DVB-T ([IET](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/rsn2.70092)). Pentru KrakenSDR (~500 USD) nu există rezultate de teren publicate contra dronelor.
- **Verdict:** proiect de cercetare pentru o universitate (ex. TUIASI, UAIC), nu sistem de alertă.

### 2.5 Optic și termic (EO/IR)

- Criteriile Johnson: detecția cere ~1,5–2 pixeli pe țintă. Pentru o țintă de ~2,3 m, FLIR dă ~1 km cu lentilă de 13 mm și ~2,2 km cu 25 mm ([FLIR](http://www.flirmedia.com/MMC/CVS/Tech_Notes/TN_0002_EN.pdf)). „Peste 5 km” e marketing.
- AI: modelele YOLO standard ratează ținte sub ~20 de pixeli; există modele specializate pe ținte termale mici ([exemplu](https://huggingface.co/RohanSardar/yolo11s_drone_tracker)) și un detector vizual Shahed-136 neverificat ([EDTH Warsaw](https://huggingface.co/shng2025/EDTH-Warsaw-shahed136-detector)).
- **Problema de fond:** o cameră cu zoom nu poate scana cerul. Trebuie îndreptată (cueing) de un senzor acustic sau radar. Camera vizibilă e inutilă noaptea; ceața reduce mult și termicul. Incidentul din 8.09 a fost în plină zi (apus ~19:38), dar cel din 31.10 a fost **chiar la apus** (~16:56 EET, calcul astronomic): în noiembrie–februarie, după-amiezile de la Iași sunt deja întuneric.
- **Atenție la furnizori:** agenția anticorupție ucraineană (NAZK) a inclus Hikvision și Dahua pe lista „sponsorilor războiului” ([NAZK](https://nazk.gov.ua/en/news/they-provide-eyes-for-russian-uavs-the-nacp-has-included-the-chinese-companies-hikvision-and-dahua-technology-in-the-list-)). Pentru o instituție: analiză de risc cibernetic înainte de achiziție.

### 2.6 Oamenii ca senzori

ePPO (Ucraina): utilizatorul autentificat îndreaptă telefonul spre țintă și apasă un buton ([Ukrinform](https://www.ukrinform.net/rubric-ato/3930665-eppo-app-helps-ukraine-close-sky-by-80.html)). În România nu există o aplicație echivalentă; canalul oficial e **112**.

## 3. Liste de materiale (orientative)

### (a) Nod acustic

| Componentă | Opțiune | Preț orientativ |
|---|---|---|
| Calculator | Raspberry Pi 5, 4 GB | ~85 USD listă (a crescut de mai multe ori în 2026, [Tom's Hardware](https://www.tomshardware.com/raspberry-pi/component-shortages-drive-raspberry-pi-prices-up-by-up-to-23-percent-escalating-lpddr4-lpddr5-costs-trigger-)) |
| Microfoane | miniDSP UMA-16 (16 canale) **sau** reSpeaker Flex XVF3800 | ~306–370 € ([Sound Imports](https://www.soundimports.eu/en/brands/minidsp/)) **sau** ~58,50 £ ([Pi Hut](https://thepihut.com/products/respeaker-flex-xvf3800-circular-with-xiao-esp32s3)) |
| GPS cu PPS | u-blox NEO-M8N | ~12–27 € (atenție la contrafaceri) |
| Conectivitate | router LTE Teltonika RUT241 | ~175 € ([sursă](https://industry-electronics.de/teltonika/rut241000000-networks-rut241-4g-lte-3g-2g-wifi-router-druckansicht-1914259.htm)) |
| Carcasă IP65, protecție anti-vânt, alimentare 12 V / solar, catarg | – | de bugetat separat |

**Subtotal:** ~300–600 € pe nod, plus carcasă și alimentare. *Ultra-ieftin:* ESP32-S3 + MEMS (~20 €), experimental. *Cost zero:* telefon Android vechi (modelul Drone Rada).

### (b) Nod Remote ID (drone civile mici)

ESP32-S3 DevKit (~17 €) + firmware deschis, sau un telefon Android cu aplicația OpenDroneID. **Sub 100 €** cu antenă și carcasă.

### (c) Nod optic/termic de bază

| Componentă | Preț orientativ |
|---|---|
| Cameră PTZ bi-spectrală 384×288, lentilă 25 mm | câteva mii de euro (preț UE de verificat) |
| Calcul AI local: Jetson Orin Nano Super | ~399 USD (majorat în iul. 2026, [CNX](https://cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101)) |
| Router LTE, catarg, PoE | câteva sute de euro |
| Pentru observare manuală: cameră termală portabilă 384×288 | ~900 € |

## 4. Comparație

| Modalitate | Rază realistă vs. Shahed | Drone mici | Alarme false | Vreme | Cost | Cine | Legal |
|---|---|---|---|---|---|---|---|
| Acustic | 2–5 km (declarat); jet: necunoscut | sute de m | tractoare, motoare 2T, furtuni | vânt > 5 m/s | < 600 €/nod | toți | fără audio brut; DPIA dacă acoperă spațiul public |
| Remote ID | 0 | 0,1–0,5 km real | puține | – | < 100 € | toți | date personale dacă se stochează |
| Radar activ | 1–12 km, după model | da | păsări | puțin | 50k–500k € | instituții | licență ANCOM |
| Radar pasiv | necunoscut (DIY) | 0,25–5 km (academic) | clutter | puțin | ~0,5–1k € + expertiză | universitate | nu emite |
| Termic PTZ | ~1–2 km (13–25 mm) | sute de m | păsări, avioane | ceață, ploaie | 1–10k € | ONG, instituții | GDPR video |

## 5. Recomandări pe actori

- **Cetățean (sub 200 €):** RO-Alert activ; receptor Remote ID sau aplicația OpenDroneID; un telefon vechi ca senzor acustic dacă apare o rețea civică organizată; raportare la 112.
- **ONG / firmă / universitate (1–10k €):** pilot cu 3–5 noduri acustice cu GPS PPS și LTE, procesare pe nod, plus 2–3 noduri Remote ID; colectare de sunete locale etichetate (tractoare, motocoase, avioane ușoare); parteneriat cu Spectrum Hive (Suceava) sau cu o universitate din Iași.
- **Primărie / Consiliu Județean / Aeroport (peste 50k €):** camere termale pe clădiri înalte, îndreptate automat de rețeaua acustică; radar autorizat ANCOM, coordonat cu MApN; DPIA; analiză de risc a furnizorilor; plan de incident după ghidul EASA.

## 6. Ce rămâne de verificat

- Detecția acustică a dronelor cu reacție (Geran-3/4): dovezi publice, spectru, rază.
- Câte noduri ar acoperi frontiera de pe Prut a județului Iași și ruta Ucraina → Botoșani, și la ce cost pe km.
- Raza Remote ID reală în mediul urban din Iași.

## 7. Realist vs. exagerat

**Realist:** rețele acustice dense, sincronizate GPS, cu clasificare pe nod; Remote ID pentru drone civile; camere termale îndreptate de alt senzor; integrarea fluxurilor oficiale.

**Exagerat:** „un microfon care aude un Shahed de la 10 km”; KrakenSDR ca radar anti-dronă la cheie; detecția RF a Shahed-urilor de către civili; „AI care vede drone la 5 km” cu o cameră cu unghi larg; radar marin refolosit.
