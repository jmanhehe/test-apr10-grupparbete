import re  # För att kontrollera textmönster
from playwright.sync_api import Page, expect # Grundläggande Playwright-element

# Applikationens bas-URL
BASE_URL = "http://localhost:5000"

def test_root_page_loads_and_shows_welcome(page: Page):
    """
    Testar att huvudsidan ('/') laddas korrekt och innehåller välkomstmeddelandet.
    Detta test kräver inga ändringar i main.py.
    """
    print(f"\nNavigerar till rot-URL: {BASE_URL}/")
    # 1. Gå till huvudsidan
    page.goto(f"{BASE_URL}/")

    # 2. Verifiera att sidans titel är "Welcome"
    # Denna titel kommer från app/rendering.py -> format_welcome_message -> to_basic_html_page.
    print("Verifierar sidtitel...")
    expect(page).to_have_title("Welcome")
    print("Sidtitel 'Welcome' verifierad.")

    # 3. Verifiera att texten "Welcome, you are visitor number" finns på sidan
    # Besöksnumret kan ändras för varje test, så vi letar efter ett mönster istället för ett exakt nummer.
    # Funktionen format_welcome_message i rendering.py placerar meddelandet inom en <p>-tagg.
    welcome_paragraph = page.locator("p") # Hitta paragraf-elementet
    welcome_text_pattern = re.compile(r"Welcome, you are visitor number \d+") # Mönster som innehåller ett tal (\d+)
    print(f"Verifierar textmönster i paragrafen: '{welcome_text_pattern.pattern}'")
    expect(welcome_paragraph).to_have_text(welcome_text_pattern) # Paragrafens text ska matcha mönstret
    print("Välkomsttextmönster verifierat.")

    print("test_root_page_loads_and_shows_welcome slutfördes framgångsrikt.")

