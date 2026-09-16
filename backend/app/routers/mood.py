from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.emotion_detector import detect_mood
from app.models import MoodLog
from app.schemas import MoodResult

router = APIRouter(prefix="/api/mood", tags=["mood"])


class MoodRequest(BaseModel):
    session_id: str
    image: str  # data URL from <video>/<canvas> capture, e.g. "data:image/jpeg;base64,..."


@router.post("/detect", response_model=MoodResult)
def detect(payload: MoodRequest, db: Session = Depends(get_db)):
    result = detect_mood(payload.image)

    db.add(MoodLog(
        session_id=payload.session_id,
        mood=result["mood"],
        confidence=result["confidence"],
    ))
    db.commit()

    return result
