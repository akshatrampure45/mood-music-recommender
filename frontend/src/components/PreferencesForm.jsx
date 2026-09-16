import { LANGUAGES, REGIONS } from '../moods'

export default function PreferencesForm({ prefs, onChange, onSubmit, disabled }) {
  return (
    <form
      className="prefs-form"
      onSubmit={(e) => {
        e.preventDefault()
        onSubmit()
      }}
    >
      <div className="prefs-field">
        <label htmlFor="language">Language</label>
        <select
          id="language"
          value={prefs.language}
          onChange={(e) => onChange({ ...prefs, language: e.target.value })}
        >
          {LANGUAGES.map((l) => (
            <option key={l} value={l === 'Any' ? '' : l}>{l}</option>
          ))}
        </select>
      </div>

      <div className="prefs-field">
        <label htmlFor="region">Region</label>
        <select
          id="region"
          value={prefs.region}
          onChange={(e) => onChange({ ...prefs, region: e.target.value })}
        >
          {REGIONS.map((r) => (
            <option key={r.code} value={r.code}>{r.label}</option>
          ))}
        </select>
      </div>

      <div className="prefs-field">
        <label htmlFor="genre">Genre (optional)</label>
        <input
          id="genre"
          type="text"
          placeholder="e.g. lo-fi, pop, classical"
          value={prefs.genre}
          onChange={(e) => onChange({ ...prefs, genre: e.target.value })}
        />
      </div>

      <button type="submit" className="prefs-submit" disabled={disabled}>
        Find playlists
      </button>
    </form>
  )
}
