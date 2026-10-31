# 12 · Anexă: catalogul complet al fluxurilor de date și hărților

*Generat pe 31.10.2026 din cercetarea pe 4 categorii + o verificare finală. Ordinea în fiecare categorie: relevanță (★) descrescătoare. „neconfirmat” = n-am putut verifica la sursă. Intrările marcate ✔ au fost reverificate sau corectate în pasul final. Rezumatul și recomandările sunt în [11-fluxuri-date-harti](11-fluxuri-date-harti.md).*

*141 intrări (17 corectate și 10 adăugate la verificare).*

## Ucraina și R. Moldova

### alerts.in.ua – hartă + API alerte ★★★★★ ✔
- **Link:** https://alerts.in.ua
- **Ce oferă:** Hartă și API cu starea alertelor aeriene (și a altor tipuri de alertă) pe oblast, raion și hromadă, plus istoric pe locație.
- **Acces:** REST JSON, bază https://api.alerts.in.ua cu prefixul /v1 (din clientul Rust ralertsinua-http, nu din documentația oficială). Biblioteca oficială Python: alerts-ua/alerts-in-ua-py. Documentația de pe devs.alerts.in.ua nu a putut fi citită (domeniu blocat în sesiune). UID-urile locațiilor se iau din API sau din bibliotecă.
- **Cost / autentificare:** Token la cerere, prin formularul de pe alerts.in.ua. Potrivit unui proiect terț, cererile de o linie sau scrise cu LLM sunt respinse, deci descrieți uzul și frecvența în cuvintele voastre. Cost: neconfirmat.
- **Licență / termeni:** neconfirmat (termenii de pe devs.alerts.in.ua nu au fost citiți)
- **Actualizare:** Aproape timp real. Limita de rată oficială e neconfirmată (clientul PHP impune implicit 5 s între cereri identice, dar e o regulă a bibliotecii). · **Acoperire:** Toată Ucraina. Relevante: oblasturile Odesa, Vinnîțea, Cernăuți și raioanele de la granița cu MD/RO.
- **Precauții:** Alertele privesc teritoriul Ucrainei; pentru Iași sunt doar pre-avertizare nespecifică, din care nu se deduc traiectorii. Permiteți devs.alerts.in.ua în setările de rețea ca să verificați termenii. Nu expuneți token-ul în frontend.
- **Sursă:** https://github.com/alerts-ua/alerts-in-ua-py · încredere medie

### Ukraine Alarm API (Ajax „Повітряна тривога”) ★★★★★ ✔
- **Link:** https://api.ukrainealarm.com
- **Ce oferă:** Alarme active pe oblast, raion și hromadă; lista regiunilor cu ID-urile lor; endpoint de status care arată când s-au schimbat datele.
- **Acces:** REST JSON: GET /api/v3/alerts, /api/v3/alerts/{regionId}, /api/v3/alerts/status, /api/v3/regions, conform clienților oficiali UkraineAlarm de pe GitHub (Python, JavaScript). Cheia se trimite în header-ul Authorization, fără prefixul Bearer (conform unui client terț).
- **Cost / autentificare:** Cheie API la cerere, prin formularul de pe api.ukrainealarm.com. Cost: neconfirmat.
- **Licență / termeni:** neconfirmat
- **Actualizare:** Timp real. Un proiect terț raportează o limită de ~1 cerere/min pe cheie (neconfirmat oficial): interogați /alerts/status și cereți /alerts doar la schimbări. · **Acoperire:** Ucraina
- **Precauții:** Oglinda fără cheie siren.pp.ua e neoficială, bună doar ca rezervă. Aceleași rezerve ca la alerts.in.ua: e pre-avertizare, nu traiectorie.
- **Sursă:** https://github.com/UkraineAlarm/UkraineAlarm-python · încredere medie

### Forțele Aeriene ale UA – @kpszsu ★★★★★
- **Link:** https://t.me/s/kpszsu
- **Ce oferă:** Avertizări de direcție pentru UAV/rachete pe oblasturi și raportul zilnic de dimineață (lansate/doborâte)
- **Acces:** Telegram; preview web t.me/s/kpszsu; ingestie Telethon/MTProto; fără RSS oficial
- **Cost / autentificare:** Gratuit (cont Telegram + api_id pentru MTProto)
- **Licență / termeni:** neconfirmat
- **Actualizare:** Minute (avertizări); zilnic (raport) · **Acoperire:** Toată Ucraina, inclusiv direcții spre Odesa/Izmail/Vinnîțea
- **Precauții:** OPSEC: nu republicați în timp real direcții/poziții sau activitatea apărării antiaeriene; doar semnal intern. Din 10.08.2026 nu mai raportează numărul de rachete lansate/interceptate (Kaggle); numărul Shahed/Geran nu mai e publicat consecvent din ~5.05.2026
- **Sursă:** https://netfreedom.org.ua/karta-tryvog-telegram-povnyj-gid-po-kanalah-mapah-ta-spovishhennyah/ ; https://www.kaggle.com/datasets/piterfm/massive-missile-attacks-on-ukraine · încredere ridicată

### Odesa OVA – Oleh Kiper (t.me/odeskaODA) ★★★★★
- **Link:** https://t.me/odeskaODA
- **Ce oferă:** Anunțuri oficiale ale administrației militare regionale Odesa: atacuri cu drone, consecințe, restricții; acoperă raioanele Izmail, Bilhorod-Dnistrovskyi, Podilsk (Dunăre și granița cu MD/Transnistria)
- **Acces:** Telegram; preview https://t.me/s/odeskaoda (același canal); site oda.od.gov.ua
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Minute–ore (consecințele vin după atac) · **Acoperire:** Oblastul Odesa
- **Precauții:** Canal personalizat – se poate schimba la schimbarea șefului (Texty); nu confundați cu t.me/odesaMVA (oraș); nu republicați locuri de impact în timp real
- **Sursă:** https://t.me/s/odeskaoda ; https://bukinfo.com.ua/oblasna-vlada/oficiyni-telegram-kanaly-viyskovyh-administraciy-spysok ; https://oda.od.gov.ua/ua/management · încredere ridicată

### Kaggle – Massive Missile Attacks on Ukraine (piterfm / Petro Ivaniuk) ★★★★★
- **Link:** https://www.kaggle.com/datasets/piterfm/massive-missile-attacks-on-ukraine
- **Ce oferă:** missile_attacks_daily.csv (~918 kB: lansate/doborâte pe tip de armă și zi) + missiles_and_uavs.csv (tipuri de arme); compilat manual din rapoartele Forțelor Aeriene și ale Statului Major
- **Acces:** Descărcare CSV de pe Kaggle sau Kaggle API/CLI
- **Cost / autentificare:** Cont Kaggle gratuit
- **Licență / termeni:** neconfirmat (verificați pagina setului)
- **Actualizare:** Actualizare manuală periodică (frecvență neconfirmată) · **Acoperire:** Din 2022 până în 2026; după 10.08.2026 fără cifre de lansare/interceptare
- **Precauții:** Lipsuri în 2026 (raportare oficială redusă); CSIS a validat doar perioada 2022–2024
- **Sursă:** https://www.kaggle.com/datasets/piterfm/massive-missile-attacks-on-ukraine · încredere ridicată

### Ministerul Apărării al R. Moldova – comunicate (army.md) ★★★★★ ✔
- **Link:** https://www.army.md
- **Ce oferă:** Comunicate oficiale despre dronele intrate în spațiul aerian al R. Moldova, restricțiile de zbor (nord, centru) și ridicarea lor, fragmentele găsite. Statistici cumulate: presa citează MA cu 65 de incidente în 2026, dintre care 17 în octombrie (cifră din 31.10.2026; sursa primară neconfirmată).
- **Acces:** Web army.md (RSS: neconfirmat). Pagina de Facebook a MA e menționată într-o publicație army.md din 2020 (URL neconfirmat). Canal Telegram oficial: negăsit în căutări, verificați footerul army.md sau gov.md. Comunicatele sunt preluate rapid de Moldpres, ProTV și Mediafax.
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Minute până la zeci de minute. Pe 31.10.2026: intrare la 16:24, restricție în nord la 16:46 și în centru la 16:52, redeschidere la 17:14; a doua dronă a intrat la 17:50. · **Acoperire:** R. Moldova
- **Precauții:** Nu urmăriți conturi Telegram care se prezintă drept ale MA fără confirmare pe army.md. MA a dezmințit public falsuri răspândite pe Telegram.
- **Sursă:** https://www.mediafax.ro/externe/update-spatiul-aerian-restrictionat-in-nordul-si-centrul-republicii-moldova-doua-drone-au-patruns-neautorizat-23835183 · încredere medie

### Europa Liberă Moldova – hartă interactivă a dronelor ★★★★★
- **Link:** https://www.europalibera.md/a/harta-interactiva-ploaia-de-drone-cum-s-a-mutat-pericolul-de-la-granita-spre-centrul-r-moldova/33871506.html
- **Ce oferă:** Hartă interactivă actualizată permanent a survolurilor și căderilor de drone în R. Moldova (≈90 cazuri, 48 căderi până la 6.10.2026, conform MApărării)
- **Acces:** Web (hartă embed); export neconfirmat
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat (© RFE/RL – reutilizare cu permisiune)
- **Actualizare:** Actualizată permanent (frecvență neconfirmată) · **Acoperire:** Republica Moldova, 2022–2026
- **Precauții:** Nu redistribuiți fără acord; cifrele diferă de alte hărți din cauza datelor-limită
- **Sursă:** https://www.europalibera.md/a/harta-interactiva-ploaia-de-drone-cum-s-a-mutat-pericolul-de-la-granita-spre-centrul-r-moldova/33871506.html · încredere ridicată

### Canal Telegram al aplicației „Повітряна тривога” (Ajax) ★★★★☆ ✔
- **Link:** https://t.me/air_alert_ua
- **Ce oferă:** Duplicat al tuturor notificărilor aplicației „Повітряна тривога” (începutul și sfârșitul alertelor pe regiuni). Canal lansat pe 15.03.2022.
- **Acces:** Telegram public t.me/air_alert_ua; preview web t.me/s/air_alert_ua (de verificat). Ingestie prin RSSHub sau Telethon.
- **Cost / autentificare:** Gratuit, fără cheie
- **Licență / termeni:** neconfirmat
- **Actualizare:** Timp real · **Acoperire:** Ucraina (toate regiunile)
- **Precauții:** Ajax a creat canalul tocmai pentru că, din motive de securitate, nu putea distribui larg accesul API. Folosiți-l ca rezervă internă, nu îl redifuzați integral. Parsarea textului se strică dacă se schimbă formatul mesajelor.
- **Sursă:** https://ajax.systems/ua/blog/air-alert-telegram-channel · încredere ridicată

### Cernăuți OVA – Ruslan Osypenko (t.me/chernivetskaODA) ★★★★☆
- **Link:** https://t.me/chernivetskaODA
- **Ce oferă:** Canalul șefului OVA Cernăuți: alerte și atacuri în regiune (ruta nordică spre nordul Moldovei → Botoșani/Suceava)
- **Acces:** Telegram; preview t.me/s/chernivetskaODA
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Minute–ore · **Acoperire:** Oblastul Cernăuți
- **Precauții:** Canal personal al șefului (conform bukoda.gov.ua), nu contul instituțional – se poate schimba odată cu persoana (Texty)
- **Sursă:** https://bukoda.gov.ua/gromadyanam/pereselencyam · încredere medie

### Vinnîțea OVA (vin.gov.ua) ★★★★☆
- **Link:** https://www.vin.gov.ua
- **Ce oferă:** Site oficial cu link „Канал в Telegram” în footer; include raionul Mohyliv-Podilskyi (vizavi de Otaci/Ocnița)
- **Acces:** Web; handle Telegram neconfirmat – de luat din footerul site-ului
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** neconfirmat · **Acoperire:** Oblastul Vinnîțea
- **Precauții:** Handle-ul nu a fost confirmat; verificați bifa de verificare și linkul de pe site; t.me/VInnEmd este pentru urgențe medicale prin text, nu alerte
- **Sursă:** https://osite.vin.gov.ua/news/oholoshennia/65369-telefony-hariachykh-linii-u-vypadku-nadzvychainykh-sytuatsii-na-terytorii-vinnychchyny-2 · încredere scăzută

### Lista oficială a canalelor Telegram ale administrațiilor militare (Oficiul Președintelui, via bukinfo) ★★★★☆
- **Link:** https://bukinfo.com.ua/oblasna-vlada/oficiyni-telegram-kanaly-viyskovyh-administraciy-spysok
- **Ce oferă:** Director al canalelor Telegram oficiale ale OVA – sursa pentru Mykolaiv OVA și pentru verificarea celorlalte
- **Acces:** Web (articol)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Static (lista poate fi depășită) · **Acoperire:** Toate oblasturile UA
- **Precauții:** Handle-urile Mykolaiv OVA și RVA Izmail/Podilsk/Mohyliv-Podilskyi rămân neconfirmate; canalele se schimbă la schimbarea șefilor (Texty, zn.ua/„Голка”)
- **Sursă:** https://bukinfo.com.ua/oblasna-vlada/oficiyni-telegram-kanaly-viyskovyh-administraciy-spysok ; https://texty.org.ua/articles/110908/oficijno-personalni-v-chomu-problema-z-oficijnymy-telehram-kanalamy-oda-ova/ · încredere medie

### ISIS – analize lunare ale atacurilor Shahed ★★★★☆
- **Link:** https://isis-online.org/isis-reports/monthly-analysis-of-russian-shahed-136-deployment-against-ukraine-updated
- **Ce oferă:** Rapoarte lunare PDF (2024–2026): lansări Shahed/Geran pe lună și pe zi, decoy-uri (Gerbera, Parody), rata de lovire, comparații cu reconstrucții independente (Oko Gora)
- **Acces:** Web/PDF (fără CSV)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat (© ISIS)
- **Actualizare:** Lunar · **Acoperire:** Ucraina, 2024–2026
- **Precauții:** Datele din iulie 2026 trebuie citite „pe două straturi”, iar totalurile diferă după metodă; extragerea din PDF se face manual
- **Sursă:** https://isis-online.org/uploads/isis-reports/documents/July_2026_Updated_Analysis_of_Russian_Shahed-type_UAVs_Deployment_Against_Ukraine.pdf · încredere ridicată

### UA AirDefense Tracker ★★★★☆
- **Link:** https://ua-air-defense-tracker.org/
- **Ce oferă:** Agregare lunară a rapoartelor zilnice ale Forțelor Aeriene din oct. 2022: UAV, rachete de croazieră și balistice, lansate și interceptate confirmat
- **Acces:** Web (export neconfirmat)
- **Cost / autentificare:** Gratuit (neconfirmat)
- **Licență / termeni:** neconfirmat
- **Actualizare:** neconfirmat (probabil lunar) · **Acoperire:** Ucraina, din oct. 2022
- **Precauții:** Moștenește golurile raportării oficiale din 2026
- **Sursă:** https://ua-air-defense-tracker.org/ · încredere medie

### Moldpres – agenția de stat (RSS) ★★★★☆ ✔
- **Link:** https://www.moldpres.md
- **Ce oferă:** Știri oficiale, inclusiv comunicatele MA și ale Guvernului despre drone și restricțiile de spațiu aerian
- **Acces:** Web; secțiunea în română moldpres.md/rom/ e confirmată. RSS observat la w.moldpres.md/config/rss.php?lang=eng (stabilitate neconfirmată); parametrul pentru română: neconfirmat.
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat (afișați doar titlu + link)
- **Actualizare:** Minute · **Acoperire:** R. Moldova
- **Precauții:** Testați RSS-ul (și o eventuală variantă lang=rom) înainte de producție. Preluați doar titlul și linkul.
- **Sursă:** https://www.moldpres.md/rom/societate/o-drona-a-patruns-neautorizat-in-spatiul-aerian-al-republicii-moldova · încredere medie

### MoldATSA AIM – AIP SUP / NOTAM ★★★★☆
- **Link:** https://aim.moldatsa.md
- **Ce oferă:** Informație aeronautică: AIP SUP-uri cu zone restricționate lângă granița cu Ucraina (ex. SUP 2022/012, SUP 001/2023), cerințe de depunere FPL cu 60/180 min în avans; NOTAM
- **Acces:** Web AIM (aim@moldatsa.md); portal NOTAM public/briefing online neconfirmat; SUP-uri arhivate pe safeairspace.net
- **Cost / autentificare:** neconfirmat
- **Licență / termeni:** neconfirmat
- **Actualizare:** Ciclu AIP/NOTAM (neconfirmat) · **Acoperire:** Spațiul aerian al R. Moldova
- **Precauții:** Informațiile de contact sunt din 2022; închiderile ad-hoc pentru drone apar mai rapid în comunicatele MApărării
- **Sursă:** https://safeairspace.net/tomes/wp-content/uploads/2022/08/LU_Sup_2022_012_en.pdf ; https://safeairspace.net/tomes/wp-content/uploads/2023/01/MOLDOVA-SUP-01-23.pdf · încredere medie

