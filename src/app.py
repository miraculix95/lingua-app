"""Streamlit entrypoint for lingua-app.

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
    RTL_LANGUAGES,
    THEMES,
    default_model_for_language,
)
from src.i18n import (  # noqa: E402
    DEFAULT_UI_LANG,
    TASK_KEYS,
    UI_LANG_NAMES,
    UI_LANGS,
    detect_ui_language,
    language_display,
    language_to_english,
    mentor_display,
    niveau_display,
    quote_for,
    t,
    task_names_for,
    tier_display,
)
from src.correction import answer_comment, correct_text, extract_comments  # noqa: E402
from src.logging_setup import get_logger  # noqa: E402
from src.state import init_session_state  # noqa: E402
from src.tasks import cloze as cloze_task  # noqa: E402
from src.tasks import conjugation as conj_task  # noqa: E402
from src.tasks import dictation as dict_task  # noqa: E402
from src.tasks import error_detection as err_task  # noqa: E402
from src.tasks import quiz as quiz_task  # noqa: E402
from src.tasks import reading as reading_task  # noqa: E402
from src.tasks import sentence_building as sent_task  # noqa: E402
from src.tasks import synonym_antonym as syn_task  # noqa: E402
from src.tasks import translation as trans_task  # noqa: E402
from src.tasks import writing as write_task  # noqa: E402
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


_LIGHT_CSS = """
<style>
    /* Light-mode palette: Streamlit's default white is too glaring.
       Main area = neutral-100 (#F3F4F6), sidebar = neutral-200 (#E5E7EB),
       cards/inputs stay white for subtle contrast. */
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    [data-testid="stHeader"] {
        background-color: #F3F4F6 !important;
    }
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarHeader"] {
        background-color: #E5E7EB !important;
    }
    .block-container {
        background-color: #F3F4F6 !important;
    }
    /* Expanders / chat bubbles / alerts stay white so they pop against the grey bg. */
    [data-testid="stExpander"],
    [data-testid="stChatMessage"],
    [data-testid="stAlert"],
    [data-testid="stNotification"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
    }
</style>
"""


_MOBILE_CSS = """
<style>
    /* ≤ 640px: shrink hero + metrics so first viewport isn't 80% headline */
    @media (max-width: 640px) {
        h1 {
            font-size: 1.6rem !important;
            line-height: 1.15 !important;
            margin-bottom: 0.25rem !important;
        }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.05rem !important; }
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
            line-height: 1.2 !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }
        /* Metric grid tweaks — allow wrap if labels don't fit, but tighter gap */
        [data-testid="stHorizontalBlock"] {
            gap: 0.25rem !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            min-width: 0 !important;
        }
        /* Main container: tighter padding */
        .block-container {
            padding-top: 1rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }
        /* Meta-hint caption: smaller font so it fits on 1–2 lines */
        [data-testid="stCaptionContainer"] {
            font-size: 0.75rem !important;
        }
    }
</style>
"""


_RTL_CSS = """
<style>
    /* RTL for main content when target language is Hebrew etc. Sidebar stays LTR. */
    .block-container [data-testid="stChatMessage"],
    .block-container [data-testid="stMarkdown"],
    .block-container [data-testid="stTextArea"] textarea,
    .block-container [data-testid="stTextInput"] input {
        direction: rtl;
        text-align: right;
    }
    /* Keep headings, buttons, selectboxes LTR-looking (they're UI, not content) */
    .block-container h1,
    .block-container h2,
    .block-container h3,
    .block-container [data-testid="stCaptionContainer"],
    .block-container button,
    .block-container [data-baseweb="select"] {
        direction: ltr;
        text-align: left;
    }
</style>
"""


_UI_RTL_CSS = """
<style>
    /* UI-level RTL: when the interface language itself is RTL (e.g. Hebrew),
       flip the whole app including sidebar, headings and widgets. */
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] *,
    .block-container,
    .block-container * {
        direction: rtl;
        text-align: right;
    }
    /* Re-LTR for code + inline monospace and URLs (they must stay LTR regardless). */
    code, pre, kbd, samp, .stCode, [data-testid="stCodeBlock"] {
        direction: ltr !important;
        text-align: left !important;
        unicode-bidi: embed;
    }
