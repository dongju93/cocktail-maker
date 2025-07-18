import type React from 'react'

const cocktailTips = [
  {
    id: 'basic-tools',
    title: '기본 도구 준비',
    description: '셰이커, 지거, 바 스푼, 스트레이너를 준비하세요.',
    icon: '🍸',
  },
  {
    id: 'measure-ingredients',
    title: '재료 측정',
    description: '정확한 비율이 맛있는 칵테일의 핵심입니다.',
    icon: '⚖️',
  },
  {
    id: 'ice-usage',
    title: '얼음 사용법',
    description: '신선한 얼음을 사용하고 충분히 넣어주세요.',
    icon: '🧊',
  },
  {
    id: 'garnish-decoration',
    title: '가니쉬 장식',
    description: '시각적 효과와 향을 위한 마지막 터치입니다.',
    icon: '🍋',
  },
]

const popularCocktails = [
  {
    id: 'old-fashioned',
    name: '올드 패션드',
    ingredients: [
      { id: 'whiskey', name: '위스키 60ml' },
      { id: 'sugar', name: '설탕 1티스푼' },
      { id: 'bitters', name: '앙고스투라 비터 2방울' },
      { id: 'ice', name: '얼음' },
      { id: 'orange-peel', name: '오렌지 필' },
    ],
    difficulty: '초급',
    time: '3분',
  },
  {
    id: 'gin-tonic',
    name: '진 토닉',
    ingredients: [
      { id: 'gin', name: '진 50ml' },
      { id: 'tonic-water', name: '토닉워터 150ml' },
      { id: 'lime', name: '라임 1조각' },
      { id: 'ice', name: '얼음' },
    ],
    difficulty: '초급',
    time: '2분',
  },
  {
    id: 'margarita',
    name: '마가리타',
    ingredients: [
      { id: 'tequila', name: '테킬라 50ml' },
      { id: 'triple-sec', name: '트리플섹 25ml' },
      { id: 'lime-juice', name: '라임즙 25ml' },
      { id: 'salt', name: '소금' },
      { id: 'ice', name: '얼음' },
    ],
    difficulty: '중급',
    time: '5분',
  },
]

