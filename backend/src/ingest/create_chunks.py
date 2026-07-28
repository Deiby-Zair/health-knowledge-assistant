from pathlib import Path
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter

# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CHUNKS_DIR = PROJECT_ROOT / "data" / "chunks"
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# CHUNK CONFIGURATION
# =========================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MIN_CHUNK_LENGTH = 30

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",   # Paragraphs
        "\n",     # Lines
        ". ",     # Sentences
        "; ",
        ", ",
        " ",
        ""
    ],
    length_function=len,
    is_separator_regex=False,
)


def split_text(text: str) -> list[str]:
    """Split text preserving semantic boundaries whenever possible."""

    chunks = text_splitter.split_text(text)

    return [
        chunk.strip()
        for chunk in chunks
        if len(chunk.strip()) >= MIN_CHUNK_LENGTH
    ]


def save_chunks(filename: str, chunks: list):
    with open(CHUNKS_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


def main():
    # =========================================================
    # FAQ CHUNKS
    # =========================================================

    faq_file = PROCESSED_DIR / "faq_clean.json"

    with open(faq_file, encoding="utf-8") as f:
        faq_data = json.load(f)

    faq_chunks = []

    for item in faq_data:

        content = (
            f"Pregunta: {item['pregunta']}\n\n"
            f"Respuesta: {item['respuesta']}"
        ).strip()

        faq_chunks.append(
            {
                "id": f"faq_{item['id']}",
                "text": content,
                "metadata": {
                    "type": "faq",
                    "source": "minsalud_faq",
                    "faq_id": item["id"],
                    "question": item["pregunta"],
                    "char_count": len(content),
                },
            }
        )

    save_chunks("faq_chunks.json", faq_chunks)

    # =========================================================
    # GLOSSARY CHUNKS
    # =========================================================

    glossary_file = PROCESSED_DIR / "glossary_clean.json"

    with open(glossary_file, encoding="utf-8") as f:
        glossary_data = json.load(f)

    glossary_chunks = []

    for item in glossary_data:

        content = (
            f"Término: {item['termino']}\n\n"
            f"Definición: {item['definicion']}"
        ).strip()

        glossary_chunks.append(
            {
                "id": f"glossary_{item['id']}",
                "text": content,
                "metadata": {
                    "type": "glossary",
                    "source": "minsalud_glossary",
                    "term": item["termino"],
                    "char_count": len(content),
                },
            }
        )

    save_chunks("glossary_chunks.json", glossary_chunks)

    # =========================================================
    # PDF CHUNKS
    # =========================================================

    pdf_dir = PROCESSED_DIR / "pdfs"

    pdf_chunks = []

    for json_file in sorted(pdf_dir.glob("*_pages.json")):

        with open(json_file, encoding="utf-8") as f:
            pages = json.load(f)

        source_name = json_file.stem.replace("_pages", ".pdf")

        for page_data in pages:

            page_number = page_data["page"]
            text = page_data["text"].strip()

            if len(text) < MIN_CHUNK_LENGTH:
                continue

            chunks = split_text(text)

            total_chunks = len(chunks)

            for index, chunk in enumerate(chunks):

                pdf_chunks.append(
                    {
                        "id": f"{json_file.stem}_p{page_number}_{index}",
                        "text": chunk,
                        "metadata": {
                            "type": "pdf",
                            "source": source_name,
                            "page": page_number,
                            "chunk_index": index,
                            "total_chunks": total_chunks,
                            "char_count": len(chunk),
                        },
                    }
                )

    save_chunks("pdf_chunks.json", pdf_chunks)

    # =========================================================
    # SUMMARY
    # =========================================================

    print("=" * 50)
    print("Chunk generation completed")
    print("=" * 50)
    print(f"FAQ chunks      : {len(faq_chunks)}")
    print(f"Glossary chunks : {len(glossary_chunks)}")
    print(f"PDF chunks      : {len(pdf_chunks)}")
    print(f"Total chunks    : {len(faq_chunks) + len(glossary_chunks) + len(pdf_chunks)}")
    
if __name__ == "__main__":
    main()