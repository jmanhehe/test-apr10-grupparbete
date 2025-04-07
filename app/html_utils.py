import html

def get_html_start_block(title="Page"):
    """
    Returns a start block for a html and body block for a basic html page
    """
    escaped = html.escape(title)
    return f"<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"UTF-8\"><title>{escaped}</title></head>\n<body>\n"

def get_html_end_block():
    """
    Returns an end block for a html and body block for a basic html page
    """
    return "</body>\n</html>\n"

def to_heading_line(text, heading_level=1):
    """
    Returns the supplied text as a HTML heading of the requested level.
    Text will be HTML-escaped.
    """
    escaped = html.escape(text)
    return f"<h{heading_level}>{escaped}</h{heading_level}>\n"

def to_text_paragraph(text):
    """
    Returns the supplied text as a HTML text paragraph.
    Text will be HTML-escaped.
    """
    escaped = html.escape(text)
    return f"<p>{escaped}</p>\n"

def to_error_message(text):
    """
    Returns the supplied text as a complete HTML page with a formatted and escaped HTML error string.
    """
    return to_basic_html_page("Error!", text, "An error occurred")

def to_basic_html_page(title, text, heading=None):
    """
    Returns the supplied title, heading and text block as a complete basic HTML formatted page
    """
    result = get_html_start_block(title)
    if (heading):
        result += to_heading_line(heading, 2)
    result += to_text_paragraph(text)
    result += get_html_end_block()
    return result