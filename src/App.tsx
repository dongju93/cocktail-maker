import type React from 'react'
import { lazy, Suspense } from 'react'
import * as reactRouterDom from 'react-router-dom'
import { BrowserRouter, Link, Route, Routes, useNavigate } from 'react-router-dom'
import { EmailPasswordPreBuiltUI } from 'supertokens-auth-react/recipe/emailpassword/prebuiltui'
import { SessionAuth, signOut, useSessionContext } from 'supertokens-auth-react/recipe/session'
import { getSuperTokensRoutesForReactRouterDom } from 'supertokens-auth-react/ui'

const CocktailGuide = lazy(() => import('./components/CocktailGuide'))
const Dashboard = lazy(() => import('./components/Dashboard'))

import ThemeToggle from './components/ThemeToggle'
import { ThemeProvider } from './contexts/ThemeContext'

const Navigation: React.FC = () => {
  const sessionContext = useSessionContext()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await signOut()
    await navigate('/')
  }

  const renderAuthSection = () => {
    if (sessionContext.loading) {
      return (
        <span className="px-4 py-2 font-medium text-gray-700 dark:text-gray-300">로딩중...</span>
      )
    }

    if (sessionContext.doesSessionExist) {
      return (
        <div className="flex items-center gap-4">
          <span className="font-medium text-gray-700 text-sm dark:text-gray-300">
            {sessionContext.userId}
          </span>
          <button
            className="hover:-translate-y-0.5 rounded-lg bg-blue-600 px-6 py-2 font-medium text-white transition-all duration-300 hover:bg-blue-700"
            onClick={handleLogout}
            type="button"
          >
            로그아웃
          </button>
        </div>
      )
    }

    return (
      <Link
        className="hover:-translate-y-0.5 rounded-lg bg-blue-600 px-6 py-2 font-medium text-white transition-all duration-300 hover:bg-blue-700"
        to="/auth"
      >
        로그인
      </Link>
    )
  }

  return (
    <nav className="sticky top-0 z-50 flex items-center justify-between border-border border-b bg-background/95 px-8 py-4 backdrop-blur-md">
      <div>
        <h2 className="font-bold text-2xl text-primary">🍹 Cocktail Maker</h2>
      </div>
      <div className="flex items-center gap-8">
        <Link
          className="rounded-lg px-4 py-2 font-medium text-text-secondary transition-all duration-300 hover:bg-primary/10 hover:text-primary"
          to="/"
        >
          홈
        </Link>
        <Link
          className="rounded-lg px-4 py-2 font-medium text-text-secondary transition-all duration-300 hover:bg-primary/10 hover:text-primary"
          to="/guide"
        >
          가이드
        </Link>
        <Link
          className="rounded-lg px-4 py-2 font-medium text-text-secondary transition-all duration-300 hover:bg-primary/10 hover:text-primary"
          to="/dashboard"
        >
          대시보드
        </Link>
        <ThemeToggle />
        {renderAuthSection()}
      </div>
    </nav>
  )
}

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </ThemeProvider>
  )
}

const AppContent: React.FC = () => {
  return (
    <div className="min-h-screen w-full bg-background text-foreground">
      <Navigation />

      <Routes>
        {/* SuperTokens 인증 라우트 */}
        {getSuperTokensRoutesForReactRouterDom(reactRouterDom, [EmailPasswordPreBuiltUI])}

        {/* 일반 라우트 */}
        <Route element={<Home />} path="/" />
        {/* 보호된 라우트 */}
        <Route
          element={
            <SessionAuth>
              <Suspense fallback={<div>로딩 중...</div>}>
                <CocktailGuide />
              </Suspense>
            </SessionAuth>
          }
          path="/guide"
        />
        <Route
          element={
            <SessionAuth>
              <Suspense fallback={<div>로딩 중...</div>}>
                <Dashboard />
              </Suspense>
            </SessionAuth>
          }
          path="/dashboard"
        />
      </Routes>
    </div>
  )
}

