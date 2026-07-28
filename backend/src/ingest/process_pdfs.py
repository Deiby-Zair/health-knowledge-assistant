from pathlib import Path
from collections import Counter
from PyPDF2 import PdfReader
import json
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PDF_DIR = PROJECT_ROOT / "data" / "raw" / "pdfs"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "pdfs"


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text while preserving paragraph structure.
    """

    if not text:
        return ""

    # Remove hyphenated words split by line breaks
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    cleaned_lines = []

    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            cleaned_lines.append(line)

    # Remove repeated blank lines
    text = "\n".join(cleaned_lines)

    return text.strip()


def remove_repeated_headers_footers(pages: list[str]) -> list[str]:
    """
    Detect repeated first/last lines across pages and remove them.
    Useful for institutional PDFs with repeated headers/footers.
    """

    if len(pages) < 3:
        return pages

    first_lines = Counter()
    last_lines = Counter()

    split_pages = []

    for text in pages:
        lines = text.split("\n")

        split_pages.append(lines)

        if lines:
            first_lines[lines[0]] += 1
            last_lines[lines[-1]] += 1

    header_candidates = {
        line
        for line, count in first_lines.items()
        if count >= max(2, len(pages) // 2)
    }

    footer_candidates = {
        line
        for line, count in last_lines.items()
        if count >= max(2, len(pages) // 2)
    }

    cleaned_pages = []

    for lines in split_pages:

        if lines and lines[0] in header_candidates:
            lines = lines[1:]

        if lines and lines[-1] in footer_candidates:
            lines = lines[:-1]

        cleaned_pages.append("\n".join(lines).strip())

    return cleaned_pages


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for pdf_path in RAW_PDF_DIR.glob("*.pdf"):

        reader = PdfReader(pdf_path)

        raw_pages = [
            clean_text(page.extract_text() or "")
            for page in reader.pages
        ]

        cleaned_pages = remove_repeated_headers_footers(raw_pages)

        pages = []

        for page_number, text in enumerate(cleaned_pages, start=1):

            pages.append(
                {
                    "page": page_number,
                    "text": text,
                    "char_count": len(text),
                    "word_count": len(text.split()),
                }
            )

        output_path = PROCESSED_DIR / f"{pdf_path.stem}_pages.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(pages, f, ensure_ascii=False, indent=2)

        print(
            f"Processed {pdf_path.name} "
            f"({len(pages)} pages)"
        )
        
if __name__ == "__main__":
    main()