const CocktailGuide: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-indigo-600 via-purple-600 to-purple-700 px-8 py-20 text-center text-white dark:from-gray-900 dark:via-gray-800 dark:to-gray-800">
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />

        <div className="relative">
          <h1 className="mb-6 animate-float font-black text-6xl text-shadow-lg md:text-7xl">
            🍹 칵테일 제작 가이드
          </h1>
          <p className="mx-auto mb-8 max-w-3xl font-light text-xl leading-relaxed opacity-90">
            프로 바텐더의 비밀을 배워보세요.
            <br />
            기본부터 고급 기법까지, 완벽한 칵테일을 만드는 모든 것을 알려드립니다.
          </p>
          <div className="flex justify-center">
            <div className="rounded-full bg-white/20 px-6 py-3 backdrop-blur-sm">
              <span className="font-semibold text-lg">
                ✨ 50+ 레시피 | 🏆 프로 팁 | 🎯 단계별 가이드
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-8 py-16">
        {/* Quick Tips Section */}
        <section className="mb-20">
          <div className="mb-12 text-center">
            <h2 className="mb-4 font-bold text-4xl text-gray-800 dark:text-white">🚀 핵심 팁</h2>
            <p className="text-gray-600 text-xl dark:text-gray-300">
              성공적인 칵테일을 위한 필수 지식
            </p>
          </div>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
            {cocktailTips.map((tip) => (
              <div
                className="group hover:-translate-y-3 rounded-2xl border border-indigo-100 bg-gradient-to-br from-blue-50 to-indigo-100 p-8 text-center transition-all duration-500 hover:shadow-2xl dark:border-gray-700 dark:from-gray-800 dark:to-gray-700"
                key={tip.id}
              >
                <div className="mb-6 text-5xl transition-transform duration-300 group-hover:scale-110">
                  {tip.icon}
                </div>
                <h3 className="mb-4 font-bold text-gray-800 text-xl dark:text-white">
                  {tip.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">{tip.description}</p>
                <div className="mt-6 h-1 w-0 bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-500 group-hover:w-full" />
              </div>
            ))}
          </div>
        </section>

        {/* Popular Cocktails Section */}
        <section className="mb-20">
          <div className="mb-12 text-center">
            <h2 className="mb-4 font-bold text-4xl text-gray-800 dark:text-white">
              🏆 인기 칵테일 레시피
            </h2>
            <p className="text-gray-600 text-xl dark:text-gray-300">
              가장 사랑받는 클래식 레시피들
            </p>
          </div>
          <div className="grid grid-cols-1 gap-10 md:grid-cols-2 lg:grid-cols-3">
            {popularCocktails.map((cocktail) => (
              <div
                className="group hover:-translate-y-2 relative overflow-hidden rounded-3xl border border-gray-100 bg-white shadow-xl transition-all duration-500 hover:shadow-2xl dark:border-gray-700 dark:bg-gray-800"
                key={cocktail.id}
              >
                {/* Card Header */}
                <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 text-white">
                  <div className="flex items-start justify-between">
                    <h3 className="font-bold text-2xl">{cocktail.name}</h3>
                    <div className="flex flex-col items-end gap-2">
                      <span
                        className={`rounded-full px-4 py-1 font-bold text-sm ${
                          cocktail.difficulty === '초급'
                            ? 'bg-green-400 text-green-900 dark:bg-green-500 dark:text-green-50'
                            : cocktail.difficulty === '중급'
                              ? 'bg-yellow-400 text-yellow-900 dark:bg-yellow-500 dark:text-yellow-50'
                              : 'bg-red-400 text-red-900 dark:bg-red-500 dark:text-red-50'
                        }`}
                      >
                        {cocktail.difficulty}
                      </span>
                      <span className="text-sm opacity-90">⏱️ {cocktail.time}</span>
                    </div>
                  </div>
                </div>

                {/* Card Body */}
                <div className="p-6">
                  <h4 className="mb-4 font-bold text-gray-800 text-lg dark:text-white">📋 재료</h4>
                  <ul className="space-y-3">
                    {cocktail.ingredients.map((ingredient) => (
                      <li
                        className="flex items-center rounded-lg bg-gray-50 p-3 transition-colors duration-300 hover:bg-indigo-50 dark:bg-gray-700 dark:hover:bg-gray-600"
                        key={`${cocktail.id}-${ingredient.id}`}
                      >
                        <span className="mr-3 text-lg">🥃</span>
                        <span className="text-gray-700 dark:text-gray-200">{ingredient.name}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Card Footer */}
                <div className="bg-gray-50 p-4 dark:bg-gray-700">
                  <button
                    className="w-full rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 py-3 font-bold text-white transition-all duration-300 hover:scale-105 hover:shadow-lg"
                    type="button"
                  >
                    📖 상세 레시피 보기
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Advanced Tips Section */}
        <section className="mb-20">
          <div className="rounded-3xl bg-gradient-to-br from-amber-50 to-orange-100 p-8 dark:from-gray-800 dark:to-gray-700">
            <h2 className="mb-8 text-center font-bold text-3xl text-gray-800 dark:text-white">
              🎯 프로 바텐더 팁
            </h2>
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              <div className="rounded-2xl bg-white p-6 shadow-lg dark:bg-gray-800">
                <h3 className="mb-3 font-bold text-orange-600 text-xl dark:text-orange-400">
                  🧊 얼음 마스터하기
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  좋은 얼음은 칵테일의 50%를 좌우합니다. 깨끗하고 단단한 얼음을 사용하고, 칵테일에
                  따라 적절한 크기를 선택하세요.
                </p>
              </div>
              <div className="rounded-2xl bg-white p-6 shadow-lg dark:bg-gray-800">
                <h3 className="mb-3 font-bold text-blue-600 text-xl dark:text-blue-400">
                  ⚖️ 정확한 측정
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  지거(Jigger)를 사용해 정확히 측정하세요. 1ml의 차이도 맛에 큰 영향을 줄 수
                  있습니다.
                </p>
              </div>
              <div className="rounded-2xl bg-white p-6 shadow-lg dark:bg-gray-800">
                <h3 className="mb-3 font-bold text-green-600 text-xl dark:text-green-400">
                  🍸 셰이킹 기술
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  강하고 빠르게 10-15초간 셰이킹하세요. 리듬감 있게 흔들면 더 부드러운 맛을 얻을 수
                  있습니다.
                </p>
              </div>
              <div className="rounded-2xl bg-white p-6 shadow-lg dark:bg-gray-800">
                <h3 className="mb-3 font-bold text-purple-600 text-xl dark:text-purple-400">
                  🍋 가니쉬의 예술
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  가니쉬는 단순한 장식이 아닙니다. 향과 맛을 더하는 중요한 요소입니다.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Safety Section */}
        <section className="mt-16">
          <div className="rounded-3xl border-red-500 border-l-8 bg-gradient-to-br from-red-50 to-pink-100 p-8 dark:from-gray-800 dark:to-gray-700">
            <h2 className="mb-6 flex items-center font-bold text-3xl text-red-700 dark:text-red-400">
              ⚠️ 음주 안전 수칙
            </h2>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {[
                '적당한 음주를 권장합니다',
                '음주 후 운전은 절대 금지입니다',
                '임산부나 미성년자는 음주를 금합니다',
                '약물 복용 시 음주를 피해주세요',
                '빈속에 음주하지 마세요',
                '충분한 수분을 섭취하세요',
              ].map((rule) => (
                <div
                  className="flex items-center rounded-xl bg-white p-4 shadow-sm dark:bg-gray-800"
                  key={rule}
                >
                  <span className="mr-4 text-2xl">✅</span>
                  <span className="font-medium text-gray-700 dark:text-gray-200">{rule}</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

export default CocktailGuide
