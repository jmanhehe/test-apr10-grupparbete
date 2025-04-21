import pytest
from playwright.sync_api import sync_playwright, expect
import time

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

def test_app_homepage(browser):
    context = browser.new_context()
    page = context.new_page()
        
    page.goto("http://localhost:5000/hello-form")

    input_field = page.get_by_label("Your name:") 
    name = "John Doe"
    input_field.fill(f"{name}")
    time.sleep(1)

    page.click("button[type='submit']")
    time.sleep(2)
    greeting = page.locator("body p")
    expect(greeting).to_have_text(f"Hello, {name}!")