#!/usr/bin/env python3
from google import genai
import os
import sys


if "GEMINI_API_KEY" not in os.environ:
    raise ValueError("GEMINI_API_KEY environment variable not set")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("Available Models for generateContent:")
# Das neue SDK nutzt eine andere Iterations-Logik
for model in client.models.list():
    # Filterung auf Modelle, die Content generieren können (grob gefiltert über Namensschema)
    if "gemini" in model.name:
        print(f"- {model.name}")
