from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CHUNKS_DIR = PROJECT_ROOT / "data" / "chunks"
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

# Chunk configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# =========================================================
# FAQ CHUNKS
# =========================================================
faq_file = PROCESSED_DIR / "faq_clean.json"
faq_data = json.load(open(faq_file, encoding="utf-8"))

faq_chunks = []

for item in faq_data:
    content = f"Pregunta: {item['pregunta']}\nRespuesta: {item['respuesta']}"

    faq_chunks.append({
        "id": f"faq_{item['id']}",
        "text": content,
        "metadata": {
            "type": "faq",
            "source": "minsalud_faq",
            "faq_id": item["id"],
            "question": item["pregunta"]
        }
    })

with open(CHUNKS_DIR / "faq_chunks.json", "w", encoding="utf-8") as f:
    json.dump(faq_chunks, f, ensure_ascii=False, indent=2)


# =========================================================
# GLOSSARY CHUNKS
# =========================================================
glossary_file = PROCESSED_DIR / "glossary_clean.json"
glossary_data = json.load(open(glossary_file, encoding="utf-8"))

glossary_chunks = []

for item in glossary_data:
    content = f"Término: {item['termino']}\nDefinición: {item['definicion']}"

    glossary_chunks.append({
        "id": f"glossary_{item['id']}",
        "text": content,
        "metadata": {
            "type": "glossary",
            "source": "minsalud_glossary",
            "term": item["termino"]
        }
    })

with open(CHUNKS_DIR / "glossary_chunks.json", "w", encoding="utf-8") as f:
    json.dump(glossary_chunks, f, ensure_ascii=False, indent=2)


# =========================================================
# PDF CHUNKS
# =========================================================
pdf_dir = PROCESSED_DIR / "pdfs"
pdf_chunks = []

for json_file in pdf_dir.glob("*_pages.json"):
    pages = json.load(open(json_file, encoding="utf-8"))

    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"]

        text_chunks = split_text(text)

        for index, chunk in enumerate(text_chunks):
            pdf_chunks.append({
                "id": f"{json_file.stem}_p{page_number}_{index}",
                "text": chunk,
                "metadata": {
                    "type": "pdf",
                    "source": json_file.stem.replace("_pages", ".pdf"),
                    "page": page_number
                }
            })

with open(CHUNKS_DIR / "pdf_chunks.json", "w", encoding="utf-8") as f:
    json.dump(pdf_chunks, f, ensure_ascii=False, indent=2)


print(f"FAQ chunks: {len(faq_chunks)}")
print(f"Glossary chunks: {len(glossary_chunks)}")
print(f"PDF chunks: {len(pdf_chunks)}")