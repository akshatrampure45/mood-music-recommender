# Auris — Mood-Matched Music Recommender

Live webcam → facial emotion detection (Python/DeepFace) → Spotify playlist
search → direct redirect into the Spotify app, refined by language/region/genre.

```
frontend (React + Vite)  →  backend (FastAPI)  →  DeepFace (emotion) + Spotify Web API
                                     ↓
                                  MySQL (mood logs, preferences, playlist opens)
```

## 1. Spotify credentials

Create an app at https://developer.spotify.com/dashboard → copy the **Client ID**
and **Client Secret**. This project uses the Client Credentials flow (app-only,
no user login), which is enough for searching public playlists and redirecting
into Spotify — nothing here needs your users to log into Spotify themselves.

## 2. MySQL

```bash
mysql -u root -p < backend/init_db.sql
```

This creates the `mood_music` database and its three tables (`mood_logs`,
`preferences`, `playlist_requests`). The backend also auto-creates any missing
tables on startup, so this step is a convenience, not a hard requirement.

## 3. Backend (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
copy .env.example .env         # Windows: copy, macOS/Linux: cp
# then edit .env with your Spotify + MySQL credentials

uvicorn app.main:app --reload --port 8000
```

First startup downloads DeepFace's emotion-detection model weights
(~a few hundred MB, one-time, cached afterward). The `/api/health` endpoint
should return `{"status": "ok"}` once it's up.

## 4. Frontend (React)

```bash
cd frontend
npm install
copy .env.example .env         # Windows: copy, macOS/Linux: cp
npm run dev
```

Open http://localhost:5173. The browser will ask for camera permission —
that's the live feed being analyzed every 2.5s (see `CAPTURE_INTERVAL_MS` in
`WebcamCapture.jsx` if you want it faster/slower).

## 5. Your background image

Drop your image at `frontend/public/background.jpg`, then in
`frontend/src/index.css` uncomment:
```css
body { --bg-image: url('/background.jpg'); }
```
It sits behind a dark gradient wash so the light-on-dark UI stays readable —
adjust the gradient opacity in the `body` rule if you want more or less of
the image showing through.

## How it's wired together

- **Mood detection**: the browser captures a webcam frame every 2.5s and
  POSTs it to `POST /api/mood/detect`. The backend runs DeepFace on it
  (downscaled first for speed) and returns the dominant emotion + full score
  breakdown, which drives the "aura" ring's color in real time.
- **Playlist search**: `GET /api/playlists` builds a Spotify search query from
  the current mood + optional language/genre, scoped to a region via
  `market=<region>`, and returns playlist cards.
- **Redirect to Spotify**: each card's "Open in Spotify" button navigates to
  the playlist's `spotify:playlist:<id>` URI first (opens the native app if
  installed), falling back to the `open.spotify.com` web link if the app
  doesn't intercept it.
- **MySQL** stores every detected mood, every preference submission, and
  every playlist actually opened — enough to later show "your most common
  mood this week" or similar without adding new tables.

## Extending it

- Swap `detector_backend="opencv"` for `"retinaface"` in
  `emotion_detector.py` for higher accuracy at some speed cost.
- Add real user accounts (the schema already keys everything off
  `session_id`, so swapping in an auth system mostly means populating that
  field from a logged-in user instead of a random UUID).
- Cache Spotify search results per (mood, language, region) for a few
  minutes to cut down on repeat API calls.