</style>
"""


def _apply_theme(learning_language: str = "", ui_lang: str = "en") -> None:
    """Inject dark-mode + mobile-responsive CSS. Adds RTL CSS for Hebrew etc.

    RTL is applied in two layers:
    - content RTL when the *learning* language is RTL (Hebrew output in main area)
    - full UI RTL when the *interface* language itself is RTL
    """
    st.markdown(_MOBILE_CSS, unsafe_allow_html=True)
    # Default True — matches the sidebar toggle's initial value on main page.
    if st.session_state.get("dark_mode", True):
        st.markdown(_DARK_CSS, unsafe_allow_html=True)
    else:
        # Dial down Streamlit's stock white — users have complained it's glaring.
        st.markdown(_LIGHT_CSS, unsafe_allow_html=True)
    if ui_lang == "he":
        st.markdown(_UI_RTL_CSS, unsafe_allow_html=True)
    elif learning_language in RTL_LANGUAGES:
        st.markdown(_RTL_CSS, unsafe_allow_html=True)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="lingua-app Streamlit app")
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


def _resolve_elevenlabs_key() -> tuple[str | None, str]:
    """BYOK priority for ElevenLabs: session-state > ELEVENLABS_KEY env.

    Returns (key, source_label). source_label ∈ {"byok", "env", "none"}.
    """
    load_dotenv(find_dotenv(usecwd=True))
    byok = st.session_state.get("byok_elevenlabs_key", "").strip()
    if byok:
        return byok, "byok"
    env = os.environ.get("ELEVENLABS_KEY", "").strip()
    if env:
        return env, "env"
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


def _render_sidebar(language: str, ui_lang: str) -> tuple[str, str, str, str, str]:
    """Render sidebar and return (mentor, level, niveau, model, learning_language)."""
    state = st.session_state["state"]

    with st.sidebar:
        # Clear panel label — users don't always realise the left strip is the settings panel.
        st.markdown(f"## {t('sidebar_heading', ui_lang)}")

        # Dark mode first — users can switch theme before any other widget loads.
        # Default ON (Bastian's pref); toggle persists once touched.
        st.toggle(t("dark_mode", ui_lang), value=st.session_state.get("dark_mode", True), key="dark_mode")

        # Interface-language — everything below respects it on rerun.
        lang_labels = list(UI_LANGS.keys())
        current_label = UI_LANG_NAMES.get(ui_lang, "English")
        st.selectbox(
            t("ui_language", ui_lang),
            lang_labels,
            index=lang_labels.index(current_label),
            key="ui_lang_label",
            help=t("help_ui_language", ui_lang),
        )
        # Mirror to a non-widget key so /about (which doesn't render this widget)
        # can still see the chosen UI language. Streamlit garbage-collects widget
        # state for widgets not rendered in the current script run.
        st.session_state["_ui_lang_persisted"] = st.session_state.get("ui_lang_label", "")

        # Learning language — user can switch the target without restarting.
        learn_displays = [language_display(k, ui_lang).capitalize() for k in LANGUAGES]
        current_learn_idx = LANGUAGES.index(language) if language in LANGUAGES else 0
        picked_learn_display = st.selectbox(
            t("learning_language", ui_lang),
            learn_displays,
            index=current_learn_idx,
            key="learning_lang_display",
            help=t("help_learning_language", ui_lang),
        )
        # Resolve picked display back to internal key and persist.
        picked_learn_key = LANGUAGES[learn_displays.index(picked_learn_display)]
        if picked_learn_key != state.learning_language:
            state.learning_language = picked_learn_key
            # Clear vocab/task state when switching — old French vocabs are useless for Spanish.
            state.vocab_list = []
            state.task = ""
            state.auto_gen_vocabs = False
            # Also bust task-specific caches: their payload (audio, quiz, passage) is
            # baked in the previous learning language and must not leak across a switch.
            for cache_key in (
                "dictation_bytes", "dictation_text", "dictation_revealed", "dictation_history",
                "current_quiz", "quiz_answers",
                "reading_passage", "reading_questions", "reading_mc_choices",
                "reading_open_answers", "reading_results", "reading_reveal",
            ):
                st.session_state.pop(cache_key, None)
            st.rerun()

        language_localized = language_display(picked_learn_key, ui_lang)
        st.markdown(f"### {t('sidebar_title', ui_lang, language=language_localized)}")

        with st.expander(t("setup_guide_title", ui_lang), expanded=False):
            st.markdown(t("setup_guide_body", ui_lang))

        with st.expander(t("coach_and_style", ui_lang), expanded=True):
            # Mentor: show translated label, store original key internally
            mentor_displays = [mentor_display(m, ui_lang) for m in MENTORS]
            mentor_pick = st.selectbox(
                t("coach", ui_lang), mentor_displays, index=0, key="mentor_display",
                help=t("help_coach", ui_lang),
            )
            mentor = MENTORS[mentor_displays.index(mentor_pick)]

            level = st.selectbox(
                t("level", ui_lang), LEVELS, index=2, key="level",
                help=t("help_level", ui_lang),
            )

            niveau_displays = [niveau_display(n, ui_lang) for n in NIVEAU_LEVELS]
            niveau_pick = st.selectbox(
                t("register", ui_lang), niveau_displays, index=3, key="niveau_display",
                help=t("help_register", ui_lang),
            )
            niveau = NIVEAU_LEVELS[niveau_displays.index(niveau_pick)]

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
                help=t("help_num_vocab", ui_lang),
            )
            url_extract = st.text_input(
                t("webpage_url", ui_lang), placeholder="https://...",
                help=t("help_url", ui_lang),
            )
            uploaded_vocab = st.file_uploader(
                t("ready_vocab_file", ui_lang), type=["txt"],
                help=t("help_ready_vocab", ui_lang),
            )

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

            # Optional: ElevenLabs BYOK for dictation TTS.
            el_key_input = st.text_input(
                t("elevenlabs_key", ui_lang),
                type="password",
                value=st.session_state.get("byok_elevenlabs_key", ""),
                help=t("elevenlabs_key_help", ui_lang),
                placeholder="xi-...",
            )
            if el_key_input != st.session_state.get("byok_elevenlabs_key", ""):
                st.session_state["byok_elevenlabs_key"] = el_key_input

            _default_model = default_model_for_language(language)
            tier_keys = list(MODEL_TIERS.keys())
            tier_displays = [tier_display(k, ui_lang) for k in tier_keys]
            default_idx = next(
                (i for i, k in enumerate(tier_keys) if MODEL_TIERS[k] == _default_model), 0,
            )
            tier_pick = st.selectbox(
                t("model_tier", ui_lang), tier_displays, index=default_idx, key="tier_display",
                help=t("help_model_tier", ui_lang),
            )
            tier_key = tier_keys[tier_displays.index(tier_pick)]
            model = MODEL_TIERS[tier_key]
            st.caption(f"`{model}`")

        _, source = _resolve_api_key()
        source_keys = {
            "byok": "key_source_byok",
            "openrouter": "key_source_or",
            "openai": "key_source_oa",
            "none": "key_source_none",
        }
        st.caption(f"{t('key_source_label', ui_lang)}: {t(source_keys[source], ui_lang)}")

        # Current vocabulary — always visible so the learner can see what's in play.
        n_vocab = len(state.vocab_list)
        expand = n_vocab > 0 and n_vocab <= 60
        with st.expander(t("current_vocabs", ui_lang, n=n_vocab), expanded=expand):
            if n_vocab == 0:
                st.markdown(t("no_vocabs_yet", ui_lang))
            else:
                st.markdown("\n".join(f"- {w}" for w in sorted(state.vocab_list, key=str.lower)))

    state.file_path_extract_trigger = extract_files
    state.uploaded_vocab_file_trigger = uploaded_vocab
    state.url_extract_trigger = url_extract
    state.number_of_words = number_of_words

    # Secondary cache-bust: any of (level, niveau, mentor) changed since last render →
    # nuke task-render caches (dictation audio, quiz, reading passage/questions, current
    # task text). Vocab stays — user may want the same words at a new level/register.
    # Language change is handled earlier with its own vocab-reset + st.rerun().
    current_secondary = (level, niveau, mentor)
    last_secondary = st.session_state.get("_last_secondary_params")
    if last_secondary is not None and last_secondary != current_secondary:
        for cache_key in (
            "dictation_bytes", "dictation_text", "dictation_revealed", "dictation_history",
            "current_quiz", "quiz_answers",
            "reading_passage", "reading_questions", "reading_mc_choices",
            "reading_open_answers", "reading_results", "reading_reveal",
        ):
            st.session_state.pop(cache_key, None)
        state.task = ""
    st.session_state["_last_secondary_params"] = current_secondary

    return mentor, level, niveau, model, picked_learn_key


def _handle_vocab_sources(
    client: openai.OpenAI, language: str, level: str, model: str, ui_lang: str,
) -> None:
    """Process the three possible vocab sources. Writes to state.vocab_list."""
    state = st.session_state["state"]
    extract_files = state.file_path_extract_trigger
    url_extract = state.url_extract_trigger
    uploaded_vocab = state.uploaded_vocab_file_trigger
    number = state.number_of_words

    lang_en = language_to_english(language)
    if extract_files and extract_files != state.file_path_extract:
        all_text = "\n".join(f.read().decode("utf-8") for f in extract_files)
        with st.status(t("status_extract_file", ui_lang), expanded=False) as status:
            state.vocab_list = _cached_extract_from_text(
                all_text, lang_en, level, number, model,
            )
            status.update(label=t("status_extracted_ok", ui_lang, n=len(state.vocab_list)), state="complete")
        # Vocab list rendered by sidebar's "current vocabs" expander — no duplicate here.
        state.file_path_extract = extract_files
    elif url_extract and url_extract != state.html_path_extract:
        with st.status(t("status_load_url", ui_lang, url=url_extract), expanded=False) as status:
            article = fetch_article_text(url_extract)
            status.update(label=t("status_extract_web", ui_lang))
            state.vocab_list = _cached_extract_from_text(
                article, lang_en, level, number, model,
            )
            status.update(
                label=t("status_extract_web_ok", ui_lang, n=len(state.vocab_list)),
                state="complete",
            )
        state.html_path_extract = url_extract
    elif uploaded_vocab and uploaded_vocab != state.uploaded_vocab_file:
        content = uploaded_vocab.read().decode("utf-8")
        state.vocab_list = [line.strip() for line in content.splitlines() if line.strip()]
        st.sidebar.success(t("vocab_loaded_ok", ui_lang, n=len(state.vocab_list)))
        state.uploaded_vocab_file = uploaded_vocab


def _render_header(language: str, mentor: str, ui_lang: str) -> None:
    """Title + mentor quote + meta-hint."""
    language_localized = language_display(language, ui_lang)
    # French doesn't capitalize language names, but it looks cleaner in a title.
    st.markdown(f"# {t('app_title', ui_lang, language=language_localized[:1].upper() + language_localized[1:])}")

    quote = quote_for(mentor, ui_lang) or MENTOR_QUOTES.get(mentor, "")
    avatar = MENTOR_AVATARS.get(mentor, "🎓")
    mentor_localized = mentor_display(mentor, ui_lang)
    if quote:
        st.caption(f'{avatar} *{mentor_localized}:* „{quote}"')

    st.caption(t("meta_hint", ui_lang))


def _generate_task(
    task_key: str, task_label: str, client: openai.OpenAI,
    language: str, level: str, niveau: str, model: str, ui_lang: str,
) -> None:
    """Build a task into state.task. Dispatches on language-independent task key."""
    state = st.session_state["state"]
    lang_en = language_to_english(language)
    ui_lang_name = UI_LANG_NAMES.get(ui_lang, "English")

    with st.status(t("status_generating_task", ui_lang, task=task_label), expanded=False) as status:
        if task_key == "writing":
            instr = write_task.build(
                themes=THEMES, previous_theme=state.theme, ui_lang=ui_lang,
            )
            state.theme = instr.internal_context["theme"]
        elif task_key == "cloze":
            instr = cloze_task.build(
                client, vocab_list=state.vocab_list, language=lang_en, level=level,
                niveau=niveau, number_trous=state.number_trous, model=model,
                ui_lang=ui_lang, ui_language_name=ui_lang_name,
            )
        elif task_key == "translation":
            instr = trans_task.build(
                client, vocab_list=state.vocab_list, language=lang_en, level=level,
                niveau=niveau, number_sentences=state.number_sentences, model=model,
                ui_language_name=ui_lang_name,
                direction=getattr(state, "translation_direction", "to_learning"),
            )
        elif task_key == "sentence":
            instr = sent_task.build(
                client, vocab_list=state.vocab_list, language=lang_en, level=level,
                niveau=niveau, model=model, ui_lang=ui_lang,
            )
        elif task_key == "error":
            instr = err_task.build(
                client, vocab_list=state.vocab_list, language=lang_en, level=level,
                niveau=niveau, model=model, ui_lang=ui_lang,
            )
        elif task_key == "synonym":
            instr = syn_task.build(vocab_list=state.vocab_list, ui_lang=ui_lang)
        elif task_key == "conjugation":
            instr = conj_task.build(
                client, vocab_list=state.vocab_list, language=lang_en, level=level,
                niveau=niveau, model=model, ui_lang=ui_lang,
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

    if st.button(
        t("correct_btn", ui_lang), type="primary", use_container_width=True,
        help=t("help_correct", ui_lang),
    ):
        state.user_text = user_text
        ui_lang_name = UI_LANG_NAMES.get(ui_lang, "English")
        lang_en = language_to_english(language)
        mentor_loc = mentor_display(mentor, ui_lang)
        with st.status(t("status_coach_reading", ui_lang, mentor=mentor_loc), expanded=False) as status:
            cleaned, comments = extract_comments(user_text)
            corrected = correct_text(
                client, task=state.task, user_text=cleaned, language=lang_en,
                niveau=niveau, mentor=mentor_loc, model=model, ui_language_name=ui_lang_name,
            )
            comment_answers = [
                (c, answer_comment(client, comment=c, model=model)) for c in comments
            ]
            state.num_corrections = getattr(state, "num_corrections", 0) + 1
            status.update(label=t("status_feedback_ready", ui_lang), state="complete")

        avatar = MENTOR_AVATARS.get(mentor, "🎓")
        with st.chat_message(name=mentor_loc, avatar=avatar):
            st.markdown(corrected)
            if comment_answers:
                st.divider()
                st.caption(t("side_questions", ui_lang))
                for q, a in comment_answers:
                    st.markdown(f"❓ *{q}*\n\n> {a}")


def _resolve_ui_lang_for_nav() -> str:
    """Best effort UI-lang detection BEFORE the sidebar has rendered.

    Used by main() to build nav labels. Priority:
    1. ``ui_lang_label`` — the sidebar widget (present while the main page
       is the active route).
    2. ``_ui_lang_persisted`` — a plain mirror we maintain because Streamlit
       garbage-collects widget state for widgets that did not render on the
       current route. Without this mirror, navigating to `/about` would lose
       the user's language choice.
    3. Request-header detection (first-visit fallback).
    """
    selected_label = (
        st.session_state.get("ui_lang_label")
        or st.session_state.get("_ui_lang_persisted")
    )
    if selected_label and selected_label in UI_LANGS:
        return UI_LANGS[selected_label]
    return _detect_initial_ui_lang()


def main() -> None:
    """Streamlit entrypoint — builds the multipage navigation.

    The main-page nav label is localised to "← Back to app" (in the user's UI
    language) so the entry is self-explanatory when you're on the About page.
    """
    st.set_page_config(
        page_title="lingua",
        page_icon="🇫🇷",
        layout="centered",
        initial_sidebar_state="auto",
    )

    ui_lang = _resolve_ui_lang_for_nav()
    pages = [
        st.Page(
            _render_main_page,
            title=t("back_to_app", ui_lang),
            icon="⬅️",
            default=True,
            url_path="",
        ),
        st.Page(
            "pages/1_ℹ️_About.py",
            title=t("nav_about", ui_lang),
            icon="ℹ️",
            url_path="about",
        ),
    ]
    st.navigation(pages).run()


def _render_main_page() -> None:
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
        ("translation_direction", "to_learning"),
        ("file_path_extract_trigger", None),
        ("uploaded_vocab_file_trigger", None),
        ("url_extract_trigger", ""),
        # Learning language: initial seed from --language CLI; sidebar overrides.
        ("learning_language", args.language),
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

    mentor, level, niveau, model, learning_language = _render_sidebar(
        state.learning_language, ui_lang,
    )
    # Sidebar's learning-language pick is authoritative after this point.
    language = learning_language
    # If user just changed the UI-lang dropdown, reflect it immediately.
    ui_lang = UI_LANGS.get(st.session_state.get("ui_lang_label", ""), ui_lang)

    _apply_theme(language, ui_lang)
    _render_header(language, mentor, ui_lang)

    key, source = _resolve_api_key()
    if not key:
        st.error(t("error_no_key", ui_lang))
        st.info(t("error_no_key_hint", ui_lang))
        st.stop()
    client = _build_client(key, source)

    log.info("Run %s — model=%s language=%s ui=%s source=%s",
             state.num_runs, model, language, ui_lang, source)

    lang_en = language_to_english(language)
    _handle_vocab_sources(client, language, level, model, ui_lang)

    st.info(t("how_it_works", ui_lang), icon="🎓")
    st.divider()
    head_col, home_col = st.columns([4, 1])
    head_col.markdown(f"## {t('main_heading', ui_lang)}")
    if home_col.button(t("home_btn", ui_lang), help=t("help_home", ui_lang), key="home_btn"):
        _soft_reset_tasks(state)
        st.rerun()
    st.caption(t("practice_intro", ui_lang))
    task_names = task_names_for(ui_lang)

    # Pre-selection overview: expander with the full catalogue of types + their
    # descriptions, so a user can browse before committing.
    with st.expander(t("types_overview_title", ui_lang), expanded=False):
        for i, key in enumerate(TASK_KEYS):
            if not key:
                continue
            name = task_names[i]
            desc = t(f"desc_{key}", ui_lang)
            st.markdown(f"**{name}** — {desc}")

    task_label = st.selectbox(
        t("choose_exercise", ui_lang), task_names, key="task_type_sel",
        help=t("help_choose_exercise", ui_lang),
    )
    task_idx = task_names.index(task_label) if task_label in task_names else 0
    task_key = TASK_KEYS[task_idx]

    # Show a short description of the picked type before any widgets render.
    # Unknown/empty task_key has no desc_* key; t() falls back to the key itself,
    # so we gate it explicitly.
    if task_key:
        st.info(t(f"desc_{task_key}", ui_lang), icon="📘")

    vocab_missing = not state.vocab_list
    needs_vocab = task_key not in ("", "writing", "reading")
    if vocab_missing and needs_vocab:
        st.info(t("no_vocab_info", ui_lang))
        if st.button(t("autogen_vocab_btn", ui_lang), type="primary"):
            with st.status(t("status_generating_vocab", ui_lang), expanded=False) as status:
                state.vocab_list = generate_vocabulary_via_function_call(
                    client, language=lang_en, level=level, niveau=niveau, model=model,
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
            help=t("help_num_blanks", ui_lang),
        )
        st.caption(t("cloze_freeform_hint", ui_lang))
    elif task_key == "translation":
        col_n, col_dir = st.columns([1, 2])
        state.number_sentences = col_n.number_input(
            t("num_sentences", ui_lang), min_value=1, max_value=20, value=state.number_sentences,
            help=t("help_num_sentences", ui_lang),
        )
        ui_lang_name = UI_LANG_NAMES.get(ui_lang, "English")
        learning_localized = language_display(language, ui_lang)
        dir_labels = {
            "to_learning": t("dir_to_learning", ui_lang, learning=learning_localized),
            "to_native": t("dir_to_native", ui_lang, native=ui_lang_name),
        }
        pick = col_dir.radio(
            t("translation_direction", ui_lang),
            list(dir_labels.values()),
            index=0,
            horizontal=True,
            key="translation_direction",
        )
        # Map picked label back to internal key:
        state.translation_direction = next(k for k, v in dir_labels.items() if v == pick)

    if task_key == "quiz":
        _render_quiz(client, lang_en, model, ui_lang, display_lang=language_display(language, ui_lang))
    elif task_key == "dictation":
        _render_dictation(client, lang_en, level, niveau, model, ui_lang)
    elif task_key == "reading":
        _render_reading(client, lang_en, level, niveau, model, ui_lang)
    elif task_key:
        if st.button(
            t("new_task_btn", ui_lang), type="primary", use_container_width=True,
            help=t("help_new_task", ui_lang),
        ) or not state.task:
            _generate_task(task_key, task_label, client, language, level, niveau, model, ui_lang)

        _correction_panel(client, language, niveau, mentor, model, ui_lang)


def _render_quiz(
    client: openai.OpenAI, language: str, model: str, ui_lang: str, display_lang: str,
) -> None:
    state = st.session_state["state"]
    if st.button(t("quiz_new_btn", ui_lang), type="primary") or "current_quiz" not in st.session_state:
        with st.status(t("status_generating_quiz", ui_lang), expanded=False) as status:
            st.session_state["current_quiz"] = quiz_task.build_quiz(
                client, vocab_list=state.vocab_list, language=language, count=5, model=model,
                ui_language_name=UI_LANG_NAMES.get(ui_lang, "English"),
            )
            st.session_state["quiz_answers"] = {}
            state.num_tasks_generated = getattr(state, "num_tasks_generated", 0) + 1
            status.update(label=t("status_quiz_ready", ui_lang), state="complete")
    quiz = st.session_state.get("current_quiz", {})
    for fw, trans in quiz.items():
        st.session_state["quiz_answers"][fw] = st.text_input(
            t("quiz_prompt_format", ui_lang, language=display_lang, trans=trans),
            key=f"quiz_{fw}",
        )
    if quiz and st.button(t("quiz_evaluate_btn", ui_lang), type="primary"):
        result = quiz_task.score_answers(quiz, st.session_state["quiz_answers"])
        st.metric(t("quiz_score", ui_lang), f"{result.correct} / {result.total}")
        for word, ok in result.per_word.items():
            st.write(f"- {word}: {'✅' if ok else '❌'}")


_PUNCT_DIFF_RE = None  # lazy-init in _tokenize


def _tokenize_for_diff(s: str) -> list[str]:
    """Split on whitespace but keep punctuation attached so 'Paris.' stays one token."""
    return [tok for tok in s.strip().split() if tok]


def _render_dictation_diff(original: str, user: str) -> None:
    """Render a word-by-word diff: green for correct, red for wrong/extra, strikethrough for missing."""
    import difflib
    orig_tokens = _tokenize_for_diff(original)
    user_tokens = _tokenize_for_diff(user)

    matcher = difflib.SequenceMatcher(
        None,
        [t.lower().strip(".,;:!?\"'") for t in orig_tokens],
        [t.lower().strip(".,;:!?\"'") for t in user_tokens],
    )

    rendered: list[str] = []
    correct = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for tok in user_tokens[j1:j2]:
                rendered.append(f":green[{tok}]")
                correct += 1
        elif tag == "replace":
            for tok in user_tokens[j1:j2]:
                rendered.append(f":red[{tok}]")
            for tok in orig_tokens[i1:i2]:
                rendered.append(f":orange[(→ {tok})]")
        elif tag == "delete":
            for tok in orig_tokens[i1:i2]:
                rendered.append(f":gray[~~{tok}~~]")
        elif tag == "insert":
            for tok in user_tokens[j1:j2]:
                rendered.append(f":red[+{tok}]")

    total = len(orig_tokens)
    pct = (correct / total * 100) if total else 0
    st.markdown(f"**{correct} / {total} words correct — {pct:.0f}%**")
    st.markdown(" ".join(rendered))


def _render_dictation(
    client: openai.OpenAI, language_en: str, level: str, niveau: str,
    model: str, ui_lang: str,
) -> None:
    """Audio-based dictation task: LLM writes text → ElevenLabs speaks it → user transcribes."""
    import base64

    import streamlit.components.v1 as components

    state = st.session_state["state"]
    el_key, el_source = _resolve_elevenlabs_key()
    if not el_key:
        st.warning(t("dict_no_key", ui_lang))
        return
    if el_source == "byok":
        st.caption(t("el_source_byok", ui_lang))
    else:
        st.caption(t("el_source_env", ui_lang))

    if st.button(
        t("dict_generate", ui_lang), type="primary", help=t("help_dict_generate", ui_lang),
    ) or "dictation_bytes" not in st.session_state:
        try:
            with st.status(t("dict_status_text", ui_lang), expanded=False) as status:
                recent = st.session_state.get("dictation_history", [])
                text = dict_task.generate_text(
                    client, language=language_en, level=level, niveau=niveau,
                    model=model, sentences=3, avoid_recent=recent,
                )
                status.update(label=t("dict_status_tts", ui_lang))
                audio = dict_task.synthesize_speech(text, api_key=el_key)
                st.session_state["dictation_text"] = text
                st.session_state["dictation_bytes"] = audio
                st.session_state["dictation_revealed"] = False
                # keep the last 5 dictations in session so avoid_recent gets a corpus
                recent = recent + [text]
                st.session_state["dictation_history"] = recent[-5:]
                state.num_tasks_generated = getattr(state, "num_tasks_generated", 0) + 1
                status.update(label=t("dict_status_ready", ui_lang), state="complete")
        except dict_task.TTSUnavailable as exc:
            st.error(t("dict_tts_error", ui_lang, err=str(exc)))
            return

    audio_bytes = st.session_state.get("dictation_bytes")
    if not audio_bytes:
        return

    # Speed slider + HTML5 audio (native st.audio has no playbackRate).
    speed = st.select_slider(
        t("dict_speed", ui_lang), options=[0.5, 0.75, 1.0, 1.25, 1.5], value=1.0, key="dict_speed",
        help=t("help_dict_speed", ui_lang),
    )
    audio_b64 = base64.b64encode(audio_bytes).decode("ascii")
    player_html = f"""
    <audio id="dict_player" controls style="width:100%; background:transparent;"
           src="data:audio/mp3;base64,{audio_b64}"></audio>
    <script>
      (function() {{
        const el = document.getElementById("dict_player");
        if (el) {{ el.playbackRate = {speed}; }}
      }})();
    </script>
    """
    components.html(player_html, height=70)

    transcript = st.text_area(
        t("dict_your_transcript", ui_lang), value="", height=140, key="dict_transcript",
    )

    if st.button(t("dict_reveal", ui_lang)):
        st.session_state["dictation_revealed"] = True
    if st.session_state.get("dictation_revealed"):
        st.markdown(f"**{t('dict_original', ui_lang)}**")
        st.info(st.session_state["dictation_text"])
        if transcript.strip():
            orig = st.session_state["dictation_text"].strip()
            _render_dictation_diff(orig, transcript.strip())


def _soft_reset_tasks(state: Any) -> None:
    """Clear the current task + all task-specific caches. Sidebar config stays.

    Resets the exercise-picker dropdown too so the user lands on the "choose
    exercise" row (= the initial state after loading the app). Preserves
    learning language, level, niveau, mentor, vocab list, UI lang, BYOK keys,
    and dark-mode. Called by the 🏠 Home button.
    """
    state.task = ""
    state.user_text = ""
    for cache_key in (
        # dictation
        "dictation_bytes", "dictation_text", "dictation_revealed", "dictation_history",
        # quiz
        "current_quiz", "quiz_answers",
        # reading (both state + source-picker widget keys)
        "reading_passage", "reading_questions", "reading_mc_choices",
        "reading_open_answers", "reading_results", "reading_reveal",
        "read_source_pick", "read_length_pick", "read_theme_input",
        "read_url_input", "read_paste_input", "read_file_input",
        # exercise dropdown — force back to the blank "choose exercise" row
        "task_type_sel",
    ):
        st.session_state.pop(cache_key, None)


def _render_reading(
    client: openai.OpenAI, language_en: str, level: str, niveau: str,
    model: str, ui_lang: str,
) -> None:
    """Reading-comprehension exercise: source a text, then MC + open questions."""
    state = st.session_state["state"]
    ui_lang_name = UI_LANG_NAMES.get(ui_lang, "English")

    source_labels = {
        "ai": t("read_source_ai", ui_lang),
        "url": t("read_source_url", ui_lang),
        "paste": t("read_source_paste", ui_lang),
        "file": t("read_source_file", ui_lang),
    }
    source_pick = st.radio(
        t("read_source", ui_lang),
        list(source_labels.values()),
        horizontal=True,
        key="read_source_pick",
        help=t("help_read_source", ui_lang),
    )
    source_key = next(k for k, v in source_labels.items() if v == source_pick)

    passage_text: str | None = None

    if source_key == "ai":
        length_labels = {
            "short": t("read_length_short", ui_lang),
            "medium": t("read_length_medium", ui_lang),
            "long": t("read_length_long", ui_lang),
        }
        length_pick = st.select_slider(
            t("read_length", ui_lang), options=list(length_labels.values()),
            value=length_labels["medium"], key="read_length_pick",
            help=t("help_read_length", ui_lang),
        )
        length_key = next(k for k, v in length_labels.items() if v == length_pick)
        theme_input = st.text_input(
            t("read_theme", ui_lang),
            value=st.session_state.get("read_theme_input", ""),
            placeholder="e.g. climate, philosophy, everyday life",
            key="read_theme_input",
            help=t("help_read_theme", ui_lang),
        )
        theme = theme_input.strip() or "everyday life"
    elif source_key == "url":
        st.text_input(
            "URL", placeholder=t("read_url_placeholder", ui_lang),
            key="read_url_input",
        )
    elif source_key == "paste":
        st.text_area(
            t("read_source_paste", ui_lang),
            placeholder=t("read_paste_placeholder", ui_lang),
            height=200, key="read_paste_input",
        )
    else:  # file
        st.file_uploader(
            t("read_source_file", ui_lang), type=["txt"], key="read_file_input",
        )

    if st.button(
        t("read_generate", ui_lang), type="primary", use_container_width=True,
        help=t("help_read_generate", ui_lang),
    ):
        # Source the passage
        try:
            if source_key == "ai":
                with st.status(t("read_status_text", ui_lang), expanded=False) as status:
                    passage_text = reading_task.generate_text(
                        client, language=language_en, level=level, niveau=niveau,
                        theme=theme, length=length_key, model=model,
                    )
                    status.update(label=t("read_status_ready", ui_lang), state="complete")
            elif source_key == "url":
                url_val = (st.session_state.get("read_url_input") or "").strip()
                if not url_val:
                    st.warning(t("read_need_passage", ui_lang))
                    return
                with st.status(t("read_status_fetch", ui_lang), expanded=False) as status:
                    from src.vocab import fetch_article_text
                    try:
                        passage_text = fetch_article_text(url_val)
                    except Exception as exc:  # noqa: BLE001 - surface any fetch error
                        status.update(label="❌", state="error")
                        st.error(t("read_url_failed", ui_lang, err=str(exc)))
                        return
                    status.update(label=t("read_status_ready", ui_lang), state="complete")
            elif source_key == "paste":
                paste_val = (st.session_state.get("read_paste_input") or "").strip()
                if not paste_val:
                    st.warning(t("read_need_passage", ui_lang))
                    return
                passage_text = paste_val
            else:
                upload = st.session_state.get("read_file_input")
                if not upload:
                    st.warning(t("read_need_passage", ui_lang))
                    return
                passage_text = upload.read().decode("utf-8").strip()
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))
            return

        # Draft the questions
        with st.status(t("read_status_questions", ui_lang), expanded=False) as status:
            questions = reading_task.generate_questions(
                client, text=passage_text, language=language_en, model=model,
                ui_language_name=ui_lang_name,
            )
            status.update(label=t("read_status_ready", ui_lang), state="complete")

        st.session_state["reading_passage"] = passage_text
        st.session_state["reading_questions"] = questions
        st.session_state["reading_mc_choices"] = [None] * len(questions.multiple_choice)
        st.session_state["reading_open_answers"] = [""] * len(questions.open_questions)
        st.session_state.pop("reading_results", None)
        st.session_state.pop("reading_reveal", None)
        state.num_tasks_generated = getattr(state, "num_tasks_generated", 0) + 1

    passage = st.session_state.get("reading_passage")
    if not passage:
        return
    questions: reading_task.ReadingQuestions | None = st.session_state.get("reading_questions")
    if questions is None:
        return

    st.markdown(f"### {t('read_passage_heading', ui_lang)}")
    st.markdown(passage)

    # Multiple choice
    st.markdown(f"### {t('read_mc_heading', ui_lang)}")
    mc_choices: list[int | None] = list(st.session_state.get("reading_mc_choices", []))
    for i, q in enumerate(questions.multiple_choice):
        options = q.get("options", [])
        kind = q.get("kind", "")
        label = f"**{i + 1}.** {q.get('question', '')}  _(`{kind}`)_"
        # Use a placeholder-None via a non-selectable sentinel so the user has to pick.
        picked = st.radio(
            label, options=options, index=None,
            key=f"read_mc_{i}", horizontal=False,
        )
        mc_choices[i] = options.index(picked) if picked in options else None
    st.session_state["reading_mc_choices"] = mc_choices

    # Open questions
    st.markdown(f"### {t('read_open_heading', ui_lang)}")
    open_answers: list[str] = list(st.session_state.get("reading_open_answers", []))
    for i, q in enumerate(questions.open_questions):
        kind = q.get("kind", "")
        label = f"**{i + 1}.** {q.get('question', '')}  _(`{kind}`)_"
        open_answers[i] = st.text_area(
            label, value=open_answers[i] if i < len(open_answers) else "",
            height=100, key=f"read_open_{i}",
        )
    st.session_state["reading_open_answers"] = open_answers

    if st.button(t("read_submit", ui_lang), type="primary", help=t("help_read_submit", ui_lang)):
        mc_result = reading_task.score_mc(questions.multiple_choice, mc_choices)
        open_evals: list[reading_task.OpenEvaluation] = []
        with st.status(t("read_status_questions", ui_lang), expanded=False) as status:
            for q, answer in zip(questions.open_questions, open_answers, strict=False):
                open_evals.append(
                    reading_task.evaluate_open(
                        client, text=passage,
                        question=q.get("question", ""),
                        reference_answer=q.get("reference_answer", ""),
                        user_answer=answer, language=language_en, model=model,
                        ui_language_name=ui_lang_name,
                    )
                )
            status.update(label=t("status_feedback_ready", ui_lang), state="complete")
        st.session_state["reading_results"] = {
            "mc": mc_result,
            "open": open_evals,
        }
        state.num_corrections = getattr(state, "num_corrections", 0) + 1

    results = st.session_state.get("reading_results")
    if results:
        mc: reading_task.MCResult = results["mc"]
        st.metric(t("read_score", ui_lang), f"{mc.correct} / {mc.total}")
        for i, (q, ok) in enumerate(zip(questions.multiple_choice, mc.per_question, strict=False)):
            mark = "✅" if ok else "❌"
            correct_opt = q.get("options", [])[q.get("correct_index", 0)]
            rationale = q.get("rationale", "")
            if ok:
                st.markdown(f"{mark} **{i + 1}.** {q.get('question', '')}")
            else:
                st.markdown(
                    f"{mark} **{i + 1}.** {q.get('question', '')}  \n"
                    f"→ **{correct_opt}** — *{rationale}*"
                )
        st.markdown(f"### {t('read_open_feedback', ui_lang)}")
        for i, (q, ev) in enumerate(zip(questions.open_questions, results["open"], strict=False)):
            verdict_label = t(f"read_verdict_{ev.verdict}", ui_lang)
            st.markdown(f"**{i + 1}.** {q.get('question', '')}  \n{verdict_label}")
            if ev.feedback:
                st.markdown(f"> {ev.feedback}")
            with st.expander(t("read_reference_answer", ui_lang)):
                st.markdown(q.get("reference_answer", ""))


if __name__ == "__main__":
    main()
