"""Minimal UI-localization.

Covers the four UI languages we expose: EN (default), DE, FR, ES. The LEARNING
target language is independent — a user can have the UI in English while
learning French.

Task-types are identified by stable keys (TASK_KEYS) so the app dispatches on
identifiers, not on localized display strings. The display list is built per
UI-language via ``task_names_for(lang)``.
"""
from __future__ import annotations

UI_LANGS: dict[str, str] = {
    "English": "en",
    "Deutsch": "de",
    "Français": "fr",
    "Español": "es",
}

UI_LANG_NAMES: dict[str, str] = {
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
}

DEFAULT_UI_LANG: str = "en"


# Task keys are stable across languages — used for dispatch in app.py.
# Empty key "" represents the unselected state.
TASK_KEYS: list[str] = [
    "",
    "writing",
    "cloze",
    "translation",
    "quiz",
    "sentence",
    "error",
    "synonym",
    "conjugation",
    "radio",
]


_TASK_NAMES: dict[str, list[str]] = {
    "en": [
        "",
        "Write a text and get feedback",
        "Fill in a cloze text",
        "Translate German sentences",
        "Vocabulary quiz",
        "Build a sentence",
        "Find and fix errors",
        "Synonyms and antonyms",
        "Verb conjugation",
        "Listen to radio",
    ],
    "de": [
        "",
        "Text schreiben und korrigieren",
        "Lückentext ausfüllen",
        "Deutsche Sätze übersetzen",
        "Vokabel-Quiz",
        "Satz bauen",
        "Fehler finden und korrigieren",
        "Synonyme und Antonyme",
        "Verb konjugieren",
        "Radio hören",
    ],
    "fr": [
        "",
        "Rédiger un texte et le faire corriger",
        "Remplir un texte à trous",
        "Traduire des phrases allemandes",
        "Quiz de vocabulaire",
        "Construire une phrase",
        "Trouver et corriger les erreurs",
        "Synonymes et antonymes",
        "Conjugaison des verbes",
        "Écouter la radio",
    ],
    "es": [
        "",
        "Escribir un texto y recibir corrección",
        "Completar un texto con huecos",
        "Traducir frases en alemán",
        "Quiz de vocabulario",
        "Construir una frase",
        "Encontrar y corregir errores",
        "Sinónimos y antónimos",
        "Conjugación de verbos",
        "Escuchar la radio",
    ],
}


def task_names_for(ui_lang: str) -> list[str]:
    return list(_TASK_NAMES.get(ui_lang, _TASK_NAMES["en"]))


