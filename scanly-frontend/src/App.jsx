import { BrowserRouter, Routes, Route } from 'react-router-dom'

import Navbar   from './components/Navbar'
import Home     from './pages/Home'
import Results  from './pages/Results'
import History  from './pages/History'

function App() {
  return (
    <BrowserRouter>
      {/* Navbar shows on every page */}
      <Navbar />

      {/* Page content switches based on URL */}
      <Routes>
        <Route path="/"        element={<Home />}    />
        <Route path="/results" element={<Results />} />
        <Route path="/history" element={<History />} />

        {/* 404 fallback */}
        <Route path="*" element={
          <div className="min-h-screen bg-gray-950 flex items-center justify-center">
            <div className="text-center">
              <p className="text-6xl font-bold text-gray-700">404</p>
              <p className="text-gray-500 mt-3">Page not found</p>
            </div>
          </div>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App