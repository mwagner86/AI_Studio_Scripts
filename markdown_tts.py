"""
Module for converting Markdown files to speech using the Google Gemini API.
Cleans Markdown syntax and handles long texts via chunking.
"""

import mimetypes
import os
import struct
import re
from typing import List, Optional, Dict
from google import genai
from google.genai import types

# Constants
DEFAULT_MODEL = "gemini-2.5-flash-preview-tts"
DEFAULT_VOICE = "Charon"
MAX_CHUNK_CHARS = 5000


def save_binary_file(file_name: str, data: bytes) -> None:
    """Saves binary data to a file."""
    with open(file_name, "wb") as f_handle:
        f_handle.write(data)
    print(f"File saved to: {file_name}")


def clean_markdown_for_tts(text: str) -> str:
    """Removes markdown syntax that disrupts the flow of speech."""
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`.*?`', '', text)
    # Replace markdown links [text](url) with 'text'
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove image tags
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove remaining markdown symbols
    text = re.sub(r'[#*_~]+', '', text)
    # Normalize whitespace
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


def parse_audio_mime_type(mime_type: str) -> Dict[str, int]:
    """Parses rate and bits from mime type string."""
    rate = 24000
    if "rate=" in mime_type:
        try:
            match = re.search(r'rate=(\d+)', mime_type)
            if match:
                rate = int(match.group(1))
        except (ValueError, AttributeError):
            pass
    return {"bits_per_sample": 16, "rate": rate}


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Adds a RIFF/WAV header to raw PCM audio data."""
    params = parse_audio_mime_type(mime_type)
    rate = params["rate"]
    bits = params["bits_per_sample"]

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", 36 + len(audio_data), b"WAVE", b"fmt ", 16, 1,
        1, rate, rate * (bits // 8), (bits // 8), bits, b"data", len(audio_data)
    )
    return header + audio_data


def generate() -> None:
    """Main function to handle the TTS generation process."""
    api_key = os.environ.get("GEMINI_API_KEY")
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
                    types.Part.from_text(text="Lies flüssig und natürlich vor:"),
                    types.Part.from_text(text=segment)
                ]
            )
        ]

        try:
            for chunk in client.models.generate_content_stream(
                model=DEFAULT_MODEL,
                contents=contents,
                config=config,
            ):
                if chunk.parts and chunk.parts[0].inline_data:
                    data = chunk.parts[0].inline_data
                    all_audio_data += data.data
                    if not final_mime_type:
                        final_mime_type = data.mime_type
        except Exception as err:  # pylint: disable=broad-except
            print(f"Error in segment {i+1}: {err}")
            continue

    if all_audio_data:
        ext = mimetypes.guess_extension(final_mime_type) if final_mime_type else ".wav"
        if ext is None or "L16" in (final_mime_type or ""):
            ext = ".wav"
            all_audio_data = convert_to_wav(
                all_audio_data, final_mime_type or "audio/L16;rate=24000"
            )

        save_binary_file(f"{user_filename}{ext}", all_audio_data)
    else:
        print("No audio data generated.")


if __name__ == "__main__":
    generate()
