from dotenv import load_dotenv, find_dotenv
import streamlit as st
import os
import openai
import random
import re
import argparse

# Load OpenAI API key from environment variables
load_dotenv(find_dotenv())
# openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()
no_answers = " Nenne nicht die Antworten. "
models = ["gpt-4o-mini-2024-07-18", "gpt-4o-2024-05-13", "gpt-3.5-turbo-0125"]
languages = ["französisch", "englisch", "spanisch", "ukrainisch", "deutsch"]
             
parser = argparse.ArgumentParser(description="Streamlit app with argparse")
parser.add_argument("--model", type=str, default="gpt-4o-mini-2024-07-18", help="Model used")
parser.add_argument("--language", type=str, default="französisch", help="Lernsprache")

model = parser.parse_args().model if parser.parse_args().model in models else models[0]
language = parser.parse_args().language if parser.parse_args().language in languages else languages[0]



#########################################################################################################################################################################################

#### laden der Vokabeln
def load_vocabulary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        vocab_list = [line.strip() for line in file]
    return vocab_list

def extract_french_vocabulary(file, level, number_of_words):
    if os.path.isdir(file):
        txt_files = [os.path.join(file, f) for f in os.listdir(file) if f.endswith('.txt')]
    elif os.path.isfile(file) and file.endswith('.txt'):
        txt_files = [file]
    else:
        raise ValueError("Der Pfad muss entweder eine .txt-Datei oder ein Verzeichnis mit .txt-Dateien sein.")

    all_text = ""
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            all_text += f.read() + "\n"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Du bist ein Sprachlehrer. Extrahiere {number_of_words} {language}e Vokabeln oder Redewendungen passend zum Mindest-Sprachniveau {level} aus dem folgenden Text. Erstelle dabei eine gute Mischung aus Verben, komplexe Ausdrücken, Adjektiven und Nomen. Gib die Vokabeln als durch Kommas getrennte Liste zurück."},
            {"role": "user", "content": all_text}
        ]
    )
    extracted_vocabulary = response.choices[0].message.content.strip().split(",")
    extracted_vocabulary = [vocab.strip() for vocab in extracted_vocabulary]
    return extracted_vocabulary


#### Korektur des User Inputs
def correct_text(task, user_text, level):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Korrigiere den folgenden {language}en Text für das Sprachlevel {level}. Beachte dabei die Aufgabenstellung. Erkläre dem Benutzer seine Fehler."},
            {"role": "user", "content": f"Aufgabe: {task}\n\nAntwort des Benutzers: {user_text}"}
        ]
    )
    return response.choices[0].message.content.strip()

#### Kommentare
def answer_comment(comment):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Beantworte die folgende Frage sachlich und präzise."},
            {"role": "user", "content": comment}
        ]
    )
    return response.choices[0].message.content.strip()

def extract_comments(text):
    comments = re.findall(r'<(.*?)>', text)
    cleaned_text = re.sub(r'<.*?>', '', text).strip()
    return cleaned_text, comments

#########################################################################################################################################################################################
#### Methoden zum Stellen der Aufgaben
def create_cloze_text(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 10))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Erstelle einen {language}en Lückentext für das Sprachlevel {level} mit den folgenden Vokabeln: {', '.join(selected_vocab)}. Gib davor zu verwendenden Vokabeln im Anschluss in einer zufälligen Reihenfolge an. {no_answers}"}
        ]
    )
    return selected_vocab, response.choices[0].message.content.strip()

def create_translation_task(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 10))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Erstelle 3 deutsche Sätze für das Sprachlevel {level}, die die folgenden {language}en Vokabeln enthalten und zur Übersetzung ins {language}e geeignet sind. Gebe die {language}en Sätze nicht an: {', '.join(selected_vocab)}.{no_answers}"}
        ]
    )
    return response.choices[0].message.content.strip()

def create_vocabulary_quiz(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 5))
    quiz = {}
    for word in selected_vocab:
        translation = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"Übersetze das Wort '{word}' ins Deutsche. {no_answers}"}
            ]
        ).choices[0].message['content'].strip()
        quiz[word] = translation
    return quiz

def create_sentence_building_task(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 5))
    words = ', '.join(selected_vocab)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Erstelle {language}e Sätze mit den folgenden Wörtern: {words}. {no_answers}"}
        ]
    )
    return words, response.choices[0].message.content.strip()

def create_error_detection_task(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 5))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Erstelle 3 fehlerhafte {language}e Sätze mit den folgenden Vokabeln, die für das Sprachlevel {level} geeignet sind. Gebe die korrekten Sätze nicht an: {', '.join(selected_vocab)}."}
        ]
    )
    return response.choices[0].message.content.strip()

