from src.correction import answer_comment, correct_text, extract_comments
from tests.fake_openai import FakeOpenAIClient


def test_extract_comments_splits_angle_brackets():
    text = "Bonjour <was heißt bonjour?> je vais bien <ist das Passé Composé?>"
    cleaned, comments = extract_comments(text)
    assert cleaned == "Bonjour  je vais bien"
    assert comments == ["was heißt bonjour?", "ist das Passé Composé?"]


def test_extract_comments_handles_no_comments():
    text = "Bonjour je vais bien"
    cleaned, comments = extract_comments(text)
    assert cleaned == "Bonjour je vais bien"
    assert comments == []


def test_correct_text_passes_mentor_to_prompt():
    fake = FakeOpenAIClient(responses=["corrigé"])
    result = correct_text(
        fake,
        task="Schreibe etwas",
        user_text="Je suis",
        language="französisch",
        niveau="Standardsprache",
        mentor="Machiavelli",
        model="gpt-4o-mini",
    )
    assert result == "corrigé"
    sys_content = fake.calls[0]["messages"][0]["content"]
    assert "Machiavelli" in sys_content


def test_answer_comment_returns_response():
    fake = FakeOpenAIClient(responses=["Das bedeutet Hallo"])
    result = answer_comment(fake, comment="Was heißt bonjour?", model="gpt-4o-mini")
    assert result == "Das bedeutet Hallo"
