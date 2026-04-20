from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv
import openai
import os
import jwt
from datetime import datetime
from database import create_user, get_user, update_credits, init_db


########################### Inits
# OpenAI
load_dotenv(find_dotenv())
client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")) ### connection every time?

# Database
init_db()

# Backend Server
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Falls du es nur lokal brauchst, kannst du ["http://127.0.0.1:8080"] setzen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################ Token functions
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(username: str):
    expires = datetime.now()
    return jwt.encode({"sub": username, "exp": expires}, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except:
        raise HTTPException(status_code=401, detail="Ungültiges Token")    

# Template-Rendering
def render_template(template_name: str):
    with open(f"frontend/{template_name}", "r") as f:
        return HTMLResponse(content=f.read())
    
############################# Authentification
@app.get("/", response_class=HTMLResponse)
async def home():
    return render_template("index.html")

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = get_user(username)
    if not user or user["password"] != password:
        return JSONResponse({"error": "Falsche Login-Daten"}, status_code=400) ### verbessern für feedback

    token = create_token(username)  # Token generieren
    return JSONResponse({"redirect": "/chat.html", "access_token": token})  # Token zurückgeben

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    print(f"DEBUG: Eingehende Registrierung - Username: {username}")  # Debug-Ausgabe

    if get_user(username):
        print("DEBUG: User existiert bereits!")
        raise HTTPException(status_code=400, detail="User existiert bereits")

    create_user(username, password)
    print("DEBUG: User wurde erstellt!")

    return RedirectResponse(url="/login", status_code=303)

################################ Chat - AI Endpoints
@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    return render_template("chat.html")

@app.post("/ask")
async def ask_openai(request: Request, token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = get_user(username)
    
    if user["credits"] <= 0:
        return HTMLResponse("<p>Keine Credits mehr! Bitte Credits kaufen.</p>")

    form_data = await request.form()
    question_text = form_data.get("message")  # Nur den reinen String extrahieren

    if not question_text:
        return HTMLResponse("<p>Fehler: Keine Frage eingegeben!</p>", status_code=400)

    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": question_text}],  # Jetzt korrekt formatiert
        temperature=0.7
    )
    
    reply = response.choices[0].message.content  # Neue Zugriffsmethode für GPT-4 API
    
    update_credits(username, -1)
    user = get_user(username)    
    
    # Antwort + Credits mit `hx-swap-oob` für mehrere Updates
    return HTMLResponse(f"""
        <p id="response"><strong>GPT:</strong> {reply}</p>
    """)
    
    
@app.get("/debug")
async def debug(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = get_user(username)
    return HTMLResponse(f"<p>DEBUG: {username} hat {user['credits']} Credits.</p>")

@app.post("/buy_credits")
async def buy_credits(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    update_credits(username, 10)
    user = get_user(username)


@app.get("/credit-count")
async def credit_count(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = get_user(username)
    return HTMLResponse(
        f"{user['credits']}",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"})

#### old endpoints
# @app.post("/openai", response_class=HTMLResponse)
# async def ask_openai(frage: str = Form(...)):  
#     try:
#         response = await client.chat.completions.create(  # OpenAI asynchron aufrufen
#             model="gpt-4-turbo",  # Falls du Azure nutzt, verwende dein Modell
#             messages=[{"role": "user", "content": frage}],
#             temperature=0.7
#         )
#         reply = response.choices[0].message.content  # Korrekte Zugriffsmethode
        
#         # return f"<p><strong>GPT sagt:</strong> {reply}</p>"
    
#     except Exception as e:
#         return f"<p><strong>Fehler:</strong> {str(e)}</p>"