const Home: React.FC = () => {
  return (
    <>
      {/* Hero Section - Dark gradient for better contrast */}
      <div className="relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 px-8 py-20 text-center">
        {/* Background decoration */}
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />

        <div className="relative animate-fade-in">
          <h1 className="mb-6 animate-float font-black text-7xl text-shadow-lg text-white tracking-tight md:text-8xl">
            🍹 Cocktail Maker
          </h1>
          <p className="mx-auto mb-12 max-w-2xl font-light text-2xl text-gray-100 leading-relaxed">
            프로 바텐더처럼 완벽한 칵테일을 만들어보세요.
            <br />
            <span className="text-yellow-300">당신만의 특별한 레시피</span>를 발견하세요.
          </p>
          <div className="flex flex-wrap justify-center gap-6">
            <Link
              className="group hover:-translate-y-2 relative overflow-hidden rounded-full bg-white px-10 py-4 font-bold text-gray-900 text-lg transition-all duration-500 hover:shadow-2xl"
              to="/guide"
            >
              <span className="relative z-10">🎯 가이드 시작하기</span>
              <div className="absolute inset-0 scale-x-0 bg-gradient-to-r from-primary to-secondary transition-transform duration-300 group-hover:scale-x-100" />
            </Link>
            <Link
              className="group hover:-translate-y-2 rounded-full border-2 border-white/30 bg-white/10 px-10 py-4 font-bold text-lg text-white backdrop-blur-sm transition-all duration-500 hover:bg-white hover:text-gray-900 hover:shadow-2xl"
              to="/dashboard"
            >
              📊 대시보드 보기
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-background py-20">
        <div className="mx-auto max-w-6xl px-8">
          <h2 className="mb-12 text-center font-bold text-4xl text-text-primary">주요 기능</h2>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div className="hover:-translate-y-2 rounded-2xl border border-border bg-background p-8 text-center shadow-xl transition-all duration-300 hover:shadow-2xl">
              <div className="mb-4 animate-scale-in text-5xl">📚</div>
              <h3 className="mb-4 font-semibold text-text-primary text-xl">칵테일 가이드</h3>
              <p className="text-text-secondary leading-relaxed">
                기본부터 고급까지 단계별 칵테일 제작 방법을 배워보세요
              </p>
            </div>
            <div className="hover:-translate-y-2 rounded-2xl border border-border bg-background p-8 text-center shadow-xl transition-all duration-300 hover:shadow-2xl">
              <div className="mb-4 animate-scale-in text-5xl">🥃</div>
              <h3 className="mb-4 font-semibold text-text-primary text-xl">재료 관리</h3>
              <p className="text-text-secondary leading-relaxed">
                다양한 술과 재료 정보를 확인하고 관리하세요
              </p>
            </div>
            <div className="hover:-translate-y-2 rounded-2xl border border-border bg-background p-8 text-center shadow-xl transition-all duration-300 hover:shadow-2xl">
              <div className="mb-4 animate-scale-in text-5xl">📊</div>
              <h3 className="mb-4 font-semibold text-text-primary text-xl">개인 대시보드</h3>
              <p className="text-text-secondary leading-relaxed">
                나만의 칵테일 레시피와 정보를 저장하고 관리하세요
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-gradient-to-r from-primary to-secondary py-16">
        <div className="mx-auto max-w-6xl px-8">
          <div className="grid grid-cols-1 gap-8 text-center text-white md:grid-cols-3">
            <div className="rounded-xl bg-white/10 p-8 backdrop-blur-sm">
              <div className="font-bold text-4xl">100+</div>
              <div className="text-lg opacity-90">칵테일 레시피</div>
            </div>
            <div className="rounded-xl bg-white/10 p-8 backdrop-blur-sm">
              <div className="font-bold text-4xl">50+</div>
              <div className="text-lg opacity-90">기본 재료</div>
            </div>
            <div className="rounded-xl bg-white/10 p-8 backdrop-blur-sm">
              <div className="font-bold text-4xl">24/7</div>
              <div className="text-lg opacity-90">언제든 이용 가능</div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-background py-20">
        <div className="mx-auto max-w-4xl px-8 text-center">
          <h2 className="mb-6 font-bold text-4xl text-text-primary">지금 시작해보세요!</h2>
          <p className="mb-8 text-text-secondary text-xl">
            완벽한 칵테일을 만들어보고 친구들과 공유해보세요
          </p>
          <Link
            className="inline-block rounded-full bg-gradient-to-r from-primary to-secondary px-12 py-4 font-bold text-lg text-white transition-all duration-300 hover:scale-105 hover:shadow-xl"
            to="/guide"
          >
            지금 시작하기 →
          </Link>
        </div>
      </div>
    </>
  )
}

export default App
