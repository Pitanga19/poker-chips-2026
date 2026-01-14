import { AuthState, AuthAction, AuthActionType } from '../types'

export const initialAuthState: AuthState = {
  token: null,
  user: null,
  isAuthenticated: false,
}

export const authReducer = (
  state: AuthState,
  action: AuthAction,
): AuthState => {
  switch (action.type) {
    case AuthActionType.REGISTER:
    case AuthActionType.LOGIN:
      if (!action.payload) {
        return state
      }
      return {
        token: action.payload.token,
        user: action.payload.user,
        isAuthenticated: true,
      }
    
    case AuthActionType.LOGOUT:
      return initialAuthState
    
    default:
      return state
  }
}
