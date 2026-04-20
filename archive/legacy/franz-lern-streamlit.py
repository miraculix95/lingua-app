from dotenv import load_dotenv, find_dotenv
import streamlit as st
import os
import openai
import random
import re
import argparse
import json
import requests, pyaudio, io
from pydub import AudioSegment
from pydub.utils import make_chunks
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4


# Falls kein Text eingegeben wurde, sag einfach: Kein Text eingegeben. -- Funktioniert leider nicht.
# Start: streamlit run franz-lern-streamlit.py -- --language=englisch

# Konstanten
no_answers = " Nenne nicht die Antworten. "
models = ["gpt-4o-mini-2024-07-18", "gpt-4o-2024-05-13", "gpt-3.5-turbo-0125"]
levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
niveau_levels = ["Gossensprache/Kriminelle Sprache", "Argot/Vulgär", "Umgangssprache", "Standardsprache", "Gehoben/Vornehm", "Hohe Literatur", "Technisch"]
languages = ["französisch", "englisch", "spanisch", "ukrainisch", "deutsch"]
mentoren = ["Netter Lehrer", "Strenger Lehrer", "Dalai Lama", "Vitalik Buterin", "Elon Musk", "Jesus Christus", 
            "Chairman Mao", "Homer", "Konfuzius", "Machiavelli"]
themen_liste = ["Urlaub", "Schule", "Essen", "Sport", "Kultur", "Medien", "Raumfahrt", "Business", "Politik"]
radio_kanale = {
    "France Info" : "http://icecast.radiofrance.fr/franceinfo-midfi.mp3",
    "France Inter" : "http://icecast.radiofrance.fr/franceinter-midfi.mp3",
    "France Culture" : "http://icecast.radiofrance.fr/franceculture-midfi.mp3",
    "BFM Radio" : "https://audio.bfmtv.com/bfmradio_128.mp3"
}

task_list = ["", 
     "Schreiben eines Textes und danach Korrektur", 
     "Ausfüllen eines Lückentextes in Fremdsprache", 
     "Vorgabe von deutschen Sätzen zum Übersetzen", 
     "Vokabel-Quiz  - noch nicht implementiert", 
     "Satzbauübung", 
     "Fehler im Text finden und korrigieren", 
     "Synonyme und Antonyme finden", 
     "Verbkonjugation üben",
     "Radio hören und aufnehmen"
     ]

function_spec = {
    "name": "generate_vocabulary_list",
    "description": "Generiert eine Liste französischer Vokabeln mit Verben.",
    "parameters": {
        "type": "object",
        "properties": {
            "vocabulary": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Eine Liste von Vokabeln."
            }
        },
        "required": ["vocabulary"]
    }
}

##################################################

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
if 'number_of_words' not in st.session_state: st.session_state.number_of_words = 40
if 'level' not in st.session_state: st.session_state.level = levels[2]
if 'niveau' not in st.session_state: st.session_state.niveau = niveau_levels[3]
if 'task_type_flagg' not in st.session_state: st.session_state.task_type_flagg = False
if 'text_input_flagg' not in st.session_state: st.session_state.text_input_flagg = False
if 'num_runs' not in st.session_state: st.session_state.num_runs = 0
if 'file_path_extract' not in st.session_state: st.session_state.file_path_extract = None
if 'uploaded_vocab_file' not in st.session_state: st.session_state.uploaded_vocab_file = None
if 'task' not in st.session_state: st.session_state.task = ""
if 'auto_gen_vocabs' not in st.session_state: st.session_state.auto_gen_vocabs = False
if 'html_path_extract' not in st.session_state: st.session_state.html_path_extract = ""
if 'stop' not in st.session_state: st.session_state.stop = True

##########################################################################################################################################################
### Protokollieren der Session-States

st.session_state.num_runs += 1
print("\n\n\nNumber of runs:", st.session_state.num_runs)
print("Session-States Start of Run:", st.session_state)            


#########################################################################################################################################################################################
#########################################################################################################################################################################################


