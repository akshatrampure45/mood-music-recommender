from functools import lru_cache

import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

from app.config import settings
from app.curated_playlists import get_curated

# Base mood -> search vocabulary. Kept short and generic-English on purpose —
# long English phrases here would dominate Spotify's relevance ranking and
# drown out a requested language, which is exactly the bug this fixes.
MOOD_KEYWORDS = {
    "happy": "happy upbeat",
    "sad": "sad emotional",
    "angry": "angry aggressive",
    "fear": "calm soothing",
    "surprise": "energetic party",
    "disgust": "chill lofi",
    "neutral": "chill focus",
}

# Maps a language selection to the term Spotify playlist titles actually use —
# "Hindi" alone under-matches, but "Bollywood" is how most Hindi playlists on
# Spotify are actually titled. Falls back to the raw language name otherwise.
LANGUAGE_LABELS = {
    "hindi": "Bollywood",
    "punjabi": "Punjabi",
    "marathi": "Marathi",
    "tamil": "Tamil",
    "telugu": "Telugu",
    "spanish": "Latin",
    "korean": "K-pop",
    "japanese": "J-pop",
    "french": "French",
    "english": "",  # no regional label needed
}


@lru_cache(maxsize=1)
def _client() -> spotipy.Spotify:
    auth = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
    )
    return spotipy.Spotify(client_credentials_manager=auth)


def _language_markers(language: str | None) -> list[str]:
    """Words that indicate a result actually matches the requested language,
    used to re-rank results toward it after the search comes back."""
    if not language:
        return []
    label = LANGUAGE_LABELS.get(language.lower(), language)
    markers = {language.lower()}
    if label:
        markers.add(label.lower())
    return list(markers)


def build_query(mood: str, language: str | None, genre: str | None) -> str:
    mood_words = MOOD_KEYWORDS.get(mood.lower(), mood)
    parts = []

    if language:
        label = LANGUAGE_LABELS.get(language.lower(), language)
        parts.append(label if label else language)

    parts.append(mood_words)

    if genre:
        parts.append(genre)

    return " ".join(p for p in parts if p)


def search_playlists(mood: str, language: str | None = None, region: str | None = None,
                      genre: str | None = None, limit: int = 8) -> tuple[str, list[dict]]:
    sp = _client()
    query = build_query(mood, language, genre)

    kwargs = {"q": query, "type": "playlist", "limit": limit}
    if region:
        kwargs["market"] = region.upper()

    try:
        results = sp.search(**kwargs)
    except (SpotifyException, Exception):
        # Covers Spotify's "Premium required for app owner" 403s and any
        # other reason the live API is unreachable — keep the app usable
        # with a curated pick instead of failing the request outright.
        return query, get_curated(mood, language)

    items = results.get("playlists", {}).get("items", []) or []
    items = [p for p in items if p]

    markers = _language_markers(language)
    if markers:
        def matches_language(p: dict) -> bool:
            haystack = f"{p.get('name', '')} {p.get('description', '')}".lower()
            return any(m in haystack for m in markers)
        # Stable sort: language-matching playlists float to the top without
        # discarding the rest, so you still get results if nothing matches.
        items.sort(key=lambda p: not matches_language(p))

    playlists = []
    for p in items:
        images = p.get("images") or []
        playlists.append({
            "id": p["id"],
            "name": p["name"],
            "description": p.get("description") or "",
            "image_url": images[0]["url"] if images else None,
            "owner": (p.get("owner") or {}).get("display_name"),
            "track_count": (p.get("tracks") or {}).get("total"),
            "spotify_url": p["external_urls"]["spotify"],
            "spotify_uri": p["uri"],
        })
    return query, playlists
