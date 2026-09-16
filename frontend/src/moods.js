// Single source of truth for how each detected emotion is represented visually.
// Keep keys aligned with DeepFace's output: angry, disgust, fear, happy, sad, surprise, neutral.
export const MOODS = {
  happy:    { label: 'Happy',    color: '#FFC857', glow: '#FFE1A0' },
  sad:      { label: 'Sad',      color: '#4A6FA5', glow: '#8FB0DE' },
  angry:    { label: 'Angry',    color: '#E14B4B', glow: '#F58C8C' },
  fear:     { label: 'Fearful',  color: '#2E8B8B', glow: '#7BC3C3' },
  surprise: { label: 'Surprised',color: '#C060E0', glow: '#E2A6F5' },
  disgust:  { label: 'Disgusted',color: '#7A8C4A', glow: '#B4C57F' },
  neutral:  { label: 'Neutral',  color: '#8A8F9C', glow: '#C3C7D1' },
}

export const DEFAULT_MOOD = 'neutral'

export const LANGUAGES = [
  'Any', 'English', 'Hindi', 'Punjabi', 'Tamil', 'Telugu', 'Marathi',
  'Spanish', 'Korean', 'Japanese', 'French',
]

export const REGIONS = [
  { code: '', label: 'Any' },
  { code: 'IN', label: 'India' },
  { code: 'US', label: 'United States' },
  { code: 'GB', label: 'United Kingdom' },
  { code: 'KR', label: 'South Korea' },
  { code: 'JP', label: 'Japan' },
  { code: 'ES', label: 'Spain' },
  { code: 'FR', label: 'France' },
]
