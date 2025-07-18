import { useContext } from 'react'
import { ThemeContext } from '../contexts/ThemeContext'

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (context === undefined) {
    console.error(
      'useTheme must be used within a ThemeProvider. Please wrap your component tree with <ThemeProvider>.',
    )
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}
