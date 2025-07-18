import type React from 'react'
import { useTheme } from '../hooks/useTheme'

const ThemeToggle: React.FC = () => {
  const { theme, toggleTheme, resolvedTheme } = useTheme()

  const getIcon = () => {
    switch (theme) {
      case 'light':
        return '☀️'
      case 'dark':
        return '🌙'
      default:
        return resolvedTheme === 'dark' ? '🌙' : '☀️'
    }
  }

  const getLabel = () => {
    switch (theme) {
      case 'light':
        return '라이트 모드'
      case 'dark':
        return '다크 모드'
      default:
        return '시스템 설정'
    }
  }

  return (
    <button
      aria-label={`현재 테마: ${getLabel()}. 클릭하여 테마를 변경합니다.`}
      className="group relative rounded-lg p-2 text-gray-600 transition-all duration-300 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-gray-300 dark:hover:bg-gray-800"
      onClick={toggleTheme}
      type="button"
    >
      <div className="relative flex items-center justify-center">
        <span className="text-xl transition-transform duration-300 group-hover:rotate-12">
          {getIcon()}
        </span>
        <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-30" />
      </div>

      {/* Tooltip */}
      <div className="-bottom-10 -translate-x-1/2 absolute left-1/2 whitespace-nowrap rounded-md bg-gray-800 px-2 py-1 text-white text-xs opacity-0 transition-opacity duration-200 group-hover:opacity-100 dark:bg-gray-600">
        {getLabel()}
      </div>
    </button>
  )
}

export default ThemeToggle