_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "app_title": "{language} — Language Tutor",
        "meta_hint": "💡 Wrap out-of-band questions in angle brackets, e.g. `<what does passé composé mean?>` — you get a separate answer.",
        "sidebar_title": "🇫🇷 Learn {language}",
        "ui_language": "🌍 Interface language",
        "dark_mode": "🌙 Dark mode",
        "coach_and_style": "👤 Coach & Style",
        "vocab_source": "📚 Vocabulary source",
        "model_api": "🤖 Model & API",
        "coach": "Coach",
        "level": "Language level",
        "register": "Register",
        "txt_files": "Txt files",
        "txt_files_help": "Extracts vocabulary at the selected level.",
        "num_vocab": "Number of vocabs",
        "webpage_url": "Webpage URL",
        "ready_vocab_file": "Ready vocab file",
        "api_key": "🔑 OpenRouter API key",
        "api_key_help": "Your key. Stays in session, never stored. Get one at openrouter.ai/keys.",
        "model_tier": "Model tier",
        "key_source_byok": "✅ Your key (BYOK)",
        "key_source_or": "🔑 Server .env (OpenRouter)",
        "key_source_oa": "⚠️ Server .env (OpenAI fallback)",
        "key_source_none": "❌ No key found",
        "key_source_label": "Key source",
        "metric_tasks": "📚 Tasks",
        "metric_corrections": "✏️ Corrections",
        "metric_runs": "🔄 Session runs",
        "choose_exercise": "🎯 Choose exercise",
        "new_task_btn": "🎯 New task",
        "correct_btn": "📝 Correct text",
        "task_heading": "Task",
        "your_answer": "✏️ Your answer:",
        "your_answer_placeholder": "Write in {language}… Embed meta-questions in <>.",
        "no_vocab_info": "No vocabulary loaded. Use a source above or:",
        "autogen_vocab_btn": "🎲 Auto-generate vocabulary",
        "status_extract_file": "📚 Extracting vocabulary from file…",
        "status_load_url": "🌐 Loading {url}…",
        "status_extract_web": "🧠 Extracting vocabulary…",
        "status_extracted_ok": "✅ {n} vocabs extracted",
        "status_extract_web_ok": "✅ {n} vocabs from web",
        "status_generating_task": "🧠 {task}…",
        "status_task_ready": "✅ Task ready",
        "status_generating_vocab": "🧠 Generating vocabulary…",
        "status_gen_vocab_ok": "✅ {n} vocabs generated",
        "status_coach_reading": "🧠 {mentor} is reading…",
        "status_feedback_ready": "✅ Feedback ready",
        "status_generating_quiz": "🧠 Generating quiz…",
        "status_quiz_ready": "✅ Quiz ready",
        "vocab_loaded_ok": "✅ {n} vocabs loaded",
        "num_blanks": "Number of blanks",
        "num_sentences": "Number of sentences",
        "error_no_key": "🔑 No API key. Enter your OpenRouter key in the sidebar.",
        "error_no_key_hint": "💡 Get one at https://openrouter.ai/keys — the key stays only in your session.",
        "radio_unavailable": "🔇 Audio output not available (headless server). Radio task only works locally.",
        "radio_channel": "📻 Channel",
        "radio_info": "Streaming core in `src/tasks/radio.py`. Transcription is on the roadmap.",
        "quiz_new_btn": "🎲 New quiz",
        "quiz_evaluate_btn": "✅ Evaluate",
        "quiz_score": "🎯 Score",
        "quiz_prompt_format": "What is the {language} word for '{trans}'?",
        "side_questions": "**Side questions:**",
    },
    "de": {
        "app_title": "{language} — Lernprogramm",
        "meta_hint": "💡 Out-of-band-Fragen in spitzen Klammern einbetten, z.B. `<was heißt passé composé?>` — bekommst separate Antwort.",
        "sidebar_title": "🇫🇷 {language} lernen",
        "ui_language": "🌍 UI-Sprache",
        "dark_mode": "🌙 Dark Mode",
        "coach_and_style": "👤 Coach & Stil",
        "vocab_source": "📚 Vokabelquelle",
        "model_api": "🤖 Modell & API",
        "coach": "Coach",
        "level": "Sprachniveau",
        "register": "Sprachregister",
        "txt_files": "Txt-Dateien",
        "txt_files_help": "Extrahiert Vokabeln auf dem eingestellten Niveau.",
        "num_vocab": "Anzahl Vokabeln",
        "webpage_url": "Webseite-URL",
        "ready_vocab_file": "Fertige Vokabel-Datei",
        "api_key": "🔑 OpenRouter API-Key",
        "api_key_help": "Dein Key. Bleibt in Session, wird nie gespeichert. Hol einen auf openrouter.ai/keys.",
        "model_tier": "Modell-Tier",
        "key_source_byok": "✅ Dein Key (BYOK)",
        "key_source_or": "🔑 Server .env (OpenRouter)",
        "key_source_oa": "⚠️ Server .env (OpenAI-Fallback)",
        "key_source_none": "❌ Kein Key gefunden",
        "key_source_label": "Key-Quelle",
        "metric_tasks": "📚 Aufgaben",
        "metric_corrections": "✏️ Korrekturen",
        "metric_runs": "🔄 Session-Runs",
        "choose_exercise": "🎯 Übung wählen",
        "new_task_btn": "🎯 Neue Aufgabe",
        "correct_btn": "📝 Text korrigieren",
        "task_heading": "Aufgabe",
        "your_answer": "✏️ Deine Antwort:",
        "your_answer_placeholder": "Schreib auf {language}… Meta-Fragen in <> einbetten.",
        "no_vocab_info": "Keine Vokabeln geladen. Lade eine Quelle oben oder:",
        "autogen_vocab_btn": "🎲 Vokabelliste automatisch generieren",
        "status_extract_file": "📚 Extrahiere Vokabeln aus Datei…",
        "status_load_url": "🌐 Lade {url}…",
        "status_extract_web": "🧠 Extrahiere Vokabeln…",
        "status_extracted_ok": "✅ {n} Vokabeln extrahiert",
        "status_extract_web_ok": "✅ {n} Vokabeln aus Web",
        "status_generating_task": "🧠 {task}…",
        "status_task_ready": "✅ Aufgabe bereit",
        "status_generating_vocab": "🧠 Generiere Vokabeln…",
        "status_gen_vocab_ok": "✅ {n} Vokabeln generiert",
        "status_coach_reading": "🧠 {mentor} liest mit…",
        "status_feedback_ready": "✅ Feedback bereit",
        "status_generating_quiz": "🧠 Generiere Quiz…",
        "status_quiz_ready": "✅ Quiz bereit",
        "vocab_loaded_ok": "✅ {n} Vokabeln geladen",
        "num_blanks": "Wortlücken",
        "num_sentences": "Anzahl Sätze",
        "error_no_key": "🔑 Kein API-Key. Gib deinen OpenRouter-Key in der Sidebar ein.",
        "error_no_key_hint": "💡 Hol einen auf https://openrouter.ai/keys — der Key bleibt nur in deiner Session.",
        "radio_unavailable": "🔇 Audio-Output nicht verfügbar (headless-Server). Radio-Task funktioniert nur lokal.",
        "radio_channel": "📻 Kanal",
        "radio_info": "Streaming-Kern in `src/tasks/radio.py`. Transkription folgt (Roadmap).",
        "quiz_new_btn": "🎲 Neues Quiz",
        "quiz_evaluate_btn": "✅ Auswerten",
        "quiz_score": "🎯 Score",
        "quiz_prompt_format": "Was ist das {language}e Wort für '{trans}'?",
        "side_questions": "**Nebenfragen:**",
    },
    "fr": {
        "app_title": "{language} — Tuteur de langue",
        "meta_hint": "💡 Entoure tes questions hors-sujet de chevrons, par ex. `<que veut dire passé composé ?>` — tu reçois une réponse à part.",
        "sidebar_title": "🇫🇷 Apprendre le {language}",
        "ui_language": "🌍 Langue de l'interface",
        "dark_mode": "🌙 Mode sombre",
        "coach_and_style": "👤 Coach & Style",
        "vocab_source": "📚 Source de vocabulaire",
        "model_api": "🤖 Modèle & API",
        "coach": "Coach",
        "level": "Niveau",
        "register": "Registre",
        "txt_files": "Fichiers Txt",
        "txt_files_help": "Extrait le vocabulaire au niveau choisi.",
        "num_vocab": "Nombre de mots",
        "webpage_url": "URL de la page",
        "ready_vocab_file": "Fichier de vocabulaire",
        "api_key": "🔑 Clé API OpenRouter",
        "api_key_help": "Ta clé. Reste en session, jamais stockée. Obtiens-en une sur openrouter.ai/keys.",
        "model_tier": "Palier du modèle",
        "key_source_byok": "✅ Ta clé (BYOK)",
        "key_source_or": "🔑 Serveur .env (OpenRouter)",
        "key_source_oa": "⚠️ Serveur .env (OpenAI)",
        "key_source_none": "❌ Pas de clé trouvée",
        "key_source_label": "Source de la clé",
        "metric_tasks": "📚 Exercices",
        "metric_corrections": "✏️ Corrections",
        "metric_runs": "🔄 Sessions",
        "choose_exercise": "🎯 Choisir un exercice",
        "new_task_btn": "🎯 Nouvel exercice",
        "correct_btn": "📝 Corriger le texte",
        "task_heading": "Exercice",
        "your_answer": "✏️ Ta réponse :",
        "your_answer_placeholder": "Écris en {language}… Questions méta entre <>.",
        "no_vocab_info": "Aucun vocabulaire chargé. Utilise une source ci-dessus ou :",
        "autogen_vocab_btn": "🎲 Générer une liste automatiquement",
        "status_extract_file": "📚 Extraction depuis le fichier…",
        "status_load_url": "🌐 Chargement de {url}…",
        "status_extract_web": "🧠 Extraction du vocabulaire…",
        "status_extracted_ok": "✅ {n} mots extraits",
        "status_extract_web_ok": "✅ {n} mots depuis le web",
        "status_generating_task": "🧠 {task}…",
        "status_task_ready": "✅ Exercice prêt",
        "status_generating_vocab": "🧠 Génération du vocabulaire…",
        "status_gen_vocab_ok": "✅ {n} mots générés",
        "status_coach_reading": "🧠 {mentor} lit ta réponse…",
        "status_feedback_ready": "✅ Feedback prêt",
        "status_generating_quiz": "🧠 Génération du quiz…",
        "status_quiz_ready": "✅ Quiz prêt",
        "vocab_loaded_ok": "✅ {n} mots chargés",
        "num_blanks": "Nombre de trous",
        "num_sentences": "Nombre de phrases",
        "error_no_key": "🔑 Pas de clé API. Saisis ta clé OpenRouter dans la barre latérale.",
        "error_no_key_hint": "💡 Obtiens-en une sur https://openrouter.ai/keys — la clé reste dans ta session.",
        "radio_unavailable": "🔇 Sortie audio indisponible (serveur headless). Exercice radio en local uniquement.",
        "radio_channel": "📻 Chaîne",
        "radio_info": "Moteur de streaming dans `src/tasks/radio.py`. Transcription à venir (roadmap).",
        "quiz_new_btn": "🎲 Nouveau quiz",
        "quiz_evaluate_btn": "✅ Évaluer",
        "quiz_score": "🎯 Score",
        "quiz_prompt_format": "Quel est le mot en {language} pour « {trans} » ?",
        "side_questions": "**Questions méta :**",
    },
    "es": {
        "app_title": "{language} — Tutor de idiomas",
        "meta_hint": "💡 Envuelve tus preguntas meta en corchetes angulares, p.ej. `<¿qué significa passé composé?>` — recibes una respuesta aparte.",
        "sidebar_title": "🇫🇷 Aprender {language}",
        "ui_language": "🌍 Idioma de la interfaz",
        "dark_mode": "🌙 Modo oscuro",
        "coach_and_style": "👤 Coach y estilo",
        "vocab_source": "📚 Fuente de vocabulario",
        "model_api": "🤖 Modelo y API",
        "coach": "Coach",
        "level": "Nivel",
        "register": "Registro",
        "txt_files": "Archivos Txt",
        "txt_files_help": "Extrae vocabulario al nivel elegido.",
        "num_vocab": "Número de palabras",
        "webpage_url": "URL de la página",
        "ready_vocab_file": "Archivo de vocabulario",
        "api_key": "🔑 Clave API de OpenRouter",
        "api_key_help": "Tu clave. Solo en la sesión, nunca se guarda. Consigue una en openrouter.ai/keys.",
        "model_tier": "Nivel del modelo",
        "key_source_byok": "✅ Tu clave (BYOK)",
        "key_source_or": "🔑 Servidor .env (OpenRouter)",
        "key_source_oa": "⚠️ Servidor .env (OpenAI)",
        "key_source_none": "❌ No se encontró clave",
        "key_source_label": "Fuente de la clave",
        "metric_tasks": "📚 Ejercicios",
        "metric_corrections": "✏️ Correcciones",
        "metric_runs": "🔄 Sesiones",
        "choose_exercise": "🎯 Elegir ejercicio",
        "new_task_btn": "🎯 Nuevo ejercicio",
        "correct_btn": "📝 Corregir texto",
        "task_heading": "Ejercicio",
        "your_answer": "✏️ Tu respuesta:",
        "your_answer_placeholder": "Escribe en {language}… Preguntas meta entre <>.",
        "no_vocab_info": "No hay vocabulario cargado. Usa una fuente arriba o:",
        "autogen_vocab_btn": "🎲 Generar lista automáticamente",
        "status_extract_file": "📚 Extrayendo del archivo…",
        "status_load_url": "🌐 Cargando {url}…",
        "status_extract_web": "🧠 Extrayendo vocabulario…",
        "status_extracted_ok": "✅ {n} palabras extraídas",
        "status_extract_web_ok": "✅ {n} palabras desde la web",
        "status_generating_task": "🧠 {task}…",
        "status_task_ready": "✅ Ejercicio listo",
        "status_generating_vocab": "🧠 Generando vocabulario…",
        "status_gen_vocab_ok": "✅ {n} palabras generadas",
        "status_coach_reading": "🧠 {mentor} está leyendo…",
        "status_feedback_ready": "✅ Feedback listo",
        "status_generating_quiz": "🧠 Generando quiz…",
        "status_quiz_ready": "✅ Quiz listo",
        "vocab_loaded_ok": "✅ {n} palabras cargadas",
        "num_blanks": "Número de huecos",
        "num_sentences": "Número de frases",
        "error_no_key": "🔑 No hay clave API. Introduce tu clave OpenRouter en la barra lateral.",
        "error_no_key_hint": "💡 Consigue una en https://openrouter.ai/keys — la clave solo vive en tu sesión.",
        "radio_unavailable": "🔇 Salida de audio no disponible (servidor headless). El ejercicio de radio solo funciona en local.",
        "radio_channel": "📻 Canal",
        "radio_info": "Motor de streaming en `src/tasks/radio.py`. Transcripción próximamente (roadmap).",
        "quiz_new_btn": "🎲 Nuevo quiz",
        "quiz_evaluate_btn": "✅ Evaluar",
        "quiz_score": "🎯 Puntuación",
        "quiz_prompt_format": "¿Cuál es la palabra en {language} para «{trans}»?",
        "side_questions": "**Preguntas laterales:**",
    },
}


