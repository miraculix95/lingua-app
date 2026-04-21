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
    "Українська": "uk",
    "Polski": "pl",
    "עברית": "he",
}

UI_LANG_NAMES: dict[str, str] = {
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "uk": "Українська",
    "pl": "Polski",
    "he": "עברית",
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
    "dictation",
    "reading",
]


_TASK_NAMES: dict[str, list[str]] = {
    "en": [
        "",
        "Write a text and get feedback",
        "Fill in a cloze text",
        "Translate sentences",
        "Vocabulary quiz",
        "Build a sentence",
        "Find and fix errors",
        "Synonyms and antonyms",
        "Verb conjugation",
        "Dictation (audio)",
        "Reading comprehension",
    ],
    "de": [
        "",
        "Text schreiben und korrigieren",
        "Lückentext ausfüllen",
        "Sätze übersetzen",
        "Vokabel-Quiz",
        "Satz bauen",
        "Fehler finden und korrigieren",
        "Synonyme und Antonyme",
        "Verb konjugieren",
        "Diktat (Audio)",
        "Leseverstehen",
    ],
    "fr": [
        "",
        "Rédiger un texte et le faire corriger",
        "Remplir un texte à trous",
        "Traduire des phrases",
        "Quiz de vocabulaire",
        "Construire une phrase",
        "Trouver et corriger les erreurs",
        "Synonymes et antonymes",
        "Conjugaison des verbes",
        "Dictée (audio)",
        "Compréhension écrite",
    ],
    "es": [
        "",
        "Escribir un texto y recibir corrección",
        "Completar un texto con huecos",
        "Traducir frases",
        "Quiz de vocabulario",
        "Construir una frase",
        "Encontrar y corregir errores",
        "Sinónimos y antónimos",
        "Conjugación de verbos",
        "Dictado (audio)",
        "Comprensión lectora",
    ],
    "uk": [
        "",
        "Написати текст і отримати фідбек",
        "Заповнити пропуски в тексті",
        "Перекласти речення",
        "Тест зі словника",
        "Побудувати речення",
        "Знайти та виправити помилки",
        "Синоніми та антоніми",
        "Дієвідмінювання",
        "Диктант (аудіо)",
        "Читання з розумінням",
    ],
    "pl": [
        "",
        "Napisz tekst i uzyskaj korektę",
        "Wypełnij tekst z lukami",
        "Przetłumacz zdania",
        "Quiz ze słownictwa",
        "Zbuduj zdanie",
        "Znajdź i popraw błędy",
        "Synonimy i antonimy",
        "Koniugacja czasowników",
        "Dyktando (audio)",
        "Czytanie ze zrozumieniem",
    ],
    "he": [
        "",
        "כתיבת טקסט וקבלת תיקון",
        "השלמת טקסט פעור",
        "תרגום משפטים",
        "חידון אוצר מילים",
        "בניית משפט",
        "איתור ותיקון שגיאות",
        "מילים נרדפות ומנוגדות",
        "הטיית פעלים",
        "הכתבה (אודיו)",
        "הבנת הנקרא",
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
        "api_key_help": "🧪 Beta tester? Leave empty — the server key will be used. Otherwise: your key, stays in session, never stored. Get one at openrouter.ai/keys.",
        "model_tier": "Model tier",
        "key_source_byok": "✅ Your key (BYOK)",
        "key_source_or": "🔑 Server .env (OpenRouter)",
        "key_source_oa": "⚠️ Server .env (OpenAI fallback)",
        "key_source_none": "❌ No key found",
        "key_source_label": "Key source",
        "metric_tasks": "📚 Tasks",
        "metric_corrections": "✏️ Corrections",
        "metric_runs": "🔄 Session runs",
        "choose_exercise": "🎯 Choose exercise type",
        "practice_intro": "Pick an exercise type below. Each is a different way to practise with your vocabulary — focus on one or go through all of them.",
        "types_overview_title": "📖 What are the exercise types?",
        "desc_writing": "📝 **Free writing.** You get a theme and write a short text in the learning language. The coach corrects grammar, vocabulary and style — in the register you picked.",
        "desc_cloze": "📖 **Cloze text (fill in the blanks).** The LLM builds a short text with blanks. You type the missing words; the coach checks them.",
        "desc_translation": "🔁 **Translate sentences.** A handful of sentences to translate — either into or out of the learning language, your pick.",
        "desc_quiz": "🎲 **Vocabulary quiz.** Flashcard-style: you get the translation, you type the word. Fuzzy matching tolerates small typos.",
        "desc_sentence": "🧩 **Sentence building.** A few vocabs are given — you build a sentence that uses them naturally.",
        "desc_error": "🔍 **Error detection.** The LLM writes a few sentences that contain grammar or spelling mistakes. You find and fix them.",
        "desc_synonym": "🔤 **Synonyms & antonyms.** A word is given — you produce synonyms and antonyms in the learning language.",
        "desc_conjugation": "🔠 **Verb conjugation.** A verb + a person is given — you conjugate it across several tenses.",
        "desc_dictation": "🎙️ **Audio dictation.** The LLM writes a short text, ElevenLabs reads it, you transcribe. Playback-speed slider lets you slow the voice down.",
        "desc_reading": "📚 **Reading comprehension.** AI-generated text, a URL, pasted text, or an uploaded .txt — then multiple-choice + open-ended questions about it.",
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
        "cloze_freeform_hint": "💬 Type your answers in any format — one per line, comma-separated, or in running prose. The LLM will match them to the blanks.",
        "num_sentences": "Number of sentences",
        "error_no_key": "🔑 No API key. Enter your OpenRouter key in the sidebar.",
        "error_no_key_hint": "💡 Get one at https://openrouter.ai/keys — the key stays only in your session.",
        "quiz_new_btn": "🎲 New quiz",
        "quiz_evaluate_btn": "✅ Evaluate",
        "quiz_score": "🎯 Score",
        "quiz_prompt_format": "What is the {language} word for '{trans}'?",
        "side_questions": "**Side questions:**",
        "writing_task_prompt": "Write a text about the topic: {theme}",
        "cloze_vocab_heading": "Vocabulary (alphabetical):",
        "cloze_use_these": "Use these",
        "cloze_text_heading": "Cloze text:",
        "error_task_prompt": "Find and fix the errors in the following text:",
        "sentence_task_prompt": "Build a sentence using these words:",
        "synant_task_prompt": "Find synonyms and antonyms for:",
        "conjugation_task_prompt": "Conjugate the verb '{verb}' for the person '{person}' in the following tenses: present, past, future, perfect, present subjunctive, near future, present continuous.",
        "translation_direction": "Direction",
        "dir_to_learning": "→ into {learning} (produce)",
        "dir_to_native": "→ into {native} (understand)",
        "current_vocabs": "📖 Current vocabulary ({n})",
        "no_vocabs_yet": "_No vocabulary loaded yet._",
        "learning_language": "🎯 Learning language",
        "dict_speed": "🐢 ⇄ 🐇  Playback speed",
        "dict_reveal": "🔍 Reveal the original",
        "dict_your_transcript": "✏️ What did you hear?",
        "dict_original": "📜 Original text",
        "dict_no_key": "🎙️ Dictation needs an ElevenLabs API key. Add `ELEVENLABS_KEY` to your `.env`.",
        "dict_generate": "🎙️ Generate new dictation",
        "dict_status_text": "🧠 Writing text…",
        "dict_status_tts": "🎙️ Synthesizing voice…",
        "dict_status_ready": "✅ Dictation ready — listen and transcribe",
        "dict_tts_error": "❌ TTS failed: {err}",
        "elevenlabs_key": "🎙️ ElevenLabs API key (optional)",
        "elevenlabs_key_help": "For dictation TTS. Stays in session, never stored. Get one at elevenlabs.io.",
        "back_to_app": "Back to the app",
        "nav_about": "About",
        "about_title": "ℹ️ About lingua",
        "about_body": (
            "**lingua-app** is an AI-powered language tutor built for practising up to C1/C2 level, "
            "with register-aware corrections and mentor personas that change the voice of the feedback.\n\n"
            "### Highlights\n"
            "What sets lingua-app apart from mass-market language apps (Duolingo, Babbel, Busuu):\n\n"
            "- **Seven language registers**, not just 'formal vs. casual' — the LLM matches corrections "
            "to the register you're writing in (criminal slang · vulgar · colloquial · standard · "
            "formal · literary · technical).\n"
            "- **Ten mentor personas** — from Kind Teacher to Machiavelli. The stylistic contrast "
            "makes errors memorable.\n"
            "- **Ten exercise types** — writing, cloze, translation (both directions), sentence building, "
            "error detection, synonyms/antonyms, verb conjugation, vocabulary quiz, audio dictation "
            "(ElevenLabs, with playback-speed slider), and reading comprehension "
            "(AI-generated / URL / paste / TXT → MC + open-ended questions).\n"
            "- **BYOK (Bring Your Own Key)** — your OpenRouter and ElevenLabs keys stay in your "
            "browser session. Never stored, never logged. Beta testers can leave the field empty — "
            "the server key is used instead.\n"
            "- **Seven learning languages** — French, English, Spanish, Ukrainian, German, Polish, Hebrew.\n"
            "- **Seven UI languages** — English, German, French, Spanish, Ukrainian, Polish, Hebrew, "
            "with IP-based auto-detection on first visit.\n\n"
            "### Author\n"
            "Built by **Bastian Brand** ([Website](https://www.bastian-brand.com/) · "
            "[GitHub](https://github.com/miraculix95) · [LinkedIn](https://www.linkedin.com/in/dr-bastian-brand/)) — "
            "Munich-based independent consultant in data analytics, finance and AI automation, McKinsey alumnus, "
            "working with private-equity, travel, insurance and automotive clients across Europe. "
            "lingua-app was originally written in early 2025 as a personal tool for French C1 practice; "
            "refactored in 2026 into this modular, tested, multilingual release.\n\n"
            "### Source code\n"
            "[lingua-app on GitHub](https://github.com/miraculix95/lingua-app) — open source under MIT. Issues, PRs, and feedback welcome."
        ),
        "setup_guide_title": "🚀 First time here? Setup in 2 min",
        "setup_guide_body": (
            "> 🧪 **Beta tester? No key required.** Skip step 1 — the app uses a shared server key. Jump to step 4.\n\n"
            "**1. Get an OpenRouter API key** (only for non-beta users)\n\n"
            "- Go to [openrouter.ai/keys](https://openrouter.ai/keys) and sign in (Google, GitHub, or email)\n"
            "- Click **Create Key**, copy it (starts with `sk-or-...`)\n"
            "- Add $5 credit under **Settings → Credits** — lasts for hundreds of exercises\n"
            "- Paste the key below in **🤖 Model & API**\n\n"
            "**2. (Optional) ElevenLabs key** — only if you want the Dictation exercise\n\n"
            "- Go to [elevenlabs.io](https://elevenlabs.io) → sign up (free tier includes ~10 min TTS/month)\n"
            "- **Profile → API Keys → Create Key**, copy it (starts with `xi-...`)\n"
            "- Paste it below in **🤖 Model & API**\n\n"
            "**3. Keys stay in your browser session only** — never stored server-side, never logged.\n\n"
            "**4. Pick a learning language, level, and an exercise type.** Vocabulary auto-generates if you don't load your own."
        ),
        "el_source_byok": "🎙️ Voice: your ElevenLabs key (BYOK)",
        "el_source_env": "🎙️ Voice: server .env ElevenLabs",
        "sidebar_heading": "⚙️ Configuration",
        "main_heading": "🎯 Practice area",
        "home_btn": "🔄 Reset",
        "help_home": "Clear the current task and return to the exercise picker. Your language, level, register, vocabulary and keys stay.",
        "how_it_works": "👈 **Step 1 — Sidebar:** set your coach, level, register, vocabulary source and API key. **Step 2 — here:** pick an exercise below and click **New task**.",
        "help_ui_language": "Language of buttons, labels and feedback.",
        "help_learning_language": "The language you want to practise. Switch any time — vocabulary resets on change.",
        "help_coach": "The persona writing your correction. Style only — grammar rules stay the same.",
        "help_level": "Your CEFR level (A1 beginner → C2 near-native). Texts and questions scale to it.",
        "help_register": "Which social register the LLM should use and correct against, from street slang to technical prose.",
        "help_num_vocab": "How many vocab items to extract / generate from the source.",
        "help_url": "Paste a news/article URL — the app extracts vocabulary from it.",
        "help_ready_vocab": "Upload a plain-text file with one vocabulary item per line.",
        "help_model_tier": "Budget is the cheapest; Best is most accurate. Non-English languages auto-use a stronger default.",
        "help_choose_exercise": "Pick what kind of practice you want next. Each option is a different way to work with your vocabulary — fill-in-the-blanks, translate sentences, listen to a dictation, read a text and answer questions, and more. Switch any time.",
        "help_new_task": "Re-roll a fresh task with the current settings.",
        "help_correct": "Send your answer to the coach for correction.",
        "help_num_blanks": "How many cloze blanks to produce.",
        "help_num_sentences": "How many translation sentences to produce.",
        "help_dict_generate": "The LLM writes a short text, ElevenLabs speaks it. You transcribe, the app diffs.",
        "help_dict_speed": "Slow down or speed up the voice without changing pitch.",
        "help_read_source": "Where the passage comes from: AI-generated, a webpage, pasted text, or an uploaded .txt.",
        "help_read_length": "Rough word count for the AI-generated passage.",
        "help_read_theme": "Optional topic seed — e.g. 'climate', 'urbanism', 'childhood'.",
        "help_read_generate": "Pulls the text and drafts multiple-choice + open questions.",
        "help_read_submit": "Evaluate: MC is scored locally, open answers are graded by the LLM against a reference.",
        "read_source": "📖 Text source",
        "read_source_ai": "Generate with AI",
        "read_source_url": "Fetch from URL",
        "read_source_paste": "Paste text",
        "read_source_file": "Upload .txt",
        "read_length": "📏 Length",
        "read_length_short": "Short (~150 words)",
        "read_length_medium": "Medium (~350 words)",
        "read_length_long": "Long (~600 words)",
        "read_theme": "🎯 Theme",
        "read_url_placeholder": "https://…",
        "read_paste_placeholder": "Paste the text to read here…",
        "read_generate": "📖 Get passage & questions",
        "read_status_text": "🧠 Writing the passage…",
        "read_status_fetch": "🌐 Fetching the page…",
        "read_status_questions": "🧠 Drafting questions…",
        "read_status_ready": "✅ Passage and questions ready",
        "read_passage_heading": "Passage",
        "read_mc_heading": "Multiple choice",
        "read_open_heading": "Open-ended",
        "read_submit": "✅ Evaluate",
        "read_score": "🎯 MC score",
        "read_open_feedback": "Open answers",
        "read_need_passage": "No passage yet. Generate or load one first.",
        "read_url_failed": "❌ Could not fetch that URL: {err}",
        "read_verdict_CORRECT": "✅ Correct",
        "read_verdict_PARTIAL": "🟡 Partially correct",
        "read_verdict_INCORRECT": "❌ Incorrect",
        "read_verdict_ERROR": "⚠️ Could not grade",
        "read_reveal_answers": "🔍 Show correct MC answers",
        "read_reference_answer": "Reference answer",
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
        "api_key_help": "🧪 Beta-Tester? Leer lassen — der Server-Key wird genutzt. Sonst: dein Key, bleibt in Session, wird nie gespeichert. Hol einen auf openrouter.ai/keys.",
        "model_tier": "Modell-Tier",
        "key_source_byok": "✅ Dein Key (BYOK)",
        "key_source_or": "🔑 Server .env (OpenRouter)",
        "key_source_oa": "⚠️ Server .env (OpenAI-Fallback)",
        "key_source_none": "❌ Kein Key gefunden",
        "key_source_label": "Key-Quelle",
        "metric_tasks": "📚 Aufgaben",
        "metric_corrections": "✏️ Korrekturen",
        "metric_runs": "🔄 Session-Runs",
        "choose_exercise": "🎯 Übungstyp wählen",
        "practice_intro": "Wähle unten einen Übungstyp. Jeder Typ ist eine andere Art, mit deinen Vokabeln zu üben — konzentrier dich auf einen oder arbeite sie der Reihe nach durch.",
        "types_overview_title": "📖 Was sind die Übungstypen?",
        "desc_writing": "📝 **Freies Schreiben.** Du bekommst ein Thema und schreibst einen kurzen Text in der Lernsprache. Der Coach korrigiert Grammatik, Wortschatz und Stil — im gewählten Register.",
        "desc_cloze": "📖 **Lückentext.** Das LLM baut einen kurzen Text mit Lücken. Du tippst die fehlenden Wörter; der Coach prüft sie.",
        "desc_translation": "🔁 **Sätze übersetzen.** Ein paar Sätze zum Übersetzen — wahlweise in oder aus der Lernsprache.",
        "desc_quiz": "🎲 **Vokabel-Quiz.** Flashcard-Stil: du siehst die Übersetzung, tippst das Wort. Tippfehler-tolerant.",
        "desc_sentence": "🧩 **Satz bauen.** Ein paar Vokabeln sind vorgegeben — du baust einen Satz, der sie natürlich benutzt.",
        "desc_error": "🔍 **Fehler finden.** Das LLM schreibt ein paar Sätze mit Grammatik- oder Rechtschreibfehlern. Du findest und korrigierst sie.",
        "desc_synonym": "🔤 **Synonyme & Antonyme.** Ein Wort ist vorgegeben — du nennst Synonyme und Antonyme in der Lernsprache.",
        "desc_conjugation": "🔠 **Verbkonjugation.** Ein Verb + eine Person sind vorgegeben — du konjugierst es in mehreren Zeiten.",
        "desc_dictation": "🎙️ **Audio-Diktat.** Das LLM schreibt einen kurzen Text, ElevenLabs liest ihn vor, du schreibst mit. Geschwindigkeits-Slider zum Verlangsamen.",
        "desc_reading": "📚 **Leseverstehen.** KI-generierter Text, URL, eingefügter Text oder hochgeladene .txt — danach Multiple-Choice- und offene Fragen dazu.",
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
        "cloze_freeform_hint": "💬 Antworten können im Freiformat eingegeben werden — pro Zeile, kommagetrennt oder im Fließtext. Das LLM ordnet sie den Lücken zu.",
        "num_sentences": "Anzahl Sätze",
        "error_no_key": "🔑 Kein API-Key. Gib deinen OpenRouter-Key in der Sidebar ein.",
        "error_no_key_hint": "💡 Hol einen auf https://openrouter.ai/keys — der Key bleibt nur in deiner Session.",
        "quiz_new_btn": "🎲 Neues Quiz",
        "quiz_evaluate_btn": "✅ Auswerten",
        "quiz_score": "🎯 Score",
        "quiz_prompt_format": "Was ist das {language}e Wort für '{trans}'?",
        "side_questions": "**Nebenfragen:**",
        "writing_task_prompt": "Schreibe einen Text zum Thema: {theme}",
        "cloze_vocab_heading": "Vokabeln (alphabetisch):",
        "cloze_use_these": "Zu benutzen",
        "cloze_text_heading": "Lückentext:",
        "error_task_prompt": "Finde und korrigiere die Fehler im folgenden Text:",
        "sentence_task_prompt": "Baue einen Satz mit diesen Wörtern:",
        "synant_task_prompt": "Finde Synonyme und Antonyme zu:",
        "conjugation_task_prompt": "Konjugiere das Verb '{verb}' für die Person '{person}' in den folgenden Zeiten: Präsens, Imparfait, Futur, Perfekt, Subjonctif présent, Futur proche und Présent continu.",
        "translation_direction": "Richtung",
        "dir_to_learning": "→ ins {learning} (produzieren)",
        "dir_to_native": "→ ins {native} (verstehen)",
        "current_vocabs": "📖 Aktuelle Vokabeln ({n})",
        "no_vocabs_yet": "_Noch keine Vokabeln geladen._",
        "learning_language": "🎯 Lernsprache",
        "dict_speed": "🐢 ⇄ 🐇  Wiedergabegeschwindigkeit",
        "dict_reveal": "🔍 Original anzeigen",
        "dict_your_transcript": "✏️ Was hast du gehört?",
        "dict_original": "📜 Original-Text",
        "dict_no_key": "🎙️ Diktat braucht einen ElevenLabs-API-Key. Setze `ELEVENLABS_KEY` in `.env`.",
        "dict_generate": "🎙️ Neues Diktat generieren",
        "dict_status_text": "🧠 Text wird geschrieben…",
        "dict_status_tts": "🎙️ Stimme wird synthetisiert…",
        "dict_status_ready": "✅ Diktat bereit — anhören und mitschreiben",
        "dict_tts_error": "❌ TTS-Fehler: {err}",
        "elevenlabs_key": "🎙️ ElevenLabs API-Key (optional)",
        "elevenlabs_key_help": "Für Diktat-TTS. Bleibt in Session, wird nie gespeichert. Hol einen auf elevenlabs.io.",
        "back_to_app": "Zurück zur App",
        "nav_about": "Über",
        "about_title": "ℹ️ Über lingua",
        "about_body": (
            "**lingua-app** ist ein KI-Sprachtutor für Praxis bis C1/C2-Niveau, mit registerbewusster "
            "Korrektur und Mentor-Personas, die die Stimme des Feedbacks ändern.\n\n"
            "### Besonderheiten\n"
            "Was lingua-app von Massenmarkt-Sprach­apps (Duolingo, Babbel, Busuu) unterscheidet:\n\n"
            "- **Sieben Sprachregister**, nicht nur 'formell vs. locker' — das LLM passt die Korrektur "
            "dem Register an, in dem du schreibst (Gossensprache · vulgär · umgangssprachlich · "
            "Standard · formell · literarisch · technisch).\n"
            "- **Zehn Mentor-Personas** — von Netter Lehrer bis Machiavelli. Der Stilkontrast "
            "macht Fehler unvergesslich.\n"
            "- **Zehn Übungstypen** — Schreiben, Lückentext, Übersetzung (beide Richtungen), "
            "Satzbau, Fehlersuche, Synonyme/Antonyme, Verbkonjugation, Vokabel-Quiz, Audio-Diktat "
            "(ElevenLabs, mit Geschwindigkeits-Slider) und Leseverstehen "
            "(KI-generiert / URL / einfügen / TXT → Multiple-Choice + offene Fragen).\n"
            "- **BYOK (Bring Your Own Key)** — OpenRouter- und ElevenLabs-Keys bleiben in deiner "
            "Browser-Session. Nichts wird gespeichert oder geloggt. Beta-Tester können das Feld leer "
            "lassen — dann wird der Server-Key genutzt.\n"
            "- **Sieben Lernsprachen** — Französisch, Englisch, Spanisch, Ukrainisch, Deutsch, Polnisch, Hebräisch.\n"
            "- **Sieben UI-Sprachen** — Englisch, Deutsch, Französisch, Spanisch, Ukrainisch, Polnisch, "
            "Hebräisch, mit IP-basierter Auto-Erkennung beim ersten Besuch.\n\n"
            "### Autor\n"
            "Gebaut von **Bastian Brand** ([Website](https://www.bastian-brand.com/) · "
            "[GitHub](https://github.com/miraculix95) · [LinkedIn](https://www.linkedin.com/in/dr-bastian-brand/)) — "
            "freiberuflicher Consultant aus München für Datenanalyse, Finanzen und KI-Automatisierung, McKinsey-Alumnus, "
            "mit Kunden aus Private Equity, Reise, Versicherung und Automobilindustrie in ganz Europa. "
            "lingua-app entstand Anfang 2025 als persönliches Tool für Französisch-C1-Praxis; 2026 als modulares, "
            "getestetes, mehrsprachiges Release refactored.\n\n"
            "### Quellcode\n"
            "[lingua-app auf GitHub](https://github.com/miraculix95/lingua-app) — Open Source unter MIT-Lizenz. Issues, PRs und Feedback willkommen."
        ),
        "setup_guide_title": "🚀 Zum ersten Mal hier? Setup in 2 Minuten",
        "setup_guide_body": (
            "> 🧪 **Beta-Tester? Kein Key nötig.** Schritt 1 überspringen — die App nutzt einen gemeinsamen Server-Key. Direkt zu Schritt 4.\n\n"
            "**1. OpenRouter-API-Key holen** (nur für Nicht-Beta-User)\n\n"
            "- Auf [openrouter.ai/keys](https://openrouter.ai/keys) gehen und einloggen (Google, GitHub oder Email)\n"
            "- **Create Key** klicken, Key kopieren (beginnt mit `sk-or-...`)\n"
            "- Unter **Settings → Credits** $5 Guthaben einzahlen — reicht für hunderte Aufgaben\n"
            "- Key unten in **🤖 Modell & API** einfügen\n\n"
            "**2. (Optional) ElevenLabs-Key** — nur für die Diktat-Aufgabe\n\n"
            "- Auf [elevenlabs.io](https://elevenlabs.io) registrieren (Free-Tier hat ~10 Min TTS/Monat)\n"
            "- **Profile → API Keys → Create Key**, kopieren (beginnt mit `xi-...`)\n"
            "- Unten in **🤖 Modell & API** einfügen\n\n"
            "**3. Keys bleiben nur in deiner Browser-Session** — nichts wird serverseitig gespeichert oder geloggt.\n\n"
            "**4. Lernsprache, Niveau und Übungstyp wählen.** Vokabeln werden automatisch generiert, wenn du keine eigenen lädst."
        ),
        "el_source_byok": "🎙️ Stimme: dein ElevenLabs-Key (BYOK)",
        "el_source_env": "🎙️ Stimme: Server .env ElevenLabs",
        "sidebar_heading": "⚙️ Konfiguration",
        "main_heading": "🎯 Übungsbereich",
        "home_btn": "🔄 Zurücksetzen",
        "help_home": "Aktuelle Aufgabe verwerfen und zurück zur Übungsauswahl. Sprache, Niveau, Register, Vokabeln und Keys bleiben.",
        "how_it_works": "👈 **Schritt 1 — Sidebar:** Coach, Niveau, Register, Vokabelquelle und API-Key einstellen. **Schritt 2 — hier:** Übung auswählen und **Neue Aufgabe** klicken.",
        "help_ui_language": "Sprache der Buttons, Labels und Korrekturen.",
        "help_learning_language": "Die Sprache, die du üben willst. Jederzeit umschaltbar — Vokabeln werden beim Wechsel geleert.",
        "help_coach": "Die Persona, die deine Korrektur schreibt. Reiner Stil — die Grammatikregeln bleiben.",
        "help_level": "Dein CEFR-Niveau (A1 Anfänger → C2 nahe Muttersprache). Texte und Fragen skalieren damit.",
        "help_register": "Welches Sprachregister das LLM nutzt und gegen das es korrigiert — von Gossensprache bis Fachsprache.",
        "help_num_vocab": "Wie viele Vokabeln aus der Quelle extrahiert/generiert werden.",
        "help_url": "Füge eine Artikel-URL ein — die App extrahiert daraus Vokabeln.",
        "help_ready_vocab": "Textdatei mit einer Vokabel pro Zeile hochladen.",
        "help_model_tier": "Budget ist am günstigsten, Best am genauesten. Für nicht-englische Sprachen ist der Default stärker voreingestellt.",
        "help_choose_exercise": "Wähle, welche Art von Übung du als Nächstes machen willst. Jede Option ist eine andere Art, mit deinen Vokabeln zu arbeiten — Lücken füllen, Sätze übersetzen, Diktat anhören, einen Text lesen und Fragen beantworten, usw. Jederzeit wechselbar.",
        "help_new_task": "Eine neue Aufgabe mit den aktuellen Einstellungen würfeln.",
        "help_correct": "Antwort an den Coach zur Korrektur schicken.",
        "help_num_blanks": "Wie viele Lücken der Text haben soll.",
        "help_num_sentences": "Wie viele Sätze zum Übersetzen erzeugt werden.",
        "help_dict_generate": "Das LLM schreibt einen kurzen Text, ElevenLabs spricht ihn. Du schreibst mit, die App vergleicht.",
        "help_dict_speed": "Stimme verlangsamen oder beschleunigen, ohne die Tonhöhe zu ändern.",
        "help_read_source": "Woher der Text kommt: KI-generiert, Webseite, eingefügter Text oder hochgeladene .txt.",
        "help_read_length": "Ungefähre Wortzahl für den KI-generierten Text.",
        "help_read_theme": "Optionales Thema — z.B. 'Klima', 'Städtebau', 'Kindheit'.",
        "help_read_generate": "Holt den Text und erzeugt Multiple-Choice- und offene Fragen.",
        "help_read_submit": "Auswerten: MC wird lokal gezählt, offene Antworten bewertet das LLM gegen eine Referenz.",
        "read_source": "📖 Textquelle",
        "read_source_ai": "KI generieren lassen",
        "read_source_url": "Von URL laden",
        "read_source_paste": "Text einfügen",
        "read_source_file": ".txt hochladen",
        "read_length": "📏 Länge",
        "read_length_short": "Kurz (~150 Wörter)",
        "read_length_medium": "Mittel (~350 Wörter)",
        "read_length_long": "Lang (~600 Wörter)",
        "read_theme": "🎯 Thema",
        "read_url_placeholder": "https://…",
        "read_paste_placeholder": "Text zum Lesen hier einfügen…",
        "read_generate": "📖 Text & Fragen erzeugen",
        "read_status_text": "🧠 Text wird geschrieben…",
        "read_status_fetch": "🌐 Seite wird geladen…",
        "read_status_questions": "🧠 Fragen werden erstellt…",
        "read_status_ready": "✅ Text und Fragen bereit",
        "read_passage_heading": "Text",
        "read_mc_heading": "Multiple Choice",
        "read_open_heading": "Offene Fragen",
        "read_submit": "✅ Auswerten",
        "read_score": "🎯 MC-Ergebnis",
        "read_open_feedback": "Offene Antworten",
        "read_need_passage": "Noch kein Text. Erst generieren oder laden.",
        "read_url_failed": "❌ URL konnte nicht geladen werden: {err}",
        "read_verdict_CORRECT": "✅ Richtig",
        "read_verdict_PARTIAL": "🟡 Teilweise richtig",
        "read_verdict_INCORRECT": "❌ Falsch",
        "read_verdict_ERROR": "⚠️ Konnte nicht bewertet werden",
        "read_reveal_answers": "🔍 Richtige MC-Antworten zeigen",
        "read_reference_answer": "Musterantwort",
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
        "api_key_help": "🧪 Beta-testeur ? Laisse vide — la clé du serveur sera utilisée. Sinon : ta clé, reste en session, jamais stockée. Obtiens-en une sur openrouter.ai/keys.",
        "model_tier": "Palier du modèle",
        "key_source_byok": "✅ Ta clé (BYOK)",
        "key_source_or": "🔑 Serveur .env (OpenRouter)",
        "key_source_oa": "⚠️ Serveur .env (OpenAI)",
        "key_source_none": "❌ Pas de clé trouvée",
        "key_source_label": "Source de la clé",
        "metric_tasks": "📚 Exercices",
        "metric_corrections": "✏️ Corrections",
        "metric_runs": "🔄 Sessions",
        "choose_exercise": "🎯 Choisir un type d'exercice",
        "practice_intro": "Choisis un type d'exercice ci-dessous. Chaque type est une manière différente de pratiquer ton vocabulaire — concentre-toi sur un ou fais-les tous.",
        "types_overview_title": "📖 Quels sont les types d'exercices ?",
        "desc_writing": "📝 **Rédaction libre.** Tu reçois un thème et écris un court texte dans la langue cible. Le coach corrige la grammaire, le vocabulaire et le style — dans le registre choisi.",
        "desc_cloze": "📖 **Texte à trous.** Le LLM construit un court texte avec des trous. Tu tapes les mots manquants ; le coach vérifie.",
        "desc_translation": "🔁 **Traduire des phrases.** Quelques phrases à traduire — au choix vers ou depuis la langue cible.",
        "desc_quiz": "🎲 **Quiz de vocabulaire.** Style flashcards : tu vois la traduction, tu tapes le mot. Tolère les petites fautes de frappe.",
        "desc_sentence": "🧩 **Construction de phrase.** Quelques mots te sont donnés — tu construis une phrase qui les utilise naturellement.",
        "desc_error": "🔍 **Détection d'erreurs.** Le LLM écrit quelques phrases contenant des fautes de grammaire ou d'orthographe. Tu les trouves et tu les corriges.",
        "desc_synonym": "🔤 **Synonymes et antonymes.** Un mot est donné — tu produis synonymes et antonymes dans la langue cible.",
        "desc_conjugation": "🔠 **Conjugaison.** Un verbe + une personne sont donnés — tu le conjugues sur plusieurs temps.",
        "desc_dictation": "🎙️ **Dictée audio.** Le LLM écrit un court texte, ElevenLabs le lit, tu transcris. Curseur de vitesse pour ralentir la voix.",
        "desc_reading": "📚 **Compréhension écrite.** Texte généré par IA, URL, texte collé ou .txt importé — puis QCM + questions ouvertes.",
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
        "cloze_freeform_hint": "💬 Saisis tes réponses librement — une par ligne, séparées par des virgules ou en texte continu. Le LLM les associera aux trous.",
        "num_sentences": "Nombre de phrases",
        "error_no_key": "🔑 Pas de clé API. Saisis ta clé OpenRouter dans la barre latérale.",
        "error_no_key_hint": "💡 Obtiens-en une sur https://openrouter.ai/keys — la clé reste dans ta session.",
        "quiz_new_btn": "🎲 Nouveau quiz",
        "quiz_evaluate_btn": "✅ Évaluer",
        "quiz_score": "🎯 Score",
        "quiz_prompt_format": "Quel est le mot en {language} pour « {trans} » ?",
        "side_questions": "**Questions méta :**",
        "writing_task_prompt": "Rédige un texte sur le thème : {theme}",
        "cloze_vocab_heading": "Vocabulaire (alphabétique) :",
        "cloze_use_these": "À utiliser",
        "cloze_text_heading": "Texte à trous :",
        "error_task_prompt": "Trouve et corrige les erreurs dans le texte suivant :",
        "sentence_task_prompt": "Construis une phrase avec ces mots :",
        "synant_task_prompt": "Trouve les synonymes et antonymes de :",
        "conjugation_task_prompt": "Conjugue le verbe « {verb} » à la personne « {person} » aux temps suivants : présent, imparfait, futur, passé composé, subjonctif présent, futur proche, présent continu.",
        "translation_direction": "Direction",
        "dir_to_learning": "→ vers {learning} (produire)",
        "dir_to_native": "→ vers {native} (comprendre)",
        "current_vocabs": "📖 Vocabulaire actuel ({n})",
        "no_vocabs_yet": "_Aucun vocabulaire chargé._",
        "learning_language": "🎯 Langue à apprendre",
        "dict_speed": "🐢 ⇄ 🐇  Vitesse de lecture",
        "dict_reveal": "🔍 Révéler l'original",
        "dict_your_transcript": "✏️ Qu'as-tu entendu ?",
        "dict_original": "📜 Texte original",
        "dict_no_key": "🎙️ La dictée nécessite une clé API ElevenLabs. Ajoute `ELEVENLABS_KEY` à ton `.env`.",
        "dict_generate": "🎙️ Générer une nouvelle dictée",
        "dict_status_text": "🧠 Rédaction du texte…",
        "dict_status_tts": "🎙️ Synthèse vocale…",
        "dict_status_ready": "✅ Dictée prête — écoute et transcris",
        "dict_tts_error": "❌ Erreur TTS : {err}",
        "elevenlabs_key": "🎙️ Clé API ElevenLabs (facultatif)",
        "elevenlabs_key_help": "Pour la TTS de la dictée. Reste en session, jamais stockée. Obtiens-en une sur elevenlabs.io.",
        "back_to_app": "Retour à l'application",
        "nav_about": "À propos",
        "about_title": "ℹ️ À propos de lingua",
        "about_body": (
            "**lingua-app** est un tuteur de langue basé sur l'IA, pensé pour s'entraîner jusqu'au "
            "niveau C1/C2, avec des corrections sensibles au registre de langue et des personas de "
            "mentor qui changent la voix du feedback.\n\n"
            "### Points forts\n"
            "Ce qui distingue lingua-app des applis grand public (Duolingo, Babbel, Busuu) :\n\n"
            "- **Sept registres de langue**, pas seulement 'soutenu vs. familier' — le LLM adapte "
            "la correction au registre dans lequel tu écris (argot · vulgaire · familier · courant · "
            "soutenu · littéraire · technique).\n"
            "- **Dix personas de mentor** — du Professeur sympathique à Machiavel. Le contraste "
            "stylistique rend les erreurs mémorables.\n"
            "- **Dix types d'exercices** — rédaction, texte à trous, traduction (dans les deux sens), "
            "construction de phrase, détection d'erreurs, synonymes/antonymes, conjugaison des verbes, "
            "quiz de vocabulaire, dictée audio (ElevenLabs, avec curseur de vitesse), et compréhension "
            "écrite (généré par IA / URL / texte collé / TXT → QCM + questions ouvertes).\n"
            "- **BYOK (Bring Your Own Key)** — tes clés OpenRouter et ElevenLabs restent dans ta "
            "session navigateur. Jamais stockées, jamais journalisées. Les beta-testeurs peuvent "
            "laisser vide — la clé du serveur sera utilisée.\n"
            "- **Sept langues à apprendre** — français, anglais, espagnol, ukrainien, allemand, polonais, hébreu.\n"
            "- **Sept langues d'interface** — anglais, allemand, français, espagnol, ukrainien, "
            "polonais, hébreu, avec détection automatique par IP à la première visite.\n\n"
            "### Auteur\n"
            "Créé par **Bastian Brand** ([Site](https://www.bastian-brand.com/) · "
            "[GitHub](https://github.com/miraculix95) · [LinkedIn](https://www.linkedin.com/in/dr-bastian-brand/)) — "
            "consultant freelance basé à Munich en analyse de données, finance et automatisation IA, ancien de McKinsey, "
            "intervenant pour des clients du private equity, du tourisme, de l'assurance et de l'automobile dans toute l'Europe. "
            "lingua-app a été écrit initialement début 2025 comme outil personnel pour s'entraîner en français C1 ; "
            "refactoré en 2026 en une version modulaire, testée et multilingue.\n\n"
            "### Code source\n"
            "[lingua-app sur GitHub](https://github.com/miraculix95/lingua-app) — open source sous licence MIT. Issues, PRs et retours bienvenus."
        ),
        "setup_guide_title": "🚀 Première visite ? Configuration en 2 min",
        "setup_guide_body": (
            "> 🧪 **Beta-testeur ? Pas besoin de clé.** Saute l'étape 1 — l'app utilise une clé serveur partagée. Va directement à l'étape 4.\n\n"
            "**1. Obtiens une clé API OpenRouter** (uniquement pour non-beta)\n\n"
            "- Va sur [openrouter.ai/keys](https://openrouter.ai/keys) et connecte-toi (Google, GitHub ou email)\n"
            "- Clique **Create Key**, copie la clé (commence par `sk-or-...`)\n"
            "- Ajoute 5 $ de crédit sous **Settings → Credits** — suffit pour des centaines d'exercices\n"
            "- Colle la clé plus bas dans **🤖 Modèle & API**\n\n"
            "**2. (Optionnel) Clé ElevenLabs** — uniquement pour la dictée\n\n"
            "- Va sur [elevenlabs.io](https://elevenlabs.io) → inscris-toi (le tier gratuit inclut ~10 min de TTS/mois)\n"
            "- **Profile → API Keys → Create Key**, copie-la (commence par `xi-...`)\n"
            "- Colle-la plus bas dans **🤖 Modèle & API**\n\n"
            "**3. Tes clés restent dans ta session de navigateur** — rien n'est stocké ni journalisé côté serveur.\n\n"
            "**4. Choisis une langue, un niveau et un type d'exercice.** Le vocabulaire est généré automatiquement si tu n'en charges pas."
        ),
        "el_source_byok": "🎙️ Voix : ta clé ElevenLabs (BYOK)",
        "el_source_env": "🎙️ Voix : .env serveur ElevenLabs",
        "sidebar_heading": "⚙️ Configuration",
        "main_heading": "🎯 Espace d'exercices",
        "home_btn": "🔄 Réinitialiser",
        "help_home": "Efface la tâche en cours et retourne au choix d'exercice. Langue, niveau, registre, vocabulaire et clés sont conservés.",
        "how_it_works": "👈 **Étape 1 — barre latérale :** choisis coach, niveau, registre, source de vocabulaire et clé API. **Étape 2 — ici :** choisis un exercice ci-dessous et clique sur **Nouvelle tâche**.",
        "help_ui_language": "Langue des boutons, libellés et corrections.",
        "help_learning_language": "La langue que tu veux pratiquer. Modifiable à tout moment — le vocabulaire est réinitialisé.",
        "help_coach": "La persona qui écrit ta correction. Style uniquement — les règles de grammaire ne changent pas.",
        "help_level": "Ton niveau CECR (A1 débutant → C2 quasi-natif). Textes et questions s'adaptent.",
        "help_register": "Le registre visé par le modèle — de l'argot à la prose technique.",
        "help_num_vocab": "Combien de mots extraire/générer depuis la source.",
        "help_url": "Colle une URL d'article — l'app en extrait le vocabulaire.",
        "help_ready_vocab": "Un fichier texte, un mot par ligne.",
        "help_model_tier": "Budget = le moins cher ; Best = le plus précis. Pour les langues non-anglaises, un modèle plus fort est sélectionné par défaut.",
        "help_choose_exercise": "Choisis le type d'exercice à faire maintenant. Chaque option est une manière différente de travailler ton vocabulaire — texte à trous, traduire des phrases, écouter une dictée, lire un texte et répondre aux questions, etc. Changeable à tout moment.",
        "help_new_task": "Regénérer une tâche avec les réglages actuels.",
        "help_correct": "Envoyer ta réponse au coach pour correction.",
        "help_num_blanks": "Combien de trous dans le texte.",
        "help_num_sentences": "Combien de phrases à traduire.",
        "help_dict_generate": "Le LLM écrit un court texte, ElevenLabs le prononce. Tu transcris, l'app compare.",
        "help_dict_speed": "Ralentir ou accélérer la voix sans changer le ton.",
        "help_read_source": "D'où vient le texte : généré par IA, page web, texte collé, ou .txt importé.",
        "help_read_length": "Nombre approximatif de mots pour le texte généré par IA.",
        "help_read_theme": "Thème optionnel — ex. « climat », « urbanisme », « enfance ».",
        "help_read_generate": "Récupère le texte et rédige les questions (QCM + ouvertes).",
        "help_read_submit": "Évaluer : QCM compté localement, réponses ouvertes notées par le LLM contre une référence.",
        "read_source": "📖 Source du texte",
        "read_source_ai": "Générer avec l'IA",
        "read_source_url": "Charger depuis une URL",
        "read_source_paste": "Coller un texte",
        "read_source_file": "Importer un .txt",
        "read_length": "📏 Longueur",
        "read_length_short": "Court (~150 mots)",
        "read_length_medium": "Moyen (~350 mots)",
        "read_length_long": "Long (~600 mots)",
        "read_theme": "🎯 Thème",
        "read_url_placeholder": "https://…",
        "read_paste_placeholder": "Colle ici le texte à lire…",
        "read_generate": "📖 Générer texte & questions",
        "read_status_text": "🧠 Rédaction du texte…",
        "read_status_fetch": "🌐 Chargement de la page…",
        "read_status_questions": "🧠 Rédaction des questions…",
        "read_status_ready": "✅ Texte et questions prêts",
        "read_passage_heading": "Texte",
        "read_mc_heading": "QCM",
        "read_open_heading": "Questions ouvertes",
        "read_submit": "✅ Évaluer",
        "read_score": "🎯 Score QCM",
        "read_open_feedback": "Réponses ouvertes",
        "read_need_passage": "Pas encore de texte. Génère-en un ou charges-en un d'abord.",
        "read_url_failed": "❌ URL impossible à charger : {err}",
        "read_verdict_CORRECT": "✅ Correct",
        "read_verdict_PARTIAL": "🟡 Partiellement correct",
        "read_verdict_INCORRECT": "❌ Incorrect",
        "read_verdict_ERROR": "⚠️ Impossible à noter",
        "read_reveal_answers": "🔍 Afficher les bonnes réponses QCM",
        "read_reference_answer": "Réponse de référence",
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
        "api_key_help": "🧪 ¿Beta-tester? Déjalo vacío — se usa la clave del servidor. Si no: tu clave, solo en la sesión, nunca se guarda. Consigue una en openrouter.ai/keys.",
        "model_tier": "Nivel del modelo",
        "key_source_byok": "✅ Tu clave (BYOK)",
        "key_source_or": "🔑 Servidor .env (OpenRouter)",
        "key_source_oa": "⚠️ Servidor .env (OpenAI)",
        "key_source_none": "❌ No se encontró clave",
        "key_source_label": "Fuente de la clave",
        "metric_tasks": "📚 Ejercicios",
        "metric_corrections": "✏️ Correcciones",
        "metric_runs": "🔄 Sesiones",
        "choose_exercise": "🎯 Elegir tipo de ejercicio",
        "practice_intro": "Elige un tipo de ejercicio abajo. Cada tipo es una forma distinta de practicar tu vocabulario — concéntrate en uno o hazlos todos.",
        "types_overview_title": "📖 ¿Qué tipos de ejercicio hay?",
        "desc_writing": "📝 **Redacción libre.** Recibes un tema y escribes un texto corto en el idioma que estudias. El coach corrige gramática, vocabulario y estilo — en el registro que elegiste.",
        "desc_cloze": "📖 **Texto con huecos.** El LLM crea un texto corto con huecos. Tú tecleas las palabras que faltan; el coach las revisa.",
        "desc_translation": "🔁 **Traducir frases.** Unas cuantas frases para traducir — al idioma que estudias o desde él, tú eliges.",
        "desc_quiz": "🎲 **Quiz de vocabulario.** Estilo tarjetas: ves la traducción, escribes la palabra. Tolera pequeños errores de tipeo.",
        "desc_sentence": "🧩 **Construir una frase.** Se te dan unas palabras — construyes una frase que las usa de forma natural.",
        "desc_error": "🔍 **Detectar errores.** El LLM escribe frases con errores de gramática u ortografía. Tú los encuentras y los corriges.",
        "desc_synonym": "🔤 **Sinónimos y antónimos.** Se te da una palabra — produces sinónimos y antónimos en el idioma que estudias.",
        "desc_conjugation": "🔠 **Conjugación de verbos.** Un verbo + una persona — lo conjugas en varios tiempos.",
        "desc_dictation": "🎙️ **Dictado audio.** El LLM escribe un texto corto, ElevenLabs lo lee, tú lo transcribes. Control de velocidad para ralentizar la voz.",
        "desc_reading": "📚 **Comprensión lectora.** Texto generado por IA, URL, texto pegado o .txt subido — luego opción múltiple + preguntas abiertas.",
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
        "cloze_freeform_hint": "💬 Escribe tus respuestas en formato libre — una por línea, separadas por comas o en texto corrido. El LLM las emparejará con los huecos.",
        "num_sentences": "Número de frases",
        "error_no_key": "🔑 No hay clave API. Introduce tu clave OpenRouter en la barra lateral.",
        "error_no_key_hint": "💡 Consigue una en https://openrouter.ai/keys — la clave solo vive en tu sesión.",
        "quiz_new_btn": "🎲 Nuevo quiz",
        "quiz_evaluate_btn": "✅ Evaluar",
        "quiz_score": "🎯 Puntuación",
        "quiz_prompt_format": "¿Cuál es la palabra en {language} para «{trans}»?",
        "side_questions": "**Preguntas laterales:**",
        "writing_task_prompt": "Escribe un texto sobre el tema: {theme}",
        "cloze_vocab_heading": "Vocabulario (alfabético):",
        "cloze_use_these": "A utilizar",
        "cloze_text_heading": "Texto con huecos:",
        "error_task_prompt": "Encuentra y corrige los errores en el siguiente texto:",
        "sentence_task_prompt": "Construye una frase con estas palabras:",
        "synant_task_prompt": "Encuentra sinónimos y antónimos de:",
        "conjugation_task_prompt": "Conjuga el verbo «{verb}» para la persona «{person}» en los siguientes tiempos: presente, pretérito imperfecto, futuro, pretérito perfecto, subjuntivo presente, futuro próximo, presente continuo.",
        "translation_direction": "Dirección",
        "dir_to_learning": "→ a {learning} (producir)",
        "dir_to_native": "→ a {native} (comprender)",
        "current_vocabs": "📖 Vocabulario actual ({n})",
        "no_vocabs_yet": "_Aún no se ha cargado vocabulario._",
        "learning_language": "🎯 Idioma a aprender",
        "dict_speed": "🐢 ⇄ 🐇  Velocidad de reproducción",
        "dict_reveal": "🔍 Revelar el original",
        "dict_your_transcript": "✏️ ¿Qué escuchaste?",
        "dict_original": "📜 Texto original",
        "dict_no_key": "🎙️ El dictado requiere una clave ElevenLabs. Añade `ELEVENLABS_KEY` a tu `.env`.",
        "dict_generate": "🎙️ Generar nuevo dictado",
        "dict_status_text": "🧠 Redactando el texto…",
        "dict_status_tts": "🎙️ Sintetizando la voz…",
        "dict_status_ready": "✅ Dictado listo — escucha y transcribe",
        "dict_tts_error": "❌ Error de TTS: {err}",
        "elevenlabs_key": "🎙️ Clave API ElevenLabs (opcional)",
        "elevenlabs_key_help": "Para la TTS del dictado. Solo en la sesión, nunca se guarda. Consigue una en elevenlabs.io.",
        "back_to_app": "Volver a la app",
        "nav_about": "Acerca de",
        "about_title": "ℹ️ Acerca de lingua",
        "about_body": (
            "**lingua-app** es un tutor de idiomas con IA pensado para practicar hasta nivel C1/C2, "
            "con correcciones sensibles al registro de lengua y personas de mentor que cambian la "
            "voz del feedback.\n\n"
            "### Lo destacado\n"
            "Qué diferencia a lingua-app de las apps de idiomas más populares (Duolingo, Babbel, Busuu):\n\n"
            "- **Siete registros de lengua**, no solo 'formal vs. informal' — el LLM ajusta la "
            "corrección al registro en el que estás escribiendo (argot · vulgar · coloquial · "
            "estándar · formal · literario · técnico).\n"
            "- **Diez personas de mentor** — desde Profesor amable hasta Maquiavelo. El contraste "
            "estilístico hace que los errores se recuerden.\n"
            "- **Diez tipos de ejercicios** — redacción, texto con huecos, traducción (ambos sentidos), "
            "construcción de frases, detección de errores, sinónimos/antónimos, conjugación de verbos, "
            "quiz de vocabulario, dictado audio (ElevenLabs, con control de velocidad) y comprensión "
            "lectora (generado por IA / URL / texto pegado / TXT → opción múltiple + preguntas abiertas).\n"
            "- **BYOK (Bring Your Own Key)** — tus claves de OpenRouter y ElevenLabs se quedan en "
            "tu sesión del navegador. Nunca se guardan ni se registran. Los beta-testers pueden "
            "dejarlo vacío — se usará la clave del servidor.\n"
            "- **Siete idiomas a aprender** — francés, inglés, español, ucraniano, alemán, polaco, hebreo.\n"
            "- **Siete idiomas de interfaz** — inglés, alemán, francés, español, ucraniano, polaco, "
            "hebreo, con detección automática por IP en la primera visita.\n\n"
            "### Autor\n"
            "Creado por **Bastian Brand** ([Sitio web](https://www.bastian-brand.com/) · "
            "[GitHub](https://github.com/miraculix95) · [LinkedIn](https://www.linkedin.com/in/dr-bastian-brand/)) — "
            "consultor independiente con sede en Múnich en análisis de datos, finanzas y automatización con IA, "
            "ex McKinsey, con clientes de private equity, viajes, seguros y automoción en toda Europa. "
            "lingua-app se escribió originalmente a principios de 2025 como herramienta personal para practicar "
            "francés C1; refactorizado en 2026 en esta versión modular, testada y multilingüe.\n\n"
            "### Código fuente\n"
            "[lingua-app en GitHub](https://github.com/miraculix95/lingua-app) — open source bajo licencia MIT. Issues, PRs y feedback son bienvenidos."
        ),
        "setup_guide_title": "🚀 ¿Primera vez aquí? Configuración en 2 min",
        "setup_guide_body": (
            "> 🧪 **¿Beta-tester? No hace falta clave.** Salta el paso 1 — la app usa una clave del servidor compartida. Pasa directamente al paso 4.\n\n"
            "**1. Consigue una clave API de OpenRouter** (solo para no-beta)\n\n"
            "- Ve a [openrouter.ai/keys](https://openrouter.ai/keys) e inicia sesión (Google, GitHub o email)\n"
            "- Haz clic en **Create Key**, copia la clave (empieza por `sk-or-...`)\n"
            "- Añade 5 $ de crédito en **Settings → Credits** — alcanza para cientos de ejercicios\n"
            "- Pega la clave abajo en **🤖 Modelo y API**\n\n"
            "**2. (Opcional) Clave de ElevenLabs** — solo para el dictado\n\n"
            "- Ve a [elevenlabs.io](https://elevenlabs.io) → regístrate (el tier gratuito incluye ~10 min de TTS/mes)\n"
            "- **Profile → API Keys → Create Key**, cópiala (empieza por `xi-...`)\n"
            "- Pégala abajo en **🤖 Modelo y API**\n\n"
            "**3. Tus claves permanecen solo en tu sesión del navegador** — nada se guarda ni se registra en el servidor.\n\n"
            "**4. Elige idioma, nivel y tipo de ejercicio.** El vocabulario se genera automáticamente si no cargas el tuyo."
        ),
        "el_source_byok": "🎙️ Voz: tu clave ElevenLabs (BYOK)",
        "el_source_env": "🎙️ Voz: .env servidor ElevenLabs",
        "sidebar_heading": "⚙️ Configuración",
        "main_heading": "🎯 Área de práctica",
        "home_btn": "🔄 Reiniciar",
        "help_home": "Descarta la tarea actual y vuelve al selector de ejercicios. Idioma, nivel, registro, vocabulario y claves se mantienen.",
        "how_it_works": "👈 **Paso 1 — barra lateral:** configura coach, nivel, registro, fuente de vocabulario y clave API. **Paso 2 — aquí:** elige un ejercicio abajo y pulsa **Nueva tarea**.",
        "help_ui_language": "Idioma de botones, etiquetas y correcciones.",
        "help_learning_language": "El idioma que quieres practicar. Cambiable en cualquier momento — el vocabulario se reinicia.",
        "help_coach": "La persona que escribe tu corrección. Solo estilo — la gramática no cambia.",
        "help_level": "Tu nivel MCER (A1 principiante → C2 casi nativo). Textos y preguntas se ajustan.",
        "help_register": "Registro social que el LLM usa y corrige — de la jerga callejera a la prosa técnica.",
        "help_num_vocab": "Cuántas palabras extraer/generar de la fuente.",
        "help_url": "Pega la URL de un artículo — la app extrae vocabulario de ahí.",
        "help_ready_vocab": "Archivo de texto, una palabra por línea.",
        "help_model_tier": "Budget es el más barato; Best el más preciso. Para idiomas no-ingleses se usa un modelo más fuerte por defecto.",
        "help_choose_exercise": "Elige qué tipo de práctica quieres hacer ahora. Cada opción es una forma distinta de trabajar tu vocabulario — rellenar huecos, traducir frases, escuchar un dictado, leer un texto y responder preguntas, etc. Cambiable en cualquier momento.",
        "help_new_task": "Regenerar una tarea con los ajustes actuales.",
        "help_correct": "Enviar tu respuesta al coach para corregir.",
        "help_num_blanks": "Cuántos huecos tendrá el texto.",
        "help_num_sentences": "Cuántas frases para traducir.",
        "help_dict_generate": "El LLM escribe un texto corto, ElevenLabs lo pronuncia. Tú transcribes, la app compara.",
        "help_dict_speed": "Ralentizar o acelerar la voz sin cambiar el tono.",
        "help_read_source": "De dónde viene el texto: generado por IA, página web, texto pegado, o .txt subido.",
        "help_read_length": "Número aproximado de palabras para el texto generado por IA.",
        "help_read_theme": "Tema opcional — p. ej. «clima», «urbanismo», «infancia».",
        "help_read_generate": "Obtiene el texto y redacta preguntas (MC + abiertas).",
        "help_read_submit": "Evaluar: MC se cuenta localmente, las respuestas abiertas las califica el LLM contra una referencia.",
        "read_source": "📖 Fuente del texto",
        "read_source_ai": "Generar con IA",
        "read_source_url": "Cargar desde URL",
        "read_source_paste": "Pegar texto",
        "read_source_file": "Subir .txt",
        "read_length": "📏 Longitud",
        "read_length_short": "Corto (~150 palabras)",
        "read_length_medium": "Medio (~350 palabras)",
        "read_length_long": "Largo (~600 palabras)",
        "read_theme": "🎯 Tema",
        "read_url_placeholder": "https://…",
        "read_paste_placeholder": "Pega aquí el texto para leer…",
        "read_generate": "📖 Generar texto y preguntas",
        "read_status_text": "🧠 Redactando el texto…",
        "read_status_fetch": "🌐 Cargando la página…",
        "read_status_questions": "🧠 Redactando preguntas…",
        "read_status_ready": "✅ Texto y preguntas listos",
        "read_passage_heading": "Texto",
        "read_mc_heading": "Opción múltiple",
        "read_open_heading": "Preguntas abiertas",
        "read_submit": "✅ Evaluar",
        "read_score": "🎯 Puntuación MC",
        "read_open_feedback": "Respuestas abiertas",
        "read_need_passage": "Aún no hay texto. Genera o carga uno primero.",
        "read_url_failed": "❌ No se pudo cargar la URL: {err}",
        "read_verdict_CORRECT": "✅ Correcto",
        "read_verdict_PARTIAL": "🟡 Parcialmente correcto",
        "read_verdict_INCORRECT": "❌ Incorrecto",
        "read_verdict_ERROR": "⚠️ No se pudo evaluar",
        "read_reveal_answers": "🔍 Mostrar respuestas MC correctas",
        "read_reference_answer": "Respuesta de referencia",
    },
    "uk": {
        "app_title": "{language} — Мовний тренер",
        "meta_hint": "💡 Обертай мета-питання кутовими дужками, напр. `<що означає passé composé?>` — отримаєш окрему відповідь.",
        "sidebar_title": "🇫🇷 Вивчати {language}",
        "ui_language": "🌍 Мова інтерфейсу",
        "dark_mode": "🌙 Темна тема",
        "coach_and_style": "👤 Тренер і стиль",
        "vocab_source": "📚 Джерело словника",
        "model_api": "🤖 Модель та API",
        "coach": "Тренер",
        "level": "Рівень мови",
        "register": "Регістр",
        "txt_files": "Txt-файли",
        "txt_files_help": "Витягує словник на вибраному рівні.",
        "num_vocab": "Кількість слів",
        "webpage_url": "URL сторінки",
        "ready_vocab_file": "Готовий файл словника",
        "api_key": "🔑 API-ключ OpenRouter",
        "api_key_help": "🧪 Бета-тестер? Залиш порожнім — використається ключ сервера. Інакше: твій ключ, тільки в сесії, ніколи не зберігається. Отримай на openrouter.ai/keys.",
        "model_tier": "Рівень моделі",
        "key_source_byok": "✅ Твій ключ (BYOK)",
        "key_source_or": "🔑 Сервер .env (OpenRouter)",
        "key_source_oa": "⚠️ Сервер .env (OpenAI)",
        "key_source_none": "❌ Ключ не знайдено",
        "key_source_label": "Джерело ключа",
        "metric_tasks": "📚 Завдання",
        "metric_corrections": "✏️ Корекції",
        "metric_runs": "🔄 Сесії",
        "choose_exercise": "🎯 Вибрати тип вправи",
        "practice_intro": "Обери тип вправи нижче. Кожен тип — інший спосіб попрактикувати словник — зосередься на одному або пройди всі по черзі.",
        "types_overview_title": "📖 Які є типи вправ?",
        "desc_writing": "📝 **Вільне письмо.** Отримуєш тему і пишеш короткий текст мовою, яку вивчаєш. Коуч виправляє граматику, лексику і стиль — у вибраному регістрі.",
        "desc_cloze": "📖 **Текст із пропусками.** LLM створює короткий текст із пропусками. Ти вписуєш потрібні слова; коуч перевіряє.",
        "desc_translation": "🔁 **Переклад речень.** Кілька речень для перекладу — у мову, яку вивчаєш, або з неї, на твій вибір.",
        "desc_quiz": "🎲 **Словниковий квіз.** Формат карток: бачиш переклад, вводиш слово. Терпить дрібні одруки.",
        "desc_sentence": "🧩 **Побудова речення.** Дано кілька слів — будуєш речення, яке їх природно використовує.",
        "desc_error": "🔍 **Пошук помилок.** LLM пише речення з граматичними або орфографічними помилками. Ти їх знаходиш і виправляєш.",
        "desc_synonym": "🔤 **Синоніми та антоніми.** Дано слово — ти наводиш синоніми й антоніми мовою, яку вивчаєш.",
        "desc_conjugation": "🔠 **Дієвідмінювання.** Дано дієслово + особу — ти відмінюєш його в кількох часах.",
        "desc_dictation": "🎙️ **Аудіодиктант.** LLM пише короткий текст, ElevenLabs його читає, ти записуєш. Повзунок швидкості — щоб сповільнити голос.",
        "desc_reading": "📚 **Читання з розумінням.** Текст, згенерований ШІ, URL, вставлений текст або .txt — потім тест + відкриті питання.",
        "new_task_btn": "🎯 Нове завдання",
        "correct_btn": "📝 Перевірити текст",
        "task_heading": "Завдання",
        "your_answer": "✏️ Твоя відповідь:",
        "your_answer_placeholder": "Пиши {language}ою… Мета-питання в <>.",
        "no_vocab_info": "Словник не завантажено. Вибери джерело вище або:",
        "autogen_vocab_btn": "🎲 Згенерувати словник автоматично",
        "status_extract_file": "📚 Витягую словник з файлу…",
        "status_load_url": "🌐 Завантажую {url}…",
        "status_extract_web": "🧠 Витягую словник…",
        "status_extracted_ok": "✅ Витягнуто {n} слів",
        "status_extract_web_ok": "✅ {n} слів з веб",
        "status_generating_task": "🧠 {task}…",
        "status_task_ready": "✅ Завдання готове",
        "status_generating_vocab": "🧠 Генерую словник…",
        "status_gen_vocab_ok": "✅ Згенеровано {n} слів",
        "status_coach_reading": "🧠 {mentor} читає…",
        "status_feedback_ready": "✅ Фідбек готовий",
        "status_generating_quiz": "🧠 Генерую квіз…",
        "status_quiz_ready": "✅ Квіз готовий",
        "vocab_loaded_ok": "✅ Завантажено {n} слів",
        "num_blanks": "Кількість пропусків",
        "cloze_freeform_hint": "💬 Відповіді можна писати в будь-якому форматі — по одному на рядок, через кому або суцільним текстом. LLM зіставить їх з пропусками.",
        "num_sentences": "Кількість речень",
        "error_no_key": "🔑 Немає API-ключа. Введи свій OpenRouter-ключ у сайдбарі.",
        "error_no_key_hint": "💡 Отримай на https://openrouter.ai/keys — ключ залишається тільки в твоїй сесії.",
        "quiz_new_btn": "🎲 Новий квіз",
        "quiz_evaluate_btn": "✅ Оцінити",
        "quiz_score": "🎯 Результат",
        "quiz_prompt_format": "Яке слово {language}ою для «{trans}»?",
        "side_questions": "**Супутні питання:**",
        "writing_task_prompt": "Напиши текст на тему: {theme}",
        "cloze_vocab_heading": "Словник (за алфавітом):",
        "cloze_use_these": "Використай",
        "cloze_text_heading": "Текст з пропусками:",
        "error_task_prompt": "Знайди та виправ помилки в наступному тексті:",
        "sentence_task_prompt": "Побудуй речення з цими словами:",
        "synant_task_prompt": "Знайди синоніми та антоніми до:",
        "conjugation_task_prompt": "Провідміняй дієслово «{verb}» для особи «{person}» у наступних часах: теперішній, минулий, майбутній, доконаний минулий, теперішній умовний, найближчий майбутній, теперішній тривалий.",
        "translation_direction": "Напрям",
        "dir_to_learning": "→ на {learning} (активно)",
        "dir_to_native": "→ на {native} (зрозуміти)",
        "current_vocabs": "📖 Поточний словник ({n})",
        "no_vocabs_yet": "_Словник ще не завантажено._",
        "learning_language": "🎯 Мова вивчення",
        "dict_speed": "🐢 ⇄ 🐇  Швидкість відтворення",
        "dict_reveal": "🔍 Показати оригінал",
        "dict_your_transcript": "✏️ Що ти почув(ла)?",
        "dict_original": "📜 Оригінальний текст",
        "dict_no_key": "🎙️ Для диктанту потрібен ключ ElevenLabs. Додай `ELEVENLABS_KEY` до `.env`.",
        "dict_generate": "🎙️ Згенерувати новий диктант",
        "dict_status_text": "🧠 Пишу текст…",
        "dict_status_tts": "🎙️ Синтезую голос…",
        "dict_status_ready": "✅ Диктант готовий — слухай і пиши",
        "dict_tts_error": "❌ Помилка TTS: {err}",
        "elevenlabs_key": "🎙️ API-ключ ElevenLabs (опційно)",
        "elevenlabs_key_help": "Для TTS диктанту. Тільки в сесії, ніколи не зберігається. Отримай на elevenlabs.io.",
        "el_source_byok": "🎙️ Голос: твій ключ ElevenLabs (BYOK)",
        "el_source_env": "🎙️ Голос: сервер .env ElevenLabs",
        "back_to_app": "Назад до застосунку",
        "nav_about": "Про",
        "about_title": "ℹ️ Про lingua",
        "about_body": (
            "**lingua-app** — це мовний тренер на базі ШІ для практики до рівня C1/C2, з "
            "виправленнями, що враховують мовний регістр, і персонами-наставниками, які змінюють "
            "голос фідбеку.\n\n"
            "### Особливості\n"
            "Чим lingua-app відрізняється від масових мовних застосунків (Duolingo, Babbel, Busuu):\n\n"
            "- **Сім мовних регістрів**, не просто «формальний проти неформального» — LLM узгоджує "
            "виправлення з регістром, у якому ти пишеш (злодійський жаргон · вульгарний · "
            "розмовний · стандартний · формальний · літературний · технічний).\n"
            "- **Десять персон-наставників** — від Доброго вчителя до Макіавеллі. Стилістичний "
            "контраст робить помилки запам'ятовуваними.\n"
            "- **Десять типів вправ** — письмо, пропуски, переклад (в обох напрямках), побудова "
            "речень, виявлення помилок, синоніми/антоніми, дієвідмінювання, словниковий квіз, "
            "аудіодиктант (ElevenLabs, зі слайдером швидкості) та читання з розумінням "
            "(згенероване ШІ / URL / вставлений текст / TXT → тест + відкриті питання).\n"
            "- **BYOK (Bring Your Own Key)** — твої ключі OpenRouter і ElevenLabs залишаються "
            "в сесії браузера. Ніколи не зберігаються і не логуються. Бета-тестери можуть "
            "залишити порожнім — використається ключ сервера.\n"
            "- **Сім мов для вивчення** — французька, англійська, іспанська, українська, німецька, польська, іврит.\n"
            "- **Сім мов інтерфейсу** — англійська, німецька, французька, іспанська, українська, "
            "польська, іврит, з авто-визначенням за IP при першому відвідуванні.\n\n"
            "### Автор\n"
            "Створено **Бастіаном Брандом** ([Вебсайт](https://www.bastian-brand.com/) · "
            "[GitHub](https://github.com/miraculix95) · [LinkedIn](https://www.linkedin.com/in/dr-bastian-brand/)) — "
            "незалежним консультантом з Мюнхена з аналізу даних, фінансів та AI-автоматизації, випускником McKinsey, "
            "з клієнтами з приватного капіталу, туризму, страхування та автомобільної галузі по всій Європі. "
            "lingua-app початково написано у 2025 році як персональний інструмент для практики французької C1; "
            "у 2026 рефакторено в цей модульний, тестований, багатомовний реліз.\n\n"
            "### Сирцевий код\n"
            "[lingua-app на GitHub](https://github.com/miraculix95/lingua-app) — open source під ліцензією MIT. Issues, PR та фідбек вітаються."
        ),
        "setup_guide_title": "🚀 Вперше тут? Налаштування за 2 хвилини",
        "setup_guide_body": (
            "> 🧪 **Бета-тестер? Ключ не потрібен.** Пропусти крок 1 — застосунок використовує спільний ключ сервера. Переходь одразу до кроку 4.\n\n"
            "**1. Отримай API-ключ OpenRouter** (лише для не-бета користувачів)\n\n"
            "- Перейди на [openrouter.ai/keys](https://openrouter.ai/keys) і увійди (Google, GitHub або email)\n"
            "- Натисни **Create Key**, скопіюй ключ (починається з `sk-or-...`)\n"
            "- Додай $5 кредиту в **Settings → Credits** — вистачить на сотні вправ\n"
            "- Встав ключ нижче в **🤖 Модель та API**\n\n"
            "**2. (Опційно) Ключ ElevenLabs** — тільки для диктанту\n\n"
            "- Зайди на [elevenlabs.io](https://elevenlabs.io) → зареєструйся (безкоштовний рівень ~10 хв TTS/місяць)\n"
            "- **Profile → API Keys → Create Key**, скопіюй (починається з `xi-...`)\n"
            "- Встав нижче в **🤖 Модель та API**\n\n"
            "**3. Ключі залишаються тільки в твоїй сесії браузера** — нічого не зберігається і не логується на сервері.\n\n"
            "**4. Вибери мову вивчення, рівень і тип вправи.** Словник генерується автоматично, якщо не завантажиш свій."
        ),
        "sidebar_heading": "⚙️ Налаштування",
        "main_heading": "🎯 Зона вправ",
        "home_btn": "🔄 Скинути",
        "help_home": "Скасувати поточне завдання і повернутися до вибору вправи. Мова, рівень, регістр, словник і ключі зберігаються.",
        "how_it_works": "👈 **Крок 1 — бічна панель:** налаштуй коуча, рівень, регістр, джерело словника та API-ключ. **Крок 2 — тут:** обери вправу нижче та натисни **Нове завдання**.",
        "help_ui_language": "Мова кнопок, підписів і відгуків.",
        "help_learning_language": "Мова, яку ти хочеш практикувати. Змінюй коли завгодно — словник обнуляється.",
        "help_coach": "Персона, що пише твою корекцію. Лише стиль — правила граматики ті самі.",
        "help_level": "Твій рівень CEFR (A1 початківець → C2 майже носій). Тексти й питання підлаштовуються.",
        "help_register": "Соціальний регістр, який використовує LLM — від вуличного сленгу до технічної прози.",
        "help_num_vocab": "Скільки слів витягнути/згенерувати з джерела.",
        "help_url": "Встав URL статті — застосунок витягне словник.",
        "help_ready_vocab": "Текстовий файл, одне слово на рядок.",
        "help_model_tier": "Budget — найдешевший, Best — найточніший. Для неанглійських мов за замовчуванням сильніша модель.",
        "help_choose_exercise": "Обери, який тип практики зараз. Кожен варіант — інший спосіб роботи зі словником: заповнення пропусків, переклад речень, прослуховування диктанту, читання тексту та відповіді на питання тощо. Міняй коли завгодно.",
        "help_new_task": "Згенерувати нове завдання з поточними налаштуваннями.",
        "help_correct": "Надіслати відповідь коучу на корекцію.",
        "help_num_blanks": "Скільки пропусків у тексті.",
        "help_num_sentences": "Скільки речень для перекладу.",
        "help_dict_generate": "LLM пише короткий текст, ElevenLabs озвучує. Ти транскрибуєш, застосунок порівнює.",
        "help_dict_speed": "Сповільнити чи прискорити голос без зміни тону.",
        "help_read_source": "Звідки текст: згенерований ШІ, веб-сторінка, вставлений текст або .txt.",
        "help_read_length": "Приблизна кількість слів для згенерованого ШІ тексту.",
        "help_read_theme": "Необов'язкова тема — напр. «клімат», «містобудування», «дитинство».",
        "help_read_generate": "Отримує текст і складає питання (тест + відкриті).",
        "help_read_submit": "Оцінити: тест рахується локально, відкриті відповіді оцінює LLM за еталоном.",
        "read_source": "📖 Джерело тексту",
        "read_source_ai": "Згенерувати ШІ",
        "read_source_url": "Завантажити з URL",
        "read_source_paste": "Вставити текст",
        "read_source_file": "Завантажити .txt",
        "read_length": "📏 Довжина",
        "read_length_short": "Короткий (~150 слів)",
        "read_length_medium": "Середній (~350 слів)",
        "read_length_long": "Довгий (~600 слів)",
        "read_theme": "🎯 Тема",
        "read_url_placeholder": "https://…",
        "read_paste_placeholder": "Встав тут текст для читання…",
        "read_generate": "📖 Згенерувати текст і питання",
        "read_status_text": "🧠 Пишу текст…",
        "read_status_fetch": "🌐 Завантажую сторінку…",
        "read_status_questions": "🧠 Складаю питання…",
        "read_status_ready": "✅ Текст і питання готові",
        "read_passage_heading": "Текст",
        "read_mc_heading": "Множинний вибір",
        "read_open_heading": "Відкриті питання",
        "read_submit": "✅ Оцінити",
        "read_score": "🎯 Бали за тест",
        "read_open_feedback": "Відкриті відповіді",
        "read_need_passage": "Тексту ще немає. Згенеруй або завантаж спочатку.",
        "read_url_failed": "❌ Не вдалося завантажити URL: {err}",
        "read_verdict_CORRECT": "✅ Правильно",
        "read_verdict_PARTIAL": "🟡 Частково правильно",
        "read_verdict_INCORRECT": "❌ Неправильно",
        "read_verdict_ERROR": "⚠️ Не вдалося оцінити",
        "read_reveal_answers": "🔍 Показати правильні відповіді",
        "read_reference_answer": "Еталонна відповідь",
    },
    "pl": {
        "app_title": "{language} — Tutor językowy",
        "meta_hint": "💡 Owiń pytania meta w nawiasy kątowe, np. `<co znaczy passé composé?>` — otrzymasz osobną odpowiedź.",
        "sidebar_title": "🇫🇷 Ucz się: {language}",
        "ui_language": "🌍 Język interfejsu",
        "dark_mode": "🌙 Tryb ciemny",
        "coach_and_style": "👤 Trener i styl",
        "vocab_source": "📚 Źródło słownictwa",
        "model_api": "🤖 Model i API",
        "coach": "Trener",
        "level": "Poziom języka",
        "register": "Rejestr",
        "txt_files": "Pliki Txt",
        "txt_files_help": "Wyciąga słownictwo na wybranym poziomie.",
        "num_vocab": "Liczba słów",
        "webpage_url": "URL strony",
        "ready_vocab_file": "Gotowy plik słownictwa",
        "api_key": "🔑 Klucz API OpenRouter",
        "api_key_help": "🧪 Beta-tester? Zostaw puste — użyty zostanie klucz serwera. Inaczej: Twój klucz, tylko w sesji, nigdy nie zapisywany. Pobierz na openrouter.ai/keys.",
        "model_tier": "Poziom modelu",
        "key_source_byok": "✅ Twój klucz (BYOK)",
        "key_source_or": "🔑 Serwer .env (OpenRouter)",
        "key_source_oa": "⚠️ Serwer .env (OpenAI)",
        "key_source_none": "❌ Nie znaleziono klucza",
        "key_source_label": "Źródło klucza",
        "metric_tasks": "📚 Zadania",
        "metric_corrections": "✏️ Korekty",
        "metric_runs": "🔄 Sesje",
        "choose_exercise": "🎯 Wybierz typ ćwiczenia",
        "practice_intro": "Wybierz typ ćwiczenia poniżej. Każdy typ to inny sposób ćwiczenia słownictwa — skup się na jednym albo przejdź wszystkie po kolei.",
        "types_overview_title": "📖 Jakie są typy ćwiczeń?",
        "desc_writing": "📝 **Pisanie swobodne.** Dostajesz temat i piszesz krótki tekst w języku, którego się uczysz. Coach poprawia gramatykę, słownictwo i styl — w wybranym rejestrze.",
        "desc_cloze": "📖 **Tekst z lukami.** LLM tworzy krótki tekst z lukami. Wpisujesz brakujące słowa; coach sprawdza.",
        "desc_translation": "🔁 **Tłumaczenie zdań.** Kilka zdań do tłumaczenia — na język, którego się uczysz, albo z niego.",
        "desc_quiz": "🎲 **Quiz słownictwa.** Styl fiszek: widzisz tłumaczenie, wpisujesz słowo. Toleruje drobne literówki.",
        "desc_sentence": "🧩 **Budowanie zdania.** Dano kilka słów — budujesz zdanie, które używa ich naturalnie.",
        "desc_error": "🔍 **Wykrywanie błędów.** LLM pisze zdania zawierające błędy gramatyczne lub ortograficzne. Znajdujesz je i poprawiasz.",
        "desc_synonym": "🔤 **Synonimy i antonimy.** Dane słowo — podajesz synonimy i antonimy w języku, którego się uczysz.",
        "desc_conjugation": "🔠 **Koniugacja czasowników.** Dany czasownik + osoba — odmieniasz go w kilku czasach.",
        "desc_dictation": "🎙️ **Dyktando audio.** LLM pisze krótki tekst, ElevenLabs go czyta, ty zapisujesz. Suwak prędkości do spowolnienia głosu.",
        "desc_reading": "📚 **Czytanie ze zrozumieniem.** Tekst wygenerowany przez AI, URL, wklejony tekst albo przesłany .txt — potem test + pytania otwarte.",
        "new_task_btn": "🎯 Nowe zadanie",
        "correct_btn": "📝 Popraw tekst",
        "task_heading": "Zadanie",
        "your_answer": "✏️ Twoja odpowiedź:",
        "your_answer_placeholder": "Pisz po {language}u… Pytania meta w <>.",
        "no_vocab_info": "Brak załadowanego słownictwa. Użyj źródła powyżej lub:",
        "autogen_vocab_btn": "🎲 Wygeneruj słownictwo automatycznie",
        "status_extract_file": "📚 Wyciągam słownictwo z pliku…",
        "status_load_url": "🌐 Ładuję {url}…",
        "status_extract_web": "🧠 Wyciągam słownictwo…",
        "status_extracted_ok": "✅ Wyciągnięto {n} słów",
        "status_extract_web_ok": "✅ {n} słów z sieci",
        "status_generating_task": "🧠 {task}…",
        "status_task_ready": "✅ Zadanie gotowe",
        "status_generating_vocab": "🧠 Generuję słownictwo…",
        "status_gen_vocab_ok": "✅ Wygenerowano {n} słów",
        "status_coach_reading": "🧠 {mentor} czyta…",
        "status_feedback_ready": "✅ Feedback gotowy",
        "status_generating_quiz": "🧠 Generuję quiz…",
        "status_quiz_ready": "✅ Quiz gotowy",
        "vocab_loaded_ok": "✅ Załadowano {n} słów",
        "num_blanks": "Liczba luk",
        "cloze_freeform_hint": "💬 Odpowiedzi możesz wpisywać w dowolnym formacie — po jednej na linię, po przecinku lub w ciągłym tekście. LLM dopasuje je do luk.",
        "num_sentences": "Liczba zdań",
        "error_no_key": "🔑 Brak klucza API. Wpisz swój klucz OpenRouter w pasku bocznym.",
        "error_no_key_hint": "💡 Pobierz na https://openrouter.ai/keys — klucz zostaje tylko w Twojej sesji.",
        "quiz_new_btn": "🎲 Nowy quiz",
        "quiz_evaluate_btn": "✅ Oceń",
        "quiz_score": "🎯 Wynik",
        "quiz_prompt_format": "Jakie jest słowo w {language}u dla «{trans}»?",
        "side_questions": "**Pytania poboczne:**",
        "writing_task_prompt": "Napisz tekst na temat: {theme}",
        "cloze_vocab_heading": "Słownictwo (alfabetycznie):",
        "cloze_use_these": "Użyj",
        "cloze_text_heading": "Tekst z lukami:",
        "error_task_prompt": "Znajdź i popraw błędy w następującym tekście:",
        "sentence_task_prompt": "Zbuduj zdanie z tych słów:",
        "synant_task_prompt": "Znajdź synonimy i antonimy do:",
        "conjugation_task_prompt": "Odmień czasownik «{verb}» dla osoby «{person}» w następujących czasach: teraźniejszy, przeszły niedokonany, przyszły, dokonany przeszły, tryb przypuszczający, bliski przyszły, ciągły teraźniejszy.",
        "translation_direction": "Kierunek",
        "dir_to_learning": "→ na {learning} (produkcja)",
        "dir_to_native": "→ na {native} (rozumienie)",
        "current_vocabs": "📖 Aktualne słownictwo ({n})",
        "no_vocabs_yet": "_Nie załadowano jeszcze słownictwa._",
        "learning_language": "🎯 Język do nauki",
        "dict_speed": "🐢 ⇄ 🐇  Prędkość odtwarzania",
        "dict_reveal": "🔍 Pokaż oryginał",
        "dict_your_transcript": "✏️ Co usłyszałeś(-aś)?",
        "dict_original": "📜 Tekst oryginalny",
        "dict_no_key": "🎙️ Dyktando wymaga klucza ElevenLabs. Dodaj `ELEVENLABS_KEY` do `.env`.",
        "dict_generate": "🎙️ Wygeneruj nowe dyktando",
        "dict_status_text": "🧠 Pisanie tekstu…",
        "dict_status_tts": "🎙️ Synteza głosu…",
        "dict_status_ready": "✅ Dyktando gotowe — słuchaj i zapisuj",
        "dict_tts_error": "❌ Błąd TTS: {err}",
        "elevenlabs_key": "🎙️ Klucz API ElevenLabs (opcjonalnie)",
        "elevenlabs_key_help": "Do TTS dyktanda. Tylko w sesji, nigdy nie zapisywany. Pobierz na elevenlabs.io.",
        "el_source_byok": "🎙️ Głos: Twój klucz ElevenLabs (BYOK)",
        "el_source_env": "🎙️ Głos: serwer .env ElevenLabs",
        "back_to_app": "Powrót do aplikacji",
        "nav_about": "O aplikacji",
        "about_title": "ℹ️ O lingua",
        "about_body": (
            "**lingua-app** to tutor językowy oparty na AI, stworzony do ćwiczenia do poziomu "
            "C1/C2, z korektami wrażliwymi na rejestr językowy i personami mentorów, które "
            "zmieniają głos feedbacku.\n\n"
            "### Wyróżniki\n"
            "Co wyróżnia lingua-app na tle popularnych aplikacji (Duolingo, Babbel, Busuu):\n\n"
            "- **Siedem rejestrów językowych**, nie tylko 'formalny vs. potoczny' — LLM "
            "dopasowuje korektę do rejestru, w którym piszesz (gwara przestępcza · wulgarny · "
            "potoczny · standardowy · formalny · literacki · techniczny).\n"
            "- **Dziesięć person mentorów** — od Miłego nauczyciela do Machiavellego. "
            "Stylistyczny kontrast sprawia, że błędy zapadają w pamięć.\n"
            "- **Dziesięć typów ćwiczeń** — pisanie, luki, tłumaczenie (w obu kierunkach), "
            "budowanie zdań, wykrywanie błędów, synonimy/antonimy, koniugacja czasowników, "
            "quiz słownictwa, dyktando audio (ElevenLabs, z suwakiem prędkości) oraz czytanie "
            "ze zrozumieniem (wygenerowane przez AI / URL / wklejony tekst / TXT → "
            "test + pytania otwarte).\n"
            "- **BYOK (Bring Your Own Key)** — Twoje klucze OpenRouter i ElevenLabs pozostają "
            "w sesji przeglądarki. Nigdy nie są zapisywane ani logowane. Beta-testerzy mogą "
            "zostawić puste — użyty zostanie klucz serwera.\n"
            "- **Siedem języków do nauki** — francuski, angielski, hiszpański, ukraiński, niemiecki, polski, hebrajski.\n"
            "- **Siedem języków interfejsu** — angielski, niemiecki, francuski, hiszpański, "
            "ukraiński, polski, hebrajski, z automatycznym wykrywaniem po IP przy pierwszej wizycie.\n\n"
            "### Autor\n"
            "Stworzony przez **Bastiana Branda** ([Strona](https://www.bastian-brand.com/) · "
            "[GitHub](https://github.com/miraculix95) · [LinkedIn](https://www.linkedin.com/in/dr-bastian-brand/)) — "
            "freelance'owego konsultanta z Monachium w analizie danych, finansach i automatyzacji AI, alumnusa McKinseya, "
            "z klientami z private equity, turystyki, ubezpieczeń i motoryzacji w całej Europie. "
            "lingua-app został napisany pierwotnie na początku 2025 roku jako osobiste narzędzie do ćwiczenia "
            "francuskiego C1; w 2026 zrefaktoryzowany do tej modularnej, testowanej, wielojęzycznej wersji.\n\n"
            "### Kod źródłowy\n"
            "[lingua-app na GitHubie](https://github.com/miraculix95/lingua-app) — open source na licencji MIT. Issues, PR-y i feedback mile widziane."
        ),
        "setup_guide_title": "🚀 Pierwszy raz tutaj? Konfiguracja w 2 min",
        "setup_guide_body": (
            "> 🧪 **Beta-tester? Klucz niepotrzebny.** Pomiń krok 1 — aplikacja korzysta ze współdzielonego klucza serwera. Przejdź od razu do kroku 4.\n\n"
            "**1. Zdobądź klucz API OpenRouter** (tylko dla użytkowników spoza bety)\n\n"
            "- Wejdź na [openrouter.ai/keys](https://openrouter.ai/keys) i zaloguj się (Google, GitHub lub email)\n"
            "- Kliknij **Create Key**, skopiuj go (zaczyna się od `sk-or-...`)\n"
            "- Dodaj 5 $ kredytu w **Settings → Credits** — starczy na setki ćwiczeń\n"
            "- Wklej klucz poniżej w **🤖 Model i API**\n\n"
            "**2. (Opcjonalnie) Klucz ElevenLabs** — tylko do dyktanda\n\n"
            "- Wejdź na [elevenlabs.io](https://elevenlabs.io) → zarejestruj się (darmowy tier ~10 min TTS/miesiąc)\n"
            "- **Profile → API Keys → Create Key**, skopiuj (zaczyna się od `xi-...`)\n"
            "- Wklej poniżej w **🤖 Model i API**\n\n"
            "**3. Klucze zostają tylko w Twojej sesji przeglądarki** — nic nie jest zapisywane ani logowane po stronie serwera.\n\n"
            "**4. Wybierz język nauki, poziom i typ ćwiczenia.** Słownictwo generuje się automatycznie, jeśli nie załadujesz własnego."
        ),
        "sidebar_heading": "⚙️ Konfiguracja",
        "main_heading": "🎯 Obszar ćwiczeń",
        "home_btn": "🔄 Zresetuj",
        "help_home": "Odrzuć bieżące zadanie i wróć do wyboru ćwiczenia. Język, poziom, rejestr, słownictwo i klucze zostają.",
        "how_it_works": "👈 **Krok 1 — pasek boczny:** ustaw coacha, poziom, rejestr, źródło słownictwa i klucz API. **Krok 2 — tutaj:** wybierz ćwiczenie poniżej i kliknij **Nowe zadanie**.",
        "help_ui_language": "Język przycisków, etykiet i korekt.",
        "help_learning_language": "Język, który chcesz ćwiczyć. Można zmienić w dowolnej chwili — słownictwo jest resetowane.",
        "help_coach": "Persona pisząca twoją korektę. Tylko styl — reguły gramatyki się nie zmieniają.",
        "help_level": "Twój poziom CEFR (A1 początkujący → C2 prawie native). Teksty i pytania się dopasowują.",
        "help_register": "Rejestr społeczny, którego używa LLM — od slangu ulicznego do prozy technicznej.",
        "help_num_vocab": "Ile słówek wydobyć/wygenerować ze źródła.",
        "help_url": "Wklej URL artykułu — aplikacja wydobędzie słownictwo.",
        "help_ready_vocab": "Plik tekstowy, jedno słowo na linię.",
        "help_model_tier": "Budget jest najtańszy, Best najdokładniejszy. Dla języków innych niż angielski domyślnie mocniejszy model.",
        "help_choose_exercise": "Wybierz, jaki typ ćwiczenia chcesz zrobić teraz. Każda opcja to inny sposób pracy ze słownictwem — uzupełnianie luk, tłumaczenie zdań, słuchanie dyktanda, czytanie tekstu i odpowiadanie na pytania itd. Można zmienić w dowolnej chwili.",
        "help_new_task": "Wygeneruj nowe zadanie z aktualnymi ustawieniami.",
        "help_correct": "Wyślij odpowiedź do coacha do korekty.",
        "help_num_blanks": "Ile luk w tekście.",
        "help_num_sentences": "Ile zdań do tłumaczenia.",
        "help_dict_generate": "LLM pisze krótki tekst, ElevenLabs go czyta. Ty transkrybujesz, aplikacja porównuje.",
        "help_dict_speed": "Zwolnij lub przyspiesz głos bez zmiany tonu.",
        "help_read_source": "Skąd tekst: wygenerowany przez AI, strona WWW, wklejony tekst lub przesłany .txt.",
        "help_read_length": "Przybliżona liczba słów w tekście generowanym przez AI.",
        "help_read_theme": "Opcjonalny temat — np. 'klimat', 'urbanistyka', 'dzieciństwo'.",
        "help_read_generate": "Pobiera tekst i układa pytania (wielokrotny wybór + otwarte).",
        "help_read_submit": "Oceń: MC liczone lokalnie, odpowiedzi otwarte ocenia LLM na tle wzorca.",
        "read_source": "📖 Źródło tekstu",
        "read_source_ai": "Wygeneruj przez AI",
        "read_source_url": "Załaduj z URL",
        "read_source_paste": "Wklej tekst",
        "read_source_file": "Prześlij .txt",
        "read_length": "📏 Długość",
        "read_length_short": "Krótki (~150 słów)",
        "read_length_medium": "Średni (~350 słów)",
        "read_length_long": "Długi (~600 słów)",
        "read_theme": "🎯 Temat",
        "read_url_placeholder": "https://…",
        "read_paste_placeholder": "Wklej tu tekst do przeczytania…",
        "read_generate": "📖 Wygeneruj tekst i pytania",
        "read_status_text": "🧠 Piszę tekst…",
        "read_status_fetch": "🌐 Ładuję stronę…",
        "read_status_questions": "🧠 Układam pytania…",
        "read_status_ready": "✅ Tekst i pytania gotowe",
        "read_passage_heading": "Tekst",
        "read_mc_heading": "Wielokrotny wybór",
        "read_open_heading": "Pytania otwarte",
        "read_submit": "✅ Oceń",
        "read_score": "🎯 Wynik MC",
        "read_open_feedback": "Odpowiedzi otwarte",
        "read_need_passage": "Brak tekstu. Najpierw wygeneruj lub załaduj.",
        "read_url_failed": "❌ Nie udało się wczytać URL: {err}",
        "read_verdict_CORRECT": "✅ Poprawne",
        "read_verdict_PARTIAL": "🟡 Częściowo poprawne",
        "read_verdict_INCORRECT": "❌ Niepoprawne",
        "read_verdict_ERROR": "⚠️ Nie udało się ocenić",
        "read_reveal_answers": "🔍 Pokaż poprawne odpowiedzi MC",
        "read_reference_answer": "Odpowiedź wzorcowa",
    },
    "he": {
        "app_title": "{language} — מורה לשפה",
        "meta_hint": "💡 עטוף שאלות מטא בסוגריים משולשים, למשל `<מה זה passé composé?>` — תקבל תשובה נפרדת.",
        "sidebar_title": "🇫🇷 ללמוד {language}",
        "ui_language": "🌍 שפת ממשק",
        "dark_mode": "🌙 מצב כהה",
        "coach_and_style": "👤 מאמן וסגנון",
        "vocab_source": "📚 מקור אוצר מילים",
        "model_api": "🤖 מודל ו-API",
        "coach": "מאמן",
        "level": "רמת שפה",
        "register": "מִשלָב",
        "txt_files": "קבצי Txt",
        "txt_files_help": "מחלץ אוצר מילים ברמה שנבחרה.",
        "num_vocab": "כמות מילים",
        "webpage_url": "כתובת URL של דף",
        "ready_vocab_file": "קובץ אוצר מילים מוכן",
        "api_key": "🔑 מפתח API של OpenRouter",
        "api_key_help": "🧪 בודק בטא? השאר ריק — ישמש המפתח של השרת. אחרת: המפתח שלך, נשאר בסשן בלבד, אף פעם לא נשמר. השג באתר openrouter.ai/keys.",
        "model_tier": "דרגת מודל",
        "key_source_byok": "✅ המפתח שלך (BYOK)",
        "key_source_or": "🔑 שרת .env (OpenRouter)",
        "key_source_oa": "⚠️ שרת .env (OpenAI)",
        "key_source_none": "❌ לא נמצא מפתח",
        "key_source_label": "מקור המפתח",
        "metric_tasks": "📚 משימות",
        "metric_corrections": "✏️ תיקונים",
        "metric_runs": "🔄 סשנים",
        "choose_exercise": "🎯 בחר סוג תרגיל",
        "practice_intro": "בחר סוג תרגיל למטה. כל סוג הוא דרך אחרת לתרגל את אוצר המילים שלך — התרכז באחד או עבור על כולם בסדר.",
        "types_overview_title": "📖 מה הם סוגי התרגילים?",
        "desc_writing": "📝 **כתיבה חופשית.** אתה מקבל נושא וכותב טקסט קצר בשפת הלימוד. המאמן מתקן דקדוק, אוצר מילים וסגנון — ברגיסטר שבחרת.",
        "desc_cloze": "📖 **טקסט פעור.** ה-LLM בונה טקסט קצר עם פערים. אתה מקליד את המילים החסרות; המאמן בודק.",
        "desc_translation": "🔁 **תרגום משפטים.** כמה משפטים לתרגום — אל שפת הלימוד או ממנה, לבחירתך.",
        "desc_quiz": "🎲 **חידון אוצר מילים.** סגנון כרטיסים: אתה רואה את התרגום, מקליד את המילה. סובלני לטעויות הקלדה קטנות.",
        "desc_sentence": "🧩 **בניית משפט.** מספר מילים ניתנות — אתה בונה משפט שמשתמש בהן באופן טבעי.",
        "desc_error": "🔍 **איתור שגיאות.** ה-LLM כותב כמה משפטים עם שגיאות דקדוק או כתיב. אתה מוצא ומתקן אותן.",
        "desc_synonym": "🔤 **מילים נרדפות ומנוגדות.** מילה ניתנת — אתה מציע נרדפות ומנוגדות בשפת הלימוד.",
        "desc_conjugation": "🔠 **הטיית פעלים.** פועל + גוף ניתנים — אתה מטה אותו בכמה זמנים.",
        "desc_dictation": "🎙️ **הכתבה קולית.** ה-LLM כותב טקסט קצר, ElevenLabs מקריא אותו, אתה מתמלל. מחוון מהירות להאטת הקול.",
        "desc_reading": "📚 **הבנת הנקרא.** טקסט שנוצר ע\"י AI, URL, טקסט מודבק או קובץ .txt שהועלה — לאחר מכן רב-ברירה + שאלות פתוחות.",
        "new_task_btn": "🎯 משימה חדשה",
        "correct_btn": "📝 תקן טקסט",
        "task_heading": "משימה",
        "your_answer": "✏️ התשובה שלך:",
        "your_answer_placeholder": "כתוב ב{language}… שאלות מטא בתוך <>.",
        "no_vocab_info": "לא נטען אוצר מילים. בחר מקור למעלה או:",
        "autogen_vocab_btn": "🎲 צור אוצר מילים אוטומטית",
        "status_extract_file": "📚 מחלץ אוצר מילים מהקובץ…",
        "status_load_url": "🌐 טוען את {url}…",
        "status_extract_web": "🧠 מחלץ אוצר מילים…",
        "status_extracted_ok": "✅ חולצו {n} מילים",
        "status_extract_web_ok": "✅ {n} מילים מהרשת",
        "status_generating_task": "🧠 {task}…",
        "status_task_ready": "✅ המשימה מוכנה",
        "status_generating_vocab": "🧠 יוצר אוצר מילים…",
        "status_gen_vocab_ok": "✅ נוצרו {n} מילים",
        "status_coach_reading": "🧠 {mentor} קורא…",
        "status_feedback_ready": "✅ הפידבק מוכן",
        "status_generating_quiz": "🧠 יוצר חידון…",
        "status_quiz_ready": "✅ החידון מוכן",
        "vocab_loaded_ok": "✅ נטענו {n} מילים",
        "num_blanks": "מספר פעורים",
        "cloze_freeform_hint": "💬 אפשר להקליד תשובות בכל פורמט — אחת בכל שורה, מופרדות בפסיק או בטקסט רציף. המודל ישבץ אותן לפעורים.",
        "num_sentences": "מספר משפטים",
        "error_no_key": "🔑 אין מפתח API. הכנס את מפתח OpenRouter שלך בסרגל הצד.",
        "error_no_key_hint": "💡 השג באתר https://openrouter.ai/keys — המפתח נשאר רק בסשן שלך.",
        "quiz_new_btn": "🎲 חידון חדש",
        "quiz_evaluate_btn": "✅ הערך",
        "quiz_score": "🎯 ניקוד",
        "quiz_prompt_format": "איך אומרים ב{language} «{trans}»?",
        "side_questions": "**שאלות צדדיות:**",
        "writing_task_prompt": "כתוב טקסט על הנושא: {theme}",
        "cloze_vocab_heading": "אוצר מילים (לפי א״ב):",
        "cloze_use_these": "להשתמש",
        "cloze_text_heading": "טקסט פעור:",
        "error_task_prompt": "מצא ותקן את השגיאות בטקסט הבא:",
        "sentence_task_prompt": "בנה משפט מהמילים הבאות:",
        "synant_task_prompt": "מצא מילים נרדפות ומנוגדות ל:",
        "conjugation_task_prompt": "הטה את הפועל «{verb}» לגוף «{person}» בזמנים הבאים: הווה, עבר, עתיד, הווה מושלם, הווה מותנה, עתיד קרוב, הווה ממושך.",
        "translation_direction": "כיוון",
        "dir_to_learning": "→ ל{learning} (הפקה)",
        "dir_to_native": "→ ל{native} (הבנה)",
        "current_vocabs": "📖 אוצר מילים נוכחי ({n})",
        "no_vocabs_yet": "_עוד לא נטען אוצר מילים._",
        "learning_language": "🎯 שפה ללימוד",
        "dict_speed": "🐢 ⇄ 🐇  מהירות ניגון",
        "dict_reveal": "🔍 חשוף את המקור",
        "dict_your_transcript": "✏️ מה שמעת?",
        "dict_original": "📜 הטקסט המקורי",
        "dict_no_key": "🎙️ הכתבה דורשת מפתח ElevenLabs. הוסף `ELEVENLABS_KEY` ל-`.env`.",
        "dict_generate": "🎙️ צור הכתבה חדשה",
        "dict_status_text": "🧠 כותב את הטקסט…",
        "dict_status_tts": "🎙️ מסנתז קול…",
        "dict_status_ready": "✅ ההכתבה מוכנה — הקשב ותעתק",
        "dict_tts_error": "❌ שגיאת TTS: {err}",
        "elevenlabs_key": "🎙️ מפתח API של ElevenLabs (אופציונלי)",
        "elevenlabs_key_help": "ל-TTS של הכתבה. נשאר בסשן בלבד, אף פעם לא נשמר. השג באתר elevenlabs.io.",
        "el_source_byok": "🎙️ קול: מפתח ElevenLabs שלך (BYOK)",
        "el_source_env": "🎙️ קול: שרת .env של ElevenLabs",
        "back_to_app": "חזרה לאפליקציה",
        "nav_about": "אודות",
        "about_title": "ℹ️ אודות lingua",
        "about_body": (
            "**lingua-app** הוא מורה לשפה מבוסס בינה מלאכותית לתרגול עד רמת C1/C2, עם "
            "תיקונים רגישים למשלב לשוני ודמויות מנטור שמחליפות את הקול של הפידבק.\n\n"
            "### נקודות בולטות\n"
            "מה מבדיל את lingua-app מאפליקציות שפה רגילות (Duolingo, Babbel, Busuu):\n\n"
            "- **שבעה משלבים לשוניים**, לא רק 'רשמי מול יומיומי' — המודל מתאים את התיקון "
            "למשלב שבו אתה כותב (סלנג עברייני · וולגרי · יומיומי · סטנדרטי · רשמי · ספרותי · טכני).\n"
            "- **עשר דמויות מנטור** — ממורה חביב ועד מקיאוולי. הניגוד הסגנוני עושה את "
            "השגיאות בלתי נשכחות.\n"
            "- **עשרה סוגי תרגילים** — כתיבה, פעורים, תרגום (בשני הכיוונים), בניית משפטים, "
            "איתור שגיאות, מילים נרדפות/מנוגדות, הטיית פעלים, חידון אוצר מילים, "
            "הכתבה (ElevenLabs, עם שליטה במהירות) והבנת הנקרא (שנוצר ע\"י AI / URL / טקסט "
            "מודבק / TXT → רב-ברירה + שאלות פתוחות).\n"
            "- **BYOK (Bring Your Own Key)** — המפתחות שלך ב-OpenRouter וב-ElevenLabs נשארים "
            "בסשן הדפדפן בלבד. אף פעם לא נשמרים ולא נרשמים. בודקי בטא יכולים להשאיר ריק — "
            "ישמש המפתח של השרת.\n"
            "- **שבע שפות ללימוד** — צרפתית, אנגלית, ספרדית, אוקראינית, גרמנית, פולנית, עברית.\n"
            "- **שבע שפות ממשק** — אנגלית, גרמנית, צרפתית, ספרדית, אוקראינית, פולנית, "
            "עברית, עם זיהוי אוטומטי לפי IP בביקור ראשון.\n\n"
            "### המחבר\n"
            "נבנה על ידי **בסטיאן ברנד** ([אתר](https://www.bastian-brand.com/) · "
            "[GitHub](https://github.com/miraculix95) · [LinkedIn](https://www.linkedin.com/in/dr-bastian-brand/)) — "
            "יועץ עצמאי ממינכן בתחום ניתוח נתונים, פיננסים ואוטומציית AI, בוגר מקינזי, "
            "עם לקוחות מתעשיית ה-private equity, התיירות, הביטוח והרכב ברחבי אירופה. "
            "lingua-app נכתב במקור בתחילת 2025 ככלי אישי לתרגול צרפתית ברמת C1; "
            "ב-2026 עבר ריפקטורינג לגרסה מודולרית, מתוכלת ורב-לשונית זו.\n\n"
            "### קוד מקור\n"
            "[lingua-app ב-GitHub](https://github.com/miraculix95/lingua-app) — קוד פתוח ברישיון MIT. Issues, PRs ופידבק יתקבלו בברכה."
        ),
        "setup_guide_title": "🚀 פעם ראשונה כאן? הגדרה ב-2 דקות",
        "setup_guide_body": (
            "> 🧪 **בודק בטא? לא נחוץ מפתח.** דלג על שלב 1 — האפליקציה משתמשת במפתח שרת משותף. עבור ישר לשלב 4.\n\n"
            "**1. השג מפתח API של OpenRouter** (רק למשתמשים שאינם בטא)\n\n"
            "- עבור אל [openrouter.ai/keys](https://openrouter.ai/keys) והתחבר (Google, GitHub או מייל)\n"
            "- לחץ על **Create Key**, העתק אותו (מתחיל ב-`sk-or-...`)\n"
            "- הוסף 5$ קרדיט תחת **Settings → Credits** — מספיק למאות תרגילים\n"
            "- הדבק את המפתח למטה ב-**🤖 מודל ו-API**\n\n"
            "**2. (אופציונלי) מפתח ElevenLabs** — רק אם תרצה את תרגיל ההכתבה\n\n"
            "- עבור אל [elevenlabs.io](https://elevenlabs.io) → הירשם (הרמה החינמית כוללת ~10 דקות TTS בחודש)\n"
            "- **Profile → API Keys → Create Key**, העתק (מתחיל ב-`xi-...`)\n"
            "- הדבק למטה ב-**🤖 מודל ו-API**\n\n"
            "**3. המפתחות שלך נשארים רק בסשן הדפדפן** — שום דבר לא נשמר ולא נרשם בצד השרת.\n\n"
            "**4. בחר שפה ללימוד, רמה וסוג תרגיל.** אוצר המילים נוצר אוטומטית אם לא תטען משלך."
        ),
        "sidebar_heading": "⚙️ הגדרות",
        "main_heading": "🎯 אזור תרגול",
        "home_btn": "🔄 איפוס",
        "help_home": "נקה את המשימה הנוכחית וחזור לבחירת תרגיל. שפה, רמה, רגיסטר, אוצר מילים ומפתחות נשמרים.",
        "how_it_works": "👈 **שלב 1 — סרגל צד:** הגדר מאמן, רמה, רגיסטר, מקור אוצר מילים ומפתח API. **שלב 2 — כאן:** בחר תרגיל מטה ולחץ **משימה חדשה**.",
        "help_ui_language": "שפת הכפתורים, התוויות והמשובים.",
        "help_learning_language": "השפה שאתה רוצה לתרגל. ניתן להחליף בכל עת — אוצר המילים מתאפס.",
        "help_coach": "הפרסונה שכותבת את התיקון. סגנון בלבד — חוקי הדקדוק נשארים.",
        "help_level": "רמת ה-CEFR שלך (A1 מתחיל → C2 כמעט שפת אם). טקסטים ושאלות מותאמים.",
        "help_register": "הרגיסטר החברתי שבו ה-LLM כותב ומתקן — מסלנג רחוב עד פרוזה טכנית.",
        "help_num_vocab": "כמה מילים לחלץ/לייצר מהמקור.",
        "help_url": "הדבק URL של מאמר — האפליקציה תחלץ אוצר מילים.",
        "help_ready_vocab": "קובץ טקסט, מילה אחת בכל שורה.",
        "help_model_tier": "Budget הוא הזול ביותר; Best המדויק ביותר. לשפות שאינן אנגלית ברירת המחדל היא מודל חזק יותר.",
        "help_choose_exercise": "בחר איזה סוג תרגול אתה רוצה לעשות עכשיו. כל אפשרות היא דרך שונה לעבוד עם אוצר המילים שלך — השלמת חורים, תרגום משפטים, הקשבה להכתבה, קריאת טקסט ומענה על שאלות ועוד. ניתן להחליף בכל עת.",
        "help_new_task": "הפק משימה חדשה עם ההגדרות הנוכחיות.",
        "help_correct": "שלח את התשובה למאמן לתיקון.",
        "help_num_blanks": "כמה חורים בטקסט.",
        "help_num_sentences": "כמה משפטים לתרגום.",
        "help_dict_generate": "ה-LLM כותב טקסט קצר, ElevenLabs מקריא. אתה מתמלל, האפליקציה משווה.",
        "help_dict_speed": "להאט או להאיץ את הקול בלי לשנות את הגובה.",
        "help_read_source": "מאיפה הטקסט: שנוצר ע\"י AI, אתר, טקסט מודבק או קובץ .txt.",
        "help_read_length": "מספר מילים משוער לטקסט שנוצר ע\"י AI.",
        "help_read_theme": "נושא אופציונלי — למשל 'אקלים', 'עירוניות', 'ילדות'.",
        "help_read_generate": "מביא את הטקסט ומנסח שאלות (רב-ברירה + פתוחות).",
        "help_read_submit": "הערכה: רב-ברירה נספר מקומית, תשובות פתוחות מוערכות ע\"י ה-LLM מול תשובה מדגמית.",
        "read_source": "📖 מקור הטקסט",
        "read_source_ai": "הפק באמצעות AI",
        "read_source_url": "טען מ-URL",
        "read_source_paste": "הדבק טקסט",
        "read_source_file": "העלה .txt",
        "read_length": "📏 אורך",
        "read_length_short": "קצר (~150 מילים)",
        "read_length_medium": "בינוני (~350 מילים)",
        "read_length_long": "ארוך (~600 מילים)",
        "read_theme": "🎯 נושא",
        "read_url_placeholder": "https://…",
        "read_paste_placeholder": "הדבק כאן את הטקסט לקריאה…",
        "read_generate": "📖 הפק טקסט ושאלות",
        "read_status_text": "🧠 כותב את הטקסט…",
        "read_status_fetch": "🌐 טוען את הדף…",
        "read_status_questions": "🧠 מנסח שאלות…",
        "read_status_ready": "✅ הטקסט והשאלות מוכנים",
        "read_passage_heading": "טקסט",
        "read_mc_heading": "רב-ברירה",
        "read_open_heading": "שאלות פתוחות",
        "read_submit": "✅ הערך",
        "read_score": "🎯 ציון רב-ברירה",
        "read_open_feedback": "תשובות פתוחות",
        "read_need_passage": "אין עדיין טקסט. הפק או טען אחד קודם.",
        "read_url_failed": "❌ לא ניתן לטעון את ה-URL: {err}",
        "read_verdict_CORRECT": "✅ נכון",
        "read_verdict_PARTIAL": "🟡 נכון חלקית",
        "read_verdict_INCORRECT": "❌ לא נכון",
        "read_verdict_ERROR": "⚠️ לא ניתן להעריך",
        "read_reveal_answers": "🔍 הצג תשובות נכונות",
        "read_reference_answer": "תשובה מדגמית",
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
    # Ukrainian
    "UA": "uk",
    # Polish
    "PL": "pl",
    # Hebrew (Israel)
    "IL": "he",
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


# -- Domain-label translations ------------------------------------------------
# Internal keys stay in the original (German) form from src/config.py so the
# rest of the code doesn't change — these dicts map them to per-UI-lang labels.

# Learning-language names (keys from src.config.LANGUAGES).
LANGUAGE_DISPLAY: dict[str, dict[str, str]] = {
    "en": {
        "französisch": "French", "englisch": "English", "spanisch": "Spanish",
        "ukrainisch": "Ukrainian", "deutsch": "German",
        "polnisch": "Polish", "hebräisch": "Hebrew",
    },
    "de": {
        "französisch": "Französisch", "englisch": "Englisch", "spanisch": "Spanisch",
        "ukrainisch": "Ukrainisch", "deutsch": "Deutsch",
        "polnisch": "Polnisch", "hebräisch": "Hebräisch",
    },
    "fr": {
        "französisch": "français", "englisch": "anglais", "spanisch": "espagnol",
        "ukrainisch": "ukrainien", "deutsch": "allemand",
        "polnisch": "polonais", "hebräisch": "hébreu",
    },
    "es": {
        "französisch": "francés", "englisch": "inglés", "spanisch": "español",
        "ukrainisch": "ucraniano", "deutsch": "alemán",
        "polnisch": "polaco", "hebräisch": "hebreo",
    },
    "uk": {
        "französisch": "французька", "englisch": "англійська", "spanisch": "іспанська",
        "ukrainisch": "українська", "deutsch": "німецька",
        "polnisch": "польська", "hebräisch": "іврит",
    },
    "pl": {
        "französisch": "francuski", "englisch": "angielski", "spanisch": "hiszpański",
        "ukrainisch": "ukraiński", "deutsch": "niemiecki",
        "polnisch": "polski", "hebräisch": "hebrajski",
    },
    "he": {
        "französisch": "צרפתית", "englisch": "אנגלית", "spanisch": "ספרדית",
        "ukrainisch": "אוקראינית", "deutsch": "גרמנית",
        "polnisch": "פולנית", "hebräisch": "עברית",
    },
}

# The English form for use in LLM prompts (prompts are in English).
LANGUAGE_IN_ENGLISH: dict[str, str] = LANGUAGE_DISPLAY["en"]


# Sprachregister (7 levels from src.config.NIVEAU_LEVELS).
NIVEAU_DISPLAY: dict[str, dict[str, str]] = {
    "en": {
        "Gossensprache/Kriminelle Sprache": "Criminal slang",
        "Argot/Vulgär": "Vulgar slang",
        "Umgangssprache": "Colloquial",
        "Standardsprache": "Standard",
        "Gehoben/Vornehm": "Formal / Elevated",
        "Hohe Literatur": "Literary",
        "Technisch": "Technical",
    },
    "de": {
        "Gossensprache/Kriminelle Sprache": "Gossensprache/Kriminelle Sprache",
        "Argot/Vulgär": "Argot/Vulgär",
        "Umgangssprache": "Umgangssprache",
        "Standardsprache": "Standardsprache",
        "Gehoben/Vornehm": "Gehoben/Vornehm",
        "Hohe Literatur": "Hohe Literatur",
        "Technisch": "Technisch",
    },
    "fr": {
        "Gossensprache/Kriminelle Sprache": "Argot criminel",
        "Argot/Vulgär": "Argot / Vulgaire",
        "Umgangssprache": "Familier",
        "Standardsprache": "Standard",
        "Gehoben/Vornehm": "Soutenu / Élevé",
        "Hohe Literatur": "Littéraire",
        "Technisch": "Technique",
    },
    "es": {
        "Gossensprache/Kriminelle Sprache": "Argot criminal",
        "Argot/Vulgär": "Argot / Vulgar",
        "Umgangssprache": "Coloquial",
        "Standardsprache": "Estándar",
        "Gehoben/Vornehm": "Culto / Formal",
        "Hohe Literatur": "Literario",
        "Technisch": "Técnico",
    },
    "uk": {
        "Gossensprache/Kriminelle Sprache": "Кримінальний сленг",
        "Argot/Vulgär": "Вульгарний сленг",
        "Umgangssprache": "Розмовна",
        "Standardsprache": "Стандартна",
        "Gehoben/Vornehm": "Піднесена / Офіційна",
        "Hohe Literatur": "Літературна",
        "Technisch": "Технічна",
    },
    "pl": {
        "Gossensprache/Kriminelle Sprache": "Slang przestępczy",
        "Argot/Vulgär": "Wulgaryzmy / Slang",
        "Umgangssprache": "Potoczny",
        "Standardsprache": "Standardowy",
        "Gehoben/Vornehm": "Podniosły / Wzniosły",
        "Hohe Literatur": "Literacki",
        "Technisch": "Techniczny",
    },
    "he": {
        "Gossensprache/Kriminelle Sprache": "סלנג פלילי",
        "Argot/Vulgär": "סלנג וולגרי",
        "Umgangssprache": "שפה מדוברת",
        "Standardsprache": "סטנדרטי",
        "Gehoben/Vornehm": "רשמי / גבוה",
        "Hohe Literatur": "ספרותי",
        "Technisch": "טכני",
    },
}


# Themes (9 writing topics from src.config.THEMES).
THEME_DISPLAY: dict[str, dict[str, str]] = {
    "en": {
        "Urlaub": "Vacation", "Schule": "School", "Essen": "Food", "Sport": "Sports",
        "Kultur": "Culture", "Medien": "Media", "Raumfahrt": "Space travel",
        "Business": "Business", "Politik": "Politics",
    },
    "de": {
        "Urlaub": "Urlaub", "Schule": "Schule", "Essen": "Essen", "Sport": "Sport",
        "Kultur": "Kultur", "Medien": "Medien", "Raumfahrt": "Raumfahrt",
        "Business": "Business", "Politik": "Politik",
    },
    "fr": {
        "Urlaub": "Vacances", "Schule": "École", "Essen": "Cuisine", "Sport": "Sport",
        "Kultur": "Culture", "Medien": "Médias", "Raumfahrt": "Voyage spatial",
        "Business": "Affaires", "Politik": "Politique",
    },
    "es": {
        "Urlaub": "Vacaciones", "Schule": "Escuela", "Essen": "Comida", "Sport": "Deporte",
        "Kultur": "Cultura", "Medien": "Medios", "Raumfahrt": "Viaje espacial",
        "Business": "Negocios", "Politik": "Política",
    },
    "uk": {
        "Urlaub": "Відпустка", "Schule": "Школа", "Essen": "Їжа", "Sport": "Спорт",
        "Kultur": "Культура", "Medien": "Медіа", "Raumfahrt": "Космонавтика",
        "Business": "Бізнес", "Politik": "Політика",
    },
    "pl": {
        "Urlaub": "Urlop", "Schule": "Szkoła", "Essen": "Jedzenie", "Sport": "Sport",
        "Kultur": "Kultura", "Medien": "Media", "Raumfahrt": "Kosmonautyka",
        "Business": "Biznes", "Politik": "Polityka",
    },
    "he": {
        "Urlaub": "חופשה", "Schule": "בית ספר", "Essen": "אוכל", "Sport": "ספורט",
        "Kultur": "תרבות", "Medien": "תקשורת", "Raumfahrt": "טיסות חלל",
        "Business": "עסקים", "Politik": "פוליטיקה",
    },
}


# Mentor names (only the two generic ones translate — the rest are proper nouns).
MENTOR_DISPLAY: dict[str, dict[str, str]] = {
    "en": {
        "Netter Lehrer": "Kind Teacher",
        "Strenger Lehrer": "Strict Teacher",
    },
    "de": {
        "Netter Lehrer": "Netter Lehrer",
        "Strenger Lehrer": "Strenger Lehrer",
    },
    "fr": {
        "Netter Lehrer": "Professeur sympathique",
        "Strenger Lehrer": "Professeur sévère",
    },
    "es": {
        "Netter Lehrer": "Profesor amable",
        "Strenger Lehrer": "Profesor estricto",
    },
    "uk": {
        "Netter Lehrer": "Добрий учитель",
        "Strenger Lehrer": "Суворий учитель",
    },
    "pl": {
        "Netter Lehrer": "Miły nauczyciel",
        "Strenger Lehrer": "Surowy nauczyciel",
    },
    "he": {
        "Netter Lehrer": "מורה חביב",
        "Strenger Lehrer": "מורה קפדן",
    },
}


# Mentor quotes per UI-lang. Proper nouns' famous quotes kept in their
# canonical English form across all UI-langs (that's how they're best known).
_EN_QUOTES = {
    "Netter Lehrer": "Every mistake is a step forward.",
    "Strenger Lehrer": "Precision is the courtesy of kings.",
    "Dalai Lama": "Be kind whenever possible. It is always possible.",
    "Vitalik Buterin": "Decentralization of power; centralization of knowledge.",
    "Elon Musk": "When something is important enough, you do it even if the odds are not in your favor.",
    "Jesus Christus": "The letter kills, the spirit gives life.",
    "Chairman Mao": "A journey of a thousand miles begins with a single step.",
    "Homer": "Even in sleep, sorrow descends upon our souls.",
    "Konfuzius": "Learning without thought is labor lost; thought without learning is perilous.",
    "Machiavelli": "Fortune favors the bold.",
}

QUOTE_DISPLAY: dict[str, dict[str, str]] = {
    "en": _EN_QUOTES,
    "de": {
        "Netter Lehrer": "Jeder Fehler ist ein Schritt nach vorne.",
        "Strenger Lehrer": "Präzision ist die Höflichkeit der Könige.",
        "Dalai Lama": "Sei freundlich, wann immer es möglich ist. Es ist immer möglich.",
        "Vitalik Buterin": "Dezentralisierung der Macht; Zentralisierung des Wissens.",
        "Elon Musk": "Wenn etwas wichtig genug ist, tust du es auch gegen die Umstände.",
        "Jesus Christus": "Der Buchstabe tötet, der Geist macht lebendig.",
        "Chairman Mao": "Eine Reise von tausend Meilen beginnt mit dem ersten Schritt.",
        "Homer": "Selbst im Schlaf fällt Trauer auf unsere Seele.",
        "Konfuzius": "Lernen ohne Nachdenken ist vergeblich; Nachdenken ohne Lernen ist gefährlich.",
        "Machiavelli": "Das Glück begünstigt die Wagemutigen.",
    },
    "fr": {
        "Netter Lehrer": "Chaque erreur est un pas en avant.",
        "Strenger Lehrer": "La précision est la politesse des rois.",
        "Dalai Lama": "Sois bienveillant chaque fois que c'est possible. C'est toujours possible.",
        "Vitalik Buterin": "Décentralisation du pouvoir ; centralisation du savoir.",
        "Elon Musk": "Quand quelque chose est assez important, on le fait même si les chances sont contre nous.",
        "Jesus Christus": "La lettre tue, l'esprit donne la vie.",
        "Chairman Mao": "Un voyage de mille lieues commence par un premier pas.",
        "Homer": "Même dans le sommeil, le chagrin descend sur nos âmes.",
        "Konfuzius": "Apprendre sans réfléchir est vain ; réfléchir sans apprendre est dangereux.",
        "Machiavelli": "La fortune sourit aux audacieux.",
    },
    "es": {
        "Netter Lehrer": "Cada error es un paso adelante.",
        "Strenger Lehrer": "La precisión es la cortesía de los reyes.",
        "Dalai Lama": "Sé amable siempre que sea posible. Siempre lo es.",
        "Vitalik Buterin": "Descentralización del poder; centralización del conocimiento.",
        "Elon Musk": "Cuando algo es lo bastante importante, lo haces aunque las probabilidades estén en contra.",
        "Jesus Christus": "La letra mata, el espíritu da vida.",
        "Chairman Mao": "Un viaje de mil millas comienza con el primer paso.",
        "Homer": "Incluso en el sueño, la tristeza desciende sobre nuestras almas.",
        "Konfuzius": "Aprender sin reflexionar es vano; reflexionar sin aprender es peligroso.",
        "Machiavelli": "La fortuna favorece a los audaces.",
    },
    "uk": {
        "Netter Lehrer": "Кожна помилка — це крок уперед.",
        "Strenger Lehrer": "Точність — це ввічливість королів.",
        "Dalai Lama": "Будьте добрими, коли тільки можливо. Це завжди можливо.",
        "Vitalik Buterin": "Децентралізація влади; централізація знань.",
        "Elon Musk": "Коли щось справді важливо, ти робиш це, навіть якщо шанси проти тебе.",
        "Jesus Christus": "Літера вбиває, дух оживотворяє.",
        "Chairman Mao": "Подорож у тисячу миль починається з першого кроку.",
        "Homer": "Навіть уві сні сум сходить на наші душі.",
        "Konfuzius": "Навчання без роздумів марне; роздуми без навчання — небезпечні.",
        "Machiavelli": "Фортуна сприяє сміливим.",
    },
    "pl": {
        "Netter Lehrer": "Każdy błąd to krok naprzód.",
        "Strenger Lehrer": "Precyzja to uprzejmość królów.",
        "Dalai Lama": "Bądź życzliwy, kiedy tylko możesz. Zawsze można.",
        "Vitalik Buterin": "Decentralizacja władzy; centralizacja wiedzy.",
        "Elon Musk": "Kiedy coś jest wystarczająco ważne, robisz to, nawet jeśli szanse są przeciw tobie.",
        "Jesus Christus": "Litera zabija, duch ożywia.",
        "Chairman Mao": "Podróż tysiąca mil zaczyna się od jednego kroku.",
        "Homer": "Nawet we śnie smutek zstępuje na nasze dusze.",
        "Konfuzius": "Uczenie się bez myślenia jest daremne; myślenie bez uczenia się jest niebezpieczne.",
        "Machiavelli": "Fortuna sprzyja odważnym.",
    },
    "he": {
        "Netter Lehrer": "כל טעות היא צעד קדימה.",
        "Strenger Lehrer": "הדיוק הוא נימוסי המלכים.",
        "Dalai Lama": "היה אדיב בכל הזדמנות. תמיד אפשר.",
        "Vitalik Buterin": "ביזור הכוח; ריכוז הידע.",
        "Elon Musk": "כשמשהו חשוב מספיק, עושים אותו גם אם הסיכויים נגדך.",
        "Jesus Christus": "האות ממיתה, הרוח מחיה.",
        "Chairman Mao": "מסע של אלף מיל מתחיל בצעד אחד.",
        "Homer": "אפילו בשינה, עצב יורד על נפשותינו.",
        "Konfuzius": "לימוד בלי מחשבה — שווא; מחשבה בלי לימוד — סכנה.",
        "Machiavelli": "המזל מחייך לאמיצים.",
    },
}


# Model-tier labels (keys from src.config.MODEL_TIERS).
TIER_DISPLAY: dict[str, dict[str, str]] = {
    "en": {
        "💰 Budget (Gemini Flash Lite)": "💰 Budget (Gemini Flash Lite)",
        "⚖️ Balanced (Claude Haiku 4.5)": "⚖️ Balanced (Claude Haiku 4.5)",
        "🚀 Premium (Mistral Large 3)": "🚀 Premium (Mistral Large 3)",
        "👑 Best (Claude Sonnet 4.6)": "👑 Best (Claude Sonnet 4.6)",
    },
    "de": {
        "💰 Budget (Gemini Flash Lite)": "💰 Günstig (Gemini Flash Lite)",
        "⚖️ Balanced (Claude Haiku 4.5)": "⚖️ Ausgewogen (Claude Haiku 4.5)",
        "🚀 Premium (Mistral Large 3)": "🚀 Premium (Mistral Large 3)",
        "👑 Best (Claude Sonnet 4.6)": "👑 Bestes (Claude Sonnet 4.6)",
    },
    "fr": {
        "💰 Budget (Gemini Flash Lite)": "💰 Économique (Gemini Flash Lite)",
        "⚖️ Balanced (Claude Haiku 4.5)": "⚖️ Équilibré (Claude Haiku 4.5)",
        "🚀 Premium (Mistral Large 3)": "🚀 Premium (Mistral Large 3)",
        "👑 Best (Claude Sonnet 4.6)": "👑 Meilleur (Claude Sonnet 4.6)",
    },
    "es": {
        "💰 Budget (Gemini Flash Lite)": "💰 Económico (Gemini Flash Lite)",
        "⚖️ Balanced (Claude Haiku 4.5)": "⚖️ Equilibrado (Claude Haiku 4.5)",
        "🚀 Premium (Mistral Large 3)": "🚀 Premium (Mistral Large 3)",
        "👑 Best (Claude Sonnet 4.6)": "👑 Mejor (Claude Sonnet 4.6)",
    },
    "uk": {
        "💰 Budget (Gemini Flash Lite)": "💰 Економний (Gemini Flash Lite)",
        "⚖️ Balanced (Claude Haiku 4.5)": "⚖️ Збалансований (Claude Haiku 4.5)",
        "🚀 Premium (Mistral Large 3)": "🚀 Преміум (Mistral Large 3)",
        "👑 Best (Claude Sonnet 4.6)": "👑 Найкращий (Claude Sonnet 4.6)",
    },
    "pl": {
        "💰 Budget (Gemini Flash Lite)": "💰 Budżetowy (Gemini Flash Lite)",
        "⚖️ Balanced (Claude Haiku 4.5)": "⚖️ Zrównoważony (Claude Haiku 4.5)",
        "🚀 Premium (Mistral Large 3)": "🚀 Premium (Mistral Large 3)",
        "👑 Best (Claude Sonnet 4.6)": "👑 Najlepszy (Claude Sonnet 4.6)",
    },
    "he": {
        "💰 Budget (Gemini Flash Lite)": "💰 חסכוני (Gemini Flash Lite)",
        "⚖️ Balanced (Claude Haiku 4.5)": "⚖️ מאוזן (Claude Haiku 4.5)",
        "🚀 Premium (Mistral Large 3)": "🚀 פרימיום (Mistral Large 3)",
        "👑 Best (Claude Sonnet 4.6)": "👑 הכי טוב (Claude Sonnet 4.6)",
    },
}


def _lookup(table: dict[str, dict[str, str]], key: str, lang: str, fallback: str) -> str:
    """Two-level lookup with safe fallback to fallback string."""
    table_for_lang = table.get(lang) or table.get(DEFAULT_UI_LANG, {})
    return table_for_lang.get(key, fallback)


def language_display(key: str, lang: str) -> str:
    return _lookup(LANGUAGE_DISPLAY, key, lang, key)


def language_to_english(key: str) -> str:
    return LANGUAGE_IN_ENGLISH.get(key, key.capitalize())


def niveau_display(key: str, lang: str) -> str:
    return _lookup(NIVEAU_DISPLAY, key, lang, key)


def theme_display(key: str, lang: str) -> str:
    return _lookup(THEME_DISPLAY, key, lang, key)


def mentor_display(key: str, lang: str) -> str:
    """Proper-noun mentors pass through; only 'Netter Lehrer' / 'Strenger Lehrer' translate."""
    return _lookup(MENTOR_DISPLAY, key, lang, key)


def quote_for(mentor_key: str, lang: str) -> str:
    return _lookup(QUOTE_DISPLAY, mentor_key, lang, "")


def tier_display(key: str, lang: str) -> str:
    return _lookup(TIER_DISPLAY, key, lang, key)


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
