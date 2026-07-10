import { Link, useLocation } from 'react-router-dom'

function Navbar() {
  const location = useLocation()

  // Helper to highlight the active link
  const isActive = (path) => location.pathname === path

  return (
    <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4">
      <div className="max-w-5xl mx-auto flex items-center justify-between">

        {/* Logo */}
        <Link to="/" className="text-xl font-bold text-white">
          SCAN<span className="text-blue-400">LY</span>
        </Link>

        {/* Nav links */}
        <div className="flex items-center gap-6">
          <Link
            to="/"
            className={`text-sm font-medium transition-colors ${
              isActive('/')
                ? 'text-blue-400'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Scan
          </Link>

          <Link
            to="/history"
            className={`text-sm font-medium transition-colors ${
              isActive('/history')
                ? 'text-blue-400'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            History
          </Link>

          {/* Status badge */}
          <span className="flex items-center gap-1.5 bg-green-900/40 border border-green-800 text-green-400 text-xs px-3 py-1 rounded-full">
            <span className="w-1.5 h-1.5 bg-green-400 rounded-full"></span>
            API Live
          </span>
        </div>

      </div>
    </nav>
  )
}

export default Navbar