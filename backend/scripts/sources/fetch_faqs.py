from pathlib import Path

from scripts.sources.fetch_sharepoint import fetch_data_from_sharepoint
from scripts.sources.guid_get import get_guid


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "faq_raw.json"

def main():
    faqs_guid = get_guid("Preguntas Frecuentes")
    fetch_data_from_sharepoint(faqs_guid, OUTPUT_FILE)

if __name__ == "__main__":
    main()