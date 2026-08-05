import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// ── Error message helper ─────────────────────────────
export const getErrorMessage = (error) => {
  const status = error.response?.status
  const detail = error.response?.data?.detail || error.response?.data?.error

  if (status === 429) return 'Too many scans. Please wait a minute and try again.'
  if (status === 422) return detail || 'Invalid input. Please check your message.'
  if (status === 413) return 'Image too large. Please use an image under 10MB.'
  if (status === 500) return 'Server error. Please try again in a moment.'
  if (status === 503) return 'Server is starting up. Please wait 30 seconds and retry.'
  if (error.code === 'ECONNABORTED') return 'Request timed out. Image scanning can take up to 60 seconds.'
  if (!error.response) return 'Cannot connect to server. Make sure the backend is running.'

  return detail || 'Something went wrong. Please try again.'
}

// ── POST /scan or /scan/text ─────────────────────────
export const scanMessage = async (text, url = null) => {
  const payload = { text: text.trim() }
  if (url && url.trim()) payload.url = url.trim()
  const response = await api.post('/scan', payload)
  return response.data
}

// ── POST /scan/text (named alias) ────────────────────
export const scanText = async (text, url = null) => {
  const payload = { text: text.trim() }
  if (url && url.trim()) payload.url = url.trim()
  const response = await api.post('/scan/text', payload)
  return response.data
}

// ── POST /scan/url ───────────────────────────────────
export const scanURL = async (url) => {
  const response = await api.post('/scan/url', { url: url.trim() })
  return response.data
}

// ── POST /scan/image ─────────────────────────────────
// Must use FormData — NOT JSON
export const scanImage = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post('/scan/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 60000,  // 60s — OCR + RoBERTa can take a while
  })
  return response.data
}

// ── GET /history ─────────────────────────────────────
export const getHistory = async (limit = 20) => {
  const response = await api.get(`/history?limit=${limit}`)
  return response.data
}

// ── DELETE /history ──────────────────────────────────
export const clearHistory = async () => {
  const response = await api.delete('/history')
  return response.data
}

// ── GET /health ──────────────────────────────────────
export const checkHealth = async () => {
  const response = await api.get('/health')
  return response.data
}

export default api