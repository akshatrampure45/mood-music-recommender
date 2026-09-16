import { useCallback, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import WebcamCapture from '../components/WebcamCapture'
import MoodAura from '../components/MoodAura'
import PreferencesForm from '../components/PreferencesForm'
import ProfileMenu from '../components/ProfileMenu'
import { DEFAULT_MOOD } from '../moods'
import { getSessionId } from '../session'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function HomePage() {
  const navigate = useNavigate()
  const sessionId = getSessionId()

  const [mood, setMood] = useState(DEFAULT_MOOD)
  const [scores, setScores] = useState(null)
  const [confidence, setConfidence] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [trackingPaused, setTrackingPaused] = useState(false)

  const [prefs, setPrefs] = useState({ language: '', region: '', genre: '' })

  const handleFrame = useCallback(
    async (dataUrl) => {
      setAnalyzing(true)
      try {
        const res = await fetch(`${API_BASE}/api/mood/detect`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: sessionId, image: dataUrl }),
        })
        if (!res.ok) throw new Error('detect failed')
        const data = await res.json()
        setMood(data.mood)
        setConfidence(data.confidence)
        setScores(data.all_scores)
      } catch (err) {
        // transient failures (e.g. no face in frame) are expected — stay on last known mood
      } finally {
        setAnalyzing(false)
      }
    },
    [sessionId]
  )

  const handleFindPlaylists = useCallback(() => {
    navigate('/results', { state: { mood, prefs } })
  }, [navigate, mood, prefs])

  return (
    <div className="page">
      <ProfileMenu />

      <header className="hero">
        <span className="eyebrow">Live mood detection</span>
        <h1>Auris</h1>
        <p className="tagline">Your expression picks the playlist.</p>
      </header>

      <section className="capture-section">
        <div className="aura-stage">
          <MoodAura mood={mood} scores={scores} confidence={confidence} analyzing={analyzing} />
          <div className="webcam-inset">
            <WebcamCapture onFrame={handleFrame} active={!trackingPaused} />
          </div>
        </div>
        <button className="pause-btn" onClick={() => setTrackingPaused((p) => !p)}>
          {trackingPaused ? 'Resume tracking' : 'Pause tracking'}
        </button>
      </section>

      <section className="prefs-section">
        <h2>Refine the match</h2>
        <PreferencesForm prefs={prefs} onChange={setPrefs} onSubmit={handleFindPlaylists} disabled={false} />
      </section>
    </div>
  )
}
