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
        const response = await fetch('http://localhost:8000/api/v1/spirits/앱솔루트 보드카', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include', // 중요: 쿠키를 포함하여 요청
        })

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
      return <div className="flex items-center gap-2 font-medium text-indigo-600">로딩 중...</div>
    }

    if (!sessionContext.doesSessionExist) {
      return (
        <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4 text-yellow-800">
          <p>로그인이 필요합니다.</p>
        </div>
      )
    }

    return null
  }

  return (
    <div className="mx-auto min-h-screen max-w-6xl bg-white p-8">
      <div className="mb-12 flex items-start justify-between border-gray-100 border-b-2 pb-8">
        <h1 className="m-0 font-bold text-4xl text-gray-800">
          <span aria-hidden="true">📊</span> 개인 대시보드
        </h1>
        {renderUserSection()}
      </div>

      <div className="flex flex-col gap-12">
        <div className="rounded-xl border border-gray-200 bg-gray-50 p-8">
          <div className="mb-8">
            <h2 className="mb-2 font-bold text-3xl text-gray-800">
              <span aria-hidden="true">🥃</span> API 연동 데모
            </h2>
            <p className="m-0 text-gray-600">백엔드 API와의 연결 상태를 확인할 수 있습니다.</p>
          </div>

          <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-md">
            <h3 className="mb-4 font-semibold text-gray-800 text-xl">앱솔루트 보드카 정보</h3>

            {loading && (
              <div className="flex justify-center py-8">
                <div className="flex items-center gap-2 font-medium text-indigo-600">
                  데이터 로딩 중...
                </div>
              </div>
            )}

            {error && (
              <div className="p-4">
                <div className="flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
                  <span aria-hidden="true" className="text-lg">
                    ⚠️
                  </span>
                  <span>오류: {error}</span>
                </div>
              </div>
            )}

            {data && (
              <div className="overflow-hidden rounded-lg border border-green-200">
                <div className="flex items-center gap-2 bg-green-50 p-4 font-semibold text-green-700">
                  <span aria-hidden="true" className="text-lg">
                    ✅
                  </span>
                  <span>API 연결 성공!</span>
                </div>
                <div className="p-4">
                  <pre className="m-0 overflow-x-auto whitespace-pre-wrap break-words rounded border border-gray-200 bg-gray-50 p-4 text-sm">
                    {JSON.stringify(data, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </div>
        </div>

        <div>
          <h2 className="mb-6 font-bold text-3xl text-gray-800">빠른 작업</h2>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            <div className="hover:-translate-y-1 rounded-xl border border-gray-200 bg-white p-6 text-center shadow-lg transition-all duration-300 hover:shadow-xl">
              <div aria-hidden="true" className="mb-4 text-4xl">
                📚
              </div>
              <h3 className="mb-2 font-semibold text-gray-800 text-xl">가이드 보기</h3>
              <p className="mb-6 text-gray-600 text-sm">칵테일 제작 가이드를 확인하세요</p>
              <a
                className="hover:-translate-y-0.5 inline-block cursor-pointer rounded-lg border-none bg-indigo-600 px-6 py-2 font-semibold text-white no-underline transition-all duration-300 hover:bg-indigo-700"
                href="/guide"
              >
                가이드로 이동
              </a>
            </div>
            <div className="hover:-translate-y-1 rounded-xl border border-gray-200 bg-white p-6 text-center shadow-lg transition-all duration-300 hover:shadow-xl">
              <div aria-hidden="true" className="mb-4 text-4xl">
                🔍
              </div>
              <h3 className="mb-2 font-semibold text-gray-800 text-xl">재료 검색</h3>
              <p className="mb-6 text-gray-600 text-sm">다양한 칵테일 재료를 검색해보세요</p>
              <button
                className="cursor-not-allowed rounded-lg border-none bg-gray-400 px-6 py-2 font-semibold text-white opacity-60"
                disabled
                type="button"
              >
                개발 예정
              </button>
            </div>
            <div className="hover:-translate-y-1 rounded-xl border border-gray-200 bg-white p-6 text-center shadow-lg transition-all duration-300 hover:shadow-xl">
              <div aria-hidden="true" className="mb-4 text-4xl">
                ⭐
              </div>
              <h3 className="mb-2 font-semibold text-gray-800 text-xl">즐겨찾기</h3>
              <p className="mb-6 text-gray-600 text-sm">좋아하는 칵테일을 저장하세요</p>
              <button
                className="cursor-not-allowed rounded-lg border-none bg-gray-400 px-6 py-2 font-semibold text-white opacity-60"
                disabled
                type="button"
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
