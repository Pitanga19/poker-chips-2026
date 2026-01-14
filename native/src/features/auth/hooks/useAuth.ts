import { useAuthDispatch, useAuthState } from '../store'
import { authStorage } from '../storage/auth.storage'
import { AuthActionType, AuthRegisterData, AuthLoginData, AuthResponse } from '../types'
import { registerUser, loginUser, getMe, logout as logoutUser } from '../../../api/auth'

export const useAuth = () => {
  const dispatch = useAuthDispatch()
  const state = useAuthState()
  
  const register = async (payload: AuthRegisterData): Promise<AuthResponse> => {
    const response = await registerUser(payload)
    
    authStorage.setToken(response.token.access_token)
    
    dispatch({ type: AuthActionType.REGISTER, payload: response })
    return response
  }
  
  const login = async (payload: AuthLoginData): Promise<AuthResponse> => {
    const response = await loginUser(payload)
    
    authStorage.setToken(response.token.access_token)
    
    dispatch({ type: AuthActionType.LOGIN, payload: response })
    return response
  }
  
  const hydrate = async (): Promise<void> => {
    const storage_token = authStorage.getToken()
    if (!storage_token) return
    
    try {
      const user = await getMe()
      const token = {
        access_token: storage_token,
        token_type: 'bearer',
      }
      
      dispatch({
        type: AuthActionType.LOGIN,
        payload: { token, user }
      })
    } catch {
      authStorage.clearToken()
      dispatch({ type: AuthActionType.LOGOUT })
    }
  }
  
  const logout = async (): Promise<void> => {
    await logoutUser()
    authStorage.clearToken()
    dispatch({ type: AuthActionType.LOGOUT })
  }
  
  return {
    ...state,
    register,
    login,
    logout,
    hydrate,
  }
}
