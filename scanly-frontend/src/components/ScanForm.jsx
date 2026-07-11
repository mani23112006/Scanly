import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function ScanForm() {
  const navigate = useNavigate()

  // ── State ───────────────────────────────────────
  const [text,    setText]    = useState('')
  const [url,     setUrl]     = useState('')
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState('')
  const [showUrl, setShowUrl] = useState(false)

  // ── Submit handler ──────────────────────────────
  const handleScan = async () => {
    // Validate — don't send empty input
    if (!text.trim()) {
      setError('Please enter a message to scan.')
      return
    }

    setError('')
    setLoading(true)

    try {
      const payload = { text: text.trim() }
      if (url.trim()) payload.url = url.trim()

      const response = await axios.post(`${API_URL}/scan`, payload)

      // Pass result to Results page via router state
      navigate('/results', { state: { result: response.data } })

    } catch (err) {
      console.error('Scan failed:', err)
      if (err.response) {
        setError(`Server error: ${err.response.data.detail || 'Something went wrong'}`)
      } else if (err.request) {
        setError('Cannot reach the backend. Make sure it is running on port 8000.')
      } else {
        setError('Something went wrong. Please try again.')
      }
       } finally {
      setLoading(false)
    }
  }

  // ── Character count color ───────────────────────
  const charColor = text.length > 4500
    ? 'text-red-400'
    : text.length > 3000
    ? 'text-yellow-400'
    : 'text-gray-600'

  return (
    <div className="w-full max-w-2xl">

      {/* Main card */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-xl">

        {/* Textarea */}
        <label className="block text-sm font-medium text-gray-400 mb-2">
          Paste your message
        </label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste any SMS, WhatsApp message, email, or suspicious text here..."
          rows={6}
          maxLength={5000}
          className="w-full bg-gray-950 border border-gray-700 rounded-xl text-gray-200
                     placeholder-gray-600 text-sm px-4 py-3 resize-none
                     focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500
                     transition-colors"
        />
          {/* Char count */}
        <div className={`text-right text-xs mt-1 ${charColor}`}>
          {text.length} / 5000
        </div>

        {/* Optional URL toggle */}
        <button
          onClick={() => setShowUrl(!showUrl)}
          className="text-xs text-gray-500 hover:text-blue-400 mt-3 transition-colors flex items-center gap-1"
        >
          {showUrl ? '− Hide' : '+ Add'} suspicious URL (optional)
        </button>

        {/* URL input */}
        {showUrl && (
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://suspicious-link.xyz/verify"
            className="w-full mt-3 bg-gray-950 border border-gray-700 rounded-xl
                       text-gray-200 placeholder-gray-600 text-sm px-4 py-3
                       focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500
                       transition-colors"
          />
        )}
  {/* Error message */}
        {error && (
          <div className="mt-4 bg-red-900/30 border border-red-800 text-red-400
                          text-sm px-4 py-3 rounded-xl">
            ⚠ {error}
          </div>
        )}

        {/* Scan button */}
        <button
          onClick={handleScan}
          disabled={loading || !text.trim()}
          className={`w-full mt-5 py-3.5 rounded-xl font-semibold text-sm transition-all
            ${loading || !text.trim()
              ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/30 hover:shadow-blue-800/40'
            }`}
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              {/* Spinner */}
              <svg className="animate-spin h-4 w-4 text-gray-400"
                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10"
                  stroke="currentColor" strokeWidth="4"/>
                <path className="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              Scanning...
            </span>
          ) : (
            '🔍 Scan Now'
          )}
        </button>
        
      </div>

      {/* Sample messages for quick testing */}
      <div className="mt-4">
        <p className="text-xs text-gray-600 mb-2">Try a sample:</p>
        <div className="flex gap-2 flex-wrap">
          {[
            { label: '🔴 Scam SMS', text: 'Your bank account is blocked. Share OTP 4829 urgently to verify account. Click http://bit.ly/verify-now' },
            { label: '🟢 Safe SMS', text: 'Hey! Are we still on for dinner at 7pm tonight? Let me know if you need the address.' },
            { label: '🟡 Suspicious', text: 'Congratulations! You have been selected for a special offer. Click here to claim your prize.' }
          ].map((sample) => (
            <button
              key={sample.label}
              onClick={() => setText(sample.text)}
              className="text-xs bg-gray-900 border border-gray-700 text-gray-400
                         hover:text-white hover:border-gray-600 px-3 py-1.5 rounded-lg
                         transition-colors"
            >
              {sample.label}
            </button>
          ))}
        </div>
      </div>

    </div>
  )
}

export default ScanForm