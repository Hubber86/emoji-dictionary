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
    "https://emoji-dictionary-1.onrender.com",  # frontend
    "http://localhost:5173",                   # local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB connection
def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise Exception("DATABASE_URL not set in environment")

    result = urlparse(db_url)
    return psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

@app.get("/")
def home():
    return {"message": "API running 🚀"}

# 🎯 Exact single word lookup
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

# 🎯 Advanced search (by word OR category)
@app.get("/search")
def search_emoji(query: str):
    query = query.lower().strip()
    conn = get_db_connection()
    cur = conn.cursor()

    # 1️⃣ Check category match (handles plural by stripping "s")
    singular = query[:-1] if query.endswith("s") else query
    cur.execute("""
        SELECT word, emoji, category 
        FROM emojis 
        WHERE category ILIKE %s
        LIMIT 50;
    """, (f"%{singular}%",))
    cat_results = cur.fetchall()

    if cat_results:
        cur.close()
        conn.close()
        return {"results": [{"word": w, "emoji": e, "category": c} for w, e, c in cat_results]}

    # 2️⃣ Word match
    cur.execute("""
        SELECT word, emoji, category 
        FROM emojis 
        WHERE word ILIKE %s
        LIMIT 20;
    """, (f"%{query}%",))
    db_results = cur.fetchall()

    # Close connection
    cur.close()
    conn.close()

    results = [{"word": w, "emoji": e, "category": c} for w, e, c in db_results]

    # 3️⃣ Fuzzy fallback
    if not results:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT word, emoji, category FROM emojis LIMIT 500;")
        all_words = cur.fetchall()
        cur.close()
        conn.close()

        word_list = [w for w, _, _ in all_words]
        close_matches = difflib.get_close_matches(query, word_list, n=5, cutoff=0.6)
        for match in close_matches:
            for w, e, c in all_words:
                if w == match:
                    results.append({"word": w, "emoji": e, "category": c})

    # Deduplicate
    seen = set()
    final = []
    for r in results:
        if r["word"] not in seen:
            final.append(r)
            seen.add(r["word"])

    return {"results": final}
