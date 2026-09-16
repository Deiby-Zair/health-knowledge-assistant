from bs4 import BeautifulSoup
import html
import re


def clean_html(text: str) -> str:
    """Clean HTML and returns only visible text."""

    if not text:
        return ""

    # Decode HTML entities
    text = html.unescape(text)

    # Parse HTML
    soup = BeautifulSoup(text, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Get visible text
    cleaned = soup.get_text(separator=" ")

    # Normalize spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned