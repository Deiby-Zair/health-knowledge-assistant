import requests

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = PROJECT_ROOT / "src" / "utils" / "pages.txt"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


url = "https://www.minsalud.gov.co/_api/web/lists?$select=Title,Id"

headers = {
    "Accept": "application/json;odata=verbose",
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

lists = r.json()["d"]["results"]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for lst in lists:
        title = lst["Title"]
        line = f"{title} - {lst['Id']}\n"
        print(line, end="")   # Opcional: seguir mostrando en consola
        f.write(line)