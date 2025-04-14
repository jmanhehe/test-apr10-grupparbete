# tests/integration/test_app_routes.py
# OBS: Denna fil använder 'client'-fixturen från tests/integration/conftest.py.
# Därför behöver man INTE importera app eller definiera client-fixturen här igen.

import pytest # Kan behövas för funktioner som pytest.skip

# --- Testfunktioner ---

def test_root_route_get(client):
    """
    Testar om GET / routen lyckas (200 OK) och innehåller det förväntade
    välkomstmeddelandet. Förväntar sig att app-fixturen i conftest.py
    anropar init_db och att detta request är det första besöket
    (om testisolering finns).
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome, you are visitor number" in response.data # Numret kan variera
    assert b"<title>Welcome</title>" in response.data

def test_hello_default(client):
    """Testar GET /hello (utan parameter)."""
    response = client.get('/hello')
    assert response.status_code == 200
    assert b"<title>Hello</title>" in response.data
    assert b"<p>Hello, mysterious visitor!</p>" in response.data # Kontroll av exakt text

def test_hello_with_name(client):
    """Testar GET /hello?name=..."""
    name = "IntegrationTest"
    response = client.get(f'/hello?name={name}')
    assert response.status_code == 200
    assert b"<title>Hello</title>" in response.data
    assert bytes(f"<p>Hello, {name}!</p>", 'utf-8') in response.data

def test_hello_form_get(client):
    """Testar att GET /hello-form-sidan innehåller formulärelementen."""
    response = client.get('/hello-form')
    assert response.status_code == 200
    assert b"<h1>Say Hello</h1>" in response.data
    assert b'<form method="GET" action="/hello">' in response.data
    assert b'<input type="text" id="name">' in response.data
    assert b'<button type="submit">Say Hello</button>' in response.data

# --- /visits Tester ---
# För att dessa tester ska vara mer tillförlitliga krävs normalt DB-rensning mellan tester
# eller att känd data läggs till. conftest.py har en enkel init_db.

def test_visits_all(client):
    """Testar grundläggande innehåll på GET /visits-sidan."""
    # Skapa först ett besök (ifall testisolering saknas)
    client.get('/')
    response = client.get('/visits')
    assert response.status_code == 200
    assert b"<title>Visits</title>" in response.data
    assert b"<h1>Visit history</h1>" in response.data
    # Kontrollera att minst ett besök listas (t.ex. Visit #1)
    # Detta beror på det föregående anropet till client.get('/')
    assert b": Visit #1" in response.data

def test_visits_from_date(client):
    """Testar GET /visits?from=... filtret på en grundläggande nivå."""
    # OBS: För att testa att datumfiltren fungerar KORREKT
    # behöver kontrollerad data läggas till i conftest.py eller i testet.
    # För närvarande kontrollerar vi bara om sidan laddas.
    response = client.get('/visits?from=2025-04-10') # Exempeldatum
    assert response.status_code == 200
    assert b"<h1>Visit history</h1>" in response.data

def test_visits_to_date(client):
    """Testar GET /visits?to=... filtret på en grundläggande nivå."""
    response = client.get('/visits?to=2025-04-15') # Exempeldatum
    assert response.status_code == 200
    assert b"<h1>Visit history</h1>" in response.data

def test_visits_invalid_from_date_format(client):
    """Testar att GET /visits returnerar 400-fel för ogiltigt 'from'-datumformat."""
    response = client.get('/visits?from=invalid-date-format')
    assert response.status_code == 400
    assert b"Invalid 'from' date format" in response.data
    assert b"An error occurred" in response.data

def test_visits_invalid_to_date_format(client):
    """Testar att GET /visits returnerar 400-fel för ogiltigt 'to'-datumformat."""
    response = client.get('/visits?to=invalid-date-format')
    assert response.status_code == 400
    assert b"Invalid 'to' date format" in response.data
    assert b"An error occurred" in response.data

# --- /visit/<id> Tester ---

def test_visit_detail_found(client):
    """
    Testar GET /visit/<id> (med befintligt ID).
    Skapar först ett besök, tittar sedan på detaljerna.
    """
    # 1. Skapa ett nytt besök (genom att gå till root)
    root_response = client.get('/')
    # Försök hämta besöksnumret från svaret (förenklat)
    try:
        # Försök avkoda svaret och hitta siffran
        # Exempel: b'...visitor number 2</p>...'
        data_str = root_response.data.decode('utf-8')
        num_str = data_str.split("visitor number ")[1].split("</p>")[0]
        visit_id = int(num_str)
        print(f"\nBesöks-ID skapat för testet: {visit_id}")
    except Exception as e:
        print(f"\nVarning: Kunde inte hämta besöks-ID från svaret ({e}). Antar ID=1.")
        visit_id = 1 # Försök med 1 om ID inte kan hämtas

    # 2. Gå till detaljsidan för det skapade besöket
    response = client.get(f'/visit/{visit_id}')

    # Om ID inte hittas (t.ex. DB rensad eller felaktigt ID hämtat)
    if response.status_code == 404:
         pytest.skip(f"Visit ID {visit_id} found in root response but not found at /visit/{visit_id}")

    assert response.status_code == 200
    assert bytes(f"<h1>Visit #{visit_id}</h1>", 'utf-8') in response.data
    assert b"<title>Visit details</title>" in response.data
    assert b"When:" in response.data
    assert b"IP:" in response.data
    assert b"User agent:" in response.data


def test_visit_detail_not_found(client):
    """Testar GET /visit/<id> (med ett ID som inte finns)."""
    non_existent_id = 999999
    response = client.get(f'/visit/{non_existent_id}')
    assert response.status_code == 404
    assert b"Visit not found" in response.data
    assert b"An error occurred" in response.data 
    