def create_synonym_antonym_task(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 3))
    task = {}
    for word in selected_vocab:
        synonym = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"Gib ein Synonym für das Wort '{word}' an. {no_answers}"}
            ]
        ).choices[0].message['content'].strip()
        antonym = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"Gib ein Antonym für das Wort '{word}' an. {no_answers}"}
            ]
        ).choices[0].message['content'].strip()
        task[word] = {"synonym": synonym, "antonym": antonym}
    return task

def create_conjugation_task(vocab_list):
    verb = random.choice(vocab_list)
    person = ["ich", "du", "er/sie/es", "wir", "ihr", "sie"]
    person = random.choice(person)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Konjugiere für {person} das Verb '{verb}' in den folgenden Zeiten: Präsens, Präteritum, Futur, Perfekt. {no_answers}"}
        ]
    )
    return verb, response.choices[0].message.content.strip()



######################################################## State Handling
def save_task_and_response(task_type, task, user_text):
    st.session_state.task_type = task_type
    st.session_state.current_task = task
    st.session_state.user_text = user_text

def update_task_type():
    st.session_state.task_type_flagg = True

def update_user_text():
    print("Update function called")
    st.session_state.last_text = st.session_state.user_text
    st.session_state.user_text = st.session_state["user_text_area"]
    if st.session_state.last_text != st.session_state.user_text:
        st.session_state.text_input_flagg = True
        
#     st.session_state.text_input_flagg = True
#     print("session state user text:", st.session_state.user_text, "user text:", user_text)


    
##########################################################################################################################################################

# Streamlit App
st.title(f"{language} Lernprogramm")
print(f"\n\{language}-Lernprogramm - Start")

### initial settings

# User inputs for file path and language level
level = st.selectbox("Wählen Sie Ihr Sprachniveau:", ["A1", "A2", "B1", "B2", "C1", "C2"], key="level")
file_path = st.text_input("Geben Sie den Pfad zu einer Datei oder einem Verzeichnis ein:", key="file_path")
uploaded_vocab_file = st.file_uploader("Oder laden Sie Ihre Vokabel-Datei hoch:", type=["txt"])
number_of_words = st.number_input("Anzahl der zu extrahierenden Vokabeln:", min_value=1, max_value=100, value=30, key="number_of_words")

# Initialize session state variables
if 'vocab_list' not in st.session_state: st.session_state.vocab_list = []
if 'task_type' not in st.session_state: 
    st.session_state.task_type = None
    task_type = None
if 'current_task' not in st.session_state:
    st.session_state.current_task = None
    task = None
if 'user_responses' not in st.session_state: st.session_state.user_responses = {}
if 'theme' not in st.session_state: st.session_state.theme = ""
if 'new_task' not in st.session_state: st.session_state.new_task = False
if 'user_text' not in st.session_state: st.session_state.user_text = ""
if 'last_text' not in st.session_state: st.session_state.last_text = ""
if 'number_of_words' not in st.session_state: st.session_state.number_of_words = number_of_words
if 'file_path' not in st.session_state: st.session_state.file_path = file_path
if 'level' not in st.session_state: st.session_state.level = level
if 'task_type_flagg' not in st.session_state: st.session_state.task_type_flagg = False
if 'text_input_flagg' not in st.session_state: st.session_state.text_input_flagg = False
if 'num_runs' not in st.session_state: st.session_state.num_runs = 0

# Load vocabulary list - nur ausgeführt, wenn "Uploaded_vocab_file" oder "File_path" angegeben sind ----> checken
st.session_state.num_runs += 1
print("Number of runs:", st.session_state.num_runs)

if uploaded_vocab_file and st.session_state.vocab_list == []:
    print("Uploaded vocab file:", uploaded_vocab_file.name)
    with open(uploaded_vocab_file.name, "wb") as f:
        f.write(uploaded_vocab_file.getbuffer())
    st.session_state.vocab_list = load_vocabulary(uploaded_vocab_file.name)
elif file_path:
    print("Vocab - File path:", file_path)
    if st.button("Vokabeln extrahieren"):
        st.session_state.vocab_list = extract_french_vocabulary(file_path, level, number_of_words)

if st.session_state.vocab_list:
    st.write("Extrahierte Vokabeln/Redewendungen:")
    st.write(st.session_state.vocab_list)

# Choose task_type
task_type = st.selectbox("Wählen Sie eine Übung:", 
    ["", "Schreiben eines Textes und danach Korrektur", f"Erstellen eines {language}en Lückentextes", 
     "Vorgabe von deutschen Sätzen zum Übersetzen", "Vokabel-Quiz", "Satzbauübung", "Fehler im Text finden und korrigieren", 
     "Synonyme und Antonyme finden", "Verbkonjugation üben"], key="task_type", on_change=update_task_type)

######### checken der Aufgaben ##################################################################################################################

# print("Task type:", task_type, st.session_state.task_type)

