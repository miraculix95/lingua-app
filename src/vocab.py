"""Vocabulary loading and extraction.

Four sources:
- ``load_vocabulary``: read a .txt file of one-word-per-line vocabulary.
- ``extract_vocabulary_from_text``: ask the LLM to extract N vocabs from given text.
- ``generate_vocabulary_via_function_call``: ask the LLM to invent a vocab list.
- ``fetch_article_text``: fetch+parse a URL (returns text, no disk write).
"""
from __future__ import annotations

import json
from typing import Any

from src.logging_setup import get_logger
from src.prompts import (
    VOCAB_FUNCTION_SPEC,
    build_vocab_autogen_prompt,
    build_vocab_extract_prompt,
)

log = get_logger(__name__)


def load_vocabulary(file_path: str) -> list[str]:
    with open(file_path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def extract_vocabulary_from_text(
    client: Any,
    *,
    text: str,
    language: str,
    level: str,
    number: int,
    model: str,
) -> list[str]:
    system = build_vocab_extract_prompt(language=language, level=level, number=number)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
    )
    raw = response.choices[0].message.content.strip()
    return [v.strip() for v in raw.split(",") if v.strip()]


def generate_vocabulary_via_function_call(
    client: Any,
    *,
    language: str,
    level: str,
    niveau: str,
    model: str,
) -> list[str]:
    """Ask the LLM to emit a vocabulary list via structured tool-calling.

    Uses the modern ``tools`` / ``tool_choice`` API (not the deprecated
    ``functions``/``function_call`` — OpenRouter providers like Mistral
    reject those with HTTP 400).
    """
    user_prompt = build_vocab_autogen_prompt(language=language, level=level, niveau=niveau)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Du bist ein Sprachlehrer."},
            {"role": "user", "content": user_prompt},
        ],
        tools=[{"type": "function", "function": VOCAB_FUNCTION_SPEC}],
        tool_choice={"type": "function", "function": {"name": "generate_vocabulary_list"}},
    )
    tool_call = response.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)["vocabulary"]


def fetch_article_text(url: str) -> str:
    """Download and parse a news article URL, return title+summary+body.

    Uses newspaper3k. Returns an in-memory string — no disk writes (fixing the
    legacy CWD-dependency bug where output was written to ``news_article.txt``).
    """
    from newspaper import Article  # imported lazily: heavy dep

    article = Article(url)
    article.download()
    article.parse()
    return f"{article.title}\n\n{article.summary}\n\n{article.text}"
