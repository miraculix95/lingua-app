"""Reading-comprehension task.

Flow:
    1. Source the passage (AI-generated / URL / pasted / uploaded .txt).
    2. LLM emits structured MC + open questions via the emit_reading_questions tool.
    3. UI collects learner answers.
    4. MC is scored locally; open questions are graded by a second LLM call
       using a reference answer.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from src.prompts import (
    READING_QUESTIONS_FUNCTION_SPEC,
    build_reading_eval_prompt,
    build_reading_questions_messages,
    build_reading_text_prompt,
)

LENGTH_TARGETS: dict[str, int] = {
    "short": 150,
    "medium": 350,
    "long": 600,
}


@dataclass
class ReadingQuestions:
    multiple_choice: list[dict]
    open_questions: list[dict]


@dataclass
class MCResult:
    correct: int
    total: int
    per_question: list[bool]


@dataclass
class OpenEvaluation:
    verdict: str  # CORRECT / PARTIAL / INCORRECT / ERROR
    feedback: str


def generate_text(
    client: Any,
    *,
    language: str,
    level: str,
    niveau: str,
    theme: str,
    length: str,
    model: str,
) -> str:
    """Generate a reading passage in the learning language.

    ``length`` is a key in ``LENGTH_TARGETS``; unknown values fall back to
    ``medium`` so a caller can always pass a raw slider label.
    """
    word_target = LENGTH_TARGETS.get(length, LENGTH_TARGETS["medium"])
    messages = build_reading_text_prompt(
        language=language, level=level, niveau=niveau,
        theme=theme, word_target=word_target,
    )
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()


def generate_questions(
    client: Any,
    *,
    text: str,
    language: str,
    model: str,
    ui_language_name: str = "English",
    num_mc: int = 5,
    num_open: int = 3,
) -> ReadingQuestions:
    """Ask the LLM for structured questions via tool-calling."""
    messages = build_reading_questions_messages(
        text=text, language=language, ui_language_name=ui_language_name,
        num_mc=num_mc, num_open=num_open,
    )
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=[{"type": "function", "function": READING_QUESTIONS_FUNCTION_SPEC}],
        tool_choice={"type": "function", "function": {"name": "emit_reading_questions"}},
    )
    payload = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    return ReadingQuestions(
        multiple_choice=list(payload.get("multiple_choice", [])),
        open_questions=list(payload.get("open_questions", [])),
    )


def score_mc(
    questions: list[dict], user_choices: list[int | None],
) -> MCResult:
    """Score MC answers locally.

    ``user_choices`` is a list parallel to ``questions`` where each entry is
    the 0-based option index the learner picked, or ``None`` if they skipped.
    """
    per_question: list[bool] = []
    for q, picked in zip(questions, user_choices, strict=False):
        correct_idx = q.get("correct_index")
        per_question.append(picked is not None and picked == correct_idx)
    return MCResult(
        correct=sum(per_question),
        total=len(questions),
        per_question=per_question,
    )


def evaluate_open(
    client: Any,
    *,
    text: str,
    question: str,
    reference_answer: str,
    user_answer: str,
    language: str,
    model: str,
    ui_language_name: str = "English",
) -> OpenEvaluation:
    """Grade a single open-ended answer with the LLM.

    Parses the model's first line as a verdict word; everything below is
    treated as free-form feedback. Falls back to ``ERROR`` if the first
    line is not one of the expected tokens — the UI can show the raw text
    as-is in that case.
    """
    if not user_answer.strip():
        return OpenEvaluation(verdict="INCORRECT", feedback="(no answer given)")
    messages = build_reading_eval_prompt(
        text=text, question=question, reference_answer=reference_answer,
        user_answer=user_answer, language=language, ui_language_name=ui_language_name,
    )
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )
    raw = (response.choices[0].message.content or "").strip()
    lines = raw.splitlines()
    first = lines[0].strip().upper() if lines else ""
    if first.startswith("CORRECT"):
        verdict = "CORRECT"
    elif first.startswith("PARTIAL"):
        verdict = "PARTIAL"
    elif first.startswith("INCORRECT"):
        verdict = "INCORRECT"
    else:
        verdict = "ERROR"
    feedback = "\n".join(lines[1:]).strip() or raw
    return OpenEvaluation(verdict=verdict, feedback=feedback)
