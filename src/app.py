"""Streamlit entrypoint for franz-lern.

Start::

    streamlit run src/app.py -- --language=französisch
"""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import field
from pathlib import Path
from typing import Any

import openai
import streamlit as st
from dotenv import find_dotenv, load_dotenv

# Make "src" importable when run via `streamlit run src/app.py`
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import (  # noqa: E402
    DEFAULT_LANGUAGE,
    LANGUAGES,
    LEVELS,
    MENTOR_AVATARS,
    MENTOR_QUOTES,
    MENTORS,
    MODEL_TIERS,
    NIVEAU_LEVELS,
    TASK_LIST,
    THEMES,
    default_model_for_language,
)
from src.correction import answer_comment, correct_text, extract_comments  # noqa: E402
from src.logging_setup import get_logger  # noqa: E402
from src.state import init_session_state  # noqa: E402
from src.tasks import cloze as cloze_task  # noqa: E402
from src.tasks import conjugation as conj_task  # noqa: E402
from src.tasks import error_detection as err_task  # noqa: E402
from src.tasks import quiz as quiz_task  # noqa: E402
from src.tasks import sentence_building as sent_task  # noqa: E402
from src.tasks import synonym_antonym as syn_task  # noqa: E402
from src.tasks import translation as trans_task  # noqa: E402
from src.tasks import writing as write_task  # noqa: E402
from src.tasks.radio import RADIO_TASK_NAME, get_channels, is_audio_available  # noqa: E402
from src.vocab import (  # noqa: E402
    extract_vocabulary_from_text,
    fetch_article_text,
    generate_vocabulary_via_function_call,
)

log = get_logger(__name__)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="franz-lern Streamlit app")
    parser.add_argument("--language", default=DEFAULT_LANGUAGE)
    args, _unknown = parser.parse_known_args()
    if args.language not in LANGUAGES:
        args.language = DEFAULT_LANGUAGE
    return args


def _resolve_api_key() -> tuple[str | None, str]:
    """Pick API key by priority: session-state BYOK > OPENROUTER_API_KEY > OPENAI_API_KEY.

    Returns (key, source_label). source_label ∈ {"byok", "openrouter", "openai", "none"}.
    """
    load_dotenv(find_dotenv(usecwd=True))
    byok = st.session_state.get("byok_key", "").strip()
    if byok:
        return byok, "byok"
    or_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if or_key:
        return or_key, "openrouter"
    oa_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if oa_key:
        return oa_key, "openai"
    return None, "none"


def _build_client(key: str, source: str) -> openai.OpenAI:
    if source == "openai":
        return openai.OpenAI(api_key=key)
    return openai.OpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")


@st.cache_data(ttl=3600, show_spinner=False)
def _cached_extract_from_text(
    text: str, language: str, level: str, number: int, model: str, _cache_version: int = 1
) -> list[str]:
    """Cache-wrapper around LLM vocab extraction.

    Client is re-built inside since it's not hashable. Cache keys on the text
    content itself — same file → same vocab list, no second LLM call.
    """
    key, source = _resolve_api_key()
    if not key:
        return []
    client = _build_client(key, source)
    return extract_vocabulary_from_text(
        client, text=text, language=language, level=level, number=number, model=model,
    )


