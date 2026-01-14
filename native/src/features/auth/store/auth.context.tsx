import React, { createContext, useContext, useReducer, ReactNode } from 'react'
import { AuthState, AuthAction } from '../types'
import { authReducer, initialAuthState } from './auth.reducer'

type AuthContextValue = {
  state: AuthState
  dispatch: React.Dispatch<AuthAction>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(authReducer, initialAuthState)

  return (
    <AuthContext.Provider value={{ state, dispatch }}>
      {children}
    </AuthContext.Provider>
  )
}

const getContext = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider')
  }
  return context
}

export const useAuthDispatch = () => getContext().dispatch
export const useAuthState = () => getContext().state
