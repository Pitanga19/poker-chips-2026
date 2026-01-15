import axios from 'axios'
import { authStorage } from '../features/auth/storage/auth.storage'

export const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL,
  timeout: 10000,
})

api.interceptors.request.use(
  async (config) => {
    const token = await authStorage.getToken()
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)
