# Gap-Analyse: lingua-app → Virtuelle Sprachschule

Datum: 2026-04-21
Ziel: Vergleich des aktuellen Tools (9 Exercise-Types, BYOK, 7 Lern-Sprachen) gegen die Vision "vollständige virtuelle Sprachschule mit DELF/DALF-Vorbereitung".

Quellen:
- `README.md` (Feature-Matrix, Stand 2026-04-21)
- `src/tasks/` (cloze, conjugation, dictation, error_detection, quiz, sentence_building, synonym_antonym, translation, writing)
- Vorangegangenes Brainstorming (Sprachschul-Übungen, DELF/DALF, Textverständnis-Workflow, SRS)

---

## Scorecard

Legende: ✅ vorhanden · 🟡 teilweise · ❌ fehlt · 🏫 Sprachschul-Core · 📜 DELF/DALF-relevant

### 1. Klassische Sprachschul-Übungen

| Übung | Status | Aktuell | Gap |
|---|---|---|---|
| Grammatik-Drills (fokussiert) | 🟡 | Cloze generisch, Conjugation vorhanden | Kein Fokus-Modus (z.B. "nur Subjonctif", "nur Pronomen"). Lückentext ist vokabel-getrieben, nicht grammatik-getrieben. |
| Transformationsübungen 🏫 | ❌ | — | Aktiv→Passiv, direkte↔indirekte Rede, Zeitenwechsel fehlen komplett. |
| Diktat (dictée) | ✅ | Dictation mit ElevenLabs + Speed-Slider + Diff | Fehlerkategorisierung (Orthographie/Accord/Grammatik) fehlt. |
| Textverständnis 🏫📜 | ❌ | — | **Größte Lücke.** Kein Reading-Comprehension-Modus (KI-Text / URL / PDF / TXT → MC + Freifeld). Kern von DELF Compréhension écrite. |
| Hörverstehen mit Fragen 📜 | ❌ | — | Dictation ≠ Hörverstehen. DELF CO verlangt Audio + QCM/Lücken/W-Fragen, nicht Transkribieren. |
| Rollenspiel / Dialog-Sim 🏫 | ❌ | — | Mentor-System ist Korrektur-Layer, kein Szene-Dialog. Arzt/Bewerbung/Reklamation fehlt. |
| Bildbeschreibung 🏫 | ❌ | — | Kein Bild-Input. |
| Mündliche Produktion 📜 | ❌ | — | Kein User-Audio-Upload, kein Whisper-Ingestion. Voice-only out (TTS), nicht in. |
| Phonetik / Minimalpaare | ❌ | — | — |
| Konversation mit inline-Korrektur | 🟡 | Writing-Task hat Korrektur | Nicht als fließender Chat-Flow — einzeln eingereichte Texte. |
| Résumé / Zusammenfassung 📜 | ❌ | — | Textverständnis-abhängig. |
| Argumentation / Essay 📜 | 🟡 | Writing generisch | Kein Essay-Modus mit Strukturbewertung (These/Argument/Gegenargument/Schluss). |
| Synthèse (C1/C2) 📜 | ❌ | — | Der DELF-Killer. Mehrere Texte → neutrale Zusammenführung. Nicht implementiert. |

### 2. DELF/DALF-Vollabdeckung

| Kompetenz | Abdeckung | Detail |
|---|---|---|
| Compréhension orale | ❌ 0% | Dictation ist kein HV. |
| Compréhension écrite | ❌ 0% | Kein Leseverstehen mit Fragen. |
| Production écrite | 🟡 ~30% | Writing-Task deckt freies Schreiben + Korrektur ab. Textsorten (Email/Leserbrief/Essay/Synthèse) nicht differenziert, keine Wortzahl-Vorgabe, keine Bewertungsraster (Kohärenz, Lexik, Grammatik, Orthographie nach DELF-Grille). |
| Production orale | ❌ 0% | Kein Voice-Input. |

**Fazit:** Von 4 DELF-Kompetenzen ist eine rudimentär (PE), drei fehlen.

### 3. Lern-Infrastruktur (Retention & Progress)

