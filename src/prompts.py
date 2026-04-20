"""Prompt templates as pure functions.

Every function returns either a plain prompt string or a full ``messages`` list
ready to pass to ``openai.chat.completions.create``. No side effects, no I/O.
"""
from __future__ import annotations

from src.config import NO_ANSWERS_HINT

VOCAB_FUNCTION_SPEC: dict = {
    "name": "generate_vocabulary_list",
    "description": "Generiert eine Liste Vokabeln mit Verben.",
    "parameters": {
        "type": "object",
        "properties": {
            "vocabulary": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Eine Liste von Vokabeln.",
            }
        },
        "required": ["vocabulary"],
    },
}


CLOZE_FUNCTION_SPEC: dict = {
    "name": "emit_cloze",
    "description": (
        "Gibt einen Lückentext strukturiert aus. Lösungen kommen ausschließlich in "
        "das 'answers'-Feld, NIEMALS in den Body oder Titel."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Kurzer Titel für den Text (keine Lösungen enthalten).",
            },
            "vocab_hints": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Kurze Bedeutungs-Erklärungen zu jeder Vokabel im Format "
                    "'wort: kurze Erklärung'."
                ),
            },
            "body": {
                "type": "string",
                "description": (
                    "Der Lückentext. Jede Lücke als '___' (drei Unterstriche) markiert. "
                    "Enthält KEINE Lösungen, keine Hinweise welches Wort in welche Lücke gehört."
                ),
            },
            "answers": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Die Lösungs-Wörter in der Reihenfolge der Lücken im Body. "
                    "Jeder Eintrag genau eine der Ziel-Vokabeln (ggf. konjugiert/dekliniert)."
                ),
            },
        },
        "required": ["title", "vocab_hints", "body", "answers"],
    },
}


def build_vocab_extract_prompt(*, language: str, level: str, number: int) -> str:
    return (
        f"You are a language teacher. Extract exactly {number} {language} vocabulary items "
        f"or expressions matching a minimum CEFR level of {level} from the following text. "
        f"Provide a good mix of verbs, complex expressions, adjectives, and nouns. "
        f"Avoid proper names and geographic names. "
        f"Return the vocabulary as a comma-separated list without numbering. "
        f"No introduction, no commentary."
    )


def build_vocab_autogen_prompt(*, language: str, level: str, niveau: str) -> str:
    return (
        f"Create a list of 20 {language} vocabulary items including verbs. "
        f"Target CEFR level: {level}. Register: {niveau}. "
        f"Pick thematically coherent words."
    )


def build_cloze_messages(
    *,
    language: str,
    level: str,
    niveau: str,
    selected_vocab: list[str],
    number_trous: int,
    ui_language_name: str = "English",
) -> list[dict]:
    """Messages for structured cloze generation via the ``emit_cloze`` tool.

    Answers land in a separate JSON field — the ``body`` string has only
    ``___`` placeholders, never the solution words.
    ``vocab_hints`` are explanations in the user's UI language.
    """
    joined = ", ".join(selected_vocab)
    return [
        {
            "role": "system",
            "content": (
                f"You are a {language} language teacher creating cloze exercises for learners. "
                f"IMPORTANT: use the emit_cloze tool for structured output. Solutions go "
                f"EXCLUSIVELY into the 'answers' field. The 'body' contains only '___' for "
                f"blanks — never reveal which word goes where inside the body or title."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Create a {language} cloze text using these vocabs: {joined}. "
                f"CEFR level: {level}. Register: {niveau}. "
                f"Exactly {number_trous} blanks marked as '___'. "
                f"Each vocab exactly once, in the proper grammatical form (conjugation, "
                f"plural, etc.). The text should form a small coherent story or context "
                f"and have a fitting title.\n\n"
                f"CRITICAL SHUFFLE RULE: The order in which vocabs appear in the blanks "
                f"MUST NOT be alphabetical, and MUST NOT match the order in which I listed "
                f"them above. Pick the blank positions randomly — e.g. if I gave you "
                f"[apple, banana, cherry, date], the blanks could fill as "
                f"[cherry, apple, date, banana] or any non-trivial permutation. A learner "
                f"must not be able to guess answers just from the vocab list order.\n\n"
                f"LANGUAGE RULE: 'vocab_hints' MUST be written in {ui_language_name} — "
                f"never English unless {ui_language_name} IS English. Each hint is a short "
                f"meaning explanation in {ui_language_name} (can be a translation or a "
                f"paraphrase, whichever is clearer).\n\n"
                f"'answers': the actual words placed in the blanks, in the order blanks "
                f"appear in body (same randomized permutation as above)."
            ),
        },
    ]


