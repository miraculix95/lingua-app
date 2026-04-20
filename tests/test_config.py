from src.config import (
    DEFAULT_LANGUAGE,
    DEFAULT_MODEL,
    LANGUAGES,
    LEVELS,
    MENTORS,
    MODELS,
    NIVEAU_LEVELS,
    RADIO_CHANNELS,
    THEMES,
)


def test_levels_are_cefr():
    assert LEVELS == ["A1", "A2", "B1", "B2", "C1", "C2"]


def test_languages_contain_core_set():
    for lang in ["französisch", "englisch", "spanisch", "deutsch"]:
        assert lang in LANGUAGES


def test_default_model_is_in_models_list():
    assert DEFAULT_MODEL in MODELS


def test_default_language_is_in_languages():
    assert DEFAULT_LANGUAGE in LANGUAGES


def test_radio_channels_have_urls():
    assert "France Info" in RADIO_CHANNELS
    assert RADIO_CHANNELS["France Info"].startswith("http")


def test_niveau_levels_spans_register_range():
    assert "Standardsprache" in NIVEAU_LEVELS
    assert "Technisch" in NIVEAU_LEVELS


def test_mentors_list_not_empty():
    assert len(MENTORS) >= 5


def test_themes_list_not_empty():
    assert len(THEMES) >= 5


def test_no_deprecated_models():
    # gpt-4-0613 was retired; anything hardcoded to it would break silently.
    assert "gpt-4-0613" not in MODELS
