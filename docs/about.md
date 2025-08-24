# 💡 서비스 소개 및 기술 스택

## 🎯 프로젝트 목표

**칵테일 주류 정보 API**는 칵테일 제조 프로세스를 더욱 효율적이고 창의적으로 만들고자 하는 열정에서 시작되었습니다. **주류(Spirits), 리큐르(Liqueurs), 그리고 다양한 보조 재료(Ingredients)**의 복잡한 특성들을 한눈에 파악하고, 필요할 때 즉시 검색하여 칵테일 제조에 활용할 수 있는 견고하고 유연한 RESTful API 서비스를 제공하는 것이 이 프로젝트의 목표입니다.

이는 단순히 데이터를 저장하는 것을 넘어, 각 재료별 고유의 **향(Aroma), 맛(Taste), 여운(Finish)**과 같은 감각적인 정보까지 체계적으로 관리하여, 사용자가 최적의 재료를 선택하고 새로운 칵테일 조합을 탐색하는 데 도움을 줍니다.

## 🛠️ 기술 스택 (Technical Stack)

이 서비스는 현대적인 웹 기술과 효율적인 데이터 관리를 위해 다음과 같은 기술 스택을 활용하여 구축되었습니다.

### 백엔드 (Backend)
- **주요 언어 및 프레임워크**: **Python 3.13** & **FastAPI**
  - 높은 성능과 빠른 개발 속도를 자랑하는 FastAPI를 기반으로 RESTful API를 구현합니다
  - uvloop 이벤트 루프 정책으로 비동기 처리 성능을 최적화합니다
  - ORJSON을 사용한 고성능 JSON 직렬화
  - Pydantic을 통한 타입 안전 데이터 검증
  
- **종속성 관리**: **UV**
  - Rust 기반의 고성능 Python 패키지 관리자
  - 기존 pip/poetry 대비 10-100배 빠른 설치 속도

### 데이터베이스 (Database)
- **MongoDB**: 주류의 복잡하고 유동적인 특성(향, 맛, 여운 등)과 이미지 메타데이터를 저장하기 위해 유연한 NoSQL 데이터베이스를 사용합니다
- **SQLite**: 맛, 향, 원산지 등 정형화된 메타데이터 관리를 위해 경량 관계형 데이터베이스를 활용합니다

### 인증 및 보안 (Authentication & Security)
- **SuperTokens**: 사용자 인증 및 세션 관리를 위한 오픈소스 솔루션
  - 이메일/패스워드 기반 인증
  - 세션 관리 및 토큰 갱신
- **JWT (JSON Web Token)**: 역할 기반 접근 제어 (RBAC)
- **보안 미들웨어**: 
  - CORS 설정
  - 압축 미들웨어 (Brotli/Gzip)
  - TrustedHost 미들웨어

### 프론트엔드 (Frontend)
- **React 19**: 최신 React 버전으로 모던 UI 구현
- **TypeScript**: 타입 안전성을 위한 정적 타입 검사
- **Vite**: 고성능 빌드 도구 및 개발 서버
- **TailwindCSS v4**: 유틸리티 우선 CSS 프레임워크
- **PNPM**: 고성능 패키지 매니저

### 코드 품질 (Code Quality)
- **Python 도구**:
  - **Ruff**: 고성능 린터 및 포매터 (Rust 기반)
  - **Pyright**: TypeScript 기반 정적 타입 검사기
  - **pytest**: 테스트 프레임워크
- **JavaScript/TypeScript 도구**:
  - **Biome**: 통합 린터 및 포매터 (Rust 기반)
  - **Vitest**: 테스트 프레임워크

### 문서화 (Documentation)
- **MkDocs**: Material 테마를 사용한 정적 문서 사이트 생성
- **mkdocstrings**: Python 독스트링 자동 파싱 및 API 문서 생성

### 개발 도구 (Development Tools)
- **Docker**: 컨테이너화된 개발 및 배포 환경
- **Pre-commit**: Git 커밋 전 자동 코드 품질 검사
- **Structlog**: 구조화된 로깅
- **Pyinstrument**: 성능 프로파일링

### 성능 최적화 (Performance)
- **uvloop**: 고성능 이벤트 루프
- **ORJSON**: 고성능 JSON 직렬화
- **Compression**: Brotli/Gzip 응답 압축
- **Async/Await**: 비동기 처리로 높은 동시성 지원

## 🤝 기여 및 피드백

이 프로젝트는 지속적으로 발전하고 있습니다. 어떤 형태의 기여나 피드백도 환영합니다. 버그 보고, 기능 제안 또는 코드 기여를 통해 프로젝트 발전에 참여해 주시면 감사하겠습니다.
