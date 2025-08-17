from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB connection
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "emojidb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )

# 🔍 Search (partial match, categories, names)
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
    result = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "results": [
            {"word": w, "emoji": e, "category": c}
            for w, e, c in result
        ]
    }
