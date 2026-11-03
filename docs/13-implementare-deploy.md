# 13 · Implementarea (Nivelul A) și deploy

*Stare: 31.10.2026. Codul: [`veghe/`](../veghe/). Teste: [`tests/`](../tests/). Configurare: [`config.example.toml`](../config.example.toml), [`.env.example`](../.env.example).*

## Ce face serviciul `veghe`

- **Citește** sursele publice din [11](11-fluxuri-date-harti.md): alerte UA (alerts.in.ua, ukrainealarm, canalul `air_alert_ua`), canale Telegram publice (Forțele Aeriene UA, administrațiile Odesa, Cernăuți, Izmail), presa și Moldpres (RSS, Google News), trafic aerian din ADS-B (adsb.lol, cu rezervă airplanes.live, opțional receptor propriu) și NOTAM-uri (ROMATSA; opțional FAA pentru R. Moldova).
- **Arhivează** fiecare mesaj în SQLite, cu ora de publicare și ora la care l-a primit (pentru măsurarea avansului real).
- **Aplică regulile** din [07](07-arhitectura-sistem.md): VIGILENȚĂ → DIRECȚIE → MOLDOVA → APROPIERE → OFICIAL, cu ETA în intervalul 450/150 km/h.
- **Trimite mesaje INTERNE** într-un grup Telegram privat (și opțional ntfy). La fiecare pornire trimite „veghe pornit”, ca să știți că livrarea merge.
- **Mesaje PUBLICE:** doar retransmiteri ale RO-Alert-urilor relatate de presa/autoritățile românești și încetarea alertei; **niciodată** conținut din canalele ucrainene; **numai după aprobarea unui operator** (`/aproba N`). Canalul public e oprit implicit.
- **Aviație:** detectează închiderea sau ocolirea spațiului aerian (traficul civil scade față de fondul recent, verificat cu o zonă de control), avioane civile în așteptare sau întoarse din drum, coduri de urgență și interferențe GPS; citește NOTAM-urile de restricție. Detalii: secțiunea „Aviație” de mai jos.
- **Aeronave militare** (din datele ADS-B publice): doar un rezumat pe tipuri generale, distanță și direcție aproximative, **doar pe canalele interne** (grupul privat; ntfy, dacă îl folosiți); fără identități, fără trasee. Rezumatul se livrează, dar **nu se păstrează**: în arhivă și în jurnal conținutul e înlocuit după livrare.
- **Siguranță la livrare:** botul refuză să trimită mesaje interne dacă „grupul intern” e de fapt un canal sau un grup public; refuză ntfy.sh fără token; comenzile sunt acceptate doar de la operatori, doar din grupul intern sau din chat privat, și doar dacă sunt recente (sub 10 minute).
- **Te anunță când orbește:** dacă o sursă cade (3 erori la rând), primiți „SURSĂ CĂZUTĂ”; la revenire, „Sursa … a revenit”. Dacă bucla principală se blochează peste 5 minute, procesul iese, iar Docker/systemd îl repornește. Cu systemd, dacă portul paginii de stare e ocupat, doar pagina nu pornește; alertele continuă (cu Docker, vedeți mai jos `VEGHE_HOST_PORT`).

### Comenzi pe Telegram (opționale; doar operatorii din `TELEGRAM_OPERATOR_IDS`)

| Comandă | Ce face |
|---|---|
| `/stare` | nivelul curent, alertele UA urmărite, ipotezele, sursele cu erori |
| `/ultimele 5` | ultimele semnale arhivate |
| `/coada` | mesajele publice care așteaptă aprobarea |
| `/aproba N` / `/respinge N` | aprobă sau respinge mesajul public N |
| `/roalert Iași 17:04` | **opțional:** notează ora exactă a unui RO-Alert (altfel ora e luată automat din presă) |

### Linia de comandă

Pe serverul cu **Docker**, comenzile rulează în container: `docker compose run --rm veghe <comandă>` (merge și cu serviciul pornit). Cu **systemd**: `cd /opt/veghe && sudo -u veghe bash -c 'set -a; . ./.env; /usr/bin/python3 -m veghe <comandă>'`.