def _render_sidebar(language: str) -> tuple[str, str, str, str]:
    """Render sidebar and return (mentor, level, niveau, model)."""
    state = st.session_state["state"]

    with st.sidebar:
        st.markdown(f"### 🇫🇷 {language.capitalize()} lernen")

        with st.expander("👤 Coach & Stil", expanded=True):
            mentor = st.selectbox("Coach", MENTORS, index=0, key="mentor")
            level = st.selectbox("Sprachniveau", LEVELS, index=2, key="level")
            niveau = st.selectbox("Sprachregister", NIVEAU_LEVELS, index=3, key="niveau")

        with st.expander("📚 Vokabelquelle", expanded=True):
            extract_files = st.file_uploader(
                "Txt-Dateien",
                accept_multiple_files=True,
                type=["txt"],
                help="Extrahiert Vokabeln auf dem eingestellten Niveau.",
            )
            number_of_words = st.number_input(
                "Anzahl Vokabeln", min_value=1, max_value=200, value=state.number_of_words,
                key="number_of_words",
            )
            url_extract = st.text_input("Webseite-URL", placeholder="https://...")
            uploaded_vocab = st.file_uploader("Fertige Vokabel-Datei", type=["txt"])

        with st.expander("🤖 Modell & API", expanded=False):
            api_key_input = st.text_input(
                "🔑 OpenRouter API-Key",
                type="password",
                value=st.session_state.get("byok_key", ""),
                help="Dein Key. Bleibt in Session, wird nie gespeichert. "
                     "Hol einen auf openrouter.ai/keys.",
                placeholder="sk-or-...",
            )
            if api_key_input != st.session_state.get("byok_key", ""):
                st.session_state["byok_key"] = api_key_input

            _default_model = default_model_for_language(language)
            tier_labels = list(MODEL_TIERS.keys())
            default_idx = next(
                (i for i, lb in enumerate(tier_labels) if MODEL_TIERS[lb] == _default_model), 0,
            )
            tier = st.selectbox("Modell-Tier", tier_labels, index=default_idx, key="tier")
            model = MODEL_TIERS[tier]
            st.caption(f"`{model}`")

        # key-source indicator
        _, source = _resolve_api_key()
        source_labels = {
            "byok": "✅ Dein Key (BYOK)",
            "openrouter": "🔑 Server .env (OpenRouter)",
            "openai": "⚠️ Server .env (OpenAI-Fallback)",
            "none": "❌ Kein Key gefunden",
        }
        st.caption(f"Key-Quelle: {source_labels[source]}")

    state.file_path_extract_trigger = extract_files
    state.uploaded_vocab_file_trigger = uploaded_vocab
    state.url_extract_trigger = url_extract
    state.number_of_words = number_of_words

    return mentor, level, niveau, model


def _handle_vocab_sources(client: openai.OpenAI, language: str, level: str, model: str) -> None:
    """Process the three possible vocab sources. Writes to state.vocab_list."""
    state = st.session_state["state"]
    extract_files = state.file_path_extract_trigger
    url_extract = state.url_extract_trigger
    uploaded_vocab = state.uploaded_vocab_file_trigger
    number = state.number_of_words

    if extract_files and extract_files != state.file_path_extract:
        all_text = "\n".join(f.read().decode("utf-8") for f in extract_files)
        with st.status("📚 Extrahiere Vokabeln aus Datei…", expanded=False) as status:
            state.vocab_list = _cached_extract_from_text(
                all_text, language, level, number, model,
            )
            status.update(label=f"✅ {len(state.vocab_list)} Vokabeln extrahiert", state="complete")
        st.sidebar.write(sorted(state.vocab_list))
        state.file_path_extract = extract_files
    elif url_extract and url_extract != state.html_path_extract:
        with st.status(f"🌐 Lade {url_extract}…", expanded=False) as status:
            article = fetch_article_text(url_extract)
            status.update(label="🧠 Extrahiere Vokabeln…")
            state.vocab_list = _cached_extract_from_text(
                article, language, level, number, model,
            )
            status.update(label=f"✅ {len(state.vocab_list)} Vokabeln aus Web", state="complete")
        st.sidebar.write(sorted(state.vocab_list))
        state.html_path_extract = url_extract
    elif uploaded_vocab and uploaded_vocab != state.uploaded_vocab_file:
        content = uploaded_vocab.read().decode("utf-8")
        state.vocab_list = [line.strip() for line in content.splitlines() if line.strip()]
        st.sidebar.success(f"✅ {len(state.vocab_list)} Vokabeln geladen")
        state.uploaded_vocab_file = uploaded_vocab


def _render_header(language: str, mentor: str) -> None:
    """Title + session metrics + mentor quote."""
    state = st.session_state["state"]

    st.markdown(f"# {language.capitalize()} — Lernprogramm")

    quote = MENTOR_QUOTES.get(mentor, "")
    avatar = MENTOR_AVATARS.get(mentor, "🎓")
    if quote:
        st.caption(f'{avatar} *{mentor}:* „{quote}"')

    col1, col2, col3 = st.columns(3)
    col1.metric("📚 Aufgaben", getattr(state, "num_tasks_generated", 0))
    col2.metric("✏️ Korrekturen", getattr(state, "num_corrections", 0))
    col3.metric("🔄 Session-Runs", state.num_runs)

    st.caption("💡 Out-of-band-Fragen in spitzen Klammern einbetten, z.B. `<was heißt passé composé?>` — bekommst separate Antwort.")


