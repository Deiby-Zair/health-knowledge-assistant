from pathlib import Path
from PyPDF2 import PdfReader
import json
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PDF_DIR = PROJECT_ROOT / "data" / "raw" / "pdfs"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "pdfs"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

for pdf_path in RAW_PDF_DIR.glob("*.pdf"):
    reader = PdfReader(pdf_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = clean_text(page.extract_text() or "")

        pages.append({
            "page": page_number,
            "text": text
        })

    output_path = PROCESSED_DIR / f"{pdf_path.stem}_pages.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

    print(f"Processed: {pdf_path.name}")