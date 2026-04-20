from fastapi import FastAPI, Form
import openai
import os
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Falls du es nur lokal brauchst, kannst du ["http://127.0.0.1:8080"] setzen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI-Client initialisieren
client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/openai", response_class=HTMLResponse)
async def ask_openai(frage: str = Form(...)):  
    try:
        response = await client.chat.completions.create(  # OpenAI asynchron aufrufen
            model="gpt-4-turbo",  # Falls du Azure nutzt, verwende dein Modell
            messages=[{"role": "user", "content": frage}],
            temperature=0.7
        )
        reply = response.choices[0].message.content  # Korrekte Zugriffsmethode
        
        return f"<p><strong>GPT sagt:</strong> {reply}</p>"
    
    except Exception as e:
        return f"<p><strong>Fehler:</strong> {str(e)}</p>"
