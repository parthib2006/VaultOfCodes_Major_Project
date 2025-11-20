import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, g
from prompt_templates import PROMPTS  # keep your prompt templates

DATABASE = os.path.join(os.path.dirname(__file__), "data.sqlite3")

app = Flask(__name__, static_folder="static", template_folder="templates")

def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            function TEXT,
            template_id TEXT,
            user_input TEXT,
            prompt_sent TEXT,
            response TEXT,
            is_helpful INTEGER,
            comment TEXT,
            ts TEXT
        )
    """)
    db.commit()

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()

# ---- MOCK AI FUNCTION ----
def call_ai_mock(prompt):
    prompt = prompt.lower()
    if "summarize" in prompt:
        return "📝 This is a mock summary of your text."
    elif "story" in prompt or "poem" in prompt or "creative" in prompt:
        return "🎨 This is a mock creative response."
    else:
        return "✅ This is a mock answer to your question."

def build_prompt(fn, tid, text, extra):
    fn_prompts = PROMPTS.get(fn, {})
    template = fn_prompts.get(tid, fn_prompts.get("short", "{USER_TEXT}"))
    
    data = {
        "USER_TEXT": text,
        "STYLE": "",
        "TONE": "",
        "AUDIENCE": "",
        "THEME": "",
        "MOOD": "",
        "MOTIFS": "",
        "LENGTH": "",
    }

    if extra:
        for k, v in extra.items():
            data[k.upper()] = v

    return template.format(**data)

@app.route("/", methods=["GET"])
def index():
    init_db()
    return render_template("index.html")

@app.route("/api/assistant", methods=["POST"])
def assistant():
    data = request.get_json() or {}
    fn = data.get("function", "answer")
    tid = data.get("template_id", "short")
    user_input = data.get("user_input", "")[:4000]
    extra = data.get("extra", {})

    prompt = build_prompt(fn, tid, user_input, extra)
    response = call_ai_mock(prompt)

    db = get_db()
    db.execute(
        "INSERT INTO logs (function, template_id, user_input, prompt_sent, response, is_helpful, comment, ts) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (fn, tid, user_input, prompt, response, None, None, datetime.utcnow().isoformat())
    )
    db.commit()
    log_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

    return jsonify({"ok": True, "response": response, "log_id": log_id})

@app.route("/api/feedback", methods=["POST"])
def feedback():
    data = request.get_json() or {}
    log_id = data.get("log_id")
    helpful = 1 if data.get("helpful") else 0
    comment = data.get("comment", "")

    if not log_id:
        return jsonify({"ok": False, "error": "missing log_id"}), 400

    db = get_db()
    db.execute(
        "UPDATE logs SET is_helpful = ?, comment = ? WHERE id = ?",
        (helpful, comment, log_id)
    )
    db.commit()

    return jsonify({"ok": True})

@app.route("/admin/logs", methods=["GET"])
def view_logs():
    db = get_db()
    rows = db.execute("SELECT * FROM logs ORDER BY ts DESC LIMIT 200").fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="127.0.0.1", port=8000, debug=True)