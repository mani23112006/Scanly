import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { scanMessage, getErrorMessage } from '../services/api'

function ScanForm() {
  const navigate = useNavigate()

  const [text,    setText]    = useState('')
  const [url,     setUrl]     = useState('')
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState('')
  const [showUrl, setShowUrl] = useState(false)

  const handleScan = async () => {
    if (!text.trim()) {
      setError('Please enter a message to scan.')
      return
    }
    setError('')
    setLoading(true)

    try {
      // ── Uses api.js service function ──────────
      const result = await scanMessage(text, url)
      navigate('/results', { state: { result } })

    } catch (err) {
      setError(getErrorMessage(err))  // clean user-facing message
    } finally {
      setLoading(false)
    }
  }

  const charColor = text.length > 4500
    ? 'text-red-400'
    : text.length > 3000
    ? 'text-yellow-400'
    : 'text-gray-600'



  return (
    <div className="w-full">
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
          className="w-full bg-gray-950 border border-gray-700 rounded-xl
                     text-gray-200 placeholder-gray-600 text-sm px-4 py-3
                     resize-none focus:outline-none focus:border-blue-500
                     focus:ring-1 focus:ring-blue-500 transition-colors"
        />

        {/* Char count */}
        <div className={`text-right text-xs mt-1 ${charColor}`}>
          {text.length} / 5000
        </div>

        {/* URL toggle */}
        <button
          onClick={() => setShowUrl(!showUrl)}
          className="text-xs text-gray-500 hover:text-blue-400 mt-3
                     transition-colors flex items-center gap-1"
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
            className="w-full mt-3 bg-gray-950 border border-gray-700
                       rounded-xl text-gray-200 placeholder-gray-600
                       text-sm px-4 py-3 focus:outline-none
                       focus:border-blue-500 focus:ring-1 focus:ring-blue-500
                       transition-colors"
          />
        )}

        {/* Error */}
        {error && (
          <div className="mt-4 bg-red-900/30 border border-red-800
                          text-red-400 text-sm px-4 py-3 rounded-xl
                          flex items-start gap-2">
            <span className="mt-0.5">⚠</span>
            <span>{error}</span>
          </div>
        )}

        {/* Scan button */}
        <button
          onClick={handleScan}
          disabled={loading || !text.trim()}
          className={`w-full mt-5 py-3.5 rounded-xl font-semibold text-sm
                      transition-all duration-150
            ${loading || !text.trim()
              ? 'bg-gray-700 text-gray-500 cursor-not-allowed opacity-60'
              : 'bg-blue-600 hover:bg-blue-500 active:bg-blue-700 text-white shadow-lg shadow-blue-900/30 hover:-translate-y-0.5 active:translate-y-0'
            }`}
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
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

   
    </div>
  )
}

export default ScanForm