######################################################## State Handling - Functions
def update_task_type(): #new task type
    st.session_state.task_type_flagg = True
    
def update_language_type(): #new task type
    st.session_state.task_type_flagg = True
    if st.session_state.auto_gen_vocabs == True:
        st.session_state.vocab_list = [] 

def update_new_task(): #means rerun and new exercice needs to be created, but tasks stays the same
    if st.button("Neue Aufgabe"): 
        st.session_state.new_task = True
        st.rerun()
    else: st.session_state.new_task = False

def save_task(task): ##means exercice has been prepared, now waiting for correction, no new exercice needs to be created
    st.session_state.task = task
    st.session_state.task_type_flagg = False
    st.session_state.new_task = False

def update_user_text():
    print("Update function called")
    st.session_state.last_text = st.session_state.user_text
    st.session_state.user_text = st.session_state["user_text_area"]
    if st.session_state.last_text != st.session_state.user_text:
        st.session_state.text_input_flagg = True
        
def update_radio():
    st.session_state.stop = False


#### Funktionen: Laden der Vokabeln

def load_vocabulary(file_path_extract):
    with open(file_path_extract, 'r', encoding='utf-8') as file:
        vocab_list = [line.strip() for line in file]
    return vocab_list

def extract_vocabulary(file_list, level, number_of_words):
    txt_files = [file.name for file in file_list if file.name.endswith('.txt')]
    print("Txt-Files: ",txt_files)
    all_text = ""
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            all_text += f.read() + "\n"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"""Du bist ein Sprachlehrer. Extrahiere genau {number_of_words} {language}e Vokabeln oder Redewendungen 
             passend zum Mindest-Sprachniveau {level} aus dem folgenden Text. Erstelle dabei eine gute Mischung aus Verben, komplexe Ausdrücken, 
             Adjektiven und Nomen. Vermeide Eigennamen und geographische Namen. Gib die Vokabeln als durch Kommas getrennte Liste ohne Nummerierung zurück. Gib das Ergebnis ohne Einleitung und Kommentar an."""},
            {"role": "user", "content": all_text}
        ]
    )
    extracted_vocabulary = response.choices[0].message.content.strip().split(",")
    extracted_vocabulary = [vocab.strip() for vocab in extracted_vocabulary]
    return extracted_vocabulary


def web_extract_vocabulary(url):
    from newspaper import Article

    # Lade und parse den Artikel
    article = Article(url)
    article.download()
    article.parse()

    # Extrahiere den Titel und den Haupttext
    title = article.title
    summary = article.summary
    text = article.text

    # Speichere in einer Datei
    with open("news_article.txt", "w", encoding="utf-8") as f:
        f.write(f"{title}\n\n{summary}\n\n{text}")

        

def generate_vocabulary_list(level, niveau):
    response = client.chat.completions.create(
        # model=model,
            model="gpt-4-0613",  # Ein Model, das functions unterstützt
        messages=[
            { "role": "system", "content": f"Du bist ein Sprachlehrer."},
            {
                "role": "user",
                "content": f"""
                Erstelle in Python Format eine Liste von 20 {language}n Vokableln inklusive Verben. Die Sprache ist {language}. 
                Die Wörter sollen passend zum Mindest-Sprachniveau {level} sein, das folgende Sprachregister treffen {niveau}. 
                Wähle thematisch zueinander passende Wörter aus. 
                ."""
            }
        ],
        functions = [function_spec],
        function_call={"name": "generate_vocabulary_list"}  # Fordere eine JSON-Antwort an
    )
    json_response = response.choices[0].message.function_call.arguments
    print("!!!!!!!!!! Neue Vokabeln generiert !!!!!!!!!!!!!")
    print(json_response)
    # vocab_list = response.choices[0].message.content.strip()
    # vocab_list = json.loads(vocab_list)
    vocab_list = json.loads(json_response)["vocabulary"]
    st.session_state.vocab_list = vocab_list
    
    ### Output in Sidebar 
    st.session_state.auto_gen_vocabs = True
    print("Autogen Vokabelliste:", st.session_state.vocab_list)
    st.sidebar.write("Extrahierte Vokabeln/Redewendungen (Autogen):")
    st.sidebar.write(st.session_state.vocab_list)

    return vocab_list

