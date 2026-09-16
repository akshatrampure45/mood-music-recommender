const FALLBACK_COVER =
  'data:image/svg+xml;utf8,' +
  encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><rect width="300" height="300" fill="#1B1F29"/></svg>`
  )

export default function PlaylistGrid({ playlists, onOpen }) {
  if (!playlists || playlists.length === 0) return null

  return (
    <div className="playlist-grid">
      {playlists.map((p) => (
        <article className="playlist-card" key={p.id}>
          <img
            className="playlist-cover"
            src={p.image_url || FALLBACK_COVER}
            alt={p.name}
            loading="lazy"
          />
          <div className="playlist-body">
            <h3>{p.name}</h3>
            <p className="playlist-meta">
              {p.owner ? `by ${p.owner}` : ''}
              {p.track_count != null ? ` · ${p.track_count} tracks` : ''}
            </p>
            <button className="playlist-open" onClick={() => onOpen(p)}>
              Open in Spotify ↗
            </button>
          </div>
        </article>
      ))}
    </div>
  )
}
