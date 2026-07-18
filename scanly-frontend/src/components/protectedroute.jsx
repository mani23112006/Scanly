import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function ProtectedRoute({ children }) {
  const { user, authLoading } = useAuth()
  const location = useLocation()

  // Still checking auth state — show nothing
  if (authLoading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center
                      justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent
                          rounded-full animate-spin mx-auto mb-3" />
          <p className="text-gray-500 text-sm">Checking auth...</p>
        </div>
      </div>
    )
  }

  // Not logged in — redirect to login, remember where they came from
  if (!user) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />
  }

  return children
}

export default ProtectedRoute