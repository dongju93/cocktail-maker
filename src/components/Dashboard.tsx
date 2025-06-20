import type React from "react"
import { useEffect, useState } from "react"
import { useSessionContext } from "supertokens-auth-react/recipe/session"

const Dashboard: React.FC = () => {
    const [data, setData] = useState<Record<string, unknown> | null>(null)
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true)
            setError(null)

            try {
                // 기본 fetch 사용, SuperTokens가 자동으로 세션 쿠키를 포함
                const response = await fetch(
                    "http://localhost:8000/api/v1/spirits/앱솔루트 보드카",
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        credentials: "include", // 중요: 쿠키를 포함하여 요청
                    },
                )

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`)
                }

                const result = await response.json()
                setData(result)
            } catch (err) {
                setError(err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다.")
            } finally {
                setLoading(false)
            }
        }

        void fetchData()
    }, [])

    const sessionContext = useSessionContext()

    const renderUserSection = () => {
        if (sessionContext.loading) {
            return <div className="loading-spinner">로딩 중...</div>
        }

        if (!sessionContext.doesSessionExist) {
            return (
                <div className="auth-required">
                    <p>로그인이 필요합니다.</p>
                </div>
            )
        }

        return null
    }

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <h1>📊 개인 대시보드</h1>
                {renderUserSection()}
            </div>

            <div className="dashboard-content">
                <div className="api-demo-section">
                    <div className="section-header">
                        <h2>🥃 API 연동 데모</h2>
                        <p>백엔드 API와의 연결 상태를 확인할 수 있습니다.</p>
                    </div>

                    <div className="api-card">
                        <h3>앱솔루트 보드카 정보</h3>

                        {loading && (
                            <div className="loading-state">
                                <div className="loading-spinner">데이터 로딩 중...</div>
                            </div>
                        )}

                        {error && (
                            <div className="error-state">
                                <div className="error-message">
                                    <span className="error-icon">⚠️</span>
                                    <span>오류: {error}</span>
                                </div>
                            </div>
                        )}

                        {data && (
                            <div className="data-display">
                                <div className="data-header">
                                    <span className="success-icon">✅</span>
                                    <span>API 연결 성공!</span>
                                </div>
                                <div className="data-content">
                                    <pre className="json-display">
                                        {JSON.stringify(data, null, 2)}
                                    </pre>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                <div className="quick-actions">
                    <h2>빠른 작업</h2>
                    <div className="actions-grid">
                        <div className="action-card">
                            <div className="action-icon">📚</div>
                            <h3>가이드 보기</h3>
                            <p>칵테일 제작 가이드를 확인하세요</p>
                            <a href="/guide" className="action-btn">
                                가이드로 이동
                            </a>
                        </div>
                        <div className="action-card">
                            <div className="action-icon">🔍</div>
                            <h3>재료 검색</h3>
                            <p>다양한 칵테일 재료를 검색해보세요</p>
                            <button type="button" className="action-btn" disabled>
                                개발 예정
                            </button>
                        </div>
                        <div className="action-card">
                            <div className="action-icon">⭐</div>
                            <h3>즐겨찾기</h3>
                            <p>좋아하는 칵테일을 저장하세요</p>
                            <button type="button" className="action-btn" disabled>
                                개발 예정
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Dashboard
