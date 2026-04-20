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
        f"Du bist ein Sprachlehrer. Extrahiere genau {number} {language}e Vokabeln "
        f"oder Redewendungen passend zum Mindest-Sprachniveau {level} aus dem folgenden "
        f"Text. Erstelle dabei eine gute Mischung aus Verben, komplexen Ausdrücken, "
        f"Adjektiven und Nomen. Vermeide Eigennamen und geographische Namen. "
        f"Gib die Vokabeln als durch Kommas getrennte Liste ohne Nummerierung zurück. "
        f"Gib das Ergebnis ohne Einleitung und Kommentar an."
    )


def build_vocab_autogen_prompt(*, language: str, level: str, niveau: str) -> str:
    return (
        f"Erstelle in Python-Format eine Liste von 20 {language}n Vokabeln inklusive "
        f"Verben. Die Sprache ist {language}. Die Wörter sollen passend zum Mindest-"
        f"Sprachniveau {level} sein, das folgende Sprachregister treffen: {niveau}. "
        f"Wähle thematisch zueinander passende Wörter aus."
    )


def build_cloze_messages(
    *,
    language: str,
    level: str,
    niveau: str,
    selected_vocab: list[str],
    number_trous: int,
) -> list[dict]:
    """Messages für strukturierte Cloze-Generierung via ``emit_cloze`` tool.

    Die Lösungen landen über das Tool-Schema in einem separaten Feld —
    der ``body``-String enthält ausschließlich ``___``-Platzhalter.
    """
    joined = ", ".join(selected_vocab)
    return [
        {
            "role": "system",
            "content": (
                f"Du bist ein Sprachlehrer für {language}. Erstelle Lückentexte für "
                f"Sprachlerner. WICHTIG: nutze das emit_cloze-Tool für strukturierte "
                f"Ausgabe — Lösungen kommen AUSSCHLIESSLICH ins 'answers'-Feld. "
                f"Der 'body' enthält nur '___' für Lücken, KEINE Lösungs-Hinweise."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Erstelle einen {language}en Lückentext mit folgenden Vokabeln: "
                f"{joined}. Sprachlevel: {level}. Sprachregister: {niveau}. "
                f"Genau {number_trous} Lücken, jede Lücke als '___' markiert. "
                f"Jede Vokabel genau einmal, in passender grammatischer Form "
                f"(Konjugation, Plural, etc.). "
                f"Der Text soll logisch Sinn machen und eine kleine Geschichte oder "
                f"einen Kontext bilden. Gib dazu einen passenden Titel aus. "
                f"'vocab_hints': eine kurze deutsche Bedeutungs-Erklärung je Vokabel. "
                f"'answers': die tatsächlich eingesetzten Wörter in der Reihenfolge "
                f"der Lücken im Body."
            ),
        },
    ]


def build_translation_prompt(
    *,
    language: str,
    level: str,
    niveau: str,
    selected_vocab: list[str],
    number_sentences: int,
) -> str:
    joined = ", ".join(selected_vocab)
    return (
        f"Übersetze die folgenden {language}en Vokabeln ins Deutsche: {joined}. "
        f"Erstelle dann {number_sentences} deutsche Sätze zum Übersetzen ins "
        f"{language}e für das Sprachregister {niveau} und das Sprachlevel {level}. "
        f"Gib die Lösung (die {language}en Sätze) nicht an.{NO_ANSWERS_HINT}"
        f"\n\nAusgabeformat:\nÜbersetze die Sätze: nummeriert.\n---\n"
        f"Benutze die folgenden Vokabeln ({language} - deutsch): als Bulletpoints."
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
        f"Erstelle einen {language}en Satz mit den folgenden Wörtern: {words}. "
        f"Benutze dabei das folgende Sprachregister: {niveau} und das folgende "
        f"Sprachlevel: {level}.{NO_ANSWERS_HINT}"
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
        f"Erstelle 3 grammatikalisch und orthografisch stark fehlerhafte {language}e "
        f"Sätze mit dem folgenden Sprachregister: {niveau} mit den folgenden Vokabeln, "
        f"die für einen Lernenden des Sprachlevels {level} verständlich sind. "
        f"Gib die korrekten Sätze nicht an: {joined}."
    )


def build_conjugation_prompt(*, language: str, level: str, vocab_list: list[str]) -> list[dict]:
    joined = ", ".join(vocab_list)
    return [
        {
            "role": "system",
            "content": "Gib einwortige Antworten wann immer möglich, ohne Nummerierung, ohne Punkt.",
        },
        {
            "role": "user",
            "content": (
                f"Wähle passend zum Sprachlevel {level} entweder a) zufällig ein Verb "
                f"aus der angehängten Vokabelliste aus: {joined}, oder b) ein beliebiges "
                f"unregelmäßiges Verb. Es muss ein Verb (Tunwort) sein."
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
) -> list[dict]:
    return [
        {
            "role": "system",
            "content": (
                f"Du bist ein muttersprachlicher {language.capitalize()}-Lehrer. Korrigiere den "
                f"folgenden Text auf Native-Speaker-Niveau. Beachte die Aufgabenstellung. "
                f"Der Nutzer verwendet das Sprachregister: {niveau}. Gib Feedback im Stile von {mentor}. "
                f"Halte dich kurz.\n\n"
                f"KORREKTUR-REGELN:\n"
                f"1. Akzeptiere ALLE grammatisch korrekten Formen — prüfe Subjekt-Verb-Kongruenz, "
                f"Tempus und Modus bevor du etwas als Fehler markierst.\n"
                f"2. Bei Lückentexten (Cloze): die Vokabeln dürfen konjugiert / dekliniert / "
                f"im Plural vorkommen. Wenn 'personnes' im Subjekt steht und die Lücke nach "
                f"einem Hilfsverb sinnvoll ein Verb braucht, ist 3. Person Plural korrekt.\n"
                f"3. Bei Lückentexten: wenn mehrere Vokabeln aus der gegebenen Liste semantisch "
                f"sinnvoll in eine Lücke passen, akzeptiere ALLE. Markiere nur wirkliche Fehler.\n"
                f"4. Falsch-Positive sind schlimmer als keine Korrektur — wenn du dir unsicher bist, "
                f"ob etwas ein Fehler ist, sag es nicht. Nicht pingelig wegen des Ausdrucks sein.\n"
                f"5. Wenn der User keinen Fehler gemacht hat, sag das klar — keine erfundenen Fehler."
            ),
        },
        {"role": "user", "content": f"Aufgabe: {task}\n\nAntwort des Benutzers: {user_text}"},
    ]


def build_answer_comment_prompt(comment: str) -> list[dict]:
    return [
        {"role": "system", "content": "Beantworte die folgende Frage sachlich und präzise."},
        {"role": "user", "content": comment},
    ]
