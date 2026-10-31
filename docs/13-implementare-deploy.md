# 13 · Implementarea (Nivelul A) și deploy

*Stare: 31.10.2026. Codul: [`veghe/`](../veghe/). Teste: [`tests/`](../tests/). Configurare: [`config.example.toml`](../config.example.toml), [`.env.example`](../.env.example).*

## Ce face serviciul `veghe`

- **Citește** sursele publice din [11](11-fluxuri-date-harti.md): alerte UA (alerts.in.ua, ukrainealarm, canalul `air_alert_ua`), canale Telegram publice (Forțele Aeriene UA, administrațiile Odesa, Cernăuți, Izmail), presa și Moldpres (RSS, Google News), trafic aerian civil (adsb.lol).
- **Arhivează** fiecare mesaj în SQLite, cu ora de publicare și ora la care l-a primit (pentru măsurarea avansului real).
- **Aplică regulile** din [07](07-arhitectura-sistem.md): VIGILENȚĂ → DIRECȚIE → MOLDOVA → APROPIERE → OFICIAL, cu ETA în intervalul 450/150 km/h.
- **Trimite mesaje INTERNE** într-un grup Telegram privat (și opțional ntfy).
- **Mesaje PUBLICE:** doar retransmiteri ale RO-Alert-urilor relatate de presa/autoritățile românești și încetarea alertei; **niciodată** conținut din canalele ucrainene; **numai după aprobarea unui operator** (`/aproba N`). Canalul public e oprit implicit.
- **Aeronavele militare** sunt ignorate complet la citire (nici măcar nu se numără); se păstrează doar numărători de aeronave civile.
- **Siguranță la livrare:** botul refuză să trimită mesaje interne dacă „grupul intern” e de fapt un canal sau un grup public; refuză ntfy.sh fără token; comenzile sunt acceptate doar de la operatori, doar din grupul intern sau din chat privat, și doar dacă sunt recente (sub 10 minute).
- **Te anunță când orbește:** dacă o sursă cade (3 erori la rând), operatorii primesc „SURSĂ CĂZUTĂ”; la revenire, „Sursa … a revenit”. Dacă bucla principală se blochează peste 5 minute, procesul iese, iar Docker/systemd îl repornește.

### Comenzi pe Telegram (doar operatorii din `TELEGRAM_OPERATOR_IDS`)

| Comandă | Ce face |
|---|---|
| `/stare` | nivelul curent, alertele UA urmărite, ipotezele, sursele cu erori |
| `/ultimele 5` | ultimele semnale arhivate |
| `/coada` | mesajele publice care așteaptă aprobarea |
| `/aproba N` / `/respinge N` | aprobă sau respinge mesajul public N |
| `/roalert Iași 17:04` | **opțional:** notează ora exactă a unui RO-Alert (altfel ora e luată automat din presă) |

### Linia de comandă

| Comandă | Ce face |
|---|---|
| `python -m veghe run` | pornește serviciul |
| `python -m veghe check-sources` | citește fiecare sursă o dată și arată ce a înțeles – **prima verificare live** |
| `python -m veghe replay tests/scenarios/2026-10-31.jsonl` | reia un incident real prin reguli, fără rețea |
| `python -m veghe report --since 2026-11-01T14:00:00Z` | primul semnal pe fiecare nivel vs. RO-Alert (din presă sau, dacă există, notat manual) |
| `python -m veghe roalert Iași --at 17:04` | opțional: doar arhivează ora exactă a unui RO-Alert (pentru raport) |
| `python -m veghe outbox` · `aproba N` · `respinge N` | coada de mesaje publice |

## Ce s-a validat și ce nu

