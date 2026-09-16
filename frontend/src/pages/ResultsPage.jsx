import { useCallback, useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import PlaylistGrid from '../components/PlaylistGrid'
import ProfileMenu from '../components/ProfileMenu'
import { MOODS } from '../moods'
import { getSessionId } from '../session'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function ResultsPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const sessionId = getSessionId()

  const state = location.state || {}
  const mood = state.mood
  const prefs = state.prefs || {}

  const [playlists, setPlaylists] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchPlaylists = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams({
        session_id: sessionId,
        mood,
        ...(prefs.language ? { language: prefs.language } : {}),
        ...(prefs.region ? { region: prefs.region } : {}),
        ...(prefs.genre ? { genre: prefs.genre } : {}),
      })
      const res = await fetch(`${API_BASE}/api/playlists?${params.toString()}`)
      if (!res.ok) throw new Error('playlist search failed')
      const data = await res.json()
      setPlaylists(data.playlists)
    } catch (err) {
      setError('Could not reach Spotify right now. Try again in a moment.')
    } finally {
      setLoading(false)
    }
  }, [sessionId, mood, prefs.language, prefs.region, prefs.genre])

  useEffect(() => {
    if (!mood) {
      navigate('/', { replace: true })
      return
    }
    fetchPlaylists()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mood])

  const openPlaylist = useCallback(
    (p) => {
      fetch(`${API_BASE}/api/playlists/open`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          mood,
          language: prefs.language || null,
          region: prefs.region || null,
          playlist_id: p.id,
          playlist_name: p.name,
          spotify_url: p.spotify_url,
        }),
      }).catch(() => {})

      const start = Date.now()
      window.location.href = p.spotify_uri // opens the Spotify app if installed
      setTimeout(() => {
        if (Date.now() - start < 2000) window.open(p.spotify_url, '_blank') // web fallback
      }, 1200)
    },
    [sessionId, mood, prefs]
  )

  if (!mood) return null

  const moodInfo = MOODS[mood] || MOODS.neutral

  return (
    <div className="results-page">
      <ProfileMenu />
      <div className="results-inner">
        <header className="hero results-hero">
          <button className="back-link" onClick={() => navigate('/')}>
            ← Back
          </button>
          <span className="eyebrow">Matched to your mood</span>
          <h1 style={{ color: moodInfo.color }}>{moodInfo.label}</h1>
          <p className="tagline">
            {prefs.language ? `${prefs.language} · ` : ''}
            {prefs.region ? `${prefs.region} · ` : ''}
            Playlists picked for right now
          </p>
        </header>

        <section className="results-section results-section--page">
          {loading && <p className="status-text">Searching Spotify…</p>}
          {error && <p className="status-text error">{error}</p>}
          {!loading && !error && playlists.length === 0 && (
            <p className="status-text">No playlists found — try a different language or region.</p>
          )}
          <PlaylistGrid playlists={playlists} onOpen={openPlaylist} />
        </section>
      </div>
    </div>
  )
}
