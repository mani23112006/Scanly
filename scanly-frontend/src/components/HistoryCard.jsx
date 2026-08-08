import { useState } from 'react'

function HistoryCard({ scan }) {

  const [expanded, setExpanded] = useState(false)

  // ── Color config per category ─────────────────
  const config = {
    Safe: {
      border:  'border-green-900/60',
      badge:   'bg-green-900/30 border-green-800 text-green-400',
      score:   'text-green-400',
      emoji:   '🟢'
    },
    Suspicious: {
      border:  'border-yellow-900/60',
      badge:   'bg-yellow-900/30 border-yellow-800 text-yellow-400',
      score:   'text-yellow-400',
      emoji:   '🟡'
    },
    Scam: {
      border:  'border-red-900/60',
      badge:   'bg-red-900/30 border-red-800 text-red-400',
      score:   'text-red-400',
      emoji:   '🔴'
    }
  }

  const c = config[scan.category] || config['Suspicious']

  // ── Format timestamp ──────────────────────────
  const formatDate = (ts) => {
    if (!ts) return 'Unknown date'
    try {
      const d = new Date(ts)
      return d.toLocaleString('en-IN', {
        day:    '2-digit',
        month:  'short',
        year:   'numeric',
        hour:   '2-digit',
        minute: '2-digit'
      })
    } catch {
      return ts
    }
  }

  // ── Truncate long messages ────────────────────
  const preview = scan.input_text?.length > 120
    ? scan.input_text.slice(0, 120) + '...'
    : scan.input_text

  const gemini = scan.gemini
  const hasGeminiDetail =
    gemini && (gemini.why_flagged?.length > 0 || gemini.safety_tips?.length > 0)

  return (
    <div className={`bg-gray-900 border ${c.border} rounded-xl p-5
                     hover:border-gray-600 transition-colors`}>

      {/* Top row — score + badge + date */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          {/* Score */}
          <span className={`text-2xl font-black ${c.score}`}>
            {scan.final_score}
            <span className="text-sm font-normal text-gray-600">%</span>
          </span>
          {/* Category badge */}
          <span className={`text-xs font-bold px-2.5 py-1 rounded-full
                            border ${c.badge}`}>
            {c.emoji} {scan.category?.toUpperCase()}
          </span>
        </div>
        {/* Date */}
        <span className="text-xs text-gray-600">
          {formatDate(scan.timestamp)}
        </span>
      </div>

      {/* Message preview */}
      <p className="text-gray-500 text-sm leading-relaxed font-mono
                    bg-gray-950 rounded-lg px-3 py-2 border border-gray-800 mb-3">
        {preview}
      </p>

      {/* ── Gemini summary (always visible if present) ── */}
      {gemini?.summary && (
        <div className="bg-gray-950 border border-gray-800 rounded-lg
                        px-3 py-2 mb-3">
          <p className="text-xs text-gray-500 flex gap-1.5">
            <span>🧠</span>
            <span className="leading-relaxed">{gemini.summary}</span>
          </p>
        </div>
      )}

      {/* Bottom row — mini score breakdown + keywords */}
      <div className="flex items-center justify-between flex-wrap gap-2 mb-2">

        {/* Mini scores */}
        <div className="flex gap-3 text-xs text-gray-600">
          <span>🤖 {scan.ml_score}%</span>
          <span>📋 {scan.rule_score}%</span>
          <span>🔗 {scan.url_score}%</span>
        </div>

        {/* Keywords — show max 3 */}
        {scan.matched_keywords?.length > 0 && (
          <div className="flex gap-1.5 flex-wrap">
            {scan.matched_keywords.slice(0, 3).map((kw) => (
              <span key={kw}
                className="text-xs bg-red-900/20 border border-red-900/40
                           text-red-500 px-2 py-0.5 rounded font-mono">
                {kw}
              </span>
            ))}
            {scan.matched_keywords.length > 3 && (
              <span className="text-xs text-gray-600">
                +{scan.matched_keywords.length - 3} more
              </span>
            )}
          </div>
        )}
      </div>

      {/* ── Expand toggle for full Gemini explanation ── */}
      {hasGeminiDetail && (
        <>
          <button
            onClick={() => setExpanded((prev) => !prev)}
            className="text-xs text-blue-400 hover:text-blue-300
                       transition-colors mt-1"
          >
            {expanded ? '▲ Hide AI explanation' : '▼ View AI explanation'}
          </button>

          {expanded && (
            <div className="mt-3 pt-3 border-t border-gray-800 space-y-3">

              {gemini.why_flagged?.length > 0 && (
                <div>
                  <p className="text-xs font-medium text-gray-400 mb-1.5">
                    🚩 Why it was flagged
                  </p>
                  <ul className="space-y-1">
                    {gemini.why_flagged.map((reason, i) => (
                      <li key={i} className="text-xs text-gray-500 flex gap-1.5">
                        <span className="text-gray-700">•</span>
                        <span>{reason}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {gemini.safety_tips?.length > 0 && (
                <div>
                  <p className="text-xs font-medium text-gray-400 mb-1.5">
                    🛡️ Safety tips
                  </p>
                  <ul className="space-y-1">
                    {gemini.safety_tips.map((tip, i) => (
                      <li key={i} className="text-xs text-gray-500 flex gap-1.5">
                        <span className="text-gray-700">•</span>
                        <span>{tip}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {gemini.recommended_action && (
                <div>
                  <p className="text-xs font-medium text-gray-400 mb-1.5">
                    🧭 Recommended action
                  </p>
                  <p className="text-xs text-gray-500">
                    {gemini.recommended_action}
                  </p>
                </div>
              )}

            </div>
          )}
        </>
      )}

    </div>
  )
}

export default HistoryCard