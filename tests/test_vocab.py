import json

from src.vocab import (
    extract_vocabulary_from_text,
    generate_vocabulary_via_function_call,
    load_vocabulary,
)
from tests.fake_openai import FakeOpenAIClient


def test_load_vocabulary_from_file(tmp_path):
    path = tmp_path / "vocab.txt"
    path.write_text("maison\nvoiture\n  chaise  \n", encoding="utf-8")
    result = load_vocabulary(str(path))
    assert result == ["maison", "voiture", "chaise"]


def test_extract_vocabulary_returns_trimmed_list():
    fake = FakeOpenAIClient(responses=["maison, voiture ,   chaise"])
    result = extract_vocabulary_from_text(
        fake,
        text="Un texte quelconque.",
        language="französisch",
        level="B1",
        number=3,
        model="gpt-4o-mini",
    )
    assert result == ["maison", "voiture", "chaise"]


def test_extract_vocabulary_records_user_message():
    fake = FakeOpenAIClient(responses=["a, b"])
    extract_vocabulary_from_text(
        fake,
        text="Texte.",
        language="französisch",
        level="B2",
        number=10,
        model="gpt-4o-mini",
    )
    messages = fake.calls[0]["messages"]
    assert any("B2" in m["content"] for m in messages)
    assert any(m["content"] == "Texte." for m in messages)


def test_generate_vocabulary_via_function_call_parses_json():
    payload = json.dumps({"vocabulary": ["a", "b", "c"]})
    fake = FakeOpenAIClient(responses=[{"tool_arguments": payload}])
    result = generate_vocabulary_via_function_call(
        fake,
        language="französisch",
        level="B1",
        niveau="Standardsprache",
        model="google/gemini-2.5-flash-lite",
    )
    assert result == ["a", "b", "c"]
    call = fake.calls[0]
    # Must use new tools-API, not deprecated functions/function_call.
    assert "tools" in call
    assert "tool_choice" in call
    assert "functions" not in call
    assert "function_call" not in call
