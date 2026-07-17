from dotenv import load_dotenv

import os

from fetch_sharepoint import fetch_data_from_sharepoint

load_dotenv()
LIST_ID = os.getenv("GLOSSARY_GUID")

fetch_data_from_sharepoint(LIST_ID, "./data/raw/glossary_raw.json")