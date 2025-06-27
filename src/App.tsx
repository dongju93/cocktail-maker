import type React from 'react'
import * as reactRouterDom from 'react-router-dom'
import { BrowserRouter, Link, Route, Routes, useNavigate } from 'react-router-dom'
import { EmailPasswordPreBuiltUI } from 'supertokens-auth-react/recipe/emailpassword/prebuiltui'
import { SessionAuth, signOut, useSessionContext } from 'supertokens-auth-react/recipe/session'
import { getSuperTokensRoutesForReactRouterDom } from 'supertokens-auth-react/ui'

import CocktailGuide from './components/CocktailGuide'
import Dashboard from './components/Dashboard'

const Navigation: React.FC = () => {
  const sessionContext = useSessionContext()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await signOut()
    navigate('/')
  }

  const renderAuthSection = () => {
    if (sessionContext.loading) {
      return <span className="px-4 py-2 font-medium text-gray-800">로딩중...</span>
    }

    if (sessionContext.doesSessionExist) {
      return (
        <div className="flex items-center gap-4">
          <span className="font-medium text-gray-800 text-sm">{sessionContext.userId}</span>
          <button
            className="hover:-translate-y-0.5 rounded-lg bg-indigo-600 px-6 py-2 font-medium text-white transition-all duration-300 hover:bg-indigo-700"
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
        className="hover:-translate-y-0.5 rounded-lg bg-indigo-600 px-6 py-2 font-medium text-white transition-all duration-300 hover:bg-indigo-700"
        to="/auth"
      >
        로그인
      </Link>
    )
  }

  return (
    <nav className="sticky top-0 z-50 flex items-center justify-between border-white/20 border-b bg-white/95 px-8 py-4 backdrop-blur-md">
      <div>
        <h2 className="font-bold text-2xl text-indigo-600">🍹 Cocktail Maker</h2>
      </div>
      <div className="flex items-center gap-8">
        <Link
          className="rounded-lg px-4 py-2 font-medium text-gray-800 transition-all duration-300 hover:bg-indigo-100 hover:text-indigo-600"
          to="/"
        >
          홈
        </Link>
        <Link
          className="rounded-lg px-4 py-2 font-medium text-gray-800 transition-all duration-300 hover:bg-indigo-100 hover:text-indigo-600"
          to="/guide"
        >
          가이드
        </Link>
        <Link
          className="rounded-lg px-4 py-2 font-medium text-gray-800 transition-all duration-300 hover:bg-indigo-100 hover:text-indigo-600"
          to="/dashboard"
        >
          대시보드
        </Link>
        {renderAuthSection()}
      </div>
    </nav>
  )
}

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col bg-gradient-to-br from-indigo-600 to-purple-700">
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
                <CocktailGuide />
              </SessionAuth>
            }
            path="/guide"
          />
          <Route
            element={
              <SessionAuth>
                <Dashboard />
              </SessionAuth>
            }
            path="/dashboard"
          />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

const Home: React.FC = () => {
  return (
    <div>
      <div className="bg-gradient-to-br from-indigo-600 to-purple-700 px-8 py-16 text-center text-white">
        <div>
          <h1 className="mb-4 font-extrabold text-6xl text-shadow-lg">🍹 Cocktail Maker</h1>
          <p className="mb-8 text-xl opacity-90">프로처럼 칵테일을 만들어보세요</p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              className="hover:-translate-y-1 rounded-full bg-white px-8 py-3 font-semibold text-indigo-600 transition-all duration-300 hover:shadow-2xl"
              to="/guide"
            >
              가이드 보기
            </Link>
            <Link
              className="rounded-full border-2 border-white bg-transparent px-8 py-3 font-semibold text-white transition-all duration-300 hover:bg-white hover:text-indigo-600"
              to="/dashboard"
            >
              대시보드
            </Link>
          </div>
        </div>
      </div>

      <div className="bg-white py-16">
        <div className="mx-auto max-w-6xl px-8">
          <h2 className="mb-12 text-center font-bold text-4xl text-gray-800">주요 기능</h2>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div className="hover:-translate-y-2 rounded-2xl border border-gray-50 bg-white p-8 text-center shadow-xl transition-all duration-300 hover:shadow-2xl">
              <div className="mb-4 text-5xl">📚</div>
              <h3 className="mb-4 font-semibold text-gray-800 text-xl">칵테일 가이드</h3>
              <p className="text-gray-600 leading-relaxed">
                기본부터 고급까지 단계별 칵테일 제작 방법을 배워보세요
              </p>
            </div>
            <div className="hover:-translate-y-2 rounded-2xl border border-gray-50 bg-white p-8 text-center shadow-xl transition-all duration-300 hover:shadow-2xl">
              <div className="mb-4 text-5xl">🥃</div>
              <h3 className="mb-4 font-semibold text-gray-800 text-xl">재료 관리</h3>
              <p className="text-gray-600 leading-relaxed">
                다양한 술과 재료 정보를 확인하고 관리하세요
              </p>
            </div>
            <div className="hover:-translate-y-2 rounded-2xl border border-gray-50 bg-white p-8 text-center shadow-xl transition-all duration-300 hover:shadow-2xl">
              <div className="mb-4 text-5xl">📊</div>
              <h3 className="mb-4 font-semibold text-gray-800 text-xl">개인 대시보드</h3>
              <p className="text-gray-600 leading-relaxed">
                나만의 칵테일 레시피와 정보를 저장하고 관리하세요
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
