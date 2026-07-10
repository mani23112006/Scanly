function Home() {
  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center px-4">

      {/* Hero section */}
      <div className="text-center mb-10">
        <h1 className="text-5xl font-bold text-white mb-3">
          SCAN<span className="text-blue-400">LY</span>
        </h1>
        <p className="text-gray-400 text-lg">
          AI-powered scam detection. Paste any message or link to check if it's safe.
        </p>
      </div>

      {/* Input card — ScanForm component goes here on Day 11 */}
      <div className="w-full max-w-2xl bg-gray-900 rounded-2xl border border-gray-800 p-8">
        <p className="text-gray-500 text-sm text-center">
          Scan form coming on Day 11
        </p>
      </div>

      {/* Feature badges */}
      <div className="flex gap-4 mt-8 flex-wrap justify-center">
        <span className="bg-gray-900 border border-gray-800 text-gray-400 text-xs px-4 py-2 rounded-full">
          🤖 AI Detection
        </span>
        <span className="bg-gray-900 border border-gray-800 text-gray-400 text-xs px-4 py-2 rounded-full">
          🔗 URL Analysis
        </span>
        <span className="bg-gray-900 border border-gray-800 text-gray-400 text-xs px-4 py-2 rounded-full">
          ⚡ Real-time Results
        </span>
        <span className="bg-gray-900 border border-gray-800 text-gray-400 text-xs px-4 py-2 rounded-full">
          📋 Scan History
        </span>
      </div>

    </div>
  )
}

export default Home