def build_translation_prompt(
    *,
    learning_language: str,
    ui_language_name: str,
    source_language_name: str,
    target_language_name: str,
    level: str,
    niveau: str,
    selected_vocab: list[str],
    number_sentences: int,
) -> str:
    """Generate a translation exercise in a chosen direction.

    Two directions:
    - source=UI-lang, target=learning-lang  → active production
    - source=learning-lang, target=UI-lang  → passive comprehension
    """
    joined = ", ".join(selected_vocab)
    return (
        f"First, show the learner the {learning_language} vocabs with their "
        f"{ui_language_name} meanings (glossary): {joined}.\n\n"
        f"Then create {number_sentences} sentences IN {source_language_name} for the "
        f"learner to translate INTO {target_language_name}. Register: {niveau}. "
        f"CEFR level: {level}. The sentences must naturally use the vocabs above. "
        f"Do NOT provide the {target_language_name} translations — the learner produces "
        f"them.{NO_ANSWERS_HINT}\n\n"
        f"Output format (write everything in {ui_language_name} EXCEPT the {source_language_name} "
        f"sentences themselves):\n"
        f"Glossary ({learning_language} → {ui_language_name}): bullet list.\n"
        f"---\n"
        f"Translate these {source_language_name} sentences into {target_language_name}: "
        f"numbered list of {number_sentences} sentences in {source_language_name}."
    )


def build_sentence_building_prompt(
    *,
    language: str,
    level: str,
    niveau: str,
    selected_vocab: list[str],
) -> str:
    words = ", ".join(selected_vocab)
    return (
        f"Create a single {language} sentence using these words: {words}. "
        f"Register: {niveau}. CEFR level: {level}.{NO_ANSWERS_HINT}"
    )


def build_error_detection_prompt(
    *,
    language: str,
    level: str,
    niveau: str,
    selected_vocab: list[str],
) -> str:
    joined = ", ".join(selected_vocab)
    return (
        f"Create 3 grammatically and orthographically flawed {language} sentences with "
        f"register: {niveau}, using these vocabs (understandable at CEFR {level}): "
        f"{joined}. Do NOT provide the corrected sentences."
    )


def build_conjugation_prompt(*, language: str, level: str, vocab_list: list[str]) -> list[dict]:
    joined = ", ".join(vocab_list)
    return [
        {
            "role": "system",
            "content": "Give single-word answers whenever possible — no numbering, no period.",
        },
        {
            "role": "user",
            "content": (
                f"Pick, matching CEFR level {level}, either (a) a random verb from this "
                f"vocabulary list: {joined}, or (b) any irregular {language} verb. "
                f"It MUST be a verb (action word)."
            ),
        },
    ]


def build_correction_prompt(
    *,
    language: str,
    niveau: str,
    mentor: str,
    task: str,
    user_text: str,
    ui_language_name: str = "English",
) -> list[dict]:
    return [
        {
            "role": "system",
            "content": (
                f"You are a native {language.capitalize()} teacher. Correct the text below "
                f"at native-speaker level. Consider the given task. The learner writes in "
                f"register: {niveau}. Give feedback in the voice and style of {mentor}. Be concise.\n\n"
                f"IMPORTANT: Respond entirely in {ui_language_name}. Do not mix languages.\n\n"
                f"CORRECTION RULES:\n"
                f"1. Accept ALL grammatically correct forms — verify subject-verb agreement, "
                f"tense, and mood BEFORE marking something as an error.\n"
                f"2. For cloze exercises: vocabulary may appear conjugated, declined, or "
                f"pluralized. If the subject is plural, a 3rd-person-plural verb form is correct.\n"
                f"3. For cloze exercises: if MULTIPLE vocab choices from the given list fit "
                f"semantically in a blank, accept ALL of them. Only flag actual errors.\n"
                f"4. False positives are worse than no correction — if uncertain whether "
                f"something is an error, stay silent. Don't nit-pick phrasing.\n"
                f"5. If the learner made no mistakes, say so clearly — do not invent errors."
            ),
        },
        {"role": "user", "content": f"Task: {task}\n\nLearner's answer: {user_text}"},
    ]


def build_dictation_text_prompt(
    *, language: str, level: str, niveau: str, sentences: int = 3,
) -> list[dict]:
    """Ask the LLM to produce a short text in the learning language for dictation."""
    return [
        {
            "role": "system",
            "content": (
                f"You generate short dictation texts for {language} learners. "
                f"Output ONLY the text itself — no title, no introduction, no "
                f"commentary. The text must be in {language}, grammatically correct, "
                f"natural-sounding, and use punctuation that is audible (commas, "
                f"periods, question marks). No quotation marks around the whole thing."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Generate a {sentences}-sentence dictation text in {language}. "
                f"CEFR level: {level}. Register: {niveau}. "
                f"Make it coherent — a small scene, thought, or micro-story — not "
                f"disconnected sentences. Keep the overall length under ~60 words."
            ),
        },
    ]


def build_answer_comment_prompt(comment: str) -> list[dict]:
    return [
        {"role": "system", "content": "Beantworte die folgende Frage sachlich und präzise."},
        {"role": "user", "content": comment},
    ]
