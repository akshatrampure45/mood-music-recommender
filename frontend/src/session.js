const KEY = 'auris_session_id'

export function getSessionId() {
  let id = localStorage.getItem(KEY)
  if (!id) {
    id = crypto.randomUUID?.() || `${Date.now()}-${Math.random()}`
    localStorage.setItem(KEY, id)
  }
  return id
}
