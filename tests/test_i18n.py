from src.i18n import (
    DEFAULT_UI_LANG,
    TASK_KEYS,
    UI_LANG_NAMES,
    UI_LANGS,
    _from_accept_language,
    detect_ui_language,
    t,
    task_names_for,
)


def test_default_lang_is_english():
    assert DEFAULT_UI_LANG == "en"


def test_all_ui_langs_have_names():
    for code in UI_LANG_NAMES.keys():
        assert code in {"en", "de", "fr", "es"}


def test_ui_langs_dict_matches_lang_names():
    assert set(UI_LANGS.values()) == set(UI_LANG_NAMES.keys())


def test_t_returns_english_by_default():
    assert "Coach" in t("coach_and_style")


def test_t_falls_back_to_english_for_unknown_lang():
    en = t("correct_btn", "en")
    assert t("correct_btn", "klingon") == en


def test_t_formats_kwargs():
    result = t("app_title", "en", language="French")
    assert "French" in result


def test_task_names_for_all_langs_have_same_length():
    lengths = {lang: len(task_names_for(lang)) for lang in ["en", "de", "fr", "es"]}
    assert len(set(lengths.values())) == 1, f"Task-name lists differ in length: {lengths}"
    assert all(v == len(TASK_KEYS) for v in lengths.values())


def test_accept_language_parses_primary():
    assert _from_accept_language("de-DE,de;q=0.9,en;q=0.8") == "de"
    assert _from_accept_language("fr-CA,fr;q=0.9") == "fr"
    assert _from_accept_language("en-US") == "en"
    assert _from_accept_language("es") == "es"
    assert _from_accept_language("ja") is None  # not supported → None → caller falls back


def test_detect_falls_back_to_english():
    # No headers at all → English.
    assert detect_ui_language(None, None) == "en"


def test_detect_uses_accept_language_when_no_ip():
    assert detect_ui_language(None, "de-DE,de;q=0.9") == "de"
    assert detect_ui_language(None, "fr-FR") == "fr"