| Feature | Status | Gap |
|---|---|---|
| Spaced Repetition (SRS) | ❌ | Vokabeln verschwinden nach Session. Ohne SRS = kein langfristiger Lernerfolg. **Höchster ROI-Hebel.** |
| Fehler-Journal | ❌ | Korrekturen werden nicht geloggt. User sieht keine Muster. |
| Streak / Tagesziel | ❌ | Kein Retention-Trigger. |
| Adaptive Difficulty | ❌ | Level ist manuell. |
| CEFR-Einstufungstest | ❌ | User muss raten. |
| Schreib-Portfolio | ❌ | Nichts wird persistiert. |
| Progress-Dashboard | ❌ | Kein sichtbarer Fortschritt. |
| Anki-Export | ❌ | — |

**Wichtiger Kontext:** BYOK + Streamlit = keine Server-State. Persistenz müsste entweder (a) LocalStorage/IndexedDB-basiert (Streamlit-unfreundlich), (b) File-Download/Upload (User exportiert/importiert JSON) oder (c) Architektur-Wechsel zu Supabase/Next.js. Entscheidung nicht trivial.

### 4. Content-Breite

| Bereich | Status | Gap |
|---|---|---|
| Registerauswahl | ✅ | 7 Register (Slang → Technisch) — Alleinstellungsmerkmal. |
| Mentor-Personas | ✅ | 10 Personas. |
| Themen-Seeds | ✅ | `themen_liste` vorhanden. |
| Business-Mode | ❌ | Kein gezielter Business-Context (Email-Templates, Meeting-Vokabular, Präsentationen). |
| Kulturmodul | ❌ | Keine Landeskunde-Integration. |
| Textsorten-Vielfalt | 🟡 | Writing ist generisch; keine expliziten Textsorten (Leserbrief, Forum-Post, Bericht, Protokoll). |

### 5. Tech/UX

| Feature | Status |
|---|---|
| 7 Lern-Sprachen | ✅ |
| 4 UI-Sprachen | ✅ |
| Dark/Light-Mode | ✅ |
| Mobile-responsive | ✅ |
| BYOK | ✅ |
| 76 Tests, ~100ms | ✅ |
| Model-Tier-Auswahl | ✅ |
| User-Accounts / Login | ❌ (bewusst: BYOK-Design) |

---

## Gap-Prioritätsmatrix

Bewertet nach Impact (Nähe zur Sprachschul-Vision) × Aufwand (Eng-Tage inkl. Tests).

### 🔴 Kritisch — ohne das keine "Sprachschule"

| # | Gap | Impact | Aufwand | ROI |
|---|---|---|---|---|
| 1 | **Textverständnis-Modus** (KI-gen / URL / PDF / TXT → MC + Freifeld) | Sehr hoch — DELF CE + Sprachschul-Standard | 3-5 Tage (firecrawl + mistral-ocr schon da) | ★★★★★ |
| 2 | **Hörverstehen mit Fragen** (Audio → QCM/Lücken/W-Fragen) | Sehr hoch — DELF CO | 3-4 Tage (ElevenLabs-TTS oder Radio-Stream + Whisper) | ★★★★★ |
| 3 | **SRS-Vokabelsystem** | Sehr hoch — Retention-Killer ohne das | 4-6 Tage (inkl. Persistenz-Entscheidung) | ★★★★★ |
| 4 | **Production écrite mit Textsorten + DELF-Grille** | Hoch — DELF PE | 2-3 Tage (Prompt-Arbeit, kein neues Feature) | ★★★★ |

### 🟡 Wichtig — macht das Tool zur Sprachschule statt Übungssammlung

| # | Gap | Impact | Aufwand | ROI |
|---|---|---|---|---|
| 5 | **Transformationsübungen** | Hoch — klassischer Sprachschul-Drill | 1-2 Tage (pattern wie Cloze) | ★★★★ |
| 6 | **Fehler-Journal** (Persistenz-abhängig) | Hoch | 2-3 Tage (nach SRS-Infra) | ★★★★ |
| 7 | **Rollenspiel / Dialog-Simulation** | Mittel-hoch | 2-3 Tage (Chat-State in Streamlit nicht-trivial) | ★★★ |
| 8 | **Grammatik-Fokus-Modus** (Cloze "nur Subjonctif") | Mittel | 1 Tag (Prompt-Variante) | ★★★★ |
| 9 | **Production orale** (Voice-Input + Whisper + Bewertung) | Hoch — DELF PO | 4-5 Tage (Mic-Capture in Streamlit schwierig) | ★★★ |
| 10 | **Synthèse (C1/C2)** | Mittel (Nische) | 2 Tage (nach Textverständnis) | ★★★ |

### 🟢 Nice-to-have — Differenzierung

