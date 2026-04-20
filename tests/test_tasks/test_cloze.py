import json

from src.tasks.cloze import build
from tests.fake_openai import FakeOpenAIClient


def _cloze_payload(title, body, answers, hints=None):
    return {
        "tool_arguments": json.dumps({
            "title": title,
            "vocab_hints": hints or [f"{a}: meaning" for a in answers],
            "body": body,
            "answers": answers,
        })
    }


def test_build_returns_structured_cloze():
    fake = FakeOpenAIClient(responses=[_cloze_payload(
        title="Test Titel",
        body="Dans la ___ il y a une ___ et une ___.",
        answers=["maison", "voiture", "chaise"],
    )])
    result = build(
        fake,
        vocab_list=["maison", "voiture", "chaise"],
        language="französisch",
        level="B1",
        niveau="Standardsprache",
        number_trous=3,
        model="google/gemini-2.5-flash-lite",
    )
    # Title + body appear; answers are NOT in displayed output.
    assert "Test Titel" in result.displayed_to_user
    assert "Dans la ___" in result.displayed_to_user
    # Vocabs are shown sorted alphabetically (so order does not hint blanks).
    displayed = result.displayed_to_user
    i_chaise = displayed.rfind("chaise")
    i_maison = displayed.rfind("maison")
    i_voiture = displayed.rfind("voiture")
    assert i_chaise < i_maison < i_voiture, "vocab list must be sorted alphabetically"
    # Answers stored for internal use (future scoring) but NOT in displayed text.
    assert result.internal_context["answers"] == ["maison", "voiture", "chaise"]


def test_build_caps_selection_at_vocab_size():
    fake = FakeOpenAIClient(responses=[_cloze_payload(
        title="T", body="___", answers=["maison"],
    )])
    result = build(
        fake,
        vocab_list=["maison"],
        language="französisch",
        level="B1",
        niveau="Standardsprache",
        number_trous=5,
        model="google/gemini-2.5-flash-lite",
    )
    assert len(result.internal_context["selected_vocab"]) == 1


def test_build_uses_tools_api_not_deprecated():
    fake = FakeOpenAIClient(responses=[_cloze_payload(
        title="T", body="___", answers=["x"],
    )])
    build(
        fake,
        vocab_list=["x"],
        language="französisch",
        level="B1",
        niveau="Standardsprache",
        number_trous=1,
        model="google/gemini-2.5-flash-lite",
    )
    call = fake.calls[0]
    assert "tools" in call and "tool_choice" in call
    assert "functions" not in call and "function_call" not in call
