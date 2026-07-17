from bs4 import BeautifulSoup
import html
import re


def clean_html(text: str) -> str:
    """Limpia HTML y devuelve solo texto visible."""

    if not text:
        return ""

    # Decodificar entidades HTML
    text = html.unescape(text)

    # Parsear HTML
    soup = BeautifulSoup(text, "html.parser")

    # Eliminar scripts y estilos
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Obtener texto visible
    cleaned = soup.get_text(separator=" ")

    # Normalizar espacios
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned