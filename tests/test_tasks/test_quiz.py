from src.tasks.quiz import build_quiz, score_answers
from tests.fake_openai import FakeOpenAIClient


def test_build_quiz_calls_llm_per_word():
    fake = FakeOpenAIClient(responses=["Haus", "Auto", "Stuhl"])
    quiz = build_quiz(
        fake,
        vocab_list=["maison", "voiture", "chaise"],
        language="französisch",
        count=3,
        model="gpt-4o-mini",
    )
    assert quiz == {"maison": "Haus", "voiture": "Auto", "chaise": "Stuhl"}
    assert len(fake.calls) == 3


def test_build_quiz_caps_at_vocab_size():
    fake = FakeOpenAIClient(responses=["Haus"])
    quiz = build_quiz(
        fake,
        vocab_list=["maison"],
        language="französisch",
        count=10,
        model="gpt-4o-mini",
    )
    assert len(quiz) == 1


def test_score_answers_counts_correct_case_insensitive():
    quiz = {"maison": "Haus", "voiture": "Auto"}
    user_answers = {"maison": "haus", "voiture": "falsch"}
    result = score_answers(quiz, user_answers)
    assert result.correct == 1
    assert result.total == 2
    assert result.per_word == {"maison": True, "voiture": False}


def test_score_answers_tolerates_missing_answer():
    quiz = {"maison": "Haus"}
    result = score_answers(quiz, {})
    assert result.correct == 0
    assert result.per_word == {"maison": False}
