from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print(f"{'Model Name':<40} | {'Supported Actions'}")
print("-" * 80)

for m in client.models.list():
    # In der google-genai Bibliothek heißt das Feld supported_actions
    actions = ", ".join(m.supported_actions) if m.supported_actions else "None"
    print(f"{m.name:<40} | {actions}")