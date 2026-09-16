"""
A small hand-picked set of real, official Spotify playlists — one or more
per mood, plus multiple per commonly-requested regional language. Used as a
fallback when the live search API is unreachable — most notably Spotify's
Feb 2026 policy that blocks *all* Development Mode API calls (including
search) whenever the app owner's Premium subscription lapses. This fallback
needs no API access at all, so it keeps working regardless of that
subscription status.

Thumbnails are fetched via Spotify's public oEmbed endpoint
(open.spotify.com/oembed), which needs no auth/API key at all — it's a
different, unrestricted surface from the Web API search endpoint that's
blocked, so it works even while that's down.

IDs verified against open.spotify.com as of Aug 2026 — all owned by the
official "Spotify" account.
"""
import requests

CURATED_PLAYLISTS = {
    "happy":    {"id": "37i9dQZF1DXdPec7aLTmlC", "name": "Happy Hits!"},
    "sad":      {"id": "37i9dQZF1DX7qK8ma5wgG1", "name": "Sad Songs"},
    "angry":    {"id": "37i9dQZF1DX76Wlfdnj7AP", "name": "Beast Mode"},
    "fear":     {"id": "37i9dQZF1DX4sWSpwq3LiO", "name": "Peaceful Piano"},
    "surprise": {"id": "37i9dQZF1DXaXB8fQg7xif", "name": "Dance Party"},
    "disgust":  {"id": "37i9dQZF1DWWQRwui0ExPn", "name": "lofi beats"},
    "neutral":  {"id": "37i9dQZF1DWZeKCadgRdKQ", "name": "Deep Focus"},
}

# When a language is picked, these take priority over the mood pick above —
# the fallback can't cross-match language x mood without live search, so it
# leads with "at least the right language" over "at least the right mood".
CURATED_LANGUAGE_PLAYLISTS = {
    "hindi": [
        {"id": "37i9dQZF1DWXtlo6ENS92N", "name": "Bollywood Central"},
        {"id": "37i9dQZF1DX0XUfTFmNBRM", "name": "Hot Hits Hindi"},
        {"id": "37i9dQZF1DWSwxyU5zGZYe", "name": "Bollywood Acoustic"},
    ],
    "punjabi": [
        {"id": "37i9dQZF1DX5cZuAHLNjGz", "name": "Punjabi 101"},
        {"id": "37i9dQZF1DWXVJK4aT7pmk", "name": "Hot Hits Punjabi"},
    ],
    "marathi": [
        {"id": "37i9dQZF1DX8BKauvV4z7b", "name": "Marathi Evergreen"},
    ],
    "tamil": [
        {"id": "37i9dQZF1DX0TyiNWW7uUQ", "name": "Kollywood Cream"},
    ],
    "telugu": [
        {"id": "37i9dQZF1DX6XE7HRLM75P", "name": "Hot Hits Telugu"},
    ],
}

# Used to top up the list to 2-3 cards when a language/mood only has one
# curated pick of its own.
UNIVERSAL_PICK = {"id": "37i9dQZF1DXcBWIGoYBM5M", "name": "Today's Top Hits"}


def _oembed_thumbnail(playlist_id: str) -> str | None:
    """Fetch a playlist's cover art via Spotify's public oEmbed endpoint —
    no API key needed, so this works independently of the Web API's auth
    status."""
    try:
        r = requests.get(
            "https://open.spotify.com/oembed",
            params={"url": f"https://open.spotify.com/playlist/{playlist_id}"},
            timeout=3,
        )
        if r.ok:
            return r.json().get("thumbnail_url")
    except Exception:
        pass
    return None


def get_curated(mood: str, language: str | None = None) -> list[dict]:
    picks: list[dict] = []

    if language and language.lower() in CURATED_LANGUAGE_PLAYLISTS:
        picks.extend(CURATED_LANGUAGE_PLAYLISTS[language.lower()])

    mood_entry = CURATED_PLAYLISTS.get(mood.lower(), CURATED_PLAYLISTS["neutral"])
    if mood_entry["id"] not in [p["id"] for p in picks]:
        picks.append(mood_entry)

    if len(picks) < 2 and UNIVERSAL_PICK["id"] not in [p["id"] for p in picks]:
        picks.append(UNIVERSAL_PICK)

    picks = picks[:3]
    note = "Curated pick — live Spotify search is temporarily unavailable."

    return [{
        "id": entry["id"],
        "name": entry["name"],
        "description": note,
        "image_url": _oembed_thumbnail(entry["id"]),
        "owner": "Spotify",
        "track_count": None,
        "spotify_url": f"https://open.spotify.com/playlist/{entry['id']}",
        "spotify_uri": f"spotify:playlist:{entry['id']}",
    } for entry in picks]
