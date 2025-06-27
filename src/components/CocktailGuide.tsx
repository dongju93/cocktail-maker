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
    <div className="min-h-screen bg-white">
      <div className="bg-gradient-to-br from-indigo-600 to-purple-700 px-8 py-16 text-center text-white">
        <div>
          <h1 className="mb-4 font-extrabold text-6xl text-shadow-lg">🍹 칵테일 제작 가이드</h1>
          <p className="text-xl opacity-90">
            프로처럼 칵테일을 만들어보세요. 기본부터 고급 기법까지!
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-6xl px-8 pb-16">
        <section className="mb-16">
          <h2 className="mb-8 text-center font-bold text-4xl text-gray-800">기본 팁</h2>
          <div className="mb-12 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
            {cocktailTips.map((tip) => (
              <div
                className="hover:-translate-y-1 rounded-xl border border-indigo-100 bg-gradient-to-br from-blue-50 to-indigo-100 p-6 text-center transition-all duration-300 hover:shadow-lg"
                key={tip.id}
              >
                <div className="mb-4 text-4xl">{tip.icon}</div>
                <h3 className="mb-2 font-semibold text-gray-800 text-lg">{tip.title}</h3>
                <p className="text-gray-600 text-sm">{tip.description}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mb-16">
          <h2 className="mb-8 text-center font-bold text-4xl text-gray-800">인기 칵테일 레시피</h2>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
            {popularCocktails.map((cocktail) => (
              <div
                className="hover:-translate-y-1 rounded-xl border border-gray-50 bg-white p-6 shadow-lg transition-all duration-300 hover:shadow-xl"
                key={cocktail.id}
              >
                <div className="mb-4 flex items-start justify-between">
                  <h3 className="font-semibold text-gray-800 text-xl">{cocktail.name}</h3>
                  <div className="flex flex-col items-end gap-2">
                    <span
                      className={`rounded-xl px-3 py-1 font-semibold text-xs ${
                        cocktail.difficulty === '초급'
                          ? 'bg-green-100 text-green-700'
                          : cocktail.difficulty === '중급'
                            ? 'bg-orange-100 text-orange-700'
                            : 'bg-red-100 text-red-700'
                      }`}
                    >
                      {cocktail.difficulty}
                    </span>
                    <span className="text-gray-600 text-xs">⏱️ {cocktail.time}</span>
                  </div>
                </div>
                <div>
                  <h4 className="mb-2 font-medium text-base text-gray-800">재료</h4>
                  <ul className="list-none">
                    {cocktail.ingredients.map((ingredient) => (
                      <li
                        className="border-gray-100 border-b py-1 text-gray-700 before:mr-2 before:content-['🥃'] last:border-b-0"
                        key={`${cocktail.id}-${ingredient.id}`}
                      >
                        {ingredient.name}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-12">
          <div className="rounded-xl border-pink-500 border-l-4 bg-gradient-to-br from-red-50 to-pink-100 p-8">
            <h2 className="mb-4 font-bold text-2xl text-pink-700">⚠️ 음주 안전 수칙</h2>
            <ul className="list-none">
              <li className="relative py-2 pl-6 text-gray-700 before:absolute before:left-0 before:font-bold before:text-pink-500 before:content-['✓']">
                적당한 음주를 권장합니다
              </li>
              <li className="relative py-2 pl-6 text-gray-700 before:absolute before:left-0 before:font-bold before:text-pink-500 before:content-['✓']">
                음주 후 운전은 절대 금지입니다
              </li>
              <li className="relative py-2 pl-6 text-gray-700 before:absolute before:left-0 before:font-bold before:text-pink-500 before:content-['✓']">
                임산부나 미성년자는 음주를 금합니다
              </li>
              <li className="relative py-2 pl-6 text-gray-700 before:absolute before:left-0 before:font-bold before:text-pink-500 before:content-['✓']">
                약물 복용 시 음주를 피해주세요
              </li>
            </ul>
          </div>
        </section>
      </div>
    </div>
  )
}

export default CocktailGuide
