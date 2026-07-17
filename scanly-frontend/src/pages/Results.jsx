import { useLocation, useNavigate } from 'react-router-dom'
import RiskBadge from '../components/RiskBadge'
import ScoreBar  from '../components/ScoreBar'

function Results() {
  const location = useLocation()
  const navigate = useNavigate()
  const result   = location.state?.result

  // ── No result — user visited /results directly ──
  if (!result) {
    return (
      <div className="min-h-screen bg-gray-950 flex flex-col
                      items-center justify-center px-4">
        <div className="text-center">
          <p className="text-6xl mb-4">🔍</p>
          <h2 className="text-2xl font-bold text-white mb-2">No scan result</h2>
          <p className="text-gray-500 mb-6">
            Scan a message first to see results here.
          </p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 hover:bg-blue-500 text-white font-medium
                       px-6 py-3 rounded-xl transition-colors"
          >
            ← Go to Scanner
          </button>
        </div>
      </div>
    )
  }

  // ── Score ring color ────────────────────────────
  const ringColor =
    result.category === 'Scam'       ? 'text-red-400' :
    result.category === 'Suspicious' ? 'text-yellow-400' :
                                       'text-green-400'

  return (
    <div className="min-h-screen bg-gray-950 px-4 py-10">
      <div className="max-w-2xl mx-auto">

        {/* ── Hero Score Section ─────────────────── */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8
                        text-center mb-5 shadow-xl">

          {/* Big score number */}
          <div className={`text-6xl md:text-8xl font-black mb-2 ${ringColor}`}>
            {result.final_score}
            <span className="text-4xl font-bold text-gray-600">%</span>
          </div>

          {/* Risk badge */}
          <div className="flex justify-center mb-4">
            <RiskBadge category={result.category} />
          </div>

          {/* Explanation */}
          <p className="text-gray-400 text-sm leading-relaxed max-w-lg mx-auto">
            {result.explanation}
          </p>
        </div>

        {/* ── Score Breakdown ────────────────────── */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-5">
          <h3 className="text-white font-semibold mb-5 flex items-center gap-2">
            📊 Score Breakdown
          </h3>
          <div className="flex flex-col gap-5">
            <ScoreBar
              label="🤖 AI / ML Model"
              score={result.ml_score}
              color="blue"
            />
            <ScoreBar
              label="📋 Rule Engine"
              score={result.rule_score}
              color="purple"
            />
            <ScoreBar
              label="🔗 URL Analysis"
              score={result.url_score}
              color="orange"
            />
          </div>

          {/* Weight legend */}
          <div className="mt-5 pt-4 border-t border-gray-800 flex gap-4
                          text-xs text-gray-600 justify-center flex-wrap">
            <span>AI = 50% weight</span>
            <span>Rules = 30% weight</span>
            <span>URL = 20% weight</span>
          </div>
               </div>

        {/* ── Matched Keywords ───────────────────── */}
        {result.matched_keywords?.length > 0 && (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-5">
            <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
              ⚠️ Flagged Keywords
              <span className="text-xs bg-red-900/40 border border-red-800
                               text-red-400 px-2 py-0.5 rounded-full">
                {result.matched_keywords.length}
              </span>
            </h3>
            <div className="flex flex-wrap gap-2">
              {result.matched_keywords.map((kw) => (
                <span
                  key={kw}
                  className="bg-red-900/20 border border-red-800/50 text-red-400
                             text-xs px-3 py-1.5 rounded-lg font-mono"
                >
                  {kw}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* ── Scanned Message Preview ────────────── */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-5">
          <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
            📝 Scanned Message
          </h3>
          <p className="text-gray-500 text-sm leading-relaxed font-mono
                        bg-gray-950 rounded-xl p-4 border border-gray-800">
            {result.input_text?.length > 300
              ? result.input_text.slice(0, 300) + '...'
              : result.input_text}
          </p>
        </div>

        {/* ── Action Buttons ─────────────────────── */}
       <div className="flex flex-col sm:flex-row gap-3">
          <button
            onClick={() => navigate('/')}
            className="flex-1 bg-blue-600 hover:bg-blue-500 text-white
                       font-semibold py-3.5 rounded-xl transition-colors"
          >
            ← Scan Another
          </button>
          <button
            onClick={() => navigate('/history')}
            className="flex-1 bg-gray-800 hover:bg-gray-700 text-gray-300
                       font-semibold py-3.5 rounded-xl transition-colors
                       border border-gray-700"
          >
            View History →
          </button>
        </div>

      </div>
    </div>
  )
}

export default Results