#########################################################################################################################################################################################

#### Methoden zum Stellen der Aufgaben - eine Funktion je Aufgabe
def create_cloze_text(vocab_list, level, niveau, number_trous):
    if not vocab_input: 
        vocab_list = generate_vocabulary_list(level, niveau)
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), number_trous))
    intro = "Fülle die Lücken im folgenden Text mit den Wörtern: " + ", ".join(selected_vocab) 
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"""Du bist ein Sprachlehrer. Deine Aufgabe ist es, dem Benutzer bei der Erstellung von Lückentexten in der Sprache {language} zu helfen. Der Text soll Vokabeln enthalten, die im angegebenen Kontext verwendet werden, wobei jedes Wort genau einmal vorkommt. 
                Die Lücken sollen so gesetzt werden, dass der Benutzer sie mit den entsprechenden Vokabeln ausfüllen muss. Die Vokabeln können in ihrer Grundform oder in abgewandelter Form (z. B. Plural, Konjugation) vorkommen. 
                Der Text soll dem Sprachlevel des Benutzers entsprechen, das im User-Prompt angegeben ist. Der Text muss ohne die Lösungen (Lücke-Verb-Zuordnung) ausgegeben werden, und ein passender Titel soll hinzugefügt werden. Der Text soll logisch Sinn machen.
                """
            },
            {
                "role": "user",
                "content": f"""Erstelle bitte einen Lückentext der {language}en Sprache mit den folgenden Vokabeln: {', '.join(selected_vocab)}. Der Text muß auf dem Sprachlevel {level} sein, das folgende Sprachregister treffen {niveau} und genau {number_trous} Lücken enthalten. 
                Vor dem eigentlichen Lückentext müssen die Bedeutungen der Vokabeln zwingend jeweils ganz kurz erklärt werden.
                Jede Lücke soll eine der Vokabeln ersetzen. Gib den Lückentext ohne Lösungen aus und füge einen passenden Titel hinzu."""
            }
            # {"role": "system", "content": f"""Erkläre dem Nutzer kurz die Bedeutungen der folgenden Vokabeln: {', '.join(selected_vocab)}. 
            #  Danach, erstelle einen {language}en Text für das Sprachlevel {level} der die folgenden Vokabeln verstreut im Text enthält: 
            #  {', '.join(selected_vocab)}, entweder in der exacten Form oder abgewandelter Form (Mehrzahl, Konjugation). 
            #  Jede Vokabel soll genau einmal vorkommen. Ersetze dann alle diese Wörter im Text mit Lücken 
            #  so dass ein Lückentext mit {number_trous} Lücken entsteht. Füge einen passenden Titel hinzu. 
            #  Gebe das Ergebnis, dass heißt die Zuordnung: Lücke-Verb nicht an !!  {no_answers}"""}
        ]
    )
    return selected_vocab, response.choices[0].message.content.strip()

def create_translation_task(vocab_list, level, niveau, number_sentences):
    if not vocab_input:
        vocab_list = generate_vocabulary_list(level, niveau)
        print("Neue Vokabelliste wird erstellt")
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 3))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"""Übersetze die folgenden {language}en Vokabeln ins Deutsche. {', '.join(selected_vocab)}. 
             Erstelle dann {number_sentences} deutsche Sätze zum Übersetzen ins {language}e für das Sprachregister {niveau}, und das Sprachlevel {level}. 
             Gebe die Lösung (die {language}en Sätze) nicht an.{no_answers}
             Ausgabeformat: 
             
             Übersetze die Sätze / den Satz: Sätze durchnummeriert
             ---
             Benutze die folgenden Vokabeln (franzöisch - deutsch): Vokabeln mit Bulletpoints 
             
             """}
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
        ).choices[0].message.content.strip()
        quiz[word] = translation
    return quiz

