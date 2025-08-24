# 🍸 칵테일 주류 정보 API

환영합니다! **칵테일 주류 정보 API**는 칵테일 제조 전문가와 애호가들을 위해
다양한 주류의 상세 정보를 효율적으로 관리하고 검색할 수 있도록 설계된
RESTful API 서비스입니다.

## ✨ 주요 기능

### 🍾 통합 재료 관리
칵테일을 구성하는 세 가지 핵심 요소를 체계적으로 관리합니다:
- **주류(Spirits)**: 위스키, 진, 럼, 보드카 등 기본 스피릿
- **리큐르(Liqueurs)**: 코인트로, 카라시 등 향료 첨가 주류  
- **기타 재료(Ingredients)**: 시럽, 주스, 비터스 등 보조 재료

### 🔍 고급 검색 기능
다양한 조건으로 재료를 검색할 수 있습니다:
- **맛 프로파일**: 단맛, 쓴맛, 드라이 등 맛 특성별 검색
- **향(Aroma)**: 꽃향, 과일향, 스파이시 등 향 특성별 검색
- **여운(Finish)**: 깔끔한, 긴, 따뜻한 등 뒷맛 특성별 검색
- **알코올 도수**: 최소/최대 도수 범위로 검색
- **원산지**: 국가 및 지역별 검색
- **페이지네이션**: 효율적인 대용량 데이터 탐색

### 📷 이미지 지원
각 재료의 시각적 정보를 제공합니다:
- **대표 이미지**: 제품의 메인 이미지
- **보조 이미지**: 최대 4개의 추가 이미지 (주류만)
- **이미지 검증**: 지원 형식 및 크기 자동 검증

### 🔐 안전한 인증 시스템
- **JWT 기반 인증**: 상태 비저장 토큰 기반 보안
- **역할 기반 접근 제어**: 관리자/사용자 권한 분리
- **토큰 갱신**: 자동 액세스 토큰 갱신 시스템
- **쿠키 기반 세션**: HttpOnly 쿠키로 XSS 방지

### ⚙️ 메타데이터 관리
검색 및 분류를 위한 구조화된 메타데이터:
- **맛(Taste)**: sweet, dry, bitter, fruity 등
- **향(Aroma)**: floral, citrus, spicy, woody 등  
- **여운(Finish)**: clean, long, warm, smooth 등
- **종류(Kind)**: 재료별 카테고리 분류

## 🚀 빠른 시작

### API 기본 정보
- **Base URL**: `http://localhost:8000/api/v1`
- **Content-Type**: `application/json` (대부분의 엔드포인트)
- **인증**: JWT 토큰 (쿠키 기반)

### 인증하기
```bash
# 회원가입
curl -X POST "http://localhost:8000/api/v1/signup" \
  -H "Content-Type: application/json" \
  -d '{"userId": "your_id", "password": "your_password"}'

# 로그인
curl -X POST "http://localhost:8000/api/v1/signin" \
  -H "Content-Type: application/json" \
  -d '{"userId": "your_id", "password": "your_password"}'
```

### 주류 검색해보기
```bash
# 모든 주류 검색 (페이지네이션)
curl "http://localhost:8000/api/v1/spirits?page_number=1&page_size=10"

# 진(Gin) 종류 검색
curl "http://localhost:8000/api/v1/spirits?kind=Gin"

# 드라이한 맛의 주류 검색
curl "http://localhost:8000/api/v1/spirits?taste=dry"
```

## 📚 문서 구조

- **[사용자 가이드](user-guide.md)**: API 사용법 및 예제
- **[API 레퍼런스](api-reference.md)**: 모든 엔드포인트 상세 문서
- **[기술 스택](about.md)**: 프로젝트 아키텍처 및 기술 정보

## 🔗 관련 링크

- **API 문서**: `/api/docs` (Swagger UI)
- **ReDoc**: `/api/redoc` (대안 문서 뷰어)
- **Health Check**: `/api/v1/health`

이 API를 통해 여러분만의 칵테일 레시피를 더욱 풍부하게 만들고,
새로운 주류 조합을 탐색해보세요!
