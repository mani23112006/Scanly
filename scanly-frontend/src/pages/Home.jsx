import ScanForm from '../components/ScanForm'

function Home() {
  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center
                    justify-center px-4 py-12">

      {/* Hero */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 bg-blue-900/30 border
                        border-blue-800 text-blue-400 text-xs px-3 py-1
                        rounded-full mb-4">
          ⚡ AI-Powered Scam Detection
        </div>
        <h1 className="text-5xl font-bold text-white mb-3">
          SCAN<span className="text-blue-400">LY</span>
        </h1>
        <p className="text-gray-400 text-lg max-w-md mx-auto">
          Paste any suspicious message or link.
          Get an instant AI risk score.
        </p>
      </div>

      {/* Scan Form */}
      <ScanForm />

      {/* Footer badges */}
      <div className="flex gap-3 mt-8 flex-wrap justify-center">
        {['🤖 ML Model', '📋 Rule Engine', '🔗 URL Analysis', '💾 History'].map(f => (
          <span key={f}
            className="bg-gray-900 border border-gray-800 text-gray-500
                       text-xs px-3 py-1.5 rounded-full">
            {f}
          </span>
        ))}
      </div>

    </div>
  )
}

export default Home