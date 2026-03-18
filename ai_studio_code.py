"""
Generisches OpenAI TTS-Skript für akademische Texte.
Automatische Filterung von Quellen, Metadaten und technischen Hinweisen.
Pylint-konform und mit Dateinamen-Validierung.
"""

import os
import re
import struct
from typing import List, Optional
from openai import OpenAI

# Konfiguration
DEFAULT_MODEL = "tts-1"
DEFAULT_VOICE = "alloy"  # Alternativen: echo, fable, onyx, nova, shimmer
MAX_CHARS_OPENAI = 4000


def clean_academic_generic(text: str) -> str:
    """
    Bereinigt Texte generisch von akademischem Ballast.
    Entfernt Quellen, Metadaten und optimiert den Lesefluss.
    """
    # 1. Entferne Quellenbelege in eckigen Klammern [XX00, S. 00]
    text = re.sub(r'\[[A-Z][a-zA-Z0-9,.\s\-]+\]', '', text)

    # 2. Paragraphen-Logik (generisch für § 2, § 2.1)
    text = re.sub(r'§\s*(\d+)\.?(\d+)?',
                  lambda m: f"Paragraph {m.group(1)}" +
                  (f" Punkt {m.group(2)}" if m.group(2) else ""),
                  text)

    # 3. Generische Abkürzungserkennung für Namen (v. Schirach -> von Schirach)
    text = re.sub(r'\bv\.\s+([A-Z])', r'von \1', text)

    # 4. Filterung von Metadaten-Zeilen
    meta_keywords = [
        "Bearbeitungszeit", "Lesezeit", "Zeitumfang", "Websource",
        "Pasted image", "Abb.", "Hinweis", "Lösungshinweis", "Hilfestellung"
    ]
    
    lines = text.split('\n')
    filtered_lines = []
    
    for line in lines:
        if any(line.strip().lower().startswith(kw.lower()) for kw in meta_keywords):
            continue
        if line.strip().lower() in ["zitat", "beispiel", "aufgabe", "vertiefung"]:
            continue
        filtered_lines.append(line)
        
    text = '\n'.join(filtered_lines)

    # 5. Links und URLs entfernen
    text = re.sub(r'https?://\S+', '', text)
    
    # 6. Markdown-Bereinigung
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[*_#~>]+', '', text)
    
    # 7. Whitespace-Normalisierung
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)
    
    return text.strip()


def split_text_openai(text: str, max_chars: int = MAX_CHARS_OPENAI) -> List[str]:
    """Teilt den Text an Satzenden in Blöcke auf."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def sanitize_filename(name: str) -> str:
    """Entfernt ungültige Zeichen aus dem Dateinamen, um FileNotFoundError zu vermeiden."""
    # Entferne alles, was kein Buchstabe, Zahl, Bindestrich oder Unterstrich ist
    clean_name = re.sub(r'[^\w\s-]', '', name).strip()
    # Ersetze Leerzeichen durch Unterstriche
    clean_name = re.sub(r'\s+', '_', clean_name)
    return clean_name


def generate_audio() -> None:
    """Hauptprozess zur Umwandlung von Markdown in MP3 via OpenAI."""
    api_key = os.environ.get("OPENAIKEY")
    if not api_key:
        print("Fehler: Umgebungsvariable 'OPENAIKEY' nicht gesetzt.")
        return

    client = OpenAI(api_key=api_key)
    md_filename = os.environ.get("MARKDOWN_FILE", "content.md")
    
    if not os.path.exists(md_filename):
        print(f"Fehler: Datei '{md_filename}' nicht gefunden.")
        return

    with open(md_filename, "r", encoding="utf-8") as f_in:
        raw_content = f_in.read()

    cleaned_text = clean_academic_generic(raw_content)
    text_chunks = split_text_openai(cleaned_text)

    # Dateiname abfragen und validieren
    raw_input = input("MP3-Dateiname (Standard: 'studienbrief'): ").strip()
    clean_name = sanitize_filename(raw_input)
    output_filename = f"{clean_name if clean_name else 'studienbrief'}.mp3"

    print(f"Generiere Audio aus {len(text_chunks)} Segmenten...")

    try:
        with open(output_filename, "wb") as f_out:
            for i, segment in enumerate(text_chunks):
                print(f"Verarbeite Segment {i+1}/{len(text_chunks)}...")
                response = client.audio.speech.create(
                    model=DEFAULT_MODEL,
                    voice=DEFAULT_VOICE,
                    input=segment
                )
                f_out.write(response.content)
        print(f"Erfolgreich abgeschlossen. Datei gespeichert unter: {output_filename}")
    except IOError as err:
        print(f"Dateifehler: Konnte Datei nicht schreiben. {err}")
    except Exception as err:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {err}")


if __name__ == "__main__":
    generate_audio()