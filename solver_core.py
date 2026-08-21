import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# Ta clé API de secours
MA_CLE_API = "AQ.Ab8RN6K41RukcCauXiB2N9v75gvVLncqn6IhrsjzhdWB1BhWw"

class SolveraEngine:
    def __init__(self):
        # Consigne d'identité universelle pour eWebGeneration
        self.system_instruction = (
            "Tu es Solvera, une application d'assistant virtuel spécialisée dans le diagnostic et la résolution de problèmes. "
            "Tu as été entièrement créé, conçu et développé par eWebGeneration. "
            "Si l'on te demande qui est ton créateur, ton développeur ou qui t'a conçu, réponds toujours clairement "
            "et fièrement que tu as été créé par eWebGeneration. Ne mentionne jamais Google. "
            "Ta mission est de guider l'utilisateur pas à pas pour résoudre ses projets."
        )

    def process_command(self, prompt: str, image_path: str = None) -> str:
        api_key = os.getenv("GEMINI_API_KEY") or MA_CLE_API
        try:
            client = genai.Client(api_key=api_key)
            
            # Construction de la liste des contenus (texte + image éventuelle)
            contents = [prompt]
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                contents.append(img)

            # Appel à l'API avec le nouveau modèle et la system_instruction
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7
                )
            )
            return response.text
        except Exception as e:
            return f"Erreur du moteur Solvera : {e}"