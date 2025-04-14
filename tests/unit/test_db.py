# tests/unit/test_db.py
import pytest
from unittest.mock import patch, MagicMock  # Nödvändigt för mockning
from datetime import datetime, timezone

# Importera funktionen som ska testas
from app.db import get_visit_by_id, add_visit, init_db, get_all_visits, format_visit_history

# Exempel på databasrad (som tuple)
SAMPLE_DB_ROW = (10, datetime(2025, 4, 13, 12, 0, 0, tzinfo=timezone.utc), '192.168.1.100', 'MockAgent')

@patch('app.db.get_db_connection') # Mocka get_db_connection inuti db.py
def test_get_visit_by_id_found(mock_get_connection):
    """
    Testar att funktionen get_visit_by_id returnerar korrekt data med hjälp av
    mockning när en post hittas i databasen.
    """
    # Skapa mock cursor- och connection-objekt
    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    # Låt mock_connection returneras när get_db_connection anropas
    mock_get_connection.return_value = mock_connection
    # Låt mock_cursor returneras när connection.cursor() anropas
    mock_connection.cursor.return_value = mock_cursor
    # Låt vår exempeldata returneras när cursor.fetchone() anropas
    mock_cursor.fetchone.return_value = SAMPLE_DB_ROW

    visit_id_to_find = 10
    result = get_visit_by_id(visit_id_to_find)

    # Förväntat resultat (som funktionen konverterat till dict)
    expected_result = {
        "id": SAMPLE_DB_ROW[0],
        "timestamp": SAMPLE_DB_ROW[1],
        "ip": SAMPLE_DB_ROW[2],
        "user_agent": SAMPLE_DB_ROW[3]
    }

    # 1. Kontrollera att funktionen returnerar korrekt resultat
    assert result == expected_result

    # 2. Kontrollera att mock-objekten anropades korrekt (valfritt men god praxis)
    mock_get_connection.assert_called_once() # Anropades get_db_connection 1 gång?
    mock_connection.cursor.assert_called_once() # Anropades cursor() 1 gång?
    # Kontrollera att execute anropades med korrekt SQL och parametrar
    mock_cursor.execute.assert_called_once_with(
        'SELECT id, timestamp, ip, user_agent FROM visits WHERE id = %s',
        (visit_id_to_find,)
    )
    mock_cursor.fetchone.assert_called_once() # Anropades fetchone() 1 gång?
    mock_cursor.close.assert_called_once() # Anropades close() 1 gång?
    mock_connection.close.assert_called_once() # Anropades close() 1 gång?


@patch('app.db.get_db_connection') # Mocka get_db_connection inuti db.py
def test_get_visit_by_id_not_found(mock_get_connection):
    """
    Testar att funktionen get_visit_by_id returnerar None med hjälp av
    mockning när en post inte hittas i databasen.
    """
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    # Låt fetchone() inte hitta någon post denna gång, returnera None
    mock_cursor.fetchone.return_value = None

    visit_id_to_find = 999
    result = get_visit_by_id(visit_id_to_find)

    # Kontrollera att resultatet är None
    assert result is None

    # Vi kan kontrollera mock-anropen igen...
    mock_get_connection.assert_called_once()
    mock_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        'SELECT id, timestamp, ip, user_agent FROM visits WHERE id = %s',
        (visit_id_to_find,)
    )
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


# --- NYTT TEST för add_visit ---

# Ange en fast tidsstämpel för testet
FIXED_DATETIME_NOW = datetime(2025, 4, 13, 14, 0, 0, tzinfo=timezone.utc)
# Ange ett fast nytt ID för testet (returneras från fetchone)
EXPECTED_NEW_ID = 5

# Vi använder två patchar: en för databasen, en för datetime
@patch('app.db.get_db_connection')
@patch('app.db.datetime') # Mocka datetime som används i db.py
def test_add_visit(mock_datetime, mock_get_connection): # Mock-objekten kommer i omvänd ordning!
    """
    Testar att funktionen add_visit lägger till ett besök med korrekt SQL
    och parametrar och returnerar den förväntade dictionaryn.
    """
    # Ställ in mock-objekten
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    # Låt vår fasta tid returneras när datetime.now() anropas
    mock_datetime.now.return_value = FIXED_DATETIME_NOW
    # Låt en tuple innehållande det förväntade nya ID:t returneras när cursor.fetchone() anropas
    mock_cursor.fetchone.return_value = (EXPECTED_NEW_ID,)

    # IP och User Agent som ska testas
    test_ip = "11.22.33.44"
    test_user_agent = "AddVisit Test Agent"

    # Kör funktionen
    result = add_visit(test_ip, test_user_agent)

    # 1. Kontrollera att den returnerade dictionaryn är korrekt
    expected_result = {
        "id": EXPECTED_NEW_ID,
        "timestamp": FIXED_DATETIME_NOW,
        "ip": test_ip,
        "user_agent": test_user_agent
    }
    assert result == expected_result

    # 2. Kontrollera mock-anropen
    mock_datetime.now.assert_called_once_with(timezone.utc) # Anropades datetime.now(timezone.utc)?
    mock_get_connection.assert_called_once()
    mock_connection.cursor.assert_called_once()
    # Kontrollera att execute anropades med korrekt INSERT-fråga och parametrar
    mock_cursor.execute.assert_called_once_with(
        'INSERT INTO visits (timestamp, ip, user_agent) VALUES (%s, %s, %s) RETURNING id',
        (FIXED_DATETIME_NOW, test_ip, test_user_agent) # Är parametrarna korrekta?
    )
    mock_cursor.fetchone.assert_called_once()
    mock_connection.commit.assert_called_once() # Anropades commit?
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


