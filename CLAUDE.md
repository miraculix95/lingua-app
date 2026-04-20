# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

Archived 2025 language-learning prototype (see parent path `oldcode/`). No git repo, no tests, no package manifest — standalone Python scripts using the shared `cc-dev/.env` or a local `.env` for `OPENAI_API_KEY`.

## Run

- Streamlit UI (primary app): `streamlit run franz-lern-streamlit.py -- --language=französisch`
  - `--language` accepts values from `languages` in the script (französisch, englisch, spanisch, ukrainisch, deutsch).
- CLI variant: `python franz-lern.py` (uses `prompt_toolkit` for multi-line input).
- Verb categorizer: `python verben_test/kategorisierung.py` — reads `verben_test/franz-verben.txt`, writes `franz-verben_sortiert.json` via LangChain + `langchain_openai`.
- MP4→MP3 batch: `python convertmp3mp4.py` (prompts for folder; requires `ffmpeg` on PATH).

Dependencies are not pinned. Expect: `streamlit openai python-dotenv prompt_toolkit requests pyaudio pydub mutagen langchain langchain-openai`. Audio work needs system `ffmpeg` and PortAudio (for `pyaudio`).

## Architecture

Two parallel implementations of the same language-tutor concept:

- `franz-lern.py` — terminal-loop version. `extract_french_vocabulary()` reads `.txt` files from `txt/` (or a single file), asks GPT-4o for a level-appropriate vocab list, then drives exercises. Older/simpler.
- `franz-lern-streamlit.py` — full Streamlit app, superset of the CLI. Heavy use of `st.session_state` (vocab_list, task_type, current_task, theme, level, niveau, mentor, …). Central constants at top of file define the task menu:
  - `task_list` — exercise types (text correction, cloze, translation, sentence building, error-finding, synonyms/antonyms, verb conjugation, radio capture).
  - `levels` (A1–C2), `niveau_levels` (register: Argot → Technisch), `mentoren` (teacher personas), `themen_liste` (topic seeds).
  - `radio_kanale` — hardcoded French radio streams (France Info/Inter/Culture, BFM); the "Radio hören und aufnehmen" task streams these via `requests` + `pyaudio`/`pydub`.
  - `function_spec` — OpenAI function-calling schema `generate_vocabulary_list` for structured vocab output.

Input corpus lives in `txt/` (French/Spanish/German mixed topic files — radio transcripts, news, psychology, tennis, strategy, vocab lists). Vocab-extraction tasks glob this directory.

`verben_test/kategorisierung.py` is a one-shot utility: LangChain `ChatOpenAI` + `StructuredOutputParser` proposes verb categories, then sorts the verbs from `franz-verben.txt` into them. Separate from the main apps.

`out/` holds two older `franz-lern-streamlit copy*.py` snapshots — treat as archive, not active code (per `~/.claude/rules/no-delete-archive.md`, don't delete).

`archiv_webapp_versuch/` is an abandoned attempt to port the Streamlit app to a web app:
- `backend/main.py` — FastAPI + async OpenAI, JWT auth (`SECRET_KEY = "supersecret"`, HS256), CORS `*`, `OAuth2PasswordBearer`. `backend/database.py` — sqlite (`users.db`) with `create_user/get_user/update_credits/init_db` (credits model implied).
- `frontend/` — static `index.html` + `chat.html`, empty `css/` and `js/` dirs.
- `documentation/instructions` (file, not dir) + `documentation/old/` holding earlier `backend_minimum.py`/`backend_openai.py` and HTML snapshots.
- `sqlite-dll-win-x64-3490100.zip` + extracted dir: Windows SQLite binaries, leftover from the author's dev environment — not relevant on this Linux server.
Treat the whole folder as reference/archive; don't revive without a plan. Hardcoded secret and wide-open CORS mean it's not prod-ready.

## Notes

- Models referenced inline: `gpt-4o-2024-05-13`, `gpt-4o-mini-2024-07-18`, `gpt-3.5-turbo-0125`. Likely outdated — verify before assuming behavior.
- No linter/formatter configured; match existing style (German comments, mixed German/English identifiers).
- `2025_03_20_wettbewerbsanalyse.xlsx` is a competitive-analysis spreadsheet, not code.
