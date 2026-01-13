import { ThemeProvider as StyledThemeProvider } from 'styled-components/native'
import { defaultTheme } from './defaultTheme'

export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <StyledThemeProvider theme={defaultTheme}>
      {children}
    </StyledThemeProvider>
  )
}
