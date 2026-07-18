import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'

import Navbar         from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'
import Home           from './pages/Home'
import Results        from './pages/Results'
import History        from './pages/History'
import Login          from './pages/Login'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/"        element={<Home />}    />
          <Route path="/results" element={<Results />} />
          <Route path="/login"   element={<Login />}   />

          {/* Protected — only logged-in users */}
          <Route path="/history" element={
            <ProtectedRoute>
              <History />
            </ProtectedRoute>
          } />

          {/* 404 */}
          <Route path="*" element={
            <div className="min-h-screen bg-gray-950 flex items-center
                            justify-center">
              <div className="text-center">
                <p className="text-6xl font-bold text-gray-700">404</p>
                <p className="text-gray-500 mt-3">Page not found</p>
              </div>
            </div>
          } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App