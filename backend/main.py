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
# Emoji lookup route (supports word OR category, with normalization)
@app.get("/emoji")
def get_emoji(word: str):
    conn = get_db_connection()
    cur = conn.cursor()

    # Normalize input
    q = word.strip().lower().rstrip("s")
    q_space = q.replace(" ", "_")      # "gateway of india" → "gateway_of_india"
    q_joined = "_".join(q.split())     # "tajmahal" → "taj_mahal"

    cur.execute("""
        SELECT word, emoji, category
        FROM emojis
        WHERE word ILIKE %s OR word ILIKE %s OR word ILIKE %s
           OR category ILIKE %s OR category ILIKE %s OR category ILIKE %s
        LIMIT 50;
    """, (
        f"%{q}%", f"%{q_space}%", f"%{q_joined}%",
        f"%{q}%", f"%{q_space}%", f"%{q_joined}%"
    ))

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

    # Split by comma, strip spaces/plurals
    queries = [q.strip().lower().rstrip("s") for q in query.split(",")]

    results = []
    for q in queries:
        # Normalize variations
        q_space = q.replace(" ", "_")      # "gateway of india" → "gateway_of_india"
        q_joined = "_".join(q.split())     # "chainbridge" → "chain_bridge"

        # Try multiple match patterns
        cur.execute("""
            SELECT word, emoji, category
            FROM emojis
            WHERE word ILIKE %s OR word ILIKE %s OR word ILIKE %s
               OR category ILIKE %s OR category ILIKE %s OR category ILIKE %s
            LIMIT 50;
        """, (
            f"%{q}%", f"%{q_space}%", f"%{q_joined}%",
            f"%{q}%", f"%{q_space}%", f"%{q_joined}%"
        ))

        results.extend(cur.fetchall())

    cur.close()
    conn.close()

    # Deduplicate
    seen = set()
    unique_results = []
    for r in results:
        if (r[0], r[1]) not in seen:
            seen.add((r[0], r[1]))
            unique_results.append({"word": r[0], "emoji": r[1], "category": r[2]})

    return {"results": unique_results}
