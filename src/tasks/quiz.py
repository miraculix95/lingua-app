"""Vocabulary quiz — fixed re-implementation of the broken legacy version.

Legacy bugs that are fixed here (see Linear TES-540):

- ``answer = [], word = []`` was Tuple-unpacking, not two lists.
- ``enumerate(quiz.items())`` yields 2-tuples not 3; the legacy for-loop crashed.
- Button-callback referenced undefined Streamlit keys.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any


@dataclass
class QuizResult:
    correct: int
    total: int
    per_word: dict[str, bool]


def build_quiz(
    client: Any,
    *,
    vocab_list: list[str],
    language: str,
    count: int,
    model: str,
) -> dict[str, str]:
    selected = random.sample(vocab_list, min(len(vocab_list), count))
    quiz: dict[str, str] = {}
    for word in selected:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Übersetze das {language}e Wort '{word}' ins Deutsche. "
                        "Antworte nur mit dem deutschen Wort, ohne Artikel, ohne Erklärung."
                    ),
                }
            ],
        )
        quiz[word] = response.choices[0].message.content.strip()
    return quiz


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
