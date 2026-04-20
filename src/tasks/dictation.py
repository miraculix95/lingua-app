"""Dictation task: LLM generates text → ElevenLabs TTS → audio for learner.

Flow:
    1. Ask the learning-language LLM for a short coherent text.
    2. Pipe it through ElevenLabs Multilingual v2 for speech.
    3. Return bytes + original text; UI plays the audio with a speed slider
       and hides the text until the learner clicks "reveal".
"""
from __future__ import annotations

from typing import Any

import requests

from src.logging_setup import get_logger
from src.prompts import build_dictation_text_prompt
from src.tasks.base import TaskInstruction

log = get_logger(__name__)

# Bella — warm, clear, works well across EN/FR/DE/ES/IT/PT multilingual.
DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


class TTSUnavailable(RuntimeError):
    """Raised when no ElevenLabs key is configured or the API call fails."""


def generate_text(
    client: Any,
    *,
    language: str,
    level: str,
    niveau: str,
    model: str,
    sentences: int = 3,
) -> str:
    messages = build_dictation_text_prompt(
        language=language, level=level, niveau=niveau, sentences=sentences,
    )
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content.strip()


def synthesize_speech(
    text: str,
    *,
    api_key: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = "eleven_multilingual_v2",
    timeout: float = 30.0,
) -> bytes:
    """Call ElevenLabs TTS, return raw MP3 bytes.

    Raises TTSUnavailable on auth / network / quota errors so the UI can
    gracefully show a fallback message without crashing.
    """
    if not api_key:
        raise TTSUnavailable("No ELEVENLABS_KEY configured.")
    url = ELEVENLABS_TTS_URL.format(voice_id=voice_id)
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=timeout)
    except requests.exceptions.RequestException as exc:
        log.warning("ElevenLabs network error: %s", exc)
        raise TTSUnavailable(f"Network error: {exc}") from exc
    if r.status_code != 200:
        log.warning("ElevenLabs HTTP %s: %s", r.status_code, r.text[:200])
        raise TTSUnavailable(f"HTTP {r.status_code}: {r.text[:200]}")
    return r.content


def build(
    client: Any,
    *,
    language: str,
    level: str,
    niveau: str,
    model: str,
    elevenlabs_key: str,
    sentences: int = 3,
) -> TaskInstruction:
    """Produce a dictation instruction with audio bytes in the context."""
    text = generate_text(
        client, language=language, level=level, niveau=niveau, model=model,
        sentences=sentences,
    )
    audio_bytes = synthesize_speech(text, api_key=elevenlabs_key)
    return TaskInstruction(
        displayed_to_user="",  # UI shows audio player, not the text, until reveal
        internal_context={"text": text, "audio": audio_bytes},
    )
