import os

from dotenv import load_dotenv

from fetch_sharepoint import fetch_data_from_sharepoint

load_dotenv()
LIST_ID = os.getenv("FAQS_GUID")

fetch_data_from_sharepoint(LIST_ID, "./data/raw/faq_raw.json")