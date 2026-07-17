from pathlib import Path
from PyPDF2 import PdfReader
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PDF_DIR = PROJECT_ROOT / "data" / "raw" / "pdfs"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "pdfs"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

for pdf_path in RAW_PDF_DIR.glob("*.pdf"):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    text = clean_text(text)

    output_path = PROCESSED_DIR / f"{pdf_path.stem}_clean.txt"
    output_path.write_text(text, encoding="utf-8")

    print(f"Procesado: {pdf_path.name}")