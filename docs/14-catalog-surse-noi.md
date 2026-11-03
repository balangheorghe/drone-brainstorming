# 14 · Catalog de surse noi (457), verificate

*Generat pe 03.11.2026. Completează catalogul din [12](12-catalog-surse.md) (141 de intrări): aici sunt doar surse **noi** față de acela. Datele brute (pentru filtrare sau import): [`14-catalog-surse-noi.json`](14-catalog-surse-noi.json).*

## Cum s-a făcut și cum se citește

- **Căutare:** 8 direcții (Ucraina, R. Moldova, România, aviație, OSINT, senzori și infrastructură, instituții internaționale, comunități locale), apoi două runde de completare. Rezultat: 465 candidați unici.
- **Verificare independentă** a fiecărei surse (existență, adresă, activitate, legalitate): **167 confirmate (✔)** și **290 probabile (~)** – există, dar activitatea curentă sau adresa exactă a fluxului n-a putut fi confirmată din mediul de lucru (multe site-uri sunt blocate acolo). 8 au fost excluse (vezi la final).
- **Relevanță (★):** 5 = poate da minute de avans sau confirmare oficială pentru Iași; 1 = context sau istoric.
- **Reguli păstrate:** doar surse publice și legale; fără camere private nesecurizate, interceptări sau date luate din spatele unei autentificări. Sursele rusești de stat apar doar ca context, cu avertisment. Conținutul canalelor ucrainene **nu se republică**.
- Câmpurile *Integrare* și *Atenție* spun cum s-ar putea folosi sursa în `veghe` și ce limite are.

## Pe scurt

| Categorie | Surse | ✔ | ★★★★+ |
|---|---|---|---|
| [Ucraina – alerte și surse oficiale](#ucraina--alerte-și-surse-oficiale) | 53 | 26 | 7 |
| [Republica Moldova](#republica-moldova) | 64 | 8 | 5 |
| [România](#românia) | 62 | 33 | 10 |
| [Aviație, ADS-B, NOTAM, GNSS](#aviație-ads-b-notam-gnss) | 47 | 29 | 1 |
| [OSINT conflict, analize, date istorice](#osint-conflict-analize-date-istorice) | 64 | 27 | 2 |
| [Senzori, meteo, infrastructură](#senzori-meteo-infrastructură) | 45 | 24 | 0 |
| [Instituții internaționale și vecini](#instituții-internaționale-și-vecini) | 59 | 20 | 0 |
| [Comunități locale, rețele sociale, aplicații](#comunități-locale-rețele-sociale-aplicații) | 63 | 0 | 7 |
| **Total** | **457** | **167** | **32** |

## Cele mai utile pentru avertizare (★★★★ și ★★★★★)

- ✔ **[alerts.in.ua API – niveluri roșu/galben + tipuri de amenințare (client oficial alerts-in-ua-py)](<https://github.com/alerts-ua/alerts-in-ua-py>)** · API · cheie gratuită · timp real · ★★★★★ — Clientul oficial al API alerts.in.ua expune acum alert_level (red/yellow) și lista amenințărilor deschise per alertă: drones, cruise_missiles, ballistic_missiles, mig31k_departure, strategic/tactic_aircraft_activity, guided_aerial_bombs; filtrare pe oblast/raion/hromada.
- ~ **[Aeroportul Internațional Iași – tabela sosiri/plecări](<https://aeroport-iasi.ro/>)** · web · liber · minute · ★★★★★ — Tabela live de zboruri (sosiri/plecări, status, terminal) a LRIA. Suspendarea zborurilor (ex. 8.09.2026, ~16:37–17:41) e un semnal de confirmare a închiderii spațiului aerian.
- ~ **[Armata Națională a R. Moldova – canal Telegram (@MDNationalArmy)](<https://t.me/MDNationalArmy>)** · Telegram · liber · minute · ★★★★★ — Canal Telegram al Armatei Naționale/MApărării MD: confirmări de survol, traiectorii de drone prin raioane (ex. Bălți → Ungheni), dezmințiri.
- ~ **[MApN – arhiva comunicatelor (site în română, /cpresa)](<https://www.mapn.ro/cpresa/>)** · web · liber · minute · ★★★★★ — Arhiva oficială a comunicatelor MApN (numerotate, pe lună/an), inclusiv detectări radar de drone, ridicarea avioanelor F-16/F-18 și RO-Alert (ex. 31.10.2026, două drone în NE).
- ~ **[Poliția de Frontieră RM – canal Telegram oficial (@politiadefrontierarm)](<https://t.me/politiadefrontiera>)** · Telegram · liber · minute · ★★★★★ — Canalul oficial IGPF: „Informare!” despre drone care traversează segmentul de frontieră (ex. Palanca; Colibași→Vadul lui Isac→România), fragmente găsite lângă graniță.
- ✔ **[BotosaniNews.ro](<https://www.botosaninews.ro/>)** · web · liber · minute · ★★★★☆ — Știri locale Botoșani: RO-Alert, fotografii ale dronei (Corlăteni, Șendriceni, Dorohoi – 12.09.2026), martori care au auzit drona la joasă înălțime.
- ✔ **[Povitriana Tryvoga – hartă oficială a mișcării aproximative a țintelor aeriene (oct. 2026)](<https://ajax.systems/ua/blog/approximate-movement-of-aerial-targets-in-the-air-alert-app/>)** · hartă · liber · minute · ★★★★☆ — Funcție nouă în aplicația oficială „Повітряна тривога” (Mintsyfra + MApN UA + Forțele Aeriene + Ajax/Stfalcon): direcția aproximativă a rachetelor de croazieră, „Banderol” și Shahed, grilă 10×10 km și heatmap „pericol crescut”; disponibilă și pe un site separat.
- ✔ **[Radio România Iași – știri regionale](<https://www.radioiasi.ro/stiri/regional/>)** · web · liber · minute · ★★★★☆ — Radio public regional: primul anunț al redeschiderii aeroportului (17:41, 8.09.2026), mărturii ale ascultătorilor (dronă văzută la Breazu–Lețcani, 31.10.2026), alerte Botoșani.
- ✔ **[Sistem de alertă pe 2 niveluri (Hotărârea CMU nr. 1092/2026): galben = drone, roșu = rachete/atac combinat](<https://news.dtkt.ua/society/economics/114437-cervonii-ta-zovtii-riven-zagrozi-za-postanovoiu-kmu-1092-iak-iz-nimi-praciuvati-biznesu-z-4-veresnia-2026-r>)** · web · liber · istoric · ★★★★☆ — Din 4.09.2026 (modificată prin Hot. 1128, în vigoare 18.09.2026) alertele aeriene din UA au nivel galben (amenințare dronă) și roșu (rachete/balistice/atac masiv); sirena de încetare a fost eliminată; alertele sunt la nivel de raion din dec. 2025.
- ✔ **[Ziarul de Iași – eticheta «drona»](<https://www.ziaruldeiasi.ro/tag/drona>)** · web · liber · minute · ★★★★☆ — Pagina de etichetă «drona» a celui mai mare cotidian ieșean: actualizări live la RO-Alert (8.09 și 31.10.2026), F-18 spaniole, urmări locale.
- ✔ **[map.ukrainealarm.com – harta oficială a alertelor (Ajax/Mintsyfra)](<https://map.ukrainealarm.com>)** · hartă · liber · timp real · ★★★★☆ — Harta oficială a alertelor aeriene alimentată din același sistem ca aplicația „Повітряна тривога”; vizualizare pe regiuni/raioane.
- ✔ **[monitor (@war_monitor) – monitorizarea aviației inamice](<https://t.me/war_monitor>)** · Telegram · liber · minute · ★★★★☆ — Canalul proiectului „monitor” (~964k abonați), sursa datelor war-monitor.org pentru harta Shahed deja listată; mesaje scurte despre poziția/direcția dronelor și rachetelor.
- ✔ **[єРадар (@eRadarrua)](<https://t.me/eRadarrua>)** · Telegram · liber · minute · ★★★★☆ — Canal de radar civil cu mesaje scurte despre direcția dronelor și rachetelor; 62.000 de mesaje (împreună cu kpszsu) au fost arhivate din preview-ul public pentru un model de predicție.
- ✔ **[„Де Ракета” (@deraketaua) – monitorizare OSINT rachete/Shahed](<https://t.me/deraketaua>)** · Telegram · liber · minute · ★★★★☆ — Unul dintre cele mai populare canale UA de urmărire a rachetelor/Shahed (>153k abonați, iul. 2026); primul mesaj la lansări masive la ~5–12 min după detecție, uneori cu ore estimate de sosire.
- ~ **[Aeroportul Internațional Chișinău (LUKK) – site oficial](<http://www.airport.md/>)** · web · liber · minute · ★★★★☆ — Site-ul aeroportului (sosiri/plecări). Spațiul aerian al R. Moldova e restricționat la incursiuni, iar drone au perturbat aeroportul pe 8.09.2026.
- ~ **[Aeroportul Internațional Chișinău – Online Panel (tabela oficială)](<https://airport.md/passenger/online-panel>)** · web · liber · timp real · ★★★★☆ — Tabela oficială sosiri/plecări cu statusuri; devieri (ex. spre Bacău) și întârzieri apar când spațiul aerian e restricționat din cauza dronelor.
- ~ **[Aeroportul Internațional „Ștefan cel Mare” Suceava – program zboruri](<https://www.aeroportsuceava.ro/en/17-program-zboruri>)** · web · liber · ore · ★★★★☆ — Programul oficial de zboruri LRSV (Wizz Air, TAROM); spațiul aerian al Sucevei a fost închis ~1 oră din cauza unei drone – anulările/întârzierile confirmă restricțiile.
- ~ **[Gruparea de forțe „Sud” (Сили оборони півдня) – Telegram](<https://t.me/s/SJTF_Odes>)** · Telegram · liber · minute · ★★★★☆ — Canalul oficial al grupării de forțe „Південь” (sudul UA, inclusiv Odesa): atacuri cu Shahed asupra regiunii Odesa/Dunăre, doborâri.
- ~ **[ISU Galați – Facebook](<https://www.facebook.com/isugalati/>)** · rețea socială · liber · minute · ★★★★☆ — Pagina oficială ISU Galați (~10.800 urmăritori): intervenții, mesaje după RO-Alert și căderi de drone în Galați.
- ~ **[ISU „Bucovina” Suceava – comunicate de presă](<https://isusv.igsu.ro/comunicate-de-presa>)** · web · liber · ore · ★★★★☆ — Comunicatele ISU Suceava; la 8.09.2026 ISU Suceava a confirmat că nicio dronă nu a căzut și că a părăsit teritoriul spre R. Moldova (Botoșenița Mare – dronă prăbușită într-un lan, alt incident).
- ~ **[ISU „Mihail Sturdza” Iași – comunicate, știri și declarații de presă 2026](<https://isuis.igsu.ro/comunicate-de-presa/stiri-de-presa-2026-175>)** · web · liber · ore · ★★★★☆ — Site-ul oficial ISU Iași (platforma IGSU): liste numerotate de știri, comunicate, declarații și buletine 2026, inclusiv documentul nr. 123/30.01.2026 «Mesaje Ro-Alert emise de ISU Iași».
- ~ **[ISU „Podul Înalt” Vaslui – comunicate de presă](<https://isuvs.igsu.ro/comunicate-de-presa>)** · web · liber · ore · ★★★★☆ — Comunicate ISU Vaslui (județ vecin cu Iași pe direcția de intrare dinspre R. Moldova: Huși, Fălciu); intervenții și bilanțuri, inclusiv la obiecte căzute.
- ~ **[Instituția Prefectului Județul Iași – comunicate](<https://is.prefectura.mai.gov.ro/>)** · web · liber · ore · ★★★★☆ — Comunicatele Prefecturii Iași (prefect Constantin Dolachi-Pelin); în incidentul din 8.09.2026 Prefectura a anunțat încetarea alertei (~17:30) și direcția dronei.
- ~ **[Liveuamap Moldova (subdomeniu + API regiunea 137)](<https://moldova.liveuamap.com>)** · hartă · liber · minute · ★★★★☆ — Pagina Liveuamap dedicată R. Moldova (incidente cu drone, resturi, alerte); API-ul oficial are regiunea Moldova = 137.
- ~ **[MAI RM – secțiunea Știri („MAI informează”)](<https://mai.gov.md/ro/news>)** · web · liber · ore · ★★★★☆ — Știrile MAI (distincte de Sinteza PDF din catalog): închideri temporare ale spațiului aerian, apeluri către populație, coordonare IGP/IGSU/IGPF.
- ~ **[Poliția de Frontieră RM – comunicate „Informare!” + raportul zilnic „Situația la frontieră în 24 ore”](<https://border.gov.md/en/comunicate-de-presa>)** · web · liber · ore · ★★★★☆ — Comunicate oficiale IGPF: survolări neautorizate de drone, fragmente (Etulia, Lencăuți, Cotiujeni/Briceni), plus bilanțul zilnic al frontierei.
- ~ **[Prima Sursă / Первоисточник – canalul Telegram oficial al Guvernului RM](<https://t.me/prima_sursa_md>)** · Telegram · liber · minute · ★★★★☆ — Canalul oficial de informare/verificare al Guvernului RM; anunță survolări de drone și restricționarea/redeschiderea spațiului aerian (ex. Shahed peste Dubăsari/Orhei, 30.03.2026).
- ~ **[Vinnîțea OVA – canal Telegram (@vinnytskaODA)](<https://t.me/vinnytskaODA>)** · Telegram · liber · minute · ★★★★☆ — Canalul oficial al administrației militare regionale Vinnîțea: alerte, drone doborâte, impacturi (inclusiv raioanele Mohyliv-Podilskyi, Tulchyn, Zhmerynka, vecine cu R. Moldova).
- ~ **[Вінницька ОДА/ОВА – canal Telegram](<https://t.me/s/VinnytsiaODA>)** · Telegram · liber · minute · ★★★★☆ — Canalul administrației militare Vinnîțea: statusuri de alertă pe raioane, consecințe atacuri; complementar site-ului vin.gov.ua (deja în catalog).
- ~ **[Могилів-Подільська міська рада – canal Telegram](<https://t.me/s/mog_pod_mr>)** · Telegram · liber · minute · ★★★★☆ — Canal oficial al orașului Mohyliv-Podilskyi (pe Nistru, vizavi de Otaci, MD): alerte și știri operative; punct de intrare al dronelor din Vinnîțea spre nordul MD.
- ~ **[Суспільне Одеса – canal Telegram](<https://t.me/s/suspilneodesa>)** · Telegram · liber · minute · ★★★★☆ — Radiodifuzorul public regional (~47.000 abonați): postări operative despre alerte aeriene și drone în raioanele Odesa, inclusiv Bugeac/Dunăre.
- ~ **[Суспільне Чернівці – canal Telegram](<https://t.me/s/suspilne_chernivtsi>)** · Telegram · liber · minute · ★★★★☆ — Publică alerte pe raioane, inclusiv raionul Dnistrovskyi (Novodnistrovsk, Sokyriany) – vecin cu Briceni/Ocnița (MD) – cu nivel «dronova zahroza».

## Ucraina – alerte și surse oficiale

- ✔ **[alerts.in.ua API – niveluri roșu/galben + tipuri de amenințare (client oficial alerts-in-ua-py)](<https://github.com/alerts-ua/alerts-in-ua-py>)** · API · cheie gratuită · timp real · ★★★★★ · flux: <https://api.alerts.in.ua/v1/alerts/active.json>  
  Clientul oficial al API alerts.in.ua expune acum alert_level (red/yellow) și lista amenințărilor deschise per alertă: drones, cruise_missiles, ballistic_missiles, mig31k_departure, strategic/tactic_aircraft_activity, guided_aerial_bombs; filtrare pe oblast/raion/hromada.  
  *Integrare:* pip install alerts-in-ua; polling la 15–30 s pe /v1/alerts/active.json și /v2/iot/active_air_raid_alerts.json; declanșare internă când threat_type='drones' apare în raioanele Izmail, Bolhrad, Bilhorod-Dnistrovskyi, Podilsk, Mohyliv-Podilskyi, Dnistrovskyi; 'strategic_aircraft_activity'/'mig31k_departure' = pre-avertizare (aviație militară RU, informație publică).  
  *Atenție:* Token obligatoriu (formular alerts.in.ua/api-request); threats doar pentru alerte active (istoricul nu le are); nivelul amenințării e independent de nivelul alertei; respectați cache/rate-limit; nu republicați.
- ✔ **[map.ukrainealarm.com – harta oficială a alertelor (Ajax/Mintsyfra)](<https://map.ukrainealarm.com>)** · hartă · liber · timp real · ★★★★☆  
  Harta oficială a alertelor aeriene alimentată din același sistem ca aplicația „Повітряна тривога”; vizualizare pe regiuni/raioane.  
  *Integrare:* Afișare în dashboard-ul intern (iframe/link) lângă harta veghe; datele brute se iau din API ukrainealarm (deja în catalog) – nu scrapați harta.  
  *Atenție:* Arată starea alertelor, nu traiectorii; o hartă goală nu înseamnă lipsa pericolului.
- ✔ **[monitor (@war_monitor) – monitorizarea aviației inamice](<https://t.me/war_monitor>)** · Telegram · liber · minute · ★★★★☆ · flux: <https://t.me/s/war_monitor>  
  Canalul proiectului „monitor” (~964k abonați), sursa datelor war-monitor.org pentru harta Shahed deja listată; mesaje scurte despre poziția/direcția dronelor și rachetelor.  
  *Integrare:* Citire t.me/s/war_monitor; regex pe toponime din sudul Odesei și Podolia; corelare automată cu alertele oficiale (alerts.in.ua).  
  *Atenție:* Neoficial, „nu e sistem oficial de alertă” (autori); poziții aproximative; nu republicați.
- ✔ **[Povitriana Tryvoga – hartă oficială a mișcării aproximative a țintelor aeriene (oct. 2026)](<https://ajax.systems/ua/blog/approximate-movement-of-aerial-targets-in-the-air-alert-app/>)** · hartă · liber · minute · ★★★★☆  
  Funcție nouă în aplicația oficială „Повітряна тривога” (Mintsyfra + MApN UA + Forțele Aeriene + Ajax/Stfalcon): direcția aproximativă a rachetelor de croazieră, „Banderol” și Shahed, grilă 10×10 km și heatmap „pericol crescut”; disponibilă și pe un site separat.  
  *Integrare:* Monitorizare vizuală de operator în timpul atacurilor spre Odesa/Dunăre; fără API public confirmat – doar observare/captură manuală pentru confirmarea direcției.  
  *Atenție:* Nu arată coordonate exacte și nu e în timp real (întârzieri); fără balistice și ținte >2000 km/h; adresa site-ului separat neconfirmată; nu înlocuiește alertele.
- ✔ **[Sistem de alertă pe 2 niveluri (Hotărârea CMU nr. 1092/2026): galben = drone, roșu = rachete/atac combinat](<https://news.dtkt.ua/society/economics/114437-cervonii-ta-zovtii-riven-zagrozi-za-postanovoiu-kmu-1092-iak-iz-nimi-praciuvati-biznesu-z-4-veresnia-2026-r>)** · web · liber · istoric · ★★★★☆  
  Din 4.09.2026 (modificată prin Hot. 1128, în vigoare 18.09.2026) alertele aeriene din UA au nivel galben (amenințare dronă) și roșu (rachete/balistice/atac masiv); sirena de încetare a fost eliminată; alertele sunt la nivel de raion din dec. 2025.  
  *Integrare:* Referință de semantică pentru parserul de alerte: mapare galben→'Shahed spre raionul X', roșu→rachete; actualizați regulile din veghe care tratează toate alertele la fel.  
  *Atenție:* Text de presă juridică, nu textul oficial; verificați Hotărârea pe kmu.gov.ua; criteriile galben/roșu pot fi revizuite săptămânal.
- ✔ **[„Де Ракета” (@deraketaua) – monitorizare OSINT rachete/Shahed](<https://t.me/deraketaua>)** · Telegram · liber · minute · ★★★★☆ · flux: <https://t.me/s/deraketaua>  
  Unul dintre cele mai populare canale UA de urmărire a rachetelor/Shahed (>153k abonați, iul. 2026); primul mesaj la lansări masive la ~5–12 min după detecție, uneori cu ore estimate de sosire.  
  *Integrare:* Citire t.me/s/deraketaua (sau Telethon) la 30–60 s; filtre pe „Одещина”, „Ізмаїл”, „Дунай”, „Вінниччина”, „Могилів”, „Молдова”, „Румунія”; doar semnal de pre-alertă internă.  
  *Atenție:* Neoficial, erori și retractări posibile; nu folosiți ca unică confirmare; ritm propriu, nu al Forțelor Aeriene.
- ~ **[Vinnîțea OVA – canal Telegram (@vinnytskaODA)](<https://t.me/vinnytskaODA>)** · Telegram · liber · minute · ★★★★☆ · flux: <https://t.me/s/vinnytskaODA>  
  Canalul oficial al administrației militare regionale Vinnîțea: alerte, drone doborâte, impacturi (inclusiv raioanele Mohyliv-Podilskyi, Tulchyn, Zhmerynka, vecine cu R. Moldova).  
  *Integrare:* Citire t.me/s/vinnytskaODA la 60 s; filtre „Могилів-Подільський”, „БпЛА”, „збито”; confirmare oficială pentru culoarul nordic spre MD/Iași.  
  *Atenție:* Postări uneori după încheierea atacului; canal personalizat al șefului OVA. Verificare: Handle-ul apare în listele oficiale și în scrapere, dar nu am confirmat activitatea curentă. Unele liste au și @VinnytsiaODA. De verificat manual (abonați și postări recente).
- ✔ **[eTryvoga – versiunea web (app.etryvoga.com) și canalul voluntar](<https://app.etryvoga.com>)** · web · liber · timp real · ★★★☆☆ · flux: <https://t.me/s/UkraineAlarmSignal>  
  Aplicație web eTryvoga și flux voluntar de alerte/amenințări (sursa setului „volunteer” din datasetul Vadimkin); complementar aplicației eTryvoga din App Store deja listate. Conținut neverificat din sandbox.  
  *Integrare:* Verificare vizuală + comparare cu alertele oficiale; nu există API public confirmat.  
  *Atenție:* Neoficial (voluntari); datele pot diferi de cele oficiale; feed Telegram neconfirmat.
- ✔ **[Evropeiska Pravda (eurointegration.com.ua)](<https://www.eurointegration.com.ua>)** · web · liber · ore · ★★★☆☆ · flux: <https://www.eurointegration.com.ua/rss/>  
  Publicația UP pentru afaceri europene: acoperă incidentele cu drone în Moldova/România din perspectivă UA (ex. „Молдова засудила порушення свого авіапростору російським Шахедом”, 14.03.2026).  
  *Integrare:* Monitorizare (Google News site:eurointegration.com.ua); confirmare post-incident și reacții diplomatice.  
  *Atenție:* Feed RSS neconfirmat; nu e sursă de avertizare.
- ✔ **[Serviciul Grăniceri al Ucrainei – DPSU (@DPSUkr)](<https://t.me/DPSUkr>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/DPSUkr>  
  Canal oficial DPSU: atacuri asupra punctelor de trecere (ex. Starokozache, 9.09.2026, 2 morți – drona a intrat apoi în MD) și situația la frontiera cu MD/RO.  
  *Integrare:* Citire t.me/s; filtre „Старокозаче”, „Рені”, „Ізмаїл”, „Молдова”; confirmare atac la granița MD/RO.  
  *Atenție:* Listă oficială din 2022; există canale false care imită DPSU (avertizare 2022).
- ✔ **[Suspilne Cernăuți (suspilne.media/chernivtsi)](<https://suspilne.media/chernivtsi/>)** · web · liber · minute · ★★★☆☆  
  Redacția regională publică Cernăuți: articole despre drone peste Bucovina, ținte doborâte, alerte (ex. „Російські безпілотники над Буковиною...”).  
  *Integrare:* Monitorizare pagină/Google News pe site:suspilne.media/chernivtsi; extragere oră + raion (Dnistrovskyi, Cernăuți).  
  *Atenție:* Feed RSS neconfirmat (listări terțe FeedSpot); articolele vin după eveniment.
- ✔ **[Suspilne Odesa (suspilne.media/odesa)](<https://suspilne.media/odesa/>)** · web · liber · minute · ★★★☆☆  
  Redacția regională publică Odesa: cronica atacurilor din regiune, impacturi pe porturile dunărene și energie.  
  *Integrare:* Monitorizare pagină / Google News site:suspilne.media/odesa; extragere toponime (Izmail, Reni, Kiliia) pentru confirmare post-incident.  
  *Atenție:* Feed RSS neconfirmat; latență de la minute la ore.
- ✔ **[Ukrhydroenergo – complexul hidro Nistru (Novodnistrovsk) / comunicate](<https://uhe.gov.ua>)** · web · liber · ore · ★★★☆☆  
  Operatorul hidrocentralelor Nistru (HPP/PSPP Novodnistrovsk), țintă a atacului din 7.03.2026 (11 drone + 4 Kalibr) cu poluare transfrontalieră a Nistrului; culoar de drone spre nordul Moldovei.  
  *Integrare:* Monitorizare comunicate + corelare cu alertele raionului Dnistrovskyi (Cernăuți) și cu avertizările de mediu din MD.  
  *Atenție:* Site neaccesat din sandbox (domeniu din cunoștințe generale); comunicatele vin după eveniment.
- ~ **[Aplicația de stat de alertare pe baza Diia (anunțată 4.09.2026)](<https://dou.ua/lenta/news/diia-app-air-alarm/>)** · aplicație · necunoscut · timp real · ★★★☆☆  
  Guvernul UA a anunțat o aplicație de stat bazată pe Diia pentru alerte și mișcarea Shahed/rachetelor – „sursă unică de stat”; portalul Diia urma modernizat până la 1.12.2026.  
  *Integrare:* De urmărit lansarea; dacă oferă API/feed public, integrare ca sursă oficială primară.  
  *Atenție:* În dezvoltare; termene și funcții nepublicate; probleme de confidențialitate semnalate. Verificare: Doar un anunț din 4.09.2026: nu există încă aplicație, sursă operațională sau feed, iar tipul „app” e prematur. Neverificat în această sesiune; urmăriți lansarea.
- ~ **[Bilhorod-Dnistrovskyi RVA/RDA – site oficial](<https://bd-rda.od.gov.ua>)** · web · liber · ore · ★★★☆☆  
  Raionul Bilhorod-Dnistrovskyi (Liman Nistru, Zatoka, Starokozache), lovit frecvent; la granița cu MD. Site-ul administrației: comunicate, avertizări, consecințe ale atacurilor.  
  *Integrare:* Verificare periodică (WordPress → încercați /feed/; neconfirmat) sau Google News site:bd-rda.od.gov.ua; folosit pentru confirmare post-incident.  
  *Atenție:* Site-ul nu a putut fi accesat din sandbox; actualizări rare/lente; informația rapidă apare pe Telegram-ul OVA/RVA (handle RVA neconfirmat). Verificare: Domeniul există în date derivate din Wikipedia. Activitatea nu e confirmată.
- ~ **[Bolhrad RVA/RDA – site oficial](<https://bolgrad-rda.od.gov.ua>)** · web · liber · ore · ★★★☆☆  
  Raionul Bolhrad, la granița cu R. Moldova (sudul Basarabiei), pe culoarul dronelor spre Dunăre/Moldova. Site-ul administrației: comunicate, avertizări, consecințe ale atacurilor.  
  *Integrare:* Verificare periodică (WordPress → încercați /feed/; neconfirmat) sau Google News site:bolgrad-rda.od.gov.ua; folosit pentru confirmare post-incident.  
  *Atenție:* Site-ul nu a putut fi accesat din sandbox; actualizări rare/lente; informația rapidă apare pe Telegram-ul OVA/RVA (handle RVA neconfirmat). Verificare: Domeniul există în date derivate din Wikipedia. Activitatea nu e confirmată.
- ~ **[Comandamentul Aerian „Sud” (Повітряне командування «Південь») – comunicate](<https://armyinform.com.ua/2024/07/02/povitryane-komanduvannya-pivden-povidomylo-pro-znyshhenyj-vorozhyj-bezpilotnyk/>)** · rețea socială · liber · ore · ★★★☆☆  
  Comandamentul apărării aeriene pentru sudul UA (inclusiv brigada AA Odesa): bilanțuri Shahed doborâte în regiunea Odesa, infirmări de zvonuri.  
  *Integrare:* Monitorizare pagina Facebook (URL neconfirmat) prin preluările ArmyInform/Suspilne; analiză post-incident.  
  *Atenție:* Feed neconfirmat (Facebook/Telegram); publică de obicei după atac. Verificare: Comandamentul există, dar URL-ul e un articol ArmyInform din iul. 2024, nu o sursă/flux. Comandamentul postează pe Facebook (pagină neconfirmată), iar datele lui apar și în @kpszsu (deja în catalog). Relevanță marginală.
- ~ **[Hmelnîțkîi OVA – canal Telegram (@khmelnytskaODA)](<https://t.me/khmelnytskaODA>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/khmelnytskaODA>  
  Canal oficial OVA Hmelnîțkîi: drone peste regiune, care pot coborî apoi spre Cernăuți/Moldova.  
  *Integrare:* Citire t.me/s; folosit ca semnal „amonte” pentru culoarul nord-vestic spre Bucovina.  
  *Atenție:* Relevanță indirectă pentru Iași; verificați că handle-ul e încă activ (listă din 2023). Verificare: Handle-ul apare doar în surse din 2022–2023 și în lista KMU. Activitatea curentă nu e confirmată. Relevanța pentru Iași e mică.
- ~ **[Izmail RVA/RDA – site oficial](<https://izmail-rda.od.gov.ua>)** · web · liber · ore · ★★★☆☆  
  Raionul Izmail (Izmail, Reni, Kiliia, Vylkove) – vizavi de Tulcea/Galați; cel mai expus raion la atacurile pe porturile dunărene. Site-ul administrației: comunicate, avertizări, consecințe ale atacurilor.  
  *Integrare:* Verificare periodică (WordPress → încercați /feed/; neconfirmat) sau Google News site:izmail-rda.od.gov.ua; folosit pentru confirmare post-incident.  
  *Atenție:* Site-ul nu a putut fi accesat din sandbox; actualizări rare/lente; informația rapidă apare pe Telegram-ul OVA/RVA (handle RVA neconfirmat). Verificare: Domeniul RVA Izmail apare în date derivate din Wikipedia, dar nu am văzut pagina live. Telegramul Izmail RDA e deja în catalog, iar site-ul e mai lent.
- ~ **[Purtătorul de cuvânt al Marinei / Forțelor de Apărare Sud (Dmîtro Pletenciuk) – tag Ukrinform](<https://www.ukrinform.ua/tag-pletencuk>)** · web · liber · ore · ★★★☆☆  
  Declarații ale Marinei UA și ale centrului de presă al Forțelor de Apărare Sud despre Shahed venite dinspre mare spre Odesa și pe coridorul maritim.  
  *Integrare:* Monitorizare pagina-tag (Google News); extragere declarații despre rute maritime ale dronelor (relevante pentru Dunăre).  
  *Atenție:* Canalul Telegram oficial al Forțelor de Apărare Sud nu a putut fi confirmat; declarațiile vin post-eveniment. Verificare: Pagina tag nu a fost văzută direct, dar forma URL se potrivește cu transliterarea Ukrinform („pletencuk”, „tag-evrointegracia”). Corecție: Pletenciuk e din nou purtătorul de cuvânt al Marinei UA; a părăsit FA Sud în iun. 2024.
- ~ **[siren.pp.ua – oglindă publică (fără cheie) a API ukrainealarm](<https://siren.pp.ua>)** · API · liber · timp real · ★★★☆☆ · flux: <https://siren.pp.ua/api/v3>  
  Wrapper public peste api.ukrainealarm.com (proiect PaulAnnekov/uasiren), fără cheie, limită 50 cereri/min/IP.  
  *Integrare:* Fallback când cheia ukrainealarm lipsește sau API-ul principal cade: GET pe https://siren.pp.ua/api/v3/... (aceleași rute ca ukrainealarm v3).  
  *Atenție:* Serviciu voluntar, fără SLA; clientul PyPI uasiren e din 2022 – verificați că oglinda e încă activă; respectați limita. Verificare: Există o oglindă publică, fără cheie, a API ukrainealarm (limită de 50 req/min/IP). Integrarea Home Assistant o folosește încă, dar clientul uasiren nu mai e actualizat din 2022. Nu am putut confirma că endpointul răspunde azi. Se suprapune cu intrarea existentă „Home Assistant – Ukraine Alarm”, care e construită pe ea.
- ~ **[Suspilne Vinnîțea – canal Telegram (@suspilne_vinnytsia)](<https://t.me/suspilne_vinnytsia>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/suspilne_vinnytsia>  
  Radiodifuzorul public, redacția Vinnîțea: știri rapide despre alerte, explozii, drone în regiune.  
  *Integrare:* Citire t.me/s; deduplicare cu OVA; sursă de presă cu standard editorial.  
  *Atenție:* Preia adesea OVA cu întârziere; nu e sursă militară. Verificare: Handle-ul apare în scrapere regionale, dar activitatea curentă nu e confirmată.
- ~ **[UKR.NET – pagina-tag Mohyliv-Podilskyi](<https://www.ukr.net/tags/mogiliv-podilskij.html>)** · web · liber · minute · ★★★☆☆  
  Agregatorul de știri UKR.NET grupează articolele locale (inclusiv surse ca „mogpodonline”) despre Mohyliv-Podilskyi.  
  *Integrare:* Polling pagină la 5 min; extragere titluri cu „дрон/шахед/вибух/Молдова”; semnal de coroborare pentru culoarul Otaci–Soroca.  
  *Atenție:* Agregator; calitatea surselor variază; necesită JavaScript pentru unele pagini; fără RSS confirmat. Verificare: Pagina-tag de pe agregatorul UKR.NET apare în rezultatele de căutare ale agentului anterior. Nu am confirmat-o independent; feedul e neconfirmat.
- ~ **[UKR.NET – știri regionale Odesa (și Cernăuți)](<https://www.ukr.net/news/odesa.html>)** · web · liber · minute · ★★★☆☆  
  Agregator cu titlurile presei locale și naționale despre Odesa și regiune (ex. „Одещина: «шахеди» вдарили по Ізмаїльському району”); există și articole din secțiunea Cernăuți (/news/details/chernivtsi/...).  
  *Integrare:* Polling la 2–5 min; filtrare pe Izmail/Reni/Kiliia/Bolhrad; deduplicare cu sursele oficiale.  
  *Atenție:* Agregator, nu sursă primară; pagina Cernăuți analogă neconfirmată ca URL de listă. Verificare: Agentul anterior a văzut varianta rusă (/ru/news/odesa.html). Varianta ucraineană e probabilă, dar neconfirmată independent.
- ✔ **[ArmyInform – agenția MApN Ucraina (@armyofukraine + armyinform.com.ua)](<https://armyinform.com.ua>)** · web · liber · ore · ★★☆☆☆ · flux: <https://armyinform.com.ua/feed/>  
  Agenția de presă a Ministerului Apărării UA: preia comunicatele Comandamentului Aerian „Sud”, Forțelor de Apărare Sud etc. (ex. „Повітряне командування «Південь» повідомило про знищений безпілотник”).  
  *Integrare:* Ingestie Telegram t.me/s/armyofukraine; site WordPress (/feed probabil, neconfirmat); filtrare „Одещина/Південь”.  
  *Atenție:* Sursă oficioasă (MApN); latență ore; ton propagandistic posibil.
- ✔ **[Centrul pentru Contracararea Dezinformării (@CenterCounteringDisinformation)](<https://t.me/CenterCounteringDisinformation>)** · Telegram · liber · ore · ★★☆☆☆ · flux: <https://t.me/s/CenterCounteringDisinformation>  
  Organism CNSA UA care demontează fake-uri rusești, inclusiv despre incidente cu drone în RO/MD.  
  *Integrare:* Citire t.me/s; marcare automată a știrilor infirmate în veghe.  
  *Atenție:* Perspectivă guvernamentală UA; nu e sursă de avertizare.
- ✔ **[Consiliul municipal Izmail – site oficial (izmail-mr.od.gov.ua)](<https://izmail-mr.od.gov.ua>)** · web · liber · ore · ★★☆☆☆  
  Site-ul primăriei Izmail: comunicate, sistemul local de avertizare, rapoarte ale primarului.  
  *Integrare:* Verificare periodică/Google News; confirmare post-incident pentru Izmail (vizavi de Tulcea).  
  *Atenție:* Nu e sursă de avertizare timpurie; feed neconfirmat; site neaccesat din sandbox.
- ✔ **[DSNS Ucraina (Serviciul de Urgență) – Telegram @dsns_telegram + dsns.gov.ua](<https://t.me/dsns_telegram>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/dsns_telegram>  
  Canal oficial DSNS: incendii și distrugeri după atacuri (inclusiv direcția regională Odesa), număr de victime, intervenții.  
  *Integrare:* Citire t.me/s; filtrare „Одеська область/Ізмаїл”; confirmare post-incident a impacturilor.  
  *Atenție:* Listă oficială din 2022 – verificați activitatea; existau mesaje false „de la DSNS” (2024).
- ✔ **[DTEK Odesa (Одеські електромережі) – pagina de întreruperi + canal DTEK](<https://www.dtek-oem.com.ua/ua/shutdowns>)** · web · liber · minute · ★★☆☆☆  
  Grafice și întreruperi de urgență în Odesa și regiune; după atacuri apar deconectări în Izmail/Odesa – proxy pentru confirmarea loviturilor pe energie.  
  *Integrare:* Polling pagină; detectare „аварійні відключення” pe localități din sud; canalul DTEK (t.me/dtek_ua, citat de presă) ca semnal suplimentar.  
  *Atenție:* Nu indică cauza exactă; site posibil protejat anti-bot; handle t.me/dtek_ua neconfirmat direct.
- ✔ **[NikVesti (Mîkolaiv) – știri regionale sud, inclusiv EN](<https://nikvesti.com>)** · web · liber · minute · ★★☆☆☆  
  Publicație din Mîkolaiv care acoperă și atacurile asupra regiunii Odesa (ex. „Russian drones damage port infrastructure in Odesa region”), cu versiune engleză.  
  *Integrare:* Monitorizare/Google News; sursă secundară pentru sud.  
  *Atenție:* Feed neconfirmat; relevanță indirectă.
- ✔ **[Spravdi (Centrul de Comunicații Strategice) – lista celor 100 de canale rusești care imită canale ucrainene](<https://spravdi.gov.ua/en/100-russian-telegram-channels-that-mimic-ukrainian-ones>)** · web · liber · istoric · ★★☆☆☆  
  Listă oficială de canale Telegram rusești deghizate în surse ucrainene.  
  *Integrare:* Folosire ca listă neagră în colectorul Telegram al veghe (ignorare/scor negativ).  
  *Atenție:* Listă statică, poate fi depășită; perspectivă guvernamentală UA.
- ✔ **[Statul Major General al FA UA (@GeneralStaffZSU)](<https://t.me/GeneralStaffZSU>)** · Telegram · liber · ore · ★★☆☆☆ · flux: <https://t.me/s/GeneralStaffZSU>  
  Rapoarte oficiale zilnice (inclusiv numărul de UAV doborâte/folosite) și comunicate militare.  
  *Integrare:* Ingestie zilnică pentru seria de timp a atacurilor; analiză post-incident.  
  *Atenție:* Bilanțuri agregate, fără detalii geografice fine; latență de ore.
- ✔ **[Ukrainska Pravda – RSS](<https://www.pravda.com.ua/rss/>)** · RSS · liber · minute · ★★☆☆☆ · flux: <https://www.pravda.com.ua/rss/view_news/>  
  Flux RSS al Ukrainska Pravda (toate materialele / doar știri / cele mai importante); pagina rss-info pentru versiunea engleză.  
  *Integrare:* Ingestie RSS la 2–5 min; filtrare pe Odesa/Izmail/Moldova/Румунія.  
  *Atenție:* Calea exactă a fluxurilor: confirmată prin pagina rss-info + listare terță FeedSpot; verificați la integrare.
- ✔ **[Ukrinform – rubrica „ATO/război” (anunțuri de alertă) + sitemap](<https://www.ukrinform.ua/rubric-ato>)** · web · liber · minute · ★★☆☆☆ · flux: <https://www.ukrinform.net/sitemap/last.xml>  
  Agenția de stat Ukrinform publică știri de tip „У низці регіонів оголошена повітряна тривога через загрозу безпілотників” și bilanțuri regionale (ex. resturi de dronă în Bucovina).  
  *Integrare:* Polling rubrică sau sitemap (ukrinform.net/sitemap/last.xml pentru EN); filtrare Odesa/Bucovina/Vinnîțea.  
  *Atenție:* RSS „block-lastnews” neconfirmat; sitemap ≠ RSS; latență minute-ore.
- ✔ **[UNIAN – RSS știri (ucraineană/engleză)](<https://www.unian.ua>)** · RSS · liber · minute · ★★☆☆☆ · flux: <https://rss.unian.net/site/news_ukr.rss>  
  Agenția UNIAN: știri non-stop, inclusiv pagini „Odesa azi” și atacuri asupra energiei din Odesa.  
  *Integrare:* Ingestie RSS; filtre geografice; deduplicare.  
  *Atenție:* URL-urile RSS provin din listare terță (FeedSpot) – verificați; versiunea .net e rusofonă.
- ✔ **[Vadimkin – Ukrainian air raid sirens dataset (oficial + voluntari, CSV)](<https://github.com/Vadimkin/ukrainian-air-raid-sirens-dataset>)** · set de date · liber · zile · ★★☆☆☆ · flux: <https://raw.githubusercontent.com/Vadimkin/ukrainian-air-raid-sirens-dataset/main/datasets/volunteer_data_en.csv>  
  CSV cu toate alertele oficiale din 15.03.2022 (nivel oblast/raion/hromada) și set voluntar eTryvoga din 25.02.2022; util pentru statistici pe Odesa/Vinnytsia/Chernivtsi și ore tipice de atac.  
  *Integrare:* Import zilnic CSV (raw.githubusercontent) în DuckDB; calcul frecvență alerte pe raioanele de graniță vs. incidente RO/MD pentru modele de predicție.  
  *Atenție:* Ultimul rând observat: 07.09.2026 – actualizarea pare oprită/întârziată; ore în UTC; sirene permanente (Luhansk, Crimeea) excluse.
- ✔ **[„Карта повітряних тривог ‼️ Вибухи ‼️ Ракети” (@povitryanatrivogaaa)](<https://t.me/povitryanatrivogaaa>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/povitryanatrivogaaa>  
  Canal OSINT popular cu hartă/mesaje despre alerte, explozii și rachete.  
  *Integrare:* Sursă secundară de coroborare în colectorul Telegram; ponderare mică în scorul de încredere.  
  *Atenție:* Neoficial; texty.org.ua a documentat canale de „alertă” care folosesc tehnici murdare pentru audiență – verificați încrucișat.
- ~ **[Administrația Porturilor Maritime ale Ucrainei (USPA/АМПУ)](<https://www.uspa.gov.ua>)** · web · liber · ore · ★★☆☆☆  
  Comunicate despre loviturile asupra porturilor Izmail și Reni (terminale avariate, nave lovite) și starea operării porturilor.  
  *Integrare:* Monitorizare comunicate; corelare cu AIS (aisstream) și cu alertele raionului Izmail.  
  *Atenție:* Comunicate post-incident; site neaccesat din sandbox. Verificare: Site oficial AMPU; domeniul apare în listele de domenii guvernamentale UA. Activitatea nu a fost verificată în sesiune. Util post-incident (atacuri pe porturile Izmail/Reni).
- ~ **[AlarmMap (alarmmap.online) – agregator de alerte și urgențe](<https://alarmmap.online>)** · hartă · liber · timp real · ★★☆☆☆  
  Hartă terță (Agroprep UA) care agregă alertele aeriene și alte situații de urgență, cu detaliu la nivel de raion.  
  *Integrare:* Oglindă vizuală de rezervă când alerts.in.ua/map.ukrainealarm.com sunt indisponibile; fără API public confirmat.  
  *Atenție:* Terț, neoficial; neaccesat din sandbox; sursa datelor nedeclarată în rezultate. Verificare: Site existent, folosit ca sursă de alerte de proiecte open-source; neoficial. Activitatea curentă și existența unui API nu sunt confirmate.
- ~ **[Bessarabia Inform (bessarabiainform.com) – presă locală Izmail/sudul Basarabiei](<https://bessarabiainform.com>)** · web · liber · ore · ★★☆☆☆  
  Publicație online locală din Izmail care acoperă sudul regiunii Odesa (Izmail, Reni, Kiliia, Bolhrad).  
  *Integrare:* Monitorizare / Google News site:bessarabiainform.com; confirmare locală post-incident pentru porturile dunărene.  
  *Atenție:* Feed neconfirmat; neaccesat din sandbox; dovada existenței e un articol academic (2021). Verificare: Domeniul există (apare în listele de filtre AdGuard). E presă locală din Izmail, în rusă. Activitatea curentă e neconfirmată; tratați-l cu prudență.
- ~ **[Glavcom – secțiunea regională Vinnîțea](<https://glavcom.ua/vinnytsia/>)** · web · liber · minute · ★★☆☆☆  
  Știri regionale Vinnîțea (alerte, impacturi, situația din raioanele de lângă Moldova).  
  *Integrare:* Monitorizare/Google News site:glavcom.ua/vinnytsia; coroborare cu @vinnytskaODA.  
  *Atenție:* Feed neconfirmat; sursă de presă secundară. Verificare: Secțiunea regională Glavcom există (mențiuni pe GitHub), dar activitatea curentă e neconfirmată. Relevanță scăzută.
- ~ **[Interfax-Ukraine – ultimele știri](<https://interfax.com.ua/news/latest.html>)** · web · liber · minute · ★★☆☆☆  
  Fluxul de ultimă oră Interfax-Ukraine (citează OVA, Forțele de Apărare, Statul Major).  
  *Integrare:* Polling pagină la 2–5 min; deduplicare cu OVA.  
  *Atenție:* Feed RSS neconfirmat; agregă surse oficiale cu întârziere. Verificare: Agenția e activă. Pagina „latest-50.html” nu e confirmată; scraperele folosesc latest.html. Niciun RSS confirmat.
- ~ **[LIGA.net – știri regionale (region_news)](<https://news.liga.net/ua/region_news>)** · web · liber · minute · ★★☆☆☆ · flux: <https://news.liga.net/ua/all/rss.xml>  
  Secțiune regională cu relatări live despre atacuri asupra porturilor dunărene (Izmail, Reni) și drone lângă România.  
  *Integrare:* Monitorizare secțiune/Google News; extragere toponime pentru cronologie.  
  *Atenție:* Feed neconfirmat; multe articole vechi (2023) în index. Verificare: Secțiunea region_news apare doar cu articole din 2022–2023 și fără /ua/. Activitatea curentă e neconfirmată. Feed-ul găsit e general, nu regional.
- ~ **[Mohyliv-Podilskyi RVA/RDA – site (rda.m-p.org.ua)](<http://rda.m-p.org.ua>)** · web · liber · ore · ★★☆☆☆  
  Administrația raionului Mohyliv-Podilskyi (vizavi de Otaci, MD) – raion de tranzit pentru drone spre nordul Moldovei.  
  *Integrare:* Verificare periodică; preferați canalul @vinnytskaODA pentru viteză.  
  *Atenție:* Domeniu preluat din Wikipedia, neverificat (non-gov.ua); poate fi învechit. Verificare: Domeniul e neconfirmat: datele mxmap au câmpul gol pentru Mohyliv-Podilskyi. Pentru brifingurile RVA folosește vin.gov.ua, care e deja în catalog.
- ~ **[Odesa OVA – site oficial (oda.od.gov.ua)](<https://oda.od.gov.ua>)** · web · liber · ore · ★★☆☆☆  
  Site-ul administrației militare regionale Odesa (complementar canalului Telegram @odeskaODA deja listat): comunicate, decizii, informări.  
  *Integrare:* Verificare periodică / Google News site:oda.od.gov.ua; arhivare comunicate pentru analiza post-incident.  
  *Atenție:* Mai lent decât Telegram-ul OVA; feed neconfirmat. Verificare: Site-ul oficial al Odesa OVA este cunoscut, dar nu am confirmat independent activitatea curentă. Telegramul @odeskaODA e deja în catalog și e mai rapid.
- ~ **[Podilsk RVA/RDA – site oficial](<https://podilsk-rda.od.gov.ua>)** · web · liber · ore · ★★☆☆☆  
  Raionul Podilsk (nordul regiunii Odesa, la granița cu Transnistria/MD). Site-ul administrației: comunicate, avertizări, consecințe ale atacurilor.  
  *Integrare:* Verificare periodică (WordPress → încercați /feed/; neconfirmat) sau Google News site:podilsk-rda.od.gov.ua; folosit pentru confirmare post-incident.  
  *Atenție:* Site-ul nu a putut fi accesat din sandbox; actualizări rare/lente; informația rapidă apare pe Telegram-ul OVA/RVA (handle RVA neconfirmat). Verificare: Domeniul lipsește din datele mxmap (câmp gol). Singura dovadă sunt fișiere încărcate în 2023, citate de agentul anterior. Neconfirmat.
- ~ **[Raionul Odesa RVA/RDA – site oficial](<https://odrda.od.gov.ua>)** · web · liber · ore · ★★☆☆☆  
  Raionul Odesa (în jurul orașului, inclusiv Ovidiopol/Chornomorsk). Site-ul administrației: comunicate, avertizări, consecințe ale atacurilor.  
  *Integrare:* Verificare periodică (WordPress → încercați /feed/; neconfirmat) sau Google News site:odrda.od.gov.ua; folosit pentru confirmare post-incident.  
  *Atenție:* Site-ul nu a putut fi accesat din sandbox; actualizări rare/lente; informația rapidă apare pe Telegram-ul OVA/RVA (handle RVA neconfirmat). Verificare: Domeniul există. Agentul anterior a citat un document din 2026/06, dar nu l-am confirmat independent.
- ~ **[Rozdilna RVA/RDA – site oficial](<https://rozdilna-rda.od.gov.ua>)** · web · liber · ore · ★★☆☆☆  
  Raionul Rozdilna, la granița cu Transnistria (nod feroviar). Site-ul administrației: comunicate, avertizări, consecințe ale atacurilor.  
  *Integrare:* Verificare periodică (WordPress → încercați /feed/; neconfirmat) sau Google News site:rozdilna-rda.od.gov.ua; folosit pentru confirmare post-incident.  
  *Atenție:* Site-ul nu a putut fi accesat din sandbox; actualizări rare/lente; informația rapidă apare pe Telegram-ul OVA/RVA (handle RVA neconfirmat). Verificare: Domeniul există în date derivate din Wikipedia. Activitatea nu e confirmată.
- ~ **[Suspilne Mîkolaiv – canal Telegram (@suspilnemykolaiv)](<https://t.me/suspilnemykolaiv>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/suspilnemykolaiv>  
  Știri locale publice Mîkolaiv (drone dinspre mare spre vest).  
  *Integrare:* Citire t.me/s; ponderare mică; doar context amonte.  
  *Atenție:* Relevanță indirectă pentru Iași. Verificare: Handle-ul e confirmat doar de liste din 2022–2023. Activitatea curentă nu e confirmată. Relevanța pentru Iași e mică.
- ~ **[Texty.org.ua – jurnalism de date despre Shahed și alerte](<https://texty.org.ua/tag/shakhedy/>)** · web · liber · zile · ★★☆☆☆  
  Analize de date: rutele Shahed/rachetelor (ex. „Небезпеки з Криму: якими маршрутами летіли шахеди і ракети”), schimbarea alertelor la nivel de raion (dec. 2025), canale Telegram cu practici dubioase.  
  *Integrare:* Lectură analitică pentru calibrarea modelului de rute spre Dunăre/Moldova.  
  *Atenție:* Analiză post-factum, nu flux operativ. Verificare: Texty e activ și scrie despre Shahed. Schema /tag/ e confirmată, dar pagina /tag/shakhedy/ nu a fost văzută direct. Fără RSS confirmat; util pentru analiza post-incident.
- ✔ **[HUR – Direcția de Informații a MApN UA (@DIUkraine)](<https://t.me/DIUkraine>)** · Telegram · liber · zile · ★☆☆☆☆ · flux: <https://t.me/s/DIUkraine>  
  Canal oficial HUR: dezvăluiri despre Shahed/Geran (componente, modificări, producție) – context tehnic.  
  *Integrare:* Citire periodică; adnotarea fișelor tehnice ale dronelor din veghe.  
  *Atenție:* Sursă de parte în conflict; nu e sursă de avertizare.
- ~ **[Berezivka RVA/RDA – site oficial](<https://berezivka-rda.od.gov.ua>)** · web · liber · ore · ★☆☆☆☆  
  Raionul Berezivka (nord-estul regiunii Odesa), pe ruta dronelor dinspre est. Site-ul administrației: comunicate, avertizări, consecințe ale atacurilor.  
  *Integrare:* Verificare periodică (WordPress → încercați /feed/; neconfirmat) sau Google News site:berezivka-rda.od.gov.ua; folosit pentru confirmare post-incident.  
  *Atenție:* Site-ul nu a putut fi accesat din sandbox; actualizări rare/lente; informația rapidă apare pe Telegram-ul OVA/RVA (handle RVA neconfirmat). Verificare: Domeniul există în date derivate din Wikipedia. Activitatea nu e confirmată.
- ~ **[war.ukraine.ua – portalul oficial de război al Ucrainei](<https://war.ukraine.ua>)** · web · liber · zile · ★☆☆☆☆  
  Portal guvernamental (Mintsyfra/MAE) cu informații generale despre război, adresat publicului internațional.  
  *Integrare:* Doar context/referință în rapoarte; fără utilitate operativă.  
  *Atenție:* Perspectivă guvernamentală UA; actualizare rară. Verificare: Portal informativ/advocacy oficial, nu flux de alertă. Relevanță 1.

## Republica Moldova

- ~ **[Poliția de Frontieră RM – canal Telegram oficial (@politiadefrontierarm)](<https://t.me/politiadefrontiera>)** · Telegram · liber · minute · ★★★★★ · flux: <https://t.me/s/politiadefrontiera>  
  Canalul oficial IGPF: „Informare!” despre drone care traversează segmentul de frontieră (ex. Palanca; Colibași→Vadul lui Isac→România), fragmente găsite lângă graniță.  
  *Integrare:* Poll t.me/s/politiadefrontierarm la 1 min; extrage toponime (Palanca, Giurgiulești, Ocnița, Briceni, Ungheni, Sculeni, Cahul) → geocodare → alertă internă.  
  *Atenție:* Există și canalul vechi @politiadefrontiera (verificați care e activ). Informarea urmează detecției radar MApN; nu e avertizare timpurie garantată. Verificare: Handle-ul „politiadefrontierarm” nu a fost găsit nicăieri; cel listat pentru PF RM e @politiadefrontiera. Neconfirmat direct (t.me blocat). Nu-l confundați cu Poliția de Frontieră Română.
- ~ **[Aeroportul Internațional Chișinău – Online Panel (tabela oficială)](<https://airport.md/passenger/online-panel>)** · web · liber · timp real · ★★★★☆  
  Tabela oficială sosiri/plecări cu statusuri; devieri (ex. spre Bacău) și întârzieri apar când spațiul aerian e restricționat din cauza dronelor.  
  *Integrare:* Scraping la 2–5 min (și mobile.airport.md/mobile-online-table-ro); alertă la devieri/întârzieri în rafală, corelate cu NOTAM AAC.  
  *Atenție:* Semnal indirect (meteo/tehnic produc același efect); respectați termenii site-ului. Verificare: Site oficial al aeroportului (OSM: website=airport.md; aeroportul se numește acum „Eugen Doga”). Panoul nu a putut fi deschis – neverificat independent (WebSearch epuizat, fetch blocat). Se suprapune cu intrarea Kayak din catalog; o poate înlocui ca sursă oficială.
- ~ **[MAI RM – secțiunea Știri („MAI informează”)](<https://mai.gov.md/ro/news>)** · web · liber · ore · ★★★★☆  
  Știrile MAI (distincte de Sinteza PDF din catalog): închideri temporare ale spațiului aerian, apeluri către populație, coordonare IGP/IGSU/IGPF.  
  *Integrare:* Scraping /ro/news la 10–15 min; filtre „spațiul aerian”, „dronă”; MAI menționează și canale Telegram proprii (MAI, IGPF, IGSU) – de adăugat după verificarea linkurilor din subsol.  
  *Atenție:* Handle-ul Telegram MAI nu e confirmat (link doar în subsolul site-ului); RSS neconfirmat. Verificare: Secțiune distinctă de „Sinteza evenimentelor” (mai.gov.md, deja în catalog), deci nu e duplicat. Neverificată în sesiune.
- ~ **[Poliția de Frontieră RM – comunicate „Informare!” + raportul zilnic „Situația la frontieră în 24 ore”](<https://border.gov.md/en/comunicate-de-presa>)** · web · liber · ore · ★★★★☆  
  Comunicate oficiale IGPF: survolări neautorizate de drone, fragmente (Etulia, Lencăuți, Cotiujeni/Briceni), plus bilanțul zilnic al frontierei.  
  *Integrare:* Scraping listă comunicate (Drupal) la 10 min; reguli pe titluri „Informare”, „dronă”, „survolarea”; arhivare pentru analiză post-incident.  
  *Atenție:* RSS neconfirmat (feed neconfirmat); etichete de dată uneori inconsistente; publicare după fapt. Verificare: Site-ul border.gov.md există, iar articolele „Informare” și „Situația la frontieră” apar în dovezi. URL-ul listei /en/comunicate-de-presa e neconfirmat; nu a fost verificat în sesiune.
- ~ **[Prima Sursă / Первоисточник – canalul Telegram oficial al Guvernului RM](<https://t.me/prima_sursa_md>)** · Telegram · liber · minute · ★★★★☆ · flux: <https://t.me/s/prima_sursa_md>  
  Canalul oficial de informare/verificare al Guvernului RM; anunță survolări de drone și restricționarea/redeschiderea spațiului aerian (ex. Shahed peste Dubăsari/Orhei, 30.03.2026).  
  *Integrare:* Preluare t.me/s/prima_sursa_md (sau RSSHub /telegram/channel) la 1–2 min; filtre: „dronă”, „spațiul aerian”, „Shahed”, „restricționat/redeschis”.  
  *Atenție:* Bilingv RO/RU; mesajele vin după confirmarea MApN (întârziere de minute). Handle confirmat de customs.gov.md și TGStat, nu direct pe gov.md. Verificare: Handle confirmat (Prima Sursă / Первоисточник), dar activitatea curentă nu a putut fi verificată (t.me blocat). Reconfirmați înainte de integrare.
- ✔ **[Europa Liberă Moldova (moldova.europalibera.org)](<https://www.europalibera.md>)** · web · liber · ore · ★★★☆☆  
  Serviciul moldovenesc RFE/RL (activ în 2026): reportaje despre survolări, închideri ale spațiului aerian, explozii (ex. Talmaza).  
  *Integrare:* RFE/RL publică RSS pe căi /api/... – căutați link rel=alternate în sursa paginii (feed neconfirmat); harta Europa Liberă e deja în catalog.  
  *Atenție:* Nu confundați cu serviciul România (închis 31.03.2026).
- ✔ **[Moldova 1 (TRM) – flux general de știri](<https://moldova1.md>)** · web · liber · ore · ★★★☆☆  
  Televiziunea publică; relatări detaliate (traiectorii, fragmente în mai multe raioane, incendii).  
  *Integrare:* Scraping /p/<id> (ID-uri incrementale) la 10 min; RSS neconfirmat.  
  *Atenție:* Un articol Moldova1 e deja în catalog; aici fluxul general.
- ✔ **[NewsMaker – canal Telegram @newsmakerlive](<https://t.me/newsmakerlive>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/newsmakerlive>  
  Fluxul Telegram al NewsMaker.md (site deja în catalog) – breaking news RM/regiune.  
  *Integrare:* t.me/s/newsmakerlive; filtre RU „дрон”, „воздушное пространство”.  
  *Atenție:* Site-ul newsmaker.md e deja în catalog; aici doar fluxul Telegram distinct.
- ✔ **[Pro TV Chișinău (protv.md)](<https://protv.md>)** · web · liber · ore · ★★★☆☆  
  Știrile PRO TV Chișinău; relatări despre traversări (ex. Vinnîțea → r. Camenca).  
  *Integrare:* Scraping /actualitate/ cu filtre; RSS neconfirmat.  
  *Atenție:* Media.
- ✔ **[Radio Chișinău (radiochisinau.md)](<https://radiochisinau.md>)** · web · liber · ore · ★★★☆☆  
  Post public al Radio România pentru RM; preia ora exactă a restricțiilor (ex. nord 16:46, centru 16:52 pe 31.10.2026).  
  *Integrare:* Scraping + pagini de căutare (/cautare/<termen>); RSS neconfirmat.  
  *Atenție:* Media.
- ✔ **[TV8 – canal Telegram @tv8md](<https://t.me/tv8md>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/tv8md>  
  Fluxul Telegram al TV8.md (breaking news în română).  
  *Integrare:* t.me/s/tv8md; filtre „dronă”, „spațiul aerian”.  
  *Atenție:* Site-ul TV8 e deja în grupul de presă din catalog; aici doar fluxul Telegram.
- ~ **[Biroul Politici de Reintegrare (BPR) – comunicate](<https://gov.md/ro/categorii-noutati/comunicate-de-presa-bpr>)** · web · liber · ore · ★★★☆☆  
  Poziția oficială a Chișinăului privind presupuse atacuri cu drone în regiunea transnistreană (confirmă/infirmă afirmațiile Tiraspolului).  
  *Integrare:* Scraping listă (paginare ?page=N); corelare cu sursele transnistrene pentru verificare.  
  *Atenție:* Chișinăul nu are acces în stânga Nistrului; reacții la ore distanță. Verificare: URL-ul listei e dedus din structura articolelor (gov.md/ro/comunicate-de-presa-bpr/...). Relevanță scăzută (Transnistria). Neverificat în sesiune.
- ~ **[Briceni/Бричаны (@PlaiulBriceni) – canal local](<https://t.me/PlaiulBriceni>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/PlaiulBriceni>  
  Canal local pentru raionul Briceni (frontiera de nord, unde au căzut fragmente Geran la Cotiujeni).  
  *Integrare:* t.me/s/PlaiulBriceni; semnal de martor pentru nord.  
  *Atenție:* Neoficial; verificați cu IGPF/MApN. Verificare: Handle-ul e citat doar prin TGStat și lipsește din lista de confirmări a generatorului, deci dovada e slabă. Sursă comunitară, cu credibilitate neverificată. Neverificat independent (WebSearch epuizat, t.me blocat).
- ~ **[Diez.md – canal Telegram @stiridiez](<https://t.me/stiridiez>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/stiridiez>  
  „Știri de ultimă oră diez.md” – breaking news în română.  
  *Integrare:* t.me/s/stiridiez; filtre RO.  
  *Atenție:* Media; verificați cu sursele oficiale. Verificare: @stiridiez e citat doar prin TGStat. Neverificat independent (WebSearch epuizat, t.me blocat). Diez.md nu apare în catalog.
- ~ **[Flightradar24 – pagina aeroportului Chișinău (RMO/LUKK)](<https://www.flightradar24.com/data/airports/rmo>)** · web · liber · timp real · ★★★☆☆  
  Tablă live, statistici de întârzieri/anulări și avioane în așteptare pentru Chișinău.  
  *Integrare:* Consultare manuală în timpul unei alerte (API-ul FR24 e deja în catalog).  
  *Atenție:* Scraping interzis de ToS; doar uz intern/manual. Verificare: Format standard de pagină de aeroport FR24 (cod RMO). Neverificat independent (WebSearch epuizat, fetch blocat). Doar vizualizare manuală: termenii FR24 interzic scraping-ul, iar API-ul FR24 e deja în catalog. Se suprapune cu #71 și cu Kayak.
- ~ **[Guvernul RM – comunicate de presă și brifinguri](<https://gov.md/ro/categorii-noutati/comunicate-de-presa>)** · web · liber · ore · ★★★☆☆  
  Comunicatele Guvernului și declarațiile purtătorului de cuvânt (ex. traseul dronelor ieșite pe la Taraclia, măsuri de apărare antiaeriană).  
  *Integrare:* Scraping cu paginare (?page=N) la 15 min; filtre pe cuvinte-cheie.  
  *Atenție:* RSS neconfirmat; volum mare de subiecte nerelevante. Verificare: Pagina oficială a Guvernului RM. Utilă pentru confirmări după incident. Neverificată în sesiune.
- ~ **[IGSU RM – comunicate de presă (igsu.gov.md)](<https://igsu.gov.md/ro/comunicate-de-presa>)** · web · liber · ore · ★★★☆☆  
  Intervenții ale salvatorilor/pompierilor RM (incendii de vegetație după căderi de drone, pirotehnicieni), Centrul Operativ de Dispecerat 24/7.  
  *Integrare:* Scraping listă comunicate; corelare geografică cu traseele raportate de MApN/IGPF pentru confirmare post-impact.  
  *Atenție:* A nu se confunda cu IGSU România (igsu.ro). Fără RSS confirmat; Telegram IGSU RM menționat de MAI, handle neconfirmat. Verificare: IGSU al R. Moldova, distinct de IGSU România din catalog. Domeniul apare în listele de domenii gov.md. URL-ul secțiunii nu a fost verificat în sesiune.
- ~ **[Jurnal TV / jurnal.md – canal Telegram @jurnal_tv + site](<https://www.jurnal.md>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/jurnal_tv>  
  Televiziune și portal de știri; relatează survolări și restricții de zbor în nord/centru.  
  *Integrare:* t.me/s/jurnal_tv + scraping jurnal.md/ro/news.  
  *Atenție:* Handle confirmat de telegramadsarchive (terț); RSS neconfirmat. Verificare: Site-ul jurnal.md e confirmat activ (articole din 30.09 și 31.10.2026), iar canalul YouTube Jurnal TV era activ pe 02.11.2026. Handle-ul jurnal_tv e citat însă doar prin telegramadsarchive, deci rămâne neverificat.
- ~ **[MAEIE RM – comunicate (condamnări, convocări, note de protest)](<https://mfa.gov.md>)** · web · liber · ore · ★★★☆☆  
  Reacția diplomatică oficială după survolări: condamnări, convocarea ambasadorului rus, note de protest – confirmare oficială a incidentelor.  
  *Integrare:* Scraping pagini /ro/content/ cu filtre „spațiul aerian”, „dronă”; folosit pentru etichetarea „confirmat oficial” în baza de incidente.  
  *Atenție:* Publicare la ore după incident; RSS neconfirmat. Verificare: Site oficial MAEIE. Comunicatele vin după incident (confirmare diplomatică). Neverificat în sesiune.
- ~ **[Moldelectrica – „Starea sistemului energetic al RM” + știri](<https://moldelectrica.md/ro/activity/system_state>)** · web · liber · minute · ★★★☆☆ · flux: <https://moldelectrica.md/utils/archive2.php?id=table&type=array>  
  Operatorul de transport energie: starea SEN; deconectări ale liniilor de interconexiune imediat după lovituri în Odesa/sudul Ucrainei (ex. 24.03.2026) – indicator indirect de atac în curs.  
  *Integrare:* Scraping pagină stare + știri la 5 min; alertă când apar deconectări/„ajutor de avarie” corelate cu alertele aeriene din Odesa.  
  *Atenție:* Semnal indirect; deconectările pot avea cauze meteo/tehnice. Verificare: Endpoint-ul de date de sistem e folosit de parserul Electricity Maps. Bun ca proxy pentru avariile de rețea după atacuri. Pagina system_state nu a fost confirmată în sesiune.
- ~ **[Noi.md](<https://noi.md>)** · web · liber · minute · ★★★☆☆  
  Portal rom/rus cu actualizări rapide de tip „UPDATE // Drona a părăsit spațiul aerian”.  
  *Integrare:* Scraping secțiunea societate (/md/societate) la 5 min; RSS neconfirmat.  
  *Atenție:* Media; verificați cu MApN. Verificare: Noi.md există (articole despre drone), dar data lor e neconfirmată. Neverificat independent (WebSearch epuizat, fetch blocat).
- ~ **[Point.md – canal Telegram @PointNews + site](<https://t.me/PointNews>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/PointNews>  
  Cel mai mare portal de știri din RM (Simpals), rus/rom; relatează rapid survolări și închideri ale spațiului aerian.  
  *Integrare:* t.me/s/PointNews la 1–2 min; site point.md/ru/novosti pentru detalii.  
  *Atenție:* Media, nu sursă oficială; RSS neconfirmat. Verificare: Point.md există (articol despre dronă), dar @PointNews e confirmat doar prin TGStat. Neverificat independent (WebSearch epuizat, t.me blocat). E un canal distinct de site, nu un duplicat.
- ~ **[Poliția RM (IGP) – „Poliția în acțiune”](<https://politia.md/ro/politia-actiune>)** · web · liber · ore · ★★★☆☆  
  Comunicatele IGP: perimetre securizate la căderi de drone, identificarea tipului (ex. primul „Gerbera” în r. Florești), neutralizarea focoaselor.  
  *Integrare:* Scraping secțiune + filtre („dronă”, „беспилотник”, „fragmente”, „pirotehnicieni”); util pentru confirmare și tipologie.  
  *Atenție:* Mult zgomot (comunicate infracționale); poliția postează și pe Telegram, handle neconfirmat. Verificare: Site oficial IGP. Utilă pentru confirmarea dronelor căzute (ex. Gerbera la Florești, sept. 2026). Neverificată în sesiune.
- ~ **[Realitatea.md – canal Telegram @realitateamd](<https://t.me/realitateamd>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/realitateamd>  
  Fluxul Telegram al Realitatea.md (știri locale rapide).  
  *Integrare:* t.me/s/realitateamd; filtre pe cuvinte-cheie.  
  *Atenție:* Site-ul Realitatea.md e deja în catalog; handle văzut doar într-o postare citată (t.me/realitateamd/97256). Verificare: Cea mai slabă dovadă din set: un singur link de postare citat în TGStat, fără pagina canalului. Site-ul realitatea.md e activ în 2026. Neverificat independent (WebSearch epuizat, t.me blocat).
- ~ **[SP / esp.md (Bălți)](<https://esp.md>)** · web · liber · ore · ★★★☆☆  
  Ziarul „СП” din Bălți – acoperire detaliată a nordului (drone peste Bălți, Soroca/Edineț; fragmente lângă Briceni; „Gerbera” în Florești).  
  *Integrare:* Scraping /ru/sobytiya/ cu filtre RU; RSS neconfirmat.  
  *Atenție:* Media regională, rusă. Verificare: Ziarul SP din Bălți (esp.md, RU/RO). Articolele citate (12.09.2026, 13.05.2026) nu au fost verificate independent (host blocat).
- ~ **[TVR Moldova (tvrmoldova.md)](<https://tvrmoldova.md>)** · web · liber · ore · ★★★☆☆  
  Televiziunea publică română pentru RM; urmărește constant survolările (Țibirica, Pepeni/Sângerei, Palanca, Hârbovăț).  
  *Integrare:* Scraping /article/ cu filtre; RSS neconfirmat.  
  *Atenție:* Media; detaliile inițiale pot fi corectate ulterior (ex. punct de intrare). Verificare: TVR Moldova există (articole despre drone pe tvrmoldova.md), dar data lor e neconfirmată. Canalul YouTube TVR MOLDOVA era activ pe 02.11.2026. Site-ul nu a putut fi deschis.
- ~ **[Ungheni – Consiliul Raional (crungheni.md) și Primăria (primaria.ungheni.md)](<https://primaria.ungheni.md>)** · web · liber · ore · ★★★☆☆  
  Ungheni e vizavi de județul Iași: un Shahed a ieșit din RM pe la Zagarancea spre Golăiești (Iași). Autoritățile locale pot confirma observări/fragmente.  
  *Integrare:* Monitorizare știri ambele site-uri; contacte pentru verificare rapidă pe malul stâng al Prutului.  
  *Atenție:* Domeniul crungheni.md provine din anunț de achiziții 2024; RSS neconfirmat. Verificare: Dovezile citate nu conțin domeniul primaria.ungheni.md (nici crungheni.md), ci doar particip, Interreg și Economedia. Neverificat independent (WebSearch epuizat, fetch blocat). URL-ul trebuie confirmat.
- ~ **[Бельцы Онлайн (@balti_online) – canal local Bălți](<https://t.me/balti_online>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/balti_online>  
  Canal local cu știri și raportări de la martori din Bălți și nord.  
  *Integrare:* t.me/s/balti_online la 2 min; folosiți doar ca semnal „martor” de confirmat.  
  *Atenție:* Neoficial, în rusă; risc de zvonuri. Verificare: Handle-ul e citat doar prin TGStat. Sursă comunitară, cu credibilitate neverificată. Neverificat independent (WebSearch epuizat, t.me blocat).
- ✔ **[Deschide.md](<https://www.deschide.md>)** · web · liber · ore · ★★☆☆☆  
  Portal de știri în română; preia rapid survolările semnalate oficial.  
  *Integrare:* Scraping cu filtre; RSS neconfirmat.  
  *Atenție:* Media; preluări.
- ✔ **[Știri.md](<https://stiri.md>)** · web · liber · ore · ★★☆☆☆  
  Agregator/portal Simpals în română; confirmări „dronă Shahed detectată”.  
  *Integrare:* Scraping /article/social; RSS neconfirmat.  
  *Atenție:* Media; agregator.
- ~ **[Agora.md](<https://agora.md>)** · web · liber · ore · ★★☆☆☆  
  Platformă independentă de știri din Chișinău (din 2009).  
  *Integrare:* Scraping cu filtre; feed neconfirmat (eurotopics listează un link RSS).  
  *Atenție:* Media. Verificare: Portal real, dar evidența e veche (eurotopics, KAS 2022). Activitatea curentă e neconfirmată (host blocat). Relevanță mică.
- ~ **[Centrul pentru Comunicare Strategică și Combatere a Dezinformării (StratCom)](<https://stratcom.md>)** · API · liber · ore · ★★☆☆☆  
  Autoritatea care demontează falsuri (inclusiv despre drone/sirene) și publică rapoarte de dezinformare.  
  *Integrare:* Site WordPress cu REST API (wp-json/wp/v2 – posts); util pentru marcarea zvonurilor false în fluxul de alerte.  
  *Atenție:* Nu e sursă de alertare; /feed RSS neconfirmat. Verificare: Site WordPress, activ în 2026 după PDF-ul planului. Endpoint-ul /wp-json/wp/v2/posts e neconfirmat. Relevanță scăzută (dezinformare).
- ~ **[Consiliul Raional Briceni (briceni.md)](<https://briceni.md>)** · web · liber · ore · ★★☆☆☆  
  Site oficial al raionului de frontieră din nord (vecin cu reg. Cernăuți/Vinnîțea); anunțuri locale, comisii de situații excepționale.  
  *Integrare:* Site WordPress – /feed/ probabil (feed neconfirmat); monitorizare la 30 min cu filtre „dronă/fragmente”.  
  *Atenție:* Publică rar despre incidente; mai util pentru contacte și măsuri post-incident. Verificare: briceni.md are PDF-uri din 2024. Activitatea curentă și existența unui canal de alertă nu sunt confirmate. Neverificat independent (WebSearch epuizat, fetch blocat).
- ~ **[Consiliul Raional Cahul (cahul.md)](<https://cahul.md>)** · web · liber · ore · ★★☆☆☆  
  Raion sudic pe Prut (vizavi de Galați); Shahed-uri au trecut pe la Colibași spre România.  
  *Integrare:* Pagini de decizii și știri; versiunea veche la old.cahul.md.  
  *Atenție:* Conținut administrativ; RSS neconfirmat. Verificare: Pagina cahul.md/en/decisions e citată, dar nu a putut fi deschisă. Neverificat independent (WebSearch epuizat, fetch blocat).
- ~ **[Consiliul Raional Căușeni (causeni.md)](<https://causeni.md>)** · web · liber · ore · ★★☆☆☆  
  Raion sud-estic lângă zona de securitate/Transnistria și reg. Odesa; site oficial CR.  
  *Integrare:* WordPress – /feed/ probabil (feed neconfirmat).  
  *Atenție:* Conținut administrativ; utilitate mai ales post-incident. Verificare: Procesul-verbal din 03.2026 de pe causeni.md indică un site activ. Neverificat independent (WebSearch epuizat, fetch blocat).
- ~ **[Consiliul Raional Florești (floresti.md)](<https://floresti.md>)** · web · liber · ore · ★★☆☆☆  
  Raion cu căderi repetate de drone (dronă pe acoperiș la Cuhurești, „Gerbera” în 2026); site oficial al CR.  
  *Integrare:* WordPress – /feed/ probabil (feed neconfirmat); filtre pe „dronă”.  
  *Atenție:* Publică mai ales documente administrative. Verificare: Calea de upload 2026/09 sugerează un site activ. Neverificat independent (WebSearch epuizat, fetch blocat).
- ~ **[Căușeni.Info (@Causeninfo) – canal local](<https://t.me/Causeninfo>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/Causeninfo>  
  Știri locale din raionul Căușeni (sud-est).  
  *Integrare:* t.me/s/Causeninfo; semnal de martor pentru sud-est.  
  *Atenție:* Neoficial; verificați. Verificare: Handle-ul e citat doar prin TGStat și lipsește din lista de confirmări a generatorului, deci dovada e slabă. Sursă comunitară, cu credibilitate neverificată. Neverificat independent (WebSearch epuizat, t.me blocat).
- ~ **[Epoca Edineț (@EpocaEdinet) – canal local](<https://t.me/EpocaEdinet>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/EpocaEdinet>  
  Știri locale Edineț (incidente, evenimente).  
  *Integrare:* t.me/s/EpocaEdinet; filtre pe cuvinte-cheie.  
  *Atenție:* Neoficial; volum mic. Verificare: Handle-ul e citat doar prin TGStat și lipsește din lista de confirmări a generatorului, deci dovada e slabă. Sursă comunitară, cu credibilitate neverificată. Neverificat independent (WebSearch epuizat, t.me blocat).
- ~ **[Logos Press (logos-pres.md)](<https://logos-pres.md>)** · web · liber · ore · ★★☆☆☆  
  Publicație economică/politică; a semnalat întârzieri de zboruri la Chișinău din cauza dronelor și explozia din r. Dondușeni.  
  *Integrare:* WordPress – /feed/ probabil (feed neconfirmat).  
  *Atenție:* Media. Verificare: Publicație reală (Logos Press). Nu am putut deschide site-ul (proxy 403), iar bugetul de căutare era epuizat. Activitatea curentă e neconfirmată independent.
- ~ **[Ministerul Infrastructurii și Dezvoltării Regionale (MIDR) – noutăți](<https://midr.gov.md/noutati>)** · web · liber · ore · ★★☆☆☆  
  Ministerul de resort al AAC/MoldATSA; anunțuri privind regimul spațiului aerian civil.  
  *Integrare:* Monitorizare cu filtre „spațiul aerian”; context pentru NOTAM-uri.  
  *Atenție:* Rar relevant; nu e sursă operativă. Verificare: Singura dovadă e un articol din 2022 (stare de urgență). Relevanță scăzută; sursa operațională e AAC (caa.md, deja în catalog). Neverificat în sesiune.
- ~ **[Misiunea RM la OSCE (Viena) – declarații privind încălcarea spațiului aerian](<https://austria.mfa.gov.md>)** · web · liber · zile · ★★☆☆☆  
  Declarații la OSCE care enumeră date și traiectorii (ex. 8, 12, 14 sept. 2026; Shahed-136 la Copanca, 13.07.2026) – cronologie oficială utilă.  
  *Integrare:* Extragere manuală/semiautomată a datelor din declarații pentru validarea bazei istorice.  
  *Atenție:* Agregat, cu întârziere de zile; perspectivă diplomatică. Verificare: Subdomeniul misiunii există (listat în date de contact ale ambasadelor). Relevanță 1 (context diplomatic).
- ~ **[Nokta.md (Comrat, Găgăuzia)](<https://nokta.md>)** · web · liber · ore · ★★☆☆☆  
  Publicație independentă rusofonă din Găgăuzia; acoperă căderi de drone (Dondușeni, Telenești – „Gerbera”).  
  *Integrare:* Scraping cu filtre RU; RSS neconfirmat.  
  *Atenție:* Media regională; verificați cu sursele oficiale. Verificare: Portal real din Comrat. Am văzut în sesiune un articol nokta.md despre căderea unei Geran (data nu apare în URL). RSS neconfirmat.
- ~ **[Președinția RM – comunicatele Consiliului Suprem de Securitate](<https://presedinte.md/rom/css-comunicate-de-presa>)** · web · liber · zile · ★★☆☆☆  
  Comunicate CSS și declarații ale Președintei despre survolări (ex. 9 drone într-o săptămână, peste 20 în septembrie) și apărarea antiaeriană.  
  *Integrare:* Monitorizare zilnică; context strategic și cifre agregate.  
  *Atenție:* Nu e sursă operativă; cifre politice agregate. Verificare: Domeniul oficial există. Comunicatele CSS sunt rare; relevanță 1–2. Neverificat în sesiune.
- ~ **[Primăria Edineț (primariaedinet.md)](<https://primariaedinet.md>)** · web · liber · ore · ★★☆☆☆  
  Primăria orașului Edineț (nord, aproape de frontiera cu Ucraina).  
  *Integrare:* WordPress – /feed/ probabil (feed neconfirmat).  
  *Atenție:* Consiliul raional Edineț nu are site confirmat (doar profil particip.gov.md). Verificare: Singura dovadă e un PDF din 2021, deci activitatea actuală nu e confirmată. Neverificat independent (WebSearch epuizat, fetch blocat).
- ~ **[Primăria municipiului Bălți (balti.md)](<https://balti.md>)** · web · liber · ore · ★★☆☆☆  
  Site oficial Bălți (al doilea oraș, nord); drone observate peste Bălți (13.05.2026).  
  *Integrare:* WordPress – /feed/ probabil (feed neconfirmat).  
  *Atenție:* Comunicatele despre incidente vin mai ales de la MApN, nu de la primărie. Verificare: Dispozițiile primarului din 2025–2026 de pe balti.md indică un site activ. Neverificat independent (WebSearch epuizat, fetch blocat).
- ~ **[Primăria Ștefan Vodă (primariastefanvoda.md)](<https://www.primariastefanvoda.md>)** · web · liber · ore · ★★☆☆☆  
  Primăria orașului Ștefan Vodă (sud-est, la granița cu reg. Odesa; căderi de drone și rachetă Banderol în 2026).  
  *Integrare:* Monitorizare știri locale; CR Ștefan Vodă are doar profil pe particip.gov.md.  
  *Atenție:* Este primăria orașului, nu consiliul raional. Verificare: Singura dovadă e un fișier fără dată vizibilă. Neverificat independent (WebSearch epuizat, fetch blocat).
- ~ **[Serviciul 112 RM + aplicația oficială 112MD](<https://112.md>)** · aplicație · liber · minute · ★★☆☆☆  
  Serviciul național unic de urgență; aplicația 112MD (lansată în martie 2026, app.112.md). Autoritățile cer raportarea dronelor/fragmentelor la 112.  
  *Integrare:* Doar referință și canal de raportare; statisticile lunare de apeluri pot fi folosite post-incident.  
  *Atenție:* Nu există API/feed public de incidente. Verificare: Serviciul 112 RM există, dar aplicația 112MD nu a fost confirmată în sesiune. Nu e un flux de alertă publică.
- ~ **[Soroca – Consiliul Raional (soroca.md) și Primăria (primsoroca.md)](<https://soroca.md>)** · web · liber · ore · ★★☆☆☆  
  Autoritățile raionului Soroca (pe Nistru, la granița cu reg. Vinnîțea); drone au survolat Soroca/Edineț în 2026.  
  *Integrare:* Monitorizare pagini de știri; listă de contacte pentru verificare locală.  
  *Atenție:* Domeniul soroca.md confirmat din anunțuri de achiziții; RSS neconfirmat. Verificare: Dovezile arată primsoroca.md, dar nu direct domeniul soroca.md (doar achizitii.md și particip). Neverificat independent (WebSearch epuizat, fetch blocat). Domeniul soroca.md trebuie confirmat.
- ~ **[Ziarul de Gardă – canal Telegram @zdgmd](<https://t.me/zdgmd>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/zdgmd>  
  Fluxul Telegram ZdG: știri și investigații, inclusiv preluări ale comunicatelor MApN despre restricții aeriene.  
  *Integrare:* t.me/s/zdgmd; util pentru analize post-incident.  
  *Atenție:* Site-ul ZdG e deja în catalog; aici doar fluxul Telegram. Verificare: Site-ul zdg.md e confirmat activ pe 31.10.2026, dar @zdgmd e citat doar prin TGStat și telegramadsarchive. Neverificat independent (WebSearch epuizat, t.me blocat). Feed distinct de site, nu un duplicat.
- ~ **[Кишинёв в теме (@vtememd) – canal Chișinău](<https://t.me/vtememd>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/vtememd>  
  Canal rusofon de știri din Chișinău care republică rapid surse (Moldova 1 etc.).  
  *Integrare:* t.me/s/vtememd; doar ca agregator secundar.  
  *Atenție:* Neoficial; republicări fără verificare. Verificare: Handle-ul e citat doar prin TGStat. Sursă comunitară, cu credibilitate neverificată. Neverificat independent (WebSearch epuizat, t.me blocat).
- ~ **[Новости Приднестровья (novostipmr.com + @novostipmrcom)](<https://t.me/novostipmrcom>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/novostipmrcom>  
  Agenția oficială a administrației de la Tiraspol; anunță primele presupuse atacuri cu drone în regiune.  
  *Integrare:* t.me/s/novostipmrcom doar ca semnal de context pentru stânga Nistrului; verificare obligatorie prin BPR/MAI.  
  *Atenție:* Sursă afiliată regimului separatist – context, credibilitate scăzută / propagandă; incidente anterioare declarate false de Chișinău. Verificare: Agenția oficială a regimului de la Tiraspol. De folosit doar ca context, credibilitate scăzută / propagandă. Handle-ul Telegram e neconfirmat independent (t.me blocat; avem doar tgstat).
- ~ **[Свободный Канал.md (@canalmd) – Europa Liberă Moldova în rusă](<https://t.me/canalmd>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/canalmd>  
  Canalul Telegram rusofon al Radio Svoboda Moldova, cu linkuri spre moldova.europalibera.org.  
  *Integrare:* t.me/s/canalmd; acoperă publicul rusofon (Transnistria/Găgăuzia).  
  *Atenție:* Media; nu e sursă de detecție. Verificare: @canalmd e prezentat ca serviciul în rusă al Europei Libere Moldova doar prin TGStat. Neverificat independent (WebSearch epuizat, t.me blocat). Trebuie confirmat din subsolul europalibera.md.
- ~ **[ТСВ Приднестровье (@tsvtiraspol)](<https://t.me/tsvtiraspol>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/tsvtiraspol>  
  Canal TV din Tiraspol cu incidente locale din Transnistria.  
  *Integrare:* t.me/s/tsvtiraspol – context pentru traiectorii peste stânga Nistrului (Bender, Tiraspol, Camenca).  
  *Atenție:* Sursă din regiunea separatistă – context, credibilitate scăzută / propagandă. Verificare: TSV, televiziunea de la Tiraspol. De folosit doar ca context, credibilitate scăzută / propagandă. Handle neconfirmat independent.
- ~ **[Biroul Național de Statistică RM – Recensământul 2024 (RPL)](<https://statistica.gov.md>)** · set de date · liber · istoric · ★☆☆☆☆  
  Populația pe localități din RPL 2024 pentru estimarea expunerii pe traseele dronelor.  
  *Integrare:* Import CSV/XLSX în baza geografică (join pe coduri CUATM).  
  *Atenție:* Date statice; verificați structura fișierelor. Verificare: BNS există, iar RPL 2024 a avut loc în aprilie 2024. Neverificat independent (WebSearch epuizat, fetch blocat). Util doar pentru expunerea populației, nu pentru avertizare.
- ~ **[CIJM / anticoruptie.md](<https://anticoruptie.md>)** · web · liber · zile · ★☆☆☆☆  
  Centrul de Investigații Jurnalistice: știri și investigații, inclusiv despre rachete și drone de-a lungul frontierei.  
  *Integrare:* Monitorizare săptămânală pentru analiză post-incident.  
  *Atenție:* Nu e sursă operativă. Verificare: CIJM e real. Publică investigații, nu știri în timp real, deci relevanța pentru avertizare e mică. Neverificat independent.
- ~ **[Comisia pentru Situații Excepționale (CSE) – dispoziții](<https://old.gov.md/ro/content/dispozitii-cse>)** · PDF · liber · zile · ★☆☆☆☆  
  Dispozițiile CSE (ex. nr. 5/2022 privind utilizarea spațiului aerian) – cadrul pentru închideri/autorizări de zbor.  
  *Integrare:* Arhivare PDF pentru context juridic; fără automatizare în timp real.  
  *Atenție:* Documente juridice; pot fi depășite de legislația 2025–2026 privind doborârea dronelor. Verificare: old.gov.md e un site vechi, iar starea de urgență s-a încheiat. Probabil doar arhivă; relevanță istorică (1).
- ~ **[Comitetul Executiv al UTA Găgăuzia (gagauzia.md)](<https://www.gagauzia.md>)** · web · liber · zile · ★☆☆☆☆  
  Site oficial al executivului autonomiei găgăuze (Comrat).  
  *Integrare:* Monitorizare ocazională pentru incidente în sud.  
  *Atenție:* Poziții politice pro-ruse frecvente; informare limitată despre drone. Verificare: Site oficial al UTA Găgăuzia. Relevanță scăzută pentru Iași. Neverificat din sesiune (host blocat).
- ~ **[date.gov.md – Portalul guvernamental de date deschise (CKAN)](<https://date.gov.md>)** · set de date · liber · istoric · ★☆☆☆☆  
  Seturi de date oficiale RM (localități, instituții, infrastructură) pentru straturi de hartă.  
  *Integrare:* API CKAN standard (/api/3/action/package_search) – de verificat pe instanța actuală.  
  *Atenție:* Documentație API actuală neconfirmată; multe seturi neactualizate. Verificare: Portal de date deschise al R. Moldova. Activitatea curentă neconfirmată – neverificat independent (WebSearch epuizat, fetch blocat). Relevanță mică (context).
- ~ **[KP Moldova (@KpMoldova)](<https://t.me/KpMoldova>)** · Telegram · liber · minute · ★☆☆☆☆ · flux: <https://t.me/s/KpMoldova>  
  Canal neoficial al ziarului KP în Moldova.  
  *Integrare:* Doar monitorizarea narativelor după incidente.  
  *Atenție:* Rețea legată de Rusia – context, credibilitate scăzută / propagandă. Verificare: KP Moldova face parte din rețeaua pro-Kremlin (detector.media). Doar context, credibilitate scăzută / propagandă. Handle neconfirmat independent.
- ~ **[particip.gov.md – profilurile consiliilor raionale (ex. CR Ocnița, Edineț, Fălești, Ștefan Vodă)](<https://particip.gov.md/ro/authorities/883>)** · web · liber · zile · ★☆☆☆☆  
  Registru oficial cu date de contact pentru consiliile raionale fără site propriu (Ocnița, Edineț, Fălești etc.).  
  *Integrare:* Construire listă de contacte/escaladare pentru verificări post-incident.  
  *Atenție:* Contactele pot fi învechite (adrese personale mail.ru). Verificare: particip.gov.md există, dar profilurile raioanelor sunt pagini de consultare publică, nu canale de alertă. Neverificat independent (WebSearch epuizat, fetch blocat). Relevanță foarte mică.
- ~ **[TGStat – catalogul canalelor Telegram „Республика Молдова”](<https://tgstat.com/>)** · web · liber · zile · ★☆☆☆☆  
  Catalog cu canale Telegram moldovenești și statistici (abonați, citări) – pentru descoperirea/validarea canalelor locale.  
  *Integrare:* Consultare manuală la extinderea listei de canale monitorizate.  
  *Atenție:* Director terț; nu confirmă caracterul oficial. Verificare: TGStat e un serviciu rusesc; folosiți-l doar ca index de descoperire. Calea /tag/moldova e neconfirmată. În sesiune apare domeniul tgstat.com.
- ~ **[Wikipedia – Moldova and the Russo-Ukrainian war](<https://en.wikipedia.org/wiki/Moldova_and_the_Russo-Ukrainian_war>)** · web · liber · istoric · ★☆☆☆☆  
  Cronologie a efectelor războiului asupra RM, inclusiv incidente cu drone/rachete (diferită de pagina „Violations…” din catalog).  
  *Integrare:* Extragere periodică pentru verificarea bazei istorice.  
  *Atenție:* Enciclopedie editabilă; verificați sursele primare. Verificare: Titlul exact al articolului e neconfirmat (posibil redirect; Wikipedia blocată din sandbox). Context istoric, distinct de articolul despre încălcările spațiului aerian din catalog.
- ~ **[Блокнот Молдова (@bloknotmd)](<https://t.me/bloknotmd>)** · Telegram · liber · minute · ★☆☆☆☆ · flux: <https://t.me/s/bloknotmd>  
  Canal rusofon de știri din Moldova.  
  *Integrare:* Doar context/monitorizare narative.  
  *Atenție:* Identificat în rețele legate de Rusia – context, credibilitate scăzută / propagandă. Verificare: Bloknot Moldova face parte din rețeaua pro-Kremlin (detector.media). Doar context, credibilitate scăzută / propagandă. Handle neconfirmat independent.
- ~ **[Приднестровец (@pridnestrovec)](<https://t.me/pridnestrovec>)** · Telegram · liber · minute · ★☆☆☆☆ · flux: <https://t.me/s/pridnestrovec>  
  Agregator mare de știri Transnistria/Rusia/Ucraina/Moldova.  
  *Integrare:* Doar context; nu declanșa alerte automate.  
  *Atenție:* Context, credibilitate scăzută / propagandă. Verificare: Evidență minimă (doar tgstat), iar natura canalului e neclară. De folosit doar ca context, credibilitate scăzută / propagandă. Handle neconfirmat independent.

## România

- ~ **[Aeroportul Internațional Iași – tabela sosiri/plecări](<https://aeroport-iasi.ro/>)** · web · liber · minute · ★★★★★  
  Tabela live de zboruri (sosiri/plecări, status, terminal) a LRIA. Suspendarea zborurilor (ex. 8.09.2026, ~16:37–17:41) e un semnal de confirmare a închiderii spațiului aerian.  
  *Integrare:* Polling la 1–2 min al tabelei; alertă când multe zboruri trec simultan în «Anulat/Întârziat/Deviat». Corelare cu ADS-B (zboruri în holding/diversiune).  
  *Atenție:* Fără API oficial; respectați termenii site-ului și o rată mică de cereri. Întârzierile pot avea cauze meteo/tehnice – nu e dovadă de dronă. Verificare: Site oficial al aeroportului Iași (LRIA). Existența și formatul tabelei de zboruri sunt neconfirmate din sesiune (host blocat).
- ~ **[MApN – arhiva comunicatelor (site în română, /cpresa)](<https://www.mapn.ro/cpresa/>)** · web · liber · minute · ★★★★★  
  Arhiva oficială a comunicatelor MApN (numerotate, pe lună/an), inclusiv detectări radar de drone, ridicarea avioanelor F-16/F-18 și RO-Alert (ex. 31.10.2026, două drone în NE).  
  *Integrare:* Polling la 2–5 min pe pagina de arhivă/homepage, extragere titlu+număr comunicat+oră; deduplicare pe ID-ul din URL (ex. /cpresa/19394_). RSS oficial: feed neconfirmat.  
  *Atenție:* Fără RSS confirmat; hostul e blocat din sandbox, testați de pe server. Orele din comunicate pot diferi de cele din presă – păstrați ora oficială. Distinct de english.mapn.ro (deja în catalog). Verificare: Varianta în română a secțiunii de presă MApN, de regulă publicată mai repede. Nu e duplicat: URL-ul diferă de english.mapn.ro/cpresa/356_ din catalog. Calea exactă e neconfirmată (host blocat).
- ✔ **[BotosaniNews.ro](<https://www.botosaninews.ro/>)** · web · liber · minute · ★★★★☆  
  Știri locale Botoșani: RO-Alert, fotografii ale dronei (Corlăteni, Șendriceni, Dorohoi – 12.09.2026), martori care au auzit drona la joasă înălțime.  
  *Integrare:* Polling 5 min pe secțiunea eveniment; extragere localități menționate pentru geolocalizare aproximativă. RSS: feed neconfirmat.  
  *Atenție:* Fotografiile și mărturiile cetățenilor pot fi greșit atribuite; verificați. Nu stocați date personale.
- ✔ **[Radio România Iași – știri regionale](<https://www.radioiasi.ro/stiri/regional/>)** · web · liber · minute · ★★★★☆  
  Radio public regional: primul anunț al redeschiderii aeroportului (17:41, 8.09.2026), mărturii ale ascultătorilor (dronă văzută la Breazu–Lețcani, 31.10.2026), alerte Botoșani.  
  *Integrare:* Polling pe /stiri/regional/ și /stiri/prim-plan/; site WordPress – încercați /feed/ (feed neconfirmat).  
  *Atenție:* Mărturiile ascultătorilor sunt neconfirmate; separați-le de declarațiile oficiale.
- ✔ **[Ziarul de Iași – eticheta «drona»](<https://www.ziaruldeiasi.ro/tag/drona>)** · web · liber · minute · ★★★★☆  
  Pagina de etichetă «drona» a celui mai mare cotidian ieșean: actualizări live la RO-Alert (8.09 și 31.10.2026), F-18 spaniole, urmări locale.  
  *Integrare:* Polling 2–5 min pe pagina de etichetă (listă scurtă, ușor de parsat); RSS: feed neconfirmat.  
  *Atenție:* Articolele se actualizează («UPDATE») – urmăriți modificările, nu doar titlurile noi. Marcați ca presă.
- ~ **[Aeroportul Internațional „Ștefan cel Mare” Suceava – program zboruri](<https://www.aeroportsuceava.ro/en/17-program-zboruri>)** · web · liber · ore · ★★★★☆  
  Programul oficial de zboruri LRSV (Wizz Air, TAROM); spațiul aerian al Sucevei a fost închis ~1 oră din cauza unei drone – anulările/întârzierile confirmă restricțiile.  
  *Integrare:* Comparați programul oficial cu ADS-B (zboruri SCV în holding/deviate) – abaterea în fereastra unei alerte = confirmare a închiderii. Tabela live: neconfirmat.  
  *Atenție:* Pagina oferă program planificat, nu status live confirmat; nu există API. Verificare: Site oficial al aeroportului Suceava (LRSV). Pagina programului de zboruri e neverificată din sesiune.
- ~ **[Instituția Prefectului Județul Iași – comunicate](<https://is.prefectura.mai.gov.ro/>)** · web · liber · ore · ★★★★☆  
  Comunicatele Prefecturii Iași (prefect Constantin Dolachi-Pelin); în incidentul din 8.09.2026 Prefectura a anunțat încetarea alertei (~17:30) și direcția dronei.  
  *Integrare:* Site WordPress pe rețeaua MAI: verificați /feed/ (feed neconfirmat); altfel polling pe /media/presa/ și /category/stiri-importante/.  
  *Atenție:* Declarațiile la cald apar mai întâi în presă (News.ro), site-ul se actualizează cu întârziere. Feed WordPress neconfirmat. Verificare: Subdomeniul prefecturii e plauzibil. Calea /media/presa/ e neconfirmată: același tipar apare la 4 prefecturi, posibil generat.
- ~ **[ISU „Bucovina” Suceava – comunicate de presă](<https://isusv.igsu.ro/comunicate-de-presa>)** · web · liber · ore · ★★★★☆  
  Comunicatele ISU Suceava; la 8.09.2026 ISU Suceava a confirmat că nicio dronă nu a căzut și că a părăsit teritoriul spre R. Moldova (Botoșenița Mare – dronă prăbușită într-un lan, alt incident).  
  *Integrare:* Polling pe isusv.igsu.ro/comunicate-de-presa; cuvinte-cheie dronă/RO-ALERT. RSS: feed neconfirmat.  
  *Atenție:* URL-ul listei e dedus din tiparul platformei IGSU (evidența arată un comunicat individual pe același subdomeniu). Verificare: Slug-ul articolului citat pare autentic (Argel, jud. Suceava). Lista de comunicate e neverificată din sesiune.
- ~ **[ISU „Mihail Sturdza” Iași – comunicate, știri și declarații de presă 2026](<https://isuis.igsu.ro/comunicate-de-presa/stiri-de-presa-2026-175>)** · web · liber · ore · ★★★★☆  
  Site-ul oficial ISU Iași (platforma IGSU): liste numerotate de știri, comunicate, declarații și buletine 2026, inclusiv documentul nr. 123/30.01.2026 «Mesaje Ro-Alert emise de ISU Iași».  
  *Integrare:* Polling la 10–15 min pe paginile de listă 2026 (stiri-de-presa-2026-175, comunicate-de-presa-2026-172, declaratii-de-presa-2026-173); detectare cuvinte-cheie «RO-ALERT», «dronă», «obiect căzut». RSS: feed neconfirmat.  
  *Atenție:* Publicare cu întârziere față de RO-Alert; ID-urile de pagină se schimbă anual (ex. -175 pentru 2026). Vechiul domeniu isujis.ro conține arhivă 2020–2024. Verificare: Subdomeniul ISU Iași pe igsu.ro e plauzibil (formatul CMS e consecvent cu celelalte ISU). Pagina pe 2026 e neverificată din sesiune.
- ~ **[ISU „Podul Înalt” Vaslui – comunicate de presă](<https://isuvs.igsu.ro/comunicate-de-presa>)** · web · liber · ore · ★★★★☆  
  Comunicate ISU Vaslui (județ vecin cu Iași pe direcția de intrare dinspre R. Moldova: Huși, Fălciu); intervenții și bilanțuri, inclusiv la obiecte căzute.  
  *Integrare:* Polling 10–15 min pe lista de comunicate; filtrare pe «dronă», «RO-ALERT», «obiect». RSS: feed neconfirmat.  
  *Atenție:* Fără API; comunicatele despre drone pot apărea doar pe Facebook sau în presă. Site-ul vechi isuvaslui.ro e arhivă. Verificare: Subdomeniul ISU Vaslui e plauzibil. Neverificat din sesiune (host blocat).
- ✔ **[Agerpres – serviciul în limba engleză](<https://agerpres.ro/english/>)** · web · liber · minute · ★★★☆☆  
  Fluxul englez al agenției naționale: știri despre suspendarea zborurilor la Iași după RO-Alert (8.09.2026), RO-Alert după atacuri la Dunăre.  
  *Integrare:* Polling pe /english/; util pentru rezumate în engleză. RSS: feed neconfirmat.  
  *Atenție:* Secțiune distinctă de agerpres.ro (deja în catalog). Drepturi de autor – doar titlu+link.
- ✔ **[Botoșăneanul](<https://www.botosaneanul.ro/>)** · web · liber · minute · ★★★☆☆  
  Cotidian local Botoșani: relatări despre RO-Alert și alarmele aeriene de dimineață din județ.  
  *Integrare:* Polling pe homepage/secțiunea actualitate; RSS: feed neconfirmat.  
  *Atenție:* Presă locală; confirmați cu ISU/MApN.
- ✔ **[DefenseRomania – știri apărare (incursiuni drone, F-16)](<https://www.defenseromania.ro/>)** · web · liber · ore · ★★★☆☆  
  Publicație de specialitate: bilanțuri (35 de pătrunderi și 6 drone doborâte în 2026), detalii despre ridicarea F-16/Eurofighter/F-18 și armamentul folosit.  
  *Integrare:* Polling pe homepage; util pentru analiza post-incident și pentru contextul aeronavelor militare. RSS: feed neconfirmat.  
  *Atenție:* Analize și speculații editoriale; verificați cu MApN. Nu republicați poziții de aeronave militare.
- ✔ **[Digi24 – canal Telegram public (t.me/s/digi24ro)](<https://t.me/digi24ro>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/digi24ro>  
  Canalul Telegram oficial Digi24 – știri breaking, inclusiv alerte de drone (ex. drona prăbușită la Plauru, Tulcea, RO-Alert Galați/Brăila).  
  *Integrare:* Polling pe previzualizarea publică t.me/s/digi24ro (HTML) sau prin Telethon/RSSHub; filtrare dronă/RO-Alert/MApN.  
  *Atenție:* Presă, nu sursă oficială – marcați «neconfirmat oficial». Respectați rate-limit Telegram.
- ✔ **[Digi24 – etichete «RO-Alert» și «MApN»](<https://www.digi24.ro/eticheta/ro-alert>)** · web · liber · minute · ★★★☆☆ · flux: <https://www.digi24.ro/rss>  
  Paginile de etichetă Digi24 (/eticheta/ro-alert, /eticheta/mapn) adună toate știrile despre RO-Alert, comunicatele MApN și avertizările MAI despre mesaje RO-Alert false.  
  *Integrare:* Polling 5 min pe cele două pagini de etichetă (listă cronologică); dedup pe ID-ul numeric din URL. RSS: feed neconfirmat (Digi24 trimite spre Google News).  
  *Atenție:* Presă; marcați «neconfirmat oficial». Distinct de canalul Telegram Digi24 și de intrarea generică din catalog.
- ✔ **[Euronews România](<https://www.euronews.ro/>)** · web · liber · minute · ★★★☆☆  
  Știri rapide cu citate din MApN și ROMATSA (redeschiderea spațiului aerian Iași), bilanțuri (6 drone doborâte în 2026), drona din copac (Iași), dronă găsită în Vaslui.  
  *Integrare:* Polling pe /articole/; RSS: feed neconfirmat.  
  *Atenție:* Presă; ROMATSA citată indirect – verificați NOTAM.
- ✔ **[Europa Liberă România (RFE/RL)](<https://romania.europalibera.org/>)** · web · liber · ore · ★★★☆☆  
  Serviciul românesc RFE/RL: știri despre RO-Alert Tulcea/Constanța, grupuri de drone deasupra Mării Negre, F-16 ridicate, analize despre apărarea aeriană.  
  *Integrare:* Platformă Pangea (comună cu Europa Liberă Moldova); RSS: feed neconfirmat – verificați pagina /rssfeeds a site-ului. Polling pe homepage.  
  *Atenție:* Distinct de europalibera.md (deja în catalog). Ritm mai lent decât presa de breaking.
- ✔ **[Monitorul de Suceava](<https://www.monitorulsv.ro/>)** · web · liber · minute · ★★★☆☆  
  Cotidian Suceava: zonele vizate de alerte (Frătăuți, Horodnic), drona prăbușită la Solca (24.09.2026), reacții politice.  
  *Integrare:* Polling pe homepage; filtrare dronă/RO-Alert; RSS: feed neconfirmat.  
  *Atenție:* Presă locală; orele pot diferi de cele oficiale.
- ✔ **[News Bucovina](<https://www.newsbucovina.ro/>)** · web · liber · minute · ★★★☆☆  
  Știri Suceava/Bucovina: drona prăbușită la Botoșenița Mare, preluări MApN (două drone, 4 F-16 + elicopter, 31.10.2026).  
  *Integrare:* Polling pe secțiunea /actualitate/; RSS: feed neconfirmat.  
  *Atenție:* Presă locală, preia comunicate; confirmați cu sursa oficială.
- ✔ **[Observator News (Antena 1)](<https://observatornews.ro/>)** · web · liber · minute · ★★★☆☆  
  Știri TV Antena 1: «filmul» alertelor (F-18 spaniole, aeroport închis), primele imagini cu avioanele care au doborât drone.  
  *Integrare:* Polling pe homepage/secțiunea eveniment; RSS: feed neconfirmat.  
  *Atenție:* Presă; nu republicați imagini fără drept.
- ✔ **[Spotmedia.ro – eveniment](<https://spotmedia.ro/stiri/eveniment>)** · web · liber · minute · ★★★☆☆  
  Știri live despre RO-Alert (Iași, Vaslui, Neamț), aeroportul Iași blocat, F-18 care urmăresc drona venită din R. Moldova.  
  *Integrare:* Polling pe /stiri/eveniment; RSS: feed neconfirmat.  
  *Atenție:* Folosit doar ca dovadă în catalogul existent, nu ca sursă monitorizată. Presă.
- ✔ **[SuceavaLIVE](<https://suceavalive.ro/>)** · web · liber · minute · ★★★☆☆  
  Știri Suceava: a raportat închiderea spațiului aerian al Sucevei ~1 oră din cauza dronei.  
  *Integrare:* Polling; site probabil WordPress – /feed/ neconfirmat.  
  *Atenție:* Presă locală; verificați cu NOTAM/ROMATSA.
- ✔ **[SVNews.ro (Suceava)](<https://www.svnews.ro/>)** · web · liber · minute · ★★★☆☆  
  Știri Suceava: începutul și încetarea alarmei de drone, traseul raportat Iași → Botoșani.  
  *Integrare:* Polling; perechile «avertizare»/«a încetat» permit estimarea duratei alertei. RSS: feed neconfirmat.  
  *Atenție:* Presă locală; verificați traseele cu MApN.
- ✔ **[Vasluianul.ro](<https://vasluianul.ro/>)** · web · liber · minute · ★★★☆☆  
  Știri Vaslui: mesajele ISU Vaslui, Shahed intrat dinspre R. Moldova (F-18 de la Baza 57), alarme false (Rediu–Brodoc).  
  *Integrare:* Polling; util și pentru catalogarea alarmelor false (bubuituri raportate la 112). RSS: feed neconfirmat.  
  *Atenție:* Presă locală; unele relatări se dovedesc false – etichetați.
- ✔ **[Viața Liberă Galați](<https://www.viata-libera.ro/>)** · web · liber · minute · ★★★☆☆  
  Cotidian Galați cu relatări detaliate din comunicatele MApN/ISU: ore exacte (RO-Alert 03:20, intrare 03:21, încetare 03:52 – 20.08.2026), aeronave ridicate (F-18 spaniole, IAR-330, F-16 Borcea), drona căzută pe blocul din Mazepa.  
  *Integrare:* Polling pe secțiunea /prima-pagina/; extragere ore din textele «UPDATE» pentru cronologia incidentelor. RSS: feed neconfirmat.  
  *Atenție:* Axa sudică (Galați/Tulcea), relevanță indirectă pentru Iași. Editorialele sunt opinii.
- ✔ **[Vremea Nouă (Vaslui)](<https://vremeanoua.ro/>)** · web · liber · minute · ★★★☆☆  
  Cotidian Vaslui: ora ridicării alertei (19:19, 31.10.2026), traseul dronei din 8.09 (Vaslui → Neamț), avioane la joasă înălțime raportate în Dumești.  
  *Integrare:* Polling; site WordPress – /feed/ neconfirmat; extragere ore de început/sfârșit alertă.  
  *Atenție:* Ton de opinie; mărturiile despre avioane nu sunt confirmate.
- ✔ **[Știrile ProTV – subiectul «MApN»](<https://stirileprotv.ro/stiri-despre/mapn/>)** · web · liber · minute · ★★★☆☆  
  Pagina de subiect ProTV cu toate știrile despre MApN: cronologii ale alertelor (aeroport închis, F-18 spaniole, F-16 de la Câmpia Turzii, RO-Alert în 5 județe).  
  *Integrare:* Polling pe pagina de subiect; extragere titluri+ore. RSS: feed neconfirmat.  
  *Atenție:* Presă; orele din titluri pot diferi de comunicatele oficiale.
- ~ **[Aeroportul Internațional „George Enescu” Bacău – zboruri și comunicate](<https://www.bacauairport.ro/en/>)** · web · liber · ore · ★★★☆☆  
  Site-ul oficial LRBC (orar, comunicate de presă). Bacău e și Baza 95 Aeriană – trafic militar (IAR-99, IAR-330) vizibil pe ADS-B.  
  *Integrare:* Polling pe paginile de orar/comunicate; corelare cu ADS-B pentru suspendări. Status live: neconfirmat.  
  *Atenție:* Fără API; actualizare neregulată. Trafic militar: doar uz intern. Verificare: Site oficial al aeroportului Bacău (LRBC). Neverificat din sesiune (host blocat).
- ~ **[IGSU – comunicate de presă naționale (bilanț 24h, mesaje RO-ALERT)](<https://igsu.ro/comunicate-de-presa>)** · web · liber · ore · ★★★☆☆  
  Comunicatele IGSU, inclusiv bilanțul zilnic al misiunilor cu numărul de mesaje RO-ALERT transmise în ultimele 24h – sursă pentru reconstituirea istoricului alertelor.  
  *Integrare:* Scrapare zilnică a «Bilanțul misiunilor din ultimele 24 de ore» → contor RO-ALERT pe zi; corelare cu incidentele de drone. RSS: feed neconfirmat.  
  *Atenție:* Bilanțul agregă toate tipurile de RO-ALERT (urși, meteo); trebuie filtrat. Distinct de pagina Facebook IGSU deja în catalog. Verificare: Site-ul igsu.ro e distinct de pagina de Facebook IGSU din catalog. În sesiune apare doar rădăcina www.igsu.ro.
- ~ **[Instituția Prefectului Botoșani – comunicate și situații de urgență](<https://bt.prefectura.mai.gov.ro/>)** · web · liber · ore · ★★★☆☆  
  Comunicatele Prefecturii Botoșani (prefect Raluca Curelariu) și pagina de situații de urgență (CJSU); Botoșani primește RO-Alert la incursiunile din nordul R. Moldova.  
  *Integrare:* Site WordPress MAI – verificați /feed/ (feed neconfirmat); polling pe /media/presa/.  
  *Atenție:* Actualizare lentă; confirmare post-factum. Verificare: Calea /media/presa/ e neconfirmată (tipar repetat la mai multe prefecturi).
- ~ **[Instituția Prefectului Suceava – comunicate și hotărâri CJSU](<https://sv.prefectura.mai.gov.ro/>)** · web · liber · ore · ★★★☆☆  
  Comunicatele Prefecturii Suceava și hotărârile CJSU; la 31.10.2026 prefectul a precizat zonele vizate (Frătăuți Noi, Horodnic).  
  *Integrare:* Polling pe /media/presa/ și /hotarari-ale-c-j-s-u-suceava/; feed WordPress neconfirmat.  
  *Atenție:* Pagina de comunicate e slab actualizată (conținut vechi indexat); declarațiile prefectului apar mai repede în presa locală. Verificare: Calea /media/presa/ e neconfirmată (tipar repetat).
- ~ **[ISU Bacău – comunicate de presă](<https://isubc.igsu.ro/comunicate-de-presa>)** · web · liber · ore · ★★★☆☆  
  Comunicatele ISU Bacău; județul a fost inclus în extinderea alertei aeriene (MApN: alertă extinsă pentru Botoșani și Bacău).  
  *Integrare:* Polling pe lista de comunicate. RSS: feed neconfirmat.  
  *Atenție:* Relevanță secundară; doar confirmare post-factum. Verificare: Subdomeniul ISU Bacău e plauzibil. Neverificat din sesiune.
- ~ **[ISU Delta Tulcea – comunicate (inclusiv mesaje RO-ALERT)](<https://isutl.igsu.ro/comunicate-de-presa>)** · web · liber · ore · ★★★☆☆  
  ISU Tulcea publică comunicate pentru fiecare RO-ALERT legat de drone (ex. 26.07.2026: mesaj transmis după semnalarea Statului Major al Forțelor Aeriene). Tulcea are cel mai lung istoric de alerte (59 mesaje până în 2026).  
  *Integrare:* Polling pe isutl.igsu.ro/comunicate-de-presa; extragere dată/oră RO-ALERT pentru calibrarea modelului de predicție (traseu Dunăre → Galați/Tulcea). RSS: feed neconfirmat.  
  *Atenție:* Orientat pe nordul Tulcei, relevanță indirectă pentru Iași. Comunicatul apare după emiterea alertei. Verificare: URL-ul e un singur comunicat (RO-ALERT 26.07.2026, consecvent cu Agerpres 27.07.2026). Pentru monitorizare folosiți lista de comunicate (cale neconfirmată).
- ~ **[ISU Neamț – comunicate de presă](<https://isunt.igsu.ro/comunicate-de-presa>)** · web · liber · ore · ★★★☆☆  
  Comunicatele ISU Neamț; județul a primit RO-Alert la 8.09.2026 (țintă detectată la 18 km N de Roman) și 31.10.2026.  
  *Integrare:* Polling pe pagina de comunicate; extragere titluri și dată. RSS: feed neconfirmat.  
  *Atenție:* Puține comunicate despre drone; majoritatea sunt despre incendii/recrutare. Doar confirmare post-factum. Verificare: Slug-ul articolului citat pare autentic. Lista de comunicate e neverificată din sesiune.
- ~ **[ISU „Gl. Eremia Grigorescu” Galați – comunicate de presă](<https://isugl.igsu.ro/comunicate-de-presa>)** · web · liber · ore · ★★★☆☆  
  Comunicatele ISU Galați – județ cu incidente grave (dronă Geran-2 căzută pe un bloc din Galați, alerte Târgu Bujor 24.08.2026).  
  *Integrare:* Polling pe lista de comunicate; util pentru istoric și confirmarea căderilor de obiecte. RSS: feed neconfirmat.  
  *Atenție:* Relevanță indirectă pentru Iași (axa sudică Dunăre). Fără API. Verificare: Subdomeniul ISU Galați e plauzibil. Neverificat din sesiune.
- ✔ **[Antena 3 CNN – actualitate](<https://www.antena3.ro/actualitate/>)** · web · liber · minute · ★★☆☆☆  
  Știri TV: RO-Alert Iași și închiderea spațiului aerian în nord și centru, apeluri DSU de a nu dezactiva RO-Alert, escortări de avioane militare.  
  *Integrare:* Polling pe /actualitate/; RSS: feed neconfirmat.  
  *Atenție:* Presă cu ton alarmist; confirmați orice detaliu tehnic.
- ✔ **[Cotidianul.ro](<https://www.cotidianul.ro/>)** · web · liber · minute · ★★☆☆☆  
  Articole «UPDATE» live: ora intrării dronei (16:37, SE Iași), pierderea contactului radar la limita Iași–Botoșani, declarații ISU Suceava.  
  *Integrare:* WordPress (?p=) – /feed/ neconfirmat; polling și urmărirea actualizărilor.  
  *Atenție:* Detaliile diferă de alte surse; stocați fiecare versiune.
- ✔ **[Economedia](<https://economedia.ro/>)** · web · liber · minute · ★★☆☆☆  
  Știri despre RO-Alert Iași/Vaslui și dronele care se îndreaptă spre nordul Moldovei.  
  *Integrare:* WordPress (?p=) – /feed/ neconfirmat; polling.  
  *Atenție:* Presă economică; acoperire secundară.
- ✔ **[G4Media](<https://www.g4media.ro/>)** · web · liber · minute · ★★☆☆☆ · flux: <https://www.g4media.ro/feed>  
  Publicație independentă: detalii despre doborârile F-16 (același pilot, două drone în <24h), interceptări de avioane militare ucrainene la Bacău.  
  *Integrare:* Site WordPress – /feed/ probabil (feed neconfirmat); polling pe homepage.  
  *Atenție:* Presă; uneori citează surse anonime.
- ✔ **[Gândul](<https://www.gandul.ro/>)** · web · liber · minute · ★★☆☆☆  
  Știri despre al doilea RO-Alert în Deltă, a treia dronă doborâtă de F-16 deasupra Mării Negre, explicațiile MApN.  
  *Integrare:* Polling pe /actualitate/; RSS: feed neconfirmat.  
  *Atenție:* Ton tabloid; confirmați.
- ✔ **[IașiTV Life](<https://iasitvlife.ro/>)** · web · liber · ore · ★★☆☆☆  
  Televiziune locală Iași: reportaje video despre reacția populației la drone și preluări de alerte RO-Alert din alte județe.  
  *Integrare:* Verificare periodică; util pentru context social post-incident. RSS: feed neconfirmat.  
  *Atenție:* Mai mult conținut video/reportaj, mai puțin breaking.
- ✔ **[Informat.ro (RO + EN)](<https://informat.ro/en/current-affairs/>)** · web · liber · minute · ★★☆☆☆  
  Știri scurte în română și engleză despre alertele de dronă din NE, drone găsite (copac în Iași), avertismente MApN despre capturi de ecran false.  
  *Integrare:* Polling pe secțiunile current-affairs/actualitate; varianta EN utilă pentru rezumate internaționale. RSS: feed neconfirmat.  
  *Atenție:* Agregator cu redacție mică; verificați.
- ✔ **[Monitorul Apărării și Securității](<https://monitorulapararii.ro/>)** · web · liber · ore · ★★☆☆☆  
  Publicație de apărare: analize despre incursiuni (drona Geran-4 din 8.09.2026, căzută în R. Moldova), lacune radar la joasă altitudine, cadrul legal de doborâre.  
  *Integrare:* Verificare zilnică; arhivare pentru analiza post-incident. RSS: feed neconfirmat.  
  *Atenție:* Ton de opinie; datele relative din căutare – verificați data articolului.
- ✔ **[Newsweek România](<https://newsweek.ro/>)** · web · liber · minute · ★★☆☆☆  
  Știri despre alertele de dronă (Iași 8.09 și 20.10.2026, Tulcea), reacțiile MApN și avioanele de luptă ridicate.  
  *Integrare:* Polling pe /actualitate/; RSS: feed neconfirmat.  
  *Atenție:* Titluri senzaționaliste; confirmați cu sursa oficială.
- ✔ **[Radio Constanța – știri Dobrogea](<https://radioconstanta.ro/>)** · web · liber · minute · ★★☆☆☆  
  Radio public regional: alerte aeriene nocturne în Tulcea, trageri în poligonul Capu Midia (context pentru activitate militară).  
  *Integrare:* Site WordPress – /feed/ neconfirmat; polling.  
  *Atenție:* Axa Dobrogea; relevanță mică pentru Iași.
- ✔ **[TVR Info](<https://tvrinfo.ro/>)** · web · liber · minute · ★★☆☆☆  
  Televiziunea publică: grupuri de drone lângă Insula Șerpilor, F-18/F-16 ridicate, drone deasupra R. Moldova.  
  *Integrare:* Site WordPress (?p=) – /feed/ neconfirmat; polling pe homepage.  
  *Atenție:* Presă publică; ritm mai lent la breaking.
- ✔ **[Ziarul Financiar (ZF) – eveniment](<https://www.zf.ro/eveniment/>)** · web · liber · ore · ★★☆☆☆  
  Știri despre RO-Alert în cinci județe și suspendarea temporară a zborurilor la Aeroportul Iași; impact economic.  
  *Integrare:* Polling rar; analiză post-incident (impact asupra aeroportului).  
  *Atenție:* Acoperire secundară.
- ✔ **[Știripesurse.ro (RO + EN)](<https://www.stiripesurse.ro/>)** · web · liber · minute · ★★☆☆☆  
  Știri rapide; a preluat avertismentul MApN că hărțile de pe site-uri neoficiale nu reflectă situația reală din spațiul aerian al României și dezmințiri de «drone» false.  
  *Integrare:* Polling; util pentru detectarea dezinformării (dezmințiri MApN). RSS: feed neconfirmat.  
  *Atenție:* Bazat pe «surse»; credibilitate variabilă.
- ~ **[Adevărul – știri locale și bloguri (Iași/Suceava/Bacău)](<https://adevarul.ro/>)** · web · liber · ore · ★★☆☆☆  
  Ediții locale (stiri-locale/iasi, suceava, bacau) și bloguri critice despre comunicarea MApN privind dronele («Bâlbâiala MApN în legătură cu uite drona, nu e drona»).  
  *Integrare:* Polling pe /stiri-locale/iasi/ și secțiunile din NE; RSS: feed neconfirmat.  
  *Atenție:* Blogurile sunt opinii; separați-le de știri. Verificare: Site real, dar host blocat; articolul-blog citat nu a fost re-verificat. Sursă generalistă, feed RSS neconfirmat.
- ~ **[DSU – site oficial (comunicate, hotărâri CNSU)](<https://dsu.mai.gov.ro/>)** · web · liber · zile · ★★☆☆☆  
  Site-ul Departamentului pentru Situații de Urgență: comunicate oficiale și hotărâri CNSU (ex. HCNSU nr. 23/28.09.2026) – cadrul de răspuns la incidente aeriene.  
  *Integrare:* Verificare zilnică a /legislatie-hotarari și /comunicate-de-presa; arhivare PDF.  
  *Atenție:* Secțiunea de comunicate e rar actualizată; declarațiile rapide (Raed Arafat) apar mai întâi în presă/Facebook. Verificare: Site oficial DSU, distinct de fiipregatit.ro din catalog. Neverificat din sesiune (host blocat).
- ~ **[Forțele Aeriene Române (roaf.ro) – știri poliție aeriană](<https://www.roaf.ro/>)** · web · liber · zile · ★★☆☆☆  
  Site-ul oficial FAR: misiuni de poliție aeriană (F-16 Borcea/Câmpia Turzii, detașamente aliate), interceptări, doborâri de drone. Context pentru avioanele militare observate pe ADS-B.  
  *Integrare:* Site WordPress (?p=ID) – încercați /feed/ (feed neconfirmat); verificare zilnică; corelare cu decolările F-16/F-18 văzute pe agregatoare ADS-B.  
  *Atenție:* Publică cu întârziere de zile. Pozițiile avioanelor militare: doar uz intern, nu republicați. Verificare: Site oficial al Forțelor Aeriene Române. Neverificat din sesiune (host blocat); actualizarea e probabil rară.
- ~ **[Instituția Prefectului Tulcea – comunicate](<https://tl.prefectura.mai.gov.ro/>)** · web · liber · ore · ★★☆☆☆  
  Comunicatele Prefecturii Tulcea (CJSU) – județul cu cele mai frecvente alerte de drone de la granița fluvială cu Ucraina.  
  *Integrare:* Polling pe /media/presa/; feed WordPress neconfirmat.  
  *Atenție:* Relevanță indirectă pentru Iași; rar comunicate dedicate dronelor. Verificare: Calea /media/presa/ e neconfirmată. Relevanță mică pentru Iași (Tulcea).
- ~ **[ISU Vrancea / Brăila / Constanța – comunicate și pagina campaniei RO-ALERT](<https://isubr.igsu.ro/comunicate-de-presa>)** · web · liber · ore · ★★☆☆☆  
  Paginile ISU din sud-est (isuvn, isubr, isuct.igsu.ro): comunicate și pagina informativă despre RO-ALERT; utile pentru incidente pe axa Dunăre/Marea Neagră.  
  *Integrare:* Polling rar (oră) pe /comunicate-de-presa ale fiecărui subdomeniu; context regional.  
  *Atenție:* Departe de Iași; relevanță mică pentru avertizare timpurie. Feed neconfirmat. Verificare: URL-ul e pagina statică a campaniei RO-ALERT a ISU Brăila, nu lista de comunicate. Numele promite și Vrancea și Constanța, care au nevoie de intrări proprii.
- ~ **[NewsNow – știri regionale România (ex. Vaslui)](<https://www.newsnow.com/ro/Actualitate/%C8%98tiri+regionale/Vaslui>)** · web · liber · minute · ★★☆☆☆  
  Agregator de titluri pe județe (pagini «Știri regionale» pentru Vaslui și alte județe) – acoperă presa locală mică fără RSS.  
  *Integrare:* Polling pe paginile județelor din NE; deduplicare cu alte surse. API: plătit/neconfirmat.  
  *Atenție:* Agregator comercial; respectați termenii (fără scraping agresiv). Doar titluri. Verificare: NewsNow e agregator real, dar pagina regională Vaslui nu a putut fi accesată (host blocat, WebSearch epuizat). Agregator terț, fără feed oficial.
- ~ **[Poliția de Frontieră – Inspectoratul Teritorial Iași (comunicare)](<https://www.politiadefrontiera.ro/ro/iasi/>)** · web · liber · ore · ★★☆☆☆  
  Comunicatele ITPF Iași (granița cu R. Moldova pe Prut: Albița, Sculeni); proiecte 2026 precum SKYWATCH. Poate semnala obiecte căzute în zona de frontieră.  
  *Integrare:* Polling orar pe lista «Comunicare»; filtrare dronă/obiect. RSS: feed neconfirmat.  
  *Atenție:* Rareori comunică despre drone; mai util pentru context de frontieră. Fără API. Verificare: Domeniul e confirmat în sesiune (PDF-uri). Calea /n-comunicare-200/ e neconfirmată.
- ~ **[Profit.ro](<https://www.profit.ro/>)** · web · liber · minute · ★★☆☆☆  
  Știri despre RO-Alert în nordul Tulcei după reperarea grupurilor de drone spre ținte ucrainene la graniță.  
  *Integrare:* Polling pe /stiri/; RSS: feed neconfirmat.  
  *Atenție:* Acoperire secundară. Verificare: Există, dar articolul din dovadă e nedatat și nu am văzut un articol 2026. Atenție: ziarulprofit.ro e altă publicație, nu Profit.ro. Acoperire secundară.
- ~ **[R3media – canal Telegram de știri](<https://t.me/R3mediaro>)** · Telegram · liber · minute · ★★☆☆☆ · flux: <https://t.me/s/R3mediaro>  
  Canal Telegram al site-ului de știri R3media (România); preia rapid știri naționale.  
  *Integrare:* Polling t.me/s/R3mediaro; doar ca semnal secundar.  
  *Atenție:* Sursă mică, editorial neverificat; folosiți doar pentru coroborare. Verificare: Handle-ul există (apare în rezultatele de căutare), dar activitatea curentă și linia editorială nu au putut fi confirmate (t.me blocat din sesiune). Editorial neverificat – folosiți doar pentru coroborare.
- ~ **[Ziarul de Bacău](<https://ziaruldebacau.ro/>)** · web · liber · ore · ★★☆☆☆  
  Cotidian Bacău: aeroportul George Enescu, Baza 95 Aeriană, comunitatea de spotteri locali; context pentru traficul militar din zona Bacău.  
  *Integrare:* WordPress (?p=) – /feed/ neconfirmat; polling rar.  
  *Atenție:* Relevanță indirectă. Verificare: Ziar local real; host blocat, articolul ?p=296871 nu a fost re-verificat (conținutul lui nu e confirmat ca fiind despre drone). Feed neconfirmat.
- ~ **[Camera Deputaților – interpelări despre incidente cu drone](<https://www.cdep.ro/interpel/2026/i5980A.pdf>)** · PDF · liber · zile · ★☆☆☆☆  
  Interpelări parlamentare și răspunsurile ministerelor (ex. i5980A/2026 – drona doborâtă de F-16 pe 26 iulie) – sursă pentru analiza post-incident și cronologii oficiale.  
  *Integrare:* Căutare periodică în registrul de interpelări cdep.ro după «dronă»; extragere text PDF.  
  *Atenție:* Întârziere de săptămâni; conținut politic. Verificare: Un singur document (interpelare), nu un feed monitorizabil; tiparul URL e plauzibil pentru cdep.ro, dar PDF-ul nu a putut fi deschis (host blocat). Util doar post-incident.
- ~ **[Capital.ro – bilanțuri MApN](<https://www.capital.ro/>)** · web · liber · zile · ★☆☆☆☆  
  Articole-bilanț pe baza datelor MApN (ex. 18 drone intrate în 2026, 3 doborâte de F-16) – utile pentru serii istorice.  
  *Integrare:* Colectare manuală pentru setul de date istoric.  
  *Atenție:* Cifrele se schimbă rapid (18 → 25 → 35); folosiți data publicării. Verificare: Site de știri real, dar host blocat din sandbox și bugetul WebSearch epuizat; nici site-ul, nici articolul MApN nu au fost re-verificate în această sesiune. Sursă generalistă, nu feed dedicat.
- ~ **[TGStat – directorul canalelor Telegram românești («România TG», @StiriRO)](<https://tgstat.com/>)** · web · liber · zile · ★☆☆☆☆  
  Director/statistici de canale Telegram; comunitatea «România TG» recomandă @StiriRO ca agregator de știri. Util pentru descoperirea altor canale RO.  
  *Integrare:* Folosire manuală pentru descoperire; canalele găsite se adaugă apoi prin t.me/s/<handle>.  
  *Atenție:* Canalele agregatoare au credibilitate scăzută și pot propaga dezinformare; @StiriRO neverificat. Verificare: TGStat este un director real de canale Telegram, dar handle-urile @RomaniaTG și @StiriRO NU au fost confirmate (host blocat, WebSearch epuizat). Nu folosiți handle-urile până la confirmare.
- ~ **[Wall-Street.ro – social](<https://www.wall-street.ro/>)** · web · liber · ore · ★☆☆☆☆  
  Știri despre drone prăbușite (Tulcea – explozie și incendiu, RO-Alert).  
  *Integrare:* Doar pentru arhivă post-incident.  
  *Atenție:* Acoperire secundară. Verificare: Site real, dar host blocat și WebSearch epuizat; articolul despre drona din Tulcea nu a fost re-verificat. Feed RSS neconfirmat.

## Aviație, ADS-B, NOTAM, GNSS

- ~ **[Aeroportul Internațional Chișinău (LUKK) – site oficial](<http://www.airport.md/>)** · web · liber · minute · ★★★★☆  
  Site-ul aeroportului (sosiri/plecări). Spațiul aerian al R. Moldova e restricționat la incursiuni, iar drone au perturbat aeroportul pe 8.09.2026.  
  *Integrare:* Anulări/întârzieri simultane la LUKK + oprirea traficului ADS-B = semnal timpuriu (dronele trec prin RM spre Prut).  
  *Atenție:* Restricțiile au și alte cauze; feed neconfirmat; fără scraping agresiv. Verificare: Site oficial (home_link OurAirports), inaccesibil din sandbox. Suprapunere parțială cu intrările Kayak (Chișinău) și caa.md din catalog, dar URL oficial distinct.
- ✔ **[adsb.fi Open Data – /v2/mil și /v2/sqk](<https://opendata.adsb.fi/api/v2/mil>)** · API · liber · timp real · ★★★☆☆  
  Endpoint public adsb.fi cu aeronavele marcate militar, plus /v2/sqk/[squawk] și /v3/lat/[lat]/lon/[lon]/dist/[dist] (până la 250 NM); compatibil ADSBexchange v2.  
  *Integrare:* A treia sursă redundantă pentru militari și squawk-uri de urgență, cu aceeași logică de unire după hex; 1 cerere/s.  
  *Atenție:* Uz personal, necomercial; citare obligatorie a adsb.fi cu link; cererile invalide (4xx) duc la blocare temporară de IP. Uz intern; nu republicați poziții de aeronave militare.
- ✔ **[adsb.lol API – /v2/mil (aeronave marcate militar)](<https://api.adsb.lol/v2/mil>)** · API · liber · timp real · ★★★☆☆  
  Endpoint public care întoarce toate aeronavele marcate militar (dbFlags & 1) din rețeaua adsb.lol, în format compatibil ADSBexchange v2.  
  *Integrare:* Interogare la 30–60 s, filtrare locală pe bbox Prut–Iași (~26–30,5°E, 45–48,6°N); canal intern separat „militar”: avioane de luptă, AWACS, realimentare sau ISR lângă Iași = indiciu de misiune de poliție aeriană în curs.  
  *Atenție:* Multe aeronave militare zboară cu transponderul oprit sau doar în Mode S; dronele Geran/Shahed nu au ADS-B. API fără SLA; cheie API anunțată pentru viitor (prin feeding). Uz intern; nu republicați poziții de aeronave militare.
- ✔ **[adsb.lol re-api (doar pentru feederi) – filtre pe server](<https://re-api.adsb.lol/>)** · API · cont gratuit · timp real · ★★★☆☆  
  Interfața readsb „re-api” a adsb.lol, accesibilă doar stațiilor care trimit date; permite filtre pe server (zonă, filter_mil, find_squawk) într-o singură cerere.  
  *Integrare:* După instalarea receptorului propriu în Iași: o cerere pe zonă cu filter_mil (militari) și una fără (civili) la 30 s, în loc de mai multe endpoint-uri publice.  
  *Atenție:* Necesită o stație care alimentează adsb.lol (acces după IP). Parametrii exacți: vezi README-json readsb. Uz intern; nu republicați poziții de aeronave militare.
- ~ **[Aeroportul Suceava „Ștefan cel Mare” (LRSV) – site oficial](<http://www.aeroportsuceava.ro/index_en.html>)** · web · liber · minute · ★★★☆☆  
  Site-ul aeroportului; LRSV e aeroport de deviere pentru Iași (cursa Eindhoven–Iași a fost deviată aici pe 31.10.2026).  
  *Integrare:* Corelare: sosiri neprogramate la LRSV + așteptări lângă LRIA = posibilă închidere a spațiului aerian la Iași.  
  *Atenție:* Devierile au și cauze meteo; feed neconfirmat. Verificare: home_link din OurAirports (poate fi învechit); site inaccesibil din sandbox. Articolul news.ro din dovezi e despre aeroportul Iași, nu Suceava.
- ~ **[airplanes.live API – /v2/mil și /v2/squawk](<https://api.airplanes.live/v2/mil>)** · API · liber · timp real · ★★★☆☆  
  Endpoint public cu toate aeronavele marcate militar; /v2/squawk/[cod] pentru coduri de urgență. Limită 1 cerere/s, uz necomercial, fără feeder obligatoriu.  
  *Integrare:* A doua sursă pentru militari, din altă rețea de receptoare: interogare alternativă cu adsb.lol, unire după hex, păstrarea celei mai noi poziții.  
  *Atenție:* Fără SLA și fără garanție de disponibilitate; necomercial. Uz intern; nu republicați poziții de aeronave militare. Verificare: airplanes.live nu a putut fi accesat în această sesiune (host blocat); readsb confirmă doar existența globe.airplanes.live. Sub-endpoint al API-ului deja în catalog (airplanes.live/api-guide). Necomercial, 1 req/s; doar uz intern.
- ~ **[FAA DINS – Defense Internet NOTAM Service](<https://www.notams.faa.gov/dinsQueryWeb/>)** · web · liber · minute · ★★★☆☆  
  Interogare NOTAM internaționale după indicator ICAO/FIR sau rază; sursa din care ICAO API Data Service preia NOTAM-urile realtime.  
  *Integrare:* Interogare la 10–15 min, doar ca semnal secundar, pentru LRBB, LUUU, UKOV, LRIA, LUKK; comparare cu lista anterioară pentru NOTAM-uri noi.  
  *Atenție:* Fără API oficial; scraper-ul AVWX pentru DINS e comentat; „nu pentru uz operațional”. Feed neconfirmat. Verificare: DINS apare în avwx-engine, dar clasa FaaDinsNotam e comentată (motiv nespecificat); accesul automat neconfirmat, doar uz manual. Inaccesibil din sandbox. Catalogul existent (NMS-API) îl menționează doar ca alternativă – URL distinct.
- ~ **[FAA NOTAM Search (notams.aim.faa.gov)](<https://notams.aim.faa.gov/notamSearch/>)** · web · liber · minute · ★★★☆☆  
  Căutare publică NOTAM a FAA după indicator ICAO, rază sau regiune; acoperirea NOTAM-urilor internaționale (LRIA, LRBB, LUKK, LUUU): neconfirmată.  
  *Integrare:* Interogare declanșată de alte semnale pentru LRIA, LRSV, LRBC, LUKK și FIR LRBB/LUUU/UKOV; parsare text pentru restricții temporare.  
  *Atenție:* Biblioteca AVWX are scraper-ul pentru acest serviciu comentat (automatizare instabilă); nu e pentru uz operațional; restricțiile apar adesea după anunțul MApN. Feed neconfirmat. Verificare: Portal FAA NOTAM Search real; în avwx-engine clasa FaaAimNotam e dezactivată („behind a recaptcha and times out”) → doar uz manual, nu automat. Inaccesibil din sandbox. Serviciu distinct de NMS-API din catalog.
- ✔ **[adsb.exposed – explorare istorică ADS-B](<https://adsb.exposed/>)** · hartă · liber · istoric · ★★☆☆☆  
  Interfață web de vizualizare/analiză pe volume mari de date ADS-B istorice generate cu readsb.  
  *Integrare:* Post-incident: vizualizarea traficului din zona Iași–Chișinău în ziua alertei (densitate, devieri) pentru raport.  
  *Atenție:* Acoperirea, sursele exacte și întârzierea de actualizare: neconfirmate. Uz intern; nu republicați poziții de aeronave militare.
- ✔ **[adsb.lol feed client](<https://github.com/adsblol/feed>)** · altele · liber · timp real · ★★☆☆☆  
  Kit de alimentare ADS-B + MLAT către adsb.lol (Docker sau script); viitoarea cheie API adsb.lol se obține prin feeding.  
  *Integrare:* Rulați-l pe receptorul din Iași ca să păstrați accesul la API când cheia devine obligatorie și să adăugați MLAT local.  
  *Atenție:* Datele trimise devin publice (ODbL); nu activați ACARS/VDL2 (comunicații nepublice).
- ✔ **[adsb.lol – arhivă zilnică globe_history_2026 (GitHub Releases)](<https://github.com/adsblol/globe_history_2026/releases>)** · set de date · liber · zile · ★★☆☆☆  
  Dump zilnic complet al datelor adsb.lol (trace-uri readsb, heatmap), licență ODbL; câte o versiune pe zi, inclusiv date de la TheAirTraffic și FlyItalyADSB.  
  *Integrare:* După incident: descărcați ziua (fișierele .tar.aa/.ab), extrageți trace-urile din bbox Iași–Chișinău și reconstruiți așteptările, devierile și zborurile militare vizibile; comparați cu cronologia MApN. Verificare vizuală rapidă: reluarea pe hartă la https://adsb.lol/?r (fișierele heatmap din arhivă).  
  *Atenție:* Volum foarte mare (README: ~1976 GiB pentru 2026); ODbL cere atribuire și share-alike pentru baze derivate. Analiza aeronavelor militare doar intern.
- ✔ **[aviationweather.gov Data API (NOAA AWC) – METAR/TAF](<https://aviationweather.gov/data/api/>)** · API · liber · minute · ★★☆☆☆ · flux: <https://aviationweather.gov/api/data/metar?ids=LRIA&format=json>  
  API public pentru METAR, TAF și PIREP (JSON) pentru orice aeroport ICAO, inclusiv LRIA, LRSV, LRBC, LUKK.  
  *Integrare:* La 30 min: plafon, vizibilitate, vânt la LRIA/LUKK, context pentru observarea vizuală și deriva dronei; arată și dacă un aeroport a încetat să emită.  
  *Atenție:* Meteo, nu semnal direct de dronă; limitele de rată: neconfirmate.
- ✔ **[Indicator GNSS propriu din JSON readsb (gpsOkBefore, NIC/NACp)](<https://github.com/wiedehopf/readsb/blob/dev/README-json.md>)** · API · liber · timp real · ★★☆☆☆  
  Câmpul experimental gpsOkBefore marchează aeronavele care au pierdut sau degradat GPS (afișat 15 min); nic, rc, nac_p dau integritatea poziției (metoda din spatele hărților de bruiaj).  
  *Integrare:* În veghe: la fiecare minut numărați aeronavele cu gpsOkBefore sau NACp scăzut în bbox RO–MD–sudul UA (adsb.lol/adsb.fi/receptor propriu) → hartă internă de bruiaj GNSS, ca context.  
  *Atenție:* Câmp experimental; bruiajul GNSS nu indică direct o dronă; nu publicați.
- ✔ **[mlat-client (wiedehopf)](<https://github.com/wiedehopf/mlat-client>)** · altele · liber · timp real · ★★☆☆☆  
  Client de multilaterație: trimite mesaje Mode S la un server care calculează poziția aeronavelor care nu transmit poziție ADS-B (doar Mode S), situație frecventă la aeronave militare.  
  *Integrare:* Receptorul din Iași alimentează MLAT la adsb.lol, adsb.fi și airplanes.live (prin ultrafeeder) → mai multe poziții MLAT în Moldova (RO) pentru aeronave doar Mode S.  
  *Atenție:* MLAT cere ≥ 3–4 receptoare care văd aceeași aeronavă; precizie variabilă (README-json: „outliers … expected”). Uz intern; nu republicați poziții de aeronave militare.
- ✔ **[NOAA tgftp – METAR/TAF text pe stație](<https://tgftp.nws.noaa.gov/data/observations/metar/stations/LRIA.TXT>)** · API · liber · minute · ★★☆☆☆  
  Fișier text cu ultimul METAR pentru o stație; TAF la /data/forecasts/taf/stations/{ICAO}.TXT; cicluri orare la /metar/cycles/{HH}Z.TXT.  
  *Integrare:* Rezervă simplă (HTTP GET) când API-ul AWC nu răspunde; parsare cu python-metar.  
  *Atenție:* Doar ultimul raport; întârziere de câteva minute.
- ✔ **[plane-alert-db – liste de aeronave militare (SDR-Enthusiasts)](<https://github.com/sdr-enthusiasts/plane-alert-db>)** · set de date · liber · zile · ★★☆☆☆ · flux: <https://raw.githubusercontent.com/sdr-enthusiasts/plane-alert-db/main/plane-alert-mil.csv>  
  CSV cu aeronave „de interes”; plane-alert-mil.csv are 9.856 intrări militare cu operator, tip și categorie (ex. Forțele Aeriene Române, NATO RQ-4D, categoriile Oxcart = ISR și UAV).  
  *Integrare:* Watchlist în veghe: alertă internă când o aeronavă din categoriile Oxcart, UAV, Quango (NATO) sau Other Air Forces apare în bbox; îmbogățirea mesajelor cu rolul aeronavei.  
  *Atenție:* Lista conține și categorii despre persoane private (oligarhi, „Dictator Alert”): nu le folosiți (risc de urmărire a persoanelor). Uz intern; nu republicați poziții de aeronave militare.
- ✔ **[Planefence / Plane-Alert (docker-planefence)](<https://github.com/sdr-enthusiasts/docker-planefence>)** · altele · liber · timp real · ★★☆☆☆  
  Container care alertează când receptorul propriu vede o aeronavă din watchlist (plane-alert-db) sau una care trece aproape; poate posta pe Mastodon/Discord.  
  *Integrare:* Pe receptorul din Iași: alertă internă (webhook → ntfy/Telegram privat) la detecția locală a unei aeronave militare/ISR.  
  *Atenție:* Dezactivați postările publice (Mastodon/Discord); excludeți categoriile despre persoane private. Uz intern; nu republicați poziții de aeronave militare.
- ✔ **[readsb (wiedehopf) – decodor + JSON cu dbFlags](<https://github.com/wiedehopf/readsb>)** · altele · liber · timp real · ★★☆☆☆  
  Decodorul Mode S/ADS-B folosit de adsb.lol, airplanes.live și adsb.fi; JSON documentat: dbFlags (militar = 1, PIA = 4, LADD = 8), emergency, nic/nac_p, gpsOkBefore; API local cu filter_mil și find_squawk.  
  *Integrare:* Pe receptorul din Iași rulați readsb cu --db-file (tar1090-db) ca să aveți flag-ul militar și API-ul local; veghe citește deja formatul re-api.  
  *Atenție:* Necesită RTL-SDR și antenă 1090 MHz; recepție doar în linie de vedere. Uz intern; nu republicați poziții de aeronave militare.
- ✔ **[tar1090-db – bază de aeronave cu flag militar (CSV)](<https://github.com/wiedehopf/tar1090-db>)** · set de date · liber · zile · ★★☆☆☆ · flux: <https://raw.githubusercontent.com/wiedehopf/tar1090-db/csv/aircraft.csv.gz>  
  CSV (~8 MB gz) hex → înmatriculare, tip, flaguri; ~23.000 de intrări marcate militar (verificat: 4A35A7 An-30 al Forțelor Aeriene Române, 33FD45 RQ-4 NATO).  
  *Integrare:* Încărcați-l în veghe ca să marcați militarii și în surse care nu dau dbFlags (OpenSky, receptor fără --db-file).  
  *Atenție:* Derivat din baza Mictronics; incomplet pentru hex-uri militare necunoscute; nu conține poziții.
- ✔ **[traffic – analiză de traiectorii (OpenSky, EUROCONTROL DDR)](<https://traffic-viz.github.io/>)** · altele · liber · istoric · ★★☆☆☆  
  Bibliotecă Python pentru manipularea și analiza traiectoriilor; accesează date ADS-B deschise (OpenSky) și fișiere EUROCONTROL DDR.  
  *Integrare:* Post-incident: reconstruiți traiectoriile din arhiva adsb.lol/OpenSky și detectați devieri sau așteptări lângă LRIA/LUKK pentru raport.  
  *Atenție:* Unelte de analiză, nu sursă de date; accesul la OpenSky Trino cere cont.
- ~ **[ADSBHub – schimb de date ADS-B](<https://www.adsbhub.org>)** · API · cont gratuit · timp real · ★★☆☆☆  
  Rețea de schimb de date ADS-B: stațiile care contribuie primesc fluxul agregat (format SBS/BaseStation); citată de adsb.lol ca agregator care își deschide datele.  
  *Integrare:* Cu receptorul din Iași: alimentați ADSBHub (container docker-adsbhub) și primiți fluxul agregat ca redundanță când API-urile publice cad.  
  *Atenție:* Accesul cere o stație care trimite date și o cheie de stație; termenii exacți și acoperirea în RO/MD: neconfirmat. Uz intern; nu republicați poziții de aeronave militare. Verificare: ADSBHub există (container docker activ care trimite date SBS), dar site-ul nu a putut fi accesat. Oferă flux SBS pentru contribuitori, nu API REST.
- ~ **[Aeroportul Bacău „George Enescu” (LRBC) – site oficial](<http://www.bacauairport.ro/>)** · web · liber · minute · ★★☆☆☆  
  Site-ul aeroportului din Bacău; județul a fost inclus în alerta RO-Alert din 31.10.2026.  
  *Integrare:* Al doilea punct de deviere de urmărit pentru zborurile spre Iași/Suceava.  
  *Atenție:* Feed neconfirmat; relevanță indirectă. Verificare: home_link din OurAirports; site inaccesibil din sandbox; activitatea curentă a site-ului neconfirmată.
- ~ **[AirNav Radar (ex-RadarBox) – hartă și API](<https://www.airnavradar.com>)** · API · plătit · timp real · ★★☆☆☆  
  Tracker comercial cu hartă publică, rețea proprie de feederi (rbfeeder) și API (api.radarbox.com/v2, client generat OpenAPI pe PyPI).  
  *Integrare:* Opțional: a doua sursă comercială pentru LRIA/LUKK dacă se obține acces API; feeding cu rbfeeder din receptorul propriu.  
  *Atenție:* API plătit (preț neconfirmat); nu faceți scraping pe hartă. Uz intern; nu republicați poziții de aeronave militare. Verificare: AirNav Radar (ex-RadarBox) confirmat prin containerul rbfeeder; site/API comercial neaccesat. Pachetul PyPI „radarbox” are metadate placeholder – nu îl folosiți ca dovadă.
- ~ **[EUROCONTROL NM B2B web services](<https://www.eurocontrol.int/network-manager>)** · API · necunoscut · minute · ★★☆☆☆  
  Serviciile B2B ale Network Manager (zboruri, reglementări ATFM, date de spațiu aerian) pentru utilizatori autorizați; client Python pyb2b.  
  *Integrare:* Doar printr-un partener eligibil (aeroport, operator): reglementări sau restricții care afectează LRIA/LRBB în timp aproape real.  
  *Atenție:* Acces cu certificat și eligibilitate (neconfirmat pentru un ONG); condițiile se negociază cu EUROCONTROL. Verificare: Serviciul NM B2B există, dar accesul cere acord EUROCONTROL + certificat (nu e deschis civililor). pyb2b 0.1.0 e din 2023-07 (neîntreținut). URL-ul dat e pagina generală Network Manager.
- ~ **[Flightjar – tracker auto-găzduit cu jurnal JSONL](<https://github.com/MrSuttonmann/flightjar>)** · altele · liber · timp real · ★★☆☆☆  
  Tracker pentru receptor propriu: hartă, panou cu rută (adsbdb) și METAR (aviationweather.gov), statistici, alerte pe watchlist și jurnal JSONL al tuturor mesajelor.  
  *Integrare:* Jurnalul JSONL = arhivă proprie pentru reconstituirea post-incident; alertele watchlist doar către grupul intern.  
  *Atenție:* Proiect mic; verificați maturitatea. Uz intern; nu republicați poziții de aeronave militare. Verificare: Repo-ul există (README, docker-compose), dar nu are changelog/date; proiect personal mic, activitate neconfirmată. Jurnalul JSONL e dezactivat implicit (BEAST_OUTFILE).
- ~ **[TheAirTraffic – hartă globe (tar1090)](<https://globe.theairtraffic.com>)** · hartă · liber · timp real · ★★☆☆☆  
  Hartă tar1090 a unui agregator comunitar care își partajează datele cu adsb.lol (incluse în arhiva deschisă).  
  *Integrare:* Verificare vizuală a unei aeronave/ trasee când adsb.lol sau airplanes.live nu răspund.  
  *Atenție:* API neconfirmat; operat de o singură persoană. Uz intern; nu republicați poziții de aeronave militare. Verificare: TheAirTraffic există (feed.theairtraffic.com în ultrafeeder, partener adsb.lol, globe.theairtraffic.com folosit de plane-notify); site neaccesat. Agregator comunitar mic, rulat de un entuziast.
- ✔ **[adsb.im – imagine feeder all-in-one](<https://adsb.im>)** · altele · liber · timp real · ★☆☆☆☆  
  Imagine pentru plăci Raspberry Pi/DietPi care alimentează simultan zeci de agregatori (adsb.lol, adsb.fi, airplanes.live, ADSBHub, OpenSky, FR24, FlightAware etc.).  
  *Integrare:* Cea mai rapidă cale de a pune în funcțiune un receptor în Iași de către voluntari fără experiență Docker.  
  *Atenție:* Dezactivați modulele ACARS/VDL2/HFDL (interceptarea comunicațiilor nepublice e interzisă).
- ✔ **[adsbdb.com – API public aeronave și rute](<https://www.adsbdb.com>)** · API · liber · zile · ★☆☆☆☆  
  API gratuit: /v0/aircraft/[MODE_S/REG], /v0/callsign/[CALLSIGN] (rută origine–destinație), /v0/airline.  
  *Integrare:* Îmbogățirea alertelor de deviere: ruta planificată vs. aeroportul real (ex. cursa Eindhoven–Iași deviată la Suceava pe 31.10.2026).  
  *Atenție:* Comunitar, fără SLA; rutele pot fi învechite.
- ✔ **[AVWX Engine – preluare și parsare METAR/TAF/SIGMET](<https://engine.avwx.rest>)** · altele · liber · minute · ★☆☆☆☆  
  Bibliotecă Python care preia rapoarte din surse guvernamentale și parsează METAR, TAF, PIREP, AIRMET/SIGMET, NOTAM (reguli de zbor, interpolare).  
  *Integrare:* Modul meteo în veghe: avwx.Metar('LRIA').update() pentru context structurat.  
  *Atenție:* Scraper-ele NOTAM FAA sunt comentate în cod (nefuncționale acum).
- ✔ **[dump1090-fa (FlightAware)](<https://github.com/flightaware/dump1090>)** · altele · liber · timp real · ★☆☆☆☆  
  Decodorul Mode S/ADS-B al FlightAware, alternativă la readsb pentru receptorul propriu.  
  *Integrare:* Folosiți-l doar dacă receptorul rulează deja stack-ul FlightAware; altfel readsb.  
  *Atenție:* Fără flag militar fără bază de date externă; recepție locală.
- ✔ **[EUROCONTROL – Aviation Intelligence / ANS Performance (ansperformance.eu)](<https://ansperformance.eu>)** · set de date · liber · zile · ★☆☆☆☆  
  Portalul Performance Review Unit: date despre trafic zilnic pe aeroporturi și state, întârzieri ATFM, publicații; descărcări de date.  
  *Integrare:* Post-incident: scăderi de trafic la LRIA/LRSV sau în spațiul MD în zilele cu incursiuni; serii pentru raport.  
  *Atenție:* Agregare zilnică sau mai rară; nu e semnal de avertizare.
- ✔ **[Iowa Environmental Mesonet (IEM) – arhivă de observații](<https://mesonet.agron.iastate.edu>)** · set de date · liber · istoric · ★☆☆☆☆  
  Arhivă de observații meteo (inclusiv METAR/ASOS) cu descărcări, întreținută de Iowa State University.  
  *Integrare:* Post-incident: METAR istoric pentru ora alertei (nori, vizibilitate, vânt).  
  *Atenție:* Acoperirea pentru LRIA/LUKK: neconfirmată aici; verificați înainte de a vă baza pe ea.
- ✔ **[Mictronics – Aircraft Database](<https://www.mictronics.de/aircraft-database/>)** · set de date · liber · zile · ★☆☆☆☆  
  Bază de date de aeronave (hex ICAO, tip, operator) cu exporturi JSON pentru dump1090/readsb; actualizare săptămânală; licență ODC Attribution.  
  *Integrare:* Sursa de bază pentru tar1090-db; folosiți direct doar dacă aveți nevoie de câmpuri suplimentare.  
  *Atenție:* Atribuire obligatorie (ODC-By); acoperire militară incompletă.
- ✔ **[mlat-server (wiedehopf) – rețea MLAT proprie](<https://github.com/wiedehopf/mlat-server>)** · altele · liber · timp real · ★☆☆☆☆  
  Server de multilaterație care nu cere ceasuri sincronizate: folosește aeronavele ADS-B ca balize și localizează aeronavele doar Mode S.  
  *Integrare:* Dacă se ajunge la 4+ receptoare proprii în IS/BT/VS (nivel B), MLAT propriu, independent de agregatori.  
  *Atenție:* Licență AGPL v3 (obligații dacă serviciul e expus în rețea); efort tehnic mare.
- ✔ **[OurAirports – date deschise despre aeroporturi](<https://ourairports.com/data/>)** · set de date · liber · zile · ★☆☆☆☆ · flux: <https://davidmegginson.github.io/ourairports-data/airports.csv>  
  CSV-uri actualizate zilnic: aeroporturi, piste, frecvențe, navaid-uri, regiuni; include link-urile oficiale (ex. LRIA → aeroport-iasi.ro).  
  *Integrare:* Geofence-uri și praguri de distanță pentru LRIA, LRSV, LRBC, LUKK în detectorul de așteptări și devieri.  
  *Atenție:* Date comunitare; verificați coordonatele pistelor.
- ✔ **[PiAware (FlightAware)](<https://flightaware.com/adsb/piaware/>)** · altele · cont gratuit · timp real · ★☆☆☆☆  
  Software care trimite datele receptorului la FlightAware (piaware, faup1090, fa-mlat-client pentru MLAT); configurare cu cont FlightAware.  
  *Integrare:* Opțional, dacă se dorește și acoperire FlightAware/AeroAPI pentru zona Iași.  
  *Atenție:* Datele trimise ajung la un serviciu comercial; verificați termenii.
- ✔ **[pyModeS – decodor Mode S/ADS-B în Python](<https://github.com/junzis/pyModeS>)** · altele · liber · istoric · ★☆☆☆☆  
  Bibliotecă Python (v3, funcție unică decode()) pentru decodarea mesajelor Mode S/ADS-B brute.  
  *Integrare:* Decodare offline a mesajelor brute înregistrate de receptorul propriu, pentru analiza post-incident.  
  *Atenție:* Licență GPL-3.0; Python 3.11+.
- ✔ **[python-metar-taf-parser (mivek)](<https://github.com/mivek/python-metar-taf-parser>)** · altele · liber · minute · ★☆☆☆☆  
  Parser Python pentru METAR și TAF (există și o versiune JavaScript, metar-taf-parser).  
  *Integrare:* Alternativă ușoară la AVWX pentru parsarea textului METAR/TAF din tgftp sau AWC.  
  *Atenție:* Doar parsare, nu sursă de date.
- ✔ **[SDR-Enthusiasts – ghid ADS-B (gitbook)](<https://sdr-enthusiasts.gitbook.io/ads-b/>)** · altele · liber · zile · ★☆☆☆☆  
  Ghid pas cu pas pentru receptoare ADS-B pe Docker (ultrafeeder, feederi, MLAT, alerte).  
  *Integrare:* Manual pentru voluntarii care instalează receptoare în județul Iași.  
  *Atenție:* Documentație, nu date.
- ✔ **[tar1090 – interfață hartă pentru receptor](<https://github.com/wiedehopf/tar1090>)** · altele · liber · timp real · ★☆☆☆☆  
  Hartă web pentru readsb/dump1090: filtre după tip, callsign, altitudine, parametri URL (?icao=…), trasee pe 8 h; baza hărților globe.* ale agregatorilor.  
  *Integrare:* Hartă locală pentru operator; link-uri ?icao=<hex> în mesajele interne către grup.  
  *Atenție:* Doar vizualizare; nu expuneți public harta receptorului dacă arată aeronave militare.
- ~ **[Aeroporturile București (LROP Otopeni) – site oficial](<http://www.bucharestairports.ro/en/>)** · web · liber · minute · ★☆☆☆☆  
  Site-ul CNAB pentru Henri Coandă; context național (închideri sau devieri la scară largă).  
  *Integrare:* Doar context; nu e indicator pentru Iași.  
  *Atenție:* Relevanță scăzută pentru avertizarea locală. Verificare: home_link din OurAirports; inaccesibil din sandbox; relevanță mică pentru Iași.
- ~ **[EUROCONTROL DDR2 – Demand Data Repository](<https://www.eurocontrol.int/ddr>)** · set de date · necunoscut · istoric · ★☆☆☆☆  
  Depozit EUROCONTROL de date de trafic planificat și realizat (traiectorii, spațiu aerian), folosit în cercetare.  
  *Integrare:* Studii post-incident cu parteneri academici: reprogramări și devieri în FIR LRBB în zilele cu incursiuni.  
  *Atenție:* Acces restricționat (eligibilitate neconfirmată); date istorice. Verificare: DDR2 există (link în README trrrj); acces doar cu acord/înregistrare EUROCONTROL; date istorice, utile doar pentru analiză. Inaccesibil din sandbox.
- ~ **[live-military-mode-s.eu – coduri Mode S militare](<https://www.live-military-mode-s.eu/>)** · set de date · necunoscut · zile · ★☆☆☆☆  
  Bază comunitară de coduri Mode S militare (hex → unitate/tip), folosită ca sursă pentru plane-alert-db.  
  *Integrare:* Verificare manuală a unui hex militar necunoscut din bbox.  
  *Atenție:* Acces și termeni neconfirmați; verificați încrucișat cu alte baze. Verificare: Listat ca sursă de date în README-ul plane-alert-db (actual). Site inaccesibil din sandbox; activitatea curentă neconfirmată. Doar uz intern, nu republicați poziții.
- ~ **[Plane Finder](<https://planefinder.net>)** · web · liber · timp real · ★☆☆☆☆  
  Tracker comercial cu hartă live și client de partajare (pfclient) pentru receptoare proprii.  
  *Integrare:* Doar verificare vizuală manuală; feeding opțional cu container docker-planefinder.  
  *Atenție:* API public neconfirmat; nu automatizați harta (termeni). Uz intern; nu republicați poziții de aeronave militare. Verificare: Plane Finder confirmat prin containerul pfclient (link-uri planefinder.net/sharing); site neaccesat din sandbox. Agregator comercial, fără API public gratuit confirmat.
- ~ **[Planespotters.net – bază de aeronave și feed ADS-B](<https://www.planespotters.net>)** · web · liber · zile · ★☆☆☆☆  
  Bază de date de aeronave și flote (fotografii, înmatriculări) și agregator ADS-B non-profit (feed.planespotters.net, MLAT).  
  *Integrare:* Identificare manuală a unei aeronave (tip, operator) după înmatriculare/hex în analiza post-incident.  
  *Atenție:* API pentru flote/foto neconfirmat; nu automatizați fără acord. Uz intern; nu republicați poziții de aeronave militare. Verificare: Planespotters confirmat ca agregator în ultrafeeder (feed/mlat.planespotters.net); site neaccesat. Nu are API public de poziții live – util doar ca bază foto/flote.
- ~ **[Scramble (scramble.nl) – baze de date de aviație militară](<https://scramble.nl/>)** · web · necunoscut · zile · ★☆☆☆☆  
  Comunitate olandeză de aviație militară cu baze de date despre flote și unități; sursă pentru plane-alert-db.  
  *Integrare:* Context: identificarea unității/bazei unei aeronave militare văzute lângă Iași.  
  *Atenție:* Unele baze pot cere abonament (neconfirmat); nu e sursă de timp real. Verificare: Listat în README-ul plane-alert-db. Site inaccesibil din sandbox. Bazele de date Scramble sunt parțial cu plată/abonament. Doar uz intern.
- ~ **[Virtual Radar Server](<https://github.com/vradarserver/vrs>)** · altele · liber · timp real · ★☆☆☆☆  
  Server și hartă locală pentru date de la receptoare (BaseStation/Beast), alternativă la tar1090.  
  *Integrare:* Doar dacă operatorii preferă Windows; altfel tar1090.  
  *Atenție:* Proiect vechi (.NET); verificați întreținerea. Verificare: Repo-ul există, dar README-ul pomenește Visual Studio 2019/TypeScript 2.3; activitate curentă neconfirmată (fără date de commit). Preferați tar1090/readsb.

## OSINT conflict, analize, date istorice

- ✔ **[єРадар (@eRadarrua)](<https://t.me/eRadarrua>)** · Telegram · liber · minute · ★★★★☆ · flux: <https://t.me/s/eRadarrua>  
  Canal de radar civil cu mesaje scurte despre direcția dronelor și rachetelor; 62.000 de mesaje (împreună cu kpszsu) au fost arhivate din preview-ul public pentru un model de predicție.  
  *Integrare:* Scraper t.me/s cu paginare ?before=; profil de parsare dedicat pentru mesajele scurte (vezi despa1r0/custom-alert); semnal de confirmare încrucișată.  
  *Atenție:* Neoficial; nivel de încredere 0,65 în configurația Puluj-g. Modelul KSE nu a câștigat precizie din aceste date la nivel de raion.
- ~ **[Liveuamap Moldova (subdomeniu + API regiunea 137)](<https://moldova.liveuamap.com>)** · hartă · liber · minute · ★★★★☆  
  Pagina Liveuamap dedicată R. Moldova (incidente cu drone, resturi, alerte); API-ul oficial are regiunea Moldova = 137.  
  *Integrare:* Monitorizare pagină sau API (a.liveuamap.com/api, cu cheie) filtrat pe resid=137; deduplicare cu presa MD.  
  *Atenție:* API-ul este plătit (aprox. 85 USD/an după o listă de surse); ToS restrictive, fără redistribuire. Subdomeniul a fost văzut în arhive de pagini, nu direct. Verificare: Subdomeniu regional distinct de liveuamap.com din catalog. API-ul e cu plată (~150 $/lună), singura cale structurată permisă; pagina e ofuscată anti-scraping. Codul 137 vine dintr-un exemplu vechi (enum „use database for regions”) – poate fi învechit.
- ✔ **[airAlertAnalysisKSE – predicția debutului alertelor pe raion (15/30/60 min)](<https://github.com/kolon3d-prog/airAlertAnalysisKSE>)** · set de date · liber · istoric · ★★★☆☆  
  Prototip KSE: LightGBM pe istoricul alertelor și pe vecinătatea raioanelor; top-30 hit ≈0,8–0,87 la 15 min; replay pe noaptea din 2026-10-08.  
  *Integrare:* Metodologie de reutilizat: propagarea pe vecinătăți (Odesa→MD→RO) ca predictor; contractul de date docs/prediction_contract.md.  
  *Atenție:* Nu e sistem de avertizare; alertele sunt un proxy decis de autorități, nu traiectorii.
- ✔ **[drone-alerter – estimarea timpului de sosire pe un coridor (Shahed reactiv)](<https://github.com/simplews/drone-alerter>)** · altele · liber · istoric · ★★★☆☆  
  Proiect care citește canale de monitorizare și estimează sosirea dronelor reactive pe un coridor; a reconstituit timpi de 4–33 min pe episoade din oct. 2026.  
  *Integrare:* Model pentru coridorul Odesa/Vinnîțea → MD → Iași: dedup Δt≤5 min, contor de ținte, mesaje de „țintă pierdută”.  
  *Atenție:* Calibrat pentru Ivano-Frankivsk; necesită un gazetar nou.
- ✔ **[MAVO – avertizare transfrontalieră Polonia (air-alert-early-warning)](<https://mavo.org.pl/en>)** · API · liber · minute · ★★★☆☆ · flux: <https://mavo.org.pl/state.json>  
  Sistem open-source care traduce alertele ucrainene în avertizare pentru Polonia, cu „base-rate gate”; public din 2026-08-12, cu state.json.  
  *Integrare:* Model analog pentru Iași; citire https://mavo.org.pl/state.json ca referință a formatului.  
  *Atenție:* Pre-alpha; acoperă vestul Ucrainei/Polonia, nu RO.
- ✔ **[Типова Одеса (@odesa_typical)](<https://t.me/odesa_typical>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/odesa_typical>  
  Canal regional din Odesa, înregistrat ca „regional reporting” într-o hartă OSINT care se actualizează zilnic.  
  *Integrare:* Preview t.me/s/odesa_typical (folosit în pipeline-ul freeosintmaper); extragere de evenimente.  
  *Atenție:* Canal comunitar; postările despre explozii sunt rapide, dar neverificate.
- ~ **[Flanc Est – hartă OSINT a incidentelor pe flancul estic NATO](<https://github.com/FloC6635/Flanc-Est>)** · hartă · liber · zile · ★★★☆☆  
  Hartă francofonă cu incidente, activități militare și interceptări pe flancul estic; conține înregistrări pentru RO (de exemplu, Plauru, 2023) și MD.  
  *Integrare:* Extragere din index.html a obiectelor {d, z, type, lieu, lat, lng} pentru validarea istoricului RO/MD.  
  *Atenție:* Proiect personal; URL-ul GitHub Pages este neconfirmat, iar sursele per rând trebuie verificate. Verificare: Repo existent: un singur index.html („Suivi flanc est — mobile”, în franceză), cu date hard-codate despre RO/MD. Ultimul commit este din 9 aug 2026, deci nu acoperă incidentele din 8 sep și 31 oct. Publicarea pe GitHub Pages nu a fost confirmată.
- ~ **[Odesa – @oddesitmedia](<https://t.me/oddesitmedia>)** · Telegram · liber · minute · ★★★☆☆  
  Canal media din Odesa, folosit de SkyWatchUA cu regulă proprie de geocodare pentru regiunea Odesa.  
  *Integrare:* Ingestie Telethon/t.me/s; extragere localități + corelare cu alertele oficiale din oblastul Odesa.  
  *Atenție:* Neoficial; descriere dedusă din cod (clasificat „odeska”). Verificare: O singură sursă GitHub (skywatchua, mapat la Odesa). Activitatea neconfirmată – reverificați.
- ~ **[Odesa – canal local de știri (@xydessa_live)](<https://t.me/xydessa_live>)** · Telegram · liber · minute · ★★★☆☆  
  Canal din regiunea Odesa clasificat ca sursă „odeska” în SkyWatchUA; raportează explozii, drone și apărare antiaeriană locală.  
  *Integrare:* Telethon sau t.me/s; mapare automată pe regiunea Odesa; util pentru dronele care intră în Moldova dinspre sudul Basarabiei.  
  *Atenție:* Canal comunitar, neoficial; conținutul nu a fost citit direct, nu repostați locațiile apărării antiaeriene. Verificare: O singură sursă GitHub (skywatchua, mapat la regiunea Odesa). Canal neoficial; activitatea neconfirmată – reverificați.
- ~ **[Reni – canal local (@ReniHub)](<https://t.me/ReniHub>)** · Telegram · liber · minute · ★★★☆☆  
  Canal local din Reni (Odesa), oraș la Dunăre vizavi de Galați; util pentru dronele de pe culoarul Izmail–Reni de lângă granița cu RO și MD.  
  *Integrare:* Telethon/t.me/s; cuvinte-cheie „шахед”, „вибух”, „Рені”; corelare cu ADS-B și RO-Alert Galați/Tulcea.  
  *Atenție:* Inclus doar ca handle în configurația Puluj-g (încredere 0,6); conținutul nu a fost verificat. Verificare: O singură sursă GitHub (Puluj-g). Reni e la granița cu RM/Galați – util dacă există; activitatea neconfirmată, reverificați.
- ~ **[Russian Aggression Incident Log (russianaggression.com)](<https://russianaggression.com>)** · hartă · liber · zile · ★★★☆☆  
  Jurnal OSINT al incidentelor hibride rusești în statele NATO/UE (drone, GPS jamming, cabluri), inclusiv incursiunile cu drone din Delta Dunării (RO/MD); export CSV/JSON.  
  *Integrare:* Export periodic CSV/JSON pentru istoricul incidentelor RO/MD; comparare cu baza internă.  
  *Atenție:* Proprietar nedeclarat; brief-urile AI trebuie verificate; tratați-l ca sursă de piste. Verificare: Descris în OSINT Tools Library (gratuit, fără cont, export CSV/JSON, include incursiuni de drone RO/MD). Site-ul nu a putut fi accesat din sandbox. Proprietarul nu este declarat, iar rezumatele sunt generate de AI. Folosiți-l doar ca sursă de piste.
- ~ **[Shahed Radar (@shahedradar)](<https://t.me/shahedradar>)** · Telegram · liber · minute · ★★★☆☆  
  Canal dedicat urmăririi dronelor Shahed (după nume), listat ca sursă în configurația Puluj-g.  
  *Integrare:* Telethon/t.me/s; sursă suplimentară pentru votul multi-canal.  
  *Atenție:* Doar handle-ul este confirmat în cod; scopul și calitatea nu au fost verificate. Verificare: O singură sursă GitHub (Puluj-g). Activitatea neconfirmată – reverificați.
- ~ **[Sudul Ucrainei – @pivdenmedia](<https://t.me/pivdenmedia>)** · Telegram · liber · minute · ★★★☆☆  
  Canal media din sud (Odesa) inclus în lista de bază a SkyWatchUA pentru monitorizarea țintelor aeriene.  
  *Integrare:* Telethon/t.me/s; filtrare pe localitățile de lângă granița cu Moldova.  
  *Atenție:* Neoficial; conținut necitit direct. Verificare: O singură sursă GitHub (skywatchua, mapat la Odesa). Activitatea neconfirmată – reverificați.
- ~ **[Куди летить (@kudy_letyt)](<https://t.me/kudy_letyt>)** · Telegram · liber · minute · ★★★☆☆  
  Canal național „încotro zboară” cu direcțiile țintelor; folosit în drone-alerter și SkyWatchUA (listă extinsă).  
  *Integrare:* Telethon/t.me/s; agregare cu Monitor și єРадар pentru vot multi-sursă.  
  *Atenție:* Neoficial; încredere 0,6 în Puluj-g. Verificare: Prezent în patru proiecte (drone-alerter PRD, skywatchua, vartovyi_tryvog, Puluj-g). Canal neoficial; activitatea curentă neconfirmată.
- ~ **[Миколаївський Ванёк (@vanek_nikolaev)](<https://t.me/vanek_nikolaev>)** · Telegram · liber · minute · ★★★☆☆  
  Canal popular de monitorizare din sud (Mykolaiv), prezent în listele mai multor proiecte de alertare și detecție a amenințărilor aeriene.  
  *Integrare:* Telethon/t.me/s; util pentru dronele care intră dinspre Marea Neagră spre Odesa/Mykolaiv înainte de a coti spre vest.  
  *Atenție:* Neoficial, stil informal; uneori ironizează, deci filtrați. Conținutul nu a fost citit direct. Verificare: Prezent în trei proiecte independente (AirThreatAI, vartovyi_tryvog, Puluj-g). Canal neoficial; activitatea curentă neconfirmată din sandbox.
- ~ **[Стратегічна авіація – monitorizarea aviației strategice ruse (@StrategicaviationT)](<https://t.me/StrategicaviationT>)** · Telegram · liber · minute · ★★★☆☆  
  Canal care urmărește decolările Tu-95/Tu-160/Tu-22M3 și MiG-31K, ceea ce anunță cu ore înainte valurile de rachete de croazieră care pot survola Moldova.  
  *Integrare:* Ingestie t.me/s sau Telethon; alertă internă de nivel „pre-atac” când apar cuvintele-cheie despre decolări sau lansări.  
  *Atenție:* Neoficial (încredere 0,8 în Puluj-g); descrierea reiese din numele canalului și din configurațiile de proiect, conținutul nu a fost citit direct. Verificare: Handle prezent în două proiecte independente (Puluj-g: „Стратегічна авіація”, trust 0.8; skywatchua). Activitatea curentă neconfirmată; t.me inaccesibil din sandbox.
- ✔ **[arXiv 2411.14625 – predicția alertelor aeriene din Ucraina](<https://arxiv.org/abs/2411.14625>)** · PDF · liber · istoric · ★★☆☆☆  
  Lucrare despre prognoza alertelor: vecinătatea regiunilor e cel mai important predictor; autorii au rulat și un canal Telegram de predicție pe baza canalelor de monitorizare.  
  *Integrare:* Referință metodologică pentru modelul de predicție.  
  *Atenție:* Rezumat văzut indirect (notă de cercetare GitHub), nu articolul complet.
- ✔ **[awesome-drone-warfare-osint – set de date despre războiul dronelor](<https://github.com/cognis-digital/awesome-drone-warfare-osint>)** · set de date · liber · zile · ★★☆☆☆  
  Catalog și CSV-uri (incidente, drone, componente, producători) cu URL-urile surselor primare, plus scrapere CAR și GUR.  
  *Integrare:* Import CSV pentru fișe de tip dronă (Geran/Gerbera) și surse; livesearch.py pentru feed-uri.  
  *Atenție:* Agregat comunitar; verificați fiecare rând la sursa citată.
- ✔ **[DeepState – canal Telegram (@DeepStateUA)](<https://t.me/DeepStateUA>)** · Telegram · liber · ore · ★★☆☆☆ · flux: <https://t.me/s/DeepStateUA>  
  Canalul proiectului DeepState (OSINT ucrainean): actualizări de front, uneori și despre loviturile aeriene.  
  *Integrare:* t.me/s/DeepStateUA în pipeline (folosit de freeosintmaper/osint-map).  
  *Atenție:* Pro-ucrainean; amână publicarea avansurilor UA din motive de securitate operațională.
- ✔ **[GUR War & Sanctions – componente străine în armele rusești (Geran-2/Shahed)](<https://war-sanctions.gur.gov.ua/en/components>)** · web · liber · zile · ★★☆☆☆  
  Portal oficial al serviciului de informații militare ucrainean (HUR): aproape 6.000 de componente cu poze, filtrabile după armă (inclusiv UAV Geran-2).  
  *Integrare:* Referință pentru identificarea resturilor după un incident; navigare pe /components/weapon.  
  *Atenție:* Nu are export CSV/JSON (scraping doar cu respectarea robots.txt); sursă oficială a unei părți combatante.
- ✔ **[ISW – Russian Offensive Campaign Assessment (index zilnic)](<https://understandingwar.org/analysis/russia-ukraine/russian-offensive-campaign-assessment/>)** · web · liber · zile · ★★☆☆☆  
  Evaluări zilnice ISW care rezumă și loviturile cu drone și rachete raportate de Ucraina.  
  *Integrare:* Scraping al indexului (200 confirmat de alt proiect); extragere NLP a cifrelor Shahed/Gerbera.  
  *Atenție:* „All rights reserved”: doar uz intern. Feed RSS neconfirmat (/feed/, /rss.xml și /feeds/all.xml apar doar în liste de probe).
- ✔ **[Militarnyi (militarnyi.com, fost mil.in.ua)](<https://militarnyi.com/en/>)** · RSS · liber · ore · ★★☆☆☆ · flux: <https://mil.in.ua/en/news/feed/>  
  Publicație ucraineană de apărare: știri despre loviturile cu Shahed, extinderea locurilor de lansare și noile tipuri de drone.  
  *Integrare:* RSS ingerat în pipeline; filtrare pe „Shahed”, „Geran”, „Moldova”, „Romania”.  
  *Atenție:* Domeniul a migrat la militarnyi.com, iar feedul mil.in.ua poate redirecționa. Media pro-ucraineană.
- ✔ **[Ministerul Apărării al Regatului Unit – feed Atom (Defence Intelligence)](<https://www.gov.uk/government/organisations/ministry-of-defence>)** · RSS · liber · zile · ★★☆☆☆ · flux: <https://www.gov.uk/government/organisations/ministry-of-defence.atom>  
  Feed Atom oficial al MoD UK; include actualizările de informații despre Ucraina.  
  *Integrare:* Ingestie Atom; filtrare pe „Ukraine”, „Shahed”, „drone”.  
  *Atenție:* Feed general al ministerului; necesită filtrare.
- ✔ **[Open Source Munitions Portal (OSMP)](<https://osmp.ngo>)** · web · liber · istoric · ★★☆☆☆  
  Bibliotecă de peste 1.000 de imagini verificate de muniții folosite, cu model, ghidaj și marcaje.  
  *Integrare:* Comparare vizuală a fotografiilor de resturi după incident (confirmare tip Shahed/Gerbera/rachetă).  
  *Atenție:* Nu vă apropiați de muniții; doar uz de referință.
- ✔ **[Puluj-g – registru de surse cu niveluri de încredere](<https://github.com/sql-monk/Puluj-g>)** · altele · liber · istoric · ★★☆☆☆  
  Configurație JSON cu peste 70 de surse (API alerts.in.ua, canale oficiale și de monitorizare) cu trustLevel, prioritate și interval de interogare.  
  *Integrare:* Model de ponderare a surselor în veghe (oficial 0,9–0,95; monitorizare 0,6–0,85).  
  *Atenție:* Handle-urile sunt listate, nu validate; pentru unele canale lipsește descrierea.
- ✔ **[The War Zone (TWZ)](<https://www.twz.com>)** · RSS · liber · ore · ★★☆☆☆ · flux: <https://www.twz.com/feed>  
  Publicație de apărare cu analize tehnice („drone forensics”) despre Shahed, Gerbera și incursiunile în NATO.  
  *Integrare:* RSS (folosit în producție de worldmonitor); filtrare pe Romania/Moldova/Shahed.  
  *Atenție:* Media SUA; viteză mai mică decât canalele UA.
- ✔ **[VIINA 2.0 – evenimente violente din știri (zhukovyuri)](<https://github.com/zhukovyuri/VIINA>)** · set de date · liber · zile · ★★☆☆☆  
  Sistem cvasi-în-timp-real de evenimente geocodate (UA și RU) clasificate prin ML, inclusiv lovituri aeriene; actualizat zilnic, licență ODbL.  
  *Integrare:* Descărcare ZIP-uri zilnice din GitHub; baseline de intensitate pentru oblasturile Odesa, Vinnîțea și Cernăuți.  
  *Atenție:* Clasificarea automată poate greși; sursele includ media rusă.
- ~ **[CAT-UXO – referințe muniții neexplodate](<https://www.cat-uxo.com>)** · web · liber · istoric · ★★☆☆☆  
  Bază de referință pentru muniții și explozivi, inclusiv date despre UCAV.  
  *Integrare:* Fișe pentru instruirea internă privind siguranța la resturi.  
  *Atenție:* Referință, nu sursă de evenimente. Verificare: Site activ în sept. 2025 conform Bellingcat Toolkit (are și membership plătit), dar lista simonhuwiler îl trece la „not maintained anymore”. Folosiți-l ca referință; OSMP e alternativa.
- ~ **[CEPA – Center for European Policy Analysis](<https://cepa.org>)** · web · liber · zile · ★★☆☆☆  
  Think-tank transatlantic cu analize despre flancul estic și despre componentele occidentale din dronele rusești.  
  *Integrare:* Monitorizare manuală sau Google News site:cepa.org.  
  *Atenție:* Feed neconfirmat. Verificare: Think tank real, citat în lista din 2026. Activitatea curentă n-a fost confirmată direct; feed neconfirmat. Relevanță de fundal.
- ~ **[CIT – Conflict Intelligence Team](<https://citeam.org>)** · web · liber · zile · ★★☆☆☆  
  Grup de investigații independent (fondat de ruși) care urmărește unitățile și operațiunile militare rusești.  
  *Integrare:* Monitorizare; feed citeam.org/feed/ neconfirmat (apare doar într-o listă RSS terță).  
  *Atenție:* Volum variabil; feed neverificat. Verificare: Există (echipă de investigații rusă din exil, nu pro-Kremlin). Activitatea curentă e neconfirmată. Feed-ul citeam.org/feed/ apare într-un scraper terț, dar e neconfirmat.
- ~ **[Conflict Armament Research (CAR)](<https://www.conflictarm.com>)** · PDF · liber · zile · ★★☆☆☆  
  ONG de criminalistică a armamentului; rapoarte de teren despre componentele dronelor și rachetelor rusești/iraniene.  
  *Integrare:* Bibliotecă de referință pentru analiza resturilor de Shahed/Gerbera găsite în RO/MD.  
  *Atenție:* Rapoarte PDF ocazionale, fără API. Verificare: Organizație reală, citată într-o listă din 2026. Activitatea curentă n-a fost confirmată direct. Rapoarte PDF de analiză tehnică a resturilor; util post-incident.
- ~ **[Defense Express](<https://en.defence-ua.com>)** · web · liber · ore · ★★☆☆☆  
  Publicație ucraineană de analiză militară, cu articole tehnice despre Geran-2/3 și dronele-momeală Gerbera.  
  *Integrare:* Monitorizare; RSS en.defence-ua.com/rss.xml neconfirmat (apare doar într-o listă de probe).  
  *Atenție:* Feed neconfirmat; media pro-ucraineană. Verificare: Site cunoscut, citat de presă în 2025. Activitatea curentă n-a fost confirmată direct. en.defence-ua.com/rss.xml apare doar într-o listă de test, deci feed neconfirmat.
- ~ **[Eyes on Russia (Centre for Information Resilience)](<https://eyesonrussia.org>)** · hartă · liber · zile · ★★☆☆☆  
  Hartă CIR cu atacuri și incidente verificate, cu marcaj de verificare.  
  *Integrare:* Extragere cu get_ceninfores_data (osint-geo-extractor); analiză post-incident.  
  *Atenție:* Datele brute sunt accesibile doar „dacă știi cum”; lag mare. Verificare: Există (hartă CIR). Activitatea curentă e neconfirmată. Datele brute se pot obține doar indirect (marcaj „🟠” în lista simonhuwiler).
- ~ **[GeoConfirmed – Ukraine](<https://geoconfirmed.org/map/ukraine>)** · hartă · liber · ore · ★★☆☆☆  
  Hartă de incidente geolocalizate din clipuri video (inclusiv lovituri cu drone), cu date brute disponibile.  
  *Integrare:* Descărcare prin osint-geo-extractor (get_geoconfirmed_data); confirmarea locului impactului după incident.  
  *Atenție:* Lag de ore/zile; verificați licența și sursa originală. Verificare: Există. Harta Ucrainei are URL dedicat. Activitatea curentă e neconfirmată, iar API/feed-ul e neconfirmat. Vechiul endpoint geoconfirmed.azurewebsites.net (folosit de osint-geo-extractor) e probabil depășit.
- ~ **[Ministerul Apărării al Rusiei – Telegram (@mod_russia / @mod_russia_en)](<https://t.me/mod_russia>)** · Telegram · liber · ore · ★★☆☆☆  
  Comunicatele oficiale ruse despre „lovituri masive” cu Geran și rachete; utile pentru a data valurile de atac.  
  *Integrare:* Doar context: t.me/s de citit cu filtrare; nu declanșează alerte.  
  *Atenție:* Context, credibilitate scăzută / propagandă. Afirmațiile nu sunt verificabile; nu redistribuiți. Verificare: Canalul oficial al MApN rus (există și @mod_russia_en). Doar ca context, credibilitate scăzută / propagandă. Activitatea curentă nu a fost confirmată direct.
- ~ **[Molfar Intelligence Institute – analize despre Alabuga și locurile de lansare](<https://www.molfar.institute/en/>)** · web · liber · zile · ★★☆☆☆  
  Agenție OSINT ucraineană; a analizat documente din Alabuga despre locurile de lansare a Shahed-urilor.  
  *Integrare:* Lectură analitică pentru harta zonelor de lansare (direcție probabilă spre Odesa/MD).  
  *Atenție:* Analize punctuale, fără feed. Verificare: Există. Analiza documentelor de la Alabuga despre locurile de lansare Shahed e citată în note de cercetare din 2026. Pagina relevantă: /en/orlando-milan-shanghai-where-do-russians-launch-shahed-drones-from-molfar-intelligence-institute-analyzes-secret-documents-from-alabuga/. Activitatea curentă n-a fost confirmată direct.
- ~ **[osint-geo-extractor (PyPI) – agregator de baze OSINT geolocalizate](<https://github.com/conflict-investigations/osint-geo-extractor>)** · API · liber · zile · ★★☆☆☆  
  Bibliotecă Python care descarcă și normalizează evenimente din Bellingcat, CIR, DefMon3, GeoConfirmed și Texty.  
  *Integrare:* pip install osint-geo-extractor; job zilnic care încarcă evenimentele într-o bază PostGIS internă.  
  *Atenție:* Unele surse pot fi oprite sau și-au schimbat formatul; verificați întreținerea repo-ului. Verificare: Biblioteca există pe PyPI, dar ultima versiune e 0.0.12 din 11.01.2024, deci pare nemenținută. Unele surse pe care le citește (GeoConfirmed azurewebsites, Texty) pot fi schimbate sau înghețate.
- ~ **[SkyWatchUA – agregator Telegram → hartă](<https://github.com/novacrafteam/skywatchua>)** · altele · liber · istoric · ★★☆☆☆  
  Server open-source care citește canale oficiale și de monitorizare, le geocodează pe regiuni (inclusiv Odesa) și le afișează pe hartă.  
  *Integrare:* Reutilizarea listelor de canale și a regulilor de geocodare (telegram.js, transform.js).  
  *Atenție:* Repo mare (circa 288 MB); pot exista fișiere .env în repo, nu le folosiți. Verificare: Codul există (v2.1.0, cu presetări de canale Telegram și RSS), dar repo-ul nu are README și este inactiv din 20 apr 2026. Folosește o sesiune gramjs pe cont propriu, doar în citire pe canale publice, ceea ce este acceptabil. Util ca listă de canale.
- ✔ **[cyterat/deepstate-map-data – istoric GeoJSON zilnic](<https://github.com/cyterat/deepstate-map-data>)** · set de date · liber · zile · ★☆☆☆☆  
  Oglindă GitHub actualizată zilnic (03:00 UTC) a teritoriului ocupat după DeepState, cu fișier unificat .geojson.gz din 2024-07-08.  
  *Integrare:* Clonare/raw GitHub; analize istorice ale frontului pentru context.  
  *Atenție:* Date derivate din DeepState; geometriile se suprapun de la o zi la alta, deci filtrați după dată.
- ✔ **[DeepStateMap – API public (GeoJSON)](<https://deepstatemap.live>)** · API · liber · ore · ★☆☆☆☆ · flux: <https://deepstatemap.live/api/history/last>  
  Hartă ucraineană a liniei frontului; endpoint-ul /api/history/last întoarce GeoJSON fără autentificare.  
  *Integrare:* Poll zilnic /api/history/last pentru context (de exemplu, schimbări în zonele de lansare de lângă front).  
  *Atenție:* Nu există licență publicată; atribuiți „© DeepStateMap.Live”. Nu e relevant pentru dronele cu rază lungă.
- ✔ **[Hărți de distrugeri din Ucraina (prs-eth, ETH Zürich) – Zenodo 14811504](<https://zenodo.org/records/14811504>)** · set de date · liber · istoric · ★☆☆☆☆  
  Set academic (Sentinel-1 + UNOSAT + Overture) cu clădiri avariate pe unități administrative, 2022–2024; cod MIT.  
  *Integrare:* Descărcare GeoJSON pentru analize istorice.  
  *Atenție:* Fișiere foarte mari (până la 17,9 GB); nu acoperă RO/MD.
- ✔ **[International Crisis Group – CrisisWatch](<https://www.crisisgroup.org>)** · RSS · liber · zile · ★☆☆☆☆ · flux: <https://www.crisisgroup.org/rss>  
  Monitor lunar al conflictelor (inclusiv Ucraina și Moldova/Transnistria) și analize.  
  *Integrare:* RSS pentru context regional.  
  *Atenție:* Ritm lunar, foarte general.
- ✔ **[Oryx – documentarea pierderilor de echipament](<https://www.oryxspioenkop.com>)** · RSS · liber · zile · ★☆☆☆☆ · flux: <https://www.oryxspioenkop.com/feeds/posts/default?alt=rss>  
  Blog OSINT care documentează vizual pierderile de echipament (inclusiv drone și sisteme de apărare antiaeriană).  
  *Integrare:* RSS Blogger (folosit în producție de worldmonitor) pentru context.  
  *Atenție:* Doar pierderi confirmate foto; nu e despre incursiuni.
- ✔ **[PetroIvaniuk/2022-Ukraine-Russia-War-Dataset – pierderi zilnice](<https://github.com/PetroIvaniuk/2022-Ukraine-Russia-War-Dataset>)** · set de date · liber · zile · ★☆☆☆☆  
  CSV/JSON zilnic cu pierderile rusești raportate de Statul Major UA (inclusiv UAV și rachete de croazieră doborâte).  
  *Integrare:* Raw GitHub (russia_losses_equipment/personnel.json) pentru serii de timp.  
  *Atenție:* Cifre oficiale ale unei părți combatante; nu e despre traiectorii.
- ✔ **[Rybar (@rybar)](<https://t.me/rybar>)** · Telegram · liber · ore · ★☆☆☆☆ · flux: <https://t.me/s/rybar>  
  Canal militar pro-Kremlin cu hărți și comentarii, uneori despre rutele Geran.  
  *Integrare:* Doar context; t.me/s/rybar (folosit într-un pipeline OSINT).  
  *Atenție:* Context, credibilitate scăzută / propagandă; dezinformare frecventă.
- ✔ **[The Economist – modelul „war fire” (FIRMS) + Zenodo/Kaggle](<https://github.com/TheEconomist/the-economist-war-fire-model>)** · set de date · liber · zile · ★☆☆☆☆ · flux: <https://raw.githubusercontent.com/TheEconomist/the-economist-war-fire-model/master/output-data/ukraine_war_fires.csv>  
  Clasificarea zilnică a detecțiilor de incendiu FIRMS din Ucraina ca „legate de război”; date CC BY 4.0, actualizate zilnic.  
  *Integrare:* CSV output-data/ukraine_war_fires.csv; context pentru impacturi (fără RO/MD).  
  *Atenție:* Probabilistic; norii ascund evenimente. Oglinzi: Zenodo 17151723, Kaggle joebeachcapital.
- ✔ **[War on the Rocks](<https://warontherocks.com>)** · RSS · liber · zile · ★☆☆☆☆ · flux: <https://warontherocks.com/feed/>  
  Analize de securitate și apărare (inclusiv războiul dronelor și apărarea antiaeriană pe flancul estic).  
  *Integrare:* RSS pentru lecturi de fond.  
  *Atenție:* Context, nu evenimente.
- ✔ **[WarSpotting – pierderi geolocalizate](<https://ukr.warspotting.net>)** · set de date · liber · zile · ★☆☆☆☆  
  Bază de pierderi de echipament verificate și geolocalizate, folosită de scrapere și hărți hexbin.  
  *Integrare:* Scraper (de exemplu, lazar-bit/warspotting-loss-scraper) pentru analize istorice.  
  *Atenție:* Context general; API-ul nu a fost verificat.
- ✔ **[Два майора (@dva_majors)](<https://t.me/dva_majors>)** · Telegram · liber · ore · ★☆☆☆☆ · flux: <https://t.me/s/dva_majors>  
  Canal „voenkor” pro-Kremlin; comentarii despre atacurile cu drone.  
  *Integrare:* Doar context; t.me/s/dva_majors.  
  *Atenție:* Context, credibilitate scăzută / propagandă.
- ~ **[Bellingcat – harta pagubelor civile din Ucraina (TimeMap JSON)](<https://ukraine.bellingcat.com>)** · set de date · liber · istoric · ★☆☆☆☆ · flux: <https://bellingcat-embeds.ams3.cdn.digitaloceanspaces.com/production/ukr/timemap/api.json>  
  Bază de incidente cu civili afectați, cu câmp weapon_system; aprox. 2.517 incidente, până în iulie 2025.  
  *Integrare:* Descărcare api.json (fără credențiale) pentru statistici istorice despre tipurile de armă.  
  *Atenție:* Actualizarea pare oprită în 2025-07; date despre victime: tratați cu grijă. Verificare: Endpoint-ul JSON funcționa în oct. 2026, dar datele se opresc la 2025-07-09 (arhivă, nu flux curent). Fără licență explicită. Coordonatele sunt difuzate la ±150 m. Bun doar pentru analiză istorică.
- ~ **[Critical Threats Project (AEI)](<https://www.criticalthreats.org>)** · web · liber · zile · ★☆☆☆☆  
  Proiect afiliat ISW cu analize despre Rusia și Iran, inclusiv despre lanțul de producție al dronelor Shahed.  
  *Integrare:* Monitorizare manuală; feed /feed neconfirmat (apare doar într-o listă de probe).  
  *Atenție:* Context strategic; nu oferă avertizare timpurie. Verificare: Există (6 articole Wikipedia îl citează). Activitatea curentă n-a fost confirmată direct. Se concentrează în principal pe Iran/Orientul Mijlociu, cu Rusia prin ISW, deci relevanță mică. Se aplică probabil aceeași politică restrictivă ca la ISW.
- ~ **[CSIS Beyond Parallel – imagini satelitare Alabuga](<https://beyondparallel.csis.org>)** · web · liber · istoric · ★☆☆☆☆  
  Subproiect CSIS cu analize de imagini satelitare (de exemplu, fabrica de Shahed de la Alabuga).  
  *Integrare:* Context despre capacitatea de producție și ritmul atacurilor.  
  *Atenție:* Nu dă avertizare timpurie. Verificare: Site-ul există, dar Beyond Parallel e axat pe Coreea (transferuri RPDC–Rusia). Afirmația despre imagini Alabuga vine doar din lista cognis și e neconfirmată. Relevanță foarte mică.
- ~ **[IISS – urmărirea componentelor rachetelor și UAV-urilor rusești](<https://www.iiss.org/globalassets/media-library---content--migration/files/research-papers/2025/09/pub25-094-tracking-the-components-of-missiles-and-uavs-used-by-russia-in-ukraine.pdf>)** · PDF · liber · istoric · ★☆☆☆☆  
  Lucrare IISS (2025) despre componentele rachetelor și UAV-urilor folosite de Rusia în Ucraina; plus Military Balance.  
  *Integrare:* Context tehnic; feed iiss.org/rss neconfirmat.  
  *Atenție:* Unele produse sunt plătite. Verificare: URL-ul rădăcină e prea generic. Raportul relevant e PDF-ul IISS din sept. 2025 (preluat din lista cognis, neverificat direct). Feed-ul iiss.org/rss dintr-un scraper terț e neconfirmat.
- ~ **[InformNapalm – baza de date despre agresiunea rusă + Telegram](<https://informnapalm.org/db/russian-aggression/>)** · web · liber · zile · ★☆☆☆☆ · flux: <https://t.me/s/informnapalm>  
  Comunitate OSINT de voluntari cu peste 2.000 de investigații și o bază interactivă de unități rusești; canal Telegram public.  
  *Integrare:* t.me/s/informnapalm pentru noutăți; bază pentru identificarea unităților care operează Shahed.  
  *Atenție:* Pro-ucrainean; verificați independent. Verificare: Baza de date și canalul Telegram apar în liste OSINT (canalul e „enabled” în registrul freeosintmaper). Activitatea curentă n-a fost confirmată direct (fetch blocat).
- ~ **[KSE Institute – componente străine în dronele militare rusești](<https://kse.ua/about-the-school/news/foreign-components-in-russian-military-drones/>)** · web · liber · istoric · ★☆☆☆☆  
  Analiză KSE a 174 de componente străine din dronele rusești.  
  *Integrare:* Context tehnic pentru identificarea resturilor.  
  *Atenție:* Studiu punctual. Verificare: Articolul e citat în liste din 2026. Nici alt proiect nu a putut accesa direct kse.ua (proxy blocat). Relevanță de fundal.
- ~ **[Lostarmour.info (RU)](<https://lostarmour.info>)** · web · liber · zile · ★☆☆☆☆  
  Bază de date rusă de pierderi și lovituri (taguri „strikes”, Lancet etc.).  
  *Integrare:* Doar context istoric, lectură manuală.  
  *Atenție:* Context, credibilitate scăzută / propagandă. Verificare: Site pro-rus cu pierderi de echipamente și lovituri (Lancet etc.). Doar ca context, credibilitate scăzută / propagandă. Relevanță foarte mică pentru Iași.
- ~ **[MilitaryLand.net](<https://militaryland.net>)** · web · liber · zile · ★☆☆☆☆  
  Site OSINT cu hărți și analize ale războiului și ordinul de luptă al unităților.  
  *Integrare:* Monitorizare manuală pentru context; fără API cunoscut.  
  *Atenție:* Context general, nu despre drone; feed neconfirmat. Verificare: Există și e citat de Wikipedia (recensământ din oct. 2026), dar n-am putut confirma activitatea curentă. Hărți și ORBAT, relevanță scăzută pentru Iași.
- ~ **[OSW – Centre for Eastern Studies (Varșovia)](<https://www.osw.waw.pl/en>)** · web · liber · zile · ★☆☆☆☆  
  Institut polonez de analiză a Rusiei, Ucrainei și regiunii (inclusiv a livrărilor de armament către Ucraina).  
  *Integrare:* Lectură de fond; feed neconfirmat.  
  *Atenție:* Context. Verificare: Există; pagina armsdeliveries e listată ca sursă de date. Activitatea curentă n-a fost confirmată direct; feed neconfirmat.
- ~ **[PNAS 2023 – „Public response to government alerts saves lives during Russian invasion of Ukraine”](<https://doi.org/10.1073/pnas.2220160120>)** · PDF · liber · istoric · ★☆☆☆☆  
  Studiu (Van Dijcke, Wright, Polyak) pe peste 3.000 de alerte și 17 milioane de dispozitive: oboseala de alertă reduce reacția; se estimează 35–45% victime evitate.  
  *Integrare:* Argument pentru calibrarea pragurilor și evitarea alertelor false în grupul intern.  
  *Atenție:* Comportamental, nu predictiv. Verificare: Articol real (Van Dijcke, Wright & Polyak, PNAS 2023) despre reacția publicului la alerte și oboseala de alertă. PDF-ul de pe harris.uchicago.edu nu a putut fi verificat. DOI-ul este dedus din numele fișierului. Relevanță: fundal pentru designul alertelor.
- ~ **[RUSI – Royal United Services Institute](<https://www.rusi.org>)** · web · liber · zile · ★☆☆☆☆ · flux: <https://news.google.com/rss/search?q=site:rusi.org+when:7d&hl=en-US&gl=US&ceid=US:en>  
  Think-tank britanic; studii despre UAV-urile rusești (de exemplu, „The Orlan Complex”) și apărarea antiaeriană.  
  *Integrare:* Feed nativ rusi.org/explore-our-research/rss.xml neconfirmat; alternativ, Google News RSS cu site:rusi.org (folosit de worldmonitor).  
  *Atenție:* Feed nativ neconfirmat. Verificare: Există. Nu am confirmat un RSS nativ; worldmonitor folosește în schimb Google News RSS cu site:rusi.org. Calea rusi.org/explore-our-research/rss.xml dintr-un scraper terț e neconfirmată.
- ~ **[russianwarship.rip – API de statistici zilnice](<https://russianwarship.rip>)** · API · liber · zile · ★☆☆☆☆ · flux: <https://russianwarship.rip/api/v2/statistics/latest>  
  API JSON cu statistica zilnică a pierderilor raportate de Statul Major UA (folosit de mai mulți boți).  
  *Integrare:* GET /api/v2/statistics/latest; serie istorică pentru UAV doborâte.  
  *Atenție:* Neoficial (agregator); cifrele oficiale nu pot fi verificate independent. Verificare: API-ul e menționat de proiecte terțe, dar activitatea curentă și endpoint-ul v2 nu au putut fi confirmate (fetch blocat). Redundant cu #279, aceleași cifre ale Statului Major.
- ~ **[TASS – RSS](<https://tass.com>)** · RSS · liber · ore · ★☆☆☆☆ · flux: <https://tass.com/rss/v2.xml>  
  Agenția de stat rusă; poziții oficiale după incidentele din RO/MD.  
  *Integrare:* RSS filtrat pe Romania/Moldova pentru narativele oficiale ruse.  
  *Atenție:* Context, credibilitate scăzută / propagandă (presă de stat). Verificare: Media de stat rusă: doar ca context, credibilitate scăzută / propagandă. Feed-ul RSS nu a fost testat direct.
- ~ **[Texty.org.ua – „Under attack” și analize despre Shahed](<https://texty.org.ua/projects/107577/under-attack-what-and-when-russia-shelled-ukraine/>)** · set de date · liber · istoric · ★☆☆☆☆  
  Proiect de date al Texty despre bombardamentele rusești, plus analize despre ciclul atacurilor cu Shahed reactive.  
  *Integrare:* get_texty_data (osint-geo-extractor); referință pentru vizualizarea rutelor.  
  *Atenție:* Focalizat pe Kiev și Ucraina; nu acoperă RO/MD. Verificare: Texty e activ (articol din 24.09.2026 despre rutele Shahed cu reacție, cu hărți de rute pentru Kiev). Nu am confirmat că proiectul „Under attack” mai e actualizat. Pentru Shahed, articolul din 2026 e mai util.
- ~ **[Ukrainian Arms Monitor (Substack)](<https://ukrainesarmsmonitor.substack.com>)** · RSS · liber · zile · ★☆☆☆☆  
  Newsletter despre armamentul și dronele din războiul din Ucraina.  
  *Integrare:* Feed Substack standard (/feed), neconfirmat.  
  *Atenție:* Autor independent; verificați afirmațiile. Verificare: Substack-ul există (postări citate). Feed neconfirmat: modelul standard Substack ar fi /feed, dar nu l-am accesat.

## Senzori, meteo, infrastructură

- ✔ **[INFP (NIEP) – rețeaua seismică națională, servicii FDSN](<https://eida-sc3.infp.ro>)** · API · necunoscut · minute · ★★★☆☆  
  Rețeaua seismică a României (INFP Măgurele), cu stații și în Moldova; servicii FDSN pentru evenimente, stații și forme de undă (cod ObsPy „NIEP”).  
  *Integrare:* ObsPy Client('NIEP'): inventar fdsnws/station pentru stațiile din NE; după un impact raportat extrageți formele de undă ±5 min și căutați semnal impulsiv; doar confirmare post-incident. Cale standard FDSN (neverificată direct): https://eida-sc3.infp.ro/fdsnws/<serviciu>/1/query.  
  *Atenție:* O explozie de focos se vede doar pe stații la câțiva–zeci de km; nu e detector de drone. Catalogul nu listează explozii; accesul la forme de undă poate fi restricționat.
- ✔ **[rsudp – stație proprie Raspberry Shake / Raspberry Boom (infrasunet) cu alertă Telegram](<https://github.com/raspishake/rsudp>)** · senzori · liber · timp real · ★★★☆☆  
  Software open-source pentru seismograf personal Raspberry Shake sau senzor de presiune Raspberry Boom: detecție STA/LTA locală, alertă sonoră, mesaj Telegram.  
  *Integrare:* Stație pe o clădire parteneră la E de Iași; modulele Alert + Telegrammer trimit în grupul intern; marcajul de timp ajută la corelarea cu rapoarte de explozii/căderi.  
  *Atenție:* Hardware cumpărat (câteva sute €); declanșări false (trafic, tunete); că infrasunetul unei drone în zbor ar fi detectabil nu e demonstrat – util doar pentru explozii apropiate.
- ✔ **[AIS-catcher – receptor AIS propriu + rețeaua aiscatcher.org](<https://www.aiscatcher.org>)** · senzori · liber · timp real · ★★☆☆☆  
  Decodor AIS open-source pentru un receptor SDR propriu, cu hartă locală, ieșiri JSON/UDP și schimb de date cu aiscatcher.org.  
  *Integrare:* Receptor RTL-SDR lângă Galați sau pe Prut (trafic spre Reni, Izmail, Giurgiulești); JSON → veghe; plecări în grup sau ancorări bruște = context pentru atacuri asupra porturilor dunărene.  
  *Atenție:* Raza VHF ~20–40 km; AIS poate fi oprit sau falsificat; nu republicați pozițiile navelor; folosiți docker-shipfeeder pentru a alimenta mai multe rețele.
- ✔ **[Batear – detector acustic open-source (ESP32-S3)](<https://github.com/batear-io/batear>)** · senzori · liber · timp real · ★★☆☆☆  
  Detector acustic de drone foarte ieftin, cu procesare pe nod, pe ESP32-S3 + microfon MEMS; alertă criptată prin LoRa sau Ethernet/PoE.  
  *Integrare:* Prototip pentru noduri pilot la E/NE de Iași; detecția (oră, scor) → MQTT/HTTP → veghe; fără audio brut.  
  *Atenție:* Testat doar pe înregistrări; README-ul folosește 915 MHz – în UE e nevoie de 868 MHz; clasificatorul nu e antrenat pe Geran/Shahed; nu stocați audio (Cod penal art. 226).
- ✔ **[DWD Open Data (MOSMIX, observații, avertizări)](<https://www.dwd.de/DE/leistungen/opendata/opendata.html>)** · set de date · liber · ore · ★★☆☆☆ · flux: <https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/>  
  Serverul de date deschise al serviciului meteo german: prognoze MOSMIX pe stații, observații, radar și avertizări (ultimele două doar pentru Germania).  
  *Integrare:* Prin biblioteca wetterdienst sau API-ul JSON Bright Sky (api.brightsky.dev); de verificat dacă MOSMIX are puncte la Iași/Chișinău/Suceava. Modelul ICON-EU – neconfirmat în această sesiune.  
  *Atenție:* Radarul și avertizările DWD acoperă doar Germania; acoperirea MOSMIX în regiune trebuie verificată.
- ✔ **[ECMWF Open Data (IFS/AIFS)](<https://www.ecmwf.int/en/forecasts/datasets/open-data>)** · set de date · liber · ore · ★★☆☆☆ · flux: <https://data.ecmwf.int/forecasts/>  
  Prognoze deschise IFS și AIFS (0,25°, CC BY 4.0): vânt pe niveluri de presiune, temperatură, precipitații; oglinzi AWS/Google/Azure.  
  *Integrare:* Pachetul ecmwf-opendata: vântul la 925–700 hPa pe culoarul Odesa–Prut–Iași, pentru viteza la sol și deriva dronelor; strat de context în panou.  
  *Atenție:* Rezoluție grosieră; limită de 500 de conexiuni simultane – folosiți oglinzile cloud; vântul nu prezice traseul.
- ✔ **[EMSC – Seismic Portal, serviciu FDSN event](<https://www.seismicportal.eu>)** · API · liber · minute · ★★☆☆☆  
  Catalogul euro-mediteranean de cutremure, actualizat în minute; interogare FDSN (JSON/QuakeML).  
  *Integrare:* Interogare la 1–2 min pe bbox RO/MD/UA; un eveniment mic, superficial, neașteptat lângă ora unui impact raportat = indiciu de corelat. Fluxul websocket și LastQuake (mărturii) – neconfirmate aici. Cale standard FDSN (neverificată direct): https://www.seismicportal.eu/fdsnws/<serviciu>/1/query.  
  *Atenție:* Exploziile sunt rar catalogate; nu confundați cu cutremurele din Vrancea (adâncime 60–200 km).
- ✔ **[ENTSO-E Transparency Platform – REST API](<https://transparency.entsoe.eu>)** · API · cheie gratuită · ore · ★★☆☆☆ · flux: <https://web-api.tp.entsoe.eu/api>  
  Date oficiale ale operatorilor de transport: consum, producție, fluxuri transfrontaliere și indisponibilități pentru RO (10YRO-TEL------P), MD (10Y1001A1001A990), UA (10Y1001C--00003F).  
  *Integrare:* entsoe-py: urmăriți indisponibilitățile neplanificate și fluxurile RO↔UA/MD ca semnal după lovituri asupra rețelei ucrainene; arhivă pentru cronologii.  
  *Atenție:* Întârziere de ore; datele UA pot fi limitate în timp de război; nu localizează lovitura; tokenul se cere după înregistrare.
- ✔ **[NOAA GFS – NOMADS și oglinda AWS](<https://nomads.ncep.noaa.gov>)** · set de date · liber · ore · ★★☆☆☆ · flux: <https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/>  
  Modelul global GFS (GRIB2), rulat la 6 ore; oglindă publică pe noaa-gfs-bdp-pds.s3.amazonaws.com.  
  *Integrare:* Herbie/xarray: vânt pe niveluri și nebulozitate; al doilea model lângă ECMWF pentru încrederea prognozei.  
  *Atenție:* Fișiere mari – descărcați doar subseturi (index .idx); doar context.
- ✔ **[outage-data-ua – grafice de deconectare pe regiuni UA (JSON, inclusiv Odesa)](<https://github.com/Baskerville42/outage-data-ua>)** · set de date · liber · ore · ★★☆☆☆ · flux: <https://raw.githubusercontent.com/Baskerville42/outage-data-ua/main/data/odesa.json>  
  Arhivă publică, actualizată automat, cu graficele de deconectare planificate („preset”) și de urgență („fact”) pe grupuri, pentru mai multe regiuni, inclusiv Odesa.  
  *Integrare:* Poll la 30–60 min; trecerea bruscă la deconectări de urgență în regiunea Odesa = semnal indirect al unui atac pe infrastructură; jurnal pentru cronologii.  
  *Atenție:* Proiect neoficial; datele sunt colectate de pe paginile furnizorilor cu un browser automatizat care trece de protecția antibot – posibilă problemă de termeni; doar semnal secundar, confirmați la sursa oficială.
- ✔ **[RainViewer API – mozaic radar meteo global](<https://github.com/rainviewer/rainviewer-api-example>)** · API · liber · minute · ★★☆☆☆ · flux: <https://api.rainviewer.com/public/weather-maps.json>  
  JSON public cu cadrele radar recente și tile-uri PNG pentru hărți Leaflet/MapLibre.  
  *Integrare:* Strat radar în harta internă; ploaia sau furtuna în NE → scădeți încrederea în detecțiile acustice și optice.  
  *Atenție:* Varianta gratuită e doar pentru uz personal (zoom max. 7, fără nowcast); acoperirea RO/MD/UA depinde de datele naționale; NU detectează drone.
- ✔ **[Raspberry Shake – date publice FDSN (rețeaua AM)](<https://data.raspberryshake.org>)** · API · liber · minute · ★★☆☆☆  
  Rețea globală de seismografe cetățenești Raspberry Shake; forme de undă și stații prin FDSN (cod ObsPy „RASPISHAKE”).  
  *Integrare:* Listați stațiile din raza de ~100 km de Iași; după un incident descărcați formele de undă și comparați cu INFP pentru ora și locul exploziei/căderii. Cale standard FDSN (neverificată direct): https://data.raspberryshake.org/fdsnws/<serviciu>/1/query.  
  *Atenție:* Densitatea stațiilor în NE RO / R. Moldova – necunoscută; stații de amatori cu zgomot urban; acces liber presupus, de verificat termenii.
- ✔ **[RIPE Atlas – măsurători de internet și streaming de rezultate](<https://atlas.ripe.net>)** · API · cont gratuit · minute · ★★☆☆☆  
  Rețea de sonde de măsurare a internetului cu API REST și streaming în timp real al rezultatelor.  
  *Integrare:* ripe.atlas.cousteau: abonare la rezultatele sondelor din Odesa/Izmail/Cernăuți/Chișinău; căderea simultană a mai multor sonde = întrerupere locală de curent sau internet după lovituri.  
  *Atenție:* Câte sonde sunt în zonă – neverificat; o sondă căzută poate fi și o pană banală; crearea de măsurători cere credite.
- ~ **[AFDJ Galați – avize către navigatori pe Dunărea de Jos](<https://www.afdj.ro>)** · web · liber · ore · ★★☆☆☆  
  Administrația Fluvială a Dunării de Jos: avize de navigație, restricții și informații pe sectorul Brăila–Sulina.  
  *Integrare:* Monitorizare a avizelor noi (închideri de senal, epave, restricții după incidente cu drone în zona Galați/Isaccea).  
  *Atenție:* Existența unui flux RSS – neconfirmată; frecvența actualizărilor necunoscută. Verificare: Domeniul oficial e cunoscut, dar nu l-am putut accesa. Nu am confirmat secțiunea de avize către navigatori.
- ~ **[Drone Rada (Lituania) – rețea civică de telefoane-senzori](<https://www.lrt.lt/en/news-in-english/19/2965205/lithuanian-startup-launches-open-source-network-to-detect-shahed-type-drones>)** · web · necunoscut · istoric · ★★☆☆☆  
  Rețea civică open-source lansată în iunie 2026: telefoane Android vechi la fereastră ascultă motoarele de tip Shahed; detecțiile alimentează o hartă în timp real.  
  *Integrare:* Cel mai apropiat model pentru o rețea civică la Iași; de urmărit codul și o eventuală colaborare.  
  *Atenție:* Eficacitate nedemonstrată public; voluntari verificați; nu e clar dacă harta e publică. Verificare: Lansat pe 19.06.2026, conform LRT și Tom's Hardware din cercetarea anterioară. Linkul de cod deschis nu l-am găsit. Atenție la confidențialitatea audio.
- ~ **[EIDA federator (ORFEUS) – acces unic la nodurile seismice europene](<http://www.orfeus-eu.org/eidaws/routing/1>)** · API · liber · minute · ★★☆☆☆  
  Punct unic FDSN pentru nodurile EIDA (inclusiv NIEP/INFP, GFZ, KOERI); ORFEUS coordonează (www.orfeus-eu.org).  
  *Integrare:* ObsPy Client('EIDA'): un singur apel pentru toate stațiile pe culoarul Odesa–Prut–Iași; util la inventarierea senzorilor. Cale standard FDSN (neverificată direct): http://eida-federator.ethz.ch/fdsnws/<serviciu>/1/query.  
  *Atenție:* Unele rețele au date restricționate; federatorul poate avea întârzieri față de nodul-sursă. Verificare: Federatorul ETH este listat în ObsPy, dar doar pe http, iar funcționarea actuală nu a fost confirmată. Ca alternativă, serviciul de rutare EIDA de la ORFEUS apare în ObsPy. Un federator nou ORFEUS este neconfirmat.
- ~ **[LightningMaps.org – hartă de fulgere (date Blitzortung)](<https://www.lightningmaps.org>)** · hartă · liber · timp real · ★★☆☆☆  
  Vizualizare în timp real a descărcărilor electrice și a tunetelor, bazată pe rețeaua Blitzortung (din catalog).  
  *Integrare:* Verificare manuală: furtuni în NE → posibile alarme false la senzorii acustici/seismici și la observatori („flash-uri”).  
  *Atenție:* Nu se face scraping (interzis de Blitzortung); pentru date automate – stație proprie sau furnizor comercial. Verificare: Nu l-am putut accesa. E înrudit cu Blitzortung (deja în catalog), dar are alt URL, deci nu e duplicat. Relevanța e mică (filtrarea furtunilor).
- ~ **[Moldelectrica – arhiva datelor sistemului energetic](<https://moldelectrica.md>)** · API · liber · ore · ★★☆☆☆ · flux: <https://moldelectrica.md/utils/archive2.php?id=table&type=array>  
  Operatorul de transport al R. Moldova: tabel public (JSON) cu producția și consumul sistemului.  
  *Integrare:* Interogare orară; salturi bruște = posibile deconectări în cascadă după lovituri pe rețeaua UA (ca în noiembrie 2022).  
  *Atenție:* Endpoint nedocumentat (folosit de Electricity Maps); se poate schimba; interogați rar. Verificare: Endpointul archive2.php apare încă în MD.py, dar configurația zonei MD din Electricity Maps folosește acum ENTSO-E pentru producție și consum. Endpointul nu mai e folosit de ei și poate fi învechit. Nu l-am putut testa (host blocat).
- ~ **[ODAS – localizarea surselor sonore pe hardware ieftin](<https://github.com/introlab/odas>)** · altele · liber · timp real · ★★☆☆☆  
  Bibliotecă C open-source (MIT) pentru localizarea, urmărirea și separarea surselor sonore cu matrice de microfoane.  
  *Integrare:* Pe nod cu ReSpeaker/UMA-16: azimutul sursei → triangulare între noduri sincronizate GPS; trimiteți doar azimut și oră.  
  *Atenție:* Nu clasifică dronele; cere calibrare și sincronizare între noduri; vântul reduce precizia. Verificare: Biblioteca există (MIT, C, localizarea surselor sonore), dar nu am dovezi de activitate recentă a proiectului.
- ~ **[Transelectrica – starea SEN în timp real](<https://www.transelectrica.ro>)** · web · liber · minute · ★★☆☆☆  
  Operatorul de transport român: pagină publică cu consumul, producția și soldul schimburilor SEN, actualizată des.  
  *Integrare:* Poll moderat; variații bruște ale schimburilor cu UA/MD = context după lovituri pe rețeaua vecină; pentru date structurate folosiți ENTSO-E.  
  *Atenție:* Pagina exactă și formatul datelor – de confirmat; fără scraping agresiv. Verificare: Domeniul oficial e cunoscut, dar nu l-am putut accesa. Nu am confirmat URL-ul paginii SEN în timp real.
- ~ **[Windy Webcams API – camere web publice](<https://api.windy.com/webcams>)** · API · cheie gratuită · minute · ★★☆☆☆  
  API pentru camere web publice indexate de Windy, căutabile pe zonă (ex. Galați, Tulcea, Iași, Prut).  
  *Integrare:* Lista camerelor publice într-o rază dată; operatorul deschide manual imaginile pentru confirmare vizuală (fum, foc) după o alertă.  
  *Atenție:* Doar camere publice înscrise; termenii nivelului gratuit – de verificat; nu republicați imagini fără drept. Verificare: Produs separat de api.windy.com (deja în catalog). Repo-ul windycom/API trimite doar la api.windy.com, iar URL-ul exact al Webcams API nu l-am confirmat.
- ✔ **[ASF Search API – imagini radar Sentinel-1](<https://docs.asf.alaska.edu/asf_search/basics/>)** · API · cont gratuit · zile · ★☆☆☆☆  
  Căutarea și descărcarea scenelor SAR Sentinel-1 (văd prin nori și noaptea) de la Alaska Satellite Facility.  
  *Integrare:* Post-incident: comparați scenele înainte/după pentru pagube mari (porturile Izmail/Reni, depozite).  
  *Atenție:* Revizită de zile; ~10 m rezoluție – nu vede o dronă, doar pagube mari; descărcarea cere cont Earthdata.
- ✔ **[Copernicus Climate Data Store – reanaliza ERA5](<https://cds.climate.copernicus.eu>)** · API · cont gratuit · zile · ★☆☆☆☆ · flux: <https://cds.climate.copernicus.eu/api>  
  Reanaliză orară ERA5 (vânt, temperatură pe niveluri), cu întârziere de câteva zile.  
  *Integrare:* cdsapi: reconstruiți condițiile din noaptea unui incident pentru cronologii și pentru calibrarea senzorilor.  
  *Atenție:* Nu e timp real; necesită cont și acceptarea licenței.
- ✔ **[Drone-detection-dataset (Svanström) – IR, vizibil și audio](<https://github.com/DroneDetectionThesis/Drone-detection-dataset>)** · set de date · liber · istoric · ★☆☆☆☆  
  650 de clipuri video (IR și vizibil) și 90 de clipuri audio adnotate: dronă, avion, pasăre, elicopter, fundal.  
  *Integrare:* Antrenarea/validarea clasificatoarelor pentru camera termală și nodul acustic; include clasele care produc confuzii.  
  *Atenție:* Drone mici, nu Shahed; adnotări în format MATLAB (există decodor Python).
- ✔ **[EarthScope (fost IRIS DMC) – servicii FDSN](<https://service.earthscope.org>)** · API · liber · minute · ★☆☆☆☆  
  Cea mai mare arhivă seismică globală (fost IRIS): metadate de stații și forme de undă din multe rețele.  
  *Integrare:* Inventar al stațiilor publice din RO/MD/UA care nu sunt în EIDA; arhivă pentru analize post-incident. Cale standard FDSN (neverificată direct): https://service.earthscope.org/fdsnws/<serviciu>/1/query.  
  *Atenție:* Acoperire regională inegală; doar post-incident.
- ✔ **[Electricity Maps – API și parsere open-source](<https://electricitymaps.com>)** · API · necunoscut · ore · ★☆☆☆☆  
  Hartă și API cu mixul de producție și fluxurile pe zone (RO, MD, UA); parserele open-source arată sursele oficiale folosite.  
  *Integrare:* Referință pentru endpointurile Moldelectrica/Ukrenergo/ENTSO-E; API pentru o vedere unificată a regiunii.  
  *Atenție:* Condițiile nivelului gratuit – neverificate; date agregate și întârziate.
- ✔ **[GEOFON (GFZ Potsdam) – FDSN și catalog rapid](<https://geofon.gfz.de>)** · API · liber · minute · ★☆☆☆☆  
  Rețea seismică globală și catalog rapid de cutremure; servicii FDSN.  
  *Integrare:* Sursă secundară pentru validarea evenimentelor seismice din regiune; arhivă pentru analize. Cale standard FDSN (neverificată direct): https://geofon.gfz.de/fdsnws/<serviciu>/1/query.  
  *Atenție:* Prag de magnitudine ridicat; nu vede explozii mici.
- ✔ **[GFZ – indicele geomagnetic Kp/Hpo](<https://kp.gfz-potsdam.de/en/data>)** · set de date · liber · ore · ★☆☆☆☆  
  Indicii Kp (3 h) și Hpo (30/60 min) ai activității geomagnetice, cu formate text publice.  
  *Integrare:* Filtru: anomaliile GNSS/ADS-B în timpul unei furtuni geomagnetice nu sunt neapărat bruiaj; context pentru GPSJam (din catalog).  
  *Atenție:* Indicator global, nu local.
- ✔ **[KOERI (Observatorul Kandilli) – nod EIDA](<https://eida.koeri.boun.edu.tr>)** · API · liber · minute · ★☆☆☆☆  
  Rețeaua seismică a Turciei, cu acoperire a bazinului Mării Negre; servicii FDSN.  
  *Integrare:* Context pentru evenimente de pe coasta Mării Negre (ex. lovituri puternice în zona Odesa). Cale standard FDSN (neverificată direct): https://eida.koeri.boun.edu.tr/fdsnws/<serviciu>/1/query.  
  *Atenție:* Rar util pentru Iași; doar context.
- ✔ **[Meteostat – date meteo istorice pe stații](<https://meteostat.net>)** · set de date · liber · istoric · ★☆☆☆☆  
  Date meteo orare și zilnice istorice pe stații, cu bibliotecă Python (licență CC BY 4.0).  
  *Integrare:* Analiză post-incident: vânt și temperatură la Iași, Botoșani, Suceava; serii pentru calibrarea senzorilor acustici pe vânt.  
  *Atenție:* Stațiile pot avea goluri; nu e sursă oficială.
- ✔ **[NASA GIBS – tile-uri WMTS cu imagini satelitare](<https://earthdata.nasa.gov/gibs>)** · hartă · liber · ore · ★☆☆☆☆ · flux: <https://gibs-a.earthdata.nasa.gov/wmts/epsg3857/best/>  
  Servicii WMTS cu imagini satelitare aproape în timp real (MODIS/VIIRS și alte straturi), gata de pus în Leaflet/OpenLayers.  
  *Integrare:* Strat de fundal în panou; verificare vizuală a fumului sau a incendiilor mari după lovituri în Odesa/Izmail.  
  *Atenție:* Rezoluție de sute de metri, întârziere de ore, nori; pentru puncte termice FIRMS (din catalog) e mai potrivit; numele straturilor – de verificat.
- ✔ **[Sensor.Community (fost luftdaten.info) – senzori cetățenești](<https://sensor.community/>)** · senzori · liber · minute · ★☆☆☆☆ · flux: <https://data.sensor.community/airrohr/v1/sensor/{sensor_id}/>  
  Rețea cetățenească de senzori de particule (PM) și meteo, cu date deschise; client Python „luftdaten”.  
  *Integrare:* Context post-incident: vârfuri de PM lângă locul unui impact sau incendiu; aceeași rețea poate găzdui senzori proprii.  
  *Atenție:* Densitate redusă în NE RO; senzori necalibrați; endpointul API exact – neconfirmat în această sesiune.
- ~ **[AISHub – schimb de date AIS între stații](<https://www.aishub.net>)** · API · cont gratuit · minute · ★☆☆☆☆  
  Rețea de partajare AIS; stațiile trimit date la data.aishub.net, iar fluxul agregat e oferit membrilor.  
  *Integrare:* Cu un receptor propriu (AIS-catcher) obțineți acces la fluxul agregat pentru Dunărea de Jos și Marea Neagră; comparație cu MarineTraffic/VesselFinder (din catalog).  
  *Atenție:* Condiția de acces (contribuție cu stație proprie) și acoperirea pe Dunăre – neverificate în această sesiune. Verificare: Apare doar în README-ul docker-shipfeeder (AISHUB_UDP_PORT). N-am văzut o dată recentă și n-am putut accesa aishub.net. Datele se obțin în schimbul unei stații proprii care trimite date.
- ~ **[CAIDA BGPStream – date BGP live și istorice](<https://bgpstream.caida.org>)** · API · liber · minute · ★☆☆☆☆  
  Bibliotecă și cadru pentru analiza datelor BGP live și istorice de la colectoarele publice.  
  *Integrare:* Urmăriți retragerile de prefixe ale furnizorilor din Odesa/Izmail; corelați cu IODA și Cloudflare Radar (din catalog).  
  *Atenție:* Cere procesare proprie; o retragere BGP nu dovedește un atac. Verificare: Există („live and historical BGP data analysis”), dar ultima versiune pybgpstream e din 05.2020. Nu am putut confirma că brokerul bgpstream.caida.org funcționează azi.
- ~ **[Centrul Hidrometeorologic al Ucrainei (UHMC)](<https://meteo.gov.ua>)** · web · liber · ore · ★☆☆☆☆  
  Serviciul meteo oficial al Ucrainei: prognoze și avertizări pentru Odesa, Vinnîțea, Cernăuți.  
  *Integrare:* Context meteo pe partea ucraineană a culoarului (furtuni, ceață).  
  *Atenție:* Disponibilitate variabilă în timp de război; format nestructurat. Verificare: Domeniul oficial e cunoscut, dar nu l-am putut accesa.
- ~ **[DADS – drone-audio-detection-samples (Hugging Face)](<https://huggingface.co/datasets/geronimobasso/drone-audio-detection-samples>)** · set de date · liber · istoric · ★☆☆☆☆  
  Set de eșantioane audio etichetate dronă / non-dronă (licență MIT, conform docs/03).  
  *Integrare:* Completează DroneAudioDataset la antrenarea clasificatorului de pe nod.  
  *Atenție:* Nu e dedicat Shahed; licența și conținutul trebuie verificate direct. Verificare: Apare doar în cercetarea anterioară (docs/03), iar huggingface.co e blocat aici. Licența (declarată MIT) trebuie verificată înainte de folosire, fiindcă un set similar s-a dovedit restricționat.
- ~ **[ePPO (UA) – raportare cetățenească a țintelor aeriene](<https://www.ukrinform.net/rubric-ato/3930665-eppo-app-helps-ukraine-close-sky-by-80.html>)** · aplicație · necunoscut · istoric · ★☆☆☆☆  
  Aplicație în care utilizatorul autentificat îndreaptă telefonul spre țintă și apasă un buton; datele merg la apărarea antiaeriană.  
  *Integrare:* Lecție de proiectare (identitate verificată, agregare centrală, fără ieșire publică); în RO canalul oficial e 112.  
  *Atenție:* Date nepublice; funcționează doar în Ucraina. Verificare: Aplicație UA cu autentificare și fără date publice, deci doar context sau model. Articolul Ukrinform nu l-am putut reaccesa.
- ~ **[NetBlocks – observator de întreruperi de internet](<https://netblocks.org>)** · web · liber · ore · ★☆☆☆☆  
  Rapoarte publice despre întreruperile de internet la nivel național/regional, inclusiv după atacuri asupra energeticii ucrainene.  
  *Integrare:* Confirmare secundară pentru întreruperi semnalate de IODA, Cloudflare Radar și RIPE Atlas.  
  *Atenție:* Fără API public confirmat; publică mai ales pe rețelele sociale, cu întârziere. Verificare: Nu l-am putut accesa. Nu are API public cunoscut, iar actualizările apar mai ales pe rețelele sociale.
- ~ **[NOAA IGRA2 – arhiva globală de radiosondaje](<https://www1.ncdc.noaa.gov/pub/data/igra/>)** · set de date · liber · zile · ★☆☆☆☆  
  Arhiva integrată de sondaje aerologice (vânt, temperatură pe verticală) pentru stații din toată lumea.  
  *Integrare:* Siphon (IGRAUpperAir): profiluri pentru stațiile din regiune; analiza inversiunilor care reduc raza senzorilor acustici.  
  *Atenție:* Întârziere de zile; stațiile exacte din RO/MD/UA – de verificat. Verificare: Arhiva IGRA2 de radiosondaje. Calea www1.ncdc.noaa.gov este folosită încă de siphon (iul 2026), dar nu a fost testată. Este posibil ca NOAA să o fi mutat pe ncei.noaa.gov (neconfirmat). Nu dublează U. Wyoming.
- ~ **[ShipXplorer (AirNav) – hartă AIS](<https://www.shipxplorer.com>)** · hartă · necunoscut · minute · ★☆☆☆☆  
  Hartă AIS alimentată de receptoare voluntare (sxfeeder).  
  *Integrare:* Verificare vizuală a traficului pe Dunăre la Izmail/Reni după o alertă; acces extins dacă alimentați cu receptor propriu.  
  *Atenție:* Termenii de acces și API – neverificați; acoperire inegală pe Dunăre. Verificare: Apare în README-ul docker-shipfeeder (sxfeeder, redenumit în 03.2024), deci mențiunea e recentă. Site-ul nu l-am putut accesa direct.
- ~ **[Sky Fortress / Sky Map (UA) – rețeaua acustică ucraineană (informații publice)](<https://militarnyi.com/en/news/lit-ukr-skyfortress-acoustic-uav-detection/>)** · web · necunoscut · istoric · ★☆☆☆☆  
  Rețea de ~10.000+ senzori acustici ieftini și platforma Sky Map; pilot în Lituania din oct. 2026.  
  *Integrare:* Model de referință pentru rețeaua acustică de la Iași (densitate, fuziune centrală); nu există flux public.  
  *Atenție:* Datele sunt militare, nepublice; cifrele de performanță sunt declarative. Verificare: Rețeaua e reală conform cercetării anterioare, dar datele ei nu sunt publice: e doar context sau model, nu un flux. Articolul nu l-am putut reaccesa.
- ~ **[Ukrenergo – date OES zilnice (endpoint folosit de Electricity Maps)](<https://ua.energy/wp-admin/admin-ajax.php>)** · API · liber · ore · ★☆☆☆☆  
  Endpoint de date (POST, action=get_data_oes) cu producția sistemului energetic unificat al Ucrainei pe zi; distinct de anunțurile Ukrenergo din catalog.  
  *Integrare:* Poll de câteva ori pe zi; scăderi bruște ale producției = context după atacuri masive asupra energeticii.  
  *Atenție:* Endpoint intern WordPress, nedocumentat; poate refuza cereri (403); date la nivel de țară, nu pe regiuni. Verificare: Endpoint WordPress admin-ajax nedocumentat (POST action=get_data_oes). E folosit în continuare de UA.fetch_production în UA.yaml de pe master. Site-ul ua.energy e deja în catalog, dar acesta e alt flux, deci nu e duplicat. Nu l-am putut testa direct.
- ~ **[Ukrzaliznytsia – anunțuri despre trafic și întârzieri](<https://uz.gov.ua>)** · web · liber · minute · ★☆☆☆☆  
  Căile ferate ucrainene: anunțuri despre întârzieri și opriri de trenuri, inclusiv din cauza atacurilor în regiunea Odesa.  
  *Integrare:* Întârzieri bruște pe liniile din regiunea Odesa = semnal indirect al unor lovituri; canalul Telegram oficial – de identificat și confirmat.  
  *Atenție:* Handle-ul Telegram nu e confirmat aici; informațiile pot fi întârziate din motive de securitate. Verificare: Domeniul oficial e cunoscut, dar nu l-am putut accesa. Anunțurile operative apar probabil mai repede pe alte canale (neconfirmat).
- ~ **[US Army – „Listening to the Sky: Acoustic Drone Detection in Ukraine” (2026)](<https://api.army.mil/e2/c/downloads/2026/04/30/af450e75/no-26-1115-listening-to-the-sky-acoustic-drone-detection-in-ukraine-mar-26.pdf>)** · PDF · liber · istoric · ★☆☆☆☆  
  Raport public al Armatei SUA despre lecțiile rețelei acustice ucrainene.  
  *Integrare:* Lectură de fundal pentru specificația nodurilor și a fuziunii centrale.  
  *Atenție:* Perspectivă militară; detaliile tehnice sunt probabil generale. Verificare: PDF citat în cercetarea anterioară (docs/03), dar api.army.mil e blocat aici. E un document de context, nu un flux.
- ~ **[Zvook (UA) – detecție acustică cu „oglinzi” pe turnuri](<https://united24media.com/defense-tech/ukraines-zvook-acoustic-system-tests-mobile-detection-of-low-flying-missiles-and-drones-21587>)** · web · necunoscut · istoric · ★☆☆☆☆  
  Sistem acustic pe turnuri GSM (10–12 m), rază declarată ~5 km pentru drone și ~7 km pentru rachete de croazieră, ~1,6% alarme false.  
  *Integrare:* Referință de proiectare pentru noduri montate la înălțime; nu există date publice.  
  *Atenție:* Performanțe declarate, din surse puține. Verificare: Apare doar în cercetarea anterioară (United24, Espreso). Nu e o sursă de date, ci un model de senzor.

## Instituții internaționale și vecini

- ✔ **[GlobalMilitary.net – European Airspace Violations tracker](<https://www.globalmilitary.net/conflicts/european-airspace/>)** · set de date · liber · zile · ★★★☆☆  
  Registru OSINT incident cu incident: dată, stat afectat, atribuire oficială, tip (dronă/rachetă/aeronavă/balon), rezultat; include RO și MD (ultimul văzut 15.10.2026).  
  *Integrare:* Scraping zilnic al paginilor /incidents/AAAALL-NN pentru validarea și completarea bazei proprii de incidente.  
  *Atenție:* Proiect OSINT privat; numărătorile pe pagină sunt inconsecvente; metodologie de verificat.
- ✔ **[Wikipedia RO – 'Incidente cu drone în România în 2026' (+ 'Atacul cu dronă de la Galați din 2026')](<https://ro.wikipedia.org/wiki/Incidente_cu_drone_%C3%AEn_Rom%C3%A2nia_%C3%AEn_2026>)** · web · liber · zile · ★★★☆☆  
  Cronologie colaborativă a incidentelor cu drone din România în 2026 (35 încălcări și 44 resturi identificate până la 17.10.2026), cu trimiteri la surse.  
  *Integrare:* Folosit ca index: verificare zilnică a istoricului reviziilor (MediaWiki API) pentru incidente noi și surse citate.  
  *Atenție:* Wikipedia – doar index, fiecare fapt se verifică în sursa primară; date uneori contradictorii (25.04 vs 29.05 Galați).
- ~ **[MAEIE Republica Moldova – comunicate (convocări, note de protest, bilanțuri)](<https://mfa.gov.md/ro/content/mae-condamna-ferm-incalcarea-spatiului-aerian-al-republicii-moldova-si-convoaca-ambasadorul>)** · web · liber · ore · ★★★☆☆  
  Comunicate oficiale după fiecare încălcare: localități (ex. Codrenii Noi, Chiștelnița), convocări ale ambasadorului rus, bilanț (102 încălcări din 2022, 65 în 2026).  
  *Integrare:* Polling orar pe secțiunea comunicate; extragere localitate+dată → confirmare oficială a incidentelor pe ruta MD→Iași.  
  *Atenție:* Publicat după incident (ore); cifrele diferă între instituții MD. Verificare: MAEIE MD există și emite comunicate/convocări după încălcări ale spațiului aerian; slug-ul exact al URL-ului nu e confirmat – de reverificat sau înlocuit cu o pagină din dovezi.
- ✔ **[AIEA – 'Update XXX – IAEA Director General Statement on Situation in Ukraine'](<https://www.iaea.org/newscenter/pressreleases>)** · web · liber · zile · ★★☆☆☆ · flux: <https://www.iaea.org/feeds/news>  
  Actualizări AIEA: număr de drone detectate lângă centralele nucleare (ex. 22 lângă CNE Ucraina de Sud, Mykolaiv) – indicator al rutelor de drone din sud.  
  *Integrare:* Parsare săptămânală a numărului de drone raportate la CNE Ucraina de Sud/Hmelnițki pentru tendințe de rută spre vest.  
  *Atenție:* Agregat pe săptămână; nu dă ore/traiectorii.
- ✔ **[Dowództwo Operacyjne RSZ (DORSZ, Polonia) – cont X @DowOperSZ și site](<https://x.com/DowOperSZ>)** · rețea socială · cont gratuit · minute · ★★☆☆☆  
  Comunicate în timp real despre ridicarea aviației, starea apărării aeriene și încălcări ale spațiului aerian polonez în timpul atacurilor asupra vestului Ucrainei.  
  *Integrare:* Indicator de amploare a valului de atac spre vest (dacă PL ridică avioane, atacul e masiv); urmărire manuală sau prin site wojsko-polskie.pl/dorsz.  
  *Atenție:* Cronologia X necesită autentificare, API X plătit; nu acoperă direct axa Odesa–Iași.
- ✔ **[EASA – Safety Information Bulletin 2022-02R4 (GNSS jamming/spoofing)](<https://ad.easa.europa.eu/ad/2022-02R4>)** · PDF · liber · zile · ★★☆☆☆  
  Buletin EASA (rev. 4, 3.07.2026) despre bruiaj/spoofing GNSS; listează zone afectate inclusiv partea estică a FIR București (LRBB) și Marea Neagră.  
  *Integrare:* Context pentru devierea dronelor prin război electronic; corelare cu GPSJam/FR24; verificare săptămânală a listei de zone (pagina EASA GNSS).  
  *Atenție:* Recomandări neobligatorii; lista de FIR-uri se actualizează periodic.
- ✔ **[EUvsDisinfo – baza de date a cazurilor de dezinformare (SEAE East StratCom)](<https://euvsdisinfo.eu/disinformation-cases/>)** · set de date · liber · zile · ★★☆☆☆ · flux: <https://euvsdisinfo.eu/feed/>  
  Cazuri documentate de narațiuni pro-Kremlin despre dronele din RO/PL/MD (ex. 'drona din România e provocare ucraineană').  
  *Integrare:* Căutare periodică după 'drone Romania/Moldova'; folosit pentru a marca în canalul intern zvonurile false după incident.  
  *Atenție:* Analiză post-factum; nu confirmă incidente, doar dezinformarea din jurul lor.
- ✔ **[OSW (Centrul pentru Studii Estice, Varșovia) – analize zilnice ale războiului](<https://www.osw.waw.pl/en/publikacje/analyses/2026-10-06/more-resolve-resources-romania-and-drone-threat>)** · web · liber · zile · ★★☆☆☆ · flux: <https://www.osw.waw.pl/en/rss.xml>  
  Analize OSW (inclusiv 'More resolve than resources: Romania and the drone threat', 6.10.2026: 30 incursiuni ian.–sept. 2026) și rapoarte zilnice 'Day N of the war'.  
  *Integrare:* Lectură zilnică a rapoartelor de război (Google News RSS pe site:osw.waw.pl, RSS propriu neconfirmat).  
  *Atenție:* Analiză, nu date brute.
- ✔ **[Rządowe Centrum Bezpieczeństwa (RCB, Polonia) – Alert RCB și comunicate](<https://www.gov.pl/web/rcb/komunikaty>)** · web · liber · minute · ★★☆☆☆  
  Arhiva alertelor SMS RCB ('zagrożenie atakiem z powietrza', neutralizarea obiectelor) cu text, zonă și oră.  
  *Integrare:* Model de comparație pentru RO-Alert; polling pagina de comunicate pentru valuri de atac spre vestul Ucrainei.  
  *Atenție:* Specific Poloniei; pagini cu metadate de dată uneori inconsecvente.
- ~ **[EEAS – Press Material (declarații Înaltul Reprezentant / purtător de cuvânt)](<https://www.eeas.europa.eu/eeas/press-material_en>)** · web · liber · ore · ★★☆☆☆  
  Declarații SEAE: condamnări ale încălcării spațiului aerian al RO/MD, convocarea diplomaților ruși, declarații UE la OSCE.  
  *Integrare:* Polling pagină filtrată pe tip 'statement'; există pagini RSS EEAS (eeas.europa.eu/.../rss_*) – URL exact al feedului curent neconfirmat.  
  *Atenție:* Reacție politică, la ore/zile după incident. Verificare: Pagina apare în căutarea anterioară, cu listări din 01.11.2026, dar nu am putut-o reaccesa. Fluxul RSS nu e confirmat.
- ~ **[Großwald – 'Russian Drone and Missile Incursions into NATO Territory: The Running Record'](<https://www.grosswald.org/>)** · set de date · liber · zile · ★★☆☆☆  
  Registru întreținut al incursiunilor rusești în spațiul NATO din 2022, cu reacția statelor/NATO pentru fiecare; România are cea mai completă evidență.  
  *Integrare:* Verificare lunară; import manual pentru analiză istorică.  
  *Atenție:* Ultimul rezumat văzut: 18.08.2026; autor independent. Verificare: Site-ul Großwald există și e activ în 2026; URL-ul exact «running record» nu a fost văzut independent.
- ~ **[Ministerul Apărării al Bulgariei (mod.bg) – știri](<https://www.mod.bg/news9527>)** · web · liber · ore · ★★☆☆☆  
  Comunicate despre drone găsite pe litoral/în Marea Neagră și distruse de Marina bulgară (inclusiv drone-momeală fără încărcătură).  
  *Integrare:* Polling pagina de știri; corelare cu atacurile asupra Odesei/Izmail pentru rutele maritime.  
  *Atenție:* Originea dronelor adesea nedeclarată; limba bulgară. Verificare: Site-ul oficial MApN al Bulgariei există. Activitatea curentă nu am putut-o confirma independent. Relevant pentru drone pe litoralul Mării Negre.
- ~ **[Misiunea Permanentă a R. Moldova la OSCE (Viena) – declarații despre încălcări ale spațiului aerian](<https://austria.mfa.gov.md/ro/content/republica-moldova-semnaleaz%C4%83-la-osce-riscurile-regionale-generate-de-%C3%AEnc%C4%83lc%C4%83rile-repetate>)** · web · liber · zile · ★★☆☆☆  
  Declarații oficiale MD la OSCE cu liste de incidente datate (ex. Copanca 13.07.2026; 8, 12, 14 sept. 2026 – dronă care a trecut din MD în RO).  
  *Integrare:* Scraping lunar al paginilor de conținut; extragere date/localități pentru baza de date de incidente.  
  *Atenție:* Bilanțuri politice; cifrele pot diferi între instituții. Verificare: Domeniul austria.mfa.gov.md există (ambasada RM la Viena și misiunea la OSCE). Pagina anume nu am putut-o verifica. Folosește-l pentru context și confirmări diplomatice.
- ~ **[NATO Allied Air Command (AIRCOM) – arhiva de știri 2026](<https://ac.nato.int/archive/2026/nato-allies-test-layered-counterdrone-defences-in-romania-in-support-of-eastern-sentry->)** · web · liber · ore · ★★☆☆☆  
  Știri oficiale AIRCOM: rotații eAP în România (Borcea, M. Kogălniceanu), Eastern Sentry, interceptări/teste anti-dronă.  
  *Integrare:* Polling pe ac.nato.int/sitemap (sau index /archive/2026) la 1–2 h; filtru cuvinte cheie Romania/drone/scramble; atașează la incident ca confirmare post-factum.  
  *Atenție:* Comunicate cu întârziere de ore/zile; nu anunță în timp real interceptările. RSS neconfirmat. Verificare: Slug-ul articolului e nereverificat: în căutarea anterioară apar alte articole din ac.nato.int/archive/2026. Secțiunea există probabil, dar nu am putut-o reaccesa.
- ~ **[NATO – newsroom nato.int (știri, transcrieri, conferințe)](<https://www.nato.int/en/news-and-events/articles/news/2025/09/12/nato-launches-eastern-sentry-to-bolster-posture-along-eastern-flank>)** · web · liber · ore · ★★☆☆☆  
  Știri și transcrieri NATO HQ (ex. conferința SG cu Președintele României, martie 2026; Eastern Sentry).  
  *Integrare:* Polling https://www.nato.int/sitemap.xml pentru URL-uri noi /news-and-events/; alternativ abonare e-mail la comunicate (nato.int/cps/en/natohq/e-mail_distribution.htm) → parser IMAP.  
  *Atenție:* Nu există RSS oficial confirmat (doar feed terț feeder.co). Ton instituțional; confirmare la nivel politic, nu operativ. Verificare: Slug-ul articolului nu e în evidența anterioară (acolo apare alt URL nato.int din 2026). Probabil corect, dar nu l-am putut reaccesa.
- ~ **[NATO – Official texts: declarații ale Consiliului Nord-Atlantic privind încălcări ale spațiului aerian](<https://www.nato.int/en/about-us/official-texts-and-resources/official-texts/2025/09/23/statement-by-the-north-atlantic-council-on-recent-airspace-violations-by-russia>)** · web · liber · zile · ★★☆☆☆  
  Declarații NAC (ex. 23.09.2025) care numesc România, Polonia, Estonia etc. ca state afectate de încălcări rusești.  
  *Integrare:* Monitorizare săptămânală a secțiunii official-texts; extragere automată a statelor/datelor menționate pentru cronologia post-incident.  
  *Atenție:* Publicate rar, doar la incidente majore; valoare de context politic. Verificare: URL-ul exact apare în căutarea anterioară, dar nu l-am putut reproduce. Secțiune distinctă de 345, deci nu e duplicat.
- ~ **[ONU – Meetings Coverage (press.un.org), pagina România](<https://press.un.org/en>)** · web · liber · ore · ★★☆☆☆  
  Rezumate oficiale ale ședințelor Consiliului de Securitate (ex. ședința de urgență din 1.06.2026 cerută de România după drona de la Galați; MD a raportat 49 incidente).  
  *Integrare:* Monitorizare pagini /romania și /ukraine; arhivare ca sursă oficială post-incident.  
  *Atenție:* Include și pozițiile Rusiei (negări) – a se cita cu atribuire. Verificare: Nu am găsit nicio dovadă pentru pagina de țară /en/romania. Site-ul press.un.org există și e activ (Consiliul de Securitate). Caută în el după „Romania”.
- ~ **[OSCE – Consiliul Permanent / Forumul pentru Cooperare în Securitate și Misiunea OSCE în Moldova](<https://www.osce.org/permanent-council>)** · PDF · liber · zile · ★★☆☆☆  
  Documente oficiale OSCE (declarații statelor despre încălcări ale spațiului aerian, mandatul Misiunii în Moldova prelungit până la 31.12.2026).  
  *Integrare:* Monitorizare documente PC/FSC (resources.osce.org) după cuvinte cheie 'drone', 'airspace', 'Moldova'.  
  *Atenție:* Declarațiile reflectă poziția statelor (inclusiv Rusia); întârziere de zile. Verificare: Calea osce.org/pc/36924 nu e confirmată. Misiunea în Moldova e la https://www.osce.org/mission-to-moldova. Feedul osce.org/rss.xml dădea 404 (martie 2026). Sunt documente PDF, utile doar ca context.
- ~ **[Președinția R. Moldova – comunicate și Consiliul Național de Securitate](<https://presedinte.md/>)** · web · liber · ore · ★★☆☆☆  
  Declarații ale Președintei după incidente (ex. Crocmaz) și bilanțuri (52 incidente 24.02.2022–9.08.2026); comunicate CNS.  
  *Integrare:* Polling zilnic; folosit pentru confirmare politică și cifre agregate.  
  *Atenție:* Mesaj politic; cifrele nu coincid cu cele MAEIE/StratCom. Verificare: Corectează numele: în R. Moldova organul este Consiliul Suprem de Securitate (CSS), nu «Consiliul Național de Securitate». Calea /css-comunicate-de-presa (fără /rom/) neconfirmată; site-ul există.
- ~ **[SHAPE – News releases (Eastern Sentry, scramble-uri NATO)](<https://shape.nato.int/news-releases/nato-scrambles-jet-in-first-eastern-sentry-response-to-defend-alliance>)** · web · liber · ore · ★★☆☆☆  
  Comunicate SHAPE despre Eastern Sentry: primul scramble (13.09.2025), suport ISR (RQ-4D), postura pe flancul estic.  
  *Integrare:* Polling https://shape.nato.int/sitemap și /news-releases; corelare cu alertele RO-Alert/MApN pentru confirmarea reacției aliate.  
  *Atenție:* Ritm neregulat; informații operative limitate. RSS neconfirmat. Verificare: Slug-ul articolului e nereverificat: în căutarea anterioară apar alte articole SHAPE (eastern-sentry-to-enhance-...). Nu l-am putut reaccesa.
- ✔ **[CEPA – Hybrid Threats (cartografierea incidentelor cu drone în Europa)](<https://cepa.org/article/mapping-a-europe-no-longer-at-peace/>)** · web · liber · zile · ★☆☆☆☆ · flux: <https://cepa.org/feed/>  
  Analize CEPA cu numărătoare a incursiunilor de drone după 9.09.2025 (cel puțin 38 incidente ulterioare) și 'Russia's shadow war surges southward'.  
  *Integrare:* Lectură lunară pentru context strategic.  
  *Atenție:* Think-tank american; nu este bază de date descărcabilă.
- ✔ **[Copernicus EMS – Rapid Mapping (activări)](<https://rapidmapping.emergency.copernicus.eu/>)** · API · liber · ore · ★☆☆☆☆ · flux: <https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations-info/?limit=50>  
  Activări de cartografiere rapidă prin satelit (EMSR…) pentru dezastre; JSON public fără cheie pe rapidmapping.emergency.copernicus.eu.  
  *Integrare:* Interogare periodică a listei de activări pentru RO/MD/UA (ex. evaluare daune după impacte majore); GeoRSS pe paginile de activare.  
  *Atenție:* Endpoint-urile exacte confirmate doar din documentație terță (ifrcgo, ocha-lens); rar activat pentru incidente cu drone.
- ✔ **[EUROCONTROL Aviation Intelligence Portal (ansperformance.eu)](<https://ansperformance.eu/data/>)** · set de date · liber · zile · ★☆☆☆☆  
  Date zilnice descărcabile: trafic IFR, întârzieri ATFM pe entitate/cauză, dashboard-uri pe aeroport.  
  *Integrare:* Descărcare lunară CSV pentru a măsura impactul incidentelor (închideri LRIA/LUKK, reroutări) asupra traficului.  
  *Atenție:* Fără API documentat; date cu întârziere de ~1 lună.
- ✔ **[Finlanda – comunicate Ministerul Apărării (valtioneuvosto.fi) despre suspiciuni de încălcare a spațiului aerian](<https://valtioneuvosto.fi/-/236553176>)** · web · liber · ore · ★☆☆☆☆ · flux: <https://valtioneuvosto.fi/staattiset-feedit/-/asset_publisher/Kh4WBNNjLkT0/rss>  
  Comunicate oficiale 'Epäilty ilmatilaloukkaus' (drone la Virolahti 3.05.2026, aeronave rusești).  
  *Integrare:* Context; ingestie prin Google News RSS pe site:valtioneuvosto.fi.  
  *Atenție:* Axă nordică; relevanță indirectă.
- ✔ **[Forțele Armate Naționale ale Letoniei (mil.lv / NBS)](<https://www.mil.lv/en/news/multiple-unmanned-aerial-vehicles-have-entered-latvian-airspace>)** · web · liber · ore · ★☆☆☆☆  
  Comunicate NBS despre incursiuni de drone, identificarea originii resturilor, finalizarea lucrărilor la locul impactului.  
  *Integrare:* Polling știri; util pentru analiza procedurilor post-impact.  
  *Atenție:* Axă baltică; atribuirea originii poate dura zile.
- ✔ **[Forțele de Apărare ale Estoniei (mil.ee) – știri](<https://mil.ee/en/news/>)** · web · liber · ore · ★☆☆☆☆ · flux: <https://mil.ee/feed/>  
  Știri EDF: dronă doborâtă de un F-16 românesc (19.05.2026), operațiune de reacție rapidă la amenințări aeriene, aplicația Ole Valmis.  
  *Integrare:* Context NATO; polling săptămânal.  
  *Atenție:* Axă Rusia–Estonia; relevanță indirectă.
- ✔ **[GDACS – Global Disaster Alert and Coordination System (UE JRC + ONU)](<https://www.gdacs.org/>)** · RSS · liber · minute · ★☆☆☆☆ · flux: <https://www.gdacs.org/xml/rss.xml>  
  Alerte automate pentru dezastre naturale (cutremure Vrancea, inundații, incendii) cu GeoRSS și API GeoJSON.  
  *Integrare:* Ingestie RSS pentru a deosebi explozii/alarme de evenimente naturale (ex. cutremur) în zona Iași–Vrancea; client Python neoficial gdacs-api.  
  *Atenție:* Nu acoperă conflicte; feed principal confirmat doar prin documentație terță + feeduri per-eveniment.
- ✔ **[MAE Lituania (urm.lt) – proteste privind încălcări ale spațiului aerian](<https://www.mfa.lt/en/news>)** · web · liber · ore · ★☆☆☆☆  
  Note de protest oficiale ale Lituaniei către Belarus după drone/baloane (2026).  
  *Integrare:* Context diplomatic; arhivare.  
  *Atenție:* Axă Belarus–Lituania, relevanță indirectă.
- ✔ **[Ministerul Apărării al Letoniei (mod.gov.lv) – știri despre drone](<https://www.mod.gov.lv/en/news>)** · web · liber · ore · ★☆☆☆☆  
  Comunicate oficiale despre drone intrate din Rusia, prăbușite în Letonia (2026), alerte cell-broadcast.  
  *Integrare:* Comparație de practică (cell broadcast + comunicat MoD); polling.  
  *Atenție:* Multe drone din zona baltică sunt ucrainene deviate de RE – nu se aplică automat la RO.
- ✔ **[ReliefWeb API v2 (OCHA)](<https://apidoc.reliefweb.int/>)** · API · cheie gratuită · ore · ★☆☆☆☆ · flux: <https://api.reliefweb.int/v2/swagger/api>  
  API JSON pentru rapoarte umanitare (Ukraine, Moldova): situation reports, flash updates, hărți.  
  *Integrare:* Endpoint /v2/reports per documentație (neverificat direct), cu filtru country=Ukraine/Moldova și appname aprobat; schema în swagger.  
  *Atenție:* De la 1.11.2025 este necesar un appname pre-aprobat (altfel 403); v1 retras.
- ✔ **[UN News (news.un.org) – știri ONU despre Ucraina](<https://news.un.org/en/>)** · web · liber · ore · ★☆☆☆☆ · flux: <https://news.un.org/feed/subscribe/en/news/region/europe/feed/rss.xml>  
  Știri ONU despre escaladare, atacuri și efecte de propagare regională (inclusiv Consiliul de Securitate LIVE).  
  *Integrare:* Feed RSS regional neconfirmat – se poate folosi Google News RSS pe site:news.un.org.  
  *Atenție:* Redundant cu press.un.org; context.
- ✔ **[UN OCHA Ukraine – rapoarte de situație și 'Humanitarian Situation Snapshot'](<https://www.unocha.org/ukraine>)** · web · liber · zile · ★☆☆☆☆  
  Rapoarte OCHA lunare/bilunare despre impactul atacurilor (inclusiv Odesa), victime civile, infrastructură energetică.  
  *Integrare:* Context post-incident pentru intensitatea atacurilor în sudul Ucrainei; fără integrare în timp real.  
  *Atenție:* Agregat lunar; nu oferă traiectorii.
- ~ **[BTA – Agenția Bulgară de Știri (secțiunea engleză)](<https://www.bta.bg/en>)** · web · liber · ore · ★☆☆☆☆  
  Agenția de stat a Bulgariei: preia rapid comunicatele MoD/Marină despre drone găsite (Byala, Sozopol, Varna).  
  *Integrare:* Google News RSS pe site:bta.bg + cuvinte cheie 'drone'.  
  *Atenție:* Presă de stat; feed RSS propriu neconfirmat. Verificare: BTA există (sunt citate articole despre drone găsite pe plajă). Feedul vechi http://www.bta.bg/en/rss/free e de dinaintea redesignului, deci neconfirmat.
- ~ **[Centrul pentru Contracararea Dezinformării (CPD/ЦПД, Ucraina, pe lângă RNBO)](<https://cpd.gov.ua/en/>)** · web · liber · zile · ★☆☆☆☆  
  Analize și prognoze ale amenințărilor informaționale, inclusiv campaniile care atribuie Ucrainei dronele din RO/MD.  
  *Integrare:* Monitorizare săptămânală a secțiunii Europe; marcaj dezinformare.  
  *Atenție:* Sursă guvernamentală parte în conflict – a se coroba. Verificare: CPD există și publică zilnic; URL-ul exact al articolului neconfirmat. Util pentru dezinformare post-incident, nu pentru avertizare.
- ~ **[Comisia Europeană – Action Plan on Drone and Counter-Drone Security / Defence Readiness Roadmap 2030 (Eastern Flank Watch)](<https://defence-industry-space.ec.europa.eu/commission-publishes-action-plan-drone-and-counter-drone-security-2026-02-11_en>)** · PDF · liber · istoric · ★☆☆☆☆  
  Documente-cadru UE: European Drone Defence Initiative și Eastern Flank Watch (calendar 2026–2028), plan anti-dronă COM(2026) 81.  
  *Integrare:* Referință pentru analiză și pentru a urmări când devin operaționale capabilitățile de detecție pe flancul estic.  
  *Atenție:* Documente de politică, nu date operative. Verificare: Document static de politică (COM(2026) 81), nu un feed. Folosește-l doar ca context. Nu l-am putut verifica independent.
- ~ **[Consiliul UE – RSS comunicate de presă](<https://www.consilium.europa.eu/en/press/press-releases/>)** · RSS · liber · ore · ★☆☆☆☆ · flux: <https://www.consilium.europa.eu/en/rss/pressreleases.ashx>  
  Comunicate Consiliul UE/Consiliul European: sancțiuni, concluzii despre războiul Rusiei, apărare aeriană a flancului estic.  
  *Integrare:* Abonare RSS direct în agregator; filtru 'drone/airspace/Romania/Moldova'.  
  *Atenție:* Volum mare, relevanță scăzută pentru avertizare; context politic. Verificare: Feedul pressreleases.ashx apare în ~69 de proiecte GitHub, dar nu l-am putut accesa direct. Varianta /en/press/press-releases/rss.xml dădea 404 (martie 2026). Util doar ca context/sancțiuni.
- ~ **[ECFR – 'Buzzkill: How to defend Europe against drones'](<https://ecfr.eu/>)** · web · liber · istoric · ★☆☆☆☆  
  Analiză ECFR cu hartă a survolărilor de infrastructură critică și a incursiunilor pe flancul estic din aug. 2024.  
  *Integrare:* Referință pentru raportul de context.  
  *Atenție:* Instantaneu la data publicării. Verificare: ECFR activ; publicația «Buzzkill» neconfirmată independent. Feed ecfr.eu/feed/ neconfirmat. Doar context.
- ~ **[ERCC Portal (DG ECHO) – hărți zilnice și produse ECHO](<https://erccportal.jrc.ec.europa.eu/ECHO-Products/Maps>)** · hartă · liber · zile · ★☆☆☆☆ · flux: <https://erccportal.jrc.ec.europa.eu/API/ERCC/Maps/GetPagedItems>  
  Hărți ECHO (Ucraina, Moldova), răspuns UCPM; ECHO Daily Flash public a fost întrerupt la 18.05.2026.  
  *Integrare:* Doar context/arhivă; descărcare hărți PDF prin API/ERCC/Maps/DownloadPublicMap.  
  *Atenție:* Produsul Flash public nu mai există; actualizări rare pe MD/UA. Verificare: ECHO Flash a fost întrerupt (18 mai 2026, conform pasului anterior). Hărțile ECHO par să continue. Endpointul API e folosit de importatorul ReliefWeb. Activitatea curentă nu e confirmată.
- ~ **[Estonia – kriis.ee (informare publică în criză, alerte de drone)](<https://www.kriis.ee/en>)** · web · liber · minute · ★☆☆☆☆  
  Portal guvernamental de criză: anunțuri despre alerte de drone trimise pe județe și încheierea pericolului.  
  *Integrare:* Model pentru mesaje post-alertă; polling știri.  
  *Atenție:* Doar Estonia. Verificare: Portalul oficial de criză al Estoniei (aplicația „Ole valmis!”, alerte) există. Știrile despre alerta de dronă vin doar de la pasul anterior. Folosește-l ca analog sau pentru lecții învățate.
- ~ **[EUROCONTROL – News & press releases](<https://www.eurocontrol.int/news/eurocontrol-and-easa-release-electronic-conspicuity-use-cases-safer-shared-airspace>)** · web · liber · zile · ★☆☆☆☆  
  Știri EUROCONTROL: perturbări ale traficului (drone la aeroporturi), rapoarte lunare ale Network Manager.  
  *Integrare:* Monitorizare lunară a rapoartelor NM pentru închideri/perturbări în regiune.  
  *Atenție:* Fără date despre incidente militare; RSS neconfirmat. Verificare: URL-ul dat e o singură știre, iar pagina de listă nu e confirmată. Nu se suprapune cu NOP/EAD din catalog. Folosește-l doar ca context.
- ~ **[Forțele Armate ale Lituaniei (kariuomene.lt) – știri](<https://kariuomene.lt/en/newsevents/lithuania-hosted-international-air-and-missile-defence-conference/26700>)** · web · liber · ore · ★☆☆☆☆  
  Știri oficiale despre misiunea NATO Baltic Air Policing (inclusiv F-16 românești la Šiauliai), apărare anti-dronă.  
  *Integrare:* Context comparativ pentru reacția NATO la drone; polling săptămânal.  
  *Atenție:* Incidente LT (din Belarus) – altă axă decât Iași. Verificare: Site-ul oficial al Forțelor Armate ale Lituaniei există. Activitatea curentă nu am putut-o confirma independent. Feedul MApN LT e kam.lt/feed/ (alt site, neconfirmat).
- ~ **[Forțele Navale ale Bulgariei (navy.mod.bg)](<https://navy.mod.bg/?page_id=291>)** · web · liber · zile · ★☆☆☆☆  
  Știri ale Marinei bulgare: neutralizarea dronelor eșuate pe plaje, statistici (peste 100 drone/resturi într-un an).  
  *Integrare:* Context pentru componenta maritimă a rutelor Shahed/Gerbera prin Marea Neagră.  
  *Atenție:* Site WordPress cu datare neclară; verificare manuală. Verificare: Subsite-ul Forțelor Navale BG pare să existe. Nu am putut verifica nici calea, nici activitatea. Folosește-l pentru drone găsite pe plajele de la Marea Neagră.
- ~ **[HQ Multinational Corps South-East (MNC-SE, Sibiu) și MND-SE (București)](<https://mncse.ro/mnd-se/>)** · web · liber · zile · ★☆☆☆☆  
  Site-ul comandamentului NATO de corp din Sibiu (controlează forțele terestre NATO din RO/BG) și pagina MND-SE.  
  *Integrare:* Monitorizare lunară (WordPress, posibil /feed – neconfirmat) pentru exerciții și dispunerea forțelor; context pentru analiză.  
  *Atenție:* Fără informații despre incidente aeriene în timp real; ultimele știri văzute sunt din 2025. Verificare: URL-ul apare în căutarea anterioară, dar nu l-am putut reaccesa. Relevanța e mică: comunicatele vin cu întârziere.
- ~ **[Hybrid CoE (Helsinki) – publicații despre amenințări hibride](<https://www.hybridcoe.fi/publications>)** · PDF · liber · istoric · ★☆☆☆☆  
  Centrul de excelență UE–NATO: manual despre amenințări hibride maritime (drone lansate de pe tancuri, oct. 2026), raport JRC 'Defending Europe against hybrid warfare'.  
  *Integrare:* Referință metodologică pentru atribuire și răspuns.  
  *Atenție:* Fără date operative. Verificare: Hybrid CoE există; pagina /publications plauzibilă, neconfirmată. Doar fundal/analiză.
- ~ **[ICAO – Newsroom (decizii Consiliu/Adunare)](<https://www.icao.int/news/icao-assembly-condemns-gnss-radio-frequency-interference-originating-dprk-and-russian>)** · web · liber · zile · ★☆☆☆☆  
  Decizii ICAO: condamnarea interferențelor GNSS din Rusia (2025), încălcarea spațiului aerian al Ucrainei.  
  *Integrare:* Arhivare ca referință juridică pentru rapoartele post-incident.  
  *Atenție:* Rar, fără date operative. Verificare: Comunicatul ICAO despre interferențele GNSS e plauzibil (Adunarea a 42-a). Pagina de listă a newsroom-ului nu e confirmată. Doar context.
- ~ **[IISS – 'The Scale of Russian Sabotage Operations Against Europe' (set de date 2018–2025)](<https://www.iiss.org/globalassets/media-library---content--migration/files/research-papers/2025/08/pub25-095-the-scale-of-russian-sabotage-operations.pdf>)** · PDF · liber · istoric · ★☆☆☆☆  
  Set de date IISS al activităților hibride rusești în Europa, pe țară/an/metodă.  
  *Integrare:* Context istoric; nu se integrează automat.  
  *Atenție:* Acoperă până în iunie 2025. Verificare: Raport static (2025), fără feed; calea e plauzibilă (același tipar ca pub25-094) dar neconfirmată direct. Relevanță: fundal.
- ~ **[Lituania – sistemul public de avertizare la drone (aplicația LT72, sirene)](<https://lt72.lt>)** · aplicație · liber · timp real · ★☆☆☆☆  
  Sistem cu alertă 'roșie'/'galbenă' pentru drone, sirene și aplicația LT72; prima alertă aeriană reală la 20.05.2026.  
  *Integrare:* Studiu de caz pentru designul alertelor (lecții: căderea aplicației, mesaje doar în lituaniană).  
  *Atenție:* Doar pentru Lituania; sursa citată este presa publică LRT. Verificare: Portalul oficial e lt72.lt. Un ghid public menționează aplicația LT72 care trimite alerte. URL-ul dat e un articol LRT. Relevanță mică pentru Iași (doar ca lecții învățate).
- ~ **[MAE Belarus (mfa.gov.by) – declarații despre drone](<https://mfa.gov.by/en/press/news_mfa/ed90e8afb9751e2a.html>)** · web · liber · zile · ★☆☆☆☆  
  Declarații oficiale belaruse despre drone/încălcări (acuzații la adresa Lituaniei).  
  *Integrare:* Doar pentru a documenta narațiunea oficială opusă în analiza post-incident; NU ca sursă de confirmare.  
  *Atenție:* Context, credibilitate scăzută / propagandă (regim aliat Kremlinului). Verificare: Sursă de stat a Belarusului, aliniată Kremlinului: admisă DOAR ca «context, credibilitate scăzută / propagandă» – această mențiune trebuie pusă la «cautions». Site posibil inaccesibil din UE.
- ~ **[Ministerul Apărării al Slovaciei (mosr.sk)](<https://www.mosr.sk/>)** · web · liber · zile · ★☆☆☆☆  
  Comunicate despre monitorizarea 24/7 a spațiului aerian la granița cu Ucraina și geo-zone pentru drone.  
  *Integrare:* Context regional; verificare lunară.  
  *Atenție:* Știri rare despre incidente; limba slovacă. Verificare: Site-ul MO slovac există; URL-ul exact al articolului 51336 nu apare în dovezi – folosește rădăcina sau pagina 56702 văzută de producător. Relevanță indirectă pentru Iași.
- ~ **[Ministerul Apărării al Ungariei (honvedelem.hu)](<https://honvedelem.hu/hirek/katonai-egyeztetes-a-magyar-drontevekenyseget-erinto-ukran-allitasokrol.html>)** · web · liber · ore · ★☆☆☆☆  
  Comunicate ale Armatei Ungare (ex. disputa cu Ucraina despre drone la granița Transcarpatia, 2025).  
  *Integrare:* Context regional (atacuri rusești în Transcarpatia, 2026); polling lunar.  
  *Atenție:* Poziții politice; limba maghiară. Verificare: Site-ul oficial MApN al Ungariei există. Vechile feeduri rss_b?c=… sunt de dinaintea redesignului, deci neconfirmate. Relevanță mică (context regional).
- ~ **[Ministerul Apărării Naționale al Turciei (MSB) – briefing-uri săptămânale](<https://www.msb.gov.tr/>)** · web · liber · zile · ★☆☆☆☆  
  Briefing-uri de presă săptămânale MSB (ex. drona doborâtă de F-16 în dec. 2025, UAV probabil rusesc eșuat la Ordu, feb. 2026).  
  *Integrare:* Context Marea Neagră; verificare săptămânală.  
  *Atenție:* În limba turcă; nu atribuie mereu originea; cont X neconfirmat. Verificare: URL-ul dat e o singură știre de tip slide. Briefingurile săptămânale MSB există, dar pagina lor de listă nu e confirmată. Relevant pentru drone în Marea Neagră.
- ~ **[OHCHR HRMMU – Protection of Civilians (actualizări lunare)](<https://ukraine.ohchr.org/en/reports/protection-of-civilians>)** · PDF · liber · zile · ★☆☆☆☆  
  Victime civile verificate lunar de Misiunea ONU de monitorizare a drepturilor omului (pe regiuni și tipuri de arme, inclusiv drone cu rază lungă).  
  *Integrare:* Import lunar al cifrelor pentru analiza intensității campaniei de drone.  
  *Atenție:* Cifre minime, verificate cu întârziere de ~2 săptămâni. Verificare: Site-ul HRMMU există și publică actualizări lunare. Calea /en/reports/protection-of-civilians nu e confirmată. Util după incident.
- ~ **[Parlamentul European – feeduri RSS (comunicate de presă)](<https://www.europarl.europa.eu/at-your-service/en/stay-informed/rss-feeds>)** · RSS · liber · ore · ★☆☆☆☆ · flux: <https://www.europarl.europa.eu/rss/doc/press-releases/en.xml>  
  Feeduri XML: toate comunicatele, plen, comisii (AFET/SEDE) – rezoluții despre încălcări ale spațiului aerian și flancul estic.  
  *Integrare:* Se iau URL-urile XML de pe pagina RSS PE și se filtrează după cuvinte cheie.  
  *Atenție:* URL exact al feedului 'Press releases – All' neconfirmat (feed neconfirmat); relevanță de context. Verificare: Pagina de feeduri RSS există. URL-ul exact al feedului de comunicate nu e confirmat. Fără „.xml” dă 404. HowTheyVote folosește …/rss/doc/press-releases-plenary/en.xml.
- ~ **[PAŻP / PANSA (Polonia) – restricții de spațiu aerian în estul Poloniei](<https://www.pansa.pl/ograniczenie-ruchu-lotniczego-we-wschodniej-czesci-polski/>)** · web · liber · zile · ★☆☆☆☆  
  Anunțuri despre zonele restricționate EP R129/R130 la granița cu UA/BY (interzicere drone civile, activare 24h).  
  *Integrare:* Referință pentru cum se definesc zone de restricție la frontieră; comparat cu NOTAM-urile ROMATSA.  
  *Atenție:* Valabilitate limitată (R130 până la 9.06.2026); verificare prin NOTAM. Verificare: PANSA există și publică restricții (de ex. zona EP R130). Pagina anume nu am putut-o verifica. Datele utile sunt în AIP/AUP.
- ~ **[PISM (Institutul Polonez de Afaceri Internaționale) – buletine](<https://www.pism.pl/>)** · PDF · liber · zile · ★☆☆☆☆ · flux: <https://www.pism.pl/rss>  
  Buletine PISM despre potențialul de escaladare rusesc, Eastern Sentry, drone lansate de pe nave din 'flota din umbră'.  
  *Integrare:* Lectură lunară pentru context.  
  *Atenție:* Unele doar în poloneză. Verificare: PISM există; PDF-ul Biuletyn nr 65 (3199) din 28.09.2026 neconfirmat direct. Feed https://www.pism.pl/rss neconfirmat.
- ~ **[U.S. European Command (EUCOM) – Media Room](<https://www.eucom.mil/pressrelease/42450/eucom-romanian-defense-officials-discuss-security-cooperation-in-romania-black-sea>)** · web · liber · zile · ★☆☆☆☆  
  Comunicate și articole EUCOM despre România/Marea Neagră (Aegis Ashore Deveselu, MQ-9 Câmpia Turzii, bombardiere la M. Kogălniceanu).  
  *Integrare:* Feed confirmat doar pentru imagini: https://www.eucom.mil/syndication-feed/rss/images (și /atom/images); feed-uri pentru press releases neconfirmate – polling pe pagina Media Room.  
  *Atenție:* Nu raportează incidente cu drone în RO; sursă de context al posturii SUA. Domeniu blocat din sandbox (verificat doar prin căutare). Verificare: Comunicatul și fluxul RSS de imagini apar în căutarea anterioară, dar nu le-am putut reaccesa. Un RSS pentru comunicatele de presă nu e confirmat.
- ~ **[Wikipedia EN – '2025 European drone sightings'](<https://en.wikipedia.org/wiki/2025_European_drone_sightings>)** · web · liber · istoric · ★☆☆☆☆  
  Lista survolărilor de drone deasupra aeroporturilor/bazelor din Europa (Copenhaga, München, Berlin, Bruxelles) 2025.  
  *Integrare:* Index pentru contextul hibrid; nu se integrează automat.  
  *Atenție:* Wikipedia – doar index; multe incidente neatribuite. Verificare: Titlul exact «2025 European drone sightings» neconfirmat (pot exista variante, ex. «2025 Danish drone incidents»). Fundal.
- ~ **[Wikipedia EN – '2025 Russian drone incursion into Poland'](<https://en.wikipedia.org/wiki/2025_Russian_drone_incursion_into_Poland>)** · web · liber · istoric · ★☆☆☆☆  
  Articol despre incursiunea din 9–10.09.2025 (≈19–23 drone, multe Gerbera), articolul 4 NATO, Eastern Sentry.  
  *Integrare:* Studiu de caz pentru scenariul de incursiune masivă cu momeli.  
  *Atenție:* Wikipedia – doar index. Verificare: Articol Wikipedia aproape sigur existent (incursiunea din sept. 2025); neaccesat. Fundal/lecții.
- ~ **[Wikipedia EN – '2026 Ukrainian drone incursions into the Baltic states'](<https://en.wikipedia.org/wiki/2026_Ukrainian_drone_incursions_into_the_Baltic_states>)** · web · liber · zile · ★☆☆☆☆  
  Cronologia dronelor ucrainene deviate de războiul electronic rusesc în Estonia/Letonia/Lituania/Finlanda în 2026.  
  *Integrare:* Index pentru analiza fenomenului de deviere prin RE (relevant și pentru drone deviate spre RO).  
  *Atenție:* Wikipedia – doar index. Verificare: Articolul a fost văzut într-o etapă anterioară; neconfirmat acum. Fundal; titlul se referă la drone ucrainene deviate, nu rusești.

## Comunități locale, rețele sociale, aplicații

- ~ **[Armata Națională a R. Moldova – canal Telegram (@MDNationalArmy)](<https://t.me/MDNationalArmy>)** · Telegram · liber · minute · ★★★★★ · flux: <https://t.me/s/MDNationalArmy>  
  Canal Telegram al Armatei Naționale/MApărării MD: confirmări de survol, traiectorii de drone prin raioane (ex. Bălți → Ungheni), dezmințiri.  
  *Integrare:* t.me/s/MDNationalArmy prin RSSHub/parsare HTML; corelare cu army.md (deja în catalog).  
  *Atenție:* Comunicatele pot veni după ieșirea dronei din spațiul MD; uneori dezmințiri ulterioare. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – handle găsit în amonte prin URL de postare (/824); feed distinct de army.md (permis). De confirmat că e canalul oficial al Armatei Naționale/MApN MD.
- ~ **[Gruparea de forțe „Sud” (Сили оборони півдня) – Telegram](<https://t.me/s/SJTF_Odes>)** · Telegram · liber · minute · ★★★★☆  
  Canalul oficial al grupării de forțe „Південь” (sudul UA, inclusiv Odesa): atacuri cu Shahed asupra regiunii Odesa/Dunăre, doborâri.  
  *Integrare:* t.me/s/SJTF_Odes prin RSSHub; filtre «Ізмаїл», «Рені», «Шахед».  
  *Atenție:* Comunicări militare, adesea agregate post-factum. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – titlul din căutare („Угруповання «Південь»”) diferă de numele intrării („Сили оборони півдня”); canalul poate fi redenumit. De confirmat.
- ~ **[ISU Galați – Facebook](<https://www.facebook.com/isugalati/>)** · rețea socială · liber · minute · ★★★★☆  
  Pagina oficială ISU Galați (~10.800 urmăritori): intervenții, mesaje după RO-Alert și căderi de drone în Galați.  
  *Integrare:* Monitorizare manuală/notificări; corelare cu RO-Alert pentru jud. Galați.  
  *Atenție:* Fără API; nu face scraping. Verificare: Nu e duplicat (catalogul existent are doar ISU IS/BT/SV/VS/NT). Pagină plauzibilă; fără API, fără scraping.
- ~ **[Вінницька ОДА/ОВА – canal Telegram](<https://t.me/s/VinnytsiaODA>)** · Telegram · liber · minute · ★★★★☆  
  Canalul administrației militare Vinnîțea: statusuri de alertă pe raioane, consecințe atacuri; complementar site-ului vin.gov.ua (deja în catalog).  
  *Integrare:* t.me/s/VinnytsiaODA prin RSSHub; filtre pe raioanele Mohyliv-Podilskyi/Tulchyn.  
  *Atenție:* Site-ul vin.gov.ua e deja în catalog; acesta e feed-ul Telegram distinct. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – feed Telegram distinct de vin.gov.ua din catalog (permis); de confirmat că e canalul oficial OVA.
- ~ **[Могилів-Подільська міська рада – canal Telegram](<https://t.me/s/mog_pod_mr>)** · Telegram · liber · minute · ★★★★☆  
  Canal oficial al orașului Mohyliv-Podilskyi (pe Nistru, vizavi de Otaci, MD): alerte și știri operative; punct de intrare al dronelor din Vinnîțea spre nordul MD.  
  *Integrare:* t.me/s/mog_pod_mr; alertă internă când apare «БпЛА»/«загроза».  
  *Atenție:* Canal municipal, nu militar. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – Moghilău-Podilskîi e la granița cu MD (Otaci), relevant; handle din căutare, de confirmat.
- ~ **[Суспільне Одеса – canal Telegram](<https://t.me/s/suspilneodesa>)** · Telegram · liber · minute · ★★★★☆  
  Radiodifuzorul public regional (~47.000 abonați): postări operative despre alerte aeriene și drone în raioanele Odesa, inclusiv Bugeac/Dunăre.  
  *Integrare:* t.me/s/suspilneodesa; extragere raioane (Ізмаїльський, Болградський, Білгород-Дністровський).  
  *Atenție:* Media, nu sursă primară; în limba ucraineană. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – canal regional Suspilne Odesa, plauzibil activ.
- ~ **[Суспільне Чернівці – canal Telegram](<https://t.me/s/suspilne_chernivtsi>)** · Telegram · liber · minute · ★★★★☆  
  Publică alerte pe raioane, inclusiv raionul Dnistrovskyi (Novodnistrovsk, Sokyriany) – vecin cu Briceni/Ocnița (MD) – cu nivel «dronova zahroza».  
  *Integrare:* t.me/s/suspilne_chernivtsi; regex pe «Дністровський район».  
  *Atenție:* Media; reia surse oficiale. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – Suspilne Cernăuți, fragment de căutare menționează alerte pe raionul Nistru; plauzibil activ.
- ~ **[Expresul.md (Ungheni) – canal Telegram](<https://t.me/s/expresul>)** · Telegram · liber · minute · ★★★☆☆  
  Canalul Telegram al ziarului regional Expresul din Ungheni (MD); știri locale din raionul de frontieră cu Iași, inclusiv incidente cu drone.  
  *Integrare:* Citire t.me/s/expresul (previzualizare publică) sau RSSHub /telegram/channel/expresul; filtrare pe «dronă», «explozie», «Sculeni».  
  *Atenție:* Media locală; poate prelua informații neconfirmate. Verificare: Handle Telegram «expresul» neconfirmat independent – de reverificat înainte de integrare (dacă nu se confirmă → not_found). Ziarul Expresul (Ungheni) există; feed t.me/s neconfirmat.
- ~ **[Iasi TV Life – pagina Facebook](<https://www.facebook.com/iasitvlife.ro/>)** · rețea socială · liber · minute · ★★★☆☆  
  Televiziune locală din Iași (~254.000 urmăritori pe FB), cu transmisii live; reacționează rapid la RO-Alert în Iași.  
  *Integrare:* Monitorizare manuală / notificări FB; site iasitvlife.ro.  
  *Atenție:* Media; nu sursă primară. Verificare: Neverificat independent (buget de căutare epuizat; facebook.com inaccesibil). Iasi TV Life e televiziune locală reală din Iași; pagina FB plauzibilă. Fără RSS public; scraping-ul FB încalcă ToS – doar monitorizare manuală sau prin site-ul propriu. Nu e duplicat (nu figurează în presa regională din catalog). Relevanță 2.
- ~ **[IGSU al MAI (R. Moldova) – Facebook](<https://www.facebook.com/dse.md/>)** · rețea socială · liber · minute · ★★★☆☆  
  Pagina oficială a Inspectoratului General pentru Situații de Urgență din Moldova: intervenții la resturi de drone, avertizări.  
  *Integrare:* Monitorizare manuală; site igsu.gov.md.  
  *Atenție:* Nu există canal Telegram IGSU MD confirmat; fără API FB. Verificare: NEVERIFICAT (buget WebSearch epuizat; facebook.com blocat) – dse.md e domeniul IGSU MD, pagina FB plauzibilă. Fără feed; doar monitorizare manuală. Site-ul dse.md poate avea comunicate (feed neconfirmat).
- ~ **[Instituția Prefectului – județele Botoșani, Vaslui, Tulcea (Facebook)](<https://www.facebook.com/prefecturabotosani/>)** · rețea socială · liber · minute · ★★★☆☆  
  Paginile oficiale ale prefecturilor Botoșani, Vaslui (facebook.com/institutiaprefectuluivaslui) și Tulcea (facebook.com/prefectTulcea); anunță încheierea alertelor și ședințele CJSU.  
  *Integrare:* Monitorizare manuală a celor trei pagini.  
  *Atenție:* Pagina «Tulcea 2017-2022» e arhivă, nu oficială; folosește prefectTulcea. Verificare: NEVERIFICAT (buget WebSearch epuizat; facebook.com blocat) – intrarea grupează 3 pagini (Botoșani, Vaslui, Tulcea); de separat în 3 intrări. Fără feed; nu scrape-ui, doar monitorizare manuală.
- ~ **[Instituția Prefectului – județul Galați (Facebook)](<https://www.facebook.com/prefecturagalati/>)** · rețea socială · liber · minute · ★★★☆☆  
  Pagina oficială a Prefecturii Galați (~11.400 urmăritori); comunicate CJSU, încetarea alertelor.  
  *Integrare:* Monitorizare manuală.  
  *Atenție:* Fără API. Verificare: NEVERIFICAT (buget WebSearch epuizat; facebook.com blocat în sandbox) – pagină publică plauzibilă a Prefecturii Galați. Fără feed; nu scrape-ui, doar monitorizare manuală / Graph API autorizat.
- ~ **[ISU „Delta” Tulcea – Facebook](<https://www.facebook.com/isudeltatulcea/>)** · rețea socială · liber · minute · ★★★☆☆  
  Pagina oficială ISU Tulcea (Delta); județul cu cele mai multe resturi de drone găsite (Plauru, Isaccea, Luncavița).  
  *Integrare:* Monitorizare manuală; site isutl.igsu.ro.  
  *Atenție:* Fără API; postări după evenimente. Verificare: Nu e duplicat (ISU Tulcea lipsește din catalogul existent). Pagină plauzibilă; fără API, fără scraping.
- ~ **[Kontur (kontur.systems) – hartă OSINT a amenințărilor aeriene + bot Telegram](<https://kontur.systems>)** · hartă · liber · timp real · ★★★☆☆  
  Sistem ucrainean de vizualizare OSINT (drone/rachete) din mesaje text publice, cu timelapse; versiune web și bot @kontur_map_bot.  
  *Integrare:* Vizualizare manuală în camera de operațiuni; bot t.me/kontur_map_bot pentru notificări.  
  *Atenție:* Coordonate aproximative calculate din mențiuni, nu radar; neoficial. Verificare: NEVERIFICAT (buget WebSearch epuizat; kontur.systems blocat) – domeniul e dedus doar din articolul dev.ua; domeniu și bot Telegram neconfirmate.
- ~ **[NOELREPORTS – Bluesky / Mastodon / Telegram](<https://bsky.app/profile/noelreports.com>)** · rețea socială · liber · minute · ★★★☆☆ · flux: <https://bsky.app/profile/noelreports.com/rss>  
  Cont OSINT/media despre războiul RU-UA, prezent pe Bluesky, Mastodon (@noelreports@mstdn.social) și Telegram (t.me/s/noel_reports); reia rapid bilanțurile Forțelor Aeriene UA și incidente cu Shahed.  
  *Integrare:* RSS Bluesky: https://bsky.app/profile/noelreports.com/rss (format /rss documentat); Mastodon: https://mstdn.social/@noelreports.rss (format .rss documentat); Telegram t.me/s/noel_reports.  
  *Atenție:* Agregator, nu sursă primară; verifică cu @kpszsu; conturile Bluesky pot fi compromise. Verificare: NEVERIFICAT (buget WebSearch epuizat; bsky/mastodon/t.me blocate) – NOELREPORTS e cont OSINT cunoscut; formatul /rss Bluesky e documentat. Agregator secundar, de coroborat.
- ~ **[Poliția Republicii Moldova – canal Telegram](<https://t.me/Politia_Republicii_Moldova>)** · Telegram · liber · minute · ★★★☆☆ · flux: <https://t.me/s/Politia_Republicii_Moldova>  
  Canalul oficial IGP Moldova; a anunțat prăbușiri de drone (ex. Ștefan Vodă) și perimetre restricționate.  
  *Integrare:* t.me/s/Politia_Republicii_Moldova; filtru pe «aparat de zbor», «dronă».  
  *Atenție:* Volum mare de postări nerelevante (trafic, infracțiuni). Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – Poliția MD raportează pe Telegram (Qatar Tribune), dar handle-ul exact Politia_Republicii_Moldova nu a putut fi reconfirmat.
- ~ **[Primăria comunei Golăiești (Iași) – pagina Facebook](<https://www.facebook.com/PrimariacomuneiGolaiesti/>)** · rețea socială · liber · ore · ★★★☆☆  
  Pagina oficială a primăriei Golăiești, comună de pe Prut spre care a fost raportată drona ieșită din MD pe la Zagarancea (incidentul cu RO-Alert în Iași). Anunțuri locale, posibile mesaje despre resturi/zone închise.  
  *Integrare:* Monitorizare manuală sau notificări FB «Urmărește»; fără API public pentru pagini fără token; nu face scraping.  
  *Atenție:* Postări rare, nu în timp real; doar confirmare post-incident. Respectă ToS Facebook. Verificare: Pagină FB plauzibilă (comună pe Prut, pe traseul Zagarancea→Golăiești); doar monitorizare manuală, fără scraping (ToS).
- ~ **[Primăria comunei Sculeni (r. Ungheni, MD) – Facebook](<https://www.facebook.com/primariaSculeni/>)** · rețea socială · liber · ore · ★★★☆☆  
  Pagina primăriei Sculeni (MD), punct de trecere a frontierei spre Sculeni-Iași; ~6.600 aprecieri; anunțuri locale.  
  *Integrare:* Monitorizare manuală; site sculeni.comuna.md.  
  *Atenție:* Postări neregulate; nu e sursă de alertă timpurie. Verificare: Pagină plauzibilă; doar monitorizare manuală, fără scraping.
- ~ **[Primăria Municipiului Galați – Facebook](<https://www.facebook.com/primariagl/>)** · rețea socială · liber · ore · ★★★☆☆  
  Pagina oficială a Primăriei Galați (~33.000 urmăritori); a comunicat după impactul dronei pe un bloc (29 mai 2026).  
  *Integrare:* Monitorizare manuală.  
  *Atenție:* Nu emite alerte aeriene; comunicare post-incident. Verificare: Handle «primariagl» neconfirmat independent; pagină plauzibilă; comunicare post-incident.
- ~ **[Primăria municipiului Ungheni (R. Moldova) – Facebook](<https://www.facebook.com/ungheni.md/>)** · rețea socială · liber · ore · ★★★☆☆  
  Pagina oficială a Primăriei Ungheni (MD), oraș de frontieră pe Prut, opus comunei Ungheni-Iași; canal oficial de consultare/comunicare.  
  *Integrare:* Monitorizare manuală; corelare cu site-ul primaria.ungheni.md.  
  *Atenție:* Nu e canal de alertă; utilă pentru confirmări locale (resturi, evacuări). Verificare: Probabil pagina oficială a Primăriei Ungheni (MD); doar monitorizare manuală.
- ~ **[Primăria Orașului Isaccea (Tulcea) – Facebook](<https://www.facebook.com/primaria.oras.isaccea/>)** · rețea socială · liber · ore · ★★★☆☆  
  Pagina primăriei Isaccea (Dunăre, vizavi de Orlivka/Izmail); zonă cu căderi frecvente de resturi de drone.  
  *Integrare:* Monitorizare manuală; corelare cu IzmailRDA.  
  *Atenție:* Postări neregulate; utilă pentru confirmări post-atac. Verificare: Pagină plauzibilă; Isaccea e zonă cu resturi frecvente de drone; monitorizare manuală.
- ~ **[Ukraine Siren Alerts (UASA) – site, boți sociali, SMS/e-mail](<https://uasa.io>)** · web · liber · timp real · ★★★☆☆  
  Serviciu nonprofit (după modelul israelian Red Color) cu boți pe rețele sociale, hartă de sirene și abonare SMS/e-mail pe regiuni ucrainene; hartă de adăposturi.  
  *Integrare:* Abonare e-mail pe regiunile Odesa/Vinnîțea/Cernăuți → parsare în n8n; boții sociali ca redundanță.  
  *Atenție:* Voluntar, dependent de donații; preia date municipale. Verificare: NEVERIFICAT (buget WebSearch epuizat; uasa.io/wikipedia blocate) – proiect cu articol Wikipedia, dar domeniul uasa.io și activitatea curentă nu sunt confirmate; posibil inactiv.
- ~ **[Бессарабiя INFORM – canal regional (Telegram)](<https://t.me/s/bessarabiainformcom>)** · Telegram · liber · minute · ★★★☆☆  
  Canal de știri regionale din sudul Basarabiei (Izmail, Reni, Bolhrad, Bilhorod-Dnistrovskyi): atacuri, explozii, viața comunităților dunărene.  
  *Integrare:* t.me/s/bessarabiainformcom; filtre pe localități de pe Dunăre.  
  *Atenție:* Media neoficială; verifică încrucișat. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – canal media regional Basarabia (sudul reg. Odesa); credibilitate de evaluat.
- ~ **[Болградська РДА – canal Telegram](<https://t.me/s/bolgradrda_news>)** · Telegram · liber · minute · ★★★☆☆  
  Canalul administrației raionului Bolhrad (sudul Basarabiei, la granița cu MD/Cahul): avertizări și consecințe atacuri.  
  *Integrare:* t.me/s/bolgradrda_news.  
  *Atenție:* Multe postări administrative. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – RDA Bolhrad (raion acum ca RVA); handle din căutare, de confirmat.
- ~ **[Думська (Dumskaya, Odesa) – canal Telegram](<https://t.me/s/OdessaDumskayaNet>)** · Telegram · liber · minute · ★★★☆☆  
  Publicație locală din Odesa; corespondenții raportează explozii și atacuri în regiune în timp real (există și t.me/s/dumskaya_ua).  
  *Integrare:* t.me/s/OdessaDumskayaNet; filtre «вибухи», «дрони».  
  *Atenție:* Media locală, nu oficială. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – două handle-uri (OdessaDumskayaNet și dumskaya_ua); de confirmat care e cel oficial/activ.
- ~ **[Измаил СИТИ / Мій Ізмаїл – canale comunitare Izmail](<https://t.me/s/izmacity>)** · Telegram · liber · minute · ★★★☆☆  
  Canale comunitare din Izmail (vizavi de Isaccea/Tulcea): semnalări rapide de explozii/drone deasupra portului; și t.me/s/moy_izmail1303.  
  *Integrare:* t.me/s/izmacity, t.me/s/moy_izmail1303; semnal slab, corelat cu IzmailRDA.  
  *Atenție:* Neoficiale; datele unor postări pot fi vechi. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – două canale comunitare (izmacity, moy_izmail1303) într-o intrare; neoficiale, risc de zvonuri. De separat/confirmat.
- ~ **[ТРИВОГА ВІННИЦЯ – canal comunitar de alerte](<https://t.me/s/trevoga_vinnitsa_noviny>)** · Telegram · liber · timp real · ★★★☆☆  
  Canal neoficial ce publică alerte pe raioanele Vinnîței cu niveluri de amenințare și direcții de deplasare.  
  *Integrare:* t.me/s/trevoga_vinnitsa_noviny; doar ca semnal secundar.  
  *Atenție:* Neoficial; texty.org.ua avertizează că unele canale de «monitorizare» folosesc clickbait. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – canal comunitar neoficial; util doar pentru coroborare.
- ~ **[„Аккерман Офіційний” – Bilhorod-Dnistrovskyi (Telegram)](<https://t.me/s/akkermanofficial>)** · Telegram · liber · minute · ★★★☆☆  
  Canal oficial al orașului Bilhorod-Dnistrovskyi (Cetatea Albă): mesaje despre atacuri cu drone și explozii în zonă, la granița cu MD (Ștefan Vodă).  
  *Integrare:* t.me/s/akkermanofficial; corelare cu alertele raionului Білгород-Дністровський.  
  *Atenție:* Caracter «oficial» declarat de canal; de verificat. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – variante de majuscule ale aceluiași handle (handle-urile Telegram nu țin cont de majuscule); canal neoficial/comunitar, de confirmat.
- ~ **[„СП” esp.md (Bălți) – canal Telegram](<https://t.me/s/gazetasp>)** · Telegram · liber · minute · ★★★☆☆  
  Canalul ziarului SP din Bălți (~8.800 abonați): știri din nordul MD, zonă survolată de drone spre Ungheni/Iași.  
  *Integrare:* t.me/s/gazetasp; filtrare în rusă/română («дрон», «беспилотник», «dronă»).  
  *Atenție:* Media locală; poate prelua zvonuri; limba rusă. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – canal al ziarului „СП” Bălți; legătura handle gazetasp ↔ esp.md de confirmat.
- ~ **[#MAExplică – MAE R. Moldova (Telegram)](<https://t.me/s/maeiexplica>)** · Telegram · liber · ore · ★★☆☆☆  
  Canal Telegram al MAE Moldova: poziții oficiale după încălcări ale spațiului aerian (convocări de ambasador, condamnări).  
  *Integrare:* t.me/s/maeiexplica; utilă pentru confirmare oficială post-incident.  
  *Atenție:* Latentă de ore; nu e sursă operațională. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – canal explicativ MAEIE; relevanță mică pentru avertizare (reacții diplomatice post-incident).
- ~ **[112MD – aplicația oficială a Serviciului 112 (R. Moldova)](<https://app.112.md>)** · aplicație · liber · timp real · ★★☆☆☆  
  Aplicația oficială 112MD (lansată 24 mar 2026), adaptată persoanelor cu deficiențe de auz/vedere; canal oficial de raportare a dronelor/resturilor în MD.  
  *Integrare:* Nu e flux de date; de recomandat în ghidul pentru localnici (raportare oficială, nu în grupuri).  
  *Atenție:* Nu există formular public dedicat dronelor; date neaccesibile terților. Verificare: NEVERIFICAT (buget WebSearch epuizat; app.112.md blocat) – aplicația oficială 112MD e pentru apeluri/alerte către cetățeni; feed public neconfirmat.
- ~ **[AMK Mapping – canal Telegram (reconstrucții de traiectorii)](<https://t.me/s/AMK_Mapping>)** · Telegram · liber · ore · ★★☆☆☆  
  Cartograf OSINT independent; a publicat cronologia unei drone reactive de la detecție în UA prin Moldova (Chișinău) spre România.  
  *Integrare:* t.me/s/AMK_Mapping; util pentru analiză post-incident și validarea traseelor.  
  *Atenție:* Reconstrucții de amator; neutralitate nevalidată; nu e sursă oficială. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – AMK Mapping e cartograf OSINT cunoscut (în special pe X); credibilitate variabilă, de folosit doar pentru coroborare.
- ~ **[Apel 112 (România) – aplicația de localizare a apelantului](<https://infocons.ro/apel-112-aplicatia-pentru-localizarea-apelantilor-la-112/>)** · aplicație · liber · timp real · ★★☆☆☆  
  Aplicația STS care transmite locația telefonului în timpul apelului la 112; canalul oficial pentru a raporta drone/resturi observate (MApN cere apel la 112).  
  *Integrare:* Recomandare în materialele pentru localnici; nu oferă date.  
  *Atenție:* Nu există formular online oficial de raportare drone găsit; datele 112 nu sunt publice. Verificare: NEVERIFICAT (buget WebSearch epuizat) – URL-ul e un articol terț (infocons.ro), nu sursa; aplicația doar transmite locația apelantului către STS, nu oferă date publice. Relevanță minimă ca sursă.
- ~ **[Bluesky – feed personalizat „Ukraine OSINT” (@chris.blue) și starter pack „War in Ukraine”](<https://bsky.app/profile/did:plc:cwx2zxldt3uxciob3nxzhkzr/feed/aaab3ry3xg3j4>)** · rețea socială · liber · minute · ★★☆☆☆  
  Feed Bluesky curatoriat cu postări OSINT despre Ucraina; plus starter pack «War in Ukraine (En/Fr)» (bsky.app/starter-pack/antoine.datapolitics.fr/3lb2eiet73e2m) pentru descoperirea conturilor.  
  *Integrare:* Citire manuală sau prin API AT Protocol (app.bsky.feed.getFeed, public).  
  *Atenție:* Curatoriere de terți; calitate variabilă. Verificare: NEVERIFICAT (buget WebSearch epuizat; bsky blocat) – feed-urile custom și starter pack-urile dispar frecvent; fără RSS nativ, necesită API AT Protocol.
- ~ **[Chisinau Live – canal YouTube](<https://www.youtube.com/c/ChisinauLive>)** · cameră publică · liber · timp real · ★★☆☆☆  
  Transmisiuni zilnice din Chișinău («Chisinau Direct – fiecare zi»); confirmare vizuală la survoluri ale capitalei.  
  *Integrare:* Verificare manuală; RSS canal YouTube (feeds/videos.xml?channel_id=…) – ID neconfirmat.  
  *Atenție:* Nu e cameră permanentă garantată. Verificare: Neverificat independent (buget de căutare epuizat; youtube.com inaccesibil). Existența și activitatea canalului /c/ChisinauLive neconfirmate de mine; doar rezultat de căutare raportat anterior. Relevanță 1 (camere oraș, nocturn inutile pentru drone).
- ~ **[Comuna Prisăcani (Iași) – paginile Facebook](<https://www.facebook.com/p/Comuna-Pris%C4%83cani-Jude%C5%A3ul-Ia%C5%9Fi-Rom%C3%A2nia-100071789076359/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagina comunei Prisăcani (pe Prut, la est de Iași); există și «Primaria Prisacani Pagina Oficiala» (facebook.com/primaria.prisacani.37).  
  *Integrare:* Monitorizare manuală.  
  *Atenție:* Statut oficial neconfirmat; primaria.prisacani.37 e posibil profil personal, nu pagină. Verificare: Păstrează doar pagina /p/ a comunei; elimină facebook.com/primaria.prisacani.37 (posibil profil personal, nu pagină oficială).
- ~ **[Comuna Răducăneni (Iași) – pagina oficială Facebook](<https://www.facebook.com/comunaraducanenioficial/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagina oficială a comunei Răducăneni (sudul jud. Iași, spre Prut); există și facebook.com/primariaraducaneni.  
  *Integrare:* Monitorizare manuală.  
  *Atenție:* Mai multe pagini cu nume similar; verifică pe cea oficială. Verificare: Două pagini cu nume similar; confirmă manual care e cea oficială.
- ~ **[Comuna Ungheni (Iași) – pagina Facebook](<https://www.facebook.com/p/Comuna-Ungheni-Iasi-100072079340986/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagina comunei Ungheni-Iași, vecină cu orașul Ungheni (MD) peste Prut, la ~21 km de Iași; anunțuri locale.  
  *Integrare:* Monitorizare manuală; eventual alertă Google pe numele comunei + «dronă».  
  *Atenție:* Pagină comunitară (~530 aprecieri), statut oficial neconfirmat; informații neverificate. Verificare: Pagină comunitară cu statut oficial neconfirmat (~530 aprecieri); relevanță mică; monitorizare manuală.
- ~ **[Consiliul Raional Briceni (MD) – Facebook](<https://www.facebook.com/consiliul.raionalbriceni.7/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagina CR Briceni, raionul care include Lipcani și Criva (frontiera nordică cu RO și UA); există și pagina comunitară «Briceni Nord Moldova» (facebook.com/raionul.briceni).  
  *Integrare:* Monitorizare manuală.  
  *Atenție:* Nu am găsit pagini oficiale separate pentru primăriile Lipcani/Criva. Slug-ul consiliul.raionalbriceni.7 pare profil personal, nu pagină oficială – de verificat. Verificare: NEVERIFICAT (buget WebSearch epuizat; facebook.com blocat) – URL cu sufix „.7” pare profil personal, nu pagină oficială; două URL-uri oferite, de confirmat care e oficial. Fără feed.
- ~ **[Consiliul raional Ungheni (MD) – Facebook](<https://www.facebook.com/ConsiliulraionalUngheni/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagina Consiliului raional Ungheni (APL nivel II), raion străbătut de drone pe ruta Bălănești–Cetireni–Zagarancea spre Iași.  
  *Integrare:* Monitorizare manuală; site crungheni.md.  
  *Atenție:* Comunicare administrativă, nu operativă. Verificare: Pagină plauzibilă; comunicare administrativă, relevanță mică.
- ~ **[InfoCons – harta adăposturilor de protecție civilă (aplicație ONG)](<https://infocons.ro/harta-adaposturilor-pentru-situatii-de-urgenta-din-romania/>)** · hartă · liber · zile · ★★☆☆☆  
  Hartă web + aplicație (Google Play/App Store/AppGallery) cu ~4.500 de adăposturi de protecție civilă, filtrabilă pe județe (inclusiv Iași).  
  *Integrare:* Link în mesajele interne post-alertă; eventual extragere pe județ (?county=iasi) cu acordul ONG-ului.  
  *Atenție:* ONG, nu oficial; date posibil neactualizate față de lista IGSU. Verificare: Neverificat independent în această rundă (buget WebSearch epuizat; infocons.ro inaccesibil din sandbox – ENOTFOUND). Dovezile sunt cele ale agentului anterior; URL-ul cu ?county= sugerează hartă funcțională pe județe. Sursă ONG, nu oficială – sursa oficială rămâne IGSU/DSU (fiipregatit.ro, deja în catalog). Relevanță mică (1–2): informare publică/post-incident, nu avertizare.
- ~ **[Informații Tulcea – pagină comunitară Facebook](<https://www.facebook.com/informatiitulcea/>)** · rețea socială · liber · minute · ★★☆☆☆  
  Pagină comunitară cu știri și semnalări din Tulcea (Isaccea, Plauru, Luncavița), zone cu căderi frecvente de drone.  
  *Integrare:* Monitorizare manuală; doar semnal slab.  
  *Atenție:* Neoficial, neverificat. Verificare: Neverificat independent (buget de căutare epuizat; facebook.com inaccesibil). Pagină comunitară, credibilitate scăzută; relevantă pe axa Dunăre/Izmail (Tulcea), nu pentru Iași. Fără RSS; scraping FB încalcă ToS – doar monitorizare manuală. Relevanță 1–2.
- ~ **[ISW (Institute for the Study of War) – Bluesky](<https://bsky.app/profile/thestudyofwar.bsky.social>)** · rețea socială · liber · ore · ★★☆☆☆ · flux: <https://bsky.app/profile/thestudyofwar.bsky.social/rss>  
  Contul Bluesky al ISW; postări zilnice cu evaluări, inclusiv drone prăbușite în Moldova (ex. 5 drone, inclusiv Banderol, 3 oct).  
  *Integrare:* RSS: https://bsky.app/profile/thestudyofwar.bsky.social/rss; complementar hărții ISW (deja în catalog).  
  *Atenție:* Analiză cu întârziere de ore/zile. Verificare: NEVERIFICAT (buget WebSearch epuizat; bsky blocat) – feed Bluesky distinct de understandingwar.org din catalog (permis); relevanță: analiză post-incident.
- ~ **[nakordoni.eu – cozi și camere live la punctele de frontieră RO-MD-UA](<https://nakordoni.eu/ro/bcp>)** · cameră publică · liber · minute · ★★☆☆☆  
  Agregator cu timpi de așteptare (actualizați la 1–10 min) și camere live la PTF, inclusiv Sculeni–Sculeni (nakordoni.eu/md/ro/bcp/skuleny-moldova-skuleny).  
  *Integrare:* Verificare manuală; schimbări bruște pot semnala închideri.  
  *Atenție:* Neoficial; preia date de la poliții de frontieră. Verificare: Neverificat independent (buget de căutare epuizat; nakordoni.eu inaccesibil – ENOTFOUND). URL-urile de dovadă (pagină Sculeni, statistici) par structural plauzibile. Sursă neoficială (agregator); camere de frontieră publice – OK. Relevanță 1–2 (context/proxy închideri).
- ~ **[News.Ungheni.org – pagină locală de știri (MD)](<https://www.facebook.com/news.ungheni.org/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagină de știri locale din Ungheni (MD); poate relata observații ale localnicilor despre drone/explozii în raion.  
  *Integrare:* Monitorizare manuală / alertă pe cuvinte cheie.  
  *Atenție:* Sursă media locală, nu oficială; verifică încrucișat. Verificare: Pagină locală de știri, neoficială; activitatea curentă neconfirmată.
- ~ **[Odesa Live – canal YouTube (camere publice)](<https://www.youtube.com/@OdesaLive>)** · cameră publică · liber · timp real · ★★☆☆☆  
  Proiect necomercial de streaming din Odesa; plus transmisiuni multi-oraș «UKRAINE LIVE NOW» (youtube.com/watch?v=Ci9WHEAfADg).  
  *Integrare:* Verificare manuală în timpul atacurilor asupra Odesei.  
  *Atenție:* Nu republica imagini care pot expune apărarea antiaeriană; fluxuri instabile. Verificare: Neverificat independent (buget de căutare epuizat; youtube.com inaccesibil). PRUDENȚĂ ETICĂ: autoritățile ucrainene (SBU) au restricționat/închis camerele publice din orașe pe timpul legii marțiale, deoarece ajută la țintire; canalul poate fi oprit sau poate opera contrar acestor restricții. Doar uz intern, niciodată redistribuit. Relevanță 1 (Odesa la ~400 km, noaptea fără valoare pentru Iași).
- ~ **[Poliția de Frontieră Română – Trafic On-line (timpi de așteptare)](<https://www.politiadefrontiera.ro/ro/traficonline>)** · hartă · liber · ore · ★★☆☆☆  
  Hartă oficială cu timpii medii de așteptare pe PTF rutiere (Sculeni, Albița, Rădăuți-Prut, Stânca); albastru = trafic suspendat temporar – proxy pentru închideri la incidente.  
  *Integrare:* Verificare periodică a statusului PTF de pe Prut; alertă internă la «suspendat».  
  *Atenție:* Actualizare la intervale (istoric ~2 h); fără API documentat. Verificare: Neverificat independent în această rundă (buget de căutare epuizat; politiadefrontiera.ro inaccesibil). Pagina „Trafic on-line” a Poliției de Frontieră e o funcție cunoscută și oficială (timpi de așteptare pe PTF, incl. Sculeni, Albița); comunicatul Agerpres 08/2026 raportat de agentul anterior susține că e activă. Proxy indirect pentru închideri de frontieră; relevanță 2.
- ~ **[Primaria Municipiului Huși – Oficial (Facebook)](<https://www.facebook.com/p/Primaria-Municipiului-Husi-Oficial-100067621895643/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagina oficială a Primăriei Huși (jud. Vaslui, aproape de Prut/Leușeni).  
  *Integrare:* Monitorizare manuală.  
  *Atenție:* ~2.300 urmăritori; doar confirmare locală. Verificare: Pagină plauzibilă; doar confirmare locală post-incident.
- ~ **[Primăria comunei Gropnița (Iași) – Facebook](<https://www.facebook.com/people/Prim%C4%83ria-comunei-Gropni%C8%9Ba/61557935918851/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagina primăriei Gropnița (comună pe Prut, NE de Iași); anunțuri locale. Site comuna-gropnita-iasi.ro.  
  *Integrare:* Monitorizare manuală.  
  *Atenție:* Postări rare; doar confirmare post-incident. Verificare: Pagină plauzibilă (format nou /people/...); relevanță mică, monitorizare manuală.
- ~ **[Primăria Comunei Țuțora (Iași) – Facebook](<https://www.facebook.com/www.comunatutora.ro/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagina primăriei Țuțora (comună pe Prut, la est de Iași); site comunatutora.ro.  
  *Integrare:* Monitorizare manuală.  
  *Atenție:* ~1.000 urmăritori; nu e sursă de alertă. Verificare: Pagină plauzibilă (handle neobișnuit «www.comunatutora.ro»); monitorizare manuală.
- ~ **[Primăria Fălciu (Vaslui) – Facebook](<https://www.facebook.com/primariafalciu/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagina primăriei Fălciu, comună pe Prut în sudul jud. Vaslui; există și pagina comunitară facebook.com/falciu.net.  
  *Integrare:* Monitorizare manuală.  
  *Atenție:* Postări administrative; nu e sursă de alertă. Verificare: Pagină plauzibilă; falciu.net e pagină comunitară, nu oficială.
- ~ **[Primăria Municipiului Iași – Facebook](<https://www.facebook.com/PrimariaMunicipiuluiIasi/>)** · rețea socială · liber · ore · ★★☆☆☆  
  Pagina oficială a Primăriei Iași; mesaje către populație (adăposturi, măsuri după alerte).  
  *Integrare:* Monitorizare manuală; nu există feed public.  
  *Atenție:* Nu emite alerte aeriene (le emite IGSU/RO-Alert). Verificare: Pagina oficială a Primăriei Iași, plauzibilă; nu emite alerte aeriene; monitorizare manuală.
- ~ **[Reddit – r/moldova](<https://www.reddit.com/r/moldova/>)** · rețea socială · liber · minute · ★★☆☆☆  
  Subreddit-ul principal al Moldovei (RO/EN/RU); utilizatorii postează rapid observații despre drone/explozii și știri.  
  *Integrare:* Doar manual: RSS Reddit se închide pe 13 nov 2026, iar API-ul public în mar 2027.  
  *Atenție:* Neverificat; Reddit blochează IP-uri de datacenter; nu baza alerte pe el. Verificare: NEVERIFICAT (buget WebSearch epuizat; reddit blocat) – subreddit existent; Reddit a eliminat RSS/API public, deci fără feed; doar API autorizat sau monitorizare manuală, nu scrape-ui.
- ~ **[Reddit – r/Romania](<https://www.reddit.com/r/Romania/>)** · rețea socială · liber · minute · ★★☆☆☆  
  Comunitatea românească (~1,1 mil. membri); fire rapide la RO-Alert/drone cu mărturii locale (Iași, Galați, Tulcea).  
  *Integrare:* Manual; RSS dispare 13 nov 2026.  
  *Atenție:* Mărturii neverificate; risc de panică/dezinformare. Verificare: NEVERIFICAT (buget WebSearch epuizat; reddit blocat) – subreddit existent; fără feed public; doar API autorizat/manual.
- ~ **[WarTranslated (Dmitri) – Bluesky](<https://bsky.app/profile/wartranslated.bsky.social>)** · rețea socială · liber · ore · ★★☆☆☆ · flux: <https://bsky.app/profile/wartranslated.bsky.social/rss>  
  Blogger estonian care traduce surse RU/UA; a semnalat convocarea ambasadorului rus de către România după drone doborâte.  
  *Integrare:* RSS: https://bsky.app/profile/wartranslated.bsky.social/rss.  
  *Atenție:* Comentariu/traducere, nu confirmare; versiunea 18+ e pe Telegram (evită). Verificare: NEVERIFICAT (buget WebSearch epuizat; bsky blocat) – evidența e un URL cu DID, handle-ul wartranslated.bsky.social nu e confirmat; mai sigur feed-ul pe DID (bsky.app/profile/did:plc:3ilzhrzkar3icae4mfyupmqp/rss).
- ~ **[WebcamRomania – camere live Iași (Piața Unirii, Palatul Culturii, Vama Sculeni)](<https://webcamromania.ro/webcam-live/judetul-iasi/>)** · cameră publică · liber · timp real · ★★☆☆☆  
  Agregator de camere publice: Piața Unirii și Palatul Culturii (Iași), Gara Pașcani, Vama Sculeni (uneori offline); confirmare vizuală/acustică urbană.  
  *Integrare:* Deschidere manuală în timpul alertelor; nu înregistra/republica fără drept.  
  *Atenție:* Camere oficiale/publice, frecvent offline; șanse mici de a surprinde drona. Verificare: Neverificat independent (buget de căutare epuizat; host inaccesibil). webcamromania.ro e agregator de camere publice; existența camerei Vama Sculeni și starea live neconfirmate. Camere publice – OK; utilitate redusă noaptea pentru drone (relevanță 1–2, eventual confirmare post-incident).
- ~ **[YouTube – „Live webcam Piața Unirii Iași”](<https://www.youtube.com/watch?v=s86lok3Arqs>)** · cameră publică · liber · timp real · ★★☆☆☆  
  Transmisiune YouTube spre Piața Unirii din Iași (există și h-IqAyY8JZM, llIl4EI5718).  
  *Integrare:* Embed/verificare manuală; YouTube Data API (cheie gratuită) pentru starea «live».  
  *Atenție:* Fluxurile își schimbă ID-ul; adesea offline. Verificare: Neverificat independent (buget de căutare epuizat; youtube.com inaccesibil). Un ID watch?v= pentru transmisiune live e efemer – se schimbă la repornirea streamului; identificatorul durabil ar fi canalul, pe care nu l-am putut confirma. Durabilitate scăzută, relevanță 1.
- ~ **[єППО (ePPO) – aplicație de raportare cetățenească a țintelor aeriene](<https://play.google.com/store/apps/details?id=ua.quick.brpg.pathfinder>)** · aplicație · cont gratuit · timp real · ★★☆☆☆  
  Aplicație ucraineană (UAMILS AB; recomandată de HUR) prin care cetățenii indică cu GPS+busolă drone/rachete observate, către apărarea antiaeriană.  
  *Integrare:* Nu oferă flux public; referință de design pentru un formular de observare. iOS: apps.apple.com/ua/app/єппо/id6443874876.  
  *Atenție:* Funcționează doar în UA, cu activare prin Diia; inutilizabilă în RO/MD; datele nu sunt publice. Verificare: NEVERIFICAT (buget WebSearch epuizat; Play Store blocat) – aplicație reală de raportare către armata UA, dar NU oferă date publice (necesită Diia, doar în UA); utilitate ca sursă: practic nulă. ID-ul pachetului de confirmat.
- ~ **[„Air Raid” – bot Discord de alerte aeriene (top.gg)](<https://top.gg/bot/958711560786812958>)** · aplicație · liber · timp real · ★★☆☆☆  
  Bot Discord care trimite alerte aeriene pe regiuni UA în canale text/voce și prin DM.  
  *Integrare:* Server Discord intern al echipei, canal cu regiunile Odesa/Vinnîțea/Cernăuți; redundanță la Telegram.  
  *Atenție:* Bot terț (rating 3,45); sursă de date neclară. Verificare: NEVERIFICAT (buget WebSearch epuizat; top.gg blocat) – bot Discord terț care preia aceleași alerte UA; redundant cu API-urile din catalog, activitate curentă neconfirmată.
- ~ **[Alerte.md – platformă civică de sesizări (Mediapoint)](<https://alerte.md>)** · web · liber · ore · ★☆☆☆☆  
  Platformă civică moldovenească în care cetățenii semnalează probleme locale primăriilor (Bălți, Cahul, Leova, Cantemir etc.); model posibil pentru raportări de resturi.  
  *Integrare:* Doar referință/parteneriat civic-tech; nu are categorie de drone.  
  *Atenție:* Nu e dedicată incidentelor aeriene; acoperire limitată la câteva orașe. Verificare: Neverificat independent (buget de căutare epuizat; alerte.md inaccesibil – ENOTFOUND). Titlul IPN indică o platformă civică de sesizări locale (Mediapoint), NU alerte aeriene; activitatea curentă neconfirmată. Atenție la confuzia de nume cu MD-ALERT (deja în catalog). Relevanță 1.
- ~ **[InfoDefenseROM – canal Telegram (rețea de propagandă InfoDefense)](<https://t.me/s/InfoDefenseRUM>)** · Telegram · liber · minute · ★☆☆☆☆  
  Canal în limba română al rețelei InfoDefense (voluntari care traduc propagandă rusă); util doar pentru a detecta narațiuni despre drone/alerte în RO.  
  *Integrare:* Doar pentru monitorizare de narațiuni; excluse din alerte.  
  *Atenție:* Context, credibilitate scăzută / propagandă (vezi ISD, DFRLab). Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – rețea de propagandă pro-Kremlin: doar context, credibilitate scăzută. Nepotrivire nume (ROM) vs handle (RUM) – de confirmat handle-ul.
- ~ **[Reddit – r/CredibleDefense (Daily MegaThread)](<https://www.reddit.com/r/CredibleDefense/>)** · rețea socială · liber · ore · ★☆☆☆☆  
  Megathread zilnic cu discuții moderate strict despre lovituri RU-UA și incursiuni în spațiul NATO; context și analiză.  
  *Integrare:* Manual; fără RSS după 13 nov 2026.  
  *Atenție:* Analiză, nu alertă; comentarii de amatori. Verificare: NEVERIFICAT (buget WebSearch epuizat; reddit blocat) – subreddit existent cu megathread zilnic; fără feed public; relevanță: context/analiză.
- ~ **[Sputnik Moldova 2.0 – canal Telegram (propagandă)](<https://t.me/s/sputnikmd_2>)** · Telegram · liber · minute · ★☆☆☆☆  
  Canal pro-Kremlin vizând publicul din Moldova; util doar pentru a detecta narațiuni false despre drone/alerte (ex. «aeroportul Chișinău evacuat»).  
  *Integrare:* Doar monitorizare de dezinformare; nu în fluxul de alerte.  
  *Atenție:* Context, credibilitate scăzută / propagandă; nu redistribui. Verificare: NEVERIFICAT (buget WebSearch epuizat; t.me blocat) – sursă de stat rusă: doar context, credibilitate scăzută / propagandă; sancționată/blocată în MD/UE, nu redistribui. Admisibilă cu această avertizare.

## Excluse la verificare

- **[Mîkolaiv OVA – Vitali Kim (@mykolaivskaODA)](<https://t.me/mykolaivskaODA>)** — inactivă: KMU l-a listat oficial în 2022, dar o verificare din 21.10.2026 a găsit doar 357 abonați, deci nu mai e canalul oficial al lui V. Kim. Succesorul nu a fost identificat; trebuie găsit manual.
- **[Ministerul Apărării RM – canale oficiale Telegram/RSS (din subsolul army.md)](<https://www.army.md/en>)** — dublură: Același site army.md ca intrarea existentă din catalog. Nu se numește niciun handle Telegram sau feed RSS, iar docs/12-catalog-surse.md notează deja „Canal Telegram oficial: negăsit”. Nu există feed distinct confirmat.
- **[HotNews.ro – articole MApN/drone](<https://hotnews.ro/>)** — dublură: Homepage-ul HotNews e deja acoperit de intrarea grupată din catalog. Dacă vreți o intrare distinctă, folosiți feed-ul RSS (live, 2.11.2026).
- **[MApN – conturi oficiale Facebook/X (link din mapn.ro)](<https://www.mapn.ro/>)** — dublură: URL-ul dat e doar site-ul MApN, mai puțin specific decât intrarea existentă english.mapn.ro/cpresa/356_; lipsesc URL-urile exacte Facebook/X. Re-adăugați doar cu link-uri confirmate către conturile oficiale.
- **[adsb.lol API – /v2/sqk/{squawk} și /v2/closest](<https://api.adsb.lol/v2/sqk/7700>)** — dublură: Același API ca #184 (rute /sqk/{squawk} și /closest/{lat}/{lon}/{radius} confirmate în cod); comasați în #184, cum s-a procedat la #188/#189. Doar uz intern.
- **[Monitorizare Vest – @monitoring_zaxid](<https://t.me/monitoring_zaxid>)** — negăsită (probabil inventată): Dovada citată e greșită: Puluj-g conține @zahidnimonitoring, nu @monitoring_zaxid. Singura mențiune e o diagramă dintr-un PRD (care scrie greșit și @monitorwarr). Alternativă posibilă, neverificată: t.me/zahidnimonitoring.
- **[ISW / Critical Threats – servicii ArcGIS REST](<https://services5.arcgis.com/SaBe5HMtmnbqSWlu/ArcGIS/rest/services>)** — licență restrictivă: „Unsafe” înseamnă aici licență, nu ilegalitate. Serviciile ArcGIS există (326, actualizate în sept. 2026), dar licența spune: „You may not use this geodata without the written consent of ISW”. Fără acord scris, nu se integrează. Folosiți harta publică ISW deja din catalog.
- **[DroneAudioDataset (Al-Emadi) – set audio pentru drone](<https://github.com/saraalemadi/DroneAudioDataset>)** — licență restrictivă: Licența interzice explicit folosirea în aplicații de securitate, supraveghere sau apărare și permite doar cercetare academică necomercială. Un sistem de avertizare pentru drone ar încălca termenii, deci trebuie exclus.
