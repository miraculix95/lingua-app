"""About page — project story, author, GitHub link.

Referenced from ``src/app.py`` via ``st.Page("pages/1_ℹ️_About.py", ...)``.
Under ``st.navigation``, only the entrypoint may call ``st.set_page_config`` —
so this file must NOT call it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Make "src" importable (same trick as src/app.py)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.app import _apply_theme  # noqa: E402 — reuse the main app's CSS injector
from src.i18n import (  # noqa: E402
    DEFAULT_UI_LANG,
    UI_LANGS,
    t,
)

# Resolve UI language: ui_lang_label is only present while the main page's
# sidebar widget is rendered — on /about that widget doesn't exist and
# Streamlit garbage-collects the key. We mirror it in `_ui_lang_persisted`
# via the sidebar on every main-page render.
selected_label = (
    st.session_state.get("ui_lang_label")
    or st.session_state.get("_ui_lang_persisted")
)
ui_lang = UI_LANGS.get(selected_label, DEFAULT_UI_LANG) if selected_label else DEFAULT_UI_LANG

# Reapply the same theme as the main page — dark-mode, mobile CSS, UI-RTL if the
# interface language itself is RTL (Hebrew). Learning language has no content on
# this page so pass empty.
_apply_theme(learning_language="", ui_lang=ui_lang)

st.markdown(f"# {t('about_title', ui_lang)}")
st.markdown(t("about_body", ui_lang))