| Comandă | Ce face |
|---|---|
| `run` | pornește serviciul (o face Docker/systemd) |
| `check-sources` | citește fiecare sursă o dată, arată ce a înțeles și **trimite un mesaj de test în grupul privat** – prima verificare live |
| `report --since 2026-11-01T14:00:00Z` | primul semnal pe fiecare nivel vs. RO-Alert (din presă sau, dacă există, notat manual) |
| `roalert Iași --at 17:04` | opțional: doar arhivează ora exactă a unui RO-Alert (pentru raport) |
| `outbox` · `aproba N` · `respinge N` | coada de mesaje publice |
| `replay tests/scenarios/2026-10-31.jsonl` | reia un incident real prin reguli, fără rețea. În Docker: `docker compose run --rm -v ./tests:/app/tests:ro veghe replay tests/scenarios/2026-10-31.jsonl` |

Exemplu: `docker compose run --rm veghe report --since 2026-11-01T14:00:00Z`.

## Ce s-a validat și ce nu

| Nivel | Rezultat | Ce dovedește |
|---|---|---|
| **Revizuire de cod independentă** (4 direcții: corectitudine, siguranță/OPSEC, funcționare 24/7, fidelitatea formatelor) | 49 de constatări, aproape toate confirmate prin reproducere; **toate cele relevante corectate**, fiecare cu test de regresie | vezi istoricul git (commit „Corecturi după revizuirea de cod”) |
| **A doua verificare independentă** (reverificarea corecturilor + căutarea de defecte noi) | 35 de corecturi confirmate; 13 defecte noi introduse de corecturi (ex. o sursă care „picură” date, coadă blocată de reîncercări, articole întârziate) – **toate corectate**, cu teste | |
| **Verificarea dinaintea unirii în `master`** (instalare pas cu pas cu Docker și cu systemd, revizuirea ultimelor modificări, documentație vs. cod; fiecare constatare reverificată independent) | prima trecere: 32 de constatări confirmate, unele găsite de mai mulți verificatori (ex. ID de grup greșit = alerte pierdute fără avertizare, port ocupat = serviciu oprit, depozit privat, comenzi care nu mergeau pe serverul cu Docker); a doua trecere, pe corecturi: 12 constatări (ex. portul 8080 ocupat oprea containerul, `data/` fără drept de scriere nedetectat) – **toate corectate**, cu teste | |
| **Teste** (geografie, analiza textului uk/ru/ro, parsere, motor, livrare, linie de comandă) | trec (391 de teste în total, pe Python 3.11–3.13) | distanțele coincid cu documentele; parserele citesc fixturile construite după **clienții oficiali** (alerts-in-ua, UkraineAlarm, Home Assistant), **selectorii RSSHub** pentru t.me/s și **documentația readsb** |
| **Scenarii reale** (8.09 și 31.10.2026) | trec | succesiunea de niveluri e cea așteptată; primul mesaj intern vine înaintea retransmiterii RO-Alert; zero conținut ucrainean în mesajele publice |
| **Test complet cu servere simulate** | trece | configurare din TOML + secrete din mediu, autentificarea corectă la API-uri, deduplicare, trimitere pe Telegram, mesajul de test și cel de pornire, erorile Telegram explicate (token/ID greșit, bot scos), refuzul comenzilor neautorizate, modul fără operatori, `check-sources`, pagina de stare |
| **Imaginea Docker** | construită și pornită | `docker compose build` reușește; `check-sources` rulează în container (inclusiv mesajul de test către un Telegram simulat și verificarea `data/`); healthcheck „healthy”; `/health` și `/status` răspund; „veghe pornit” la pornire; port ocupat → `VEGHE_HOST_PORT`; oprire curată la `docker compose stop`; baza de date se creează în `data/` cu drepturi doar pentru serviciu |
| **Rulare reală a serviciului** (fără acces la surse) | merge | bucla nu cade la erori de rețea, aplică pauze progresive (de la 2× intervalul sursei, până la 15 min), oprire curată la SIGTERM |
| **Module NOTAM și ADS-B** (cercetare pe surse primare, construcție, revizuire adversarială cu teste de mutație; apoi verificarea integrării: corectitudine, confidențialitate/OPSEC, scenarii simulate cap-coadă) | trec; verificarea integrării a găsit 36 de constatări confirmate (unele raportate de mai mulți verificatori), iar reverificarea a confirmat corectarea lor și a mai găsit 15 probleme mici (ex. nota militară veche în fișierul bazei de date, o zonă „oarbă” mascată de zona de control) – toate corectate (ex. rezumatul militar rămânea în arhivă, NOTAM-uri programate pierdute la repornire, mesaje repetate când datele oscilează, ADS-B „orb” fără avertizare) – **corectate**, cu teste | formatele ROMATSA WFS, FAA NMS, readsb/adsb.lol (câmpuri NIC/NACp, `gpsOkBefore`, `dbFlags`) sunt luate din codul și fixturile publice ale proiectelor care le folosesc; ROMATSA și adsb.lol **nu** au putut fi interogate din sesiune → se verifică cu `check-sources` pe server |
| **Surse reale (live) și Telegram real** | **nevalidat aici** | rețeaua sesiunii de dezvoltare blochează Telegram, API-urile ucrainene, Google News și adsb.lol. **Validarea live = `check-sources` pe server** (inclusiv mesajul de test în grup) |

