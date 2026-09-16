import requests
import json

def fetch_data_from_sharepoint(list_id, output_file):
    url = (
        f"https://www.minsalud.gov.co/_api/web/"
        f"lists(guid'{list_id}')/items?$top=5000"
    )

    headers = {
        "Accept": "application/json;odata=verbose",
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=30)

    print("Status:", r.status_code)
    r.raise_for_status()

    data = r.json()
    items = data["d"]["results"]

    print(f"Downloaded records: {len(items)}")
    print("Columns:", list(items[0].keys())[:15])

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"File saved: {output_file}")