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
            return <span className="text-gray-800 font-medium px-4 py-2">로딩중...</span>
        }

        if (sessionContext.doesSessionExist) {
            return (
                <div className="flex items-center gap-4">
                    <span className="text-gray-800 font-medium text-sm">
                        {sessionContext.userId}
                    </span>
                    <button
                        className="bg-indigo-600 text-white px-6 py-2 rounded-lg font-medium transition-all duration-300 hover:bg-indigo-700 hover:-translate-y-0.5"
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
                className="bg-indigo-600 text-white px-6 py-2 rounded-lg font-medium transition-all duration-300 hover:bg-indigo-700 hover:-translate-y-0.5"
                to="/auth"
            >
                로그인
            </Link>
        )
    }

    return (
        <nav className="bg-white/95 backdrop-blur-md border-b border-white/20 px-8 py-4 flex justify-between items-center sticky top-0 z-50">
            <div>
                <h2 className="text-indigo-600 font-bold text-2xl">🍹 Cocktail Maker</h2>
            </div>
            <div className="flex gap-8 items-center">
                <Link
                    className="text-gray-800 font-medium px-4 py-2 rounded-lg transition-all duration-300 hover:bg-indigo-100 hover:text-indigo-600"
                    to="/"
                >
                    홈
                </Link>
                <Link
                    className="text-gray-800 font-medium px-4 py-2 rounded-lg transition-all duration-300 hover:bg-indigo-100 hover:text-indigo-600"
                    to="/guide"
                >
                    가이드
                </Link>
                <Link
                    className="text-gray-800 font-medium px-4 py-2 rounded-lg transition-all duration-300 hover:bg-indigo-100 hover:text-indigo-600"
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
            <div className="min-h-screen flex flex-col max-w-7xl mx-auto w-full bg-gradient-to-br from-indigo-600 to-purple-700">
                <Navigation />

                <Routes>
                    {/* SuperTokens 인증 라우트 */}
                    {getSuperTokensRoutesForReactRouterDom(reactRouterDom, [
                        EmailPasswordPreBuiltUI,
                    ])}

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
            <div className="bg-gradient-to-br from-indigo-600 to-purple-700 py-16 px-8 text-center text-white">
                <div>
                    <h1 className="text-6xl font-extrabold mb-4 text-shadow-lg">
                        🍹 Cocktail Maker
                    </h1>
                    <p className="text-xl mb-8 opacity-90">프로처럼 칵테일을 만들어보세요</p>
                    <div className="flex gap-4 justify-center flex-wrap">
                        <Link
                            className="bg-white text-indigo-600 px-8 py-3 rounded-full font-semibold transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl"
                            to="/guide"
                        >
                            가이드 보기
                        </Link>
                        <Link
                            className="bg-transparent text-white border-2 border-white px-8 py-3 rounded-full font-semibold transition-all duration-300 hover:bg-white hover:text-indigo-600"
                            to="/dashboard"
                        >
                            대시보드
                        </Link>
                    </div>
                </div>
            </div>

            <div className="bg-white py-16">
                <div className="max-w-6xl mx-auto px-8">
                    <h2 className="text-center text-4xl font-bold mb-12 text-gray-800">
                        주요 기능
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="bg-white p-8 rounded-2xl text-center shadow-xl border border-gray-50 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl">
                            <div className="text-5xl mb-4">📚</div>
                            <h3 className="text-gray-800 mb-4 text-xl font-semibold">
                                칵테일 가이드
                            </h3>
                            <p className="text-gray-600 leading-relaxed">
                                기본부터 고급까지 단계별 칵테일 제작 방법을 배워보세요
                            </p>
                        </div>
                        <div className="bg-white p-8 rounded-2xl text-center shadow-xl border border-gray-50 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl">
                            <div className="text-5xl mb-4">🥃</div>
                            <h3 className="text-gray-800 mb-4 text-xl font-semibold">재료 관리</h3>
                            <p className="text-gray-600 leading-relaxed">
                                다양한 술과 재료 정보를 확인하고 관리하세요
                            </p>
                        </div>
                        <div className="bg-white p-8 rounded-2xl text-center shadow-xl border border-gray-50 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl">
                            <div className="text-5xl mb-4">📊</div>
                            <h3 className="text-gray-800 mb-4 text-xl font-semibold">
                                개인 대시보드
                            </h3>
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
