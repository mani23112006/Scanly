import { useLocation, useNavigate } from 'react-router-dom'

function Results() {
  const location = useLocation()
  const navigate = useNavigate()

  // Results data will be passed here via router state on Day 12
  const result = location.state?.result

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center px-4">

      <div className="w-full max-w-2xl">

        <h2 className="text-3xl font-bold text-white mb-2 text-center">
          Scan Results
        </h2>
        <p className="text-gray-500 text-center mb-8">
          Full results display coming on Day 12
        </p>

        {/* Show raw result data if we already have it */}
        {result ? (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
            <p className="text-green-400 font-mono text-sm">
              Score: {result.final_score} — {result.category}
            </p>
            <p className="text-gray-400 text-sm mt-2">
              {result.explanation}
            </p>
          </div>
        ) : (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 text-center">
            <p className="text-gray-500">No scan result to display.</p>
          </div>
        )}

        <button
          onClick={() => navigate('/')}
          className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-xl transition-colors"
        >
          ← Scan Another Message
        </button>

      </div>
    </div>
  )
}

export default Results