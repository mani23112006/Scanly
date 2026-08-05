// OCRPreview.jsx

import { useState } from 'react'

export default function OCRPreview({
  extractedText,
  ocrConfidence,
  ocrLines,
  ocrWarning,
}) {

  // Controls whether full OCR text is shown
  const [expanded, setExpanded] = useState(false)

  // If OCR extracted nothing, don't render the card
  if (!extractedText) {
    return null
  }

  // Show only first 150 characters initially
  const preview =
    extractedText.length > 150
      ? extractedText.slice(0, 150) + '...'
      : extractedText

  // Convert confidence from decimal to percentage
  const confPct = Math.round((ocrConfidence || 0) * 100)

  // Decide confidence color
  const confColor =
    confPct >= 70
      ? 'text-green-400'
      : confPct >= 40
        ? 'text-yellow-400'
        : 'text-red-400'

  return (

    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5 mb-4">

      {/* ================= Header ================= */}

      <div className="flex items-center justify-between mb-3">

        <span className="text-white font-medium text-sm">
          📷 OCR Extracted Text
        </span>

        <div className="flex items-center gap-3 text-xs">

          {/* Number of OCR lines */}

          {ocrLines && (

            <span className="text-gray-500">
              {ocrLines} lines
            </span>

          )}

          {/* OCR Confidence */}

          <span
            className={`
              font-mono
              font-medium
              ${confColor}
            `}
          >
            {confPct}% OCR confidence
          </span>

        </div>

      </div>

      {/* ================= Warning ================= */}

      {ocrWarning && (

        <div className="bg-yellow-900/20 border border-yellow-800/50 text-yellow-400 text-xs px-3 py-2 rounded-lg mb-3">

          ⚠ {ocrWarning}

        </div>

      )}

      {/* ================= OCR Text ================= */}

      <div className="bg-gray-950 rounded-xl p-3 border border-gray-800">

        <p className="text-gray-400 text-xs leading-relaxed font-mono">

          {expanded ? extractedText : preview}

        </p>

      </div>

      {/* ================= Expand / Collapse ================= */}

      {extractedText.length > 150 && (

        <button

          onClick={() => setExpanded(!expanded)}

          className="text-xs text-blue-400 hover:text-blue-300 mt-2 transition-colors"

        >

          {expanded
            ? '↑ Show less'
            : '↓ Show full text'}

        </button>

      )}

    </div>

  )
}