from openai import OpenAI
import random
import argparse
import re
import os
from dotenv import load_dotenv, find_dotenv
from prompt_toolkit import prompt ### für Multi-line Input

# OpenAI API-Schlüssel
# client.api_key = 'YOUR_OPENAI_API_KEY'
load_dotenv(find_dotenv())
client = OpenAI()

def load_vocabulary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        vocab_list = [line.strip() for line in file]
    return vocab_list


def extract_french_vocabulary(file, level, number_of_words):
    # Check if the input is a file or a directory
    if os.path.isdir(file):
        txt_files = [os.path.join(file, f) for f in os.listdir(file) if f.endswith('.txt')]
    elif os.path.isfile(file) and file.endswith('.txt'):
        txt_files = [file]
    else:
        raise ValueError("Der Pfad muss entweder eine .txt-Datei oder ein Verzeichnis mit .txt-Dateien sein.")

    # Read all text from the txt files
    all_text = ""
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            all_text += f.read() + "\n"

    # Prompt to OpenAI to extract 100 vocabulary words/expressions
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "system", "content": f"Du bist ein Sprachlehrer. Extrahiere {number_of_words} französische Vokabeln oder Redewendungen passend zum Sprachniveau {level} aus dem folgenden Text. Erstelle dabei eine gute Mischung aus Verben, komplexe Ausdrücken, Adjektiven und Nomen. Gib die Vokabeln als durch Kommas getrennte Liste zurück."},
            {"role": "user", "content": all_text}
        ]
    )
    # Extract and clean the response
    extracted_vocabulary = response.choices[0].message.content.strip().split(",")
    # Trim any leading/trailing whitespace from each vocabulary word/expression
    extracted_vocabulary = [vocab.strip() for vocab in extracted_vocabulary]
    # Return the list of extracted vocabulary
    return extracted_vocabulary

def correct_text(task, user_text, level):
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "system", "content": f"Korrigiere den folgenden französischen Text für das Sprachlevel {level}. Beachte dabei die Aufgabenstellung. Erkläre dem Benutzer seine Fehler."},
            {"role": "user", "content": f"Aufgabe: {task}\n\nAntwort des Benutzers: {user_text}"}
        ]
    )
    return response.choices[0].message.content.strip()

def answer_comment(comment):
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
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

def create_cloze_text(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 3))
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "system", "content": f"""Erstelle einen französischen Lückentext für das Sprachlevel {level} mit den folgenden 
             Vokabeln: {', '.join(selected_vocab)}. Gib davor zu verwendenden Vokabeln im Anschluss in einer zufälligen Reihenfolge an."""}
        ]
    )
    return selected_vocab, response.choices[0].message.content.strip()

def create_translation_task(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 10))
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "system", "content": f"""Erstelle deutsche Sätze für das Sprachlevel {level}, die die folgenden französischen Vokabeln 
             enthalten und zur Übersetzung ins Französische geeignet sind. Gebe die französischen Sätze nicht an: {', '.join(selected_vocab)}."""}
        ]
    )
    return response.choices[0].message.content.strip()

def create_vocabulary_quiz(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 5))
    quiz = {}
    for word in selected_vocab:
        translation = client.chat.completions.create(
            model="gpt-4o-2024-05-13",
            messages=[
                {"role": "system", "content": f"Übersetze das Wort '{word}' ins Deutsche."}
            ]
        ).choices[0].message.content.strip()
        quiz[word] = translation
    return quiz

def create_sentence_building_task(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 5))
    words = ', '.join(selected_vocab)
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "system", "content": f"Erstelle französische Sätze mit den folgenden Wörtern: {words}."}
        ]
    )
    return words, response.choices[0].message.content.strip()

def create_error_detection_task(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 5))
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "system", "content": f"""Erstelle fehlerhafte französische Sätze mit den folgenden Vokabeln, 
             die für das Sprachlevel {level} geeignet sind. Gebe die korrekten Sätze nicht an: {', '.join(selected_vocab)}."""}
        ]
    )
    return response.choices[0].message.content.strip()

