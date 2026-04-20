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

MODELS: list[str] = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4-turbo",
]

DEFAULT_MODEL: str = "gpt-4o-mini"
DEFAULT_LANGUAGE: str = "französisch"

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
