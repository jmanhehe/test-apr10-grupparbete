# Testplan: Webapp Testprojekt

*(Testplan skapad: 2025-04-11)*

## 1. Introduktion / Översikt

Detta dokument beskriver testplanen för testprocessen av den Flask-baserade webbapplikationen som tillhandahålls inom ramen för projektet `test-apr10-grupparbete`. Syftet med planen är att definiera testomfattning, mål, strategi, resurser och leverabler.

Applikationen som ska testas är en enkel webbapplikation som loggar besöksinformation (IP-adress, tidpunkt, user-agent) och visar denna information (`/`, `/visits`, `/visit/<id>`) samt erbjuder en enkel interaktiv hälsningsfunktion (`/hello`, `/hello-form`). Applikationen körs lokalt med Docker Compose.

## 2. Omfattning (Scope)

### 2.1. Inom Omfattning (In Scope)

Följande punkter ingår i denna testplans omfattning:

* Test av alla huvudfunktioner och routes specificerade i README-filen:
    * Hemsida (`/`): Visning av innehåll och verifiering att besöksräknaren uppdateras.
    * Besökslistning (`/visits`): Listning av alla besök samt validering av datumfiltrering med `from`- och `to`-parametrar.
    * Detaljer för enskilt besök (`/visit/<id>`): Korrekt visning av besöksdetaljer med ett giltigt ID.
    * Hälsningsmeddelande (`/hello`): Korrekt visning av meddelanden, både med och utan `name`-parameter.
    * Hälsningsformulär (`/hello-form`): Visning av formuläret samt verifiering att ifyllt namn skickas korrekt till `/hello`-routen och att resultatet visas.
* Funktionell korrekthet: Säkerställa att alla funktioner fungerar som förväntat, att data bearbetas och visas korrekt.
* Grundläggande negativa scenarier och felhantering: Försök med ogiltiga `/visit/<id>`, ogiltiga filtreringsparametrar, ogiltig indata i formulär (om tillämpligt).
* Utförande av manuella tester: Utforskande tester och scenariobaserade manuella tester baserade på identifierade testfall.
* Skapande och körning av automatiserade tester (enligt README-krav):
    * Enhetstester (`pytest`): För interna funktioner i applikationskoden (mål >= 80% kodtäckning).
    * Integrationstester (`pytest`): Minst ett test för varje route, inklusive interaktioner med databasen.
    * Systemtester (`Playwright`): Minst ett end-to-end-scenario som interagerar med applikationen via användargränssnittet.
* Rapportering av funna buggar i det format som specificeras i README.
* Rättelse av rapporterade buggar (om några hittas) och verifiering av att rättningarna fungerar via automatiserade tester.

### 2.2. Utanför Omfattning (Out of Scope)

Följande punkter ligger utanför denna testplans omfattning:

* Prestanda-, last- eller stresstester (Applikationens beteende under hög belastning kommer inte att testas).
* Omfattande säkerhetstester (Detaljerade säkerhetsanalyser som SQL Injection, XSS, etc. kommer inte att utföras).
* Omfattande användbarhetstester (Detaljerade analyser av användarupplevelsen kommer inte att utföras).
* Detaljerade kompatibilitetstester på ett stort antal olika webbläsare/operativsystem-kombinationer (Tester kommer primärt att utföras i den webbläsare som används i utvecklingsmiljön).
* Test av själva driftsättningsprocessen (deployment) av applikationen eller dess Docker-image till andra miljöer.

## 3. Testmål (Test Objectives)

De primära målen för testningen i detta projekt är att:

* Verifiera att all specificerad funktionalitet i webbapplikationens routes (`/`, `/visits`, `/visit/<id>`, `/hello`, `/hello-form`), inklusive parametrar och formulärhantering, fungerar korrekt enligt de krav som implicit ges i README och genom applikationens observerade beteende.
* Uppnå och demonstrera minst 80% kodtäckning för applikationskoden i `app/`-katalogen med enhetstester skrivna med `pytest`.
* Säkerställa att varje route (`/`, `/visits`, `/visit/<id>`, `/hello`, `/hello-form`) i applikationen täcks av minst ett meningsfullt integrationstest skrivet med `pytest`, vilket inkluderar interaktion med databasen där det är relevant.
* Implementera och framgångsrikt köra minst ett representativt end-to-end systemtest med `Playwright` som simulerar en typisk användarinteraktion med applikationen.
* Identifiera, dokumentera och rapportera eventuella funktionella buggar, fel eller avvikelser från förväntat beteende i en separat testrapport.
* Säkerställa att alla kritiska och högprioriterade buggar som identifieras under testningen blir rättade och att rättelserna verifieras med hjälp av uppdaterade eller nya (helst automatiserade) tester.
* Demonstrera förståelse för och praktisk tillämpning av olika testnivåer (enhet, integration, system) och testtyper (manuell, automatiserad) under projektets gång.
* Tillämpa relevanta testdesignteniker (såsom ekvivalensklassindelning, gränsvärdesanalys, black-box och white-box-perspektiv) vid skapandet av testfall, vilka kommer att dokumenteras separat.