# Country → UI-lang mapping for IP-based auto-detection.
_COUNTRY_TO_LANG: dict[str, str] = {
    # German-speaking
    "DE": "de", "AT": "de", "CH": "de", "LI": "de",
    # French-speaking (primary)
    "FR": "fr", "MC": "fr", "LU": "fr", "BE": "fr", "SN": "fr", "CI": "fr",
    "CM": "fr", "CD": "fr", "MG": "fr", "HT": "fr",
    # Spanish-speaking
    "ES": "es", "MX": "es", "AR": "es", "CO": "es", "PE": "es", "CL": "es",
    "VE": "es", "EC": "es", "GT": "es", "BO": "es", "CU": "es", "DO": "es",
    "HN": "es", "PY": "es", "NI": "es", "SV": "es", "CR": "es", "PA": "es",
    "UY": "es", "PR": "es",
    # English-speaking (default everywhere else)
    "US": "en", "GB": "en", "IE": "en", "CA": "en", "AU": "en", "NZ": "en",
}


def _from_accept_language(accept: str) -> str | None:
    """Parse browser Accept-Language header into our UI-lang code."""
    if not accept:
        return None
    primary = accept.split(",")[0].split(";")[0].split("-")[0].strip().lower()
    return primary if primary in UI_LANG_NAMES else None