def create_sentence_building_task(vocab_list, level):
    if not vocab_input: 
        vocab_list = generate_vocabulary_list(level, niveau)
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 2))
    words = ', '.join(selected_vocab)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Erstelle einen {language}e Satz mit den folgenden Wörtern : {words}."
             f"Benutze dabei das folgende Sprachregister: {niveau} und das folgende Sprachlevel: {level}. {no_answers}"}
        ]
    )
    return words, response.choices[0].message.content.strip()

def create_error_detection_task(vocab_list, level, niveau):
    if not vocab_input: 
        vocab_list = generate_vocabulary_list(level, niveau)
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 5))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Erstelle 3 grammatikalisch und orthografisch stark fehlerhafte {language}e Sätze mit dem folgenden Sprachregister: {niveau} mit den folgenden Vokabeln, die für einen Lernenden des Sprachlevels {level} von der Komplexität her verständlich sind. Gebe die korrekten Sätze nicht an: {', '.join(selected_vocab)}."}
        ]
    )
    return response.choices[0].message.content.strip()

def create_synonym_antonym_task(vocab_list, level):
    if not vocab_input: 
        vocab_list = generate_vocabulary_list(level, niveau)    
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 1))
    return selected_vocab

def create_conjugation_task(vocab_list, level, niveau):
    if not vocab_input: 
        vocab_list = generate_vocabulary_list(level, niveau)    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"gib einwortige Antworten wann immer möglich, ohne Nummerierung, ohne Punkt"},
            {"role": "user", "content": f"""Wähle passend zum Sprachlevel {level} entweder a) zufällig ein Verb aus der angehängten Vokabelliste aus:
             {', '.join(vocab_list)}. oder b) ein beliebiges unregelmäßiges Verb. Es muss ein Verb, also ein Tunwort sein."""}
        ]
    )
    return response.choices[0].message.content.strip()

#########################################################################################################################################################################################

#### Beantworten der Kommentare und user inputs
def extract_comments(text):
    comments = re.findall(r'<(.*?)>', text)
    cleaned_text = re.sub(r'<.*?>', '', text).strip()
    return cleaned_text, comments

def answer_comments(comments):
    for comment in comments:
        comment_response = answer_comment(comment)
        st.markdown(f"Kommentar: {comment}  \nAntwort: {comment_response}")

def answer_comment(comment):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Beantworte die folgende Frage sachlich und präzise."},
            {"role": "user", "content": comment}
        ]
    )
    return response.choices[0].message.content.strip()

#### Beantworten der User Inputs
def correct_text(task, user_text, level, niveau):
    print("Task:", task)    
    print("User Text:", user_text)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"""Korrigiere den folgenden {language}en Text. Beachte dabei die Aufgabenstellung.  
             Beachte das der Nutzer das folgende Sprachregister: {niveau} benutzt. 
             Erkläre dem Benutzer seine Fehler und gib Feedback im Stile von {mentor}. Nicht pingelig wegen des Ausdrucks sein. 
             Halte dich kurz."""},
            {"role": "user", "content": f"Aufgabe: {task}\n\nAntwort des Benutzers: {user_text}"}
        ]
    )
    return response.choices[0].message.content.strip()


#########################################################################################################################################################################################

###################################### Main Streamlit App ##############################################################

### Opening AI and parameters
load_dotenv(find_dotenv())
client = openai.OpenAI()
             
parser = argparse.ArgumentParser(description="Streamlit app with argparse")
parser.add_argument("--model", type=str, default="gpt-4o-mini-2024-07-18", help="Model used")
parser.add_argument("--language", type=str, default="französisch", help="Lernsprache")

model = parser.parse_args().model if parser.parse_args().model in models else models[0]
language = parser.parse_args().language if parser.parse_args().language in languages else languages[0]

### Stramlit App
st.title(f"{language.capitalize()} - Lernprogramm")
st.write("Outgame-Kommentare bitte in <> packen")
print(f"\n{language.upper()}-Lernprogramm - Start")
# os.chdir(r'C:\Users\Brand\Videos')
# print("CWD:", os.getcwd())

