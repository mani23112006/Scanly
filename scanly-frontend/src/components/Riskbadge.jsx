function RiskBadge({ category }) {

  const config = {
    Safe: {
      bg:     'bg-green-900/40',
      border: 'border-green-700',
      text:   'text-green-400',
      dot:    'bg-green-400',
      emoji:  '🟢',
      label:  'SAFE'
    },
    Suspicious: {
      bg:     'bg-yellow-900/40',
      border: 'border-yellow-700',
      text:   'text-yellow-400',
      dot:    'bg-yellow-400',
      emoji:  '🟡',
      label:  'SUSPICIOUS'
    },
    Scam: {
      bg:     'bg-red-900/40',
      border: 'border-red-700',
      text:   'text-red-400',
      dot:    'bg-red-400',
      emoji:  '🔴',
      label:  'SCAM'
    }
  }

  // Fallback if category is unknown
  const style = config[category] || config['Suspicious']

  return (
    <div className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-full
                     border ${style.bg} ${style.border}`}>
      {/* Pulsing dot */}
      <span className="relative flex h-2.5 w-2.5">
        <span className={`animate-ping absolute inline-flex h-full w-full
                          rounded-full ${style.dot} opacity-60`}></span>
        <span className={`relative inline-flex rounded-full h-2.5 w-2.5 ${style.dot}`}>
        </span>
      </span>
      {/* Label */}
      <span className={`font-bold text-sm tracking-widest ${style.text}`}>
        {style.emoji} {style.label}
      </span>
    </div>
  )
}

export default RiskBadge