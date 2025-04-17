import pytest
from playwright.sync_api import sync_playwright, expect

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
    input_field.fill("John Doe")

    page.click("button[type='submit']")

    greeting = page.locator("body p")
    expect(greeting).to_have_text("Hello, John Doe!")