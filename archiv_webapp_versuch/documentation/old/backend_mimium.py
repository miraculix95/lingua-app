from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS aktivieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Falls du es nur lokal brauchst, kannst du ["http://127.0.0.1:8080"] setzen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/daten")
async def get_daten():
    # return {"message": "Hallo von FastAPI!"}
    return "Let's rock n roll."
