import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { ThemeProvider } from './src/theme/ThemeProvider'
import { GlobalStyle } from './src/theme/GlobalStyle'
import { AuthProvider } from './src/features/auth/store'
import AppNavigator from './src/navigation/AppNavigator'

export default function App() {
  return (
    <ThemeProvider>
      <GlobalStyle>
        <AuthProvider>
          <NavigationContainer>
            <AppNavigator />
          </NavigationContainer>
        </AuthProvider>
      </GlobalStyle>
    </ThemeProvider>
  )
}