def create_synonym_antonym_task(vocab_list, level):
    selected_vocab = random.sample(vocab_list, min(len(vocab_list), 5))
    task = {}
    for word in selected_vocab:
        synonym = client.chat.completions.create(
            model="gpt-4o-2024-05-13",
            messages=[
                {"role": "system", "content": f"Gib ein Synonym für das Wort '{word}' an."}
            ]
        ).choices[0].message.content.strip()
        antonym = client.chat.completions.create(
            model="gpt-4o-2024-05-13",
            messages=[
                {"role": "system", "content": f"Gib ein Antonym für das Wort '{word}' an."}
            ]
        ).choices[0].message.content.strip()
        task[word] = {"synonym": synonym, "antonym": antonym}
    return task

def create_conjugation_task(vocab_list, level):
    verb = random.choice(vocab_list)
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "system", "content": f"Konjugiere das Verb '{verb}' in den folgenden Zeiten: Präsens, Präteritum, Futur, Perfekt."}
        ]
    )
    return verb, response.choices[0].message.content.strip()

def main():
    parser = argparse.ArgumentParser(description="Französisch-Lernprogramm")
    parser.add_argument('--level', type=str, required=True, help="Sprachlevel des Benutzers (z.B. A1, A2, B1, B2, C1, C2)")
    parser.add_argument('--dictionary', type=str, required=False, default="vokabeln.txt", help="Vokabeln-Datei (z.B. vokabeln.txt)")
    parser.add_argument('--input_text', type=str, required=False, default="", help="Texte mit interessanten Wörtern")
    
    args = parser.parse_args()
    level = args.level
    dictionary = args.dictionary#
    input_text = args.input_text
    
    
    if input_text:
        vocab_list = extract_french_vocabulary(input_text, level, 30)
        with open(dictionary, 'w', encoding='utf-8') as file:
            for word in vocab_list:
                file.write(word + '\n')
    else: vocab_list = load_vocabulary(dictionary)

    print("\n\nFranzösisch-Lernprogramm")
    print("\nWörterbuch:", vocab_list)
    
    while True:
        print("\n\n\n")
        print("Wähle eine Option:")
        print("a) Schreiben eines Textes und danach Korrektur")
        print("b) Erstellen eines französischen Lückentextes")
        print("c) Vorgabe von deutschen Sätzen zum Übersetzen")
        print("d) Vokabel-Quiz")
        print("e) Satzbauübung")
        print("f) Fehler im Text finden und korrigieren")
        print("g) Synonyme und Antonyme finden")
        print("h) Verbkonjugation üben")
        print("<exit> zum Beenden")
        print("\n")
        choice = input("Deine Wahl: ").strip().lower()

        if choice == "<exit>":
            break

        if choice == "a":
            theme = random.choice(["Urlaub", "Schule", "Essen", "Sport", "Kultur"])
            task = f"Schreibe einen Text über das Thema: {theme}"
            print(task)
            while True:
                user_text = input("\nDein Text: ").strip()
                cleaned_text, comments = extract_comments(user_text)
                print("Korrigierter Text:", cleaned_text)
                print("Kommentare:", comments)
                corrected_text = correct_text(task, cleaned_text, level)
                print("Korrigierter Text:", corrected_text)
                for comment in comments:
                    comment_response = answer_comment(comment)
                    print(f"Kommentar: {comment}\nAntwort: {comment_response}")
                satisfied = input("\nBist du mit deiner Antwort zufrieden? (ja/nein): ").strip().lower()
                if satisfied == "ja":
                    break

        elif choice == "b":
            selected_vocab, cloze_text = create_cloze_text(vocab_list, level)
            task = f"Fülle die Lücken im folgenden Text mit den Wörtern: {', '.join(selected_vocab)}\n\n{cloze_text}"
            print(task)
            while True:
                user_filled_text = input("\nDein Text: ").strip()
                cleaned_text, comments = extract_comments(user_filled_text)
                corrected_text = correct_text(task, cleaned_text, level)
                print("Korrigierter Text:", corrected_text)
                for comment in comments:
                    comment_response = answer_comment(comment)
                    print(f"Kommentar: {comment}\nAntwort: {comment_response}")
                satisfied = input("\nBist du mit deiner Antwort zufrieden? (ja/nein): ").strip().lower()
                if satisfied == "ja":
                    break

        elif choice == "c":
            translation_task = create_translation_task(vocab_list, level)
            task = f"Übersetze die folgenden deutschen Sätze ins Französische:\n\n{translation_task}"
            print(task)
            while True:
                user_translation = input("\nDeine Übersetzung: ").strip()
                cleaned_text, comments = extract_comments(user_translation)
                corrected_translation = correct_text(task, cleaned_text, level)
                print("Korrigierte Übersetzung:", corrected_translation)
                for comment in comments:
                    comment_response = answer_comment(comment)
                    print(f"Kommentar: {comment}\nAntwort: {comment_response}")
                satisfied = input("\nBist du mit deiner Antwort zufrieden? (ja/nein): ").strip().lower()
                if satisfied == "ja":
                    break

        elif choice == "d":
            quiz = create_vocabulary_quiz(vocab_list, level)
            score = 0
            for word, translation in quiz.items():
                task = f"Was ist die französische Bedeutung von '{translation}'?"
                answer = input(task).strip().lower()
                if answer == word.lower():
                    print("Richtig!")
                    score += 1
                else:
                    print(f"Falsch. Die richtige Antwort ist '{word}'.")
            print(f"Du hast {score} von {len(quiz)} richtig.")

        elif choice == "e":
            words, example_sentence = create_sentence_building_task(vocab_list, level)
            task = f"Baue einen Satz mit den folgenden Wörtern: {words}\nBeispielsatz: {example_sentence}"
            print(task)
            while True:
                user_sentence = input("\nDein Satz: ").strip()
                cleaned_text, comments = extract_comments(user_sentence)
                corrected_sentence = correct_text(task, cleaned_text, level)
                print("Korrigierter Satz:", corrected_sentence)
                for comment in comments:
                    comment_response = answer_comment(comment)
                    print(f"Kommentar: {comment}\nAntwort: {comment_response}")
                satisfied = input("\nBist du mit deiner Antwort zufrieden? (ja/nein): ").strip().lower()
                if satisfied == "ja":
                    break

        elif choice == "f":
            error_text = create_error_detection_task(vocab_list, level)
            task = f"Finde und korrigiere die Fehler im folgenden Text:\n\n{error_text}"
            print(task)
            while True:
                user_correction = input("\nDeine Korrektur: ").strip()
                cleaned_text, comments = extract_comments(user_correction)
                corrected_text = correct_text(task, cleaned_text, level)
                print("Korrigierter Text:", corrected_text)
                for comment in comments:
                    comment_response = answer_comment(comment)
                    print(f"Kommentar: {comment}\nAntwort: {comment_response}")
                satisfied = input("\nBist du mit deiner Antwort zufrieden? (ja/nein): ").strip().lower()
                if satisfied == "ja":
                    break

        elif choice == "g":
            task = create_synonym_antonym_task(vocab_list, level)
            for word, meanings in task.items():
                print(f"Finde ein Synonym und ein Antonym für '{word}'")
                print(f"Synonym: {meanings['synonym']}, Antonym: {meanings['antonym']}")
                while True:
                    user_synonym = input("\nDein Synonym: ").strip()
                    user_antonym = input("\nDein Antonym: ").strip()
                    correct = user_synonym == meanings['synonym'] and user_antonym == meanings['antonym']
                    print(f"Richtiges Synonym: {meanings['synonym']}, Richtiges Antonym: {meanings['antonym']}")
                    satisfied = input("\nBist du mit deiner Antwort zufrieden? (ja/nein): ").strip().lower()
                    if satisfied == "ja":
                        break

        elif choice == "h":
            verb, conjugations = create_conjugation_task(vocab_list, level)
            task = f"Konjugiere das Verb '{verb}' in den folgenden Zeiten: Präsens, Präteritum, Futur, Perfekt"
            print(task)
            print(conjugations)
            while True:
                user_conjugation = input("\nDeine Konjugation: ").strip()
                cleaned_text, comments = extract_comments(user_conjugation)
                corrected_conjugation = correct_text(task, cleaned_text, level)
                print("Korrigierte Konjugation:", corrected_conjugation)
                for comment in comments:
                    comment_response = answer_comment(comment)
                    print(f"Kommentar: {comment}\nAntwort: {comment_response}")
                satisfied = input("\nBist du mit deiner Antwort zufrieden? (ja/nein): ").strip().lower()
                if satisfied == "ja":
                    break

        else:
            print("Ungültige Wahl, bitte versuche es erneut.")

if __name__ == "__main__":
    main()