### Sidebar und Sidebar Funktionen   
st.sidebar.title("Einstellungen")
mentor = st.sidebar.selectbox("Wählen Sie Ihren Coach:", mentoren, index=0, key="mentor", on_change=update_task_type)
level = st.sidebar.selectbox("Wählen Sie Ihr Sprachniveau:", levels, key="level", on_change=update_language_type)
niveau = st.sidebar.selectbox("Wahlen Sie Ihr Sprachregister:", niveau_levels, key="niveau", on_change=update_language_type)
st.sidebar.divider()
st.sidebar.markdown("## Vokabelliste")
st.sidebar.write("Bei Bedarf erstellt die Software automatisch ein Vokabelliste")
file_path_extract = st.sidebar.file_uploader("Extrahieren Sie Vokabeln aus ein oder mehreren Txt-Dateien (max. 60kb):", accept_multiple_files=True, type=["txt"])
number_of_words = st.sidebar.number_input("Anzahl der zu extrahierenden Vokabeln:", min_value=1, max_value=200, key="number_of_words")
html_path_extract = st.sidebar.text_input("Extrahieren Sie Vokabeln von einer Webseite:")
uploaded_vocab_file = st.sidebar.file_uploader("Alternativ, laden Sie Ihre Vokabel-Datei [.txt] hoch:", type=["txt"])


# Debug
print("Extract - File path:", file_path_extract)
print("Extract - File path (Old):", st.session_state.file_path_extract)
print("Vocab - File path:", uploaded_vocab_file)
print("Vocab - File path (Old):", st.session_state.uploaded_vocab_file)

# Extrahieren von Vokabeln aus einem TXT-Artikel
if file_path_extract and file_path_extract != st.session_state.file_path_extract:  #update Fachtext vocab input -> action
    print("Vocab - File path:", file_path_extract)
    #if st.button("Vokabeln extrahieren"):
    st.session_state.vocab_list = extract_vocabulary(file_path_extract, level, number_of_words) ### Kernzeile
    st.sidebar.write("Extrahierte Vokabeln/Redewendungen (Quelltext):")
    st.sidebar.write(sorted(st.session_state.vocab_list))

### Extrahieren von Vokabeln aus einer Webseite
elif html_path_extract and html_path_extract != st.session_state.html_path_extract: #update Fachtext vocab input -> action
    st.write("Extrahieren von Vokabeln aus", html_path_extract)
    web_extract_vocabulary(html_path_extract)
    filepath = os.path.join(os.getcwd(), "news_article.txt")
    file_object = open(filepath, 'r', encoding='utf-8')
    st.session_state.vocab_list = extract_vocabulary([file_object], level, number_of_words) ### Kernzeile
    st.sidebar.write("Extrahierte Vokabeln/Redewendungen (Webseite):")
    st.sidebar.write(sorted(st.session_state.vocab_list))  
  
### Extrahieren von Vokabeln aus einer TXT-Vokabeldatei  
elif uploaded_vocab_file and uploaded_vocab_file != st.session_state.uploaded_vocab_file: #update Vokabelliste vocab input -> action
    print("Uploaded vocab file:", uploaded_vocab_file.name)
    st.session_state.vocab_list = load_vocabulary(uploaded_vocab_file.name) ### Kernzeile
    st.sidebar.write("Extrahierte Vokabeln/Redewendungen (Vokabelliste):")
    st.sidebar.write(sorted(st.session_state.vocab_list))

### automatische Vokabelliste
elif st.session_state.auto_gen_vocabs: #update Vokabelliste vocab input -> action
    print("Autogen Vokabelliste:", st.session_state.vocab_list)
    st.sidebar.write("Extrahierte Vokabeln/Redewendungen (Autogen):")
    st.sidebar.write(sorted(st.session_state.vocab_list))

else: 
    st.sidebar.write("Kein Vokabellisten-Update")

