import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

print(f"Clé détectée : {key[:10]}...")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
res = requests.get(url).json()

if "models" in res:
    print("\n--- MODÈLES DISPONIBLES POUR TA CLÉ ---")
    for m in res["models"]:
        if "generateContent" in m.get("supportedGenerationMethods", []):
            # Affiche le nom exact du modèle
            print(m["name"].replace("models/", ""))
else:
    print("Erreur :", res)