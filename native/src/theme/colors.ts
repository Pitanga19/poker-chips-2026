import { ThemeColors } from './styled'

// WHITE
export const WHITE = '#fff'

// GRAY
export const GRAY = '#444'
export const GRAY_DARK = '#222'

// RED
export const RED_LIGHT = '#f66'
export const RED = '#e33'
export const RED_DARK = '#922'

export const defaultColors: ThemeColors = {
    // Fondo y texto general
    background: GRAY_DARK,
    text: WHITE,
    
    // Barra de navegación
    navBackground: GRAY_DARK,
    navPressedBackground: GRAY,
    navText: WHITE,
    
    // Tarjetas
    cardBackground: GRAY,
    cardText: WHITE,
    
    // Botones
    buttonBackground: RED,
    buttonPressedBackground: RED_LIGHT,
    buttonDisabledBackground: RED_DARK,
    buttonText: WHITE,
    
    // Inputs
    inputBackground: GRAY_DARK,
    
    // Errores
    error: RED_LIGHT,
  }