def _generate_task(
    task_type: str, client: openai.OpenAI, language: str, level: str, niveau: str, model: str,
) -> None:
    """Build a task into state.task (displayed_to_user string)."""
    state = st.session_state["state"]

    label = f"🧠 {task_type or 'Aufgabe'}…"
    with st.status(label, expanded=False) as status:
        if task_type == "Schreiben eines Textes und danach Korrektur":
            instr = write_task.build(themes=THEMES, previous_theme=state.theme)
            state.theme = instr.internal_context["theme"]
        elif task_type == "Ausfüllen eines Lückentextes in Fremdsprache":
            instr = cloze_task.build(
                client, vocab_list=state.vocab_list, language=language, level=level,
                niveau=niveau, number_trous=state.number_trous, model=model,
            )
        elif task_type == "Vorgabe von deutschen Sätzen zum Übersetzen":
            instr = trans_task.build(
                client, vocab_list=state.vocab_list, language=language, level=level,
                niveau=niveau, number_sentences=state.number_sentences, model=model,
            )
        elif task_type == "Satzbauübung":
            instr = sent_task.build(
                client, vocab_list=state.vocab_list, language=language, level=level,
                niveau=niveau, model=model,
            )
        elif task_type == "Fehler im Text finden und korrigieren":
            instr = err_task.build(
                client, vocab_list=state.vocab_list, language=language, level=level,
                niveau=niveau, model=model,
            )
        elif task_type == "Synonyme und Antonyme finden":
            instr = syn_task.build(vocab_list=state.vocab_list)
        elif task_type == "Verbkonjugation üben":
            instr = conj_task.build(
                client, vocab_list=state.vocab_list, language=language, level=level,
                niveau=niveau, model=model,
            )
        else:
            status.update(label="—", state="error")
            return
        state.task = instr.displayed_to_user
        state.user_text = ""  # reset input for new task
        state.num_tasks_generated = getattr(state, "num_tasks_generated", 0) + 1
        status.update(label="✅ Aufgabe bereit", state="complete")


@st.fragment
def _correction_panel(
    client: openai.OpenAI, language: str, niveau: str, mentor: str, model: str,
) -> None:
    """Isolated fragment — reruns only this panel on correction-button click."""
    state = st.session_state["state"]
    if not state.task:
        return

    st.markdown("### Aufgabe")
    st.markdown(state.task)

    user_text = st.text_area(
        "✏️ Deine Antwort:",
        value=state.user_text,
        height=140,
        key="user_text_area",
        placeholder=f"Schreib auf {language.capitalize()}… Meta-Fragen in <> einbetten.",
    )

    if st.button("📝 Text korrigieren", type="primary", use_container_width=True):
        state.user_text = user_text
        with st.status(f"🧠 {mentor} liest mit…", expanded=False) as status:
            cleaned, comments = extract_comments(user_text)
            corrected = correct_text(
                client, task=state.task, user_text=cleaned, language=language,
                niveau=niveau, mentor=mentor, model=model,
            )
            comment_answers = [
                (c, answer_comment(client, comment=c, model=model)) for c in comments
            ]
            state.num_corrections = getattr(state, "num_corrections", 0) + 1
            status.update(label="✅ Feedback bereit", state="complete")

        avatar = MENTOR_AVATARS.get(mentor, "🎓")
        with st.chat_message(name=mentor, avatar=avatar):
            st.markdown(corrected)
            if comment_answers:
                st.divider()
                st.caption("**Nebenfragen:**")
                for q, a in comment_answers:
                    st.markdown(f"❓ *{q}*\n\n> {a}")