### Presa moldovenească (Newsmaker, Unimedia, ZdG, IPN, TV8, NordNews, Realitatea, Radio Moldova) + news.yam.md ★★★★☆
- **Link:** https://newsmaker.md
- **Ce oferă:** Relatări rapide despre survoluri, căderi, închideri ale spațiului aerian; NordNews acoperă nordul (Soroca/Edineț/Briceni); news.yam.md agregă știrile
- **Acces:** Web; RSS neconfirmat pentru toate (doar Moldpres are RSS observat); monitorizare prin agregator sau scraping respectuos
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat (drepturi de autor ale redacțiilor – folosiți doar titlu + link)
- **Actualizare:** Minute–ore · **Acoperire:** Republica Moldova
- **Precauții:** Pot exista erori/dubluri; deduplicare pe eveniment; date personale (fotografii de case, nume) – minimizare GDPR
- **Sursă:** https://newsmaker.md/ro/o-drona-a-intrat-neautorizat-in-spatiul-aerian-al-republicii-moldova-zborurile-in-nordul-si-centrul-tarii-restrictionate-temporar ; https://nordnews.md/uncategorized/md-alert-sistem-avertizare-populatie-moldova/ ; https://unimedia.info/ro/news/b23a87574dff28eb/video-moldovenii-vor-putea-primi-alerte-despre-pericole-prin-sistemul-md-alert-abia-din-2027-sefa-mai-urmeaza-sa-lansam-licitatia.html · încredere medie

### sergeiown/Alert_Server (referință arhitectură) ★★★☆☆
- **Link:** https://github.com/sergeiown/Alert_Server
- **Ce oferă:** Backend Node.js self-hosted care unifică alerts.in.ua, UkraineAlarm și Neptun, cu push pe WebSocket, SQLite, hartă de amenințări, prognoză statistică
- **Acces:** Cod sursă GitHub
- **Cost / autentificare:** Gratuit (necesită propriile token-uri API)
- **Licență / termeni:** MIT (conform descrierii repo)
- **Actualizare:** Depinde de sursele upstream · **Acoperire:** Ucraina
- **Precauții:** Integrarea Neptun poate încălca termenii acestuia (neconfirmați); verificați ToS ale fiecărei surse
- **Sursă:** https://github.com/sergeiown/Alert_Server · încredere ridicată

### Odesa – administrația militară a orașului (t.me/odesaMVA) ★★★☆☆
- **Link:** https://t.me/odesaMVA
- **Ce oferă:** Canalul șefului administrației militare a orașului Odesa (Serhii Lysak): atacuri asupra orașului, consecințe
- **Acces:** Telegram; preview t.me/s/odesaMVA
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Minute–ore · **Acoperire:** Orașul Odesa
- **Precauții:** Canal personalizat; acoperire doar urbană
- **Sursă:** https://t.me/odesaMVA · încredere ridicată

### NEPTUN – hartă Shahed/rachete ★★★☆☆
- **Link:** https://neptun.in.ua
- **Ce oferă:** Hartă cu alerte și traiectorii estimate pentru Shahed, rachete, KAB; AI clasifică mesajele din canalele Telegram ale OVA și ZSU și estimează direcția
- **Acces:** Web + aplicație Android (com.neptunalarm.neptun_alarm_app); API public neconfirmat
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** ~5 s de la mesajul Telegram la hartă (declarat) · **Acoperire:** Ucraina
- **Precauții:** Estimări din mesaje, NU radar; site-uri clonă cu nume similar (aktualnoua, provse) fac afirmații neverificate; nu scrapuiți/republicați; OPSEC
- **Sursă:** https://neptun.in.ua/about ; https://neptun.in.ua/blog/yak-pratsyuye-karta-shahediv · încredere medie

### monitor – hartă a amenințărilor aeriene (beta) ★★★☆☆
- **Link:** https://dev.ua/news/mapa-shakhediv-vid-monitor-1791880610
- **Ce oferă:** Hartă beta a alertelor și a mișcării aproximative a dronelor și rachetelor
- **Acces:** Web (URL-ul hărții neconfirmat – vezi articolul dev.ua)
- **Cost / autentificare:** Gratuit (neconfirmat)
- **Licență / termeni:** neconfirmat
- **Actualizare:** La fiecare 20 s; versiune de bază ~200 KB · **Acoperire:** Ucraina
- **Precauții:** Poziții aproximative; nu republicați; OPSEC
- **Sursă:** https://dev.ua/news/mapa-shakhediv-vid-monitor-1791880610 · încredere medie

### mapa.ua ★★★☆☆
- **Link:** https://mapa.ua/
- **Ce oferă:** Hartă a alertelor și a mișcării UAV (Shahed etc.), rachete de croazieră/balistice, KAB; notificări push
- **Acces:** Web/aplicație; API neconfirmat
- **Cost / autentificare:** neconfirmat
- **Licență / termeni:** neconfirmat
- **Actualizare:** neconfirmat · **Acoperire:** Ucraina
- **Precauții:** Neoficial; acuratețe neverificată; nu republicați
- **Sursă:** https://mapa.ua/ · încredere scăzută

### CSIS Futures Lab – Russian Firepower Strike Tracker ★★★☆☆
- **Link:** https://www.csis.org/programs/futures-lab/projects/russian-firepower-strike-tracker-analyzing-missile-attacks-ukraine
- **Ce oferă:** Tracker/analiză a loviturilor cu rachete și drone; a validat setul Kaggle față de cifrele oficiale
- **Acces:** Web (format de date neconfirmat)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Static (acoperire încheiată) · **Acoperire:** 27.09.2022–30.11.2024
- **Precauții:** Nu acoperă 2025–2026
- **Sursă:** https://www.csis.org/programs/futures-lab/projects/russian-firepower-strike-tracker-analyzing-missile-attacks-ukraine · încredere medie

### Unmanned Systems Tracker – Air Defence log ★★★☆☆
- **Link:** https://unmannedsystemstracker.com/air-defence/
- **Ce oferă:** Jurnal al apărării antiaeriene / atacurilor aeriene, reîmprospătat zilnic
- **Acces:** Web; export automat prin GitHub Actions (repo neconfirmat)
- **Cost / autentificare:** neconfirmat
- **Licență / termeni:** neconfirmat
- **Actualizare:** Zilnic · **Acoperire:** Ucraina
- **Precauții:** Metodologie neverificată
- **Sursă:** https://unmannedsystemstracker.com/air-defence/ · încredere scăzută

### Airwars – hartă/investigație Shahed ★★★☆☆
- **Link:** https://airwars.org/shahed-map/
- **Ce oferă:** Hartă și vizualizare investigativă a atacurilor Shahed (Rusia–Ucraina–Iran)
- **Acces:** Web
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** neconfirmat · **Acoperire:** neconfirmat
- **Precauții:** Conținut investigativ; perioada acoperită neconfirmată
- **Sursă:** https://airwars.org/shahed-map/ ; https://airwars.org/investigation/shahed-year-russia-ukraine-iran · încredere scăzută

### MAI Moldova – Sinteza evenimentelor (PDF zilnic) ★★★☆☆
- **Link:** https://mai.gov.md
- **Ce oferă:** Rezumat zilnic al evenimentelor raportate de structurile MAI
- **Acces:** PDF pe mai.gov.md/sites/default/files/inline-files/…
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Zilnic · **Acoperire:** Republica Moldova
- **Precauții:** Nu s-a confirmat dacă include incidentele cu drone; necesită parsare PDF; conține date personale – GDPR/minimizare
- **Sursă:** https://mai.gov.md/sites/default/files/inline-files/Sinteza%2021%20-%2022.12.2024.pdf · încredere medie

### Aeroportul Chișinău – stare zboruri (proxy pentru închideri) ★★★☆☆
- **Link:** https://www.ro.kayak.com/Chisinau-Chisinau-Intl-Aeroport.RMO.ap.html
- **Ce oferă:** Sosiri/plecări; întârzierile, întoarcerile și deviațiile semnalează indirect închideri ale spațiului aerian
- **Acces:** Tabela oficială neconfirmată; terți (Kayak) sau ADS-B (adsb.lol/OpenSky)
- **Cost / autentificare:** Gratuit (terți)
- **Licență / termeni:** neconfirmat (ToS terți – fără scraping)
- **Actualizare:** Minute · **Acoperire:** Aeroportul Chișinău (IATA RMO conform Kayak; istoric KIV – de verificat)
- **Precauții:** Semnal indirect; nu urmăriți aeronave militare
- **Sursă:** https://www.ro.kayak.com/Chisinau-Chisinau-Intl-Aeroport.RMO.ap.html · încredere scăzută

### TV8 – infografic: toate dronele și rachetele găsite în Moldova ★★★☆☆
- **Link:** https://tv8.md/2026/10/17/infografic-harta-tuturor-dronelor-si-rachetelor-gasite-in-moldova-dupa-atacurile-rusiei-in-ucraina/299258
- **Ce oferă:** Hartă statică cu locurile unde s-au găsit fragmente de drone și rachete, inclusiv în stânga Nistrului (ex. Giurgiulești 20.08.2026, Văleni/Cahul 5.08.2026)
- **Acces:** Web (imagine/infografic)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Static (17.10.2026) · **Acoperire:** Republica Moldova, incl. Transnistria
- **Precauții:** Instantaneu; geocodare manuală
- **Sursă:** https://tv8.md/2026/10/17/infografic-harta-tuturor-dronelor-si-rachetelor-gasite-in-moldova-dupa-atacurile-rusiei-in-ucraina/299258 · încredere ridicată

### Realitatea.md – harta incidentelor aeriene ★★★☆☆
- **Link:** https://realitatea.md/harta-incidentelor-aeriene-ce-zone-ale-moldovei-au-fost-survolate-de-drone-si-rachete/
- **Ce oferă:** Hartă a zonelor survolate de drone și rachete; 81 de încălcări în 2022–2026, dintre care 44 în 2026 (până la 24.09), conform MApărării
- **Acces:** Web
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Static (24.09.2026) · **Acoperire:** Republica Moldova
- **Precauții:** Instantaneu; metodologie de presă
- **Sursă:** https://realitatea.md/harta-incidentelor-aeriene-ce-zone-ale-moldovei-au-fost-survolate-de-drone-si-rachete/ · încredere ridicată

### Moldova1 – analiză și hartă pe raioane ★★★☆☆
- **Link:** https://moldova1.md/p/81940/neutralitate-fragila-r-moldova--gazda-a-60-de-drone-rusesti-si-iraniene-in-cei-patru-ani-si-jumatate-de-razboi-harta-celor-mai-afectate-raioane
- **Ce oferă:** 60 de incidente în 2022–2026 (până la 28.07.2026), cel puțin 12 cu încărcătură explozivă; hartă a celor mai afectate raioane
- **Acces:** Web
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Static (07.2026) · **Acoperire:** Republica Moldova
- **Precauții:** Cifre diferite de MApărării din cauza datei-limită
- **Sursă:** https://moldova1.md/p/81940/neutralitate-fragila-r-moldova--gazda-a-60-de-drone-rusesti-si-iraniene-in-cei-patru-ani-si-jumatate-de-razboi-harta-celor-mai-afectate-raioane · încredere ridicată

### єТривога (eTryvoga) ★★☆☆☆
- **Link:** https://apps.apple.com/ua/app/%D1%94%D1%82%D1%80%D0%B8%D0%B2%D0%BE%D0%B3%D0%B0/id1611921749
- **Ce oferă:** Aplicație civilă de notificare a alertelor aeriene; App Store indică Telegram @UkraineAlarmSignal
- **Acces:** Aplicație mobilă; Telegram @UkraineAlarmSignal (neverificat din sursa primară); fără API cunoscut
- **Cost / autentificare:** Gratuit (Patreon pentru susținere)
- **Licență / termeni:** neconfirmat
- **Actualizare:** Real-time (neconfirmat) · **Acoperire:** Ucraina
- **Precauții:** Au fost raportate erori de alertă (ex. alertă falsă de artilerie la Odesa – Espreso); nu e sursă oficială
- **Sursă:** https://apps.apple.com/ua/app/%D1%94%D1%82%D1%80%D0%B8%D0%B2%D0%BE%D0%B3%D0%B0/id1611921749 ; https://espreso.tv/u-roboti-zastosunku-etrivoga-stavsya-zbiy-poperedzhali-pro-zagrozu-artbostrilu-odesi · încredere scăzută

### alerts.net.ua – statusuri explozii (JSON neoficial) ★★☆☆☆
- **Link:** http://alerts.net.ua/explosives_statuses_v2.json
- **Ce oferă:** JSON cu statusuri de explozii pe regiuni (folosit de un bot Telegram open-source)
- **Acces:** HTTP JSON (endpoint menționat în repo GitHub)
- **Cost / autentificare:** neconfirmat
- **Licență / termeni:** neconfirmat
- **Actualizare:** neconfirmat · **Acoperire:** Ucraina (neconfirmat)
- **Precauții:** Proveniență neoficială/necunoscută; HTTP necriptat; nu republicați locuri de explozii în timp real
- **Sursă:** https://github.com/yurnov/ua-explosion-notification-bot · încredere scăzută

### Alte hărți Shahed (neboskhyl, shahmap, Zalizne Nebo, DIMAP, SkyAlert, Argegis) ★★☆☆☆
- **Link:** https://neboskhyl.com/
- **Ce oferă:** Hărți live cu ținte și cursuri prognozate (neboskhyl: rută cu altitudine și prognoză pe câteva minute; shahmap.online: alerte pe oblast/raion; zaliznenebo.world, dimap.live, skyalert.pp.ua; alarmmap.online/argegis doar Kiev/Dnipropetrovsk)
- **Acces:** Web; fără API documentat
- **Cost / autentificare:** Gratuit (shahmap: fără înregistrare)
- **Licență / termeni:** neconfirmat
- **Actualizare:** Unul dintre servicii declară erori de ±2 min (rachete) / până la 5 min (drone) · **Acoperire:** Ucraina (parțial)
- **Precauții:** Datele provin din canale Telegram de monitorizare, nu din radar; calitate variabilă; doar consultare internă; OPSEC
- **Sursă:** https://neboskhyl.com/ ; https://shahmap.online/en ; https://skyalert.pp.ua/karta-onlayn-monitorynhu-shakhediv-v-ukrayini · încredere scăzută

### time-machine-data (VIINA × Massive Missile Attacks) ★★☆☆☆
- **Link:** https://github.com/mdniprovskyi/time-machine-data
- **Ce oferă:** Pipeline care pune în corespondență VIINA (incidente din știri) cu setul Kaggle MMAU, normalizat pe dată/locație/tip de armă
- **Acces:** GitHub
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** „Free, non-commercial” (conform descrierii repo; licența exactă neconfirmată)
- **Actualizare:** neconfirmat (repo creat în aug. 2026) · **Acoperire:** Ucraina
- **Precauții:** Proiect mic, fără istoric de mentenanță
- **Sursă:** https://github.com/mdniprovskyi/time-machine-data · încredere medie

### MotherDuck „Skyfall” – vizualizare atacuri aeriene ★★☆☆☆
- **Link:** https://motherduck.com/dive-gallery/dives/skyfall-1350-nights-of-drones-missiles-over-ukraine
- **Ce oferă:** Vizualizare a rapoartelor zilnice ale Forțelor Aeriene (drone și rachete)
- **Acces:** Web
- **Cost / autentificare:** Gratuit (neconfirmat)
- **Licență / termeni:** neconfirmat
- **Actualizare:** Static · **Acoperire:** 09.2022–06.2026
- **Precauții:** Vizualizare, nu sursă primară
- **Sursă:** https://motherduck.com/dive-gallery/dives/skyfall-1350-nights-of-drones-missiles-over-ukraine · încredere scăzută

### Energy Map (DiXi Group) ★★☆☆☆
- **Link:** https://map.ua-energy.org
- **Ce oferă:** 440–450+ seturi de date energetice machine-readable, inclusiv un set despre atacurile masive cu rachete și drone asupra infrastructurii critice (lansate/doborâte pe zi)
- **Acces:** Web + API (pagină „API description”)
- **Cost / autentificare:** Gratuit (neconfirmat)
- **Licență / termeni:** Reutilizare permisă cu respectarea drepturilor DiXi Group și link spre Energy Map
- **Actualizare:** Variabil pe set · **Acoperire:** Ucraina
- **Precauții:** Datele Ukrenergo despre întreruperi nu au fost găsite ca open data
- **Sursă:** https://map.ua-energy.org/en/information/about ; https://map.ua-energy.org/en/datasets/9091d6f9-564f-434a-a9d2-bba9657ca2c1 · încredere medie

### MD-ALERT (în implementare) / modul EVO ★★☆☆☆
- **Link:** https://radiomoldova.md/p/72133/pas-inainte-pentru-md-alert-guvernul-a-aprobat-conceptul-iar-igsu-poate-porni-implementarea
- **Ce oferă:** Viitor sistem de avertizare publică prin cell broadcast, radio/TV, sirene și EVO/MNotify; poate include obiecte neautorizate în spațiul aerian
- **Acces:** Indisponibil azi; modul interimar în aplicația EVO în pregătire
- **Cost / autentificare:** n/a (~5 mil. EUR, finanțare BIRD/Banca Mondială)
- **Licență / termeni:** n/a
- **Actualizare:** n/a – operațional țintă la finalul lui 2027 · **Acoperire:** Republica Moldova
- **Precauții:** Nu există feed public; nu-l prezentați ca operațional
- **Sursă:** https://radiomoldova.md/p/72133/pas-inainte-pentru-md-alert-guvernul-a-aprobat-conceptul-iar-igsu-poate-porni-implementarea ; https://ziuaveche.ro/international/basarabia/republica-moldova-pregateste-alerte-de-urgenta-in-aplicatia-evo-sistemul-md-alert-ramane-programat-pentru-2027-352248.html/ · încredere ridicată

### AAC Moldova – hartă zone UAS + punctualitate aeroport ★★☆☆☆
- **Link:** https://www.caa.md
- **Ce oferă:** Hartă digitală a zonelor geografice și restricțiilor pentru drone (campania „Fly legally, fly safely!”, oct. 2025); rapoarte lunare de punctualitate pentru aeroportul Chișinău; cadru normativ (HG 949/2022)
- **Acces:** Web
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Lunar (rapoarte); hartă – neconfirmat · **Acoperire:** Republica Moldova
- **Precauții:** Strat de context (zone restricționate), nu detecție
- **Sursă:** https://www.caa.md/en/press-releases/launch-information-campaign-users-unmanned-aircraft-fly-legally-fly-safely ; https://caa.md/en/press-releases/flight-punctuality-chisinau-international-airport-may-2025 · încredere medie

