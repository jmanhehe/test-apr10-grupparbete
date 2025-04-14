# tests/unit/test_rendering.py
import pytest
from datetime import datetime, timezone  # Importera datetime för tidsstämpel
# Importera alla funktioner som ska testas från app.rendering
from app.rendering import (
    format_hello_greeting,
    format_visit_details,
    format_welcome_message,
    format_visit_history
)

# Test 1: Innehåller format_hello_greeting("Alice") texten "Hello, Alice!"?
def test_format_hello_greeting_contains_correct_name():
    """
    Kontrollerar att funktionen format_hello_greeting returnerar en text
    som innehåller det angivna namnet.
    """
    name = "Alice"
    result_html = format_hello_greeting(name)
    # Kom ihåg att utdatan innehåller hela HTML-koden, inte bara textdelen.
    # Men som en enkel kontroll kan vi se om texten finns i utdatan.
    assert f"Hello, {name}!" in result_html

# Test 2: Finns tidsstämpel (timestamp) i format_visit_details()?
def test_format_visit_details_contains_timestamp():
    """
    Kontrollerar om funktionen format_visit_details inkluderar
    tidsstämpeln (timestamp) i besöksdetaljerna.
    """
    # Skapa ett exempel på ett visit-objekt (liknande det som returneras från db.py)
    sample_timestamp = datetime(2025, 4, 13, 10, 30, 0, tzinfo=timezone.utc)
    sample_visit = {
        "id": 1,
        "timestamp": sample_timestamp,
        "ip": "127.0.0.1",
        "user_agent": "TestBrowser"
    }

    result_html = format_visit_details(sample_visit)

    # Funktionen konverterar timestamp direkt till sträng och använder den: f"When: {visit['timestamp']}"
    # Låt oss därför kontrollera om strängrepresentationen av timestamp finns i HTML-koden.
    # Not: Istället för format som str(sample_timestamp) eller sample_timestamp.isoformat()
    # kontrollerar den hur Python som standard konverterar ett datetime-objekt till sträng.
    # För att vara säker på hur det ser ut i utdatan kan du vid behov även skriva ut den med print.
    assert f"When: {str(sample_timestamp)}" in result_html
    # Eller en mer generell kontroll:
    # assert str(sample_timestamp) in result_html


def test_format_welcome_message_contains_visitor_number():
    """
    Testar om funktionen format_welcome_message innehåller korrekt besöksnummer.
    """
    # Exempel på visit-objekt (endast 'id' verkar behövas)
    sample_visit = {"id": 123, "timestamp": datetime.now(), "ip": "1.1.1.1", "user_agent": "test"}
    expected_text = f"Welcome, you are visitor number {sample_visit['id']}"

    actual_html = format_welcome_message(sample_visit)

    # Kontrollera att texten finns i den returnerade HTML-koden
    assert expected_text in actual_html
    # Vi kan också kontrollera den grundläggande HTML-strukturen (valfritt)
    assert "<title>Welcome</title>" in actual_html

def test_format_visit_history_empty_list():
    """
    Testar hur funktionen format_visit_history beter sig när den får en tom lista.
    """
    history = []
    actual_html = format_visit_history(history)

    # Utdatan bör innehålla rubrik men inga listelement
    assert "Visit history" in actual_html
    # Kontrollera att inga besökselement finns (beroende på funktionens exakta output)
    assert "Visit #" not in actual_html # Eller kontrollera formatet "-ÅÅÅÅ-MM-DD..."

def test_format_visit_history_with_one_visit():
    """
    Testar att funktionen format_visit_history fungerar med en lista
    som innehåller ett enda besök.
    """
    sample_timestamp = datetime(2025, 4, 13, 11, 0, 0, tzinfo=timezone.utc)
    history = [
        {"id": 1, "timestamp": sample_timestamp, "ip": "1.2.3.4", "user_agent": "TestAgent1"}
    ]

    actual_html = format_visit_history(history)

    # Kontrollera om den förväntade besökstexten finns i HTML-koden
    # Format i rendering.py: f"- {visit['timestamp']}: Visit #{visit['id']}\n"
    expected_visit_line = f"- {str(sample_timestamp)}: Visit #{history[0]['id']}"

    assert "Visit history" in actual_html
    assert expected_visit_line in actual_html
    # Vi kan också kontrollera att den kommer inom en p-tagg
    # (Anta att rendering.py använder to_text_paragraph)
    assert f"<p>{expected_visit_line}" # Den bör föregås av en <p>-tagg  