**Ce înseamnă „validat” aici:** logica, parserele și livrarea sunt testate pe formate reale (preluate din clienții oficiali și din sursele RSSHub/readsb) și pe incidentele reale reluate. **Nu** înseamnă că sursele reale răspund exact așa azi: asta se vede doar cu `check-sources` pe server.

## Mod „doar primesc alerte” (fără intervenție)

Configurarea implicită e deja așa:

- `public_enabled = false` → nimic nu pleacă public, deci **nu aveți nimic de aprobat**;
- toate mesajele interne vin **automat** în grupul Telegram privat: VIGILENȚĂ, DIRECȚIE, ATENȚIE, APROPIERE, OFICIAL, ÎNCETARE, DE VERIFICAT (titlu de presă cu încetare *și* alertă nouă – merită citit), ADS-B (trafic civil oprit sau mult redus, avioane în așteptare/întoarse, cod de urgență), GNSS (interferență GPS), ADS-B MILITAR (doar avioane de luptă sau drone), NOTAM (restricții noi lângă Iași/Prut sau în R. Moldova; anulare/expirare), SURSĂ CĂZUTĂ / „Sursa … a revenit”, „veghe pornit”;
- RO-Alert-ul e preluat **automat din presă**; nu trebuie înregistrat;
- **fără mesaje repetate:** VIGILENȚĂ vine o dată pe episod (o alertă care se oprește și repornește nu dă mesaje noi; episodul se încheie după 30 min fără alerte), cu o actualizare doar dacă alerta ajunge mult mai aproape de Iași. Aceeași dronă e anunțată din nou doar dacă: urcă la un nivel mai grav; apare prima ei poziție; s-a apropiat clar de Iași (≥ 25 km, ≥ 10 km în faza APROPIERE – o apropiere venită prea curând e trimisă după pauză, nu pierdută); vine o veste nouă despre ea (ex. „a dispărut de pe radar”, o singură dată); sau ultimul mesaj are peste 15 min și poziția s-a schimbat. Formulări ca „încă un UAV”, „un nou aparat”, „ще одна група БпЛА” deschid o ipoteză nouă (o dronă nouă nu e ascunsă). O sursă intermitentă e anunțată „căzută / a revenit” cel mult o dată la 2 ore, dar o cădere nouă care ține peste 15 min e anunțată. În plus, un mesaj intern identic (fără oră) cu unul din ultimele 10 min nu se retrimite – rămâne în arhivă ca „duplicat” și pleacă totuși dacă originalul n-a putut fi livrat (`dedup_min` în `[notify]`, 0 = oprit; RO-Alert și ÎNCETARE nu trec prin acest filtru). După o repornire continuă episodul VIGILENȚĂ, ipotezele deschise și starea RO-Alert/ÎNCETARE, fără mesaje repetate;
- comenzile (`/stare`, `/roalert` …) sunt opționale.

Singurele acțiuni: instalarea o dată și `check-sources` la început. În rest, doar citiți mesajele. Mesajele sunt informative. Excepții, rare:
- APROPIERE fără RO-Alert sugerează anunțarea ISU/112 – la latitudinea voastră;
- mesajul despre **ceasul serverului** → porniți sincronizarea: `sudo timedatectl set-ntp true`;
- o **SURSĂ CĂZUTĂ care nu revine** (zile) → corectați sau scoateți sursa din `config.toml` (vezi mai jos ce înseamnă ✗), apoi reporniți: `docker compose up -d --force-recreate` sau `sudo systemctl restart veghe` (configurarea se citește doar la pornire). Restul surselor merg în continuare.

