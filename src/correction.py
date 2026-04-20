"""Text correction and comment handling.

Legacy behavior: users can embed ``<meta-questions>`` in angle brackets; those
get extracted, answered separately, and the cleaned text is fed to the
corrector.
"""
from __future__ import annotations

import re
from typing import Any

from src.prompts import build_answer_comment_prompt, build_correction_prompt

_COMMENT_RE = re.compile(r"<(.*?)>")


def extract_comments(text: str) -> tuple[str, list[str]]:
    comments = _COMMENT_RE.findall(text)
    cleaned = _COMMENT_RE.sub("", text).strip()
    return cleaned, comments


def correct_text(
    client: Any,
    *,
    task: str,
    user_text: str,
    language: str,
    niveau: str,
    mentor: str,
    model: str,
) -> str:
    messages = build_correction_prompt(
        language=language, niveau=niveau, mentor=mentor, task=task, user_text=user_text,
    )
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content.strip()


def answer_comment(client: Any, *, comment: str, model: str) -> str:
    messages = build_answer_comment_prompt(comment)
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content.strip()
