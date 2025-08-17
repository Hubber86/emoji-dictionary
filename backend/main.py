from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = FastAPI()

# ✅ CORS settings
origins = [
    "https://emoji-dictionary-1.onrender.com",  # your frontend URL
    "http://localhost:5173",                   # optional: local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection function
def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise Exception("DATABASE_URL not set in environment")

    result = urlparse(db_url)
    return psycopg2.connect(
        database=result.path[1:],  # strip leading "/"
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

# Root route
@app.get("/")
def home():
    return {"message": "API running 🚀"}

# Emoji lookup route (supports word OR category)
@app.get("/emoji")
def get_emoji(word: str):
    conn = get_db_connection()
    cur = conn.cursor()

    # Lowercase + simple plural stripping
    singular = word.lower().rstrip("s")

    # First: try exact word match
    cur.execute("SELECT word, emoji, category FROM emojis WHERE word = %s;", (singular,))
    results = cur.fetchall()

    # If no direct word found → check if it's a category
    if not results:
        cur.execute("SELECT word, emoji, category FROM emojis WHERE category = %s;", (singular,))
        results = cur.fetchall()

    cur.close()
    conn.close()
    
    if results:
        return {"results": [{"word": r[0], "emoji": r[1], "category": r[2]} for r in results]}
    return {"error": "Not found"}

# 🔎 Autocomplete search
@app.get("/search")
def search_emojis(query: str):
    if not query:
        return {"results": []}

    conn = get_db_connection()
    cur = conn.cursor()

    # Handle plurals (simple heuristic: strip trailing 's')
    singular = query.lower().rstrip("s")

    # Match words or categories
    cur.execute("""
        SELECT word, emoji, category
        FROM emojis
        WHERE word ILIKE %s OR category ILIKE %s
        LIMIT 20;
    """, (f"%{singular}%", f"%{singular}%"))
    
    results = cur.fetchall()
    cur.close()
    conn.close()

    return {"results": [{"word": r[0], "emoji": r[1], "category": r[2]} for r in results]}
