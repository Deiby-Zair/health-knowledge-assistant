import os

from dotenv import load_dotenv
from pathlib import Path

from backend.src.ingest.fetch_sharepoint import fetch_data_from_sharepoint

load_dotenv()
LIST_ID = os.getenv("FAQS_GUID")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "faq_raw.json"

fetch_data_from_sharepoint(LIST_ID, OUTPUT_FILE)