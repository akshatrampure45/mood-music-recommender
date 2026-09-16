from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class MoodResult(BaseModel):
    mood: str
    confidence: float
    all_scores: dict


class PlaylistItem(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    owner: Optional[str] = None
    track_count: Optional[int] = None
    spotify_url: str          # https://open.spotify.com/playlist/<id>  (always works, web + app if installed)
    spotify_uri: str          # spotify:playlist:<id>                    (direct app deep link)


class PlaylistResponse(BaseModel):
    mood: str
    query_used: str
    playlists: List[PlaylistItem]


class PlaylistRequestLog(BaseModel):
    session_id: str
    mood: str
    language: Optional[str] = None
    region: Optional[str] = None
    playlist_id: str
    playlist_name: str
    spotify_url: str
