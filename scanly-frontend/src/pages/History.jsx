import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import HistoryCard from '../components/HistoryCard'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function History() {
  const navigate = useNavigate()

  const [scans,   setScans]   = useState([])
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState('')

  // ── Fetch history on mount ─────────────────────
  const fetchHistory = async () => {
    setLoading(true)
    setError('')
    try {
      const res = await axios.get(`${API_URL}/history?limit=50`)
      setScans(res.data.scans || [])
    } catch (err) {
      console.error('History fetch failed:', err)
      if (err.request) {
        setError('Cannot reach backend. Make sure it is running on port 8000.')
      } else {
        setError('Failed to load history. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchHistory()
  }, [])   // empty [] = run once when page loads

  // ── Clear all history ──────────────────────────
  const handleClear = async () => {
    if (!window.confirm('Delete all scan history? This cannot be undone.')) return
    try {
      await axios.delete(`${API_URL}/history`)
      setScans([])
    } catch {
      setError('Failed to clear history.')
    }
  }

  // ── Loading skeleton ───────────────────────────
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 px-4 py-10">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <div>
              <div className="h-8 w-40 bg-gray-800 rounded-lg animate-pulse mb-2" />
              <div className="h-4 w-24 bg-gray-800 rounded animate-pulse" />
            </div>
          </div>
          {/* Skeleton cards */}
          {[1, 2, 3].map((i) => (
            <div key={i}
              className="bg-gray-900 border border-gray-800 rounded-xl p-5
                         mb-4 animate-pulse">
              <div className="flex items-center gap-3 mb-3">
                <div className="h-7 w-14 bg-gray-800 rounded" />
                <div className="h-5 w-24 bg-gray-800 rounded-full" />
                <div className="h-4 w-32 bg-gray-800 rounded ml-auto" />
              </div>
              <div className="h-12 bg-gray-800 rounded-lg mb-3" />
              <div className="h-4 w-48 bg-gray-800 rounded" />
            </div>
          ))}
        </div>
      </div>
    )
  }
  
  // ── Error state ────────────────────────────────
  if (error) {
    return (
      <div className="min-h-screen bg-gray-950 px-4 py-10">
        <div className="max-w-3xl mx-auto">
          <div className="bg-red-900/20 border border-red-800 rounded-2xl
                          p-8 text-center">
            <p className="text-4xl mb-3">⚠️</p>
            <p className="text-red-400 font-medium mb-2">{error}</p>
            <button
              onClick={fetchHistory}
              className="mt-4 bg-red-800 hover:bg-red-700 text-white
                         text-sm px-5 py-2 rounded-xl transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  // ── Empty state ────────────────────────────────
  if (scans.length === 0) {
    return (
      <div className="min-h-screen bg-gray-950 px-4 py-10">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-8">Scan History</h2>
          <div className="bg-gray-900 border border-gray-800 rounded-2xl
                          p-12 text-center">
            <p className="text-5xl mb-4">📭</p>
            <p className="text-white font-semibold text-lg mb-2">
              No scans yet
            </p>
            <p className="text-gray-500 text-sm mb-6">
              Scan your first message to see results here.
            </p>
            <button
              onClick={() => navigate('/')}
              className="bg-blue-600 hover:bg-blue-500 text-white font-medium
                         px-6 py-3 rounded-xl transition-colors"
            >
              → Scan a Message
            </button>
          </div>
        </div>
      </div>
    )
  }

  // ── Main history list ──────────────────────────
  return (
    <div className="min-h-screen bg-gray-950 px-4 py-10">
      <div className="max-w-3xl mx-auto">

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center
                justify-between mb-6 gap-4">

          <div>
            <h2 className="text-3xl font-bold text-white">Scan History</h2>
            <p className="text-gray-500 mt-1 text-sm">
              {scans.length} scan{scans.length !== 1 ? 's' : ''} total
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={fetchHistory}
              className="bg-gray-800 hover:bg-gray-700 text-gray-400
                         text-sm px-4 py-2 rounded-xl transition-colors
                         border border-gray-700"
            >
              ↻ Refresh
            </button>
            <button
              onClick={() => navigate('/')}
              className="bg-blue-600 hover:bg-blue-500 text-white text-sm
                         font-medium px-4 py-2 rounded-xl transition-colors"
            >
              + New Scan
            </button>
          </div>
        </div>

        {/* Stats bar */}
       <div className="grid grid-cols-3 sm:grid-cols-3 gap-2 md:gap-3 mb-6">
          {[
            { label: 'Total Scans', value: scans.length, color: 'text-blue-400' },
            { label: 'Scams Found', value: scans.filter(s => s.category === 'Scam').length, color: 'text-red-400' },
            { label: 'Safe', value: scans.filter(s => s.category === 'Safe').length, color: 'text-green-400' }
          ].map(stat => (
            <div key={stat.label}
              className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
              <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
              <p className="text-gray-600 text-xs mt-1">{stat.label}</p>
            </div>
          ))}
        </div>
        
        {/* Scan list */}
        <div className="flex flex-col gap-4">
          {scans.map((scan) => (
            <HistoryCard key={scan.id} scan={scan} />
          ))}
        </div>

        {/* Clear history */}
        <div className="mt-8 text-center">
          <button
            onClick={handleClear}
            className="text-xs text-gray-700 hover:text-red-500
                       transition-colors underline underline-offset-2"
          >
            Clear all history
          </button>
        </div>

      </div>
    </div>
  )
}

export default History