st.session_state.file_path_extract = file_path_extract
st.session_state.uploaded_vocab_file = uploaded_vocab_file

############################################################################################################################################
#### Handling Hauptfenster

# Choose task_type
task_type = st.selectbox("Wählen Sie eine Übung:", 
    task_list, key="task_type", on_change=update_task_type)


######### Stellen und Handling der Aufgaben ##################################################################################################################
need_to_create_new_task = st.session_state.task_type_flagg or st.session_state.new_task or (st.session_state.level != level)
vocab_input = (file_path_extract or uploaded_vocab_file or (st.session_state.vocab_list and st.session_state.level == level)) 
print("Vocab input:", vocab_input)
print("level:", level)
print("st.session_state.level:", st.session_state.level)
print("need_to_create_new_task:", need_to_create_new_task)
print("st.session_state.task_type_flagg:", st.session_state.task_type_flagg)
print("st.session_state.new_task:", st.session_state.new_task)
print("file_path_extract:", file_path_extract)
print("uploaded_vocab_file:", uploaded_vocab_file)



if task_type == "Schreiben eines Textes und danach Korrektur" and need_to_create_new_task:
    while True:
        theme = random.choice(themen_liste)
        if theme != st.session_state.theme: break
    task = f"Schreibe einen Text über das Thema: {theme}"; 
    st.session_state.theme = theme
    save_task(task)

elif task_type == f"Ausfüllen eines Lückentextes in Fremdsprache" and need_to_create_new_task:
    number_trous = st.number_input("Anzahl der Wortlücken:", min_value=3, max_value=20, value=4, key="number_of_trous", on_change=update_task_type)
    selected_vocab, cloze_text = create_cloze_text(st.session_state.vocab_list, level, niveau, number_trous)
    task = f"Fülle die Lücken im folgenden Text mit den Wörtern: {', '.join(selected_vocab)}\n\n{cloze_text}"
    save_task(task)

elif task_type == "Vorgabe von deutschen Sätzen zum Übersetzen" and need_to_create_new_task:
    number_sentences = st.number_input("Anzahl der Sätze:", min_value=1, max_value=20, value=1, key="number_sentences", on_change=update_task_type)
    translation_task = create_translation_task(st.session_state.vocab_list, level, niveau, number_sentences)
    task = translation_task
    # task = f"Übersetze die folgenden deutschen Sätze ins {language.capitalize()}e:\n\n{translation_task} und nutze die genannten Vokabeln."
    st.session_state.user_translation = ""
    save_task(task)

elif task_type == "Satzbauübung" and need_to_create_new_task:  
    words, example_sentence = create_sentence_building_task(st.session_state.vocab_list, level)
    task = f"Baue einen Satz mit den folgenden Wörtern: \n {words} \n"
    save_task(task)

elif task_type == "Fehler im Text finden und korrigieren" and need_to_create_new_task:
    error_text = create_error_detection_task(st.session_state.vocab_list, level, niveau)
    task = f"Finde und korrigiere die Fehler im folgenden Text:\n\n{error_text}"
    save_task(task)

elif task_type == "Synonyme und Antonyme finden" and need_to_create_new_task:  
    selected_vocab = create_synonym_antonym_task(st.session_state.vocab_list, level)
    task = f"Finde die Synonyme und Antonyme von : {selected_vocab[0]}"
    save_task(task)
        
elif task_type == "Verbkonjugation üben" and need_to_create_new_task:
    verb = create_conjugation_task(st.session_state.vocab_list, level, niveau).lower()
    print ("Verb:", verb)
    print ("Vokabels:", st.session_state.vocab_list)
    person = ["ich", "du", "er/sie/es", "wir", "ihr", "sie"]; person = random.choice(person)
    task = f"""Konjugiere das Verb '{verb}' für die Person '{person}' in den folgenden Zeiten: 
    Präsens, Imparfait, Futur, Perfekt, Subjonctive présent, Futur proche und Praesens proche."""
    save_task(task)    
      
