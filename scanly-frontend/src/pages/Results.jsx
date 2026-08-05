import { useLocation, useNavigate } from 'react-router-dom'
import { useEffect } from 'react'
import RiskBadge       from '../components/RiskBadge'
import ScoreBar        from '../components/ScoreBar'
import ConfidenceMeter from '../components/ConfidenceMeter'
import OCRPreview      from '../components/OCRPreview'

function Results() {
  const location = useLocation()
  const navigate = useNavigate()
  const result   = location.state?.result
  const scanType = location.state?.scanType || 'text'

  // Update browser tab title with result
  useEffect(() => {
    if (result) {
      document.title = `${result.final_score}% ${result.category} — SCANLY`
    }
    return () => { document.title = 'SCANLY — AI Scam Detection' }
  }, [result])

  // Handle direct /results URL access (no state)
  if (!result) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
        <div className="text-center max-w-sm">
          <div className="text-5xl mb-4">🔍</div>
          <h2 className="text-xl font-semibold text-white mb-2">No scan result</h2>
          <p className="text-gray-500 text-sm mb-6">
            Scan a message first to see results here.
          </p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 hover:bg-blue-500 text-white text-sm
                       font-medium px-6 py-2.5 rounded-xl transition-colors"
          >
            ← Back to Scan
          </button>
        </div>
      </div>
    )
  }

  const {
    final_score,
    category,
    confidence,
    model_version,
    processing_time_ms,
    ml_score,
    rule_score,
    url_score,
    matched_keywords = [],
    flagged_urls = [],
    explanation,
    extracted_text,
    ocr_confidence,
    ocr_lines,
    ocr_warning,
    status,
    message,
  } = result

  // Score ring color
  const scoreColor =
    category === 'Scam'       ? 'text-red-400'
    : category === 'Suspicious' ? 'text-yellow-400'
    : 'text-green-400'

  const ringColor =
    category === 'Scam'       ? 'border-red-500'
    : category === 'Suspicious' ? 'border-yellow-500'
    : 'border-green-500'

  // No-text image result
  if (status === 'no_text') {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
        <div className="text-center max-w-sm">
          <div className="text-5xl mb-4">📷</div>
          <h2 className="text-xl font-semibold text-white mb-2">No text found</h2>
          <p className="text-gray-500 text-sm mb-6">
            {message || 'No readable text could be extracted from the image.'}
          </p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 hover:bg-blue-500 text-white text-sm
                       font-medium px-6 py-2.5 rounded-xl transition-colors"
          >
            ← Try another image
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-950 py-10 px-4">
      <div className="max-w-2xl mx-auto">

        {/* Back button */}
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-gray-500 hover:text-gray-300
                     text-sm mb-6 transition-colors"
        >
          ← Back to Scan
        </button>

        {/* Hero score card */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8 mb-4 text-center">

          {/* Scan type badge */}
          <div className="inline-flex items-center gap-1.5 bg-gray-800 text-gray-400
                          text-xs px-3 py-1 rounded-full mb-5">
            {scanType === 'image' ? '📷 Image Scan'
             : scanType === 'url' ? '🔗 URL Scan'
             : '📝 Text Scan'}
          </div>

          {/* Risk badge */}
          <div className="flex justify-center mb-4">
            <RiskBadge category={category} />
          </div>

          {/* Score ring */}
          <div className={`inline-flex items-center justify-center
                          w-36 h-36 rounded-full border-4 ${ringColor}
                          bg-gray-950 mb-4`}>
            <div>
              <div className={`text-5xl font-bold ${scoreColor}`}>
                {final_score}
              </div>
              <div className="text-gray-500 text-xs mt-0.5">risk score</div>
            </div>
          </div>

          {/* Explanation */}
          <p className="text-gray-400 text-sm max-w-md mx-auto leading-relaxed">
            {explanation}
          </p>

          {/* Processing time */}
          {processing_time_ms && (
            <p className="text-gray-700 text-xs mt-3">
              Analysed in {processing_time_ms}ms
            </p>
          )}
        </div>

        {/* ── Confidence Meter (text + image scans only) ── */}
        <ConfidenceMeter
          confidence={confidence}
          modelVersion={model_version}
        />

        {/* ── OCR Preview (image scans only) ── */}
        {extracted_text && (
          <OCRPreview
            extractedText={extracted_text}
            ocrConfidence={ocr_confidence}
            ocrLines={ocr_lines}
            ocrWarning={ocr_warning}
          />
        )}

        {/* ── Score breakdown ── */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5 mb-4">
          <h3 className="text-white font-medium text-sm mb-4">
            📊 Score Breakdown
          </h3>
          <div className="space-y-3">
            <ScoreBar label="🤖 AI Model"    score={ml_score}   />
            <ScoreBar label="📋 Rule Engine" score={rule_score} />
            <ScoreBar label="🔗 URL Check"   score={url_score}  />
          </div>
        </div>

        {/* ── Matched keywords ── */}
        {matched_keywords.length > 0 && (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5 mb-4">
            <h3 className="text-white font-medium text-sm mb-3">
              🚨 Flagged Keywords
            </h3>
            <div className="flex flex-wrap gap-2">
              {matched_keywords.map((kw, i) => (
                <span key={i}
                  className="bg-red-900/30 border border-red-800 text-red-400
                             text-xs px-3 py-1 rounded-full">
                  {kw}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* ── Flagged URLs ── */}
        {flagged_urls && flagged_urls.length > 0 && (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5 mb-4">
            <h3 className="text-white font-medium text-sm mb-3">
              🔗 Suspicious URLs
            </h3>
            <div className="space-y-2">
              {flagged_urls.map((url, i) => (
                <div key={i}
                  className="bg-gray-950 border border-gray-700 rounded-lg
                             px-3 py-2 font-mono text-xs text-red-400 break-all">
                  {url}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Input text preview ── */}
        {result.input_text && scanType !== 'image' && (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5 mb-4">
            <h3 className="text-gray-500 font-medium text-xs uppercase
                           tracking-wider mb-2">
              Scanned Text
            </h3>
            <p className="text-gray-400 text-sm leading-relaxed break-words">
              {result.input_text}
            </p>
          </div>
        )}

        {/* URL details (URL scans) */}
        {scanType === 'url' && result.checks && (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5 mb-4">
            <h3 className="text-white font-medium text-sm mb-3">
              🔍 URL Analysis
            </h3>
            <div className="space-y-2">
              {Object.entries(result.checks).map(([key, val]) => (
                <div key={key} className="flex items-center justify-between
                                          text-sm py-1 border-b border-gray-800
                                          last:border-0">
                  <span className="text-gray-400">
                    {key.replace(/_/g, ' ')}
                  </span>
                  <span className={val ? 'text-red-400' : 'text-green-400'}>
                    {val ? '⚠ Yes' : '✓ No'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Scan again button ── */}
        <button
          onClick={() => navigate('/')}
          className="w-full py-3.5 rounded-xl font-semibold text-sm
                     bg-blue-600 hover:bg-blue-500 text-white
                     transition-all hover:-translate-y-0.5 mt-2"
        >
          🔍 Scan Another
        </button>

      </div>
    </div>
  )
}

export default Results