if task_type == "Schreiben eines Textes und danach Korrektur":
    # Get new theme - only if new task selected, or manually triggered
    print("Start task - rediger")
    print("New Task type flagg:", st.session_state.task_type_flagg, "new task flagg:", st.session_state.new_task)
    if st.session_state.task_type_flagg or st.session_state.new_task:  
        print("Select topic")
        st.session_state.theme = random.choice(["Urlaub", "Schule", "Essen", "Sport", "Kultur", "Medien", "Raumfahrt", "Business", "Politik"])
        st.session_state.task_type_flagg = False
        st.session_state.new_task = False

        
    ### Aufnahme des Textes
    task = f"Schreibe einen Text über das Thema: {st.session_state.theme}"; st.write(task)
    st.text_area("Dein Text:", value=st.session_state.user_text, key="user_text_area", on_change=update_user_text)
    print("Input texte: session state user text:", st.session_state.user_text, "old text:", st.session_state.last_text)
    
    ### korrigieren des Textes
    if st.session_state.text_input_flagg and st.session_state.user_text:     ### checken, ob user_text geändert wurde, nur dann Korrektur ausgeben
        print("Correction task")
        st.session_state.text_input_flagg = False
        cleaned_text, comments = extract_comments(st.session_state.user_text)
        corrected_text = correct_text(task, cleaned_text, level)
        
        st.write("Korrigierter Text:")
        st.write(corrected_text)
        for comment in comments:
            comment_response = answer_comment(comment)
            st.write(f"Kommentar: {comment}\nAntwort: {comment_response}")
        ## save_task_and_response(task_type, task, st.session_state.user_text) ##notwendig ???

    if st.button("Neue Aufgabe"):
        st.session_state.new_task = True
        st.session_state.theme = ""
        st.session_state.user_text = ""
        print("new task - update:", st.session_state.new_task)        
        st.rerun()

elif task_type == f"Erstellen eines {language}en Lückentextes":
    print("Start task - cloze")
    print(st.session_state.vocab_list)
    print("Task type:", task_type, st.session_state.task_type)
    if st.session_state.vocab_list:
        if st.session_state.task_type_flagg or st.session_state.new_task:  
            selected_vocab, cloze_text = create_cloze_text(st.session_state.vocab_list, level)
            task = f"Fülle die Lücken im folgenden Text mit den Wörtern: {', '.join(selected_vocab)}\n\n{cloze_text}"
            st.session_state.task_type_flagg = False
            st.session_state.new_task = False
            st.session_state.task = task
        st.write(st.session_state.task)
        user_filled_text = st.text_area("Dein Text:", value=st.session_state.user_responses.get(st.session_state.task, ""))
        if st.button("Text korrigieren"):
            st.session_state.task_type_flagg = False
            st.session_state.new_task = False
            cleaned_text, comments = extract_comments(user_filled_text)
            corrected_text = correct_text(st.session_state.task, cleaned_text, level)
            st.write("Korrigierter Text:")
            st.write(corrected_text)
            for comment in comments:
                comment_response = answer_comment(comment)
                st.write(f"Kommentar: {comment}\nAntwort: {comment_response}")
            # save_task_and_response(task_type, task, user_filled_text)
        if st.button("Neue Aufgabe"): 
            st.session_state.new_task = True
            st.session_state.user_filled_text = ""
            st.rerun()
        else: st.session_state.new_task = False
    else:
        st.write("Noch keine Vokabeln ausgewählen. Bitte zuerst Vokabeln auswählen.")


elif task_type == "Vorgabe von deutschen Sätzen zum Übersetzen":
    if st.session_state.vocab_list:
        if task_type != st.session_state.task_type: 
            translation_task = create_translation_task(st.session_state.vocab_list, level)
            task = f"Übersetze die folgenden deutschen Sätze ins {language}e:\n\n{translation_task}"
            st.write(task)
            user_translation = st.text_area("Deine Übersetzung:", value=st.session_state.user_responses.get(task, ""))
        if st.button("Übersetzung korrigieren"):
            cleaned_text, comments = extract_comments(user_translation)
            corrected_translation = correct_text(task, cleaned_text, level)
            st.write("Korrigierte Übersetzung:")
            st.write(corrected_translation)
            for comment in comments:
                comment_response = answer_comment(comment)
                st.write(f"Kommentar: {comment}\nAntwort: {comment_response}")
            save_task_and_response(task_type, task, user_translation)
            if st.button("Neue Aufgabe"): st.session_state.new_task = True
            else: st.session_state.new_task = False


elif task_type == "Vokabel-Quiz":
    if st.session_state.vocab_list:
        quiz = create_vocabulary_quiz(st.session_state.vocab_list, level)
        score = 0
        for word, translation in quiz.items():
            answer = st.text_input(f"Was ist die {language}e Bedeutung von '{translation}'?", key=word)
            if st.button("Antwort überprüfen", key=f"{word}_check"):
                if answer.lower() == word.lower():
                    st.write("Richtig!")
                    score += 1
                else:
                    st.write(f"Falsch. Die richtige Antwort ist '{word}'.")
        st.write(f"Du hast {score} von {len(quiz)} richtig.")

