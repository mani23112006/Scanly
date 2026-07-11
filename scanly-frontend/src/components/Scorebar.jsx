function ScoreBar({ label, score, color }) {
  // color prop: 'blue' | 'purple' | 'orange'
  const colorMap = {
    blue: {
      bar:  'bg-blue-500',
      text: 'text-blue-400',
      bg:   'bg-blue-900/20'
    },
    purple: {
      bar:  'bg-purple-500',
      text: 'text-purple-400',
      bg:   'bg-purple-900/20'
    },
    orange: {
      bar:  'bg-orange-500',
      text: 'text-orange-400',
      bg:   'bg-orange-900/20'
    }
  }

  const c = colorMap[color] || colorMap['blue']

  // Clamp score between 0 and 100
  const pct = Math.min(Math.max(score, 0), 100)

  // Risk level label for the score number
  const riskLabel =
    pct >= 71 ? 'High' :
    pct >= 31 ? 'Medium' : 'Low'

  return (
    <div className="w-full">
      {/* Label row */}
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-sm text-gray-400 font-medium">{label}</span>
        <div className="flex items-center gap-2">
          <span className={`text-xs ${c.text} font-mono`}>{riskLabel}</span>
          <span className={`text-sm font-bold ${c.text}`}>{pct}%</span>
        </div>
      </div>

      {/* Track */}
      <div className="w-full bg-gray-800 rounded-full h-2.5 overflow-hidden">
        {/* Fill — width driven by score */}
        <div
          className={`h-2.5 rounded-full ${c.bar} transition-all duration-700 ease-out`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

export default ScoreBar