### Safe Airspace – arhivă de riscuri și AIP SUP ★★☆☆☆
- **Link:** https://safeairspace.net
- **Ce oferă:** Arhivă de notificări și AIP SUP-uri (inclusiv Moldova) privind riscurile din zonele de conflict
- **Acces:** Web/PDF
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** neconfirmat · **Acoperire:** Global, inclusiv Moldova/Ucraina
- **Precauții:** Context, nu timp real
- **Sursă:** https://safeairspace.net/tomes/wp-content/uploads/2023/01/MOLDOVA-SUP-01-23.pdf · încredere medie

## România, spațiu aerian, ADS-B, AIS

### RO-Alert (cell-broadcast) ★★★★★ ✔
- **Link:** https://ro-alert.ro
- **Ce oferă:** Mesaje oficiale cell-broadcast (ISU/IGSU) pe județ sau zonă: „posibilă incursiune de drone”, „posibilă cădere de obiecte”, încetarea alarmei aeriene
- **Acces:** Doar recepție pe telefon; nu există feed, API sau arhivă publică. Cronologia se reconstituie din comunicatele MApN/IGSU și din Agerpres. Pe 31.10.2026: Iași la 17:04 (nordul județului), Neamț 17:27, Vaslui 17:53, Botoșani 18:10, Bacău 18:15, Suceava 18:44 (ore din presă, 31.10.2026, atribuite MApN; doar ora 17:04 pentru Iași e confirmată în sursa citată, restul se verifică în comunicatul MApN). Încheierea alarmei: Agerpres, agerpres.ro/social/2026/10/31/…-1608742.
- **Cost / autentificare:** Recepție gratuită; feed/API: inexistent sau neconfirmat
- **Licență / termeni:** neconfirmat
- **Actualizare:** Timp real pe telefon. Pe 31.10, primul mesaj a venit la ~40 min după intrarea dronei în MD (16:24 → 17:04). · **Acoperire:** România (pe celule, la nivel de județ sau zonă)
- **Precauții:** Un telefon-receptor dedicat (Android cu jurnal de cell broadcast) poate înregistra mesajele pentru uz intern; fezabilitatea tehnică și juridică e neconfirmată. Mesajele nu precizează mereu zona sau durata (cazul Botoșani). Nu imitați formatul RO-Alert în notificările proprii.
- **Sursă:** https://telem.ro/alerta-de-drone-in-sase-judete-din-moldova-iasi-neamt-vaslui-botosani-bacau-si-suceava/ · încredere medie

### MApN – comunicate de presă ★★★★★ ✔
- **Link:** https://english.mapn.ro/cpresa/356_
- **Ce oferă:** Comunicate despre detecțiile radar, aeronavele ridicate de la sol și încheierea alertelor
- **Acces:** Secțiunea de presă de pe mapn.ro. Anunțurile rapide apar pe pagina de Facebook a MApN (confirmat de Agerpres pe 31.10.2026; URL-ul paginii e neconfirmat). Agerpres preia comunicatele integral. RSS: neconfirmat.
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** Comunicate publice; termenii de reutilizare: neconfirmat
- **Actualizare:** Zeci de minute pe Facebook; ore pentru comunicatul complet · **Acoperire:** România
- **Precauții:** Facebook nu oferă API public de citire fără aprobarea Meta, așa că pentru automatizare folosiți Agerpres și presa ca intermediar. Nu republicați despre aeronavele militare mai mult decât a publicat MApN.
- **Sursă:** https://agerpres.ro/social/2026/10/31/mesaj-ro-alert-in-iasi-si-neamt-despre-posibila-incursiune-de-drona-dupa-ce-a-fost-detectata-de-rada--1608742 · încredere medie

