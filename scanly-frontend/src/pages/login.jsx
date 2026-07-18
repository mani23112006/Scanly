import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function Login() {
  const navigate  = useNavigate()
  const location  = useLocation()
  const { login, register, continueAsGuest } = useAuth()

  const [email,    setEmail]    = useState('')
  const [password, setPassword] = useState('')
  const [isSignUp, setIsSignUp] = useState(false)
  const [loading,  setLoading]  = useState(false)
  const [error,    setError]    = useState('')

  // Go back to where user came from, or home
  const from = location.state?.from || '/'

  const handleSubmit = async () => {
    if (!email.trim() || !password.trim()) {
      setError('Please enter both email and password.')
      return
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters.')
      return
    }

    setError('')
    setLoading(true)

    try {
      if (isSignUp) {
        await register(email, password)
      } else {
        await login(email, password)
      }
      navigate(from, { replace: true })
    } catch (err) {
      const code = err.code
      if (code === 'auth/user-not-found')    setError('No account found with this email.')
      else if (code === 'auth/wrong-password') setError('Incorrect password.')
      else if (code === 'auth/email-already-in-use') setError('Email already registered. Sign in instead.')
      else if (code === 'auth/invalid-email') setError('Invalid email address.')
      else if (code === 'auth/invalid-credential') setError('Invalid email or password.')
      else setError('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleGuest = () => {
    continueAsGuest()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center
                    justify-center px-4">
      <div className="w-full max-w-md">

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            SCAN<span className="text-blue-400">LY</span>
          </h1>
          <p className="text-gray-500 text-sm">
            {isSignUp ? 'Create an account' : 'Sign in to your account'}
          </p>
        </div>

    {/* Card */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8">

          {/* Email */}
          <div className="mb-4">
            <label className="block text-sm text-gray-400 mb-1.5">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full bg-gray-950 border border-gray-700 rounded-xl
                         text-gray-200 placeholder-gray-600 text-sm px-4 py-3
                         focus:outline-none focus:border-blue-500
                         focus:ring-1 focus:ring-blue-500 transition-colors"
            />
          </div>

          {/* Password */}
          <div className="mb-5">
            <label className="block text-sm text-gray-400 mb-1.5">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
              className="w-full bg-gray-950 border border-gray-700 rounded-xl
                         text-gray-200 placeholder-gray-600 text-sm px-4 py-3
                         focus:outline-none focus:border-blue-500
                         focus:ring-1 focus:ring-blue-500 transition-colors"
            />
          </div>

          {/* Error */}
          {error && (
            <div className="mb-4 bg-red-900/30 border border-red-800
                            text-red-400 text-sm px-4 py-3 rounded-xl">
              ⚠ {error}
            </div>
          )}

          {/* Submit button */}
          <button
            onClick={handleSubmit}
            disabled={loading}
            className={`w-full py-3.5 rounded-xl font-semibold text-sm
                        transition-all mb-3
              ${loading
                ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-500 text-white hover:-translate-y-0.5'
              }`}
          >
            {loading ? 'Please wait...' : isSignUp ? 'Create Account' : 'Sign In'}
          </button>

          {/* Toggle sign in / sign up */}
          <button
            onClick={() => { setIsSignUp(!isSignUp); setError('') }}
            className="w-full text-sm text-gray-500 hover:text-gray-300
                       transition-colors py-2"
          >
            {isSignUp
              ? 'Already have an account? Sign in'
              : "Don't have an account? Sign up"}
          </button>

          {/* Divider */}
          <div className="flex items-center gap-3 my-4">
            <div className="flex-1 h-px bg-gray-800" />
            <span className="text-xs text-gray-600">or</span>
            <div className="flex-1 h-px bg-gray-800" />
          </div>

          {/* Guest button */}
          <button
            onClick={handleGuest}
            className="w-full py-3 rounded-xl font-medium text-sm
                       bg-gray-800 hover:bg-gray-700 text-gray-300
                       border border-gray-700 transition-colors"
          >
            👤 Continue as Guest
          </button>

          <p className="text-xs text-gray-600 text-center mt-3">
            Guest mode: scan messages freely. Sign in to save history.
          </p>

        </div>
      </div>
    </div>
  )
}

export default Login