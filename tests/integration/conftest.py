import pytest
import os
import time  
# Importera huvudapplikationen och databasens initieringsfunktion
# OBS: För att dessa importer ska fungera är inställningen `pythonpath = .` i filen `pytest.ini` viktig!
from app.main import app as flask_app
from app.db import init_db, get_db_connection

# Ställ in miljövariabler för databasen (för testmiljön)
# Vi kan använda värdena från Docker eller specifika värden för test.
# Viktigt: Om testerna körs utanför Docker,
#          kan en testdatabasanslutning behöva konfigureras här.
# För närvarande antar vi värdena från Docker Compose.
os.environ['DB_NAME'] = os.getenv('DB_NAME', 'postgres')
os.environ['DB_USER'] = os.getenv('DB_USER', 'postgres')
os.environ['DB_PASSWORD'] = os.getenv('DB_PASSWORD', 'password')
# OBS: Tester körs vanligtvis mot en separat databas.
# Om 'db'-tjänsten från docker-compose ska användas direkt bör host vara 'db'.
# Om testerna använder en separat lokal db kan host vara 'localhost'.
# För närvarande antar vi '127.0.0.1' (localhost) så att lokala tester också kan köras.
# Vid behov kan vi ändra detta eller strategin för testdatabasen.
os.environ['DB_HOST'] = os.getenv('DB_HOST', '127.0.0.1')
os.environ['DB_PORT'] = os.getenv('DB_PORT', '5432')


@pytest.fixture(scope='function') # Körs före varje testfunktion
def app():
    """Skapar en Flask app-fixture."""

    # Sätt applikationen i testläge
    flask_app.config.update({
        "TESTING": True,
    })

    # Vänta en kort stund för att databasen eventuellt ska starta (t.ex. 5 sekunder)
    print("\nVäntar 5 sekunder för att DB eventuellt ska starta...")
    time.sleep(5)
    print("Fortsätter med fixture-setup.")

    try:
        init_db() # Säkerställ att tabellen existerar
    except Exception as e:
        print(f"VARNING: Kunde inte initiera DB i fixture: {e}")
        # Här måste vi bestämma hur vi ska hantera felsituationen.
        # Kanske testerna bör hoppas över? Fortsätt tills vidare.

    yield flask_app # Testfunktionen körs här

    # Rensa upp efter testerna kan göras här (t.ex. ta bort databastabeller)
    # För närvarande lägger vi inte till något rensningssteg.


@pytest.fixture()
def client(app):
    """Fixture som tillhandahåller Flasks testklient."""
    return app.test_client() 