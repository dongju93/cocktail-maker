import type React from 'react'
import { useEffect, useState } from 'react'
import { useSessionContext } from 'supertokens-auth-react/recipe/session'

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
                    'http://localhost:8000/api/v1/spirits/앱솔루트 보드카',
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        credentials: 'include', // 중요: 쿠키를 포함하여 요청
                    },
                )

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`)
                }

                const result = await response.json()
                setData(result)
            } catch (err) {
                setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.')
            } finally {
                setLoading(false)
            }
        }

        void fetchData()
    }, [])

    const sessionContext = useSessionContext()

    const renderUserSection = () => {
        if (sessionContext.loading) {
            return (
                <div className="flex items-center gap-2 text-indigo-600 font-medium">
                    로딩 중...
                </div>
            )
        }

        if (!sessionContext.doesSessionExist) {
            return (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-yellow-800">
                    <p>로그인이 필요합니다.</p>
                </div>
            )
        }

        return null
    }

    return (
        <div className="p-8 max-w-6xl mx-auto bg-white min-h-screen">
            <div className="flex justify-between items-start mb-12 pb-8 border-b-2 border-gray-100">
                <h1 className="text-gray-800 text-4xl font-bold m-0">📊 개인 대시보드</h1>
                {renderUserSection()}
            </div>

            <div className="flex flex-col gap-12">
                <div className="bg-gray-50 p-8 rounded-xl border border-gray-200">
                    <div className="mb-8">
                        <h2 className="text-gray-800 mb-2 text-3xl font-bold">🥃 API 연동 데모</h2>
                        <p className="text-gray-600 m-0">
                            백엔드 API와의 연결 상태를 확인할 수 있습니다.
                        </p>
                    </div>

                    <div className="bg-white rounded-xl p-6 shadow-md border border-gray-200">
                        <h3 className="text-gray-800 mb-4 text-xl font-semibold">
                            앱솔루트 보드카 정보
                        </h3>

                        {loading && (
                            <div className="flex justify-center py-8">
                                <div className="flex items-center gap-2 text-indigo-600 font-medium">
                                    데이터 로딩 중...
                                </div>
                            </div>
                        )}

                        {error && (
                            <div className="p-4">
                                <div className="flex items-center gap-2 bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
                                    <span className="text-lg">⚠️</span>
                                    <span>오류: {error}</span>
                                </div>
                            </div>
                        )}

                        {data && (
                            <div className="border border-green-200 rounded-lg overflow-hidden">
                                <div className="bg-green-50 p-4 flex items-center gap-2 text-green-700 font-semibold">
                                    <span className="text-lg">✅</span>
                                    <span>API 연결 성공!</span>
                                </div>
                                <div className="p-4">
                                    <pre className="bg-gray-50 border border-gray-200 rounded p-4 m-0 text-sm overflow-x-auto whitespace-pre-wrap break-words">
                                        {JSON.stringify(data, null, 2)}
                                    </pre>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                <div>
                    <h2 className="text-gray-800 mb-6 text-3xl font-bold">빠른 작업</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="bg-white rounded-xl p-6 text-center shadow-lg border border-gray-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
                            <div className="text-4xl mb-4">📚</div>
                            <h3 className="text-gray-800 mb-2 text-xl font-semibold">
                                가이드 보기
                            </h3>
                            <p className="text-gray-600 mb-6 text-sm">
                                칵테일 제작 가이드를 확인하세요
                            </p>
                            <a
                                href="/guide"
                                className="bg-indigo-600 text-white border-none px-6 py-2 rounded-lg font-semibold cursor-pointer transition-all duration-300 hover:bg-indigo-700 hover:-translate-y-0.5 no-underline inline-block"
                            >
                                가이드로 이동
                            </a>
                        </div>
                        <div className="bg-white rounded-xl p-6 text-center shadow-lg border border-gray-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
                            <div className="text-4xl mb-4">🔍</div>
                            <h3 className="text-gray-800 mb-2 text-xl font-semibold">재료 검색</h3>
                            <p className="text-gray-600 mb-6 text-sm">
                                다양한 칵테일 재료를 검색해보세요
                            </p>
                            <button
                                type="button"
                                className="bg-gray-400 text-white border-none px-6 py-2 rounded-lg font-semibold cursor-not-allowed opacity-60"
                                disabled
                            >
                                개발 예정
                            </button>
                        </div>
                        <div className="bg-white rounded-xl p-6 text-center shadow-lg border border-gray-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
                            <div className="text-4xl mb-4">⭐</div>
                            <h3 className="text-gray-800 mb-2 text-xl font-semibold">즐겨찾기</h3>
                            <p className="text-gray-600 mb-6 text-sm">
                                좋아하는 칵테일을 저장하세요
                            </p>
                            <button
                                type="button"
                                className="bg-gray-400 text-white border-none px-6 py-2 rounded-lg font-semibold cursor-not-allowed opacity-60"
                                disabled
                            >
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
