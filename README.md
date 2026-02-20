# Gemini Python Scripts (Chat + Markdown TTS)

A small collection of Python scripts using the **Google Gemini API** via the **`google-genai`** SDK:

- Interactive terminal chat with a Gemini model
- Model discovery / capability listing
- Markdown → cleaned text → **Text-to-Speech (TTS)** audio generation (with chunking for long documents)

## Requirements

- Python 3.10+ (recommended)
- A Gemini API key in the environment: `GEMINI_API_KEY`
- Dependency: `google-genai`

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install google-genai
```

Set your API key:

Linux/macOS:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Windows (PowerShell):

```powershell
$env:GEMINI_API_KEY = "YOUR_API_KEY"
```

## Scripts

### `gemini.py` — Interactive chat (streaming)

Starts an interactive chat session in the terminal and streams responses as they are generated.

- Default model: `models/gemini-2.5-flash`

Run:

```bash
./gemini.py
# or
python3 gemini.py
```

Type `exit` (or `quit`) to leave.

### `list_models.py` — List available Gemini models

Lists models returned by `client.models.list()` and prints those with `gemini` in the name.

Run:

```bash
python3 list_models.py
```

### `test.py` — List models + supported actions

Prints a table of model names and their `supported_actions` (as exposed by the `google-genai` library).

Run:

```bash
python3 test.py
```

### `markdown_tts.py` — Markdown to speech (audio)

Converts a Markdown file to speech using a Gemini TTS model:

- Cleans Markdown formatting (code blocks, links, images, HTML tags, etc.)
- Splits long text into chunks (defaults to ~5000 characters)
- Streams audio back and concatenates it
- If the API returns raw PCM (`audio/L16`), it wraps it in a WAV header

Defaults:

- Model: `gemini-2.5-flash-preview-tts`
- Voice: `Charon`
- Input file: `content.md` (configurable via `MARKDOWN_FILE`)

Run:

```bash
# optional: choose a different markdown file
export MARKDOWN_FILE="content.md"

python3 markdown_tts.py
```

The script will ask for an output filename (without extension) and then write the resulting audio file.

## Environment variables

- `GEMINI_API_KEY` (required): your API key.
- `MARKDOWN_FILE` (optional): which Markdown file to read for TTS (default: `content.md`).

## Notes / Troubleshooting

- **Model access**: not every API key has access to every model. If you get a “model not found / not permitted” error, run `python3 list_models.py` or `python3 test.py` to discover what your key can use.
- **Costs & privacy**: sending content to an API may incur costs and may be subject to your organization’s policies. Avoid uploading sensitive material unless you are allowed to.
- **Large documents**: chunking is character-based and sentence-splitting is best-effort. If you notice awkward breaks, reduce `MAX_CHUNK_CHARS` in `markdown_tts.py`.
