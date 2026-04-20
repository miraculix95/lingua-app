"""Vocabulary quiz — fixed re-implementation of the broken legacy version.

Legacy bugs that are fixed here (see Linear TES-540):

- ``answer = [], word = []`` was Tuple-unpacking, not two lists.
- ``enumerate(quiz.items())`` yields 2-tuples not 3; the legacy for-loop crashed.
- Button-callback referenced undefined Streamlit keys.

Single-call optimization (2026-04-20): translations fetched for all words in a
single tool-call rather than N sequential completions. Cuts quiz-build time
from ~10s to ~1-2s.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Any


@dataclass
class QuizResult:
    correct: int
    total: int
    per_word: dict[str, bool]


_QUIZ_FUNCTION_SPEC: dict = {
    "name": "emit_quiz_translations",
    "description": "Return translations of each input word into the target language.",
    "parameters": {
        "type": "object",
        "properties": {
            "translations": {
                "type": "object",
                "description": (
                    "Map from source word (as given) to translated word. "
                    "Value is a single word in the target language, no article, "
                    "no explanation, no punctuation."
                ),
                "additionalProperties": {"type": "string"},
            }
        },
        "required": ["translations"],
    },
}


def build_quiz(
    client: Any,
    *,
    vocab_list: list[str],
    language: str,
    count: int,
    model: str,
    ui_language_name: str = "English",
) -> dict[str, str]:
    """Build a quiz dict {source_word: target_translation} in a single API call."""
    selected = random.sample(vocab_list, min(len(vocab_list), count))
    joined = ", ".join(selected)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You translate {language} words into {ui_language_name}. "
                    f"Use the emit_quiz_translations tool. For each given word, return "
                    f"the single most common {ui_language_name} word — no article, "
                    f"no explanation, no punctuation."
                ),
            },
            {
                "role": "user",
                "content": f"Translate these {language} words into {ui_language_name}: {joined}",
            },
        ],
        tools=[{"type": "function", "function": _QUIZ_FUNCTION_SPEC}],
        tool_choice={"type": "function", "function": {"name": "emit_quiz_translations"}},
    )
    tool_call = response.choices[0].message.tool_calls[0]
    payload = json.loads(tool_call.function.arguments)
    raw = payload["translations"]
    # Preserve the selected-word order, even if the LLM reorders keys.
    return {word: raw.get(word, "").strip() for word in selected}


def score_answers(quiz: dict[str, str], user_answers: dict[str, str]) -> QuizResult:
    per_word = {
        word: user_answers.get(word, "").strip().lower() == translation.strip().lower()
        for word, translation in quiz.items()
    }
    return QuizResult(
        correct=sum(per_word.values()),
        total=len(quiz),
        per_word=per_word,
    )
