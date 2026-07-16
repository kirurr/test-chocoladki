import csv
import io
import os
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request,
    send_from_directory,
)
from flask_cors import CORS

import metrics
from catalog import CATALOG_BY_ID, get_catalog, product_name
from db import init_db, query

BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR.parent / "frontend" / "dist"

load_dotenv(BASE_DIR / ".env")

app = Flask(__name__, static_folder=None, template_folder=str(BASE_DIR / "templates"))
CORS(app, resources={r"/api/*": {"origins": "*"}})

SURVEY_QUESTION_IDS = {"age", "gender", "frequency", "priority", "discount_driven"}


def now_ms():
    return int(time.time() * 1000)


def get_session(session_id):
    row = query("SELECT * FROM sessions WHERE id = ?", (session_id,), fetch="one")
    if row is None:
        abort(404, description="session not found")
    return row


# ---- API ----

@app.post("/api/session")
def create_session():
    session_id = str(uuid.uuid4())
    variant = "A" if uuid.uuid4().int % 2 == 0 else "B"
    query(
        "INSERT INTO sessions (id, variant, started_at, user_agent) VALUES (?, ?, ?, ?)",
        (session_id, variant, now_ms(), request.headers.get("User-Agent", "")),
    )
    return jsonify(
        {"session_id": session_id, "variant": variant, "catalog": get_catalog()}
    )


@app.post("/api/session/<session_id>/survey")
def save_survey(session_id):
    get_session(session_id)
    data = request.get_json(silent=True) or {}
    answers = data.get("answers")
    if not isinstance(answers, list) or not answers:
        abort(400, description="answers required")
    for a in answers:
        qid = a.get("question_id")
        ans = a.get("answer")
        if qid not in SURVEY_QUESTION_IDS or ans is None:
            abort(400, description=f"invalid answer: {a}")
        query(
            "INSERT INTO survey_answers (session_id, question_id, answer) VALUES (?, ?, ?)",
            (session_id, qid, str(ans)),
        )
    query(
        "UPDATE sessions SET catalog_shown_at = ? WHERE id = ?",
        (now_ms(), session_id),
    )
    return jsonify({"ok": True})


@app.post("/api/session/<session_id>/click")
def log_click(session_id):
    get_session(session_id)
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    since_shown = data.get("since_shown")
    click_order = data.get("click_order")
    if product_id not in CATALOG_BY_ID or since_shown is None or click_order is None:
        abort(400, description="product_id, since_shown, click_order required")
    query(
        """INSERT INTO clicks (session_id, product_id, clicked_at, since_shown, click_order)
           VALUES (?, ?, ?, ?, ?)""",
        (session_id, product_id, now_ms(), int(since_shown), int(click_order)),
    )
    if int(click_order) == 1:
        query(
            "UPDATE sessions SET first_click_at = ?, time_to_first_click = ? WHERE id = ?",
            (now_ms(), int(since_shown), session_id),
        )
    return jsonify({"ok": True})


@app.post("/api/session/<session_id>/choice")
def save_choice(session_id):
    get_session(session_id)
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    since_shown = data.get("since_shown")
    reason = data.get("reason", "")
    if product_id not in CATALOG_BY_ID or since_shown is None:
        abort(400, description="product_id, since_shown required")
    query(
        """UPDATE sessions
           SET chosen_product_id = ?, choice_reason = ?, chosen_at = ?,
               time_to_choice = ?, completed = 1
           WHERE id = ?""",
        (product_id, str(reason), now_ms(), int(since_shown), session_id),
    )
    existing = query(
        """SELECT id FROM clicks
           WHERE session_id = ? AND product_id = ?
           ORDER BY click_order DESC LIMIT 1""",
        (session_id, product_id),
        fetch="one",
    )
    if existing:
        query("UPDATE clicks SET is_final = 1 WHERE id = ?", (existing["id"],))
    else:
        next_order = query(
            "SELECT COALESCE(MAX(click_order), 0) + 1 AS n FROM clicks WHERE session_id = ?",
            (session_id,),
            fetch="one",
        )["n"]
        query(
            """INSERT INTO clicks (session_id, product_id, clicked_at, since_shown, is_final, click_order)
               VALUES (?, ?, ?, ?, 1, ?)""",
            (session_id, product_id, now_ms(), int(since_shown), int(next_order)),
        )
    return jsonify({"ok": True})


# ---- Metrics ----

@app.get("/metrics")
def metrics_page():
    return render_template(
        "metrics.html", data=metrics.summary(), questions=metrics.SURVEY_QUESTIONS
    )


@app.get("/api/metrics.csv")
def metrics_csv():
    sessions = metrics.raw_sessions()
    buf = io.StringIO()
    fields = [
        "id", "variant", "started_at", "time_to_first_click", "time_to_choice",
        "chosen_product_id", "chosen_product_name", "choice_reason", "completed",
        "age", "gender", "frequency", "priority", "discount_driven",
    ]
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for s in sessions:
        row = dict(s)
        row.update(s.get("survey", {}))
        writer.writerow(row)
    return (
        buf.getvalue(),
        200,
        {
            "Content-Type": "text/csv; charset=utf-8",
            "Content-Disposition": "attachment; filename=sessions.csv",
        },
    )


# ---- Frontend (prod) ----

@app.get("/")
def index():
    if not (DIST_DIR / "index.html").exists():
        return (
            "Frontend not built. Run `npm run build` in frontend/ "
            "or use the Vite dev server on :5173.",
            200,
        )
    return send_from_directory(DIST_DIR, "index.html")


@app.get("/<path:path>")
def static_proxy(path):
    target = DIST_DIR / path
    if target.exists() and target.is_file():
        return send_from_directory(DIST_DIR, path)
    if (DIST_DIR / "index.html").exists():
        return send_from_directory(DIST_DIR, "index.html")
    abort(404)


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
