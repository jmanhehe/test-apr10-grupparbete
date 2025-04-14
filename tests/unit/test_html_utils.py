# tests/unit/test_html_utils.py
import pytest
# Lägg till nya funktioner till befintlig import:
from app.html_utils import (
    to_heading_line,
    get_html_end_block,
    to_text_paragraph,
    get_html_start_block,
    to_basic_html_page,  
    to_error_message     
)


def test_to_heading_line_creates_correct_h2_tag():
    """
    Kontrollerar att funktionen to_heading_line skapar korrekt <h2>-tagg
    för en rubrik på nivå 2.
    """
    text = "Title"
    heading_level = 2
    expected_html = "<h2>Title</h2>\n"

    actual_html = to_heading_line(text, heading_level)

    assert actual_html == expected_html

def test_to_heading_line_escapes_html_chars():
    """
    Testar om funktionen to_heading_line hanterar (escape:ar) speciella HTML-tecken.
    """
    text = "<script>alert('danger')</script>"
    heading_level = 1
    # Apostrof ' blir &#x27;.
    expected_html = "<h1>&lt;script&gt;alert(&#x27;danger&#x27;)&lt;/script&gt;</h1>\n"

    actual_html = to_heading_line(text, heading_level)

    assert actual_html == expected_html

def test_get_html_end_block_returns_correct_tags():
    """
    Testar att funktionen get_html_end_block returnerar korrekta sluttaggar.
    """
    expected = "</body>\n</html>\n"
    actual = get_html_end_block()
    assert actual == expected

def test_to_text_paragraph_wraps_text_in_p_tags():
    """
    Testar att funktionen to_text_paragraph omsluter texten med korrekta <p>-taggar.
    """
    text = "Bu bir paragraf metnidir." # Texten kan förbli på turkiska eller översättas här också
    expected = "<p>Bu bir paragraf metnidir.</p>\n"
    actual = to_text_paragraph(text)
    assert actual == expected

def test_to_text_paragraph_escapes_html():
    """
    Testar att funktionen to_text_paragraph hanterar (escape:ar) HTML-tecken.
    """
    text = "<b>Bold</b>"
    expected = "<p>&lt;b&gt;Bold&lt;/b&gt;</p>\n" # < och > ska hanteras (escape:as)
    actual = to_text_paragraph(text)
    assert actual == expected

def test_get_html_start_block_contains_title():
    """
    Testar att funktionen get_html_start_block inkluderar den givna titeln
    inom <title>-taggen.
    """
    title = "Sidtitel" 
    expected_title_tag = f"<title>{title}</title>"
    actual = get_html_start_block(title)
    
    assert expected_title_tag in actual
    # Kontrollera även att grundläggande HTML-taggar finns med
    assert "<!DOCTYPE html>" in actual
    assert "<html lang=\"en\">" in actual
    assert "<body>" in actual

def test_get_html_start_block_escapes_title():
    """
    Testar att funktionen get_html_start_block hanterar (escape:ar)
    specialtecken i titeln.
    """
    title = "<Rubrik>" 
    # Vi förväntar oss taggen innehållande den hanterade (escaped) titeln
    expected_title_tag = "<title>&lt;Rubrik&gt;</title>" 
    actual = get_html_start_block(title)
    assert expected_title_tag in actual


def test_to_basic_html_page_without_heading():
    """
    Testar att funktionen to_basic_html_page fungerar utan rubrik (heading).
    """
    title = "Enkel Sida" 
    text = "Sidinnehåll här" 
    actual = to_basic_html_page(title, text)

    assert f"<title>{title}</title>" in actual
    assert f"<p>{text}</p>" in actual
    assert "<h2>" not in actual # Rubrik ska inte finnas

def test_to_basic_html_page_with_heading():
    """
    Testar att funktionen to_basic_html_page fungerar med rubrik (heading).
    """
    title = "Sida med rubrik" 
    text = "Sidinnehåll" 
    heading = "Detta är en rubrik" 
    actual = to_basic_html_page(title, text, heading)

    assert f"<title>{title}</title>" in actual
    assert f"<p>{text}</p>" in actual
    assert f"<h2>{heading}</h2>" in actual # H2-rubrik ska finnas

def test_to_error_message_formats_correctly():
    """
    Testar att funktionen to_error_message formaterar felmeddelandet korrekt.
    """
    error_text = "Något gick fel!" 
    actual = to_error_message(error_text)

    # to_error_message anropar to_basic_html_page med specifika parametrar:
    # title="Error!", text=error_text, heading="An error occurred"
    assert "<title>Error!</title>" in actual
    assert "<h2>An error occurred</h2>" in actual
    assert f"<p>{error_text}</p>" in actual 