# --- NYA TESTER för init_db och get_all_visits ---

@patch('app.db.get_db_connection')
def test_init_db(mock_get_connection):
    """
    Testar att funktionen init_db kör SQL för att skapa tabellen och sedan
    utför commit och close.
    """
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    # Kör funktionen
    init_db()

    # Kontrollera mock-anropen
    mock_get_connection.assert_called_once()
    mock_connection.cursor.assert_called_once()
    # Kontrollera att execute anropades med korrekt CREATE TABLE-fråga
    # (Du kan kopiera den exakta SQL-texten från db.py och klistra in här,
    # eller bara kontrollera att den innehåller nyckelorden)
    assert 'CREATE TABLE IF NOT EXISTS visits' in mock_cursor.execute.call_args[0][0]
    mock_connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


# Vi kan använda den tidigare definierade SAMPLE_DB_ROW här också
# Eller låt oss definiera ny exempeldata
SAMPLE_DB_ROWS_FOR_ALL = [
    (1, datetime(2025, 4, 10, 10, 0, 0, tzinfo=timezone.utc), '1.1.1.1', 'Agent1'),
    (2, datetime(2025, 4, 11, 11, 0, 0, tzinfo=timezone.utc), '2.2.2.2', 'Agent2')
]

@patch('app.db.get_db_connection')
def test_get_all_visits_returns_list(mock_get_connection):
    """
    Testar att funktionen get_all_visits returnerar posterna från databasen
    som en lista i korrekt format.
    """
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    # Låt vår exempel-datalista returneras när fetchall anropas
    mock_cursor.fetchall.return_value = SAMPLE_DB_ROWS_FOR_ALL

    # Kör funktionen
    result = get_all_visits()

    # Förväntat resultat (lista med dicts)
    expected_result = [
        {"id": row[0], "timestamp": row[1], "ip": row[2], "user_agent": row[3]}
        for row in SAMPLE_DB_ROWS_FOR_ALL
    ]

    # 1. Kontrollera att resultatet är som förväntat
    assert result == expected_result

    # 2. Kontrollera mock-anropen
    mock_get_connection.assert_called_once()
    mock_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with('SELECT id, timestamp, ip, user_agent FROM visits ORDER BY id')
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@patch('app.db.get_db_connection')
def test_get_all_visits_empty(mock_get_connection):
    """
    Testar att funktionen get_all_visits returnerar en tom lista när
    det inte finns några poster i databasen.
    """
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    # Låt fetchall returnera en tom lista denna gång
    mock_cursor.fetchall.return_value = []

    # Kör funktionen
    result = get_all_visits()

    # Kontrollera att resultatet är en tom lista
    assert result == []

    # Kontrollera mock-anropen (fetchall anropas ändå)
    mock_get_connection.assert_called_once()
    mock_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with('SELECT id, timestamp, ip, user_agent FROM visits ORDER BY id')
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


# --- NYTT TEST för format_visit_history ---

def test_format_visit_history():
    """
    Testar att funktionen format_visit_history returnerar den givna
    indatan oförändrad.
    """
    # Du bör få tillbaka det du skickar in till funktionen
    sample_input1 = []
    sample_input2 = [{"id": 1}, {"id": 2}]
    sample_input3 = "Detta är en sträng" # Indata av annan typ

    result1 = format_visit_history(sample_input1)
    result2 = format_visit_history(sample_input2)
    result3 = format_visit_history(sample_input3)

    # Kontrollera om resultatet är detsamma som indatan (värdejämlikhet, inte referensjämlikhet)
    assert result1 == sample_input1
    assert result1 is sample_input1 # Returnerades samma objekt? (Ja, för denna funktion)

    assert result2 == sample_input2
    assert result2 is sample_input2

    assert result3 == sample_input3
    assert result3 is sample_input3 