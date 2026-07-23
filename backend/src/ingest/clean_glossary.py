import json
from pathlib import Path
from backend.src.utils.text_cleaning import clean_html

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "glossary_raw.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "glossary_clean.json"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


clean_data = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    items = json.load(f)

for item in items:
    clean_data.append({
        "id": item.get("Id"),
        "termino": clean_html(item.get("Title")),
        "definicion": clean_html(item.get("DESCRIPCI_x00d3_N"))
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(clean_data, f, ensure_ascii=False, indent=2)

print(f"Clean terms: {len(clean_data)}")