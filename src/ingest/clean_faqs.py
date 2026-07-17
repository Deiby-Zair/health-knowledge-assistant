import json
from pathlib import Path
from src.utils.text_cleaning import clean_html

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "faq_raw.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "faq_clean.json"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

faqs = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    items = json.load(f)

for item in items:
    faqs.append({
        "id": item.get("Id"),
        "pregunta": clean_html(item.get("Pregunta")),
        "respuesta": clean_html(item.get("Respuesta"))
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(faqs, f, ensure_ascii=False, indent=2)

print(f"Clean FAQs: {len(faqs)}")