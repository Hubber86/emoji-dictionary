from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

# ✅ Allowed frontend origins
origins = [
    "https://emoji-dictionary-1.onrender.com",  # deployed frontend
    "https://emoji-dictionary.onrender.com",
    "http://localhost:5173",                    # local dev
]

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 🚨 opens to everyone
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "emojidb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )

# 🔍 Search (partial match on word/category)
@app.get("/search")
def search_emojis(query: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT word, emoji, category 
        FROM emojis 
        WHERE word ILIKE %s OR category ILIKE %s
        LIMIT 20;
        """,
        (f"%{query}%", f"%{query}%"),
    )
    results = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "results": [
            {"word": w, "emoji": e, "category": c}
            for w, e, c in results
        ]
    }

# 🎯 Exact word lookup
@app.get("/emoji")
def get_emoji(word: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT word, emoji, category FROM emojis WHERE word = %s;",
        (word.lower(),),
    )
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        w, e, c = result
        return {"word": w, "emoji": e, "category": c}
    return {"error": "Emoji not found"}
