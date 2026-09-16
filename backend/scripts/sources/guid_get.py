import requests

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GUID_FILE = PROJECT_ROOT / "data" / "raw" / "list_guids.txt"

GUID_FILE.parent.mkdir(parents=True, exist_ok=True)
        
def get_guid(name: str) -> str:
    with GUID_FILE.open(encoding="utf-8") as file:
        for line in file:
            if " - " not in line:
                continue

            line_name, guid = line.strip().split(" - ", 1)

            if line_name == name:
                return guid

    raise ValueError(f"No se encontró GUID para: {name}")

def main():

    url = "https://www.minsalud.gov.co/_api/web/lists?$select=Title,Id"

    headers = {
        "Accept": "application/json;odata=verbose",
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()

    lists = r.json()["d"]["results"]

    with open(GUID_FILE, "w", encoding="utf-8") as f:
        for lst in lists:
            title = lst["Title"]
            line = f"{title} - {lst['Id']}\n"
            print(line, end="")   # Opcional: seguir mostrando en consola
            f.write(line)

if __name__ == "__main__":
    main()