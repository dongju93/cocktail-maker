import type React from 'react'
import { useSessionContext } from 'supertokens-auth-react/recipe/session'
import { useSpirit, useHealthCheck } from '../hooks/useApi'

const Dashboard: React.FC = () => {
  // Use React Query hooks
  const {
    data: spiritData,
    isLoading: spiritLoading,
    error: spiritError,
  } = useSpirit('앱솔루트 보드카')
  const { isLoading: healthLoading, error: healthError } = useHealthCheck()

  const sessionContext = useSessionContext()

  const renderUserSection = () => {
    if (sessionContext.loading) {
      return (
        <div className="flex items-center gap-3">
          <div className="h-3 w-3 animate-spin rounded-full border-2 border-indigo-600 border-t-transparent" />
          <span className="font-medium text-indigo-600">로딩 중...</span>
        </div>
      )
    }

    if (!sessionContext.doesSessionExist) {
      return (
        <div className="rounded-xl border border-yellow-200 bg-yellow-50 p-4 text-yellow-800 dark:border-yellow-600 dark:bg-yellow-900/20 dark:text-yellow-200">
          <p className="flex items-center gap-2">
            <span>⚠️</span>
            로그인이 필요합니다.
          </p>
        </div>
      )
    }

    return (
      <div className="rounded-xl bg-green-50 p-4 dark:bg-green-900/20">
        <div className="flex items-center gap-2 text-green-700 dark:text-green-300">
          <span>👋</span>
          <span className="font-medium">환영합니다!</span>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-indigo-600 via-purple-600 to-purple-700 px-8 py-16 text-white">
        <div className="mx-auto max-w-6xl">
          <div className="flex flex-col items-start justify-between gap-8 md:flex-row md:items-center">
            <div>
              <h1 className="mb-4 font-black text-5xl md:text-6xl">📊 개인 대시보드</h1>
              <p className="font-light text-xl opacity-90">
                당신만의 칵테일 여정을 관리하고 추적해보세요
              </p>
            </div>
            {renderUserSection()}
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-8 py-16">
        {/* Stats Cards */}
        <section className="mb-16">
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
            <div className="rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 p-6 text-white shadow-xl">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-100">제작한 칵테일</p>
                  <p className="font-bold text-3xl">12</p>
                </div>
                <div className="text-4xl opacity-80">🍸</div>
              </div>
            </div>
            <div className="rounded-2xl bg-gradient-to-br from-green-500 to-green-600 p-6 text-white shadow-xl">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-100">즐겨찾기</p>
                  <p className="font-bold text-3xl">5</p>
                </div>
                <div className="text-4xl opacity-80">⭐</div>
              </div>
            </div>
            <div className="rounded-2xl bg-gradient-to-br from-purple-500 to-purple-600 p-6 text-white shadow-xl">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-100">보유 재료</p>
                  <p className="font-bold text-3xl">28</p>
                </div>
                <div className="text-4xl opacity-80">🥃</div>
              </div>
            </div>
            <div className="rounded-2xl bg-gradient-to-br from-orange-500 to-orange-600 p-6 text-white shadow-xl">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-orange-100">레벨</p>
                  <p className="font-bold text-3xl">초급</p>
                </div>
                <div className="text-4xl opacity-80">🏆</div>
              </div>
            </div>
          </div>
        </section>

        {/* API Demo Section */}
        <section className="mb-16">
          <div className="rounded-3xl border border-gray-200 bg-white p-8 shadow-xl dark:border-gray-700 dark:bg-gray-800">
            <div className="mb-8">
              <h2 className="mb-4 font-bold text-3xl text-gray-800 dark:text-white">
                🔗 API 연동 데모
              </h2>
              <p className="text-gray-600 text-lg dark:text-gray-300">
                백엔드 API와의 실시간 연결 상태를 확인할 수 있습니다
              </p>
            </div>

            <div className="rounded-2xl border border-gray-100 bg-gray-50 p-6 dark:border-gray-600 dark:bg-gray-700">
              <h3 className="mb-6 font-bold text-gray-800 text-xl dark:text-white">
                🥃 앱솔루트 보드카 정보
              </h3>

              {(spiritLoading || healthLoading) && (
                <div className="flex flex-col items-center justify-center py-12">
                  <div className="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-indigo-200 border-t-indigo-600 dark:border-indigo-700 dark:border-t-indigo-400" />
                  <p className="font-medium text-indigo-600 text-lg dark:text-indigo-400">
                    데이터를 불러오는 중...
                  </p>
                </div>
              )}

              {(spiritError || healthError) && (
                <div className="rounded-xl border-red-500 border-l-4 bg-red-50 p-6 dark:bg-red-900/20">
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">🚨</span>
                    <div>
                      <h4 className="font-bold text-red-700 dark:text-red-300">연결 오류</h4>
                      <p className="text-red-600 dark:text-red-400">
                        API 연결 오류가 발생했습니다. 잠시 후 다시 시도해주세요.
                      </p>
                      <button
                        className="mt-3 rounded-lg bg-red-600 px-4 py-2 text-white hover:bg-red-700"
                        onClick={() => window.location.reload()}
                        type="button"
                      >
                        다시 시도
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {!!spiritData && (
                <div className="overflow-hidden rounded-xl border border-green-200 bg-white dark:border-green-700 dark:bg-gray-800">
                  <div className="flex items-center gap-3 bg-green-50 p-4 dark:bg-green-900/20">
                    <span className="text-2xl">✅</span>
                    <div>
                      <h4 className="font-bold text-green-700 dark:text-green-300">연결 성공!</h4>
                      <p className="text-green-600 dark:text-green-400">
                        API에서 데이터를 성공적으로 받아왔습니다
                      </p>
                    </div>
                  </div>
                  <div className="p-6">
                    <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-600 dark:bg-gray-700">
                      <div className="text-gray-700 text-sm dark:text-gray-300">
                        데이터가 성공적으로 로드되었습니다.
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Quick Actions */}
        <section className="mb-16">
          <h2 className="mb-8 font-bold text-3xl text-gray-800 dark:text-white">⚡ 빠른 작업</h2>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
            <div className="group hover:-translate-y-2 relative overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-xl transition-all duration-500 hover:shadow-2xl dark:border-gray-700 dark:bg-gray-800">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
              <div className="relative p-8 text-center">
                <div className="mb-6 text-6xl transition-transform duration-300 group-hover:scale-110">
                  📚
                </div>
                <h3 className="mb-4 font-bold text-2xl text-gray-800 dark:text-white">
                  가이드 보기
                </h3>
                <p className="mb-8 text-gray-600 dark:text-gray-300">
                  전문가가 알려주는 칵테일 제작의 모든 것
                </p>
                <a
                  className="inline-block rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 px-8 py-3 font-bold text-white transition-all duration-300 hover:scale-105 hover:shadow-lg"
                  href="/guide"
                >
                  가이드로 이동 →
                </a>
              </div>
            </div>

            <div className="group hover:-translate-y-2 relative overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-xl transition-all duration-500 hover:shadow-2xl dark:border-gray-700 dark:bg-gray-800">
              <div className="absolute inset-0 bg-gradient-to-br from-green-500/10 to-blue-500/10 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
              <div className="relative p-8 text-center">
                <div className="mb-6 text-6xl transition-transform duration-300 group-hover:scale-110">
                  🔍
                </div>
                <h3 className="mb-4 font-bold text-2xl text-gray-800 dark:text-white">재료 검색</h3>
                <p className="mb-8 text-gray-600 dark:text-gray-300">
                  다양한 칵테일 재료를 탐색하고 관리하세요
                </p>
                <button
                  className="inline-block cursor-not-allowed rounded-xl bg-gray-400 px-8 py-3 font-bold text-white opacity-60 dark:bg-gray-600 dark:text-gray-400"
                  disabled
                  type="button"
                >
                  개발 예정 🚧
                </button>
              </div>
            </div>

            <div className="group hover:-translate-y-2 relative overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-xl transition-all duration-500 hover:shadow-2xl dark:border-gray-700 dark:bg-gray-800">
              <div className="absolute inset-0 bg-gradient-to-br from-yellow-500/10 to-orange-500/10 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
              <div className="relative p-8 text-center">
                <div className="mb-6 text-6xl transition-transform duration-300 group-hover:scale-110">
                  ⭐
                </div>
                <h3 className="mb-4 font-bold text-2xl text-gray-800 dark:text-white">즐겨찾기</h3>
                <p className="mb-8 text-gray-600 dark:text-gray-300">
                  좋아하는 칵테일을 저장하고 관리하세요
                </p>
                <button
                  className="inline-block cursor-not-allowed rounded-xl bg-gray-400 px-8 py-3 font-bold text-white opacity-60 dark:bg-gray-600 dark:text-gray-400"
                  disabled
                  type="button"
                >
                  개발 예정 🚧
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Recent Activity */}
        <section>
          <h2 className="mb-8 font-bold text-3xl text-gray-800 dark:text-white">📈 최근 활동</h2>
          <div className="rounded-3xl border border-gray-200 bg-white p-8 shadow-xl dark:border-gray-700 dark:bg-gray-800">
            <div className="space-y-6">
              {[
                { icon: '🍸', action: '마가리타 레시피를 확인했습니다', time: '2시간 전' },
                { icon: '📚', action: '칵테일 가이드를 읽었습니다', time: '5시간 전' },
                { icon: '⭐', action: '올드 패션드를 즐겨찾기에 추가했습니다', time: '1일 전' },
                { icon: '🥃', action: '위스키 정보를 조회했습니다', time: '2일 전' },
              ].map((activity) => (
                <div
                  className="flex items-center gap-4 rounded-xl bg-gray-50 p-4 dark:bg-gray-700"
                  key={activity.action}
                >
                  <div className="text-2xl">{activity.icon}</div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-800 dark:text-white">{activity.action}</p>
                    <p className="text-gray-500 text-sm dark:text-gray-400">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

export default Dashboard
