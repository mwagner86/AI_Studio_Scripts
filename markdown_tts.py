"""
Module for converting Markdown files to high-quality speech using Gemini API.
Includes chunking (1200 chars) and silence padding to maintain audio fidelity.
"""

import mimetypes
import os
import struct
import re
from typing import List, Optional, Dict
from google import genai
from google.genai import types

# Constants for quality and stability
# gemini-2.5-flash-preview-tts
# is a smaller, faster TTS model that may have slightly lower audio quality but is more cost-effective and has lower latency.
# gemini-2.5-pro-preview-tts
# is a high-quality TTS model with good stability, but it may have higher latency and cost compared to smaller models.
# Adjust as needed based on your requirements.

DEFAULT_MODEL = "gemini-2.5-flash-preview-tts"
DEFAULT_VOICE = "Charon"
MAX_CHUNK_CHARS = 1200  # Smaller chunks to prevent speed-up and quality loss
SILENCE_DURATION = 0.5  # Seconds of silence between segments
SAMPLE_RATE = 24000


def save_binary_file(file_name: str, data: bytes) -> None:
    """Saves binary data to a file."""
    with open(file_name, "wb") as f_handle:
        f_handle.write(data)
    print(f"File saved to: {file_name}")


def clean_markdown_for_tts(text: str) -> str:
    """Removes markdown syntax that disrupts the flow of speech."""
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`.*?`', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'[#*_~]+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_text(text: str, max_chars: int = MAX_CHUNK_CHARS) -> List[str]:
    """Splits text into segments at sentence boundaries."""
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


def generate_silence(duration: float, rate: int = SAMPLE_RATE) -> bytes:
    """Generates a sequence of null bytes to represent silence in PCM L16."""
    num_samples = int(rate * duration)
    # L16 means 2 bytes per sample (16-bit)
    return b'\x00\x00' * num_samples


def convert_to_wav(audio_data: bytes, rate: int = SAMPLE_RATE) -> bytes:
    """Adds a RIFF/WAV header to raw PCM audio data."""
    bits = 16
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", 36 + len(audio_data), b"WAVE", b"fmt ", 16, 1,
        1, rate, rate * (bits // 8), (bits // 8), bits, b"data", len(audio_data)
    )
    return header + audio_data


def generate() -> None:
    """Main function to handle the TTS generation process."""
    api_key = os.environ.get("GEMINI_API_KEY_3")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return

    client = genai.Client(api_key=api_key)
    md_filename = os.environ.get("MARKDOWN_FILE", "content.md")
    md_path = os.path.join(os.path.dirname(__file__), md_filename)

    try:
        with open(md_path, "r", encoding="utf-8") as md_file:
            raw_text = md_file.read()
    except FileNotFoundError:
        print(f"Error: Markdown file not found at {md_path}")
        return

    cleaned_text = clean_markdown_for_tts(raw_text)
    text_chunks = split_text(cleaned_text)

    user_filename = input("Enter filename (without extension): ").strip()
    if not user_filename:
        user_filename = "output_audio"

    print(f"Processing {len(text_chunks)} segments...")

    all_audio_data = b""
    final_mime_type: Optional[str] = None

    config = types.GenerateContentConfig(
        temperature=1.0,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=DEFAULT_VOICE
                )
            )
        ),
    )

    for i, segment in enumerate(text_chunks):
        print(f"Segment {i+1}/{len(text_chunks)}...")
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text="Sprich diesen Text ruhig und deutlich vor:"),
                    types.Part.from_text(text=segment)
                ]
            )
        ]

        try:
            for chunk in client.models.generate_content_stream(
                model=DEFAULT_MODEL, contents=contents, config=config
            ):
                if chunk.parts and chunk.parts[0].inline_data:
                    data = chunk.parts[0].inline_data
                    all_audio_data += data.data
                    if not final_mime_type:
                        final_mime_type = data.mime_type

            # Add silence between segments for better transitions
            if i < len(text_chunks) - 1:
                all_audio_data += generate_silence(SILENCE_DURATION)

        except Exception as err:  # pylint: disable=broad-except
            print(f"Error in segment {i+1}: {err}")

    if all_audio_data:
        ext = ".wav"
        # Always use WAV for combined L16 chunks
        final_audio = convert_to_wav(all_audio_data, SAMPLE_RATE)
        save_binary_file(f"{user_filename}{ext}", final_audio)
    else:
        print("No audio data generated.")


if __name__ == "__main__":
    generate()
