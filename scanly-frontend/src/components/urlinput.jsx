// URLInput.jsx

// React hook
import { useState } from 'react'

// Used to navigate to the Results page
import { useNavigate } from 'react-router-dom'

// API function and error helper
import { scanURL, getErrorMessage } from '../services/api'

export default function URLInput() {

  // Navigate between pages
  const navigate = useNavigate()

  // URL entered by the user
  const [url, setUrl] = useState('')

  // Loading state while backend processes the URL
  const [loading, setLoading] = useState(false)

  // Error message shown on screen
  const [error, setError] = useState('')

  // =========================
  // Scan URL
  // =========================
  const handleScan = async () => {

    // Remove extra spaces
    const trimmed = url.trim()

    // Empty input validation
    if (!trimmed) {
      setError('Please enter a URL.')
      return
    }

    // Basic URL validation
    if (!trimmed.includes('.')) {
      setError(
        'Please enter a valid URL (e.g. https://suspicious-link.xyz)'
      )
      return
    }

    setError('')
    setLoading(true)

    try {

      // Send URL to backend
      const result = await scanURL(trimmed)

      // Go to Results page
      navigate('/results', {
        state: {
          result,
          scanType: 'url',
        },
      })

    } catch (err) {

      // Show readable error
      setError(getErrorMessage(err))

    } finally {

      // Stop loading
      setLoading(false)

    }
  }

  // =========================
  // Sample URLs
  // =========================
  const SAMPLE_URLS = [
    {
      label: '🔴 IP URL',
      url: 'http://192.168.1.1/bank/verify',
    },
    {
      label: '🔴 Shortener',
      url: 'http://bit.ly/free-prize-claim',
    },
    {
      label: '🟡 Suspicious',
      url: 'http://secure-login.bank.verify.xyz/account',
    },
    {
      label: '🟢 Safe',
      url: 'https://google.com',
    },
  ]

  return (

    <div className="w-full">

      {/* ================= Card ================= */}

      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">

        {/* Label */}
        <label className="block text-sm font-medium text-gray-400 mb-2">
          Paste a suspicious URL
        </label>

        {/* URL Input */}
        <input
          type="text"
          value={url}

          onChange={(e) => {
            setUrl(e.target.value)
            setError('')
          }}

          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleScan()
            }
          }}

          placeholder="https://suspicious-link.xyz/verify/account"

          className="
            w-full
            bg-gray-950
            border
            border-gray-700
            rounded-xl
            text-gray-200
            placeholder-gray-600
            text-sm
            px-4
            py-3
            focus:outline-none
            focus:border-blue-500
            focus:ring-1
            focus:ring-blue-500
            transition-colors
          "
        />

        {/* Information */}
        <p className="text-xs text-gray-600 mt-2">
          Checks: IP address, HTTP vs HTTPS, TLD, subdomains,
          URL shorteners
        </p>

        {/* Error */}
        {error && (

          <div className="mt-3 bg-red-900/30 border border-red-800 text-red-400 text-sm px-4 py-3 rounded-xl">
            ⚠ {error}
          </div>

        )}

        {/* Scan Button */}

        <button
          onClick={handleScan}
          disabled={loading || !url.trim()}

          className={`
            w-full
            mt-4
            py-3.5
            rounded-xl
            font-semibold
            text-sm
            transition-all

            ${
              loading || !url.trim()

                ? 'bg-gray-700 text-gray-500 cursor-not-allowed opacity-60'

                : 'bg-blue-600 hover:bg-blue-500 text-white hover:-translate-y-0.5'
            }
          `}
        >

          {loading ? (

            <span className="flex items-center justify-center gap-2">

              {/* Spinner */}

              <svg
                className="animate-spin h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
              >

                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />

                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373
                  0 0 5.373 0 12h4z"
                />

              </svg>

              Analysing URL...

            </span>

          ) : (

            '🔗 Analyse URL'

          )}

        </button>

      </div>

      {/* ================= Sample URLs ================= */}

      <div className="mt-3">

        <p className="text-xs text-gray-600 mb-2">
          Try a sample:
        </p>

        <div className="flex gap-2 flex-wrap">

          {SAMPLE_URLS.map((sample) => (

            <button
              key={sample.label}

              onClick={() => setUrl(sample.url)}

              className="
                text-xs
                bg-gray-900
                border
                border-gray-700
                text-gray-400
                hover:text-white
                px-3
                py-1.5
                rounded-lg
                transition-colors
              "
            >

              {sample.label}

            </button>

          ))}

        </div>

      </div>

    </div>

  )
}