| Nivel | Rezultat | Ce dovedește |
|---|---|---|
| **Revizuire de cod independentă** (4 direcții: corectitudine, siguranță/OPSEC, funcționare 24/7, fidelitatea formatelor) | 49 de constatări, aproape toate confirmate prin reproducere; **toate cele relevante corectate**, fiecare cu test de regresie | vezi istoricul git (commit „Corecturi după revizuirea de cod”) |
| **A doua verificare independentă** (reverificarea corecturilor + căutarea de defecte noi) | 35 de corecturi confirmate; 13 defecte noi introduse de corecturi (ex. o sursă care „picură” date, coadă blocată de reîncercări, articole întârziate) – **toate corectate**, cu teste | |
| **Teste unitare** (geografie, analiza textului uk/ru/ro, parsere) | trec (86 de teste în total) | distanțele coincid cu documentele; parserele citesc fixturile construite după **clienții oficiali** (alerts-in-ua, UkraineAlarm, Home Assistant), **selectorii RSSHub** pentru t.me/s și **documentația readsb** |
| **Scenarii reale** (8.09 și 31.10.2026) | trec | succesiunea de niveluri e cea așteptată; primul mesaj intern vine înaintea retransmiterii RO-Alert; zero conținut ucrainean în mesajele publice |
| **Test complet cu servere simulate** | trece | configurare din TOML + secrete din mediu, autentificarea corectă la API-uri, deduplicare, trimitere pe Telegram, refuzul comenzilor neautorizate, aprobarea unui mesaj public, `check-sources`, pagina de stare |
| **Rulare reală a serviciului** (15 s, fără acces la surse) | merge | bucla nu cade la erori de rețea, aplică pauze progresive (40 s → 10 min), `/health` și `/status` răspund, oprire curată la SIGTERM |
| **Surse reale (live)** | **nevalidat aici** | rețeaua acestei sesiuni blochează Telegram, API-urile ucrainene, Google News și adsb.lol. **Validarea live = `check-sources` pe server, în primele 5 minute** |
| **Imaginea Docker** | **neconstruită aici** | daemonul Docker nu rulează în sesiune; `docker compose config` e valid |

**Ce înseamnă „validat” aici:** logica, parserele și livrarea sunt testate pe formate reale (preluate din clienții oficiali și din sursele RSSHub/readsb) și pe incidentele reale reluate. **Nu** înseamnă că sursele reale răspund exact așa azi: asta se vede doar cu `check-sources` pe server.

## Mod „doar primesc alerte” (fără intervenție)

Configurarea implicită e deja așa:

- `public_enabled = false` → nimic nu pleacă public, deci **nu aveți nimic de aprobat**;
- toate mesajele interne (VIGILENȚĂ, DIRECȚIE, ATENȚIE, APROPIERE, OFICIAL, ÎNCETARE, SURSĂ CĂZUTĂ) vin **automat** în grupul Telegram privat;
- RO-Alert-ul e preluat **automat din presă**; nu trebuie înregistrat;
- comenzile (`/stare`, `/roalert` …) sunt opționale.

Singurele acțiuni: instalarea o dată și `check-sources` la început. În rest, doar citiți mesajele. Mesajele sunt informative; singura sugestie de acțiune apare la APROPIERE fără RO-Alert (anunțarea ISU/112), și rămâne la latitudinea voastră.

## Deploy: de ce aveți nevoie

