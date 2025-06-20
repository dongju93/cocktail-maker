import "./App.css"
import type React from "react"
import * as reactRouterDom from "react-router-dom"
import { BrowserRouter, Link, Route, Routes, useNavigate } from "react-router-dom"
import { EmailPasswordPreBuiltUI } from "supertokens-auth-react/recipe/emailpassword/prebuiltui"
import { SessionAuth, signOut, useSessionContext } from "supertokens-auth-react/recipe/session"
import { getSuperTokensRoutesForReactRouterDom } from "supertokens-auth-react/ui"

import CocktailGuide from "./components/CocktailGuide"
import Dashboard from "./components/Dashboard"

const Navigation: React.FC = () => {
    const sessionContext = useSessionContext()
    const navigate = useNavigate()

    const handleLogout = async () => {
        await signOut()
        navigate("/")
    }

    const renderAuthSection = () => {
        if (sessionContext.loading) {
            return <span className="nav-link">로딩중...</span>
        }

        if (sessionContext.doesSessionExist) {
            return (
                <div className="nav-user-section">
                    <span className="nav-user-email">{sessionContext.userId}</span>
                    <button
                        onClick={handleLogout}
                        className="nav-link auth-link logout-btn"
                        type="button"
                    >
                        로그아웃
                    </button>
                </div>
            )
        }

        return (
            <Link to="/auth" className="nav-link auth-link">
                로그인
            </Link>
        )
    }

    return (
        <nav className="main-nav">
            <div className="nav-brand">
                <h2>🍹 Cocktail Maker</h2>
            </div>
            <div className="nav-links">
                <Link to="/" className="nav-link">
                    홈
                </Link>
                <Link to="/guide" className="nav-link">
                    가이드
                </Link>
                <Link to="/dashboard" className="nav-link">
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
            <Navigation />

            <Routes>
                {/* SuperTokens 인증 라우트 */}
                {getSuperTokensRoutesForReactRouterDom(reactRouterDom, [EmailPasswordPreBuiltUI])}

                {/* 일반 라우트 */}
                <Route path="/" element={<Home />} />
                {/* 보호된 라우트 */}
                <Route
                    path="/guide"
                    element={
                        <SessionAuth>
                            <CocktailGuide />
                        </SessionAuth>
                    }
                />
                <Route
                    path="/dashboard"
                    element={
                        <SessionAuth>
                            <Dashboard />
                        </SessionAuth>
                    }
                />
            </Routes>
        </BrowserRouter>
    )
}

const Home: React.FC = () => {
    return (
        <div className="home-page">
            <div className="hero-section">
                <div className="hero-content">
                    <h1>🍹 Cocktail Maker</h1>
                    <p className="hero-subtitle">프로처럼 칵테일을 만들어보세요</p>
                    <div className="hero-buttons">
                        <Link to="/guide" className="btn btn-primary">
                            가이드 보기
                        </Link>
                        <Link to="/dashboard" className="btn btn-secondary">
                            대시보드
                        </Link>
                    </div>
                </div>
            </div>

            <div className="features-section">
                <div className="container">
                    <h2>주요 기능</h2>
                    <div className="features-grid">
                        <div className="feature-card">
                            <div className="feature-icon">📚</div>
                            <h3>칵테일 가이드</h3>
                            <p>기본부터 고급까지 단계별 칵테일 제작 방법을 배워보세요</p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">🥃</div>
                            <h3>재료 관리</h3>
                            <p>다양한 술과 재료 정보를 확인하고 관리하세요</p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">📊</div>
                            <h3>개인 대시보드</h3>
                            <p>나만의 칵테일 레시피와 정보를 저장하고 관리하세요</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default App