elif task_type == "Radio hören und dann antworten" and need_to_create_new_task:  
    def stop_stream():
        st.session_state.stop = True
        stream.stop_stream()
        stream.close()
        p.terminate()

    ### Radio Inputs
    codec = "mp3"
    radio_kanal = st.selectbox("Wählen Sie Ihren Radiokanal:", list(radio_kanale.keys()), index=0, key="radio", on_change=update_radio)
    print("Started streamhandler")
    st.button("Stop", on_click=stop_stream)
    p = pyaudio.PyAudio()
    audio_buffer = io.BytesIO()
    
    ### Connect to the radio stream
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(radio_kanale[radio_kanal], stream=True, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
    except Exception as e:
        print(f"An error occurred: {e}")
    
    ### Find the sample rate
    initial_data = response.raw.read(1024 * 10)
    if codec == 'mp3': sample_rate = MP3(io.BytesIO(initial_data)).info.sample_rate
    if codec == 'aacp': sample_rate = MP4(io.BytesIO(initial_data)).info.sample_rate
    print(f'Sample rate: {sample_rate}')
    audio_buffer.write(initial_data)
    ### output device
    stream = p.open(format=pyaudio.paInt16,  # Assuming 16-bit audio format
                    channels=2,  # Assuming stereo audio
                    rate=sample_rate,  # Common sample rate for audio
                    output=True)
    
    ### Play radio
    while st.session_state.stop is False:
        data = response.raw.read(1024)
        audio_buffer.write(data)
        if audio_buffer.tell() > 1024 * 10:  # Process in chunks of 10 KB
            audio_buffer.seek(0)
            audio_data = AudioSegment.from_file(audio_buffer, format="mp3")
            audio_chunks = make_chunks(audio_data, 1024)
            for chunk in audio_chunks:
                    stream.write(chunk._data)
            audio_buffer.seek(0)
            audio_buffer.truncate(0)

    ### Transkription
    st.write("Datei gespreichert")
    st.write("Audiofile transkribiert")
    with open("radio_text.txt", 'r', encoding='utf-8') as file:
        radio_text = file.read()
    st.write("Transkription:")
    st.markdown(f'<div style="height: 300px; overflow: auto;">{radio_text}</div>', unsafe_allow_html=True)
 

#### to be done ###
elif task_type == "Vokabel-Quiz":
    if st.session_state.vocab_list:
        answer = [], word = []
        quiz = create_vocabulary_quiz(st.session_state.vocab_list, level)
        num = len(quiz)
        score = 0
        for index, word, translation in enumerate(quiz.items()):
            answer[index] = st.text_input(f"Was ist das {language}e Wort für '{translation}'?")
        
        if st.button("Antwort überprüfen", key=f"{word}_check"):
            for index in range(num):
                if answer[word].lower() == quiz[index]["word"].lower():
                    st.write("Richtig!")
                    score += 1
                else:
                    st.write(f"Falsch. Die richtige Antwort ist '{word}'.")
        st.write(f"Du hast {score} von {len(quiz)} richtig.")
    else: st.write("Noch keine Vokabeln ausgewählt. Bitte zuerst Vokabeln auswählen.")


#######################################################################################
### Input entgegennehmen und Korrigieren des Textes
if task_type != "Radio hören und aufnehmen":
    st.write(st.session_state.task)
    st.text_area("Dein Text:", value=st.session_state.user_text, key="user_text_area", on_change=update_user_text)


    if st.button("Text korrigieren"):     ### checken, ob user_text geändert wurde, nur dann Korrektur ausgeben
        st.session_state.text_input_flagg = False
        cleaned_text, comments = extract_comments(st.session_state.user_text)
        corrected_text =    correct_text(st.session_state.task, cleaned_text, level, niveau)
        print("Cleaned Text:", cleaned_text)
        print("Comments:", comments)
        st.write("Korrigierter Text:")
        st.write(corrected_text)
        answer_comments(comments)

    ### Neue Aufgabe
    update_new_task()

print("Session-States End of Run:", st.session_state)            
print("Programm-Run-Ende")