elif task_type == "Satzbauübung":
    if st.session_state.vocab_list:
        if task_type != st.session_state.task_type: 
            words, example_sentence = create_sentence_building_task(st.session_state.vocab_list, level)
            task = f"Baue einen Satz mit den folgenden Wörtern: {words}\nBeispielsatz: {example_sentence}"
            st.write(task)
            user_sentence = st.text_area("Dein Satz:", value=st.session_state.user_responses.get(task, ""))
        if st.button("Satz korrigieren"):
            cleaned_text, comments = extract_comments(user_sentence)
            corrected_sentence = correct_text(task, cleaned_text, level)
            st.write("Korrigierter Satz:")
            st.write(corrected_sentence)
            for comment in comments:
                comment_response = answer_comment(comment)
                st.write(f"Kommentar: {comment}\nAntwort: {comment_response}")
            save_task_and_response(task_type, task, user_sentence)
            if st.button("Neue Aufgabe"): st.session_state.new_task = True
            else: st.session_state.new_task = False


elif task_type == "Fehler im Text finden und korrigieren":
    if st.session_state.vocab_list:
        if task_type != st.session_state.task_type: 
            error_text = create_error_detection_task(st.session_state.vocab_list, level)
            task = f"Finde und korrigiere die Fehler im folgenden Text:\n\n{error_text}"
            st.write(task)
            user_correction = st.text_area("Deine Korrektur:", value=st.session_state.user_responses.get(task, ""))
        if st.button("Text korrigieren"):
            cleaned_text, comments = extract_comments(user_correction)
            corrected_text = correct_text(task, cleaned_text, level)
            st.write("Korrigierter Text:")
            st.write(corrected_text)
            for comment in comments:
                comment_response = answer_comment(comment)
                st.write(f"Kommentar: {comment}\nAntwort: {comment_response}")
            save_task_and_response(task_type, task, user_correction)
            if st.button("Neue Aufgabe"): st.session_state.new_task = True
            else: st.session_state.new_task = False


elif task_type == "Synonyme und Antonyme finden":
    if st.session_state.vocab_list:
        task = create_synonym_antonym_task(st.session_state.vocab_list, level)
        for word, meanings in task.items():
            if task_type != st.session_state.task_type: 
                st.write(f"Finde ein Synonym und ein Antonym für '{word}'")
                st.write(f"Synonym: {meanings['synonym']}, Antonym: {meanings['antonym']}")
                user_synonym = st.text_input("Dein Synonym:", key=f"{word}_synonym", value=st.session_state.user_responses.get(f"{word}_synonym", ""))
                user_antonym = st.text_input("Dein Antonym:", key=f"{word}_antonym", value=st.session_state.user_responses.get(f"{word}_antonym", ""))
            if st.button("Antwort überprüfen", key=f"{word}_check"):
                correct = user_synonym == meanings['synonym'] and user_antonym == meanings['antonym']
                if correct:
                    st.write("Richtig!")
                else:
                    st.write(f"Richtiges Synonym: {meanings['synonym']}, Richtiges Antonym: {meanings['antonym']}")
                st.session_state.user_responses[f"{word}_synonym"] = user_synonym
                st.session_state.user_responses[f"{word}_antonym"] = user_antonym
                if st.button("Neue Aufgabe"): st.session_state.new_task = True
                else: st.session_state.new_task = False


elif task_type == "Verbkonjugation üben":
    if st.session_state.vocab_list:
        if task_type != st.session_state.task_type: 
            verb, conjugations = create_conjugation_task(st.session_state.vocab_list, level)
            task = f"Konjugiere das Verb '{verb}' in den folgenden Zeiten: Präsens, Präteritum, Futur, Perfekt"
            st.write(task)
            st.write(conjugations)
            user_conjugation = st.text_area("Deine Konjugation:", value=st.session_state.user_responses.get(task, ""))
        if st.button("Konjugation überprüfen"):
            cleaned_text, comments = extract_comments(user_conjugation)
            corrected_conjugation = correct_text(task, cleaned_text, level)
            st.write("Korrigierte Konjugation:")
            st.write(corrected_conjugation)
            for comment in comments:
                comment_response = answer_comment(comment)
                st.write(f"Kommentar: {comment}\nAntwort: {comment_response}")
            if st.button("Neue Aufgabe"): st.session_state.new_task = True
            save_task_and_response(task_type, task, user_conjugation)
            if st.button("Neue Aufgabe"): st.session_state.new_task = True
            else: st.session_state.new_task = False
            
print("Programm-Run-Ende")

