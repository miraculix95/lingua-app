"""Session-state container.

Replaces the scattered ``if 'foo' not in st.session_state: st.session_state.foo = ...``
blocks from the legacy monolith (14 of them). The whole state lives in one
dataclass, stored at ``st.session_state["state"]``.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SessionState:
    vocab_list: list[str] = field(default_factory=list)
    task_type: str | None = None
    current_task: str | None = None
    user_responses: dict = field(default_factory=dict)
    theme: str = ""
    new_task: bool = False
    user_text: str = ""
    last_text: str = ""
    number_of_words: int = 40
    level: str = "B1"
    niveau: str = "Standardsprache"
    task_type_flagg: bool = False
    text_input_flagg: bool = False
    num_runs: int = 0
    file_path_extract: Any = None
    uploaded_vocab_file: Any = None
    task: str = ""
    auto_gen_vocabs: bool = False
    html_path_extract: str = ""
    stop: bool = True


def init_session_state(streamlit_state: Any) -> None:
    if "state" not in streamlit_state:
        streamlit_state["state"] = SessionState()
    streamlit_state["state"].num_runs += 1
