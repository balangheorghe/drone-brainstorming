# 05 · Cadrul legal: ce e permis, cui și cu ce autorizații

> **Nu e consultanță juridică.** E o hartă pentru brainstorming. Înainte de radar, camere spre spațiul public sau un canal public de informare, verificați textele consolidate pe [legislatie.just.ro](https://legislatie.just.ro) și cereți părerea unui jurist și a autorităților (ANCOM, ANSPDCP, AACR, ISU Iași, Poliția de Frontieră).

*Stare: 31.10.2026. Paliere: **P1** = cetățean/comunitate; **P2** = ONG/firmă/universitate; **P3** = administrație locală, instituție, operator de infrastructură critică (ex. Aeroportul Iași).*

## Pe scurt

- **Detecția și alertarea publică pentru amenințări aeriene militare sunt competențe ale statului** (MApN, IGSU/ISU/DSU, STS). Inițiativele civile le completează, nu le dublează și nu le imită.
- **Permis tuturor:** recepție pasivă (Remote ID, ADS-B, detecție de energie RF fără decodare), senzori acustici fără stocare de audio brut, camere orientate spre cer (cu reguli GDPR), raportare la 112.
- **Doar cu autorizare:** radar activ (licență ANCOM), camere care acoperă sistematic spațiul public (DPIA), echipamente în zona de frontieră (de verificat cu Poliția de Frontieră).
- **Interzis actorilor nestatali:** bruiaj, spoofing, preluarea controlului, doborâre, interceptarea comunicațiilor, declanșarea RO-Alert sau a sirenelor publice.

## 1. Cine face ce (statul)

| Funcție | Instituție | Temei (de verificat) |
|---|---|---|
| Supravegherea spațiului aerian, poliția aeriană, acțiunea contra dronelor neautorizate | MApN (în sistemul integrat NATO) | Legea 257/2001, modificată în 2025 (§2) |
| Înștiințare, avertizare, alarmare, sirene publice | IGSU/ISU, coordonate de DSU | OUG 21/2004; Legea 481/2004 (protecția civilă) |
| RO-Alert | emis de autoritățile abilitate, operat tehnic de STS, difuzat prin operatorii mobili | art. 110 din Codul european al comunicațiilor electronice; legislația națională de transpunere |
| Spectrul radio, autorizarea emițătoarelor | ANCOM | OUG 111/2011 (comunicații electronice) |
| Aviația civilă, drone civile, zone geografice UAS | AACR (+ ROMATSA) | Reg. (UE) 2019/947 și 2019/945; Legea 21/2020 (Codul aerian) |
| Protecția datelor | ANSPDCP | GDPR; Legea 190/2018 |
| Securitate cibernetică (NIS2) | DNSC | transpunerea NIS2 |
| 112 | STS | OUG 34/2008 |

## 2. Legea din 2025 privind doborârea dronelor

- În **mai 2025** a fost promulgată legea care modifică Legea 257/2001 și permite MApN să acționeze pe timp de pace împotriva dronelor care intră neautorizat în spațiul aerian al României, inclusiv prin doborâre; Curtea Constituțională a respins contestațiile ([Romania Insider](https://www.romania-insider.com/romania-enacts-law-down-drones-may-2025); [CCR](https://www.romania-insider.com/ccr-clears-law-shoot-down-unauthorized-drones-2025)). Presa o numește „Legea 73/2025”.
- Aplicare: doborârile din 2026 (de ex. Sulina, 17.10).
- **Pentru P1–P3:** legea nu dă niciun drept de neutralizare actorilor nestatali. Rolul lor legal: **detecție pasivă, documentare, raportare**.

## 3. Radio: emisie, bruiaj, recepție

- **Bruiajul e interzis** cetățenilor, ONG-urilor, firmelor și operatorilor de infrastructură, inclusiv aeroporturilor; e rezervat instituțiilor abilitate prin lege. Echipamentele radio trebuie să evite interferențele dăunătoare (Directiva RED, art. 3(2)).
- **Radarul activ e un emițător:** are nevoie de autorizare ANCOM de utilizare a frecvențelor și de conformitate RED (marcaj CE). Benzile scutite de licență (de ex. 24 GHz) vizează dispozitive cu rază scurtă; un radar de supraveghere în banda X/Ku cere drept individual. Lângă aeroport: coordonare aeronautică.
- **LoRa și alte radiouri pentru noduri:** doar benzile permise în UE (de ex. 868 MHz), nu 915 MHz din proiectele americane.
- **Recepția pasivă:**
  - **Remote ID** (Wi-Fi/Bluetooth): protocol deschis, conceput să fie recepționat de telefoane – recepția e exact utilizarea prevăzută.
  - **ADS-B**: emisii publice ale aviației civile; prudență la republicarea aeronavelor de stat.
  - **Detecție de energie RF / spectru** (fără decodarea conținutului): risc juridic scăzut.
  - **Decodarea legăturilor de comandă, video sau telemetrie ori interceptarea comunicațiilor: risc penal** (Cod penal art. 302 – violarea secretului corespondenței; art. 361 – interceptarea ilegală a unei transmisii de date informatice).

## 4. Drone civile (AACR, reguli UE)

- Reg. (UE) 2019/947: categorii deschisă / specifică / certificată; înregistrarea operatorilor; zone geografice UAS.
- Reg. (UE) 2019/945 (modificat prin 2020/1058): dronele din clasele C1–C3 (și categoria specifică) transmit **identificare directă la distanță**: nr. operator, serie, poziție, înălțime, direcție, viteză, poziția pilotului. C0 și dronele vechi fără marcaj nu emit.
- **Datele Remote ID sunt date personale** (operator, poziția pilotului) dacă le stocați sau publicați.
- Dronele militare de tip Geran nu emit Remote ID sau ADS-B (deducție logică); detecția lor e cu radar, acustic, optic, iar răspunsul e competența MApN.
- Drone proprii folosite ca senzori: înregistrare AACR, zone geografice; lângă aeroport – autorizare. Fără „urmărire” de drone cu drone.

## 5. Camere și microfoane (GDPR)

- Excepția „uz casnic” **nu** acoperă o cameră care filmează spațiul public (CJUE, C-212/13 Ryneš). Orientați camerele spre cer, mascați strada și vecinii, nu publicați imagini cu persoane.
- **DPIA obligatorie** pentru monitorizarea sistematică, pe scară largă, a unei zone publice (GDPR art. 35(3)(c)); ANSPDCP are lista operațiunilor care cer DPIA.
- Temei: autoritățile – interes public (art. 6(1)(e)); ONG/firme – de regulă interes legitim (art. 6(1)(f)). Panouri și note de informare (Ghidul EDPB 3/2019).
- **Microfoane:** Codul penal (art. 226) incriminează înregistrarea convorbirilor private. Proiectați senzorii acustici cu **procesare pe dispozitiv, fără stocarea audio brut și fără vorbire inteligibilă**; transmiteți doar detecții (oră, scor, azimut).
- Retenție minimă, control al accesului, protocol scris pentru predarea datelor către autorități.

## 6. Infrastructură critică (Aeroportul Iași, utilități)

- **NIS2:** administratorii de aeroporturi sunt entități din sectorul transport aerian; un sistem de detecție conectat în rețea intră în măsurile de securitate cibernetică și raportare a incidentelor.
- **Directiva CER (2022/2557)** cere măsuri de protecție fizică, inclusiv detecție; statutul transpunerii în România trebuie verificat.
- Referința operațională: ghidul EASA „Drone Incident Management at Aerodromes” – plan de incident, evaluarea credibilității observațiilor, coordonare cu traficul aerian și forțele de ordine.
- Neutralizarea rămâne la stat.

## 7. Zona de frontieră

Montarea de senzori lângă Prut poate intra sub regimul frontierei de stat (OUG 105/2001) și necesita acordul Poliției de Frontieră și al proprietarilor. **Verificați înainte de amplasare.**

## 8. Publicare, alarme false, răspundere

- Nu publicați în timp real poziții, decolări sau dispozitive militare (Legea 182/2002 privind informațiile clasificate; art. 407 Cod penal pentru divulgarea secretului).
- **Informații false:** art. 404 Cod penal cere cunoașterea falsității și punerea în pericol a securității naționale; o eroare de bună-credință nu se încadrează automat, dar poate genera alte forme de răspundere (inclusiv civilă, art. 1357 Cod civil).
- **Alarmarea falsă și apelurile abuzive la 112** sunt sancționate (Legea 61/1991; OUG 34/2008).
- **Reguli pentru un canal privat:** nume și design care nu seamănă cu RO-Alert sau cu o instituție; mențiunea „neoficial – urmați RO-Alert/ISU”; separați „neconfirmat” de „oficial (link)”; oră și sursă la fiecare mesaj; corecții publice; nicio instrucțiune contrară autorităților; jurnale pentru audit.
- Telegram: verificați termenii pentru citirea automată a canalelor publice.

## 9. Raportarea de către cetățeni

- Canalul oficial: **112** – ora, locul, direcția, sunetul, altitudinea aproximativă; foto/video doar dacă nu vă puneți în pericol.
- Nu vă apropiați de fragmente.
- Nu există (la data documentului) o aplicație oficială de raportare a dronelor în România.

## 10. Tabel: acțiune → cine → condiții

| Acțiune | Cine | Condiții |
|---|---|---|
| Recepție Remote ID | P1, P2, P3 | fără emisie; GDPR dacă stocați |
| Recepție ADS-B | P1, P2, P3 | nu acoperă drone militare; prudență la aeronave de stat |
| Detecție RF fără decodare | P2, P3 (tehnic și P1) | fără conținut, fără date nepublice |
| Decodare / interceptare de comunicații | **nimeni nestatal** | infracțiune |
| Senzori acustici | P1 (proprietate proprie), P2, P3 | procesare pe nod, fără audio brut; DPIA dacă acoperă spațiul public |
| Camere optice / termice | P1 (limitat), P2, P3 | spre cer, mascare, temei, DPIA, panouri |
| Radar activ | P3 (P2 doar ca prestator) | licență ANCOM, RED, coordonare aeronautică |
| Senzori în zona de frontieră | P2, P3 | acordul Poliției de Frontieră și al proprietarului (de verificat) |
| Bruiaj, spoofing, neutralizare | **nimeni nestatal** (nici aeroportul) | rezervate statului |
| Doborâre | **numai MApN** | legea din 2025 |
| RO-Alert, sirene publice | **numai autoritățile** | – |
| Canal privat de informare | P1, P2 (P3 doar cu protocol cu ISU) | disclaimer, fără imitarea RO-Alert, corecții, fără date militare în timp real |
| Partajare de date cu ISU/MApN | P2, P3 | protocol scris, temei GDPR, minimizare |
