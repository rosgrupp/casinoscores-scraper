import requests
import time
import json
from datetime import datetime
import os

base_url = "https://api.casinoscores.com/svc-evolution-game-events/api/supercolorgame"
headers = {
    "accept": "*/*",
    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "origin": "https://casinoscores.com",
    "priority": "u=1, i",
    "referer": "https://casinoscores.com/",
    "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}

params_base = {
    "size": 19,
    "sort": "data.settledAt,desc",
    "duration": 4320,
    "isLightningMultiplierMatched": "false"
}

numero_pagine = 344
cartella_risultati = "risultati"
os.makedirs(cartella_risultati, exist_ok=True)

def scarica_dati():
    risultati = []
    for page in range(numero_pagine):
        params = params_base.copy()
        params["page"] = page
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            dati = response.json()
            for elemento in dati:
                result = elemento.get("data", {}).get("result", {})
                first = result.get("first", "")
                second = result.get("second", "")
                third = result.get("third", "")
                risultati.append({
                    "first": first,
                    "second": second,
                    "third": third
                })
        except requests.RequestException as e:
            print(f"Errore pagina {page}: {e}")
        time.sleep(0.5)
    return risultati

# 🔹 Esegue solo una volta (GitHub lo riavvia ogni 72h)
print("📥 Avvio download dati nuovi...")
dati = scarica_dati()

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
nome_file = f"respondecolor_{timestamp}.json"
percorso_file = os.path.join(cartella_risultati, nome_file)

with open(percorso_file, "w", encoding="utf-8") as f:
    json.dump(dati, f, ensure_ascii=False, indent=2)

print(f"✅ File salvato in {percorso_file}")
