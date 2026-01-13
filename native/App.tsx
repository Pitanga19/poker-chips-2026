import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { ThemeProvider } from './src/theme/ThemeProvider'
import { GlobalStyle } from './src/theme/GlobalStyle'
import AppNavigator from './src/navigation/AppNavigator'

export default function App() {
  return (
    <ThemeProvider>
      <GlobalStyle>
        <NavigationContainer>
          <AppNavigator />
        </NavigationContainer>
      </GlobalStyle>
    </ThemeProvider>
  )
}
