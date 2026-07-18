import axios from 'axios'

// ── Base URL from environment variable ─────────────
// Development:  http://localhost:8000
// Production:   your Render URL (set on Day 19)
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ── Axios instance with shared config ──────────────
// All API calls share this base URL, timeout, headers
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,    // 30 seconds (ML inference can be slow)
  headers: {
    'Content-Type': 'application/json',
  }
})

// ── Request interceptor ─────────────────────────────
// Runs before every request — good place for auth tokens later
api.interceptors.request.use(
  (config) => {
    // Future: add auth token here
    // config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => Promise.reject(error)
)

// ── Response interceptor ────────────────────────────
// Runs after every response — centralised error logging
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Log all errors in one place
    console.error('[API Error]', {
      url:    error.config?.url,
      status: error.response?.status,
      data:   error.response?.data,
    })
    return Promise.reject(error)
  }
)

// ── Error message helper ────────────────────────────
// Converts axios errors into clean user-facing strings
export const getErrorMessage = (error) => {
  if (error.response) {
    // Server responded with error status
    const status = error.response.status
    const detail = error.response.data?.detail

    if (status === 422) return 'Invalid input. Please check your message and try again.'
    if (status === 500) return 'Server error. Please try again in a moment.'
    if (detail)         return `Error: ${detail}`
    return `Request failed with status ${status}`

  } else if (error.request) {
    // Request made but no response — server unreachable
    return 'Cannot reach the backend server. Make sure it is running on port 8000.'

  } else {
    return 'Something went wrong. Please try again.'
  }
}

// ══════════════════════════════════════════════════
// API FUNCTIONS
// ══════════════════════════════════════════════════

// ── POST /scan ──────────────────────────────────────
// Send a message for scanning, get risk analysis back
export const scanMessage = async (text, url = null) => {
  const payload = { text: text.trim() }
  if (url && url.trim()) payload.url = url.trim()

  const response = await api.post('/scan', payload)
  return response.data
}

// ── GET /history ────────────────────────────────────
// Fetch past scan results from MongoDB
export const getHistory = async (limit = 50) => {
  const response = await api.get(`/history?limit=${limit}`)
  return response.data   // { status, count, scans: [...] }
}

// ── DELETE /history ─────────────────────────────────
// Clear all scan history
export const clearHistory = async () => {
  const response = await api.delete('/history')
  return response.data
}

// ── GET /health ─────────────────────────────────────
// Check if the backend is reachable
export const checkHealth = async () => {
  const response = await api.get('/health')
  return response.data
}

export default api