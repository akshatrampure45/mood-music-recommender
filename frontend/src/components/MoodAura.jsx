import { MOODS } from '../moods'

/**
 * The aura is the page's signature element: a ring of light around the
 * webcam feed that behaves like a mood ring. Its dominant color follows
 * the detected emotion, and the conic-gradient stops are weighted by the
 * secondary emotion scores, so a "70% happy / 20% surprise" frame renders
 * as gold with a violet edge instead of snapping to a flat color block.
 */
export default function MoodAura({ mood, scores, confidence, analyzing }) {
  const current = MOODS[mood] || MOODS.neutral
  const entries = scores
    ? Object.entries(scores).sort((a, b) => b[1] - a[1]).slice(0, 3)
    : [[mood, 100]]

  const gradientStops = entries
    .map(([m, v], i) => `${(MOODS[m] || MOODS.neutral).color} ${i === 0 ? 0 : ''}`)
    .join(', ')

  const ringStyle = {
    '--aura-color': current.color,
    '--aura-glow': current.glow,
    background: `conic-gradient(from 0deg, ${entries
      .map(([m]) => (MOODS[m] || MOODS.neutral).color)
      .join(', ')}, ${current.color})`,
  }

  return (
    <div className="aura" data-analyzing={analyzing}>
      <div className="aura-ring" style={ringStyle} />
      <div className="aura-inner" />
      <div className="aura-label-block">
        <span className="aura-mood" style={{ color: current.color }}>
          {current.label}
        </span>
        {confidence != null && (
          <span className="aura-confidence">{Math.round(confidence * 100)}% confidence</span>
        )}
      </div>
    </div>
  )
}
