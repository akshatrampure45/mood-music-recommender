from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MoodLog(Base):
    __tablename__ = "mood_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True, nullable=False)
    mood = Column(String(32), nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True, nullable=False)
    language = Column(String(64))
    region = Column(String(8))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PlaylistRequest(Base):
    __tablename__ = "playlist_requests"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True, nullable=False)
    mood = Column(String(32), nullable=False)
    language = Column(String(64))
    region = Column(String(8))
    playlist_id = Column(String(64))
    playlist_name = Column(String(255))
    spotify_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
