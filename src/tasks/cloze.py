from __future__ import annotations

import random
from typing import Any

from src.prompts import build_cloze_system_prompt, build_cloze_user_prompt
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
    selected = random.sample(vocab_list, min(len(vocab_list), number_trous))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": build_cloze_system_prompt(language=language)},
            {
                "role": "user",
                "content": build_cloze_user_prompt(
                    language=language,
                    level=level,
                    niveau=niveau,
                    selected_vocab=selected,
                    number_trous=number_trous,
                ),
            },
        ],
    )
    body = response.choices[0].message.content.strip()
    joined = ", ".join(selected)
    return TaskInstruction(
        displayed_to_user=f"Fülle die Lücken im folgenden Text mit den Wörtern: {joined}\n\n{body}",
        internal_context={"selected_vocab": selected, "body": body},
    )
