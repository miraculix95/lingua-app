from __future__ import annotations

import json
import random
from typing import Any

from src.prompts import CLOZE_FUNCTION_SPEC, build_cloze_messages
from src.tasks.base import TaskInstruction


def build(
    client: Any,
    *,
    vocab_list: list[str],
    language: str,
    level: str,
    niveau: str,
    number_trous: int,
    model: str,
) -> TaskInstruction:
    """Generate a cloze exercise with two anti-cheat mitigations.

    1. **Solution-leak prevention:** Structured output via tools API — answers
       land in a dedicated JSON field, never in the user-facing body string.
    2. **Order-tell prevention:** The vocab list shown to the learner is
       sorted alphabetically, independent of the order the LLM chose to
       place words in blanks.
    """
    selected = random.sample(vocab_list, min(len(vocab_list), number_trous))
    messages = build_cloze_messages(
        language=language,
        level=level,
        niveau=niveau,
        selected_vocab=selected,
        number_trous=number_trous,
    )
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=[{"type": "function", "function": CLOZE_FUNCTION_SPEC}],
        tool_choice={"type": "function", "function": {"name": "emit_cloze"}},
    )
    tool_call = response.choices[0].message.tool_calls[0]
    payload = json.loads(tool_call.function.arguments)

    title = payload["title"]
    vocab_hints = payload.get("vocab_hints", [])
    body = payload["body"]
    answers = payload["answers"]

    # Show vocabs alphabetically so blank-order doesn't leak from list-order.
    display_vocab = sorted(selected, key=str.lower)

    displayed = (
        f"**{title}**\n\n"
        f"**Vokabeln (alphabetisch):**\n"
        + "\n".join(f"- {h}" for h in vocab_hints)
        + f"\n\n**Zu benutzen:** {', '.join(display_vocab)}\n\n"
        f"**Lückentext:**\n\n{body}"
    )

    return TaskInstruction(
        displayed_to_user=displayed,
        internal_context={
            "selected_vocab": selected,
            "answers": answers,  # order matches blank-order in body
            "body": body,
            "title": title,
        },
    )
