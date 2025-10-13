import requests
import time
import json
import os
from datetime import datetime

# URL base an request
base_url = "https://api.casinoscores.com/svc-evolution-game-events/api/supercolorgame"
headers = {
    "accept": "*/*",
    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "origin": "https://casinoscores.com",
    "referer": "https://casinoscores.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}

# Params request
params_base = {
    "size": 19,
    "sort": "data.settledAt,desc",
    "duration": 4320,
    "isLightningMultiplierMatched": "false"
}

# Number of page to be downloaded
numero_pagine = 344
risultati = []

# Download data
for page in range(numero_pagine):
    params = params_base.copy()
    params["page"] = page

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        dati = response.json()

        for elemento in dati:
            try:
                result = elemento["data"]["result"]
                risultati.append({
                    "first": result.get("first", ""),
                    "second": result.get("second", ""),
                    "third": result.get("third", "")
                })
            except (KeyError, TypeError):
                risultati.append({"first": "", "second": "", "third": ""})

    except requests.RequestException as e:
        risultati.append({
            "error_page": page,
            "error_message": str(e)
        })

    time.sleep(0.5)

# Folder if not exist
os.makedirs("risultati", exist_ok=True)

# Count existing files
existing_files = [f for f in os.listdir("risultati") if f.startswith("risultato_")]
next_index = len(existing_files) + 1

# Name with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
file_name = f"risultati/risultato_{next_index}_{timestamp}.json"

# Save file JSON
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(risultati, f, ensure_ascii=False, indent=2)

print(f"✅ File salvato: {file_name}")

