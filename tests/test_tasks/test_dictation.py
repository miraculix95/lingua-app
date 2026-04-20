from src.tasks.dictation import TTSUnavailable, generate_text, synthesize_speech
from tests.fake_openai import FakeOpenAIClient


def test_generate_text_returns_stripped_content():
    fake = FakeOpenAIClient(responses=["Un petit texte pour la dictée.\n\n"])
    result = generate_text(
        fake, language="French", level="B1", niveau="Standardsprache",
        model="google/gemini-2.5-flash-lite", sentences=3,
    )
    assert result == "Un petit texte pour la dictée."


def test_synthesize_raises_without_key():
    try:
        synthesize_speech("hello", api_key="")
    except TTSUnavailable:
        return
    raise AssertionError("expected TTSUnavailable")
