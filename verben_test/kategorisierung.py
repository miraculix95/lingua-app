import json
# from langchain.llms import OpenAI
# from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from typing import List, Dict, Any
from dotenv import load_dotenv, find_dotenv

# Datenstruktur für die Kategorien
class DynamicCategory:
    def __init__(self, name: str, verbs: List[str]):
        self.name = name
        self.verbs = verbs

    def to_dict(self):
        return {"name": self.name, "verbs": self.verbs}

# Funktion: Einlesen der unsortierten Verben
def read_verbs_from_file(input_file: str) -> List[str]:
    with open(input_file, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]  # Entfernt Leerzeilen

def propose_categories(verbs: List[str]) -> List[str]:
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    # Prompt: Kategorien vorschlagen
    prompt = f"""
    Hier ist eine Liste französischer Verben:
    {', '.join(verbs)}

    Erstelle eine Liste von semantischen Kategorien, die zu diesen Verben passen könnten.
    Gib nur die Kategorien zurück, jeweils durch ein Komma getrennt.
    """

    response = llm.invoke(prompt)
    categories = response.content.split(",")  # Extrahiere die Kategorien
    return [cat.strip() for cat in categories if cat.strip()]

def assign_verbs_to_categories(verbs: List[str], categories: List[str]) -> List[DynamicCategory]:
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    # Prompt: Verben zu Kategorien zuordnen
    prompt = f"""
    Hier ist eine Liste französischer Verben:
    {', '.join(verbs)}

    Und hier sind Kategorien:
    {', '.join(categories)}

    Ordne die Verben den Kategorien zu. Gib die Antwort im folgenden JSON-Format zurück:
    [
        {{"name": "Bewegung", "verbs": ["grimper", "sauter"]}},
        {{"name": "Emotionen", "verbs": ["émouvoir", "stupéfier"]}}
    ]
    """

    response = llm.invoke(prompt)
    print("Output zweiter Output:", response.content, "xxxEnde")
    parsed_response = json.loads(response.content)  # JSON parsen
    return [DynamicCategory(cat["name"], cat["verbs"]) for cat in parsed_response]

# Funktion: Verarbeiten der Verben mit LangChain
# def process_verbs_with_llm(verbs: List[str]) -> List[DynamicCategory]:
#     llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    
#     # OutputParser definieren
#     response_schema = ResponseSchema(
#         name="categories",
#         description="Eine Liste von Kategorien mit Namen und den zugeordneten Verben."
#     )
#     parser = StructuredOutputParser.from_response_schemas([response_schema])
#     format_instructions = parser.get_format_instructions()
    
#     # Prompt vorbereiten
#     prompt = f"""
#     Hier ist eine Liste französischer Verben:
#     {', '.join(verbs)}

#     Sortiere diese Verben semantisch in dynamische Kategorien. Jede Kategorie sollte einen Namen haben und die zugehörigen Verben enthalten. Gib die Antwort im folgenden Format zurück:
#     {format_instructions}
#     """
#     print("Prompt:", prompt)
#     # LLM-Abfrage
#     print("Execute llm")
#     response = llm.invoke(prompt)
#     print("LLM executed")
#     parsed_response = parser.parse(response.content)  # Ausgabe parsen und validieren
#     categories = parsed_response.get("categories", [])
    
#     # Konvertiere die Kategorien in DynamicCategory-Objekte
#     return [DynamicCategory(cat["name"], cat["verbs"]) for cat in categories]

def validate_and_clean_categories(categories: List[DynamicCategory], original_verbs: List[str]) -> List[DynamicCategory]:
    # Alle Verben aus der Ausgabe sammeln
    output_verbs = []
    for category in categories:
        output_verbs.extend(category.verbs)
    
    # Fehlende und zusätzliche Verben ermitteln
    missing_verbs = set(original_verbs) - set(output_verbs)
    extra_verbs = set(output_verbs) - set(original_verbs)
    
    # Entferne zusätzliche Verben
    cleaned_categories = []
    for category in categories:
        category.verbs = [verb for verb in category.verbs if verb not in extra_verbs]
        cleaned_categories.append(category)
    
    # Füge fehlende Verben in eine neue Kategorie ein
    if missing_verbs:
        cleaned_categories.append(DynamicCategory("Nicht kategorisiert", list(missing_verbs)))
    
    return cleaned_categories

# Funktion: Speichern der Ergebnisse
def save_output(categories: List[DynamicCategory], output_file: str):
    # Konvertiere Kategorien in ein JSON-kompatibles Format
    data = [category.to_dict() for category in categories]
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Die sortierten Verben wurden erfolgreich in {output_file} gespeichert.")

# Hauptprogramm
def main(input_file: str, output_file: str):
    load_dotenv(find_dotenv())
    # 1. Verben einlesen
    unsorted_verbs = read_verbs_from_file(input_file)
    
    # 2. Kategorien vorschlagen
    categories = propose_categories(unsorted_verbs)
    print(f"Vorgeschlagene Kategorien: {categories}")
    
    # 3. Verben zu Kategorien zuordnen
    assigned_categories = assign_verbs_to_categories(unsorted_verbs, categories)

    # 4. Validierung und Bereinigung
    final_categories = validate_and_clean_categories(assigned_categories, unsorted_verbs)

    # 4. Speichere die bereinigten Kategorien
    save_output(final_categories, output_file); print("Finished all")

# Ausführung
if __name__ == "__main__":
    input_file = "franz-verben.txt"
    output_file = "franz-verben_sortiert.json"
    main(input_file, output_file)
