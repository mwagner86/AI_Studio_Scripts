# Setup

## 1) Create and activate venv

```bash
mkdir tts-project
cd tts-project
```

## 2) Initialize venv

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install google-genai
```

## 3) Set API key and run the script

Windows:

```PowerShell
$env:GEMINI_API_KEY = "DEIN_API_KEY"
$env:MARKDOWN_FILE = "content.md"
```

Linux/Mac:

```Bash
Linux/Mac:
export GEMINI_API_KEY="YOUR_API_KEY"
export MARKDOWN_FILE="content.md"
```
