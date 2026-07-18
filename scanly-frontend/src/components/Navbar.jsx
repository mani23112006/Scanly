import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'


function Navbar() {

  const { user, isGuest, logout } = useAuth()
const navigate = useNavigate()

const handleLogout = async () => {
  await logout()
  navigate('/')
}

  const location  = useLocation()
  const [open, setOpen] = useState(false)

  const isActive = (path) => location.pathname === path

  const linkClass = (path) =>
    `text-sm font-medium transition-colors ${
      isActive(path)
        ? 'text-blue-400'
        : 'text-gray-400 hover:text-white'
    }`

  return (
    <nav className="bg-gray-900/80 backdrop-blur-md border-b
                    border-gray-800 px-4 md:px-6 py-4 sticky top-0 z-50">
      <div className="max-w-5xl mx-auto flex items-center justify-between">

        {/* Logo */}
        <Link to="/" className="text-xl font-bold text-white"
              onClick={() => setOpen(false)}>
          SCAN<span className="text-blue-400">LY</span>
        </Link>

        {/* Desktop links */}
      <div className="hidden md:flex items-center gap-6">
  <Link to="/"        className={linkClass('/')}>Scan</Link>

  {/* History only shown to logged-in users */}
  {user && (
    <Link to="/history" className={linkClass('/history')}>
      History
    </Link>
  )}

  {/* Auth status */}
  {user ? (
    <div className="flex items-center gap-3">
      <span className="text-xs text-gray-500 truncate max-w-32">
        {user.email}
      </span>
      <button
        onClick={handleLogout}
        className="text-xs bg-gray-800 hover:bg-gray-700 text-gray-400
                   px-3 py-1.5 rounded-lg border border-gray-700
                   transition-colors"
      >
        Sign out
      </button>
    </div>
  ) : isGuest ? (
    <Link to="/login"
      className="text-xs bg-blue-600 hover:bg-blue-500 text-white
                 px-3 py-1.5 rounded-lg transition-colors">
      Sign in
    </Link>
  ) : (
    <Link to="/login"
      className="text-xs bg-blue-600 hover:bg-blue-500 text-white
                 px-3 py-1.5 rounded-lg transition-colors">
      Sign in
    </Link>
  )}

  <span className="flex items-center gap-1.5 bg-green-900/40
                   border border-green-800 text-green-400
                   text-xs px-3 py-1 rounded-full">
    <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse">
    </span>
    API Live
  </span>
</div>

        {/* Mobile hamburger */}
        <button
          onClick={() => setOpen(!open)}
          className="md:hidden text-gray-400 hover:text-white
                     transition-colors p-1"
          aria-label="Toggle menu"
        >
          {open ? (
            /* X icon */
            <svg className="w-6 h-6" fill="none" stroke="currentColor"
                 viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round"
                    strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            /* Hamburger icon */
            <svg className="w-6 h-6" fill="none" stroke="currentColor"
                 viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round"
                    strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          )}
        </button>
      </div>

      {/* Mobile dropdown */}
      {open && (
        <div className="md:hidden border-t border-gray-800 pt-4 pb-2
                        px-4 mt-3 flex flex-col gap-4">
          <Link to="/" onClick={() => setOpen(false)}
                className={linkClass('/')}>
            🔍 Scan
          </Link>
          <Link to="/history" onClick={() => setOpen(false)}
                className={linkClass('/history')}>
            📋 History
          </Link>
          <span className="flex items-center gap-1.5 text-green-400 text-xs">
            <span className="w-1.5 h-1.5 bg-green-400 rounded-full
                             animate-pulse"></span>
            API Live
          </span>
        </div>
      )}
    </nav>
  )
}

export default Navbar