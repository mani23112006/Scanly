import { createContext, useContext, useEffect, useState } from 'react'
import {
  onAuthStateChanged,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut
} from 'firebase/auth'
import { auth } from '../firebase'

// ── Create context ──────────────────────────────────
const AuthContext = createContext(null)

// ── Custom hook — components use this ──────────────
export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}

// ── Provider component ──────────────────────────────
export function AuthProvider({ children }) {
  const [user,        setUser]        = useState(null)
  const [isGuest,     setIsGuest]     = useState(false)
  const [authLoading, setAuthLoading] = useState(true)

  // Listen to Firebase auth state changes
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser)
      setAuthLoading(false)
    })
    return unsubscribe   // cleanup on unmount
  }, [])
    // ── Login with email + password ─────────────────
  const login = async (email, password) => {
    const result = await signInWithEmailAndPassword(auth, email, password)
    setIsGuest(false)
    return result
  }

  // ── Register new account ────────────────────────
  const register = async (email, password) => {
    const result = await createUserWithEmailAndPassword(auth, email, password)
    setIsGuest(false)
    return result
  }

  // ── Continue as guest (no Firebase auth needed) ─
  const continueAsGuest = () => {
    setIsGuest(true)
  }
    // ── Sign out ─────────────────────────────────────
  const logout = async () => {
    await signOut(auth)
    setUser(null)
    setIsGuest(false)
  }

  // ── Is authenticated? (real user OR guest) ──────
  const isAuthenticated = !!user || isGuest

  const value = {
    user,
    isGuest,
    isAuthenticated,
    authLoading,
    login,
    register,
    continueAsGuest,
    logout,
  }
    return (
    <AuthContext.Provider value={value}>
      {/* Don't render app until Firebase resolves auth state */}
      {!authLoading && children}
    </AuthContext.Provider>
  )
}