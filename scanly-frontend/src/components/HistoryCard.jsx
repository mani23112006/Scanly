function HistoryCard({ scan }) {

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

      {/* Bottom row — mini score breakdown + keywords */}
      <div className="flex items-center justify-between flex-wrap gap-2">

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

    </div>
  )
}

export default HistoryCard