def main() -> None:
    args = _parse_args()
    language = args.language

    init_session_state(st.session_state)
    state = st.session_state["state"]
    # Add polish-state fields on-the-fly (backward compat with old SessionState)
    for attr, default in [
        ("num_tasks_generated", 0),
        ("num_corrections", 0),
        ("number_trous", 4),
        ("number_sentences", 1),
        ("file_path_extract_trigger", None),
        ("uploaded_vocab_file_trigger", None),
        ("url_extract_trigger", ""),
    ]:
        if not hasattr(state, attr):
            setattr(state, attr, default)

    mentor, level, niveau, model = _render_sidebar(language)
    _render_header(language, mentor)

    key, source = _resolve_api_key()
    if not key:
        st.error("🔑 Kein API-Key. Gib deinen OpenRouter-Key in der Sidebar ein.")
        st.info("💡 Holst du auf https://openrouter.ai/keys — Key bleibt nur in deiner Session.")
        st.stop()
    client = _build_client(key, source)

    log.info("Run %s — model=%s language=%s source=%s", state.num_runs, model, language, source)

    _handle_vocab_sources(client, language, level, model)

    st.divider()
    task_type = st.selectbox("🎯 Übung wählen", TASK_LIST, key="task_type_sel")

    vocab_missing = not state.vocab_list
    needs_vocab = task_type not in ("", "Schreiben eines Textes und danach Korrektur")
    if vocab_missing and needs_vocab:
        st.info("Keine Vokabeln geladen. Lade eine Quelle oben oder:")
        if st.button("🎲 Vokabelliste automatisch generieren", type="primary"):
            with st.status("🧠 Generiere Vokabeln…", expanded=False) as status:
                state.vocab_list = generate_vocabulary_via_function_call(
                    client, language=language, level=level, niveau=niveau, model=model,
                )
                state.auto_gen_vocabs = True
                status.update(label=f"✅ {len(state.vocab_list)} Vokabeln generiert", state="complete")
            st.rerun()
        return

    # Task-specific input widgets + generation trigger
    if task_type == "Ausfüllen eines Lückentextes in Fremdsprache":
        state.number_trous = st.number_input(
            "Wortlücken", min_value=3, max_value=20, value=state.number_trous,
        )
    elif task_type == "Vorgabe von deutschen Sätzen zum Übersetzen":
        state.number_sentences = st.number_input(
            "Sätze", min_value=1, max_value=20, value=state.number_sentences,
        )

    if task_type == "Vokabel-Quiz":
        _render_quiz(client, language, model)
    elif task_type == RADIO_TASK_NAME:
        _render_radio()
    elif task_type:
        col_gen, col_new = st.columns([1, 1])
        if col_gen.button("🎯 Neue Aufgabe", type="primary", use_container_width=True) or not state.task:
            _generate_task(task_type, client, language, level, niveau, model)

        _correction_panel(client, language, niveau, mentor, model)


def _render_quiz(client: openai.OpenAI, language: str, model: str) -> None:
    state = st.session_state["state"]
    if st.button("🎲 Neues Quiz", type="primary") or "current_quiz" not in st.session_state:
        with st.status("🧠 Generiere Quiz…", expanded=False) as status:
            st.session_state["current_quiz"] = quiz_task.build_quiz(
                client, vocab_list=state.vocab_list, language=language, count=5, model=model,
            )
            st.session_state["quiz_answers"] = {}
            state.num_tasks_generated = getattr(state, "num_tasks_generated", 0) + 1
            status.update(label="✅ Quiz bereit", state="complete")
    quiz = st.session_state.get("current_quiz", {})
    for fw, trans in quiz.items():
        st.session_state["quiz_answers"][fw] = st.text_input(
            f"🇩🇪 → 🇫🇷 '{trans}'",
            key=f"quiz_{fw}",
        )
    if quiz and st.button("✅ Auswerten", type="primary"):
        result = quiz_task.score_answers(quiz, st.session_state["quiz_answers"])
        st.metric("🎯 Score", f"{result.correct} / {result.total}")
        for word, ok in result.per_word.items():
            st.write(f"- {word}: {'✅' if ok else '❌'}")


def _render_radio() -> None:
    if not is_audio_available():
        st.warning("🔇 Audio-Output nicht verfügbar (headless-Server). Radio-Task funktioniert nur lokal.")
        return
    channels = get_channels()
    channel = st.selectbox("📻 Kanal", list(channels.keys()))
    st.info("Streaming-Kern in `src/tasks/radio.py`. Transkription folgt (Roadmap).")
    st.code(channels[channel], language=None)


if __name__ == "__main__":
    main()