## Aviație: ADS-B, aeronave militare, NOTAM

**Ce poate și ce nu:** dronele de tip Shahed **nu** transmit ADS-B, deci nu pot fi văzute direct. Aviația dă semnale **indirecte**: închideri de spațiu aerian, avioane deviate, bruiaj GPS, reacția aviației militare. Toate mesajele de mai jos sunt interne și informative; niciunul nu ridică singur nivelul de alertă.

| Mesaj | Când apare | Cum se evită alarmele false |
|---|---|---|
| **ADS-B: trafic oprit** | traficul civil din jurul Iași/Chișinău scade de la fondul obișnuit (≥ 2) la 0, de 3 ori la rând | se trimite doar în vigilență sau cu o ipoteză deschisă; zona de control (Transilvania) trebuie să fie normală și datele proaspete – altfel e „lipsă de date”, nu închidere. Atenție: o pană a receptoarelor voluntare doar în zona respectivă arată la fel |
| **ADS-B: trafic mult redus (ocolire)** | traficul scade sub 30 % din fondul ultimelor ore (fond ≥ 4, trafic > 0), de 3 ori la rând | aceleași condiții; starea se încheie abia după 3 citiri bune peste 50 % din fond, iar citirile cu date lipsă nu o schimbă; același mesaj nu se repetă mai des de 30 min |
| **ADS-B: așteptări / întoarceri** | avioane civile care se rotesc în așteptare (≥ 12 NM de drum cu deplasare mică) sau care se întorc ≥ 150° de pe rută | ≥ 2 aeronave în vigilență, ≥ 3 oricând; nu se numără avioanele mici, elicopterele și cele joase; întoarcerile joase de lângă aeroport (apropieri obișnuite) sunt ignorate; din nou doar dacă numărul crește cu ≥ 2, altfel un memento după 60 min |
| **ADS-B: URGENȚĂ 7700/7600/7500** | o aeronavă civilă transmite un cod de urgență în cel puțin 2 citiri (7500: 3) | o singură dată pe aeronavă și cod; aeronava nu e identificată |
| **GNSS** | proporția aeronavelor civile cu poziție GPS degradată (NACp < 8 / NIC < 7, sau GPS pierdut) depășește pragul în 2 evaluări la rând; pragul e max(10 %, fondul zonei pe 7 zile + 10 puncte); 2 aeronave fără GPS ajung singure | **începe abia după 3 zile** de fond măsurat (zona Mării Negre are bruiaj frecvent); maxim 4 mesaje/zi/zonă, la cel puțin 30 min |
| **ADS-B MILITAR** | apar avioane de luptă sau drone militare vizibile public în raza de 150 NM de Iași | un mesaj la apariție; din nou când numărul crește (cu ≥ 2 în primele 20 min de la ultimul mesaj, cu oricât după aceea) sau după 20 min fără ele (pâlpâirile nu produc mesaje noi). AWACS, cisterne, transport nu declanșează mesaje (zboară des deasupra României): apar în `/stare` și, alături de avioanele de luptă, în mesajul ADS-B MILITAR. În notele altor mesaje (VIGILENȚĂ, ATENȚIE …) apar doar numerele pe tipuri, fără poziții, și doar când sunt avioane de luptă/drone. Datele mai vechi de 5 min nu se mai folosesc |
| **NOTAM** | NOTAM nou: spațiu aerian închis, zboruri UAS/drone, interferențe GNSS, aeroport Iași/Chișinău/Bălți închis, restricții cu drone sau în R. Moldova – lângă Iași/Prut sau în FIR Chișinău | restricțiile militare de rutină și cele departe se arhivează fără mesaj; mai multe NOTAM-uri în 10 min vin într-un singur mesaj; reemiterile lunare nu se reanunță |

