# PlotWeavers Backend

Flask API for PlotWeavers. Provides authentication, stories, chapters, comments, favorites, likes, uploads, and user endpoints.

## Docs
- See `docs/features/README.md` for the full feature catalog and endpoint references.

## Tech Stack
- Python, Flask
- Flask-JWT-Extended
- SQLAlchemy
- Flask-CORS

## Setup
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python app.py`

## Environment Variables
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL`
  - If not set, SQLite is used at `plotweavers.db`.

## Notes
- Tables are created on app startup.
- Uploads are stored under `uploads/profiles` and `uploads/stories`.
- Images are served via `/uploads/profiles/<filename>` and `/uploads/stories/<filename>`.
