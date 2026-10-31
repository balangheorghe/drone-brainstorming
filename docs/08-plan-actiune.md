# 08 · Plan de acțiune: de unde începem

*Stare: 31.10.2026. Costurile sunt orientative; verificați înainte de cumpărare.*

## 0. Alegeți-vă rolul

Recomandările diferă după cine implementează. Toate pornesc de la aceeași idee: **avertizarea vine din amonte, pe canale oficiale; senzorii locali confirmă; alerta publică e a statului.** Cu surse publice nu veți „bate” RO-Alert-ul (vezi [02](02-surse-predictie.md) §1.4) – asta nu e scopul.

| Rol | Ce puteți face legal | Buget orientativ | Ce câștigă Iașul |
|---|---|---|---|
| **Cetățean / grup de voluntari** | ascultați surse publice, recepție pasivă (Remote ID, ADS-B), senzor acustic pe proprietatea proprie, raportare la 112 | 0–200 € | oameni informați corect, rapoarte bune la 112 |
| **ONG / firmă / universitate** | bot OSINT, rețea pilot de senzori pasivi, cronologii publice, date pentru autorități | 0 € (A) → câteva mii € (B) | jurnal precis, primele date locale, pilot demonstrabil |
| **Primărie / Consiliu Județean / Aeroport / Prefectură** | radar autorizat, camere termale, plan de incident, protocol cu MApN/ISU, cereri de finanțare | zeci de mii → milioane € | acoperire 24/7, aeroport protejat, alertare mai precisă |

## 1. Pachetul de start recomandat (ONG / grup tehnic)

**Săptămâna 1 – fără cost**
1. Un telefon Android dedicat, cu RO-Alert activat, ținut în Iași: notați ora fiecărui mesaj (manual, la început).
2. Rulați [`analysis/ua_alerts_analysis.py`](../analysis/ua_alerts_analysis.py) mâine dimineață: va include cele două drone din 31.10 (Odesa și Vinnița). Atenție: după 7.09 setul are doar date de voluntari pe regiuni, care subestimează; pentru date pe raioane folosiți API-urile.
3. Faceți un **jurnal de incidente** (tabel): pentru fiecare alertă – ora alertei UA, ora detecției MD, ora restricției MD, ora publicării primului articol MD, ora RO-Alert, județele, ora încetării. Completați retroactiv din [09-evenimente-2026](09-evenimente-2026.md) (16.08, 24.08, 8.09, 12.09, 24.09, 31.10).
4. Cereți token-uri: alerts.in.ua și api.ukrainealarm.com.

**Săptămânile 2–6 – Nivelul A (bot OSINT, cost: timp + un VPS mic)**
- Colectori pentru sursele din [07](07-arhitectura-sistem.md) §2, cu **arhivă brută** (text, oră publicare, oră primire).
- Reguli simple: S1 vigilență (alertă UA activă), S3 Moldova (detecție/restricție), S4 apropiere (curs vest, ETA ≤ 30 min).
- Notificări doar într-un **grup închis** de operatori. Canal public doar pentru retransmiterea mesajelor oficiale și pentru cronologii după incident.
- **Mod umbră 30–90 de zile:** măsurați avansul real față de RO-Alert și rata de „alarme” interne.

**Lunile 2–6 – Nivelul B (pilot de senzori, câteva mii €)**
- Parteneriat cu o universitate din Iași (TUIASI, UAIC) și/sau Spectrum Hive (Suceava).
- 3–5 noduri acustice (~300–600 €/nod + carcasă, alimentare) în est/nord-est de Iași, pe clădiri ale partenerilor, cu acord.
- 2–3 receptoare Remote ID (< 100 € fiecare).
- Colectare de sunete locale etichetate (tractoare, drujbe, motociclete, avioane ușoare) – esențial pentru clasificator.
- DPIA (evaluare de impact asupra datelor) dacă nodurile acoperă spațiul public; procesare pe nod, fără audio brut.
- Verificați la Poliția de Frontieră regimul zonei de frontieră înainte de a monta noduri lângă Prut.

**Lunile 3–12 – Nivelul C (prin instituții)**
- Dosar către Prefectură, Consiliul Județean și Aeroportul Iași: datele din jurnal + pilotul B + caiet de sarcini după modelul CNAB, restrâns la detecție.
- Cerere de includere a frontierei de pe Prut în: componenta anti-dronă SAFE (~2,2 mld. €), EDDI, Eastern Flank Watch.

## 2. Ce să cereți autorităților (scrisoare către ISU Iași, Prefectura Iași, DSU)

1. **Alertare pe zone mai mici decât județul** (mesajul din 31.10 nu avea nici zonă, nici durată).
2. **Pre-alertă în două trepte** („atenție” vs. „adăpostiți-vă acum”), după modelul israelian.
3. **Mesaj explicit de încetare**, cu oră.
4. **Cronologie oficială publicată după fiecare incident** (orele de la 8.09 diferă între surse: 16:30 / 16:37 / 16:47 pentru alertă și detecție; 17:33 / 17:50 / 17:55 pentru încetare).
5. **Un punct de contact** pentru date de la senzori civili sau universitari, cu un protocol scris.
6. **O arhivă publică, citibilă automat, a mesajelor RO-Alert** (oră, zonă, text) – pentru transparență și cercetare.
7. **Ce protocol de informare există cu Armata Națională a R. Moldova** și dacă poate fi accelerat.
8. Pentru Aeroportul Iași: există un plan de gestionare a incidentelor cu drone (ghidul EASA)? Cine decide suspendarea zborurilor?

## 3. Ce să NU faceți

- Nu emiteți mesaje publice de tip „adăpostiți-vă” și nu imitați RO-Alert (nume, culori, format).
- Nu republicați traiectorii din canalele ucrainene (sunt incriminate în Ucraina și pot ajuta adversarul).
- Nu publicați poziții ale senzorilor, aeronave militare sau hărți de impact imediat după eveniment.
- Nu folosiți bruiaj, radar fără licență sau emițătoare pe benzi nepermise (ex. LoRa 915 MHz din proiecte americane).
- Nu interceptați comunicații (celulare, legături video/telemetrie) – risc penal.
- Nu promiteți „X minute de avertizare” înainte de a le fi măsurat.

## 4. Întrebări deschise (de lămurit în următoarele săptămâni)

1. **Semnalele ucrainene pe raioane** (date oficiale după 7.09, prin API): confirmă tiparul „8/8” și pe incidentele din sept.–oct.?
2. **Cât de bine aud senzorii acustici dronele cu reacție?**
3. **Ce acoperire ar cere frontiera de pe Prut a județului Iași** (număr de noduri, cost pe km)?
4. **Există un feed RO-Alert** sau o arhivă oficială?
5. **Cum se poate calibra modelul** pe toate cele 65 de încălcări moldovenești din 2026 + alertele UA.

## 5. Pași următori posibili în acest repo

- Implementarea Nivelului A (colectori, arhivă, reguli, bot Telegram în grup închis).
- Un tabel de evenimente 2026 (MD + RO) legat automat de istoricul alertelor UA, pentru calibrare.
- Specificația unui nod acustic de test și protocolul de colectare a sunetelor locale.