**Aeronave militare – reguli:** rezumatul conține doar tipul general (avion de luptă, dronă, avion radar/recunoaștere, avion-cisternă, transport, elicopter), distanța rotunjită la 10 km și direcția pe 8 puncte (aeronavele cu marcaj de confidențialitate PIA/LADD sunt doar numărate). Ajunge pe toate canalele interne – dacă folosiți ntfy.sh **fără token** (`allow_public_ntfy = true`), oricine știe topicul îl poate citi. În arhivă și în jurnal conținutul se înlocuiește după livrare (și fișierul bazei de date e curățat); pentru a nu reanunța după o repornire se păstrează doar numărul avioanelor de luptă/dronelor de la ultimul mesaj și ora lui – fără tipuri, poziții sau identități. `check-sources` arată doar câte aeronave militare sunt în zonă. **Nu redistribuiți aceste mesaje**: publicarea pozițiilor aeronavelor militare în timpul unei operațiuni poate ajuta adversarul și poate avea consecințe legale. Avioanele de poliție aeriană zboară des fără ADS-B: **absența lor nu înseamnă nimic**. Oprire: `military = { enabled = false, … }` în `config.toml`.

**NOTAM – surse:**
- **ROMATSA** (România, FIR București) – implicit, fără cheie. Include zonele restricționate de la granița cu R. Moldova și Ucraina. Serverul ROMATSA are o configurație TLS veche; programul încearcă automat o setare compatibilă, fără să dezactiveze verificarea certificatului.
- **FAA NOTAM Management Service** – singura sursă găsită care ar putea avea NOTAM-urile R. Moldova (FIR Chișinău). Cere credențiale: scrieți la notams@faa.gov și cereți acces la NMS-API (producție); primiți un client_id și un client_secret, pe care le puneți în `.env` (`FAA_NMS_CLIENT_ID`, `FAA_NMS_CLIENT_SECRET`), apoi `enabled = true` la sursa `faa` din `config.toml`. Nu e confirmat că FAA dă acces persoanelor din afara SUA, nici că NMS conține NOTAM-urile Moldovei.

**Praguri:** toate sunt propuneri inițiale, de reglat după câteva săptămâni de date; cele ale analizei (GNSS, așteptări, întoarceri, scădere) sunt în `[sources.adsb.analysis]`, iar regulile de trimitere (30 % pentru ocolire, 20/30/60 min între mesaje) sunt în cod (`veghe/engine.py`). Programul păstrează doar agregate pe zonă (câte avioane, câte cu GPS degradat), niciodată identități sau trasee.

## Deploy: de ce aveți nevoie

