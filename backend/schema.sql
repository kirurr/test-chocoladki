CREATE TABLE IF NOT EXISTS sessions (
    id                  TEXT PRIMARY KEY,
    variant             TEXT NOT NULL,
    started_at          INTEGER NOT NULL,
    catalog_shown_at    INTEGER,
    first_click_at      INTEGER,
    chosen_at           INTEGER,
    time_to_first_click INTEGER,
    time_to_choice      INTEGER,
    chosen_product_id   TEXT,
    choice_reason       TEXT,
    completed           INTEGER NOT NULL DEFAULT 0,
    user_agent          TEXT
);

CREATE TABLE IF NOT EXISTS clicks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL REFERENCES sessions(id),
    product_id  TEXT NOT NULL,
    clicked_at  INTEGER NOT NULL,
    since_shown INTEGER NOT NULL,
    is_final    INTEGER NOT NULL DEFAULT 0,
    click_order INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_answers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL REFERENCES sessions(id),
    question_id TEXT NOT NULL,
    answer      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_clicks_session   ON clicks(session_id);
CREATE INDEX IF NOT EXISTS idx_survey_session   ON survey_answers(session_id);
CREATE INDEX IF NOT EXISTS idx_sessions_variant ON sessions(variant);
