import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

# On teste la version v1 officielle et les derniers noms valides
endpoints_to_test = [
    ("https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent", "v1 / gemini-2.0-flash"),
    ("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent", "v1beta / gemini-2.0-flash-lite"),
    ("https://generativelanguage.googleapis.com/v1beta/models/gemini-flash:generateContent", "v1beta / gemini-flash standard")
]

print("--- TEST FINAL DES ENDPOINTS ---")
for url_base, label in endpoints_to_test:
    url = f"{url_base}?key={key}"
    payload = {"contents": [{"parts": [{"text": "bonjour"}]}]}
    res = requests.post(url, json=payload).json()
    
    if "candidates" in res:
        print(f"\n✅ LE VOILÀ ! Endpoint gagnant : {label}")
        print(f"URL à utiliser : {url_base}")
        break
    else:
        err = res.get("error", {}).get("message", "Erreur inconnue")
        print(f"❌ {label} -> {err[:50]}...")