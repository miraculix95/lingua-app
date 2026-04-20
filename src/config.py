"""Static configuration constants for franz-lern.

Everything that used to be top-of-file globals in franz-lern-streamlit.py lives
here. Kept pure (no imports beyond stdlib) so tests stay fast.
"""
from __future__ import annotations

LEVELS: list[str] = ["A1", "A2", "B1", "B2", "C1", "C2"]

NIVEAU_LEVELS: list[str] = [
    "Gossensprache/Kriminelle Sprache",
    "Argot/Vulgär",
    "Umgangssprache",
    "Standardsprache",
    "Gehoben/Vornehm",
    "Hohe Literatur",
    "Technisch",
]

LANGUAGES: list[str] = [
    "französisch",
    "englisch",
    "spanisch",
    "ukrainisch",
    "deutsch",
]

MENTORS: list[str] = [
    "Netter Lehrer",
    "Strenger Lehrer",
    "Dalai Lama",
    "Vitalik Buterin",
    "Elon Musk",
    "Jesus Christus",
    "Chairman Mao",
    "Homer",
    "Konfuzius",
    "Machiavelli",
]

MENTOR_AVATARS: dict[str, str] = {
    "Netter Lehrer": "🎓",
    "Strenger Lehrer": "📏",
    "Dalai Lama": "🧘",
    "Vitalik Buterin": "⛓️",
    "Elon Musk": "🚀",
    "Jesus Christus": "✝️",
    "Chairman Mao": "🌾",
    "Homer": "📜",
    "Konfuzius": "🏯",
    "Machiavelli": "🗡️",
}

MENTOR_QUOTES: dict[str, str] = {
    "Netter Lehrer": "Jeder Fehler ist ein Schritt nach vorne.",
    "Strenger Lehrer": "Präzision ist die Höflichkeit der Könige.",
    "Dalai Lama": "Be kind whenever possible. It is always possible.",
    "Vitalik Buterin": "Decentralization of power; centralization of knowledge.",
    "Elon Musk": "When something is important enough, you do it even if the odds are not in your favor.",
    "Jesus Christus": "Der Buchstabe tötet, der Geist macht lebendig.",
    "Chairman Mao": "Eine Reise von tausend Meilen beginnt mit dem ersten Schritt.",
    "Homer": "Even in sleep, sorrow descends upon our souls.",
    "Konfuzius": "Lernen ohne Nachdenken ist vergeblich; Nachdenken ohne Lernen ist gefährlich.",
    "Machiavelli": "Fortune favors the bold.",
}

THEMES: list[str] = [
    "Urlaub",
    "Schule",
    "Essen",
    "Sport",
    "Kultur",
    "Medien",
    "Raumfahrt",
    "Business",
    "Politik",
]

# OpenRouter model IDs (https://openrouter.ai/models).
# 4-tier selection: budget / balanced / premium / best.
# See research/2026-04-20-model-provider-analysis.md for the rationale.
MODEL_TIERS: dict[str, str] = {
    "💰 Budget (Gemini Flash Lite)": "google/gemini-2.5-flash-lite",
    "⚖️ Balanced (Claude Haiku 4.5)": "anthropic/claude-haiku-4.5",
    "🚀 Premium (Mistral Large 3)": "mistralai/mistral-large-2512",
    "👑 Best (Claude Sonnet 4.6)": "anthropic/claude-sonnet-4.6",
}

MODELS: list[str] = list(MODEL_TIERS.values())

# Default picked by learning-language — cyrillic languages need UK-safe model.
DEFAULT_MODEL: str = "google/gemini-2.5-flash-lite"
DEFAULT_MODEL_UK: str = "anthropic/claude-haiku-4.5"

DEFAULT_LANGUAGE: str = "französisch"


def default_model_for_language(language: str) -> str:
    """Pick a sensible default model based on target language.

    Ukrainian uses Cyrillic + Slavic grammar; smaller models hallucinate
    there. Haiku is the cheapest option that handles it reliably.
    """
    if language.lower().startswith("ukrain"):
        return DEFAULT_MODEL_UK
    return DEFAULT_MODEL

RADIO_CHANNELS: dict[str, str] = {
    "France Info": "http://icecast.radiofrance.fr/franceinfo-midfi.mp3",
    "France Inter": "http://icecast.radiofrance.fr/franceinter-midfi.mp3",
    "France Culture": "http://icecast.radiofrance.fr/franceculture-midfi.mp3",
    "BFM Radio": "https://audio.bfmtv.com/bfmradio_128.mp3",
}

TASK_LIST: list[str] = [
    "",
    "Schreiben eines Textes und danach Korrektur",
    "Ausfüllen eines Lückentextes in Fremdsprache",
    "Vorgabe von deutschen Sätzen zum Übersetzen",
    "Vokabel-Quiz",
    "Satzbauübung",
    "Fehler im Text finden und korrigieren",
    "Synonyme und Antonyme finden",
    "Verbkonjugation üben",
    "Radio hören und aufnehmen",
]

NO_ANSWERS_HINT: str = " Nenne nicht die Antworten. "
