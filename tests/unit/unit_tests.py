import pytest

from rendering import format_hello_greeting, format_visit_details, format_welcome_message, format_visit_history

def test_format_welcome_message():
 sample_visit = {"id" : 123}
 expected_result = "Welcome", f"Welcome, you are visitor number {sample_visit['id']}"
 assert format_welcome_message(sample_visit) == expected_result
