/**
 * GeminiInsights.jsx
 *
 * Renders Gemini's human-readable explanation of an already-completed
 * Scanly scan result. Gemini never performs detection — this component
 * only displays the four fields the backend returns under `gemini`:
 * summary, why_flagged, safety_tips, recommended_action.
 *
 * If `gemini` is missing or null (e.g. Gemini failed and no fallback
 * was attached), the component renders nothing so it never breaks
 * the Results page.
 */

function GeminiInsights({ gemini }) {
  if (!gemini) return null

  const {
    summary,
    why_flagged = [],
    safety_tips = [],
    recommended_action,
  } = gemini

  const actionColor =
    recommended_action?.toLowerCase().includes('do not') ||
    recommended_action?.toLowerCase().includes('block') ||
    recommended_action?.toLowerCase().includes('delete')
      ? 'border-red-800 bg-red-900/20 text-red-300'
      : 'border-blue-800 bg-blue-900/20 text-blue-300'

  return (
    <div className="space-y-4 mb-4">

      {/* Summary */}
      {summary && (
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
          <h3 className="text-white font-medium text-sm mb-3 flex items-center gap-2">
            🧠 Summary
          </h3>
          <p className="text-gray-400 text-sm leading-relaxed">
            {summary}
          </p>
        </div>
      )}

      {/* Why flagged */}
      {why_flagged.length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
          <h3 className="text-white font-medium text-sm mb-3 flex items-center gap-2">
            🚩 Why It Was Flagged
          </h3>
          <ul className="space-y-2">
            {why_flagged.map((reason, i) => (
              <li
                key={i}
                className="text-gray-400 text-sm leading-relaxed flex gap-2"
              >
                <span className="text-gray-600">•</span>
                <span>{reason}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Safety tips */}
      {safety_tips.length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
          <h3 className="text-white font-medium text-sm mb-3 flex items-center gap-2">
            🛡️ Safety Tips
          </h3>
          <ul className="space-y-2">
            {safety_tips.map((tip, i) => (
              <li
                key={i}
                className="text-gray-400 text-sm leading-relaxed flex gap-2"
              >
                <span className="text-gray-600">•</span>
                <span>{tip}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommended action */}
      {recommended_action && (
        <div className={`border rounded-2xl p-5 ${actionColor}`}>
          <h3 className="font-medium text-sm mb-2 flex items-center gap-2">
            🧭 Recommended Action
          </h3>
          <p className="text-sm leading-relaxed">
            {recommended_action}
          </p>
        </div>
      )}

    </div>
  )
}

export default GeminiInsights