### OpenSky Network – REST API (live) ★★★★★
- **Link:** https://openskynetwork.github.io/opensky-api/rest.html
- **Ce oferă:** Vectori de stare pe bounding box (/states/all), traiectorii (/tracks) și zboruri pe aeroport sau aeronavă (/flights/*).
- **Acces:** REST cu OAuth2 client credentials: client ID și secret din contul OpenSky, token de ~30 min. Basic auth nu mai e acceptat (din 18.03.2026, conform clientului oficial). Bucket-uri de credite separate pentru /states, /tracks și /flights.
- **Cost / autentificare:** Gratuit. Credite: anonim 400/zi, standard 4.000/zi, feeder activ (≥30% uptime) 8.000/zi, licențiat 14.400/oră. Un bbox de cel mult 25 grade² costă 1 credit.
- **Licență / termeni:** Gratuit pentru cercetare/necomercial; uzul comercial cere licență. Statutul unui ONG: neconfirmat.
- **Actualizare:** Secunde · **Acoperire:** Global, dependent de receptoare; densitatea peste Moldova și estul României: neconfirmat
- **Precauții:** La epuizarea creditelor primiți 429, cu header-ul X-Rate-Limit-Retry-After-Seconds. Un bbox de 25,5–30,5°E × 44,8–48,6°N (≈19 grade²) costă 1 credit, deci ~1 cerere la 22 s cu cont standard. Filtrați aeronavele militare/de stat la ingestie; GDPR pentru aeronavele private.
- **Sursă:** https://openskynetwork.github.io/opensky-api/rest.html ; https://github.com/openskynetwork/opensky-api · încredere ridicată

### adsb.lol ★★★★★ ✔
- **Link:** https://adsb.lol
- **Ce oferă:** Poziții ADS-B/MLAT live (format readsb, compatibil cu ADSBexchange RapidAPI), rute plauzibile, arhive istorice zilnice (globe_history).
- **Acces:** REST https://api.adsb.lol/v2/...; documentația interactivă oficială e la api.adsb.lol/docs. Exemplu: /v2/point/{lat}/{lon}/{radius}, cu rază de max. 250 NM (după clienți terți; verificați unitățile în documentație). Istoric: adsb.lol/docs/open-data/historical (release-uri pe GitHub).
- **Cost / autentificare:** Gratuit, deocamdată fără cheie. Repo-ul oficial anunță o cheie viitoare, obținută prin feeding.
- **Licență / termeni:** Datele sunt sub ODbL, ca la OSM (conform repo-ului). Termenii API-ului live și limita oficială de rată: neconfirmat.
- **Actualizare:** Secunde (live); istoric zilnic · **Acoperire:** Global, depinde de feederi
- **Precauții:** Filtrați aeronavele militare. ODbL impune share-alike pentru bazele de date derivate. Dronele Shahed nu emit ADS-B.
- **Sursă:** https://github.com/adsblol/api · încredere medie

### Receptor ADS-B propriu – sdr-enthusiasts/docker-adsb-ultrafeeder ★★★★★
- **Link:** https://github.com/sdr-enthusiasts/docker-adsb-ultrafeeder
- **Ce oferă:** Container all-in-one cu readsb (decodor), tar1090 (hartă locală), graphs1090, autogain, multi-feeder (trimite simultan date la mai mulți agregatori) și mlat-hub. Date locale proprii, independente de agregatori. Există un container separat pentru FR24 (sdr-enthusiasts/docker-flightradar24) și interfețe cu alerte pe watchlist (ex. flightjar: Telegram/ntfy/webhook).
- **Acces:** Docker pe Raspberry Pi sau x86, cu receptor SDR pe 1090 MHz și antenă
- **Cost / autentificare:** Software open-source gratuit; costul hardware: neconfirmat
- **Licență / termeni:** neconfirmat (vezi fișierul LICENSE din repo)
- **Actualizare:** Sub o secundă (local) · **Acoperire:** Raza depinde de antenă și teren (neconfirmat); de la Iași poate acoperi traficul civil de peste Prut și din centrul Moldovei
- **Precauții:** Dronele Shahed/Geran, în general, nu emit ADS-B; receptorul vede doar anomaliile traficului civil. Nu publicați poziții militare. Nu dezvăluiți locația exactă a antenei. Feeding-ul aduce beneficii (OpenSky 8.000 credite/zi, AeroAPI 10 USD/lună).
- **Sursă:** https://github.com/sdr-enthusiasts/docker-adsb-ultrafeeder ; https://github.com/sdr-enthusiasts/docker-flightradar24 ; https://github.com/MrSuttonmann/flightjar · încredere ridicată

### IGSU – pagina oficială Facebook (și DSU) ★★★★☆
- **Link:** https://www.facebook.com/igsu.situatiideurgenta/
- **Ce oferă:** Comunicate IGSU: emiterea RO-Alert, recomandări (nu vă apropiați de obiectele căzute, sunați la 112), apel la surse oficiale, informări după eveniment.
- **Acces:** Web/aplicația Facebook. Fără aprobarea Meta nu există API public de citire a paginilor, deci monitorizarea e manuală. Canale WhatsApp/Telegram IGSU/DSU: neconfirmat. Aplicația DSU: detalii neconfirmate.
- **Cost / autentificare:** gratuit (manual)
- **Licență / termeni:** Termenii Meta; reutilizarea conținutului IGSU: neconfirmat
- **Actualizare:** neconfirmat (de obicei minute–ore după eveniment) · **Acoperire:** Național
- **Precauții:** Scraping-ul Facebook încalcă ToS Meta. Comentariile utilizatorilor sunt date personale (GDPR) și nu se stochează. Folosiți pagina doar ca semnal oficial de confirmare.
- **Sursă:** https://www.facebook.com/igsu.situatiideurgenta/ · încredere medie

### ISU Iași / Botoșani / Suceava / Vaslui / Neamț și Prefectura Iași ★★★★☆
- **Link:** neconfirmat
- **Ce oferă:** Comunicate locale despre alerte și încetarea lor. Exemplu, 8 sep 2026: prefectul Costel Dolachi a spus că drona venea din R. Moldova și că „situația este monitorizată”; alerta s-a încheiat pe la ~17:30, după ce drona a părăsit spațiul aerian. ISU Suceava a dat confirmări privind (ne)căderea unor obiecte.
- **Acces:** Pagini Facebook/site-uri instituționale, monitorizate manual. Conturile și URL-urile exacte: neconfirmat.
- **Cost / autentificare:** gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Minute–ore · **Acoperire:** Județele Iași, Botoșani, Suceava, Vaslui, Neamț
- **Precauții:** Relatările instituțiilor diferă (MApN: 16:37 în SE județului Iași vs. 16:47 lângă Roman). Stocați fiecare declarație cu sursa și ora ei. GDPR pentru comentarii.
- **Sursă:** https://newsweek.ro/actualitate/alerta-de-drona-la-iasi-au-fost-ridicate-doua-avioane-de-lupta-reactia-mapn ; https://spotmedia.ro/stiri/eveniment/ro-alert-in-iasi-vaslui-si-neamt-o-drona-venita-dinspre-republica-moldova-e-monitorizata · încredere scăzută

### Agerpres (agenția națională de presă) ★★★★☆
- **Link:** https://agerpres.ro
- **Ce oferă:** Preia comunicatele MApN (ex. 27.07.2026, „Grup de drone detectat în proximitatea frontierei fluviale cu Ucraina; a fost emis mesaj RO-ALERT”). Are o secțiune de comunicate și o arhivă căutabilă, utile pentru istoric.
- **Acces:** Web. RSS oficial actual: neconfirmat (în 2010 portalul anunța notificări RSS/email). Există un feed terț pe feeder.co, doar pentru secțiunea economică.
- **Cost / autentificare:** Web gratuit; fluxuri profesionale cu abonament (preț neconfirmat)
- **Licență / termeni:** Conținut protejat de drepturi de autor; condițiile de republicare: neconfirmat
- **Actualizare:** Minute–ore · **Acoperire:** România (național)
- **Precauții:** Nu republicați textele integral; afișați titlu + link. Automatizarea prin scraping poate încălca termenii.
- **Sursă:** https://agerpres.ro/2026/07/27/mapn-grup-de-drone---detectat-in-proximitatea-frontierei-fluviale-cu-ucraina-a-fost-emis-mesaj-ro-al--1579665 ; https://www.bursa.ro/lansare-portal-de-stiri-agerpres-4274777 · încredere medie

### EUROCONTROL EAD Basic ★★★★☆
- **Link:** https://www.ead.eurocontrol.int/cms-eadbasic/opencms/en/ead-solutions/ead-basic/
- **Ce oferă:** Bulletine PIB ad-hoc (NOTAM) pe aerodrom sau FIR, plus AIP și hărți. Utile pentru LRIA/LRSV/LRBC, FIR LRBB și FIR Chișinău (LUUU): închideri de aerodrom sau de spațiu aerian.
- **Acces:** Aplicație web după înregistrare gratuită (formularul trimite datele de acces pe email). Fără API; EAD Pro e pentru uz operațional.
- **Cost / autentificare:** Înregistrare gratuită
- **Licență / termeni:** „For general purposes only… shall not be used for operational purposes.” Set limitat de informații.
- **Actualizare:** NOTAM aproape în timp real (neconfirmat exact) · **Acoperire:** Europa (statele EAD)
- **Precauții:** Fără API; automatizarea prin scraping probabil încalcă termenii. Folosiți doar pentru consultare manuală și confirmare. Nu pentru uz operațional.
- **Sursă:** https://www.ead.eurocontrol.int/cms-eadbasic/opencms/en/ead-solutions/ead-basic/ ; https://www.ead.eurocontrol.int/cms-eadbasic/opencms/en/registering · încredere ridicată

### airplanes.live ★★★★☆ ✔
- **Link:** https://airplanes.live/api-guide
- **Ce oferă:** Date ADS-B/MLAT live, nefiltrate
- **Acces:** REST api.airplanes.live/v2. Referința interactivă oficială e la airplanes.live/api-docs/, ghidul la airplanes.live/api-guide (1 cerere/s). Store-ul airplanes.live listează și „api access” contra cost (detalii neconfirmate).
- **Cost / autentificare:** Acces public gratuit, cu limită de rată. Nivel plătit: preț neconfirmat.
- **Licență / termeni:** Termenii sunt la airplanes.live/terms-of-use/ (pagina pare veche, ~3 ani). Clauza de uz necomercial e preluată din catalog și nu a fost reconfirmată din textul termenilor.
- **Actualizare:** Secunde · **Acoperire:** Global
- **Precauții:** „Nefiltrat” înseamnă că sunt incluse aeronave militare și cele blocate în alte rețele: nu le afișați. Un proiect terț raportează că airplanes.live refuză cereri din unele rețele cloud (Fly.io). Testați de pe serverul vostru și păstrați adsb.fi/adsb.lol ca rezervă.
- **Sursă:** https://airplanes.live/api-docs/ · încredere medie

### gov2-ro/ro-alert (prototip dashboard) ★★★☆☆
- **Link:** https://github.com/gov2-ro/ro-alert
- **Ce oferă:** Prototip (PoC) de dashboard RO-Alert pe lab.gov2.ro. Sursa declarată: data.gov.ro și IGSU. Repo-ul include scriptul build_data.py. Nu am putut verifica dacă include mesaje istorice.
- **Acces:** Clonare de pe GitHub (repo public). Din această sesiune nu a putut fi citit.
- **Cost / autentificare:** gratuit
- **Licență / termeni:** neconfirmat (verificați fișierul LICENSE)
- **Actualizare:** neconfirmat (probabil static) · **Acoperire:** România – neconfirmat
- **Precauții:** Conținutul nu a fost verificat; nu îl tratați ca arhivă oficială. Căutarea pe GitHub nu a găsit altă arhivă RO-Alert.
- **Sursă:** https://github.com/gov2-ro/ro-alert · încredere scăzută

### Presa regională și națională RO (BZI, Ziarul de Iași, Radio România Iași, Digi24, HotNews) ★★★☆☆
- **Link:** https://www.bzi.ro
- **Ce oferă:** Relatări rapide despre RO-Alert, suspendări de zboruri la Aeroportul Iași (8 sep 2026, toate zborurile suspendate temporar după RO-Alert de la ~16:37), întârzieri și diversiuni.
- **Acces:** RSS: URL-uri neconfirmate. Le găsiți în sursa paginii, la `<link rel="alternate" type="application/rss+xml">`.
- **Cost / autentificare:** gratuit
- **Licență / termeni:** Drepturi de autor ale publicațiilor; afișați titlu + link
- **Actualizare:** Minute · **Acoperire:** Iași / Moldova / național
- **Precauții:** Calitate variabilă; orele și datele diferă între articole; risc de dezinformare. Marcați aceste știri ca „neconfirmat oficial”.
- **Sursă:** https://www.ziarulprofit.ro/alerta-de-atac-cu-drone-in-cinci-judete-din-moldova-aeroportul-din-iasi-a-fost-inchis/ ; https://spotmedia.ro/stiri/eveniment/ro-alert-in-iasi-vaslui-si-neamt-o-drona-venita-dinspre-republica-moldova-e-monitorizata · încredere scăzută

### ROMATSA – hartă zone geografice UAS (flightplan portal) ★★★☆☆ ✔
- **Link:** https://flightplan.romatsa.ro/init/drones
- **Ce oferă:** Harta oficială a zonelor geografice UAS (restricționate sau interzise); NOTAM-urile active sunt afișate separat. Versiunea e valabilă din 30.04.2026 (zone noi RZ1076 și RZ0177; CTR LROP modificat pe 26.11.2025).
- **Acces:** Hartă web, plus fișiere descărcabile .shp, .json și .xlsx de pe aceeași pagină. Există și pagina /init/drones/manage_zones.
- **Cost / autentificare:** Gratuit (vizualizare și descărcare)
- **Licență / termeni:** neconfirmat
- **Actualizare:** Versiuni periodice sau ad-hoc; NOTAM-urile se actualizează separat · **Acoperire:** România
- **Precauții:** ROMATSA avertizează că lipsa zonelor de pe hartă nu înseamnă lipsa restricțiilor (reîmprospătați cache-ul). Zona de excludere de 30 km de la granița cu Ucraina, în nordul Dobrogei, apare doar într-un ghid privat: verificați ordinul în Monitorul Oficial.
- **Sursă:** https://flightplan.romatsa.ro/init/drones · încredere ridicată

### ROMATSA AIS – eAIP România și NOTAM (aisro.ro) ★★★☆☆
- **Link:** https://www.aisro.ro
- **Ce oferă:** AIP România (zone P/R/D din ENR 5, aerodromurile LRIA, LRSV, LRBC), amendamente, suplimente, NOTAM.
- **Acces:** Web. Briefing online și înregistrare: neconfirmat.
- **Cost / autentificare:** neconfirmat
- **Licență / termeni:** neconfirmat
- **Actualizare:** AIP pe cicluri AIRAC; NOTAM: neconfirmat · **Acoperire:** FIR București (LRBB)
- **Precauții:** Datele de contact provin dintr-un profil FAA din 2014; verificați pe site-ul live. Pentru automatizare, preferați EAD Basic (manual) sau un furnizor autorizat.
- **Sursă:** https://www.faa.gov/air_traffic/publications/ifim/country_info/PDF/RO.pdf · încredere scăzută

### EASA Conflict Zone Information Bulletins (CZIB) ★★★☆☆
- **Link:** https://www.easa.europa.eu/en/domains/air-operations/czibs
- **Ce oferă:** CZIB-2022-01R14 Ucraina: acoperă toate nivelurile de zbor din FIR UKLV, UKBV, UKBU, UKDV, UKFV și UKOV. Revizia din 24.07.2026 a prelungit valabilitatea până la 31.01.2027, fără modificări de conținut. În 2022, CZIB includea și FIR Chișinău; ulterior a fost revizuit la redeschiderea parțială a spațiului moldovenesc (dată neconfirmată).
- **Acces:** Pagini web + PDF. RSS/API: neconfirmat.
- **Cost / autentificare:** gratuit
- **Licență / termeni:** neconfirmat (conținut public EASA)
- **Actualizare:** Revizuiri la câteva luni · **Acoperire:** Zone de conflict relevante pentru operatorii UE
- **Precauții:** Strat de context strategic, nu tactic. Statutul curent al FIR Chișinău (LUUU) în CZIB nu a fost confirmat.
- **Sursă:** https://www.easa.europa.eu/en/domains/air-operations/czibs/czib-2022-01r14 · încredere ridicată

### Safe Airspace (safeairspace.net) ★★★☆☆
- **Link:** https://safeairspace.net/summary/
- **Ce oferă:** Rezumat de risc pentru zonele de conflict (ex. actualizarea din 25.10.2026). Moldova e la nivelul 2 (risc evaluat), cu risc secundar de spillover drone/rachete; operatorii francezi sunt sfătuiți să evite zona de lângă granița cu Ucraina. Are pagini separate pentru Ucraina și alte țări.
- **Acces:** Web. Feed/API: neconfirmat.
- **Cost / autentificare:** gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Zile · **Acoperire:** Global
- **Precauții:** Agregator neoficial; citați cu link. Nu îl folosiți ca semnal tactic.
- **Sursă:** https://safeairspace.net/summary/ · încredere medie

### OpenSky Network – baza istorică (Trino) ★★★☆☆
- **Link:** https://pypi.org/project/pyopensky/
- **Ce oferă:** Baza istorică (state vectors, liste de zboruri) pentru analize retrospective: modele normale de trafic, închideri și diversiuni anterioare în zonă.
- **Acces:** Trino prin biblioteca pyopensky (shell-ul Impala e depreciat). Acces pe bază de cerere: formularul opensky-network.org/data/apply apare într-o sursă din 2020 și trebuie verificat.
- **Cost / autentificare:** Gratuit pentru cercetare la instituții academice/guvernamentale; eligibilitatea ONG: neconfirmat. Licență comercială disponibilă (preț neconfirmat).
- **Licență / termeni:** Termeni OpenSky pentru cercetare
- **Actualizare:** Istoric (decalaj neconfirmat) · **Acoperire:** Global
- **Precauții:** Aprobarea e manuală; un parteneriat cu o universitate ar putea facilita accesul (neconfirmat). Excludeți aeronavele militare și din analizele publicate.
- **Sursă:** https://pypi.org/project/pyopensky/ ; https://en.wikipedia.org/wiki/OpenSky_Network · încredere medie

### FlightAware AeroAPI ★★★☆☆
- **Link:** https://flightaware.com/commercial/aeroapi/
- **Ce oferă:** Status zboruri, poziții, istoric, sosiri/plecări și întârzieri pe aeroport (util pentru LRIA/LRSV/LRBC).
- **Acces:** REST v4, interogare pe cerere, cu cheie API
- **Cost / autentificare:** Nivel Personal: fără minim lunar, până la 5 USD/lună gratuit (10 USD pentru feederii ADS-B), apoi plată per result set (15 înregistrări). Limită ~10 result sets/min (sursă terță).
- **Licență / termeni:** Nivelul Personal permite doar uz personal/academic. Pentru un dashboard public probabil e nevoie de alt nivel (neconfirmat).
- **Actualizare:** Secunde–minute · **Acoperire:** Global
- **Precauții:** Un dashboard public nu se încadrează în uzul personal; verificați nivelul de licență. Costurile cresc cu paginarea.
- **Sursă:** https://flightaware.com/commercial/aeroapi/ · încredere ridicată

### aisstream.io ★★★☆☆ ✔
- **Link:** https://aisstream.io
- **Ce oferă:** Mesaje AIS live (poziții de nave). Context pentru Dunăre și Marea Neagră (Galați, Tulcea, Izmail, Reni).
- **Acces:** WebSocket wss://stream.aisstream.io/v0/stream. Mesajul JSON de abonare trebuie trimis în cel mult 3 s și conține APIKey, BoundingBoxes (obligatoriu) și, opțional, FiltersShipMMSI (max. 200 în documentația curentă, 50 într-o pagină veche) și FilterMessageTypes. Compresia permessage-deflate e opțională.
- **Cost / autentificare:** Cheie gratuită, cu înregistrare. Max. 3 conexiuni abonate pe cont și 3 conexiuni pe IP; max. o actualizare de abonare pe secundă; throttling pe cheie și pe utilizator.
- **Licență / termeni:** neconfirmat
- **Actualizare:** Secunde · **Acoperire:** Global (stații comunitare). Acoperirea Dunării de Jos: neconfirmat.
- **Precauții:** Țineți cheia doar pe server și trimiteți clienților doar datele de care au nevoie. Mesajele se pierd dacă nu sunt consumate repede. AIS poate fi falsificat sau oprit. Nu urmăriți nave militare.
- **Sursă:** https://aisstream.io/documentation · încredere ridicată

### virgil-ideas/eu-drone-events-2026 ★★★☆☆
- **Link:** https://github.com/virgil-ideas/eu-drone-events-2026
- **Ce oferă:** Hartă interactivă și cronologie a evenimentelor cu drone din UE în 2026, cu surse și culori pe tipul rezultatului.
- **Acces:** GitHub (HTML static); conținutul nu a fost verificat
- **Cost / autentificare:** gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Ultima actualizare pe GitHub: 29.10.2026 · **Acoperire:** UE 2026; includerea RO/MD: neconfirmat
- **Precauții:** Proiect recent, de proveniență necunoscută. Folosiți-l doar ca punct de plecare spre sursele primare.
- **Sursă:** https://github.com/virgil-ideas/eu-drone-events-2026 · încredere scăzută

### FAA NOTAM Management Service (NMS-API) ★★☆☆☆
- **Link:** https://www.faa.gov/about/initiatives/notam/faqs
- **Ce oferă:** API NOTAM al FAA, aflat în tranziție la formatul ICAO. Acoperirea NOTAM-urilor internaționale (LR/LU): neconfirmat. Alternativa istorică pentru NOTAM internaționale este DINS (notams.faa.gov); accesul automatizat: neconfirmat.
- **Acces:** Accesul la NMS-API se cere de la FAA (contact în FAQ). Un client terț indică adresa NOTAMS@faa.gov.
- **Cost / autentificare:** Credențiale la cerere; cost neconfirmat
- **Licență / termeni:** neconfirmat
- **Actualizare:** neconfirmat · **Acoperire:** SUA (confirmat); internațional: neconfirmat
- **Precauții:** Eligibilitatea unui ONG din România e neconfirmată. Pentru Europa, preferați EAD Basic.
- **Sursă:** https://www.faa.gov/about/initiatives/notam/faqs ; https://www.notams.faa.gov/about.html · încredere medie

### ADS-B Exchange (API RapidAPI / Enterprise) ★★☆☆☆
- **Link:** https://www.adsbexchange.com
- **Ce oferă:** Date ADS-B/MLAT live, prin API personal (RapidAPI) sau enterprise.
- **Acces:** RapidAPI, listarea „ADSBExchange.com”, planul Personal Use. Uzul comercial necesită contract enterprise.
- **Cost / autentificare:** ~10 USD/lună pentru 10.000 cereri, uz personal (sursă terță; altă sursă terță indică 19 USD). Enterprise: preț nepublicat.
- **Licență / termeni:** Personal/necomercial pe RapidAPI; uzul comercial doar prin enterprise
- **Actualizare:** Secunde · **Acoperire:** Global
- **Precauții:** Cifrele provin din surse terțe și se contrazic; verificați pe RapidAPI. ADSBx și-a retras sau schimbat serviciile API (forum X-Plane). Pentru un ONG, adsb.lol sau airplanes.live sunt mai potrivite.
- **Sursă:** https://skylinkapi.com/blog/ads-b-exchange-api-pricing-commercial-use-alternatives/ ; https://forums.x-plane.org/forums/topic/326044-ads-b-exchange-is-retiringchanging-api-services/ · încredere scăzută

### Flightradar24 API ★★☆☆☆
- **Link:** https://www.flightradar24.com/blog/b2b/flightradar24-api/
- **Ce oferă:** Poziții live, istoric de zboruri, informații despre aeroporturi, pe bază de credite.
- **Acces:** REST API cu cheie; sandbox gratuit care nu consumă credite
- **Cost / autentificare:** Explorer: 9 USD/lună, 60.000 credite/lună (blog FR24, posibil depășit). Essential/Advanced: neconfirmat.
- **Licență / termeni:** Termeni comerciali FR24; redistribuirea publică: neconfirmat
- **Actualizare:** Secunde · **Acoperire:** Global
- **Precauții:** Verificați pagina oficială de prețuri și T&C-ul actualizat. Excludeți aeronavele militare.
- **Sursă:** https://www.flightradar24.com/blog/b2b/flightradar24-api/ · încredere medie

### VesselFinder API ★★☆☆☆
- **Link:** https://www.vesselfinder.com/vessel-positions-api
- **Ce oferă:** Poziții de nave (AIS terestru și satelit), voiaje, date master. Separat există Live Data API pentru toate navele dintr-o zonă (abonament).
- **Acces:** REST cu credite preplătite
- **Cost / autentificare:** 10.000 credite = 330 EUR; 20.000 = 625 EUR; 50.000 = 1.470 EUR (fără TVA), valabile 12 luni. 1 credit/înregistrare AIS terestru, 10 credite/înregistrare satelit.
- **Licență / termeni:** Comercial, conform termenilor VesselFinder
- **Actualizare:** Minute (neconfirmat exact) · **Acoperire:** Global
- **Precauții:** Costuri mari pentru monitorizare continuă; preferați aisstream.io pentru prototip.
- **Sursă:** https://www.vesselfinder.com/vessel-positions-api ; https://api.vesselfinder.com/ · încredere ridicată

### MarineTraffic API ★★☆☆☆
- **Link:** https://www.marinetraffic.com
- **Ce oferă:** Endpoint-uri pentru poziții de flotă, port, zonă și navă individuală.
- **Acces:** REST cu cheie (detalii neconfirmate)
- **Cost / autentificare:** neconfirmat
- **Licență / termeni:** neconfirmat (comercial)
- **Actualizare:** neconfirmat · **Acoperire:** Global
- **Precauții:** Prețurile și termenii nu au fost găsiți; verificați direct.
- **Sursă:** https://providers.apievangelist.com/providers/marine-traffic/ · încredere scăzută

## Hărți de bază, GIS, platforme de afișare și livrarea alertelor

### geoBoundaries (gbOpen) ★★★★★
- **Link:** https://www.geoboundaries.org
- **Ce oferă:** Limite administrative ADM0–ADM2 (și mai jos unde există) pentru România, Moldova, Ucraina într-o schemă unitară; strat de bază transfrontalier pentru maparea regiunilor de alertă
- **Acces:** Descărcare GeoJSON/Shapefile; disponibil și în Google Earth Engine (WM/geoLab/geoBoundaries) și prin pachetul R geobounds; endpoint API direct neconfirmat în sesiune
- **Cost / autentificare:** Gratuit, fără înregistrare
- **Licență / termeni:** Majoritar CC BY 4.0, dar gbOpen conține și ODbL, CC BY-SA, licențe naționale; licența fiecărui fișier e în metadate. gbAuthoritative (UN SALB) = doar necomercial
- **Actualizare:** Versiuni periodice (v6.0.0 în GEE); fără flux în timp real · **Acoperire:** Global, inclusiv RO, MD, UA
- **Precauții:** Verificați licența per fișier (nu presupuneți CC BY 4.0 pentru tot); nu folosiți setul SALB într-un produs comercial; atribuire obligatorie
- **Sursă:** https://stat.ethz.ch/CRAN/web/packages/geobounds/COPYRIGHTS · încredere ridicată

### HDX COD-AB Ucraina (Common Operational Dataset – Administrative Boundaries) ★★★★★
- **Link:** https://data.humdata.org/dataset/cod-ab-ukr
- **Ce oferă:** Admin1: 27 oblasti; Admin2: 139 raioane; Admin3: 1769 hromade; Admin4: 29.706 localități (acoperire parțială); versiunea 05; există și varianta COD-EM edge-matched
- **Acces:** Descărcare de pe HDX (SHP/GeoJSON etc., formate exacte neconfirmate; data.humdata.org a fost inaccesibil din sesiune)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat (o listare derivată arată cc-by-igo cu isopen=False)
- **Actualizare:** Limite ajustate ultima dată în ianuarie 2025; hromadele modificate la începutul lui 2024 · **Acoperire:** Ucraina
- **Precauții:** Licența trebuie verificată direct pe HDX; ID-urile regiunilor din alerts.in.ua/ukrainealarm trebuie legate manual de codurile COD-AB (nu există tabel de corespondență confirmat); datele de populație COD-PS doar la cerere
- **Sursă:** https://geo.btaa.org/catalog/d23f529f-31e4-4021-a65b-13987e5cfb42 · încredere medie

### OpenStreetMap – extrase Geofabrik (RO/MD/UA) ★★★★★
- **Link:** https://download.geofabrik.de/europe.html
- **Ce oferă:** Date OSM complete: drumuri, căi ferate, linii electrice, piloni, turnuri, castele de apă, școli, biserici, aerodromuri; bază pentru amplasarea senzorilor și pentru harta surselor de zgomot
- **Acces:** Descărcare .osm.pbf/shapefile per țară; procesare locală cu QGIS, osmium, osm2pgsql
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** ODbL (© OpenStreetMap contributors); share-alike pentru baze de date derivate (neverificat în sesiune pentru Geofabrik)
- **Actualizare:** Extrase actualizate frecvent (zilnic, neverificat în sesiune) · **Acoperire:** România, Moldova, Ucraina
- **Precauții:** Nu publicați straturi de amplasare a senzorilor sau hărți de infrastructură critică suprapuse pe rute de drone; atribuire obligatorie
- **Sursă:** https://www.openstreetmap.org/copyright · încredere medie

### Telegram Bot API ★★★★★
- **Link:** https://core.telegram.org/bots/api
- **Ce oferă:** Boți pentru alerte în grupuri și canale, comenzi, abonări
- **Acces:** HTTPS Bot API (token de la @BotFather)
- **Cost / autentificare:** Gratuit; broadcast plătit peste 30 msg/s (0,1 Stars/mesaj, până la 1000 msg/s)
- **Licență / termeni:** Termenii Telegram
- **Actualizare:** Secunde · **Acoperire:** Global
- **Precauții:** Limite: ~1 msg/s per chat, 20 msg/min într-un grup, ~30 msg/s total (eroare 429); chaturile cu boți nu sunt criptate end-to-end; nu postați poziții sau traiectorii în timp real în canale publice
- **Sursă:** https://core.telegram.org/bots/faq · încredere ridicată

### ntfy ★★★★★
- **Link:** https://ntfy.sh
- **Ce oferă:** Notificări push prin HTTP PUT/POST pe topicuri; aplicații Android/iOS/web; atașamente, priorități
- **Acces:** Self-hosted (binar/Docker) sau serviciul ntfy.sh
- **Cost / autentificare:** Self-hosted gratuit; ntfy.sh are plan gratuit cu limite de rată și planuri plătite (prețuri neconfirmate, vezi ntfy.sh/#pricing)
- **Licență / termeni:** Apache 2.0 și GPLv2
- **Actualizare:** Secunde · **Acoperire:** Global
- **Precauții:** Pe instanța publică folosiți topicuri rezervate sau cu control de acces; la self-host configurați voi limitele de rată și autentificarea
- **Sursă:** https://docs.ntfy.sh/faq/ · încredere ridicată

### geo-spatial.org – limite UAT România (oglindă GitHub akaleeroy/romania-uat) ★★★★☆
- **Link:** https://github.com/akaleeroy/romania-uat
- **Ce oferă:** Poligoane UAT (comune/orașe/municipii) cu cod SIRUTA în câmpul natcode; datate 20.12.2019
- **Acces:** GeoJSON descărcabil din repo; proiecție EPSG:3844 (Stereo70)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat (o postare din 2010 pe lista OSM afirmă domeniu public, neoficial)
- **Actualizare:** Static (2019) · **Acoperire:** România
- **Precauții:** Reproiectați din EPSG:3844 în EPSG:4326 pentru hărți web; licență neconfirmată; limitele pot fi depășite de modificări UAT
- **Sursă:** https://github.com/akaleeroy/romania-uat · încredere medie

### Copernicus DEM GLO-30 ★★★★☆
- **Link:** https://registry.opendata.aws/copernicus-dem/
- **Ce oferă:** Model digital de suprafață la ~30 m; util pentru viewshed (amplasare senzori acustici/optici), profile de teren, culoare de zbor la joasă altitudine
- **Acces:** AWS S3 arn:aws:s3:::copernicus-dem-30m (eu-central-1), listare fără cont cu --no-sign-request; COG-uri
- **Cost / autentificare:** Gratuit, fără cont
- **Licență / termeni:** Licență Copernicus DEM GLO-30 „Full, Free & Open” (PDF ESA); licența afișată pe AWS poate fi o versiune mai veche
- **Actualizare:** Static · **Acoperire:** Global; unele țări nepublice, lista e separată (RO/MD/UA neconfirmat dacă sunt afectate)
- **Precauții:** Este DSM (include clădiri și vegetație), nu DTM; verificați licența curentă
- **Sursă:** https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/DEM/resources/license/License-COPDEM-30.pdf · încredere ridicată

### Overpass API (OSM) ★★★★☆
- **Link:** https://overpass-api.de
- **Ce oferă:** Interogări punctuale pe date OSM, de ex. man_made=mast|tower|water_tower, tower:type=communication, power=line|tower|substation, amenity=school|place_of_worship|hospital, railway=rail, highway=motorway|trunk|primary, aeroway=aerodrome
- **Acces:** HTTP API cu Overpass QL; interfață web overpass-turbo; răspuns 429 la depășire; utilizatorul e identificat după IP
- **Cost / autentificare:** Gratuit (instanța publică)
- **Licență / termeni:** Date ODbL
- **Actualizare:** Aproape timp real față de baza OSM · **Acoperire:** Global
- **Precauții:** Ghid: max. ~10.000 cereri/zi și ~1 GB/zi; pentru utilizare recurentă de ~100 de ori mai puțin (≈<100 cereri/zi), însumat pe toți utilizatorii aplicației. Nu folosiți pentru polling din dashboard; folosiți extrase locale
- **Sursă:** https://dev.overpass-api.de/overpass-doc/en/preface/commons.html · încredere ridicată

### GHSL GHS-POP R2023A (JRC / Copernicus) ★★★★☆
- **Link:** https://human-settlement.emergency.copernicus.eu/ghs_pop2023.php
- **Ce oferă:** Grilă de populație (persoane/celulă) la 100 m, epoci 1975–2030 din 5 în 5 ani; pentru estimarea populației de sub culoarele de survol
- **Acces:** Descărcare GeoTIFF de pe site; AWS S3 arn:aws:s3:::jrc-ghsl/ghs-pop (eu-central-1, fără cont); GEE community catalog; STAC pe source.coop
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** CC BY 4.0 (un catalog indică eronat CC0)
- **Actualizare:** Lansări multianuale · **Acoperire:** Global
- **Precauții:** Proiecție Mollweide (reproiectați); estimări modelate, nu recensământ; atribuire obligatorie
- **Sursă:** https://registry.opendata.aws/ghs-pop/ · încredere ridicată

### Grafana OSS – panoul Geomap ★★★★☆
- **Link:** https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/geomap/
- **Ce oferă:** Hartă cu mai multe straturi peste date de serii de timp (markeri, heatmap, GeoJSON static în v10, GeoJSON dinamic alpha în 9.x); strat de bază configurabil prin provisioning
- **Acces:** Self-hosted (Docker/binare); surse de date: PostgreSQL/PostGIS, InfluxDB, JSON/Infinity etc.
- **Cost / autentificare:** Gratuit self-hosted; Grafana Cloud cu prețuri neconfirmate
- **Licență / termeni:** AGPLv3 (neverificat în sesiune)
- **Actualizare:** Timp real (refresh configurabil) · **Acoperire:** N/A
- **Precauții:** Tipurile de straturi diferă între versiuni (lista din documentația v13 nu mai arată stratul GeoJSON); nu expuneți fără autentificare; tabloul intern nu se face public
- **Sursă:** https://grafana.com/docs/grafana/v10.0/panels-visualizations/visualizations/geomap · încredere medie

### Leaflet ★★★★☆
- **Link:** https://leafletjs.com
- **Ce oferă:** Bibliotecă JS ușoară pentru hărți web publice (straturi GeoJSON, tile-uri raster)
- **Acces:** Bibliotecă JS (CDN/npm)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** BSD-2-Clause (neverificat în sesiune)
- **Actualizare:** N/A · **Acoperire:** N/A
- **Precauții:** Nu încărcați tile-uri de pe tile.openstreetmap.org la volum mare; folosiți tile-uri proprii sau PMTiles
- **Sursă:** https://leafletjs.com · încredere medie

### MapLibre GL JS + PMTiles (Protomaps) ★★★★☆
- **Link:** https://maplibre.org
- **Ce oferă:** Hărți vectoriale WebGL; cu PMTiles se servesc hărți de bază offline sau self-hosted dintr-un singur fișier static
- **Acces:** Bibliotecă JS (npm/CDN); PMTiles servit de pe orice server static sau S3
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** BSD-3-Clause (neverificat în sesiune)
- **Actualizare:** N/A · **Acoperire:** N/A
- **Precauții:** Hărțile de bază derivate din OSM păstrează atribuirea ODbL
- **Sursă:** https://maplibre.org · încredere medie

### QGIS ★★★★☆
- **Link:** https://qgis.org
- **Ce oferă:** Analiză offline: viewshed/vizibilitate pe DEM, buffere, amplasare senzori, joncțiuni SIRUTA/COD-AB, export GeoJSON/PMTiles
- **Acces:** Aplicație desktop (Windows/macOS/Linux)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** GPL (neverificat în sesiune)
- **Actualizare:** N/A · **Acoperire:** N/A
- **Precauții:** Proiectele cu amplasamente de senzori rămân interne
- **Sursă:** https://qgis.org · încredere medie

### TAK – clienți ATAK-CIV / iTAK / WinTAK ★★★★☆
- **Link:** https://tak.gov
- **Ce oferă:** Hartă comună de echipă (Cursor-on-Target), chat, marcaje, pachete de date, hărți offline; clienți Android/iOS/Windows
- **Acces:** Distribuire prin tak.gov și magazinele de aplicații (detalii neverificate în sesiune)
- **Cost / autentificare:** neconfirmat
- **Licență / termeni:** neconfirmat
- **Actualizare:** Timp real în rețea · **Acoperire:** N/A
- **Precauții:** Pozițiile voluntarilor sunt date personale (GDPR: consimțământ, retenție); folosiți doar cu server propriu securizat
- **Sursă:** https://github.com/brian7704/OpenTAKServer · încredere scăzută

### OpenTAKServer (OTS) ★★★★☆
- **Link:** https://github.com/brian7704/OpenTAKServer
- **Ce oferă:** Server TAK open source: conexiuni TCP/SSL de la ATAK, WinTAK, iTAK, TAKAware, TAKX, CloudTAK, PyTAK; LDAP/Active Directory; streaming video; Mission API
- **Acces:** Self-hosted (instalare Python; imagini Docker comunitare)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** GPL-3.0
- **Actualizare:** Timp real · **Acoperire:** N/A
- **Precauții:** Expus pe internet doar cu TLS + certificate client; forkurile au seturi de funcții diferite
- **Sursă:** https://github.com/brian7704/OpenTAKServer · încredere ridicată

### Node-RED ★★★★☆
- **Link:** https://nodered.org
- **Ce oferă:** Fluxuri low-code: polling HTTP (alerts.in.ua, ukrainealarm), MQTT (Meshtastic), normalizare, deduplicare, trimitere spre Telegram/ntfy/baze de date
- **Acces:** Self-hosted (npm/Docker/Raspberry Pi)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** Apache-2.0 (neverificat în sesiune)
- **Actualizare:** Timp real · **Acoperire:** N/A
- **Precauții:** Activați autentificarea pe editor; nu stocați tokenuri API în fluxuri exportate
- **Sursă:** https://nodered.org · încredere medie

### Pushover ★★★★☆
- **Link:** https://pushover.net
- **Ce oferă:** Notificări push fiabile pe iOS/Android/desktop, prin API simplu
- **Acces:** API HTTPS (token de aplicație + cheie utilizator)
- **Cost / autentificare:** 4,99 USD o singură dată per platformă (iOS, Android, Desktop); Pushover for Teams: 5 USD/utilizator/lună
- **Licență / termeni:** Termeni comerciali Pushover
- **Actualizare:** Secunde · **Acoperire:** Global
- **Precauții:** 10.000 mesaje/lună gratuit per cont, comun tuturor aplicațiilor contului (Teams: 25.000); data trecerii la limita per cont (1 mai 2026) vine doar dintr-un blog
- **Sursă:** https://support.pushover.net/i12-message-size-and-frequency-limitations · încredere medie

### Meshtastic (LoRa mesh, EU_868) ★★★★☆
- **Link:** https://meshtastic.org
- **Ce oferă:** Mesagerie text și poziții offline prin mesh LoRa între noduri ieftine; gateway MQTT opțional spre Node-RED
- **Acces:** Firmware open source pe noduri LoRa; aplicații Android/iOS/web; configurare regiune EU_868
- **Cost / autentificare:** Software gratuit; cost hardware neconfirmat
- **Licență / termeni:** Firmware open source (licența exactă neverificată în sesiune)
- **Actualizare:** Secunde–minute (în funcție de hopuri și duty cycle) · **Acoperire:** Local (km, în funcție de teren și antene)
- **Precauții:** EU_868: 869,4–869,65 MHz, duty cycle 10% pe oră glisantă (nodul se oprește la atingerea limitei), max. 27 dBm ERP; schimbați PSK-ul implicit (canalul implicit e public); dezactivați uplink-ul MQTT public; pozițiile sunt date personale; cadrul național ANCOM/ANRCETI neverificat
- **Sursă:** https://meshtastic.org/docs/configuration/radio/lora · încredere ridicată

### ANCPI Geoportal INSPIRE – Unități administrative (RELUAT) ★★★☆☆
- **Link:** https://geoportal.ancpi.ro
- **Ce oferă:** Limitele UAT din proiectul RELUAT (geometrie linie), cu limitele nesoluționate marcate ca contestate
- **Acces:** Serviciu de descărcare ATOM (fișier Main_ATOM_AU.xml; calea completă se ia din GetCapabilities la geoportal.ancpi.ro), EPSG:4258; serviciu de vizualizare WMS la geoportal.ancpi.ro/inspireview; WFS neconfirmat
- **Cost / autentificare:** neconfirmat (probabil gratuit)
- **Licență / termeni:** neconfirmat
- **Actualizare:** Publicare 2012-12-09, revizie 2016-12-07; metadatele spun că datele sunt în actualizare · **Acoperire:** România
- **Precauții:** Set vechi; limite contestate; fără WFS confirmat; verificați actualitatea înainte de folosire
- **Sursă:** https://inspire-geoportal.ec.europa.eu/srv/api/records/%7B58A5960D-901A-47E4-9CEA-FB6F29D15E64%7D · încredere medie

### data.gov.ro – set de date UAT (24.02.2021) ★★★☆☆
- **Link:** https://data.gov.ro
- **Ce oferă:** Limite UAT oficiale publicate pe portalul de date deschise
- **Acces:** Descărcare de pe data.gov.ro (format și URL exact neconfirmate)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Set datat 24.02.2021 · **Acoperire:** România
- **Precauții:** Identificat doar indirect (folosit ca sursă de comunitatea OSM); verificați licența și versiunea
- **Sursă:** https://lists.openstreetmap.org/pipermail/talk-ro/2022-October/003437.html · încredere scăzută

### SIRUTA (INS) – Registrul localităților și UAT ★★★☆☆
- **Link:** https://insse.ro
- **Ce oferă:** Coduri unice pentru localități și UAT; cheie de joncțiune între geometrii UAT și statisticile INS (TEMPO, RPL2021)
- **Acces:** Descărcare de pe site-ul INS (URL exact neconfirmat în sesiune)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat (discuții OSM din 2010: fără licență explicită)
- **Actualizare:** Actualizat la modificări administrative; frecvență neconfirmată · **Acoperire:** România
- **Precauții:** Opinia despre licență vine din comunitate, nu e aviz juridic
- **Sursă:** https://lists.openstreetmap.org/pipermail/talk-ro/2010-September/001367.html · încredere scăzută

### geodata.gov.md – geoportalul tematic AGCC (R. Moldova) ★★★☆☆ ✔
- **Link:** https://geodata.gov.md
- **Ce oferă:** Straturi spațiale oficiale ale R. Moldova (rețele geodezice, grile, alte straturi tematice), publicate ca WMS
- **Acces:** Portalul geodata.gov.md (WMS; URL-urile GetCapabilities sunt neconfirmate). Rapoartele INDS plasează unitățile administrative de nivel 1 și 2 pe cadastru.md/ecadastru, nu pe geodata.gov.md. Portaluri mai vechi: geoportalinds.gov.md (WMS/WMTS/WCS/WFS) și harta.asd.md. Oglinda neoficială de pe source.coop notează că straturile wms_* sunt doar linkuri WMS live, fără WFS/WCS.
- **Cost / autentificare:** neconfirmat
- **Licență / termeni:** neconfirmat
- **Actualizare:** neconfirmat · **Acoperire:** R. Moldova
- **Precauții:** Pentru limite vectoriale folosiți geoBoundaries sau HDX până se confirmă un WFS oficial. Agenția și-a schimbat numele (ARFC → AGCC); unele date sunt produse de INGEOCAD.
- **Sursă:** https://inds.gov.md/wp-content/uploads/sites/6/2025/08/Monitorizare_INDS_ISEM_2025.signed.pdf · încredere scăzută

### Moldova geodata – oglindă cloud-native (source.coop, neoficială) ★★★☆☆
- **Link:** https://source.coop/nlebovits/moldova-geodata
- **Ce oferă:** Copie a straturilor geodata.gov.md în GeoParquet și PMTiles; colecțiile wms_* (de ex. DTM) sunt doar linkuri la WMS live
- **Acces:** HTTP/S3 (catalog STAC: data.source.coop/nlebovits/moldova-geodata/catalog.json); EPSG:4026
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Snapshot; frecvență neconfirmată · **Acoperire:** Republica Moldova
- **Precauții:** Nu e publicație oficială AGCC; straturile WMS nu au WFS/WCS
- **Sursă:** https://data.source.coop/nlebovits/moldova-geodata/README.md · încredere medie

### ANCOM aisemnal.ro – harta semnalului mobil ★★★☆☆
- **Link:** https://www.aisemnal.ro
- **Ce oferă:** Hartă de acoperire pentru voce 2G/3G/4G, toți operatorii, din campanii de drive-test ANCOM 2019–2024 pe drumuri naționale, județene și comunale; include metroul din București
- **Acces:** Hartă web + aplicație Android (ro.ancom.aisemnal); niciun flux de date deschise confirmat
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Campanii anuale · **Acoperire:** România (drumuri publice)
- **Precauții:** Măsurători doar pe drumuri și în spații publice; fără API; util pentru alegerea între LTE și LoRa la senzori
- **Sursă:** https://www.aisemnal.ro/despre-harta · încredere ridicată

### OpenCelliD ★★★☆☆
- **Link:** https://opencellid.org
- **Ce oferă:** Bază de date cu poziții estimate ale celulelor (MCC/MNC/LAC/CID), din crowdsourcing; oglindă PMTiles pe source.coop
- **Acces:** API și descărcare completă (CSV gz ~105 MB) cu token de cont; oglindă PMTiles: source.coop/smartmaps/opencellid
- **Cost / autentificare:** Înregistrare necesară; limite și niveluri de preț neconfirmate
- **Licență / termeni:** CC BY-SA 4.0 (bazele de date derivate se distribuie sub aceeași licență)
- **Actualizare:** Continuu (crowdsourcing); frecvența dump-urilor neconfirmată · **Acoperire:** Global (densitate variabilă în MD/UA)
- **Precauții:** Pozițiile sunt estimate, nu amplasamente reale ale antenelor; share-alike; nu publicați straturi derivate fără atribuire
- **Sursă:** https://en.wikipedia.org/wiki/OpenCelliD · încredere medie

### WorldPop (100 m) ★★★☆☆
- **Link:** https://www.worldpop.org
- **Ce oferă:** Populație estimată la 100 m, 2000–2021 (GEE WorldPop/GP/100m/pop); Moldova și pe HDX (2000–2020, variante constrained/unconstrained)
- **Acces:** Descărcare web, HDX, Google Earth Engine
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** CC BY 4.0 (citați www.worldpop.org)
- **Actualizare:** Serii anuale, oprite în 2020–2021 · **Acoperire:** Global
- **Precauții:** Colecția veche WorldPop/POP e depreciată; date modelate
- **Sursă:** https://developers.google.com/earth-engine/datasets/catalog/WorldPop_GP_100m_pop · încredere ridicată

### INS România – TEMPO-Online și RPL2021 ★★★☆☆
- **Link:** https://www.recensamantromania.ro
- **Ce oferă:** Populația rezidentă și după domiciliu pe localități (municipiu/oraș/comună); rezultate definitive RPL2021; serii TEMPO post-recensământ (de ex. 1 ian. 2023)
- **Acces:** Tabele web/export TEMPO-Online pe insse.ro (cod exact al tabelului neconfirmat); publicații județene PDF
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Anual (TEMPO); recensământ decenal · **Acoperire:** România, nivel UAT/localitate
- **Precauții:** Legați datele de geometrii prin codul SIRUTA
- **Sursă:** https://iasi.insse.ro/wp-content/uploads/2024/05/Anuar-Iasi-2023-INS.pdf · încredere medie

### uMap ★★★☆☆
- **Link:** https://umap.openstreetmap.fr
- **Ce oferă:** Hărți personalizate rapide peste OSM, cu straturi la distanță (GeoJSON, GeoRSS, GPX, KML, CSV, OSM) încărcate live sau din cache; integrare prin iframe
- **Acces:** Instanța publică umap.openstreetmap.fr sau self-host (de ex. YunoHost)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** Aplicație AGPL-3.0; licența datelor e aleasă per hartă (ODbL, WTFPL, Licence Ouverte etc.)
- **Actualizare:** Live din URL-uri remote (dacă au CORS sau trec prin proxy) · **Acoperire:** N/A
- **Precauții:** Hărțile publice sunt vizibile oricui: publicați doar date întârziate și agregate
- **Sursă:** https://thejeshgn.com/2024/08/14/creating-maps-using-umap · încredere medie

### Kepler.gl ★★★☆☆
- **Link:** https://kepler.gl
- **Ce oferă:** Analiză vizuală în browser a seturilor mari (puncte, arce, traiectorii, hexbin, animație în timp); potrivit pentru analiza istorică a incidentelor
- **Acces:** Aplicație web sau bibliotecă React/Jupyter
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** MIT (neverificat în sesiune)
- **Actualizare:** N/A (fișiere încărcate) · **Acoperire:** N/A
- **Precauții:** Exporturile HTML pot conține datele brute: verificați înainte de partajare
- **Sursă:** https://github.com/keplergl/kepler.gl · încredere medie

### FreeTAKServer (FTS) ★★★☆☆
- **Link:** https://github.com/FreeTAKTeam/FreeTAKServer
- **Ce oferă:** Server TAK în Python3: partajare geo, chat, fișiere, administrare web, federație, înregistrare CoT; rulează de la AWS până pe Android
- **Acces:** Self-hosted (pip/Docker)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** Eclipse Public License (EPL)
- **Actualizare:** Timp real · **Acoperire:** N/A
- **Precauții:** Starea dezvoltării e neclară în surse; suportul WinTAK depinde parțial de un plugin; unele pluginuri cer acces takmaps.com
- **Sursă:** https://github.com/FreeTAKTeam/FreeTAKServer · încredere medie

### n8n (Community Edition) ★★★☆☆
- **Link:** https://n8n.io
- **Ce oferă:** Automatizări cu sute de conectori (HTTP, Telegram, Signal prin API, baze de date)
- **Acces:** Self-hosted (Docker/npm) sau n8n Cloud (plătit)
- **Cost / autentificare:** Self-hosted gratuit pentru uz intern; Cloud plătit; SSO și proiecte partajate doar în planurile plătite
- **Licență / termeni:** Sustainable Use License (source-available, nu OSI): permis uzul intern și personal; interzisă găzduirea ca serviciu pentru clienți sau white-label
- **Actualizare:** Timp real · **Acoperire:** N/A
- **Precauții:** Verificați licența dacă ONG-ul oferă fluxurile altor organizații; nu expuneți instanța fără autentificare
- **Sursă:** https://docs.n8n.io/n8n-community-license/community-license/license-faq · încredere ridicată

### Home Assistant – integrarea Ukraine Alarm (+ Air Threat Monitor, HACS) ★★★☆☆
- **Link:** https://www.home-assistant.io/integrations/ukraine_alarm/
- **Ce oferă:** 6 senzori binari per regiune ucraineană (aer, artilerie, chimic, nuclear, lupte urbane, necunoscut), actualizați la 10 s prin siren.pp.ua (wrapper public peste Ukraine Alarm); integrarea custom Air Threat Monitor adaugă amenințări apropiate și radar
- **Acces:** Setări → Dispozitive și servicii → Adaugă integrare; Air Threat Monitor ca repository custom HACS
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** Home Assistant open source (licența exactă neverificată în sesiune)
- **Actualizare:** ~10 s · **Acoperire:** Regiuni din Ucraina (util pentru Odesa, Vinnîțea, Cernăuți)
- **Precauții:** Dependență de un wrapper terț (siren.pp.ua); nu redistribuiți public date de amenințare în timp real
- **Sursă:** https://www.home-assistant.io/integrations/ukraine_alarm/ · încredere ridicată

### Signal prin signal-cli (+ signal-cli-rest-api) ★★★☆☆
- **Link:** https://github.com/AsamK/signal-cli
- **Ce oferă:** Trimitere și primire mesaje Signal (E2E) de pe server: CLI, daemon JSON-RPC, D-Bus; wrapper REST disponibil
- **Acces:** Self-hosted (Java/binare native; Docker pentru wrapper-ul REST)
- **Cost / autentificare:** Gratuit; necesită un număr de telefon dedicat
- **Licență / termeni:** signal-cli: GPLv3; signal-cli-rest-api: neconfirmat
- **Actualizare:** Secunde · **Acoperire:** Global
- **Precauții:** Neoficial; trebuie actualizat regulat (clienții expiră după ~3 luni); risc de blocare a contului; numerele membrilor sunt date personale
- **Sursă:** https://git.cs.tu-dortmund.de/marvin.weiler/signal-cli-with-http-logging/raw/branch/master/README.md · încredere medie

### Gotify ★★★☆☆
- **Link:** https://gotify.net
- **Ce oferă:** Server push self-hosted cu API REST/WebSocket și aplicație Android
- **Acces:** Self-hosted (binar/Docker)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** MIT (neverificat în sesiune)
- **Actualizare:** Secunde · **Acoperire:** N/A
- **Precauții:** Client iOS oficial neconfirmat; potrivit ca redundanță internă
- **Sursă:** https://gotify.net · încredere medie

### GADM ★★☆☆☆
- **Link:** https://gadm.org
- **Ce oferă:** Limite administrative globale pe mai multe niveluri
- **Acces:** Descărcare (GPKG/SHP etc.)
- **Cost / autentificare:** Gratuit pentru uz academic/necomercial
- **Licență / termeni:** Uz necomercial; redistribuirea sau uzul comercial nu sunt permise fără acord prealabil
- **Actualizare:** Versiuni rare · **Acoperire:** Global
- **Precauții:** Evitați pentru un dashboard public sau redistribuit; preferați geoBoundaries gbOpen
- **Sursă:** https://www.naturalearthdata.com/?p=3348 · încredere medie

### SRTM GL1 (NASA/USGS LP DAAC) ★★☆☆☆
- **Link:** https://lpdaac.usgs.gov/products/srtmgl1v003/
- **Ce oferă:** Elevație ~30 m (1 arc-secundă), alternativă la GLO-30
- **Acces:** Descărcare prin NASA Earthdata (cont necesar)
- **Cost / autentificare:** Gratuit, cont Earthdata
- **Licență / termeni:** neverificat în sesiune (în general considerat fără restricții, date NASA)
- **Actualizare:** Static (2000) · **Acoperire:** Aproape global (60°N–56°S)
- **Precauții:** Mai vechi și cu goluri; preferați GLO-30
- **Sursă:** https://lpdaac.usgs.gov/products/srtmgl1v003/ · încredere medie

### ANCOM Netograf.ro ★★☆☆☆
- **Link:** https://www.netograf.ro
- **Ce oferă:** Măsurători de viteză internet fix și mobil; statistici semestriale și anuale pe operatori
- **Acces:** Web + aplicații Android/iOS/Windows; date deschise neconfirmate
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Statistici semestriale · **Acoperire:** România
- **Precauții:** Nu e hartă de acoperire radio; util doar pentru calitatea backhaul-ului
- **Sursă:** https://www.ancom.ro/en/about-us/media-en/press-releases/actual-speed-ensured-by-the-fixed-and-mobile-internet-providers-in-romania-available-on-netograf-ro/ · încredere medie

### ANRCETI / operatori mobili R. Moldova – acoperire ★★☆☆☆
- **Link:** https://en.anrceti.md
- **Ce oferă:** Informații de reglementare; cifre de acoperire agregate (ex. 4G ≈96,4% teritoriu / 99% populație într-un document de licență, operator neidentificat); hărți web ale operatorilor (Orange, Moldcell)
- **Acces:** Web; nicio hartă interactivă ANRCETI sau API găsită
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** neconfirmat · **Acoperire:** Republica Moldova (acoperire mai slabă lângă frontiere)
- **Precauții:** Cifrele depind de an și de operator; hărțile operatorilor sunt vizualizatoare proprietare, fără API (neverificat)
- **Sursă:** https://storage.mtender.gov.md/get/1fcda3b2-e0f1-405f-a898-7e57c7b6a4d3-1764086507998 · încredere scăzută

### CORINE Land Cover 2018 (Copernicus Land Monitoring Service) ★★☆☆☆
- **Link:** https://land.copernicus.eu/api/en/products/corine-land-cover/clc2018
- **Ce oferă:** Acoperirea și utilizarea terenului (44 clase), raster 100 m și vector; util pentru zone deschise, păduri, zgomot de fond, accesibilitate
- **Acces:** Descărcare CLMS (unele variante cer autentificare); Google Earth Engine COPERNICUS/CORINE/V20/100m
- **Cost / autentificare:** Gratuit (cont CLMS pentru unele descărcări)
- **Licență / termeni:** Politica de date deschise Copernicus (Reg. UE 1159/2013); unele cataloage indică CC BY 4.0
- **Actualizare:** Ciclu de 6 ani · **Acoperire:** România da; Moldova și Ucraina neconfirmat (probabil neacoperite)
- **Precauții:** Pentru MD/UA aveți nevoie de un produs global alternativ (neverificat în sesiune)
- **Sursă:** https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_CORINE_V20_100m?authuser=1 · încredere medie

### EU-DEM v1.1 (Copernicus Land) ★☆☆☆☆
- **Link:** https://land.copernicus.eu
- **Ce oferă:** DEM european ~25 m
- **Acces:** neconfirmat (disponibilitatea curentă pe portalul CLMS nu a putut fi confirmată)
- **Cost / autentificare:** neconfirmat
- **Licență / termeni:** neconfirmat
- **Actualizare:** Static · **Acoperire:** Europa (EEA39; MD/UA neconfirmat)
- **Precauții:** Starea produsului e neconfirmată; folosiți Copernicus DEM GLO-30
- **Sursă:** https://land.copernicus.eu/api/en/products/corine-land-cover/clc2018 · încredere scăzută

### BeaconDB ★☆☆☆☆
- **Link:** https://beacondb.net
- **Ce oferă:** Bază de geolocalizare WiFi/celule, înlocuitor comunitar pentru Mozilla Location Service
- **Acces:** API compatibil MLS/Ichnaea; dump-urile publice nu sunt încă gata
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** Dump-uri anunțate ca domeniu public (încă nepublicate)
- **Actualizare:** Continuu · **Acoperire:** Global, densitate scăzută
- **Precauții:** Experimental; unele date încă neobfuscate; relevanță mică pentru detecție
- **Sursă:** https://libre_geolocation.codeberg.page/ · încredere medie

## Meteo, sateliți, internet, știri, seturi de date despre conflict

### Open-Meteo Forecast API (inclusiv niveluri de presiune) ★★★★☆ ✔
- **Link:** https://open-meteo.com/
- **Ce oferă:** Prognoze orare: vânt la suprafață și pe niveluri de presiune (ex. 850/700 hPa), nebulozitate, vizibilitate, precipitații. Context pentru zborul dronelor și pentru observare.
- **Acces:** REST GET api.open-meteo.com/v1/forecast, fără cheie, pentru uz necomercial. Abonații folosesc customer-api.open-meteo.com, cu cheie.
- **Cost / autentificare:** Gratuit pentru uz necomercial: sub 10.000 de apeluri/zi, 5.000/oră și 600/minut. Abonament plătit pentru uz comercial (fără limită zilnică; preț pe pagina de pricing).
- **Licență / termeni:** CC BY 4.0, cu atribuire obligatorie. „Necomercial” înseamnă site-uri sau aplicații private ori non-profit, fără abonamente sau reclame.
- **Actualizare:** La fiecare rulare de model (exact: neconfirmat) · **Acoperire:** Global
- **Precauții:** Planul gratuit nu are garanție de uptime, iar IP-urile care abuzează pot fi blocate fără avertisment. Păstrați rezultatele în cache.
- **Sursă:** https://open-meteo.com/en/terms · încredere ridicată

### GDELT DOC 2.0 API ★★★★☆
- **Link:** https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- **Ce oferă:** Căutare full-text multilingvă în știrile monitorizate de GDELT; liste de articole (ArtList), timeline-uri de volum și ton, imagini
- **Acces:** REST GET https://api.gdeltproject.org/api/v2/doc/doc?query=...&mode=ArtList&format=json; max. 250 de înregistrări; parametrii timespan și operatorii sourcecountry/sourcelang – verificați în documentație
- **Cost / autentificare:** Gratuit, fără autentificare
- **Licență / termeni:** Neconfirmat în sesiune (GDELT declară public că datele sunt deschise, cu citare)
- **Actualizare:** Ciclu GDELT 2.0 de 15 min (confirmat direct pentru GEO, indirect pentru DOC); fereastră de ~3 luni · **Acoperire:** Global, multilingv (inclusiv presa RO/MD/UA)
- **Precauții:** Semnal de știri cu întârziere (minute–zeci de minute) și zgomot; deduplicați. Nu e avertizare; folosiți-l pentru confirmarea comunicatelor oficiale.
- **Sursă:** https://jentic.com/apis/api.gdeltproject.org/gdelt · încredere medie

### Google News RSS (căutare) ★★★★☆
- **Link:** https://news.google.com/
- **Ce oferă:** Flux RSS de articole pentru interogări (ex. 'dronă Iași', 'spațiul aerian Galați', 'Ungheni dronă')
- **Acces:** GET https://news.google.com/rss/search?q=<interogare>+when:1h&hl=ro&gl=RO&ceid=RO:ro; operatorul when: în q; localizarea MD (ceid=MD:ro) neconfirmată
- **Cost / autentificare:** Gratuit, fără cheie
- **Licență / termeni:** Nedocumentat oficial; supus ToS Google; conținutul aparține editorilor
- **Actualizare:** Minute–zeci de minute (neconfirmat) · **Acoperire:** Presa indexată de Google News pentru RO/MD
- **Precauții:** Parametri nedocumentați, se pot schimba. Fără parametrii de localizare, fluxul poate fi gol. Interogați rar și cu cache. Linkurile sunt redirecționări codificate. Doar titluri și linkuri, fără republicarea conținutului.
- **Sursă:** https://newscatcherapi.com/blog/google-news-rss-search-parameters-the-missing-documentaiton · încredere medie

### Wikipedia – 'Violations of non-combatant airspace during the Russo-Ukrainian war (2022–present)' ★★★★☆
- **Link:** https://en.wikipedia.org/wiki/Violations_of_non-combatant_airspace_during_the_Russo-Ukrainian_war_(2022%E2%80%93present)
- **Ce oferă:** Tabel de incidente (date, locuri, tip de aparat) pentru România, Moldova, Polonia etc.; România are cel puțin 70 de violări din 2023
- **Acces:** Web; MediaWiki API (action=parse) sau dump-uri pentru extragerea tabelelor
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** Text CC BY-SA 4.0 (atribuire și share-alike)
- **Actualizare:** Ore–zile (editări comunitare) · **Acoperire:** Țările vecine Ucrainei, 2022–prezent
- **Precauții:** Fiecare rând trebuie verificat cu MApN și cu MApN Moldova (army.md). Datele pot conține erori sau vandalism. Respectați share-alike dacă redistribuiți.
- **Sursă:** https://en.wikipedia.org/wiki/Violations_of_non-combatant_airspace_during_the_Russo-Ukrainian_war_(2022%E2%80%93present) · încredere ridicată

### ANM – Administrația Națională de Meteorologie (radar și avertizări) ★★★☆☆
- **Link:** https://www.meteoromania.ro/
- **Ce oferă:** Imagini radar meteo, avertizări cu cod de culoare, prognoze pentru România
- **Acces:** Web (imagini radar suprapuse); server raportat de utilizatori opendata.meteoromania.ro/radar/ (format și termeni neconfirmați); API oficial pentru avertizări neconfirmat
- **Cost / autentificare:** Neconfirmat (date istorice ANM livrate tradițional prin contract)
- **Licență / termeni:** Neconfirmat; în 2015, ANM oferea date doar prin contract, cu drepturi de autor asupra datelor istorice
- **Actualizare:** Radar ~4–5 min pe serverul opendata (raportat), ~15 min pe sursa veche · **Acoperire:** România (radarele acoperă și o parte din R. Moldova – neconfirmat)
- **Precauții:** Folosiți radarul STRICT ca strat meteo (ploaie/furtună → alarme false acustice). Nu îl prezentați ca detecție de drone. Postarea despre opendata a fost ștearsă, deci verificați direct; respectați drepturile ANM.
- **Sursă:** https://community.windy.com/topic/39217/open-romanian-radar-data · încredere scăzută

### MeteoAlarm (EUMETNET) – pistă neverificată ★★★☆☆ ✔
- **Link:** https://meteoalarm.org/
- **Ce oferă:** Avertizări meteo oficiale (pentru România, emise de ANM), în format CAP/Atom
- **Acces:** Registrul WMO al autorităților de alertare listează pentru ANM feed-ul CAP http://meteoalarm.eu/ATOM/RO.xml (pe hostul vechi). Hostul nou folosește tiparul https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-<țară> (ex. united-kingdom); varianta pentru „romania” e neconfirmată. Feed pentru R. Moldova: neconfirmat (SHS a adoptat abordarea MeteoAlarm în 2015).
- **Cost / autentificare:** Gratuit (neconfirmat)
- **Licență / termeni:** neconfirmat
- **Actualizare:** La emiterea avertizărilor (neconfirmat) · **Acoperire:** România (R. Moldova: neconfirmat)
- **Precauții:** feeds.meteoalarm.org nu a fost accesibil din sesiune: testați URL-ul înainte de integrare. Sursa oferă doar context meteo.
- **Sursă:** https://alertingauthority.wmo.int/authorities.php?recId=135 · încredere medie

### University of Wyoming – sondaje aerologice (upper air) ★★★☆☆
- **Link:** https://weather.uwyo.edu/upperair/sounding.html
- **Ce oferă:** Profile verticale text (PRES, HGHT, TEMP, DWPT, RELH, DRCT, SKNT etc.) de la stațiile de radiosondaj; permit identificarea inversiunilor termice și a vântului pe verticală
- **Acces:** Web, formular cu ieșire 'Text: List' parsabilă (biblioteci ca SkewT); ID-urile stațiilor din regiune (București, Chișinău etc.) – neconfirmat, alegeți-le din hartă
- **Cost / autentificare:** Gratuit (fără înregistrare, conform utilizării comune) – neconfirmat
- **Licență / termeni:** Neconfirmat
- **Actualizare:** Radiosondaje de regulă la 00/12 UTC, publicate la câteva ore după lansare – neconfirmat · **Acoperire:** Rețea globală de radiosondaj; stațiile din apropierea Iașului sunt rare
- **Precauții:** Pentru calibrarea senzorilor acustici: inversiunile nocturne pot amplifica sau ghida sunetul (raze de detecție variabile). Interfața poate fi schimbată, ceea ce strică parserele. Ca alternativă de model: temperaturile pe niveluri de presiune din Open-Meteo.
- **Sursă:** https://www.meted.ucar.edu/mesoprim/skewtd3/upload_instructions.htm · încredere medie

### NASA FIRMS – Area API (VIIRS NRT active fire) ★★★☆☆ ✔
- **Link:** https://firms.modaps.eosdis.nasa.gov/api/area/
- **Ce oferă:** Detecții de anomalii termice și incendii (VIIRS, MODIS). Context post-impact: incendii la depozite sau la infrastructură.
- **Acces:** REST CSV: /api/area/csv/[MAP_KEY]/[SOURCE]/[west,south,east,north sau world]/[DAY_RANGE 1–5]/[DATE opțional]. Endpoint de status pentru MAP_KEY (transaction_limit, current_transactions). Există și WMS/WFS. Exemplu de bbox: 26,44,32,49.
- **Cost / autentificare:** MAP_KEY gratuit. Limită: 5.000 de tranzacții la 10 minute (cererile mari contează ca mai multe). Limita se poate mări la cerere.
- **Licență / termeni:** Date NASA deschise; termenii exacți: neconfirmat
- **Actualizare:** NRT, ~3 h după trecerea satelitului · **Acoperire:** Global
- **Precauții:** Nu detectează drone. Are fals pozitive (arderi agricole, industrie). Nu publicați aproape în timp real locuri de impact din Ucraina.
- **Sursă:** https://firms.modaps.eosdis.nasa.gov/api/area/ · încredere ridicată

### IODA – Internet Outage Detection and Analysis (Georgia Tech) ★★★☆☆ ✔
- **Link:** https://ioda.inetintel.cc.gatech.edu/
- **Ce oferă:** Semnale de conectivitate (BGP, active probing, telescop) și alerte sau evenimente de întrerupere, pe țară, regiune și ASN
- **Acces:** API v2 la https://api.ioda.inetintel.cc.gatech.edu/v2/ (ex. /v2/outages/alerts, /v2/signals/raw/country/{cod}), conform proiectelor terțe. Specificația (posibil pentru v1) e în wiki-ul CAIDA/ioda-api.
- **Cost / autentificare:** Fără cheie (conform proiectelor terțe). Limita de rată: neconfirmat.
- **Licență / termeni:** neconfirmat
- **Actualizare:** Aproape timp real (neconfirmat) · **Acoperire:** Global
- **Precauții:** Semnal indirect. Testați căile v2 înainte de producție; fereastra maximă pe cerere e de 31 de zile (conform unui wrapper).
- **Sursă:** https://github.com/CAIDA/ioda-api/wiki/API-Specification · încredere medie

### Cloudflare Radar API (traffic anomalies / outages) ★★★☆☆ ✔
- **Link:** https://radar.cloudflare.com/
- **Ce oferă:** Anomalii de trafic internet și adnotări despre întreruperi, pe țară și ASN
- **Acces:** REST https://api.cloudflare.com/client/v4/radar/... (ex. traffic_anomalies), cu header-ul Authorization: Bearer <token>
- **Cost / autentificare:** Gratuit. Necesită cont Cloudflare și un Custom Token cu permisiunea Account > Radar > Read.
- **Licență / termeni:** Datele din API și descărcările: CC BY-NC 4.0 (necomercial). Graficele încorporabile: CC BY 4.0.
- **Actualizare:** neconfirmat. Anomaliile acoperă ultimele 7 zile, adnotările până la 364 de zile (conform catalogului). · **Acoperire:** Global
- **Precauții:** Clauza NC: un ONG trebuie să verifice că proiectul nu are componentă comercială. E un semnal indirect (pene de curent sau de internet după atacuri), nu o avertizare.
- **Sursă:** https://developers.cloudflare.com/radar/get-started/first-request/ · încredere ridicată

### GDELT GEO 2.0 API ★★★☆☆
- **Link:** https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/
- **Ce oferă:** Hartă/GeoJSON a locațiilor menționate în știri pentru un cuvânt-cheie, pe ultimele 7 zile
- **Acces:** REST (api.gdeltproject.org/api/v2/geo/geo) – parametrii și formatele se verifică în documentația din blog
- **Cost / autentificare:** Gratuit, fără autentificare
- **Licență / termeni:** Neconfirmat (date GDELT deschise, cu citare)
- **Actualizare:** La 15 min (conform anunțului oficial) · **Acoperire:** Global; fereastră de 7 zile
- **Precauții:** Documentația are ~9 ani; verificați că endpoint-ul mai funcționează. Geocodarea automată greșește frecvent (ex. Ungheni MD vs. Ungheni RO).
- **Sursă:** https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/ · încredere medie

### ACLED – Armed Conflict Location & Event Data ★★★☆☆
- **Link:** https://acleddata.com/api-documentation/getting-started
- **Ce oferă:** Evenimente de conflict georeferențiate (lovituri aeriene/drone, explozii, proteste) pentru Ucraina, Moldova, România
- **Acces:** API REST cu autentificare OAuth pentru scripturi (cookie pentru browser); cont myACLED
- **Cost / autentificare:** Nivelul implicit 'Open' NU are acces API; Research/Partner/Enterprise da. Email instituțional recomandat (domeniile generice nu mai primesc acces extins, conform raportărilor), cerere la access@acleddata.com
- **Licență / termeni:** EULA ACLED (restricții de redistribuire, atribuire obligatorie)
- **Actualizare:** Neconfirmat în sesiune (actualizări periodice, de regulă săptămânale) · **Acoperire:** Global, inclusiv UA/MD/RO
- **Precauții:** Pentru tipare istorice (ex. sudul Odesei, Izmail/Reni), nu pentru alertare. Respectați EULA. Fără acces Research, API-ul întoarce 403.
- **Sursă:** https://acleddata.com/myacled-faqs · încredere medie

### Liveuamap ★★★☆☆
- **Link:** https://liveuamap.com/
- **Ce oferă:** Hartă live cu evenimente geolocalizate (atacuri, drone, explozii) din surse deschise
- **Acces:** Web; API comercial (pagina promo/api)
- **Cost / autentificare:** Pro ~150 $/lună (200 cereri/zi), Enterprise de la ~1.000 $/lună (1.500 cereri/zi) – din pagina unui competitor, NECONFIRMAT; există un nivel gratuit de vizualizare
- **Licență / termeni:** Neconfirmat
- **Actualizare:** Minute (live) – neconfirmat · **Acoperire:** Ucraina, Moldova, regiunea Mării Negre
- **Precauții:** OPSEC: unele intrări descriu în timp real mișcări de drone sau poziții de apărare antiaeriană; nu le republicați automat. Verificați ToS înainte de orice reutilizare.
- **Sursă:** https://www.worldmonitor.app/compare/worldmonitor-vs-liveuamap/ · încredere scăzută

### ISIS (Institute for Science and International Security) – analize lunare Shahed ★★★☆☆
- **Link:** https://isis-online.org/isis-reports/monthly-analysis-of-russian-shahed-136-deployment-against-ukraine
- **Ce oferă:** Estimări lunare ale lansărilor Shahed/Geran (inclusiv momeli), ponderi ale variantelor cu reacție, rate de impact (aug. 2025 – iun. 2026)
- **Acces:** Rapoarte PDF; extragere manuală sau semi-automată a tabelelor
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** Neconfirmat (citați sursa)
- **Actualizare:** Lunar, cu întârziere de câteva săptămâni · **Acoperire:** Ucraina (agregat național)
- **Precauții:** Cifrele diferă între surse (cu sau fără momeli). Folosiți-le pentru modelarea volumului de risc, nu pentru alertare.
- **Sursă:** https://isis-online.org/uploads/isis-reports/documents/June-2026-Updated-Analysis-of-Russian-Shahed-type-UAVs-Deployment-Against-Ukraine-up-to-July-6J-Additional-Expert-View.pdf · încredere medie

### Serviciul Hidrometeorologic de Stat (R. Moldova) ★★☆☆☆
- **Link:** http://www.meteo.md/
- **Ce oferă:** Prognoze 24 h și 2–7 zile, avertizări cu coduri de culoare (abordare de tip MeteoAlarm adoptată în 2015)
- **Acces:** Web; nu s-a găsit niciun API sau feed (domeniul meteo.gov.md este neconfirmat)
- **Cost / autentificare:** Neconfirmat
- **Licență / termeni:** Neconfirmat
- **Actualizare:** Neconfirmat · **Acoperire:** Republica Moldova
- **Precauții:** Fără feed automat cunoscut; scraping doar cu respectarea termenilor. Context meteo pentru coridorul Ungheni/nordul Moldovei.
- **Sursă:** https://cis2.eea.europa.eu/provider/589/ · încredere scăzută

### Windy (hartă + Point/Map Forecast API) ★★☆☆☆
- **Link:** https://api.windy.com/
- **Ce oferă:** Hartă interactivă cu vânt, nori, precipitații pe straturi și modele; Point Forecast API pentru puncte
- **Acces:** Web (hartă); API REST (Point Forecast, documentat la api.windy.com/point-forecast/docs); Map Forecast API pentru încorporare
- **Cost / autentificare:** Cheia trial întoarce DATE RANDOMIZATE (doar pentru test); planul Professional ar costa ~990 € (raportat de utilizatori, neconfirmat)
- **Licență / termeni:** Neconfirmat (termenii Windy API); ECMWF inclus sau nu – informații contradictorii
- **Actualizare:** Point API la intervale de 3 h (conform staff) · **Acoperire:** Global
- **Precauții:** Nu integrați cheia trial în producție (date false intenționat). Pentru ONG, Open-Meteo e de preferat; Windy rămâne doar pentru vizualizare manuală.
- **Sursă:** https://community.windy.com/topic/23138/trial-api-data-randomly-shuffled · încredere medie

### Blitzortung.org (rețea comunitară de detecție a fulgerelor) ★★☆☆☆
- **Link:** https://www.blitzortung.org/
- **Ce oferă:** Hartă în timp real a descărcărilor electrice; util ca filtru pentru alarmele false acustice (tunete)
- **Acces:** Doar hartă web publică; NU există API public; accesul la date brute e permis doar operatorilor de stații înregistrate
- **Cost / autentificare:** Gratuit pentru operatori de stație (cer construirea și operarea unei stații)
- **Licență / termeni:** Uz necomercial, fără vânzarea datelor; declarații contradictorii pe forum despre CC BY-SA 4.0 – neconfirmat oficial
- **Actualizare:** Aproape real-time (secunde–minute) pe hartă – neconfirmat · **Acoperire:** Europa bine acoperită (densitatea stațiilor în RO/MD neconfirmată)
- **Precauții:** Nu faceți scraping pe serverele Blitzortung (interzis explicit). Rețea experimentală/hobby, nevalidată. Pentru integrare automată: stație proprie sau furnizor comercial.
- **Sursă:** https://forum.blitzortung.org/showthread.php?pid=12520 · încredere medie

### Copernicus Data Space Ecosystem / Sentinel Hub ★★☆☆☆
- **Link:** https://dataspace.copernicus.eu/
- **Ce oferă:** Imagini Sentinel-1 (SAR, independent de nori) și Sentinel-2 (optic 10 m), API-uri Process/Catalog, openEO
- **Acces:** Cont gratuit; API Sentinel Hub (OGC/Process), openEO, S3; calculator PU disponibil
- **Cost / autentificare:** Gratuit, cu cotă lunară (~10.000 PU și 10.000 cereri/lună – sursă secundară); ~300 PU/min; cota se resetează lunar; volumele mari prin CREODIAS (plătit)
- **Licență / termeni:** Datele Copernicus Sentinel sunt libere și deschise, cu atribuire ('Contains modified Copernicus Sentinel data') – detalii în politica oficială
- **Actualizare:** Ore–zile de la achiziție; revizitare de câteva zile · **Acoperire:** Global (RO/MD/UA complet)
- **Precauții:** Nu e timp real. Util pentru verificarea locului unui impact sau al unei prăbușiri (ex. Galați/Tulcea) după zile. Nu publicați analize de daune la infrastructura ucraineană.
- **Sursă:** https://dataspace.copernicus.eu/node/561 · încredere medie

### EUMETSAT Data Store / EUMETView ★★☆☆☆
- **Link:** https://www.eumetsat.int/
- **Ce oferă:** Imagini Meteosat SEVIRI (nori, ceață, convecție), produse derivate; vizualizare EUMETView cu servicii OGC WMS/WCS/WFS (în funcție de produs)
- **Acces:** EUMETView: navigare fără cont (descărcarea necesită login); Data Store: cont gratuit și acceptarea licenței per produs
- **Cost / autentificare:** Gratuit (înregistrare)
- **Licență / termeni:** Mixt: unele date CC BY 4.0; 'Recommended Data' sub licență EUMETSAT (politica de date 2026)
- **Actualizare:** NRT de regulă sub 1 h (sursă secundară) · **Acoperire:** Disc complet Europa/Africa; include RO/MD/UA
- **Precauții:** Doar context (nebulozitate/ceață pentru observatori vizuali și senzori optici). Verificați licența fiecărui produs înainte de redistribuire.
- **Sursă:** https://www-cdn.eumetsat.int/files/2026-01/45173%20-%20Data_Policy.pdf · încredere medie

### NASA Black Marble (VNP46A1/VNP46A2, NRT) ★★☆☆☆
- **Link:** https://www.earthdata.nasa.gov/data/projects/black-marble
- **Ce oferă:** Radianță nocturnă zilnică și lumini nocturne corectate pentru Lună – detectarea panelor de curent după loviturile asupra rețelei
- **Acces:** LAADS DAAC / LANCE (HDF5), pachete R/Python (blackmarbler); cont NASA Earthdata (gratuit)
- **Cost / autentificare:** Gratuit (cont Earthdata)
- **Licență / termeni:** Date NASA deschise – termeni exacți neconfirmați
- **Actualizare:** Contradictoriu: NRT în ~3 h (NASA) vs. ~1 săptămână (pachetul R) · **Acoperire:** Global, 500 m
- **Precauții:** Norii, Luna și zăpada afectează semnalul. O pagină NASA afișa un aviz de nefinanțare (verificați actualitatea). OPSEC: prezentați datele pentru Ucraina doar agregat și cu întârziere.
- **Sursă:** https://www.earthdata.nasa.gov/s3fs-public/2025-05/BlackMarbleUserGuide_Collection2.0.pdf · încredere medie

### Ukrenergo + operatori regionali (oblenergo) – anunțuri de întreruperi ★★☆☆☆
- **Link:** https://ua.energy/
- **Ce oferă:** Anunțuri despre întreruperi de urgență și programate pe regiuni, cauzate de lovituri asupra rețelei; orare după adresă pe site-urile oblenergo
- **Acces:** Telegram (canalul oficial Ukrenergo – handle neconfirmat), Facebook, site-uri; NU există API public cunoscut
- **Cost / autentificare:** Gratuit (canale publice)
- **Licență / termeni:** Neconfirmat
- **Actualizare:** Minute–ore după evenimente · **Acoperire:** Ucraina (inclusiv Odesa, Vinnytsia, Chernivtsi)
- **Precauții:** Context după fapt; nu republicați detalii despre obiectivele lovite. Scraping-ul Telegram trebuie să respecte ToS.
- **Sursă:** https://en.interfax.com.ua/news/general/1157101.html · încredere medie

### Media Cloud (Search API + Directory) ★★☆☆☆
- **Link:** https://www.mediacloud.org/
- **Ce oferă:** Arhivă de peste 200 mil. articole, director de peste 60.000 de surse, colecții pe țări; analiză de acoperire mediatică
- **Acces:** Search API (client Python open-source 'api-client' pe GitHub); Directory pentru selectarea surselor RO/MD
- **Cost / autentificare:** Cont necesar – costul neconfirmat (proiect academic/non-profit)
- **Licență / termeni:** Neconfirmat
- **Actualizare:** Neconfirmat (ingestie continuă) · **Acoperire:** Peste 100 de țări (colecțiile RO/MD neconfirmate)
- **Precauții:** Pentru analiză istorică și de narative, nu pentru timp real. Verificați colecțiile RO/MD (support@mediacloud.org).
- **Sursă:** https://www.mediacloud.org/documentation/search-api-guide · încredere medie

### Event Registry / NewsAPI.ai ★★☆☆☆
- **Link:** https://newsapi.ai/plans
- **Ce oferă:** Articole și evenimente grupate multilingv, entități, concepte
- **Acces:** REST/SDK cu cheie API
- **Cost / autentificare:** Nivel gratuit ~2.000 de căutări; planuri plătite de la ~90 $/lună (agregator terț) – neconfirmat
- **Licență / termeni:** Neconfirmat
- **Actualizare:** Neconfirmat · **Acoperire:** Global multilingv (româna neconfirmată)
- **Precauții:** Prețuri neconfirmate oficial. Util doar dacă e nevoie de grupare automată a evenimentelor.
- **Sursă:** https://www.xpay.sh/saas-pricing/event-registry/ · încredere scăzută

### UCDP – Uppsala Conflict Data Program (GED și GED Candidate) ★★☆☆☆
- **Link:** https://ucdp.uu.se/apidocs/
- **Ce oferă:** Evenimente letale georeferențiate; GED Candidate lunar (preliminar)
- **Acces:** API ucdpapi.pcr.uu.se cu header x-ucdp-access-token; descărcări CSV de pe ucdp.uu.se/downloads fără înregistrare
- **Cost / autentificare:** Tokenul se cere pe email (răspuns în 3–5 zile lucrătoare); descărcările sunt gratuite
- **Licență / termeni:** Neconfirmat
- **Actualizare:** GED Candidate lunar, cu ~1 lună întârziere; GED anual, cu ~7 luni întârziere · **Acoperire:** Global (doar evenimente cu victime)
- **Precauții:** Doar evenimente letale; incursiunile de drone în RO/MD lipsesc de obicei. Folosiți-l pentru context.
- **Sursă:** https://ucdp.uu.se/downloads/ged/ged251.pdf · încredere medie

### CSIS Missile Threat ★★☆☆☆
- **Link:** https://missilethreat.csis.org/
- **Ce oferă:** Profile tehnice ale rachetelor și dronelor (rază, viteză, sarcină) – referință pentru clasificarea amenințărilor
- **Acces:** Web; nu s-a găsit un tracker de lansări sau un feed
- **Cost / autentificare:** Gratuit (vizualizare)
- **Licență / termeni:** Neconfirmat
- **Actualizare:** Neregulat · **Acoperire:** Global
- **Precauții:** Neverificat în sesiune; nu e un flux de date.
- **Sursă:** https://missilethreat.csis.org/ · încredere scăzută

### NewsAPI.org ★☆☆☆☆
- **Link:** https://newsapi.org/pricing
- **Ce oferă:** API de căutare articole/titluri din mii de surse
- **Acces:** REST cu cheie API
- **Cost / autentificare:** Planul Developer gratuit DOAR pentru dezvoltare (interzis în staging/producție), ~100 cereri/zi și articole cu întârziere de 24 h (sursă terță); Business ~449 $/lună (sursă terță)
- **Licență / termeni:** Conform ToS NewsAPI.org; planul gratuit nu se poate folosi în producție
- **Actualizare:** 24 h pe planul gratuit (sursă terță); real-time pe planurile plătite – neconfirmat · **Acoperire:** Global (acoperirea RO/MD neconfirmată)
- **Precauții:** Raport cost/beneficiu slab pentru ONG; GDELT și Google News RSS acoperă nevoia gratuit.
- **Sursă:** https://newsapi.org/pricing · încredere medie

### ISW – hartă interactivă a invaziei Rusiei în Ucraina ★☆☆☆☆
- **Link:** https://understandingwar.org/
- **Ce oferă:** Hărți ale liniei frontului și ale controlului teritorial, evaluări zilnice
- **Acces:** Web (viewer interactiv); nu s-a găsit un feed sau API documentat
- **Cost / autentificare:** Gratuit (vizualizare)
- **Licență / termeni:** Neconfirmat
- **Actualizare:** Zilnic – neconfirmat · **Acoperire:** Ucraina (front terestru)
- **Precauții:** Nu acoperă amenințarea aeriană spre RO/MD. Neverificat în sesiune; folosiți doar ca context general.
- **Sursă:** https://understandingwar.org/ · încredere scăzută

## Adăugate la verificarea finală

### adsb.fi – Open Data API ★★★★☆ ✔
- **Link:** https://adsb.fi
- **Ce oferă:** Poziții ADS-B/MLAT live în format compatibil cu ADSBexchange v2. Căutare după hex/ICAO, indicativ, înmatriculare și squawk. Endpoint /v2/mil (aeronave marcate militare). Căutarea pe zonă v2 lat/lon/dist e depreciată; README-ul cere v3 pentru integrări noi.
- **Acces:** REST JSON la opendata.adsb.fi/api (v2/v3), conform README-ului oficial github.com/adsbfi/opendata. Endpoint /v2/snapshot doar pentru feederi (deblocat după IP). Calea exactă v3 pentru zonă: vezi README.
- **Cost / autentificare:** Gratuit, fără cheie. Limită ~1 cerere/s, raportată de terți (README-ul nu precizează).
- **Licență / termeni:** Doar uz personal, necomercial. Datele nu pot fi licențiate, vândute, închiriate sau date în leasing. Citarea adsb.fi cu link spre pagina principală e obligatorie. Fără garanție; accesul poate fi suspendat.
- **Actualizare:** Secunde (live); snapshot pentru feederi la 30 s (sursă terță) · **Acoperire:** Global, depinde de feederi. Acoperirea RO-NE/MD/UA-S e neconfirmată și se poate îmbunătăți cu un receptor propriu.
- **Precauții:** Nu folosiți /v2/mil și nu afișați aeronave militare (F-16 ridicate de la sol, AWACS, avioane de realimentare): risc OPSEC. Filtrați după indicatorul militar. Dronele Shahed nu emit ADS-B, deci sursa servește doar ca indicator indirect (trafic civil oprit, diversiuni). Statutul de uz necomercial pentru un ONG trebuie clarificat.
- **Sursă:** https://github.com/adsbfi/opendata/blob/main/README.md · încredere ridicată

### EUROCONTROL NOP – Public Portal (Network Operations Portal) ★★★★☆ ✔
- **Link:** https://www.eurocontrol.int/portal/network-operations-portal
- **Ce oferă:** Situația curentă a rețelei: Headline News despre evenimente ATFCM cu impact semnificativ (actualizate în timp real de personalul NM), hartă cu închideri de spațiu aerian și zone congestionate, întârzieri, reglementări ATFM.
- **Acces:** Web public (Public NOP), accesibil oricui. NOP-ul protejat e rezervat organizațiilor implicate operațional (ATFM, companii aeriene, aeroporturi). Feed/API public: neconfirmat.
- **Cost / autentificare:** Gratuit, fără cont (versiunea publică)
- **Licență / termeni:** neconfirmat (termenii EUROCONTROL)
- **Actualizare:** Aproape timp real (Headline News actualizate de NM) · **Acoperire:** Zona EUROCONTROL, inclusiv FIR București. Afișarea FIR Chișinău (LUUU): neconfirmată.
- **Precauții:** Arată efectele (închideri, reglementări), nu cauza, și nu indică drone. Nu automatizați scraping-ul fără acord; folosiți-l ca link sau pentru verificare manuală.
- **Sursă:** https://www.eurocontrol.int/portal/network-operations-portal · încredere ridicată

### Izmail RDA/RVA – canal Telegram (t.me/IzmailRDA) ★★★★☆ ✔
- **Link:** https://t.me/IzmailRDA
- **Ce oferă:** Anunțuri oficiale ale raionului Izmail (Dunărea de Jos, în fața Galațiului și Tulcei): alerte, consecințele atacurilor, recomandări pentru populație.
- **Acces:** Telegram; preview web t.me/s/IzmailRDA (de verificat). Link „Телеграм РДА” pe site-ul izmail-rda.od.gov.ua. Ingestie prin RSSHub/Telethon.
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Minute–ore · **Acoperire:** Raionul Izmail (Izmail, Reni, Kiliia – Delta Dunării)
- **Precauții:** Handle-ul provine de pe site-ul RDA, dintr-o postare din 2024. Un articol din 29.10.2026 trimite la alt canal, printr-un link de invitație, așa că verificați pe izmail-rda.od.gov.ua. Nu republicați locurile de impact înaintea comunicării oficiale (art. 114-2 CP UA).
- **Sursă:** https://izmail-rda.od.gov.ua/ · încredere medie

### RSSHub – rută Telegram → RSS ★★★★☆ ✔
- **Link:** https://docs.rsshub.app
- **Ce oferă:** Convertește canalele Telegram publice (kpszsu, air_alert_ua, odeskaODA etc.) în fluxuri RSS ușor de consumat din Node-RED, n8n sau Grafana.
- **Acces:** Rută /telegram/channel/:username/:routeParams?, pe instanța publică rsshub.app sau pe o instanță găzduită propriu (Docker). Opțiuni: showLinkPreview, includeFwd, includeReply, includeServiceMsg. Cu TELEGRAM_SESSION configurat folosește MTProto; altfel face scraping pe preview-ul public.
- **Cost / autentificare:** Gratuit, găzduit propriu. Limitele instanței publice: neconfirmat.
- **Licență / termeni:** Licența software: neconfirmat (proiect open-source). Conținutul aparține canalelor; respectați termenii Telegram.
- **Actualizare:** Depinde de cache-ul instanței (configurabil la găzduire proprie) · **Acoperire:** Orice canal Telegram public
- **Precauții:** Pentru alerte folosiți o instanță proprie, nu instanța publică partajată (poate întârzia sau bloca). Canalele își pot dezactiva preview-ul web. Nu republicați integral conținutul.
- **Sursă:** https://docs.rsshub.app/guide · încredere medie

### GPSJam.org – hartă a interferențelor GNSS ★★★☆☆ ✔
- **Link:** https://gpsjam.org
- **Ce oferă:** Hartă zilnică (agregare pe 24 h, hexagoane) a interferențelor GNSS probabile, calculată din valorile NIC (Navigation Integrity Category) raportate de aeronave prin ADS-B. Navigare pe zile anterioare.
- **Acces:** Web (hartă). Export/API: neconfirmat.
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat (datele de bază provin de la ADS-B Exchange)
- **Actualizare:** Zilnic (agregare pe 24 h) · **Acoperire:** Global, doar unde există trafic ADS-B. Spațiul aerian al UA (și periodic al MD) nu are trafic civil, deci datele de acolo sunt rare.
- **Precauții:** Este un proxy (NIC), nu o măsurare directă. Aeronavele „văd” bruiajul de la distanțe mari, așa că o zonă roșie nu înseamnă neapărat efect la sol. Există fals pozitive (teste sau exerciții militare). Folosiți doar ca strat de context, nu pentru avertizare.
- **Sursă:** https://gpsjam.org/about · încredere medie

### OpenAIP – date aeronautice deschise (spațiu aerian) ★★★☆☆ ✔
- **Link:** https://www.openaip.net
- **Ce oferă:** Date aeronautice comunitare: poligoane de spațiu aerian (CTR, TMA, zone restricționate/periculoase), aeroporturi, mijloace de navigație. Strat de context pentru hartă (ex. CTR Iași LRIA).
- **Acces:** API cu „Client ID Token”, creat în secțiunea „API Clients” din profilul de cont (conform documentației unor aplicații terțe). Descărcări în masă: neconfirmat.
- **Cost / autentificare:** Cont gratuit; proiect întreținut de voluntari, finanțat din donații
- **Licență / termeni:** Licența oficială e neconfirmată. Pe forum, administratorul a permis utilizarea în aplicații necomerciale, cu atribuire către openAIP.
- **Actualizare:** Actualizări comunitare (frecvență neconfirmată) · **Acoperire:** Global, inclusiv RO/MD (completitudine neconfirmată)
- **Precauții:** Nu e sursă oficială. Pentru restricții în vigoare consultați AIP/NOTAM (ROMATSA, MoldATSA, EAD). Zonele temporare din NOTAM pot lipsi.
- **Sursă:** https://groups.google.com/g/openaip/c/mUdnOppU5Eo · încredere scăzută

### ICAO API Data Service – NOTAM (realtime/stored) ★★★☆☆ ✔
- **Link:** https://icao.int/Aviation-API-Data-Service/Pages/default.aspx
- **Ce oferă:** NOTAM-uri în timp real, preluate din FAA Defense Internet NOTAM Service pentru o listă de locații date, și NOTAM-uri stocate (actualizate la 3 h).
- **Acces:** REST după înregistrarea pe portalul ICAO API, cu listă de indicatori ICAO (ex. LRIA, LRSV, LRBB, LUKK, LUUU). Max. 10 indicatori/cerere: raport de forum, neconfirmat.
- **Cost / autentificare:** 100 de apeluri gratuite la înregistrare (perioadă de probă, conform paginilor ICAO; un forum vorbește de 100/lună, neconfirmat). Apoi „booster packs” (până la 40.000 de apeluri) sau abonament nelimitat. Prețuri prin ICAOAPI@icao.int.
- **Licență / termeni:** Unele achiziții cer un acord de licență ICAO. Detalii: neconfirmat.
- **Actualizare:** Realtime (endpoint realtime) sau 3 h (endpoint stored) · **Acoperire:** Global
- **Precauții:** Cota gratuită e mică: potrivit doar pentru interogări punctuale, declanșate de alte semnale. NOTAM-urile de restricție pot apărea după anunțurile MApN sau MA MD.
- **Sursă:** https://icao.int/safety/iStars/Pages/Get-NOTAM-Data.aspx · încredere medie

### Odesa OVA – lista canalelor Telegram ale administrațiilor militare raionale (RVA) ★★★☆☆ ✔
- **Link:** https://www.thesis.od.ua/2024/02/05/v-odeskij-ova-opublikuvaly-telegram-kanaly-rajonnyh-vijskovyh-administraczij/
- **Ce oferă:** Lista canalelor Telegram ale celor 7 raioane din oblastul Odesa, publicată de Odesa OVA în februarie 2024. Relevante: Izmail, Bolhrad, Bilhorod-Dnistrovskyi, Podilsk (la granița cu R. Moldova/Transnistria).
- **Acces:** Web (articol de presă locală care redă lista OVA)
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Static (2024; lista poate fi depășită) · **Acoperire:** Oblastul Odesa
- **Precauții:** Verificați fiecare handle pe site-ul oficial al RDA/RVA respective. Canalele raionale publică consecințe, nu traiectorii.
- **Sursă:** https://www.thesis.od.ua/2024/02/05/v-odeskij-ova-opublikuvaly-telegram-kanaly-rajonnyh-vijskovyh-administraczij/ · încredere medie

### Aplicația DSU + canalul WhatsApp DSU + fiipregatit.ro ★★★☆☆ ✔
- **Link:** https://fiipregatit.ro
- **Ce oferă:** Aplicația mobilă gratuită DSU (știri, hartă interactivă, sfaturi, avertizări), canalul WhatsApp al DSU pentru actualizări în timp real și portalul FIIPREGATIT.
- **Acces:** Aplicație Android/iOS; canal WhatsApp anunțat de DSU (Raed Arafat). Feed/API: neconfirmat. Dacă aplicația păstrează istoricul RO-Alert: neconfirmat. Lansarea canalului WhatsApp: vezi focuspress.ro/departamentul-pentru-situatii-de-urgenta-a-lansat-un-canal-de-comunicare-pe-whatsapp/ (articol vechi de ~2 ani; verificați dacă e încă activ).
- **Cost / autentificare:** Gratuit
- **Licență / termeni:** neconfirmat
- **Actualizare:** Minute (neconfirmat) · **Acoperire:** România
- **Precauții:** Nu are un feed automatizabil confirmat, deci monitorizarea e manuală. IGSU a semnalat mesaje WhatsApp false trimise în numele său: urmăriți doar canalul anunțat oficial de DSU.
- **Sursă:** https://www.antena3.ro/actualitate/aplicatie-alerte-actualizata-dsu-harta-interactiva-sfaturi-664253.html · încredere medie

### Flightradar24 – hartă GPS jamming ★★☆☆☆ ✔
- **Link:** https://www.flightradar24.com/data/gps-jamming
- **Ce oferă:** Hartă a interferențelor GNSS derivată din datele ADS-B FR24 (alternativă la GPSJam).
- **Acces:** Web; API/export neconfirmat
- **Cost / autentificare:** Gratuit (vizualizare)
- **Licență / termeni:** Termenii FR24; redistribuirea și scraping-ul: neconfirmat (probabil interzise)
- **Actualizare:** neconfirmat (probabil zilnic) · **Acoperire:** Global, unde există trafic ADS-B
- **Precauții:** Aceleași limite ca GPSJam (proxy NIC, fals pozitive). Folosiți ca link sau captură cu atribuire, nu prin scraping.
- **Sursă:** https://flightradar24.com/data/gps-jamming · încredere scăzută
