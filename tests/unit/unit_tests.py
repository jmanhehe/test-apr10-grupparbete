import pytest

from html_utils import to_basic_html_page, get_html_start_block, get_html_end_block, to_heading_line, to_text_paragraph

from rendering import format_hello_greeting, format_visit_details, format_welcome_message, format_visit_history

def test_format_welcome_message():
 
    sample_visit = {"id" : 123}
    expected_text = f"Welcome, you are visitor number {sample_visit['id']}"

    actual_html = format_welcome_message(sample_visit)

    assert expected_text in actual_html

def test_format_visit_history():
    sample_history = [
        {"id": 1, "timestamp": "2023-10-01 10:00:00"},
        {"id": 2, "timestamp": "2023-10-02 11:00:00"},
    ]
    expected_output = get_html_start_block("Visits")
    expected_output += to_heading_line("Visit history")
    for visit in sample_history:
        expected_output += to_text_paragraph(f"- {visit['timestamp']}: Visit #{visit['id']}\n")
    expected_output += get_html_end_block()

    actual_html = format_visit_history(sample_history)

    assert expected_output in actual_html

def test_format_visit_details():
    visit = {
        "id": 42,
        "timestamp": "Fri, 11 Apr 2025 08:25:13 GMT",
        "ip": "192.168.1.1",
        "user_agent": "Mozilla/5.0"
    }

    expected_output = get_html_start_block("Visit details")
    expected_output += to_heading_line(f"Visit #{visit['id']}")
    expected_output += to_text_paragraph(f"When: {visit['timestamp']}")
    expected_output += to_text_paragraph(f"IP: {visit['ip']}")
    expected_output += to_text_paragraph(f"User agent: {visit['user_agent']}")
    expected_output += get_html_end_block()

    actual_output = format_visit_details(visit)

    assert actual_output == expected_output



