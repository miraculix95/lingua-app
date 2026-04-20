import sqlite3

DB_NAME = "users.db"

def init_db():
    print("Initializing database...")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY, 
        password TEXT, 
        credits INTEGER DEFAULT 5
    )
    """)
    conn.commit()
    conn.close()

def create_user(username, password):
    print(f"DEBUG: create_user() aufgerufen mit: {username}")
    
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"DEBUG: User {username} erfolgreich gespeichert!")
    
    except Exception as e:
        print(f"FEHLER: {e}")
    
    finally:
        conn.close()

def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user is None:
        return None  # Sicherstellen, dass kein Fehler auftritt
    
    return {"username": user[0], "password": user[1], "credits": user[2]}


def update_credits(username, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET credits = credits + ? WHERE username=?", (amount, username))
    conn.commit()
    conn.close()

init_db()
