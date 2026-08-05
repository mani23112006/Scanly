import ScanTabs from '../components/ScanTabs'

function Home() {
  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center px-4 py-12">

      {/* Hero */}
      <div className="text-center mb-8 max-w-xl">

        <div
          className="inline-flex items-center gap-2
                     bg-blue-900/30 border border-blue-800
                     text-blue-400 text-xs px-3 py-1
                     rounded-full mb-5"
        >
          ⚡ RoBERTa AI · OCR · URL Analysis
        </div>

        {/* Responsive heading */}
        <h1
          className="text-4xl md:text-6xl font-bold
                     text-white mb-3 tracking-tight"
        >
          SCAN<span className="text-blue-400">LY</span>
        </h1>

        <p className="text-gray-400 text-base md:text-lg leading-relaxed">
          Scan text, URLs, or screenshots for scam indicators.
        </p>

      </div>

      {/* Scan Tabs */}
      <ScanTabs />

      {/* Feature badges */}
      <div className="flex gap-2 mt-8 flex-wrap justify-center">

        {[
          '🤖 RoBERTa AI',
          '📋 Rule Engine',
          '🔗 URL Check',
          '📷 Image OCR',
          '💾 History',
        ].map((feature) => (

          <span
            key={feature}
            className="bg-gray-900 border border-gray-800
                       text-gray-500 text-xs px-3 py-1.5
                       rounded-full hover:border-gray-600
                       hover:text-gray-400 transition-colors"
          >
            {feature}
          </span>

        ))}

      </div>

    </div>
  )
}

export default Home