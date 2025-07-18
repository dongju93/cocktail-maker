import type React from 'react'
import { createContext, useEffect, useMemo, useState } from 'react'

export type Theme = 'light' | 'dark' | 'system'

interface ThemeContextType {
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: 'light' | 'dark'
  toggleTheme: () => void
}

export const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

interface ThemeProviderProps {
  children: React.ReactNode
  defaultTheme?: Theme
  storageKey?: string
}

export function ThemeProvider({
  children,
  defaultTheme = 'system',
  storageKey = 'cocktail-maker-theme',
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(defaultTheme)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    const storedTheme = localStorage.getItem(storageKey) as Theme | null
    if (storedTheme) {
      setTheme(storedTheme)
    }
    setMounted(true)
  }, [storageKey])

  // HTML 클래스 설정 및 테마 적용
  useEffect(() => {
    if (!mounted) return

    const root = window.document.documentElement
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    const resolvedTheme = theme === 'system' ? systemTheme : theme

    // 기존 클래스 제거 후 새 클래스 추가
    root.classList.remove('light', 'dark')
    root.classList.add(resolvedTheme)

    localStorage.setItem(storageKey, theme)

    // 시스템 테마 변경 감지 (system 테마일 때만)
    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      const handleChange = () => {
        const newSystemTheme = mediaQuery.matches ? 'dark' : 'light'
        root.classList.remove('light', 'dark')
        root.classList.add(newSystemTheme)
      }

      mediaQuery.addEventListener('change', handleChange)
      return () => mediaQuery.removeEventListener('change', handleChange)
    }
  }, [theme, mounted, storageKey])

  const resolvedTheme = useMemo((): 'light' | 'dark' => {
    if (!mounted) return 'light'
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    return theme === 'system' ? systemTheme : theme
  }, [theme, mounted])

  const toggleTheme = () => {
    setTheme((prevTheme) => {
      const newTheme = prevTheme === 'system' ? 'light' : prevTheme === 'light' ? 'dark' : 'system'
      return newTheme
    })
  }

  const value = {
    theme,
    setTheme,
    resolvedTheme,
    toggleTheme,
  }

  // Always provide context, even when not mounted
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}
