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
    THEMES,
    default_model_for_language,
)
from src.i18n import (  # noqa: E402
    DEFAULT_UI_LANG,
    TASK_KEYS,
    UI_LANG_NAMES,
    UI_LANGS,
    detect_ui_language,
    t,
    task_names_for,
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


_DARK_CSS = """
<style>
    /* Outer containers */
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stApp"] {
        background-color: #0F172A !important;
        color: #E5E7EB !important;
    }
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarHeader"] {
        background-color: #1E293B !important;
    }

    /* Text everywhere */
    [data-testid="stSidebar"] *,
    [data-testid="stAppViewContainer"] * {
        color: #E5E7EB !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {
        color: #E5E7EB !important;
    }

    /* Form controls — Streamlit's BaseWeb needs nested-div overrides */
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div,
    [data-baseweb="base-input"],
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input {
        background-color: #1E293B !important;
        color: #E5E7EB !important;
        border-color: #334155 !important;
    }
    /* Select dropdown menu */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [data-baseweb="list"] {
        background-color: #1E293B !important;
    }
    [data-baseweb="list"] li {
        color: #E5E7EB !important;
    }
    [data-baseweb="list"] li:hover {
        background-color: #334155 !important;
    }

    /* Chat message + expander + status + alerts */
    [data-testid="stChatMessage"] {
        background-color: #1E293B !important;
    }
    [data-testid="stExpander"],
    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
    }
    /* Expander header text — must be explicitly brightened */
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary *,
    [data-testid="stExpander"] details > summary,
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"],
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
        color: #F3F4F6 !important;
        opacity: 1 !important;
        font-weight: 500;
    }
    [data-testid="stStatusWidget"],
    [data-testid="stAlert"],
    [data-testid="stNotification"] {
        background-color: #1E293B !important;
        color: #E5E7EB !important;
    }

    /* File uploader drop zone */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #1E293B !important;
        border: 1px dashed #334155 !important;
    }

    /* Buttons */
    button[kind="primary"], button[kind="primaryFormSubmit"] {
        background-color: #4F46E5 !important;
        border-color: #4F46E5 !important;
        color: #FFFFFF !important;
    }
    button[kind="secondary"], button:not([kind]) {
        background-color: #334155 !important;
        color: #E5E7EB !important;
        border: 1px solid #475569 !important;
    }

    /* Misc */
    hr { border-color: #334155 !important; }
    code { background-color: #0F172A !important; color: #FCD34D !important; }
    [data-testid="stToggle"] label { color: #E5E7EB !important; }
</style>
"""


def _apply_theme() -> None:
    """Inject dark-mode CSS if user toggled it."""
    if st.session_state.get("dark_mode", False):
        st.markdown(_DARK_CSS, unsafe_allow_html=True)


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


def _detect_initial_ui_lang() -> str:
    """Once per session: sniff X-Forwarded-For + Accept-Language."""
    if "ui_lang_detected" in st.session_state:
        return st.session_state["ui_lang_detected"]
    try:
        headers = st.context.headers  # Streamlit ≥ 1.37
    except Exception:
        headers = {}
    xff = headers.get("X-Forwarded-For") or headers.get("x-forwarded-for")
    al = headers.get("Accept-Language") or headers.get("accept-language")
    detected = detect_ui_language(x_forwarded_for=xff, accept_language=al)
    st.session_state["ui_lang_detected"] = detected
    return detected


def _render_sidebar(language: str, ui_lang: str) -> tuple[str, str, str, str]:
    """Render sidebar and return (mentor, level, niveau, model)."""
    state = st.session_state["state"]

    with st.sidebar:
        # Interface-language first — everything below respects it on rerun.
        lang_labels = list(UI_LANGS.keys())
        current_label = UI_LANG_NAMES.get(ui_lang, "English")
        st.selectbox(
            t("ui_language", ui_lang),
            lang_labels,
            index=lang_labels.index(current_label),
            key="ui_lang_label",
        )

        st.markdown(f"### {t('sidebar_title', ui_lang, language=language.capitalize())}")

        st.toggle(t("dark_mode", ui_lang), value=st.session_state.get("dark_mode", False), key="dark_mode")

        with st.expander(t("coach_and_style", ui_lang), expanded=True):
            mentor = st.selectbox(t("coach", ui_lang), MENTORS, index=0, key="mentor")
            level = st.selectbox(t("level", ui_lang), LEVELS, index=2, key="level")
            niveau = st.selectbox(t("register", ui_lang), NIVEAU_LEVELS, index=3, key="niveau")

        with st.expander(t("vocab_source", ui_lang), expanded=True):
            extract_files = st.file_uploader(
                t("txt_files", ui_lang),
                accept_multiple_files=True,
                type=["txt"],
                help=t("txt_files_help", ui_lang),
            )
            number_of_words = st.number_input(
                t("num_vocab", ui_lang), min_value=1, max_value=200, value=state.number_of_words,
                key="number_of_words",
            )
            url_extract = st.text_input(t("webpage_url", ui_lang), placeholder="https://...")
            uploaded_vocab = st.file_uploader(t("ready_vocab_file", ui_lang), type=["txt"])

        with st.expander(t("model_api", ui_lang), expanded=False):
            api_key_input = st.text_input(
                t("api_key", ui_lang),
                type="password",
                value=st.session_state.get("byok_key", ""),
                help=t("api_key_help", ui_lang),
                placeholder="sk-or-...",
            )
            if api_key_input != st.session_state.get("byok_key", ""):
                st.session_state["byok_key"] = api_key_input

            _default_model = default_model_for_language(language)
            tier_labels = list(MODEL_TIERS.keys())
            default_idx = next(
                (i for i, lb in enumerate(tier_labels) if MODEL_TIERS[lb] == _default_model), 0,
            )
            tier = st.selectbox(t("model_tier", ui_lang), tier_labels, index=default_idx, key="tier")
            model = MODEL_TIERS[tier]
            st.caption(f"`{model}`")

        _, source = _resolve_api_key()
        source_keys = {
            "byok": "key_source_byok",
            "openrouter": "key_source_or",
            "openai": "key_source_oa",
            "none": "key_source_none",
        }
        st.caption(f"{t('key_source_label', ui_lang)}: {t(source_keys[source], ui_lang)}")

    state.file_path_extract_trigger = extract_files
    state.uploaded_vocab_file_trigger = uploaded_vocab
    state.url_extract_trigger = url_extract
    state.number_of_words = number_of_words

    return mentor, level, niveau, model


def _handle_vocab_sources(
    client: openai.OpenAI, language: str, level: str, model: str, ui_lang: str,
) -> None:
    """Process the three possible vocab sources. Writes to state.vocab_list."""
    state = st.session_state["state"]
    extract_files = state.file_path_extract_trigger
    url_extract = state.url_extract_trigger
    uploaded_vocab = state.uploaded_vocab_file_trigger
    number = state.number_of_words

    if extract_files and extract_files != state.file_path_extract:
        all_text = "\n".join(f.read().decode("utf-8") for f in extract_files)
        with st.status(t("status_extract_file", ui_lang), expanded=False) as status:
            state.vocab_list = _cached_extract_from_text(
                all_text, language, level, number, model,
            )
            status.update(label=t("status_extracted_ok", ui_lang, n=len(state.vocab_list)), state="complete")
        st.sidebar.write(sorted(state.vocab_list))
        state.file_path_extract = extract_files
    elif url_extract and url_extract != state.html_path_extract:
        with st.status(t("status_load_url", ui_lang, url=url_extract), expanded=False) as status:
            article = fetch_article_text(url_extract)
            status.update(label=t("status_extract_web", ui_lang))
            state.vocab_list = _cached_extract_from_text(
                article, language, level, number, model,
            )
            status.update(
                label=t("status_extract_web_ok", ui_lang, n=len(state.vocab_list)),
                state="complete",
            )
        st.sidebar.write(sorted(state.vocab_list))
        state.html_path_extract = url_extract
    elif uploaded_vocab and uploaded_vocab != state.uploaded_vocab_file:
        content = uploaded_vocab.read().decode("utf-8")
        state.vocab_list = [line.strip() for line in content.splitlines() if line.strip()]
        st.sidebar.success(t("vocab_loaded_ok", ui_lang, n=len(state.vocab_list)))
        state.uploaded_vocab_file = uploaded_vocab


def _render_header(language: str, mentor: str, ui_lang: str) -> None:
    """Title + session metrics + mentor quote."""
    state = st.session_state["state"]

    st.markdown(f"# {t('app_title', ui_lang, language=language.capitalize())}")

    quote = MENTOR_QUOTES.get(mentor, "")
    avatar = MENTOR_AVATARS.get(mentor, "🎓")
    if quote:
        st.caption(f'{avatar} *{mentor}:* „{quote}"')

    col1, col2, col3 = st.columns(3)
    col1.metric(t("metric_tasks", ui_lang), getattr(state, "num_tasks_generated", 0))
    col2.metric(t("metric_corrections", ui_lang), getattr(state, "num_corrections", 0))
    col3.metric(t("metric_runs", ui_lang), state.num_runs)

    st.caption(t("meta_hint", ui_lang))


def _generate_task(
    task_key: str, task_label: str, client: openai.OpenAI,
    language: str, level: str, niveau: str, model: str, ui_lang: str,
) -> None:
    """Build a task into state.task. Dispatches on language-independent task key."""
    state = st.session_state["state"]

    with st.status(t("status_generating_task", ui_lang, task=task_label), expanded=False) as status:
        if task_key == "writing":
            instr = write_task.build(themes=THEMES, previous_theme=state.theme)
            state.theme = instr.internal_context["theme"]
        elif task_key == "cloze":
            instr = cloze_task.build(
                client, vocab_list=state.vocab_list, language=language, level=level,
                niveau=niveau, number_trous=state.number_trous, model=model,
            )
        elif task_key == "translation":
            instr = trans_task.build(
                client, vocab_list=state.vocab_list, language=language, level=level,
                niveau=niveau, number_sentences=state.number_sentences, model=model,
            )
        elif task_key == "sentence":
            instr = sent_task.build(
                client, vocab_list=state.vocab_list, language=language, level=level,
                niveau=niveau, model=model,
            )
        elif task_key == "error":
            instr = err_task.build(
                client, vocab_list=state.vocab_list, language=language, level=level,
                niveau=niveau, model=model,
            )
        elif task_key == "synonym":
            instr = syn_task.build(vocab_list=state.vocab_list)
        elif task_key == "conjugation":
            instr = conj_task.build(
                client, vocab_list=state.vocab_list, language=language, level=level,
                niveau=niveau, model=model,
            )
        else:
            status.update(label="—", state="error")
            return
        state.task = instr.displayed_to_user
        state.user_text = ""
        state.num_tasks_generated = getattr(state, "num_tasks_generated", 0) + 1
        status.update(label=t("status_task_ready", ui_lang), state="complete")


@st.fragment
def _correction_panel(
    client: openai.OpenAI, language: str, niveau: str, mentor: str, model: str, ui_lang: str,
) -> None:
    """Isolated fragment — reruns only this panel on correction-button click."""
    state = st.session_state["state"]
    if not state.task:
        return

    st.markdown(f"### {t('task_heading', ui_lang)}")
    st.markdown(state.task)

    user_text = st.text_area(
        t("your_answer", ui_lang),
        value=state.user_text,
        height=140,
        key="user_text_area",
        placeholder=t("your_answer_placeholder", ui_lang, language=language.capitalize()),
    )

    if st.button(t("correct_btn", ui_lang), type="primary", use_container_width=True):
        state.user_text = user_text
        ui_lang_name = UI_LANG_NAMES.get(ui_lang, "English")
        with st.status(t("status_coach_reading", ui_lang, mentor=mentor), expanded=False) as status:
            cleaned, comments = extract_comments(user_text)
            corrected = correct_text(
                client, task=state.task, user_text=cleaned, language=language,
                niveau=niveau, mentor=mentor, model=model, ui_language_name=ui_lang_name,
            )
            comment_answers = [
                (c, answer_comment(client, comment=c, model=model)) for c in comments
            ]
            state.num_corrections = getattr(state, "num_corrections", 0) + 1
            status.update(label=t("status_feedback_ready", ui_lang), state="complete")

        avatar = MENTOR_AVATARS.get(mentor, "🎓")
        with st.chat_message(name=mentor, avatar=avatar):
            st.markdown(corrected)
            if comment_answers:
                st.divider()
                st.caption(t("side_questions", ui_lang))
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

    # UI-language: detect once, user can override via dropdown which writes ui_lang_label
    detected = _detect_initial_ui_lang()
    # If user selected a label, use it; otherwise fall back to detected.
    selected_label = st.session_state.get("ui_lang_label")
    if selected_label and selected_label in UI_LANGS:
        ui_lang = UI_LANGS[selected_label]
    else:
        ui_lang = detected

    mentor, level, niveau, model = _render_sidebar(language, ui_lang)
    # If user just changed the dropdown, ui_lang below reflects new choice
    ui_lang = UI_LANGS.get(st.session_state.get("ui_lang_label", ""), ui_lang)

    _apply_theme()
    _render_header(language, mentor, ui_lang)

    key, source = _resolve_api_key()
    if not key:
        st.error(t("error_no_key", ui_lang))
        st.info(t("error_no_key_hint", ui_lang))
        st.stop()
    client = _build_client(key, source)

    log.info("Run %s — model=%s language=%s ui=%s source=%s",
             state.num_runs, model, language, ui_lang, source)

    _handle_vocab_sources(client, language, level, model, ui_lang)

    st.divider()
    task_names = task_names_for(ui_lang)
    task_label = st.selectbox(t("choose_exercise", ui_lang), task_names, key="task_type_sel")
    task_idx = task_names.index(task_label) if task_label in task_names else 0
    task_key = TASK_KEYS[task_idx]

    vocab_missing = not state.vocab_list
    needs_vocab = task_key not in ("", "writing")
    if vocab_missing and needs_vocab:
        st.info(t("no_vocab_info", ui_lang))
        if st.button(t("autogen_vocab_btn", ui_lang), type="primary"):
            with st.status(t("status_generating_vocab", ui_lang), expanded=False) as status:
                state.vocab_list = generate_vocabulary_via_function_call(
                    client, language=language, level=level, niveau=niveau, model=model,
                )
                state.auto_gen_vocabs = True
                status.update(
                    label=t("status_gen_vocab_ok", ui_lang, n=len(state.vocab_list)),
                    state="complete",
                )
            st.rerun()
        return

    # Task-specific input widgets
    if task_key == "cloze":
        state.number_trous = st.number_input(
            t("num_blanks", ui_lang), min_value=3, max_value=20, value=state.number_trous,
        )
    elif task_key == "translation":
        state.number_sentences = st.number_input(
            t("num_sentences", ui_lang), min_value=1, max_value=20, value=state.number_sentences,
        )

    if task_key == "quiz":
        _render_quiz(client, language, model, ui_lang)
    elif task_key == "radio":
        _render_radio(ui_lang)
    elif task_key:
        if st.button(t("new_task_btn", ui_lang), type="primary", use_container_width=True) or not state.task:
            _generate_task(task_key, task_label, client, language, level, niveau, model, ui_lang)

        _correction_panel(client, language, niveau, mentor, model, ui_lang)


def _render_quiz(client: openai.OpenAI, language: str, model: str, ui_lang: str) -> None:
    state = st.session_state["state"]
    if st.button(t("quiz_new_btn", ui_lang), type="primary") or "current_quiz" not in st.session_state:
        with st.status(t("status_generating_quiz", ui_lang), expanded=False) as status:
            st.session_state["current_quiz"] = quiz_task.build_quiz(
                client, vocab_list=state.vocab_list, language=language, count=5, model=model,
            )
            st.session_state["quiz_answers"] = {}
            state.num_tasks_generated = getattr(state, "num_tasks_generated", 0) + 1
            status.update(label=t("status_quiz_ready", ui_lang), state="complete")
    quiz = st.session_state.get("current_quiz", {})
    for fw, trans in quiz.items():
        st.session_state["quiz_answers"][fw] = st.text_input(
            t("quiz_prompt_format", ui_lang, language=language, trans=trans),
            key=f"quiz_{fw}",
        )
    if quiz and st.button(t("quiz_evaluate_btn", ui_lang), type="primary"):
        result = quiz_task.score_answers(quiz, st.session_state["quiz_answers"])
        st.metric(t("quiz_score", ui_lang), f"{result.correct} / {result.total}")
        for word, ok in result.per_word.items():
            st.write(f"- {word}: {'✅' if ok else '❌'}")


def _render_radio(ui_lang: str) -> None:
    if not is_audio_available():
        st.warning(t("radio_unavailable", ui_lang))
        return
    channels = get_channels()
    channel = st.selectbox(t("radio_channel", ui_lang), list(channels.keys()))
    st.info(t("radio_info", ui_lang))
    st.code(channels[channel], language=None)


if __name__ == "__main__":
    main()