1. **Un server Linux mic în UE** (1 vCPU, 1 GB RAM, 10 GB disc ajung), cu Docker și Docker Compose. Orice furnizor de VPS. Alternativ, un Raspberry Pi permanent conectat, cu systemd (fără Docker).
2. **Un bot Telegram:** creat cu [@BotFather](https://t.me/BotFather) → `TELEGRAM_BOT_TOKEN`.
3. **Un grup Telegram privat** pentru operatori (fără link/nume public), cu botul adăugat → `TELEGRAM_INTERNAL_CHAT_ID` (începe cu `-100…`; îl aflați trimițând un mesaj în grup și citind `https://api.telegram.org/bot<TOKEN>/getUpdates`). Dacă grupul are nume public (@…), botul refuză să trimită în el.
4. **ID-urile numerice ale operatorilor** → `TELEGRAM_OPERATOR_IDS` (de ex. prin @userinfobot).
5. **Token-uri pentru API-urile ucrainene** (opționale la început; canalul `air_alert_ua` merge fără):
   - alerts.in.ua: formularul [alerts.in.ua/api-request](https://alerts.in.ua/api-request) – descrieți scopul civil cu cuvintele voastre;
   - ukrainealarm: formularul de pe [api.ukrainealarm.com](https://api.ukrainealarm.com).
6. (Opțional) **ID-urile operatorilor** pot lipsi: fără ele nu se pot da comenzi, dar alertele vin oricum.
7. (Mai târziu) **un canal Telegram public**, doar dacă decideți să retransmiteți oficial → `TELEGRAM_PUBLIC_CHAT_ID` + `public_enabled = true`.

## Deploy: pașii (Docker)

```bash
# pe server
git clone -b claude/iasi-drone-early-warning https://github.com/balangheorghe/drone-brainstorming.git veghe && cd veghe
cp config.example.toml config.toml        # ajustați dacă e cazul
cp .env.example .env && nano .env         # completați token-urile
mkdir -p data && sudo chown 10001:10001 data   # utilizatorul din container
docker compose build
docker compose run --rm veghe check-sources    # VALIDAREA LIVE: fiecare sursă trebuie să aibă ✓
docker compose up -d
docker compose logs -f                    # urmăriți primele minute
chmod 600 .env                            # secretele doar pentru voi
```

Actualizare ulterioară: `git pull && docker compose build && docker compose up -d`. (Codul e pe branch-ul `claude/iasi-drone-early-warning` până la unirea în `master`.)

Pe Telegram, în grupul privat: `/stare`. Pagina de stare e disponibilă doar pe server: `curl http://127.0.0.1:8080/status` (sau printr-un tunel SSH).

**Ce faceți dacă `check-sources` arată ✗:**
- `telegram:<canal>` cu „nu conține mesaje publice” → canalul nu are previzualizare publică sau și-a schimbat numele; scoateți-l sau corectați-l în `config.toml`;
- `rss:moldpres` sau alt RSS cu „nu e un flux RSS/Atom” → URL-ul s-a schimbat; căutați `<link rel="alternate" type="application/rss+xml">` în pagina publicației;
- `alerts_in_ua` cu 401/403 → token greșit sau încă neaprobat;
- `adsb` cu 4xx → adsb.lol a introdus cheie (vezi adsb.lol/feed); folosiți airplanes.live sau un receptor propriu.

## Deploy: alternativa fără Docker (systemd)

```bash
sudo useradd --system --home /opt/veghe veghe
sudo git clone -b claude/iasi-drone-early-warning https://github.com/balangheorghe/drone-brainstorming.git /opt/veghe
cd /opt/veghe && sudo cp config.example.toml config.toml && sudo cp .env.example .env   # completați .env
sudo mkdir -p data && sudo chown -R veghe:veghe /opt/veghe/data
sudo -u veghe bash -c 'set -a; . ./.env; python3 -m veghe check-sources'
sudo cp deploy/veghe.service /etc/systemd/system/ && sudo systemctl enable --now veghe
```

Necesită Python ≥ 3.11 și pachetul `tzdata` al sistemului.

## Primele 30–90 de zile („mod umbră”)

- Lăsați `public_enabled = false`. Serviciul doar arhivează și trimite mesaje interne.
- **Nu trebuie să faceți nimic** la fiecare alertă: RO-Alert-ul e preluat automat din presă (mesajul „OFICIAL” în grupul privat).
- Când vreți, după un incident: `python -m veghe report --since …` → cât avans a dat fiecare nivel față de RO-Alert. Ora RO-Alert vine din presă (ora publicării, de obicei la câteva minute după alerta reală, deci avansul real e puțin mai mic). Dacă vreți precizie la minut, puteți nota ora cu `/roalert`, dar nu e necesar.
- Ajustați sursele (scoateți ce nu merge, adăugați RSS-uri verificate) și pragurile din `[engine]`.
- Abia apoi decideți, împreună cu ISU, dacă și ce să publicați.

## Limite cunoscute

- Analiza textului e pe cuvinte-cheie și localități; formulările neobișnuite pot fi ratate. Toate mesajele publice trec prin operator.
- Coordonatele localităților sunt aproximative (±2–5 km); ETA-urile sunt în linie dreaptă.
- Starea ipotezelor e în memorie: după o repornire, ipotezele deschise se pierd (arhiva rămâne). La prima citire după pornire, știrile fără dată sunt doar arhivate (ca să nu declanșeze alerte vechi).
- RO-Alert-ul e aflat din presă, nu direct din rețeaua RO-Alert (care nu are flux public). Mesajul „OFICIAL” vine deci la câteva minute după alerta de pe telefon; rolul lui e confirmarea, nu avertizarea timpurie (aceea vine din nivelurile anterioare).
- `python -m veghe roalert` din linia de comandă doar arhivează (pentru raport); pentru a informa serviciul activ folosiți `/roalert` pe Telegram.
- Google News RSS nu e un API oficial; poate fi limitat. Previzualizarea t.me/s nu e un API garantat.
