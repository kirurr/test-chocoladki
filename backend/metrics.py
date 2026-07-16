from catalog import product_name
from db import query

SURVEY_QUESTIONS = {
    "age": "Age",
    "gender": "Gender",
    "frequency": "Purchase frequency",
    "priority": "What matters most",
    "discount_driven": "Discount-driven",
}


def _round(value, ndigits=0):
    if value is None:
        return None
    return round(value, ndigits)


def _seconds(ms):
    if ms is None:
        return None
    return round(ms / 1000, 1)


def choices_by_product():
    rows = query(
        """
        SELECT variant, chosen_product_id, COUNT(*) AS n
        FROM sessions
        WHERE chosen_product_id IS NOT NULL
        GROUP BY variant, chosen_product_id
        """,
        fetch="all",
    )
    products = {}
    for r in rows:
        pid = r["chosen_product_id"]
        row = products.setdefault(pid, {"product": product_name(pid), "A": 0, "B": 0})
        row[r["variant"]] = r["n"]
    result = list(products.values())
    result.sort(key=lambda x: (x["A"] + x["B"]), reverse=True)
    return result


def timing_by_variant():
    rows = query(
        """
        SELECT variant,
               COUNT(*) AS sessions,
               SUM(completed) AS completed,
               AVG(time_to_first_click) AS avg_first_click,
               AVG(time_to_choice) AS avg_choice
        FROM sessions
        GROUP BY variant
        ORDER BY variant
        """,
        fetch="all",
    )
    for r in rows:
        r["avg_first_click"] = _seconds(r["avg_first_click"])
        r["avg_choice"] = _seconds(r["avg_choice"])
    return rows


def click_behavior_by_variant():
    rows = query(
        """
        SELECT s.variant,
               COUNT(c.id) AS total_clicks,
               SUM(CASE WHEN c.is_final = 0 THEN 1 ELSE 0 END) AS non_final_clicks,
               COUNT(DISTINCT s.id) AS sessions_with_clicks
        FROM sessions s
        JOIN clicks c ON c.session_id = s.id
        GROUP BY s.variant
        ORDER BY s.variant
        """,
        fetch="all",
    )
    for r in rows:
        total = r["total_clicks"] or 0
        non_final = r["non_final_clicks"] or 0
        sessions = r["sessions_with_clicks"] or 0
        r["non_final_share"] = _round(100 * non_final / total, 1) if total else None
        r["avg_clicks_to_choice"] = _round(total / sessions, 2) if sessions else None
    return rows


def choice_by_priority():
    rows = query(
        """
        SELECT sa.answer AS priority, s.chosen_product_id, COUNT(*) AS n
        FROM sessions s
        JOIN survey_answers sa ON sa.session_id = s.id AND sa.question_id = 'priority'
        WHERE s.chosen_product_id IS NOT NULL
        GROUP BY sa.answer, s.chosen_product_id
        ORDER BY sa.answer, n DESC
        """,
        fetch="all",
    )
    grouped = {}
    for r in rows:
        grouped.setdefault(r["priority"], []).append(
            {"product": product_name(r["chosen_product_id"]), "n": r["n"]}
        )
    return grouped


def raw_sessions():
    sessions = query(
        """
        SELECT id, variant, started_at, time_to_first_click, time_to_choice,
               chosen_product_id, choice_reason, completed
        FROM sessions
        ORDER BY started_at DESC
        """,
        fetch="all",
    )
    answers = query(
        "SELECT session_id, question_id, answer FROM survey_answers", fetch="all"
    )
    by_session = {}
    for a in answers:
        by_session.setdefault(a["session_id"], {})[a["question_id"]] = a["answer"]
    for s in sessions:
        s["chosen_product_name"] = (
            product_name(s["chosen_product_id"]) if s["chosen_product_id"] else ""
        )
        s["survey"] = by_session.get(s["id"], {})
    return sessions


def summary():
    return {
        "choices_by_product": choices_by_product(),
        "timing_by_variant": timing_by_variant(),
        "click_behavior": click_behavior_by_variant(),
        "choice_by_priority": choice_by_priority(),
    }
