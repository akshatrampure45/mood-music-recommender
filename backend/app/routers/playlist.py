from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PlaylistRequest, Preference
from app.schemas import PlaylistResponse, PlaylistRequestLog
from app.spotify_service import search_playlists

router = APIRouter(prefix="/api/playlists", tags=["playlists"])


@router.get("", response_model=PlaylistResponse)
def get_playlists(
    session_id: str,
    mood: str,
    language: str | None = Query(None),
    region: str | None = Query(None),
    genre: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query_used, playlists = search_playlists(mood, language, region, genre)

    db.add(Preference(session_id=session_id, language=language, region=region))
    db.commit()

    return {"mood": mood, "query_used": query_used, "playlists": playlists}


@router.post("/open")
def log_open(payload: PlaylistRequestLog, db: Session = Depends(get_db)):
    """Called right before the frontend redirects the user to Spotify, so we
    keep a record of which playlist a given mood actually led to."""
    db.add(PlaylistRequest(**payload.model_dump()))
    db.commit()
    return {"status": "logged"}
