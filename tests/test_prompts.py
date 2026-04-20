from src.prompts import (
    CLOZE_FUNCTION_SPEC,
    VOCAB_FUNCTION_SPEC,
    build_answer_comment_prompt,
    build_cloze_messages,
    build_conjugation_prompt,
    build_correction_prompt,
    build_error_detection_prompt,
    build_sentence_building_prompt,
    build_translation_prompt,
    build_vocab_autogen_prompt,
    build_vocab_extract_prompt,
)


def test_vocab_extract_prompt_includes_level_and_count():
    p = build_vocab_extract_prompt(language="französisch", level="B2", number=30)
    assert "B2" in p
    assert "30" in p
    assert "französisch" in p


def test_vocab_autogen_prompt_includes_niveau():
    p = build_vocab_autogen_prompt(language="französisch", level="B1", niveau="Technisch")
    assert "B1" in p
    assert "Technisch" in p


def test_cloze_messages_contain_vocabs_and_trous():
    msgs = build_cloze_messages(
        language="französisch",
        level="B2",
        niveau="Standardsprache",
        selected_vocab=["maison", "voiture"],
        number_trous=4,
    )
    combined = " ".join(m["content"] for m in msgs)
    assert "maison" in combined
    assert "voiture" in combined
    assert "4" in combined
    assert "emit_cloze" in combined  # tool is mentioned by name in system prompt


def test_cloze_function_spec_has_answers_separate():
    # Answers live in their own field so they can't leak into body.
    props = CLOZE_FUNCTION_SPEC["parameters"]["properties"]
    assert "body" in props
    assert "answers" in props
    assert "title" in props


def test_translation_prompt_includes_sentences_count():
    p = build_translation_prompt(
        language="französisch",
        level="B1",
        niveau="Standardsprache",
        selected_vocab=["manger"],
        number_sentences=3,
    )
    assert "3" in p
    assert "manger" in p


def test_sentence_building_prompt_contains_words():
    p = build_sentence_building_prompt(
        language="französisch",
        level="B1",
        niveau="Standardsprache",
        selected_vocab=["maison", "voiture"],
    )
    assert "maison" in p and "voiture" in p


def test_error_detection_prompt_mentions_level():
    p = build_error_detection_prompt(
        language="französisch",
        level="B2",
        niveau="Umgangssprache",
        selected_vocab=["aller"],
    )
    assert "B2" in p and "aller" in p


def test_conjugation_prompt_is_messages_list():
    msgs = build_conjugation_prompt(language="französisch", level="B1", vocab_list=["aller"])
    assert isinstance(msgs, list)
    assert msgs[0]["role"] == "system"
    assert msgs[1]["role"] == "user"
    assert "aller" in msgs[1]["content"]


def test_correction_prompt_includes_mentor_persona():
    p = build_correction_prompt(
        language="französisch",
        niveau="Standardsprache",
        mentor="Machiavelli",
        task="Schreibe einen Text",
        user_text="Je suis",
    )
    assert "Machiavelli" in p[0]["content"]
    assert "Je suis" in p[1]["content"]


def test_answer_comment_prompt_is_messages_list():
    msgs = build_answer_comment_prompt("Was ist passé composé?")
    assert isinstance(msgs, list)
    assert msgs[-1]["role"] == "user"
    assert "passé composé" in msgs[-1]["content"]


def test_vocab_function_spec_has_required_keys():
    assert VOCAB_FUNCTION_SPEC["name"] == "generate_vocabulary_list"
    assert "vocabulary" in VOCAB_FUNCTION_SPEC["parameters"]["properties"]