| # | Gap | Impact | Aufwand |
|---|---|---|---|
| 11 | CEFR-Einstufungstest | Mittel | 2 Tage |
| 12 | Streak/Tagesziel | Mittel (Persistenz-abhängig) | 1 Tag |
| 13 | Business-Mode | Mittel (zahlende Zielgruppe) | 2 Tage |
| 14 | Kulturmodul | Niedrig | 1-2 Tage |
| 15 | Anki-Export | Niedrig | 1 Tag |
| 16 | Shadowing-Modus | Niedrig-mittel | 2 Tage |
| 17 | Bildbeschreibung | Niedrig | 1 Tag (LLM-Vision) |
| 18 | Phonetik-Drills | Niedrig | 3-4 Tage |

---

## Strategische Beobachtungen

1. **Die drei Top-Gaps (Textverständnis + Hörverstehen + SRS) kippen das Produkt**
   von "Schreibkorrektur-Tool" zu "Sprachschule". Ohne sie bleibt es ein gutes,
   aber eng fokussiertes Writing-Tool. Mit ihnen deckt es den Kern von DELF ab.

2. **BYOK-Architektur wird bei Persistenz zum Engpass.**
   SRS + Fehler-Journal + Portfolio + Streak brauchen persistenten User-State.
   Die saubere Trennung "keine Server-Daten" kollidiert mit dem Lern-Infrastruktur-
   Pillar. Drei Wege:
   - (a) File-basiert (JSON-Download/Upload) — BYOK-rein, aber UX-Reibung
   - (b) LocalStorage via Streamlit-Komponente — fragil
   - (c) Supabase-Backend einführen + Login — das ist der Next.js-Rewrite aus der Roadmap
   **Das ist die zentrale Architektur-Entscheidung vor dem nächsten Ausbau.**
   Als ADR dokumentieren (siehe `~/.claude/rules/adr-discipline.md`).

3. **Voice-Input (Production orale, Phonetik) ist in Streamlit Friktions-reich.**
   Browser-Mic-Capture + Whisper-Upload ist machbar, aber Streamlit-Komponenten
   dafür sind nicht mature. Das ist ein weiteres Argument für Next.js V2.

4. **DELF-Branding ist ein ungehobener Marketing-Hebel.**
   "DELF/DALF-Vorbereitung B1-C2" ist ein klar googelbarer Zielmarkt mit
   zahlungsbereiten Usern. Aktuell kommuniziert das Tool das nicht.
   Erst wenn die 4 Kompetenzen abgedeckt sind, ist das eine tragbare Claim.

5. **Reading-Comprehension ist der "Katalysator-Feature":**
   KI-Textgenerierung hast du schon. firecrawl für URL, mistral-ocr für PDF hast
   du in tools-catalog. MC-Fragen via Function-Calling ist dein bestehendes
   Pattern (`generate_vocabulary_list`). Der Gap ist klein, der Impact riesig.

---

## Empfohlene Roadmap (vier Releases)

- **V1.5 — Reading & Listening** (2 Wochen): Gaps #1 + #2. Deckt zwei von vier DELF-Kompetenzen ab.
- **V1.6 — Retention-Infrastruktur** (2-3 Wochen, Architektur-ADR vorab): SRS + Fehler-Journal + Streak. Braucht Persistenz-Entscheidung.
- **V1.7 — Production-Ausbau** (2 Wochen): PE-Textsorten mit DELF-Grille + Transformationsübungen + Grammatik-Fokus.
- **V2.0 — Next.js + Voice** (Roadmap): Production orale, bessere Mic-Handling, Account-System. Ist der geplante Rewrite.

## Offene Entscheidungen für Bastian

1. **Zielgruppe:** persönliches Tool (dein C1-Französisch) oder marktfähig (DELF-Vorbereitung als SaaS)? Beeinflusst Roadmap massiv.
2. **Persistenz-Architektur:** BYOK-rein (File-Export) oder Backend (Supabase/Next.js)? ADR-Kandidat.
3. **Monetization-Hook:** Wenn marktfähig — Free (BYOK) vs. Paid (managed keys + SRS + Portfolio + Account)?
4. **DELF-Positionierung:** explizit in Claim und UI ("DELF B2 Prep"), oder generisch weiter?

Für (1)+(3) passt `superpowers:brainstorming` vor jedem weiteren Scope-Commit.
Für (2) ein ADR im Konzept-Ticket (Template `TES-434` → architektur-konzept.md).
