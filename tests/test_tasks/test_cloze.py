from src.tasks.cloze import build
from tests.fake_openai import FakeOpenAIClient


def test_build_returns_cloze_text():
    fake = FakeOpenAIClient(responses=["Titel\n\nLückentext mit Lücke ___."])
    result = build(
        fake,
        vocab_list=["maison", "voiture", "chaise"],
        language="französisch",
        level="B1",
        niveau="Standardsprache",
        number_trous=2,
        model="gpt-4o-mini",
    )
    assert "Lückentext" in result.displayed_to_user
    assert len(result.internal_context["selected_vocab"]) == 2


def test_build_caps_selection_at_vocab_size():
    fake = FakeOpenAIClient(responses=["text"])
    result = build(
        fake,
        vocab_list=["maison"],
        language="französisch",
        level="B1",
        niveau="Standardsprache",
        number_trous=5,
        model="gpt-4o-mini",
    )
    assert len(result.internal_context["selected_vocab"]) == 1
