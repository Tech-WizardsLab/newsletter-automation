# backend/app.py
import os, sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from services.newsletter_service import build_newsletter

DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "database.db"))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS news (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          url TEXT,
          category TEXT DEFAULT 'GLOBAL',
          approved INTEGER DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS events (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          date TEXT,
          location TEXT,
          url TEXT,
          approved INTEGER DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_first_request
def setup():
    init_db()

@app.get("/news")
def list_news():
    conn = get_db()
    items = conn.execute(
        "SELECT id,title,url,category,approved,created_at FROM news ORDER BY created_at DESC"
    ).fetchall()
    return jsonify({"news": [dict(x) for x in items]})

@app.post("/news/approve/<int:news_id>")
def approve_news(news_id: int):
    conn = get_db()
    conn.execute("UPDATE news SET approved=1 WHERE id=?", (news_id,))
    conn.commit()
    return jsonify({"success": True, "id": news_id})

@app.put("/news/<int:news_id>")
def edit_news(news_id: int):
    data = request.get_json() or {}
    title = data.get("title")
    category = data.get("category")
    url = data.get("url")
    sets, vals = [], []
    if title is not None:
        sets.append("title=?"); vals.append(title)
    if category is not None:
        sets.append("category=?"); vals.append(category)
    if url is not None:
        sets.append("url=?"); vals.append(url)
    if not sets:
        return jsonify({"success": False, "error": "No fields provided"}), 400
    vals.append(news_id)
    conn = get_db()
    conn.execute(f"UPDATE news SET {', '.join(sets)} WHERE id=?", vals)
    conn.commit()
    return jsonify({"success": True, "id": news_id})

@app.delete("/news/<int:news_id>")
def delete_news(news_id: int):
    conn = get_db()
    conn.execute("DELETE FROM news WHERE id=?", (news_id,))
    conn.commit()
    return jsonify({"success": True, "id": news_id})

@app.get("/events")
def list_events():
    conn = get_db()
    items = conn.execute(
        "SELECT id,title,date,location,url,approved FROM events ORDER BY date"
    ).fetchall()
    return jsonify({"events": [dict(x) for x in items]})

@app.post("/events/approve/<int:event_id>")
def approve_event(event_id: int):
    conn = get_db()
    conn.execute("UPDATE events SET approved=1 WHERE id=?", (event_id,))
    conn.commit()
    return jsonify({"success": True, "id": event_id})

@app.get("/generate-newsletter")
def generate_newsletter():
    conn = get_db()
    news = [
        dict(x)
        for x in conn.execute(
            "SELECT * FROM news WHERE approved=1 ORDER BY category, created_at DESC"
        ).fetchall()
    ]
    events = [
        dict(x)
        for x in conn.execute(
            "SELECT * FROM events WHERE approved=1 ORDER BY date"
        ).fetchall()
    ]
    content = build_newsletter(news, events)
    return jsonify({"newsletter": content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
