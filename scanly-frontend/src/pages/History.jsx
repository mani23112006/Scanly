import { useNavigate } from 'react-router-dom'

function History() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gray-950 px-4 py-10">

      <div className="max-w-3xl mx-auto">

        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold text-white">Scan History</h2>
            <p className="text-gray-500 mt-1">Your past scan results</p>
          </div>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-xl transition-colors"
          >
            + New Scan
          </button>
        </div>

        {/* History list — real data fetched from API on Day 13 */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 text-center">
          <p className="text-gray-500">History list coming on Day 13</p>
          <p className="text-gray-600 text-sm mt-2">
            Will fetch from GET /history endpoint
          </p>
        </div>

      </div>
    </div>
  )
}

export default History