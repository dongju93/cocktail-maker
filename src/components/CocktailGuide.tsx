import type React from "react"

const CocktailGuide: React.FC = () => {
    const cocktailTips = [
        {
            id: "basic-tools",
            title: "기본 도구 준비",
            description: "셰이커, 지거, 바 스푼, 스트레이너를 준비하세요.",
            icon: "🍸",
        },
        {
            id: "measure-ingredients",
            title: "재료 측정",
            description: "정확한 비율이 맛있는 칵테일의 핵심입니다.",
            icon: "⚖️",
        },
        {
            id: "ice-usage",
            title: "얼음 사용법",
            description: "신선한 얼음을 사용하고 충분히 넣어주세요.",
            icon: "🧊",
        },
        {
            id: "garnish-decoration",
            title: "가니쉬 장식",
            description: "시각적 효과와 향을 위한 마지막 터치입니다.",
            icon: "🍋",
        },
    ]

    const popularCocktails = [
        {
            id: "old-fashioned",
            name: "올드 패션드",
            ingredients: [
                { id: "whiskey", name: "위스키 60ml" },
                { id: "sugar", name: "설탕 1티스푼" },
                { id: "bitters", name: "앙고스투라 비터 2방울" },
                { id: "ice", name: "얼음" },
                { id: "orange-peel", name: "오렌지 필" },
            ],
            difficulty: "초급",
            time: "3분",
        },
        {
            id: "gin-tonic",
            name: "진 토닉",
            ingredients: [
                { id: "gin", name: "진 50ml" },
                { id: "tonic-water", name: "토닉워터 150ml" },
                { id: "lime", name: "라임 1조각" },
                { id: "ice", name: "얼음" },
            ],
            difficulty: "초급",
            time: "2분",
        },
        {
            id: "margarita",
            name: "마가리타",
            ingredients: [
                { id: "tequila", name: "테킬라 50ml" },
                { id: "triple-sec", name: "트리플섹 25ml" },
                { id: "lime-juice", name: "라임즙 25ml" },
                { id: "salt", name: "소금" },
                { id: "ice", name: "얼음" },
            ],
            difficulty: "중급",
            time: "5분",
        },
    ]

    return (
        <div className="cocktail-guide">
            <div className="hero-section">
                <div className="hero-content">
                    <h1>🍹 칵테일 제작 가이드</h1>
                    <p>프로처럼 칵테일을 만들어보세요. 기본부터 고급 기법까지!</p>
                </div>
            </div>

            <div className="content-container">
                <section className="tips-section">
                    <h2>기본 팁</h2>
                    <div className="tips-grid">
                        {cocktailTips.map((tip) => (
                            <div key={tip.id} className="tip-card">
                                <div className="tip-icon">{tip.icon}</div>
                                <h3>{tip.title}</h3>
                                <p>{tip.description}</p>
                            </div>
                        ))}
                    </div>
                </section>

                <section className="recipes-section">
                    <h2>인기 칵테일 레시피</h2>
                    <div className="recipes-grid">
                        {popularCocktails.map((cocktail) => (
                            <div key={cocktail.id} className="recipe-card">
                                <div className="recipe-header">
                                    <h3>{cocktail.name}</h3>
                                    <div className="recipe-meta">
                                        <span className={`difficulty ${cocktail.difficulty}`}>
                                            {cocktail.difficulty}
                                        </span>
                                        <span className="time">⏱️ {cocktail.time}</span>
                                    </div>
                                </div>
                                <div className="ingredients">
                                    <h4>재료</h4>
                                    <ul>
                                        {cocktail.ingredients.map((ingredient) => (
                                            <li key={`${cocktail.id}-${ingredient.id}`}>
                                                {ingredient.name}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                <section className="safety-section">
                    <div className="safety-card">
                        <h2>⚠️ 음주 안전 수칙</h2>
                        <ul>
                            <li>적당한 음주를 권장합니다</li>
                            <li>음주 후 운전은 절대 금지입니다</li>
                            <li>임산부나 미성년자는 음주를 금합니다</li>
                            <li>약물 복용 시 음주를 피해주세요</li>
                        </ul>
                    </div>
                </section>
            </div>
        </div>
    )
}

export default CocktailGuide
