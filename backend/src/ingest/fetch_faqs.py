import os
from dotenv import load_dotenv
from pathlib import Path

from src.ingest.fetch_sharepoint import fetch_data_from_sharepoint

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "faq_raw.json"

def main():
    load_dotenv()
    LIST_ID = os.getenv("FAQS_GUID")

    fetch_data_from_sharepoint(LIST_ID, OUTPUT_FILE)
    
if __name__ == "__main__":
    main()