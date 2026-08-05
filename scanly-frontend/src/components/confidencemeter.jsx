// ConfidenceMeter.jsx

export default function ConfidenceMeter({
  confidence,
  modelVersion,
}) {

  // If confidence is not available, don't render anything
  if (confidence === null || confidence === undefined) {
    return null
  }

  // Convert decimal confidence into percentage
  // Example:
  // 0.92 -> 92
  const pct = Math.round(confidence * 100)

  // Decide progress bar color
  const color =
    pct >= 80
      ? 'bg-red-500'
      : pct >= 50
        ? 'bg-yellow-500'
        : 'bg-green-500'

  // Decide confidence label
  const label =
    pct >= 80
      ? 'High scam confidence'
      : pct >= 50
        ? 'Moderate confidence'
        : 'Low scam probability'

  return (

    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5 mb-4">

      {/* ================= Header ================= */}

      <div className="flex items-center justify-between mb-3">

        <div>

          <span className="text-white font-medium text-sm">
            🤖 AI Confidence
          </span>

          <span className="text-gray-600 text-xs ml-2">
            {label}
          </span>

        </div>

        {/* Model Version */}

      {modelVersion && (
  <span className="text-xs text-gray-600 bg-gray-800 px-2 py-0.5 rounded">
    AI Model
  </span>
)}

      </div>

      {/* ================= Progress Bar ================= */}

      <div className="w-full bg-gray-800 rounded-full h-3 overflow-hidden">

        <div
          className={`
            h-3
            rounded-full
            ${color}
            transition-all
            duration-700
            ease-out
          `}
          style={{
            width: `${pct}%`,
          }}
        />

      </div>

      {/* ================= Labels ================= */}

      <div className="flex justify-between mt-1.5">

        <span className="text-xs text-gray-600">
          Safe
        </span>

        <span
          className={`
            text-sm
            font-bold

            ${
              pct >= 80

                ? 'text-red-400'

                : pct >= 50

                  ? 'text-yellow-400'

                  : 'text-green-400'
            }

          `}
        >
          {pct}%
        </span>

        <span className="text-xs text-gray-600">
          Scam
        </span>

      </div>

    </div>

  )
}