1. **Un server Linux mic în UE** (1 vCPU, 1 GB RAM, 10 GB disc ajung), cu Docker și Docker Compose. Orice furnizor de VPS. Alternativ, un Raspberry Pi permanent conectat, cu systemd (fără Docker) și Python ≥ 3.11 (Debian 12 / Raspberry Pi OS Bookworm îl au; Ubuntu 22.04 are 3.10 – nu ajunge).
2. **Acces la depozit:** depozitul GitHub e **privat**, deci serverul are nevoie de o cheie de citire (pașii de mai jos, „cheie de deploy”).
3. **Un bot Telegram:** creat cu [@BotFather](https://t.me/BotFather) → `TELEGRAM_BOT_TOKEN`.
4. **Un grup Telegram privat** (fără link/nume public), cu botul adăugat → `TELEGRAM_INTERNAL_CHAT_ID`. Cum aflați ID-ul: în grup scrieți `/start@NumeleBotului` (comenzile ajung la bot și cu „privacy mode” activ), apoi deschideți `https://api.telegram.org/bot<TOKEN>/getUpdates` și căutați `"chat":{"id":…}`. E un **număr negativ**: `-100…` la supergrupuri, `-…` la grupurile simple. Dacă grupul e transformat ulterior în supergrup, ID-ul se schimbă (vă anunță `check-sources`). Dacă grupul are nume public (@…), botul refuză să trimită în el.
5. (Opțional) **ID-urile numerice ale operatorilor** → `TELEGRAM_OPERATOR_IDS` (de ex. prin @userinfobot). Fără ele alertele vin oricum; doar comenzile (`/stare` …) nu sunt acceptate.
6. **Token-uri pentru API-urile ucrainene** (opționale la început; canalul `air_alert_ua` merge fără):
   - alerts.in.ua: formularul [alerts.in.ua/api-request](https://alerts.in.ua/api-request) – descrieți scopul civil cu cuvintele voastre;
   - ukrainealarm: formularul de pe [api.ukrainealarm.com](https://api.ukrainealarm.com).
7. (Mai târziu) **un canal Telegram public**, doar dacă decideți să retransmiteți oficial → `TELEGRAM_PUBLIC_CHAT_ID` + `public_enabled = true` **și `TELEGRAM_OPERATOR_IDS`** (fără operatori, nimeni nu poate aproba din Telegram, iar mesajele publice expiră după 30 min).

**Formatul `.env`:** `CHEIE=valoare`, fără spații în jurul lui `=`, fără comentarii pe același rând, fără ghilimele (ID-uri multiple: `111,222`).

## Deploy: pașii (Docker)

Comenzile `docker` cer `sudo` dacă utilizatorul nu e în grupul `docker`.

```bash
# pe server – 1. cheia de deploy (doar citire) pentru depozitul privat
mkdir -p -m 700 ~/.ssh && ssh-keygen -t ed25519 -N '' -f ~/.ssh/veghe_deploy
cat ~/.ssh/veghe_deploy.pub
#   → GitHub: depozitul → Settings → Deploy keys → Add deploy key (lipiți cheia; NU bifați „Allow write access”)

# 2. codul
git clone -b master -c core.sshCommand="ssh -i ~/.ssh/veghe_deploy -o IdentitiesOnly=yes" \
    git@github.com:balangheorghe/drone-brainstorming.git veghe && cd veghe     # la prima conectare răspundeți „yes”

# 3. configurarea (secretele doar pentru voi)
install -m 644 config.example.toml config.toml   # ajustați dacă e cazul
install -m 600 .env.example .env && nano .env    # TELEGRAM_BOT_TOKEN, TELEGRAM_INTERNAL_CHAT_ID (+ opționalele)
mkdir -p data && sudo chown 10001:10001 data     # utilizatorul din container (ca root, fără sudo: chown 10001:10001 data)

# 4. construire și VALIDAREA LIVE
docker compose build
docker compose run --rm veghe check-sources
#   → fiecare sursă cu ✓, „✓ baza de date”, „✓ telegram intern …” și MESAJUL DE TEST trebuie să apară în grupul privat

# 5. pornire
docker compose up -d
docker compose logs -f        # în grup trebuie să apară „veghe pornit”; ieșiți cu Ctrl-C (serviciul rămâne pornit)
```

Actualizare ulterioară: `git pull && docker compose build && docker compose up -d` (`config.toml`, `.env` și `data/` nu sunt atinse). Dacă versiunea nouă aduce secțiuni noi în `config.example.toml` (`check-sources` vă avertizează: „config.toml pare din versiunea veche”), copiați-l din nou peste `config.toml` (secretele sunt în `.env` și rămân) sau adăugați secțiunile lipsă.

Verificări ulterioare: în grup apare „veghe pornit” la fiecare repornire. Pagina de stare e disponibilă doar pe server: `curl http://127.0.0.1:8080/status` (sau printr-un tunel SSH; alt port dacă ați setat `VEGHE_HOST_PORT`). Dacă ați setat `TELEGRAM_OPERATOR_IDS`, puteți scrie și `/stare` în grup. Containerul pornește singur după o repornire a serverului dacă serviciul Docker e activ (`sudo systemctl enable docker`).

**Ce faceți dacă `check-sources` arată ✗** (sau altceva nu merge):
- `docker compose up -d` spune „address already in use” / „port is already allocated” → portul 8080 e ocupat pe server: puneți `VEGHE_HOST_PORT=8081` în `.env` și rulați din nou `docker compose up -d`; pagina de stare e apoi la `http://127.0.0.1:8081`;
- `baza de date` → directorul `data/` nu e al containerului: `sudo chown 10001:10001 data`, apoi din nou `check-sources`;
- `telegram intern` → mesajul spune cauza: token greșit (401), ID de grup greșit sau grup transformat în supergrup (400), botul nu e în grup (403), grup cu nume public (refuzat). Corectați `.env` și rulați din nou;
- `telegram:<canal>` cu „nu conține mesaje publice” → canalul nu are previzualizare publică sau și-a schimbat numele; scoateți-l sau corectați-l în `config.toml`;
- `rss:moldpres` sau alt RSS cu „nu e un flux RSS/Atom” → URL-ul s-a schimbat; căutați `<link rel="alternate" type="application/rss+xml">` în pagina publicației;
- `alerts_in_ua` cu 401/403 → token greșit sau încă neaprobat;
- `adsb` cu 4xx → adsb.lol a introdus cheie (vezi adsb.lol/feed); folosiți airplanes.live sau un receptor propriu.

O sursă se scoate ștergând (sau comentând) blocul ei din `config.toml`, ori cu `enabled = false` în bloc.

## Deploy: alternativa fără Docker (systemd)

```bash
/usr/bin/python3 --version            # trebuie ≥ 3.11 (altfel instalați 3.11+ și schimbați ExecStart în veghe.service)
sudo apt-get install -y tzdata git    # Debian / Raspberry Pi OS

# cheia de deploy, a lui root (clonarea se face cu sudo)
sudo mkdir -p -m 700 /root/.ssh && sudo ssh-keygen -t ed25519 -N '' -f /root/.ssh/veghe_deploy
sudo cat /root/.ssh/veghe_deploy.pub  # → GitHub: Settings → Deploy keys → Add deploy key (fără drept de scriere)

sudo useradd --system --home /opt/veghe veghe
sudo git clone -b master -c core.sshCommand="ssh -i /root/.ssh/veghe_deploy -o IdentitiesOnly=yes" \
    git@github.com:balangheorghe/drone-brainstorming.git /opt/veghe
cd /opt/veghe
sudo install -m 644 config.example.toml config.toml
sudo install -m 640 -o root -g veghe .env.example .env && sudo nano .env
sudo mkdir -p data && sudo chown veghe:veghe data
sudo -u veghe bash -c 'set -a; . ./.env; /usr/bin/python3 -m veghe check-sources'   # ✓ (surse, baza de date) + mesajul de test în grup
sudo cp deploy/veghe.service /etc/systemd/system/ && sudo systemctl enable --now veghe
systemctl status veghe --no-pager
curl -s http://127.0.0.1:8080/health   # ok
sudo journalctl -u veghe -n 50 --no-pager   # „veghe pornit”, fără „Traceback”; în grup apare „veghe pornit”
```

Actualizare ulterioară: `sudo git -C /opt/veghe pull && sudo systemctl restart veghe`. Dacă portul 8080 e ocupat pe server, schimbați `status_port` în `config.toml`.

## Test pe un calculator cu Windows (WSL)

Pentru încercări, nu pentru funcționare permanentă (alertele vin doar cât calculatorul e pornit și nu doarme).

```bash
# PowerShell ca administrator, o dată: wsl --install -d Ubuntu-24.04  (Python 3.12 inclus)
# Dacă aveți deja Ubuntu 22.04 (Python 3.10, prea vechi):
sudo apt update && sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa && sudo apt install -y python3.11
```

- Țineți proiectul **în Linux** (ex. `~/veghe`), nu pe `/mnt/c` sau `/mnt/d`: baza SQLite pe un disc Windows văzut din WSL se poate bloca și e lentă.
- Pornire, din folderul proiectului: `python3.11 -m veghe check-sources`, apoi `python3.11 -m veghe run` (Ctrl-C oprește). Fișierul `.env` de lângă `config.toml` e citit automat. Pe Ubuntu 24.04: `python3` în loc de `python3.11`.
- După somn/hibernare, ceasul WSL poate rămâne în urmă (serviciul vă anunță): `wsl --shutdown` în PowerShell și redeschideți Ubuntu.

## Receptor ADS-B propriu (opțional)

Agregatoarele publice depind de voluntari; un receptor în Iași dă date sigure pentru zona orașului și deosebește clar „0 avioane” de „lipsă de date”.

| Componentă | Preț aproximativ |
|---|---|
| FlightAware Pro Stick Plus (cu filtru 1090 MHz) sau RTL-SDR Blog V4 + filtru 1090 | 35–45 € (filtrul 25–30 €) |
| Antenă exterioară verticală 1090 MHz, ~5,5 dBi, conector N | 30–60 € |
| Cablu coaxial cu pierderi mici 5–10 m + adaptor N–SMA | 25–45 € |
| Descărcător / împământare | 15–25 € |
| Raspberry Pi 4 (1–2 GB) + sursă oficială + microSD 32 GB „high endurance” + carcasă | 75–110 € |
| UPS mic (opțional) | 30–60 € |

**Total:** aproximativ 180–280 € (prețuri estimative).

**Amplasare:** acoperiș sau catarg cu orizont liber, mai ales spre est (Prut, R. Moldova); cablu cât mai scurt. Raza teoretică se verifică pe heywhatsthat.com.

**Instalare** (pe Raspberry Pi): scriptul `readsb-install.sh` (wiedehopf/adsb-scripts), apoi `readsb-set-location <lat> <lon>`, câștig automat (`--gain auto`) și, **obligatoriu**, baza de date a aeronavelor (`--db-file /usr/local/share/tar1090/aircraft.csv.gz`; fără ea aeronavele militare nu pot fi deosebite și programul oprește analiza pe aeronavă). Pentru `veghe`: `--net-api-port 8042`, iar în `config.toml`: `local_url = "http://127.0.0.1:8042/?circle={lat},{lon},{radius}&jv2"` și `local_points = ["LRIA Iași"]`. Adresa `127.0.0.1` merge doar dacă `veghe` rulează fără Docker pe același aparat; cu Docker folosiți IP-ul din rețeaua locală al receptorului (și legați API-ul readsb la acea adresă, nu la internet). Dacă receptorul nu răspunde, programul trece singur pe agregatorul public; `check-sources` arată sursa folosită pentru fiecare zonă („local”, „principal”, „rezervă N”) și erorile încercărilor; `/stare` o arată când nu e agregatorul principal și marchează zonele fără date bune în ultimele 5 min. Opțional, receptorul poate alimenta și adsb.lol (cu `--privacy` la MLAT).

## Primele 30–90 de zile („mod umbră”)

- Lăsați `public_enabled = false`. Serviciul doar arhivează și trimite mesaje interne.
- **Nu trebuie să faceți nimic** la fiecare alertă: RO-Alert-ul e preluat automat din presă (mesajul „OFICIAL” în grupul privat).
- Când vreți, după un incident: `docker compose run --rm veghe report --since …` → cât avans a dat fiecare nivel față de RO-Alert. Ora RO-Alert vine din presă (ora publicării, de obicei la câteva minute după alerta reală, deci avansul real e puțin mai mic). Dacă vreți precizie la minut, puteți nota ora cu `/roalert` (cu operatori) sau `docker compose run --rm veghe roalert Iași --at 17:04`, dar nu e necesar.
- Ajustați sursele (scoateți ce nu merge, adăugați RSS-uri verificate) și pragurile din `[engine]`.
- Abia apoi decideți, împreună cu ISU, dacă și ce să publicați.

## Limite cunoscute

- Analiza textului e pe cuvinte-cheie și localități; formulările neobișnuite pot fi ratate. Toate mesajele publice trec prin operator.
- Coordonatele localităților sunt aproximative (±2–5 km); ETA-urile sunt în linie dreaptă.
- Starea se păstrează peste reporniri (ipoteze deschise, VIGILENȚĂ, RO-Alert/ÎNCETARE, NOTAM, aviație), pentru cel mult câteva ore; după o oprire lungă, sistemul pornește de la zero. La prima citire după pornire, știrile fără dată sunt doar arhivate (ca să nu declanșeze alerte vechi).
- RO-Alert-ul e aflat din presă, nu direct din rețeaua RO-Alert (care nu are flux public). Mesajul „OFICIAL” vine deci la câteva minute după alerta de pe telefon; rolul lui e confirmarea, nu avertizarea timpurie (aceea vine din nivelurile anterioare).
- Comanda `roalert` din linia de comandă doar arhivează (pentru raport); serviciul pornit află doar prin `/roalert` pe Telegram (cu operatori).
- ADS-B nu vede dronele; dă doar semnale indirecte (închideri, devieri, bruiaj, reacția aviației militare). Pragurile pentru GNSS, așteptări și ocoliri sunt propuneri, de reglat pe datele adunate. NOTAM-urile R. Moldova cer credențiale FAA (neconfirmat că sunt acolo).
- Acoperă dronele (inclusiv cele cu reacție). Rachetele nu declanșează DIRECȚIE/ATENȚIE/APROPIERE (prea rapide pentru acest lanț de surse publice): doar VIGILENȚĂ și, dacă presa relatează un RO-Alert, OFICIAL. Aviația militară ostilă nu e detectată; avioanele militare vizibile în ADS-B public (de regulă proprii/aliate) apar doar ca rezumat intern. Amenințările terestre nu sunt acoperite.
- Google News RSS nu e un API oficial; poate fi limitat. Previzualizarea t.me/s nu e un API garantat.
