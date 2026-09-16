from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.emotion_detector import warmup
from app.routers import auth, mood, playlist


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # safe no-op if init_db.sql was already run
    warmup()  # load the emotion model once at startup, not on the first request
    yield


app = FastAPI(title="Mood Music Recommender API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(mood.router)
app.include_router(playlist.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
