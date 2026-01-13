import 'styled-components/native'

export interface ThemeTypography {
  fontFamily: string
  
  sizes: {
    xs: number
    sm: number
    md: number
    lg: number
    xl: number
  },
  
  lineHeights: {
    xs: number
    sm: number
    md: number
    lg: number
    xl: number
  },
  
  weights: {
    regular: number
    medium: number
    bold: number
  },
}

export interface ThemeSpacing {
  xs: number
  sm: number
  md: number
  lg: number
  xl: number
}

export interface ThemeColors {
    // Fondo y texto general
    background: string
    text: string
    
    // Barra de navegación
    navBackground: string
    navPressedBackground: string
    navText: string
    
    // Tarjetas
    cardBackground: string
    cardText: string
    
    // Botones
    buttonBackground: string
    buttonPressedBackground: string
    buttonDisabledBackground: string
    buttonText: string
    
    // Inputs
    inputBackground: string
    
    // Errores
    error: string
}

export interface ThemeRadii {
  sm: number
  md: number
  lg: number
}

declare module 'styled-components/native' {
  export interface DefaultTheme {
    typography: ThemeTypography
    spacing: ThemeSpacing
    colors: ThemeColors
    radii: ThemeRadii
  }
}
