// ImageUpload.jsx

// React Hooks
import { useState, useRef, useCallback } from 'react'

// React Router
import { useNavigate } from 'react-router-dom'

// API
import { scanImage, getErrorMessage } from '../services/api'

// ===============================================
// Allowed image types
// ===============================================
const ALLOWED = [
  'image/jpeg',
  'image/jpg',
  'image/png',
  'image/webp',
  'image/gif',
  'image/bmp',
]

// Maximum file size
const MAX_MB = 10

export default function ImageUpload() {

  // Navigate to Results page
  const navigate = useNavigate()

  // Hidden file input reference
  const inputRef = useRef(null)

  // Selected image
  const [file, setFile] = useState(null)

  // Preview URL
  const [preview, setPreview] = useState(null)

  // Loading state
  const [loading, setLoading] = useState(false)

  // Loading message
  const [loadingMsg, setLoadingMsg] = useState('')

  // Error message
  const [error, setError] = useState('')

  // Dragging state
  const [isDragging, setIsDragging] = useState(false)

  // ===================================================
  // Validate selected image
  // ===================================================
  const validateAndSet = (f) => {

    setError('')

    // Check image type
    if (!ALLOWED.includes(f.type)) {
      setError(
        `Unsupported file type: ${f.type}. Use JPG, PNG, or WEBP.`
      )
      return
    }

    // Check image size
    if (f.size > MAX_MB * 1024 * 1024) {
      setError(
        `File too large (${(f.size / 1024 / 1024).toFixed(1)}MB). Max: ${MAX_MB}MB`
      )
      return
    }

    // Store image
    setFile(f)

    // Generate preview
    setPreview(URL.createObjectURL(f))
  }

  // ===================================================
  // Drag & Drop
  // ===================================================

  const onDragOver = useCallback((e) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const onDragLeave = useCallback((e) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const onDrop = useCallback((e) => {

    e.preventDefault()

    setIsDragging(false)

    const f = e.dataTransfer.files[0]

    if (f) {
      validateAndSet(f)
    }

  }, [])

  // ===================================================
  // File picker
  // ===================================================

  const onFileChange = (e) => {

    const f = e.target.files[0]

    if (f) {
      validateAndSet(f)
    }

  }

  // ===================================================
  // Remove image
  // ===================================================

  const clearFile = () => {

    setFile(null)

    setPreview(null)

    setError('')

    if (inputRef.current) {
      inputRef.current.value = ''
    }

  }

  // ===================================================
  // Scan Image
  // ===================================================

  const handleScan = async () => {

    if (!file) return

    setError('')

    setLoading(true)

    // Fake progress messages for better UX

    setLoadingMsg('Reading image...')

    await new Promise((r) => setTimeout(r, 500))

    setLoadingMsg('Extracting text via OCR...')

    await new Promise((r) => setTimeout(r, 800))

    setLoadingMsg('Analysing with AI...')

    try {

      // Upload image
      const result = await scanImage(file)

      // Navigate to Results page
      navigate('/results', {
        state: {
          result,
          scanType: 'image',
        },
      })

    }

    catch (err) {

      setError(getErrorMessage(err))

    }

    finally {

      setLoading(false)

      setLoadingMsg('')

    }

  }

  // ===================================================
  // UI
  // ===================================================

  return (

    <div className="w-full">

      {/* ================= Drop Zone ================= */}

      <div

        onDragOver={onDragOver}

        onDragLeave={onDragLeave}

        onDrop={onDrop}

        onClick={() => !file && inputRef.current?.click()}

        className={`
          relative
          bg-gray-900
          border-2
          border-dashed
          rounded-2xl
          transition-all
          cursor-pointer

          ${
            isDragging

              ? 'border-blue-500 bg-blue-900/10'

              : file

                ? 'border-gray-700 cursor-default'

                : 'border-gray-700 hover:border-gray-500'
          }

        `}
      >

        {/* Hidden file picker */}

        <input

          ref={inputRef}

          type="file"

          accept={ALLOWED.join(',')}

          onChange={onFileChange}

          className="hidden"

        />

        {/* No file selected */}

        {!file && (

          <div className="py-12 px-6 text-center">

            <div className="text-4xl mb-3">

              {isDragging ? '📂' : '🖼️'}

            </div>

            <p className="text-gray-300 font-medium mb-1">

              {isDragging
                ? 'Drop your screenshot here'
                : 'Drop screenshot here'}

            </p>

            <p className="text-gray-600 text-sm mb-4">

              or click to browse

            </p>

            <p className="text-gray-700 text-xs">

              JPG · PNG · WEBP · BMP · GIF · max {MAX_MB}MB

            </p>

          </div>

        )}

        {/* ================= Preview ================= */}

        {file && (

          <div className="p-4">

            <div className="flex gap-4 items-start">

              {/* Thumbnail */}

              <img

                src={preview}

                alt="preview"

                className="
                  w-24
                  h-24
                  object-cover
                  rounded-xl
                  border
                  border-gray-700
                  flex-shrink-0
                "

              />

              {/* File Information */}

              <div className="flex-1 min-w-0">

                <p className="text-gray-200 text-sm font-medium truncate">

                  {file.name}

                </p>

                <p className="text-gray-500 text-xs mt-1">

                  {(file.size / 1024).toFixed(0)} KB · {file.type}

                </p>

                <div className="flex gap-2 mt-3">

                  <span className="bg-green-900/30 border border-green-800 text-green-400 text-xs px-2 py-1 rounded">

                    ✓ Ready to scan

                  </span>

                  <button

                    onClick={clearFile}

                    className="text-xs text-gray-600 hover:text-red-400 transition-colors"

                  >

                    Remove

                  </button>

                </div>

              </div>

            </div>

          </div>

        )}

        {/* ================= Loading Overlay ================= */}

        {loading && (

          <div className="absolute inset-0 bg-gray-900/90 rounded-2xl flex flex-col items-center justify-center">

            <svg
              className="animate-spin h-8 w-8 text-blue-400 mb-3"
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
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              />

            </svg>

            <p className="text-blue-400 font-medium text-sm">

              {loadingMsg}

            </p>

            <p className="text-gray-600 text-xs mt-1">

              OCR + AI analysis — may take 5–15s

            </p>

          </div>

        )}

      </div>

      {/* ================= Error ================= */}

      {error && (

        <div className="mt-3 bg-red-900/30 border border-red-800 text-red-400 text-sm px-4 py-3 rounded-xl">

          ⚠ {error}

        </div>

      )}

      {/* ================= Scan Button ================= */}

      <button

        onClick={handleScan}

        disabled={loading || !file}

        className={`
          w-full
          mt-4
          py-3.5
          rounded-xl
          font-semibold
          text-sm
          transition-all

          ${
            loading || !file

              ? 'bg-gray-700 text-gray-500 cursor-not-allowed opacity-60'

              : 'bg-blue-600 hover:bg-blue-500 text-white hover:-translate-y-0.5'
          }

        `}

      >

        {loading
          ? loadingMsg || 'Scanning...'
          : '🔍 Scan Screenshot'}

      </button>

      {/* ================= Tip ================= */}

      <p className="text-xs text-gray-600 text-center mt-3">

        Works with WhatsApp · SMS · Email · UPI · Bank alerts

      </p>

    </div>

  )
}