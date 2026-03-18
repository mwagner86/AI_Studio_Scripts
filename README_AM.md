# Academic Markdown to Speech (OpenAI TTS)

Dieses Tool konvertiert akademische Lehrmaterialien und Studienbriefe im **Markdown-Format** in hochwertige Audio-Dateien (MP3). Es nutzt die **OpenAI Text-to-Speech API** und ist speziell darauf optimiert, wissenschaftliche Artefakte zu filtern, um ein flüssiges Hörbuch-Erlebnis zu schaffen.

---

## Kernfunktionen

**Akademische Bereinigung:**

Automatisches Entfernen von Quellenbelegen (z. B. `[Pi17, S. 31]`), Bildverweisen (z. B. `Pasted image...`) und Metadaten wie "Lesezeit" oder "Bearbeitungszeit".

**Intelligentes Chunking:**

 Zerlegt lange Texte an Satzgrenzen in API-konforme Segmente, um das Limit von 4.096 Zeichen pro Request optimal zu nutzen.

**Sprachfluss-Optimierung:**

* Wandelt Paragraphen-Zeichen (`§`) in das Wort "Paragraph" um.
* Erkennt und korrigiert Abkürzungen (z. B. "v. Schirach" zu "von Schirach").
* Filtert URLs und technische Website-Links (YouTube etc.) aus, um Buchstabieren zu verhindern.

**Nahtlose Zusammenführung:** Alle Audio-Segmente werden sequenziell in eine einzige MP3-Datei geschrieben, ohne hörbare Schnitte.

---

## Voraussetzungen

### System

* Python 3.10 oder höher
* Ein aktiver OpenAI API-Key (Paid Tier empfohlen für längere Texte)

### Installation

1. Virtuelle Umgebung erstellen (optional):

```bash
    python3 -m venv .venv
    source .venv/bin/activate
```

2. OpenAI SDK installieren:

```bash
    pip install openai
```

---

## Konfiguration

Bevor das Skript gestartet wird, müssen die API-Schlüssel als Umgebungsvariable gesetzt werden:

```bash
export OPENAIKEY="deinkey"
```

Optional kann der Pfad zur Quelldatei angepasst werden (Standard ist `content.md` im selben Verzeichnis):

```bash
export MARKDOWN_FILE="studienbrief_ethik.md"
```

---

## Nutzung

1. Füge den gewünschten Text in die Datei `content.md` ein.
2. Starte das Konversions-Skript:

```bash
    python3 tts_openai.py
```

3. Gib den gewünschten Namen für die MP3-Datei ein (z. B. `Ethik_Lerneinheit_2`).
4. Die fertige Datei wird im selben Ordner gespeichert.

---

## Fehlerbehebung

* **Error: OPENAIKEY not found:**
Stelle sicher, dass `export OPENAIKEY="..."` im aktuellen Terminal-Tab ausgeführt wurde.

* **429 Resource Exhausted:**
Obwohl du im Paid Tier bist, können kurzzeitige Rate-Limits auftreten. Das Skript fängt Fehler pro Segment ab und gibt einen Hinweis aus.

* **Fehlende Abschnitte im Audio:** Prüfe, ob der Text in `content.md` Wörter aus der `meta_keywords`-Liste im Skript enthält, die fälschlicherweise ganze Zeilen löschen könnten.

---

## Rechtlicher Hinweis

Dieses Tool dient der Barrierefreiheit und dem persönlichen Studium. Beachte bei der Umwandlung von geschützten Lehrmaterialien die Urheberrechtsbestimmungen deines Bildungsanbieters.
