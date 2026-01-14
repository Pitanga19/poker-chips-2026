import axios from 'axios'
import { authStorage } from '../features/auth/storage/auth.storage'

export const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
})

api.interceptors.request.use((config) => {
  const token = authStorage.getToken()
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  
  return config
})
