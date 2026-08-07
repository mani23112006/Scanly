export default function ConfidenceMeter({
  confidence,
  modelVersion,
}) {

  if (confidence === null || confidence === undefined) {
    return null
  }

  // confidence can be 0.19 or 19
  const pct =
    confidence <= 1
      ? Math.round(confidence * 100)
      : Math.round(confidence)

  // Progress bar color
  const color =
    pct >= 70
      ? 'bg-red-500'
      : pct >= 31
        ? 'bg-yellow-500'
        : 'bg-green-500'

  // Risk label
  const label =
    pct >= 70
      ? 'High scam risk'
      : pct >= 31
        ? 'Medium scam risk'
        : 'Low scam risk'

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5 mb-4">

      {/* Header */}
      <div className="flex items-center justify-between mb-3">

        <div>
          <span className="text-white font-medium text-sm">
            🤖 AI Risk Score
          </span>

          <span className="text-gray-500 text-xs ml-2">
            {label}
          </span>
        </div>

        {modelVersion && (
          <span className="text-xs text-gray-600 bg-gray-800 px-2 py-0.5 rounded">
            AI Model 
          </span>
        )}

      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-800 rounded-full h-3 overflow-hidden">

        <div
          className={`h-3 rounded-full ${color} transition-all duration-700`}
          style={{
            width: `${pct}%`,
          }}
        />

      </div>

      {/* Labels */}
      <div className="flex justify-between mt-1.5">

        <span className="text-xs text-gray-600">
          Safe
        </span>

        <span
          className={`text-sm font-bold ${
            pct >= 70
              ? 'text-red-400'
              : pct >= 31
                ? 'text-yellow-400'
                : 'text-green-400'
          }`}
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