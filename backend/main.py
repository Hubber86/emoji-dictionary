from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import difflib

# Load .env file
load_dotenv()

app = FastAPI()

# ✅ CORS settings
origins = [
    "https://emoji-dictionary-1.onrender.com",  # your frontend URL
    "http://localhost:5173",                   # local dev
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

# 🎯 Exact emoji lookup route
@app.get("/emoji")
def get_emoji(word: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT emoji FROM emojis WHERE word = %s;", (word.lower(),))
    result = cur.fetchone()
    cur.close()
    conn.close()
    
    if result:
        return {"word": word, "emoji": result[0]}
    return {"error": "Not found"}

# 🎯 Search / autocomplete route
@app.get("/search")
def search_emoji(query: str):
    query = query.lower().strip()
    conn = get_db_connection()
    cur = conn.cursor()

    # 1️⃣ Substring / category match
    cur.execute("""
        SELECT word, emoji 
        FROM emojis 
        WHERE word ILIKE %s 
        LIMIT 20;
    """, (f"%{query}%",))
    db_results = cur.fetchall()

    cur.close()
    conn.close()

    # Convert to list of dicts
    results = [{"word": w, "emoji": e} for w, e in db_results]

    # 2️⃣ Fuzzy fallback (for plural/typos)
    if not results:
        # Pull a small dictionary to compare
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT word, emoji FROM emojis LIMIT 500;")  # limit to avoid huge load
        all_words = cur.fetchall()
        cur.close()
        conn.close()

        word_list = [w for w, _ in all_words]
        close_matches = difflib.get_close_matches(query, word_list, n=5, cutoff=0.6)
        for match in close_matches:
            for w, e in all_words:
                if w == match:
                    results.append({"word": w, "emoji": e})

    # Deduplicate
    seen = set()
    final = []
    for r in results:
        if r["word"] not in seen:
            final.append(r)
            seen.add(r["word"])

    return {"results": final}
