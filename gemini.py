#!/usr/bin/env python3
from google import genai
import os
import sys

# Konfiguration (Aktualisiert auf Preview-Version)
MODEL_ID = 'models/gemini-2.5-flash'

if "GEMINI_API_KEY" not in os.environ:
    print("Error: GEMINI_API_KEY environment variable not set")
    sys.exit(1)

# Client Initialisierung (Neues SDK: google-genai)
try:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
except Exception as e:
    print(f"Client Init Error: {e}")
    sys.exit(1)

try:
    # Chat Session erstellen (Neue Syntax: client.chats.create)
    chat = client.chats.create(model=MODEL_ID)

    print(f"Connected to {MODEL_ID} (Type 'exit' to quit)")
    print("-" * 40)

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break # Beendet bei Ctrl+D

        if user_input.lower() in ['exit', 'quit']:
            break
        if not user_input.strip():
            continue

        print("Gemini: ", end="", flush=True)

        try:
            # Streaming Response (Neue Syntax: send_message_stream)
            response = chat.send_message_stream(user_input)
            for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            print("\n")
        except Exception as e:
            print(f"\n> [!Warning] API Error during generation: {e}")

except Exception as e:
    print(f"\nConnection Error: {e}")
    print(f"> [!Warning] Verify if '{MODEL_ID}' is accessible via your API Key.")
