import { api } from './client'
import {
  UserRead, AuthRegisterData, AuthLoginData, AuthResponse,
} from '../features/auth/types'

export const registerUser = async (payload: AuthRegisterData): Promise<AuthResponse> => {
  const { data } = await api.post('/auth/register', payload)
  return data
}
export const loginUser = async (payload: AuthLoginData): Promise<AuthResponse> => {
  const { data } = await api.post('/auth/login', payload)
  return data
}
export const getMe = async (): Promise<UserRead> => {
  const { data } = await api.get('/auth/me')
  return data
}
export const logout = async (): Promise<void> => {
  const { data } = await api.post('/auth/logout')
  return data
}
