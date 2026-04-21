import json

from src.tasks.reading import (
    LENGTH_TARGETS,
    MCResult,
    OpenEvaluation,
    ReadingQuestions,
    evaluate_open,
    generate_questions,
    generate_text,
    score_mc,
)
from tests.fake_openai import FakeOpenAIClient


def _questions_payload(mc, open_q):
    return {"tool_arguments": json.dumps({
        "multiple_choice": mc,
        "open_questions": open_q,
    })}


def test_generate_text_strips_and_uses_length():
    fake = FakeOpenAIClient(responses=["  A passage in French.  \n"])
    out = generate_text(
        fake, language="French", level="B2", niveau="Standardsprache",
        theme="climate", length="medium", model="m",
    )
    assert out == "A passage in French."
    # Length target made it into the prompt.
    combined = " ".join(m["content"] for m in fake.calls[0]["messages"])
    assert str(LENGTH_TARGETS["medium"]) in combined
    assert "climate" in combined


def test_generate_text_unknown_length_falls_back_to_medium():
    fake = FakeOpenAIClient(responses=["x"])
    generate_text(
        fake, language="French", level="A2", niveau="Standardsprache",
        theme="food", length="gigantic", model="m",
    )
    combined = " ".join(m["content"] for m in fake.calls[0]["messages"])
    assert str(LENGTH_TARGETS["medium"]) in combined


def test_generate_questions_uses_tools_api():
    mc = [{
        "question": "Q1?", "kind": "fact", "options": ["a", "b", "c", "d"],
        "correct_index": 1, "rationale": "b is stated.",
    }]
    op = [{"question": "Open?", "kind": "inference", "reference_answer": "R."}]
    fake = FakeOpenAIClient(responses=[_questions_payload(mc, op)])
    result = generate_questions(
        fake, text="some text", language="French", model="m",
        ui_language_name="English", num_mc=1, num_open=1,
    )
    assert isinstance(result, ReadingQuestions)
    assert len(result.multiple_choice) == 1
    assert len(result.open_questions) == 1
    call = fake.calls[0]
    assert "tools" in call and "tool_choice" in call
    assert "functions" not in call  # modern API only


def test_score_mc_counts_correctly():
    questions = [
        {"question": "Q1", "correct_index": 0, "options": ["a", "b", "c", "d"]},
        {"question": "Q2", "correct_index": 2, "options": ["a", "b", "c", "d"]},
        {"question": "Q3", "correct_index": 1, "options": ["a", "b", "c", "d"]},
    ]
    result = score_mc(questions, [0, 2, None])
    assert isinstance(result, MCResult)
    assert result.correct == 2
    assert result.total == 3
    assert result.per_question == [True, True, False]


def test_score_mc_skipped_is_wrong():
    questions = [{"question": "Q1", "correct_index": 0, "options": ["a", "b"]}]
    result = score_mc(questions, [None])
    assert result.correct == 0
    assert result.per_question == [False]


def test_evaluate_open_parses_verdict():
    fake = FakeOpenAIClient(responses=["CORRECT\nNice — you covered the key point."])
    ev = evaluate_open(
        fake, text="passage", question="Q?", reference_answer="ref",
        user_answer="my answer", language="French", model="m",
    )
    assert isinstance(ev, OpenEvaluation)
    assert ev.verdict == "CORRECT"
    assert "Nice" in ev.feedback


def test_evaluate_open_handles_partial_and_incorrect():
    fake = FakeOpenAIClient(responses=[
        "PARTIAL\nYou mentioned X but missed Y.",
        "INCORRECT\nThis contradicts the passage.",
    ])
    ev1 = evaluate_open(
        fake, text="t", question="Q", reference_answer="r",
        user_answer="a", language="French", model="m",
    )
    ev2 = evaluate_open(
        fake, text="t", question="Q", reference_answer="r",
        user_answer="a", language="French", model="m",
    )
    assert ev1.verdict == "PARTIAL"
    assert ev2.verdict == "INCORRECT"


def test_evaluate_open_empty_answer_short_circuits():
    fake = FakeOpenAIClient(responses=[])
    ev = evaluate_open(
        fake, text="t", question="Q", reference_answer="r",
        user_answer="   ", language="French", model="m",
    )
    assert ev.verdict == "INCORRECT"
    assert not fake.calls  # no LLM call made


def test_evaluate_open_unknown_verdict_maps_to_error():
    fake = FakeOpenAIClient(responses=["Hmm maybe\nstuff"])
    ev = evaluate_open(
        fake, text="t", question="Q", reference_answer="r",
        user_answer="a", language="French", model="m",
    )
    assert ev.verdict == "ERROR"
