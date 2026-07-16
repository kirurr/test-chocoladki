# Chocolates — UX study prototype

A prototype site for studying chocolate choice (an eye-tracking imitation). A user
completes a short survey and picks a chocolate bar from the shelf in one of two
visual versions (A — discount emphasis, B — brand emphasis). Clicks, timings, and
survey answers are written to the database. The public `/metrics` page shows
aggregates and a CSV export.

Full brief and data schema — see [`spec.md`](spec.md).

## Stack

- Backend: Flask + SQLite (a local `backend/dev.db` file, created on first run).
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

The `backend/dev.db` file and its schema are created automatically on startup.

## Production build

```bash
cd frontend
npm run build            # -> frontend/dist

cd ../backend
pip install -r requirements.txt
python app.py            # Flask serves dist at http://localhost:5000
# or: gunicorn wsgi:application
```

## Deploy

See [`DEPLOY.md`](DEPLOY.md) for PythonAnywhere deployment steps.

## Product images

`frontend/public/images/` holds the product photos `choco_01.jpg…choco_10.jpg`.
To swap them, replace the files keeping the same names (or update the `image`
field in `backend/catalog.py`). Rebuild the frontend afterwards.

## Data

- `/metrics` — aggregate tables.
- `/api/metrics.csv` — raw sessions, one row per respondent (UTF-8). Timing columns are in milliseconds.
