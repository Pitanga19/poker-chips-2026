import { Platform } from 'react-native'
import * as SecureStore from 'expo-secure-store'

const TOKEN_KEY = 'auth_token'
const WEB = Platform.OS === 'web'

export const authStorage = {
  async getToken(): Promise<string | null> {
    if (WEB) {
      return localStorage.getItem(TOKEN_KEY)
    }
    return await SecureStore.getItemAsync(TOKEN_KEY)
  },
  
  async setToken(token: string): Promise<void> {
    if (WEB) {
      localStorage.setItem(TOKEN_KEY, token)
      return
    }
    await SecureStore.setItemAsync(TOKEN_KEY, token)
  },
  
  async clearToken(): Promise<void> {
    if (WEB) {
      localStorage.removeItem(TOKEN_KEY)
      return
    }
    await SecureStore.deleteItemAsync(TOKEN_KEY)
  },
}