def _from_ip(ip: str, timeout: float = 2.0) -> str | None:
    """Call ipapi.co to get country → map to UI-lang. Quiet on errors."""
    if not ip or ip.startswith("127.") or ip.startswith("10.") or ip.startswith("192.168."):
        return None
    try:
        import requests  # lazy: keeps unit tests independent of network

        r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=timeout)
        country = (r.json().get("country_code") or "").upper()
    except Exception:
        return None
    return _COUNTRY_TO_LANG.get(country)


def detect_ui_language(
    x_forwarded_for: str | None = None,
    accept_language: str | None = None,
) -> str:
    """Best-effort guess of UI language.

    Order: IP geo (via X-Forwarded-For) → browser Accept-Language → English.
    """
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
        hit = _from_ip(ip)
        if hit:
            return hit
    if accept_language:
        hit = _from_accept_language(accept_language)
        if hit:
            return hit
    return DEFAULT_UI_LANG


def t(key: str, lang: str = DEFAULT_UI_LANG, **fmt: object) -> str:
    """Lookup a UI string for a given language, with format kwargs.

    Falls back to English if the (lang, key) combo is missing.
    """
    table = _TRANSLATIONS.get(lang, _TRANSLATIONS[DEFAULT_UI_LANG])
    raw = table.get(key) or _TRANSLATIONS[DEFAULT_UI_LANG].get(key, key)
    if fmt:
        try:
            return raw.format(**fmt)
        except (KeyError, IndexError):
            return raw
    return raw
