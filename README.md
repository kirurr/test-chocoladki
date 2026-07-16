# Chocolates — UX study prototype

A prototype site for studying chocolate choice (an eye-tracking imitation). A user
completes a short survey and picks a chocolate bar from the shelf in one of two
visual versions (A — discount emphasis, B — brand emphasis). Clicks, timings, and
survey answers are written to the database. The public `/metrics` page shows
aggregates and a CSV export.

Full brief and data schema — see [`spec.md`](spec.md).

## Stack

- Backend: Flask + libsql (Turso) with a fallback to local SQLite (`dev.db`).
- Frontend: React + Vite. In production Flask serves the built `frontend/dist`.

## Development

Two terminals.

```bash
# 1) backend (http://localhost:5000)
cd backend
python -m venv venv
venv/Scripts/activate        # Windows; on Linux/mac: source venv/bin/activate
pip install -r requirements.txt
python app.py

# 2) frontend (http://localhost:5173, proxies /api to :5000)
cd frontend
npm install
npm run dev
```

Without the `TURSO_*` variables the backend writes to a local `backend/dev.db` file.

## Production build

```bash
cd frontend
npm run build            # -> frontend/dist

cd ../backend
pip install -r requirements.txt
python app.py            # Flask serves dist at http://localhost:5000
# or: gunicorn wsgi:application
```

## Turso

1. Create a database in Turso, get its URL and auth token.
2. Copy `backend/.env.example` to `backend/.env` and fill in:
   ```
   TURSO_DATABASE_URL=libsql://<db>.turso.io
   TURSO_AUTH_TOKEN=<token>
   ```
The schema is created automatically on startup (`init_db`).

## Deploy on PythonAnywhere

1. Build the frontend locally (`npm run build`), upload the whole project including `frontend/dist`.
2. Web app → point the WSGI file at `backend/wsgi.py` (the `application` variable).
3. Set the `TURSO_*` variables in the web app config.

## Product images

`frontend/public/images/` holds SVG placeholders `choco_01…choco_10`.
To use real photos, replace the files keeping the same names (or update the
`image` field in `backend/catalog.py`). Rebuild the frontend afterwards.

## Data

- `/metrics` — aggregate tables.
- `/api/metrics.csv` — raw sessions, one row per respondent (UTF-8). Timing columns are in milliseconds.
