from fastapi import FastAPI
import psycopg2
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = FastAPI()

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

@app.get("/")
def home():
    return {"message": "API running locally 🚀"}

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