## 5. Testmiljö (Test Environment)

Alla tester (manuella och automatiserade) kommer att utföras i följande miljö:
* **System:** Lokal utvecklingsmaskin (Windows 11, macOS Sonoma )
* **Applikationshosting:** Applikationen körs lokalt via Docker Desktop med hjälp av `docker-compose`, startad med skriptet `local-start.sh` eller `local-start.bat`.
* **Webbläsare (för manuella tester och Playwright):** (Google Chrome)
* **Databas:** SQLite-databas som körs inom Docker-containern (enligt `docker-compose.yml`).

## 6. Roller och Ansvar (Roles and Responsibilities)

Detta är ett grupparbete med fyra medlemmar. Ansvarsfördelningen är planerad enligt följande (detta är ett **förslag** och kan justeras av gruppen internt):

* **[Gruppmedlem 1 Namn]:**
    * Övergripande koordinering och ansvar för att Testplanen (detta dokument) blir komplett.
    * Huvudansvar för utveckling och underhåll av **Enhetstester** (`pytest`) för funktionerna i `app/`-katalogen (särskilt fokus på t.ex. `db.py`, `rendering.py`).
    * Bidra till buggfixning, speciellt för fel som upptäcks via enhetstester.

* **[Gruppmedlem 2 Namn]:**
    * Huvudansvar för **Testfallsdesign**: Identifiera, dokumentera (`testcases.md/pdf/xlsx`) och underhålla testfall för både manuella och automatiserade tester. Tillämpa relevanta testdesignteniker (black-box, white-box, ekvivalensklasser, gränsvärden).
    * Huvudansvar för utförandet av **Manuella Tester** (både utforskande och scenariobaserade).

* **[Gruppmedlem 3 Namn]:**
    * Huvudansvar för utveckling och underhåll av **Integrationstester** (`pytest`) för samtliga routes (`/`, `/visits`, etc.), inklusive verifiering av databasinteraktioner.
    * Huvudansvar för **Buggrapportering**: Sammanställa och formatera den slutliga testrapporten (`testrapport.md/pdf`) baserat på funna buggar från alla testaktiviteter.
    * Bidra till buggfixning, speciellt för fel som upptäcks via integrationstester.

* **[Gruppmedlem 4 Namn]:**
    * Huvudansvar för utveckling och underhåll av **Systemtester** (`Playwright`) för att testa end-to-end-flöden i applikationen.
    * Ansvar för att skriva och färdigställa sammanfattningen (`summering.md`).
    * Koordinera och leda arbetet med den slutliga **Presentationen** av projektet.


## 7. Testleverabler (Test Deliverables)

Följande dokument och kod kommer att produceras och levereras som resultat av testarbetet (enligt README "Inlämning"):
* `summering.md`: Sammanfattning av arbetet.
* `testplan/testplan.md`: Detta dokument (Testplanen).
* `testplan/testcases.md` (eller `.pdf`/`.xlsx`): Dokumentation av identifierade och utförda testfall.
* `tests/`: Katalog innehållande all automatiserad testkod (enhets-, integrations- och systemtester).
* `testrapport.md` (eller `.pdf`): Sammanställning av testresultat och en lista över funna buggar.

## 8. Verktyg (Tools)

Följande verktyg kommer att användas under testprocessen:
* **Versionshantering:** Git / GitHub
* **Containerisering:** Docker Desktop (inkl. Docker Compose)
* **Testramverk (Automatiserad):** `pytest`, `Playwright`
* **Kodtäckning:** `coverage.py` (via `pytest-cov`)
* **Webbläsare:** [Google Chrome]
* **Texteditor/IDE:** [VS Code, PyCharm]
* **Dokumentation:** Markdown (.md), eventuellt PDF/XLSX för testfall/rapport.
