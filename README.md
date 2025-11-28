# 칵테일 메이커

FastAPI와 React로 구축된 현대적인 한국어 칵테일 재료 데이터베이스 및 레시피 관리 시스템

## 🚀 개요

이 풀스택 웹 애플리케이션은 칵테일 재료, 레시피, 메타데이터를 관리하기 위한 종합 플랫폼을 제공합니다. 시스템은 주류, 리큐르, 보조 재료를 지원하며 상세한 속성 관리 및 검색 기능을 제공합니다.

### ✨ 기능 요약

- **🍸 핵심 재료 및 레시피 관리**: 주류, 리큐르, 칵테일 레시피의 등록, 조회, 수정, 삭제(CRUD)를 지원합니다.
- **🔍 강력한 검색 엔진**: 이름, 재료, 맛, 향 등 다중 조건을 활용한 고급 검색 및 한국어 초성 검색 기능을 제공합니다.
- **💡 개인화 및 추천**: 보유한 재료를 기반으로 만들 수 있는 칵테일을 추천하고, 나만의 레시피 컬렉션을 관리할 수 있습니다.
- **🔐 안전한 인증 및 권한**: JWT 토큰 기반의 역할별(관리자, 사용자) 접근 제어를 통해 시스템을 안전하게 보호합니다.
- **👥 커뮤니티 및 공유**: 사용자들이 직접 레시피를 공유하고 피드백을 주고받을 수 있는 소통 공간을 제공합니다.

## 🛠️ 기술 스택

### 백엔드

- **[FastAPI](https://fastapi.tiangolo.com/)** - 현대적인 비동기 Python 웹 프레임워크
- **Python 3.13+** - uvloop 이벤트 루프 정책을 사용한 최신 Python
- **[MongoDB](https://www.mongodb.com/)** - Motor(비동기 드라이버)를 통한 주 데이터 저장소
- **[SQLite](https://www.sqlite.org/)** - SQLAlchemy ORM을 사용한 메타데이터 저장소
- **[Pydantic](https://pydantic.dev/)** - 데이터 검증 및 설정 관리
- **JWT** - 역할 기반 접근을 제공하는 커스텀 인증 시스템
- **[Gunicorn](https://gunicorn.org/) + [Uvicorn](https://www.uvicorn.org/)** - 프로덕션 ASGI 서버

### 프론트엔드

- **[React 19](https://react.dev/)** - TypeScript를 사용한 최신 React
- **[Vite](https://vite.dev/)** - Rolldown 번들러를 사용한 빌드 도구
- **[TailwindCSS v4](https://tailwindcss.com/)** - 유틸리티 우선 CSS 프레임워크
- **[React Router v7](https://reactrouter.com/)** - 클라이언트 사이드 라우팅
- **[TypeScript](https://www.typescriptlang.org/)** - 정적 타입 검사

### 개발 도구

- **[UV](https://github.com/astral-sh/uv)** - 빠른 Python 패키지 관리자
- **[PNPM](https://pnpm.io/)** - 효율적인 Node.js 패키지 관리자
- **[Ruff](https://github.com/astral-sh/ruff)** - 빠른 Python 린터 및 포맷터
- **[Pyrefly](https://github.com/mauro-balades/pyrefly)** - Python 정적 타입 검사기 및 LSP
- **[Biome](https://biomejs.dev/)** - 빠른 TypeScript/React 린터 및 포맷터
- **[MkDocs](https://www.mkdocs.org/)** - 문서 생성기

## 🏗️ 아키텍처

### 애플리케이션 구조

```
cocktail-maker/
├── app/                    # FastAPI 백엔드
│   ├── auth/               # 인증 (JWT, 역할, 암호화)
│   ├── database/           # 데이터베이스 연결 (MongoDB, SQLite)
│   ├── model/              # Pydantic 데이터 모델 및 유효성 검사
│   ├── query/              # 데이터베이스 쿼리 로직 (추상화 포함)
│   ├── utils/              # 로깅, 시간 등 공통 유틸리티
│   ├── gunicorn.conf.py    # Gunicorn 서버 설정
│   └── main.py             # FastAPI 애플리케이션 진입점 및 라우팅
├── src/                    # React 프론트엔드
│   ├── assets/             # 정적 에셋 (이미지, SVG)
│   ├── components/         # 재사용 가능한 React 컴포넌트
│   ├── contexts/           # React 컨텍스트 (테마 등)
│   ├── hooks/              # 커스텀 훅 (API 호출, 테마 관리)
│   ├── types/              # TypeScript 타입 정의
│   ├── App.tsx             # 메인 애플리케이션 컴포넌트 및 라우팅
│   └── main.tsx            # React 애플리케이션 진입점
├── tests/                  # Pytest 테스트 스위트
├── docs/                   # MkDocs 문서
├── compose/                # Docker Compose 설정
├── data/                   # 이미지 등 데이터 저장소
├── public/                 # Vite public 에셋
├── .github/workflows/      # GitHub Actions CI/CD 워크플로우
├── pyproject.toml          # Python 프로젝트 및 의존성 설정 (uv)
├── package.json            # Frontend 프로젝트 및 의존성 설정 (pnpm)
└── README.md
```

### 백엔드 (app/)

- **듀얼 데이터베이스 시스템**:
  - **MongoDB**: 주 데이터(주류, 리큐르, 재료, 칵테일) 저장을 위해 `Motor` 비동기 드라이버 사용.
  - **SQLite**: 맛, 향 등 메타데이터를 `SQLAlchemy` ORM을 통해 관계형으로 관리하여 데이터 일관성 보장.
- **비동기 우선 설계**:
  - `FastAPI`와 `uvloop` 이벤트 루프 정책을 채택하여 모든 데이터베이스 작업을 `async/await`으로 처리, 높은 처리량 달성.
- **인증 시스템**:
  - **JWT 토큰**: 액세스(15분) 및 리프레시(7일) 토큰 패턴을 사용한 상태 비저장 인증.
  - **역할 기반 접근 제어(RBAC)**: `Admin`, `User`, `Guest` 역할을 정의하고 `Security` 의존성을 통해 엔드포인트 보호.
  - **보안 쿠키**: `HttpOnly` 및 `Secure` 속성을 적용한 쿠키로 토큰을 전송하여 XSS 공격 방지.
- **추상화된 쿼리 레이어 (`app/query/`)**:
  - `CreateDocument`, `RetrieveDocument`, `SearchDocument` 등 추상 기본 클래스를 정의하여 CRUD 작업 표준화.
  - 각 엔티티(주류, 리큐르 등)에 대한 구체적인 쿼리 클래스를 구현하여 재사용성 및 유지보수성 향상.
- **표준화된 API 응답**:
  - 모든 API는 `{"status", "code", "data", "message"}` 형식의 일관된 JSON 구조로 응답하여 클라이언트 처리 용이성 증대.
- **이미지 처리**:
  - `multipart/form-data`를 통한 파일 업로드 및 `Pillow`를 이용한 이미지 유효성 검사 및 처리.

### 프론트엔드 (src/)

- **React 19 및 TypeScript**: 최신 React 기능과 강력한 타입 시스템을 활용하여 안정적인 UI 개발.
- **Vite 빌드 시스템**: `Rolldown` 번들러 기반의 Vite를 사용하여 빠른 개발 서버와 최적화된 프로덕션 빌드 제공.
- **TailwindCSS v4**: 유틸리티 우선 CSS 프레임워크를 통해 일관되고 반응형 디자인 시스템 구축.
- **클라이언트 사이드 라우팅**: `React Router v7`을 사용하여 모던하고 직관적인 페이지 네비게이션 구현.
- **서버 상태 관리**: `@tanstack/react-query`를 사용하여 API 데이터 캐싱, 동기화, 재요청 등 서버 상태를 효율적으로 관리.
- **커스텀 훅 (`src/hooks/`)**: `useApi`, `useMetadata` 등 API 호출 및 비즈니스 로직을 추상화한 커스텀 훅을 통해 코드 중복 최소화 및 재사용성 극대화.
- **컴포넌트 기반 아키텍처**: 기능별로 분리된 재사용 가능한 컴포넌트(`SpiritsRegister`, `ImageUpload` 등)를 통해 유지보수성 및 확장성 확보.
- **테마 관리**: `ThemeContext`를 사용하여 라이트/다크 모드 등 전역 테마를 손쉽게 관리.
- **API 프록시**: `vite.config.ts`가 `/api` 요청을 FastAPI(`http://127.0.0.1:8000`)로 프록시하여 별도 CORS 설정 없이 개발할 수 있습니다.
- **SuperTokens UI 통합**: `EmailPasswordPreBuiltUI` 라우트를 `getSuperTokensRoutesForReactRouterDom`으로 삽입하고, 보호 라우트는 `SessionAuth`로 감싸 인증된 사용자만 접근하도록 구성.

### 인증 및 세션 흐름
- **SuperTokens** (app/main.py, src/main.tsx): Email+Password + Session 조합으로 JWT 없이 세션을 관리하며, FastAPI 레이어에서는 `verify_session` 의존성으로 보호된 API를 강제합니다.
- **레거시 JWT** (app/auth/jwt.py): SuperTokens 도입 이전 경로가 남아 있으며 `@deprecated` 상태로 유지됩니다.
- **API 키 발급기** (app/auth/public_api.py): PBKDF2HMAC(SHA512, 210k iterations)을 이용한 결정적 키를 생성해 외부 파트너와 통합할 수 있습니다.

### 요청 처리 & 응답 표준화
1. FastAPI 엔드포인트는 `model` 계층의 Pydantic 타입으로 입력을 검증합니다.
2. 메타데이터 필드는 `MetadataValidation`(app/query/metadata.py)이 SQLite 기준값과 비교하여 허용 여부를 판정합니다.
3. MongoDB 작업은 `CreateDocument`/`SearchDocument` 추상 클래스를 상속한 쿼리 레이어를 통해 실행되고, Motor 비동기 클라이언트로 처리량을 확보합니다.
4. 모든 성공/실패 응답은 `return_formatter` 또는 `problem_details_formatter`(RFC 9457)을 통해 일관된 JSON 스펙(`status`, `code`, `data`, `message`)을 유지합니다.

### 이미지 파이프라인
- 업로드된 바이너리는 `app/query/queries.py` → `Images.save_image_files_to_local_dir()` 경로를 통해 `data/images/<collection>/<documentId>/*.png`로 저장됩니다.
- `Images.remove_image_files_in_local_dir()`와 MongoDB 문서 업데이트를 묶어 CRUD 시 이미지 정합성을 보장합니다.

### 관측 및 성능 도구
- **Structlog + orjson** (`app/utils/logger.py`): 모든 서버 로깅을 JSONL(`log/service.jsonl`)로 남겨 분석 파이프라인에 투입하기 쉽습니다.
- **PyInstrument 미들웨어** (`?profile=true`): 어느 엔드포인트에서든 쿼리 파라미터만 추가하면 HTML/텍스트 프로파일을 확인할 수 있습니다.
- **X-Server-Version 헤더**: FastAPI 미들웨어가 배포 버전을 응답 헤더에 삽입해 프론트 혹은 모니터링 툴이 실행 중인 빌드를 추적할 수 있습니다.

### 주요 UI 라우트
| 경로 | 컴포넌트 | 설명 |
| --- | --- | --- |
| `/` | `Home` (`src/App.tsx`) | 랜딩 + 기능 소개, CTA |
| `/guide` | `CocktailGuide` | SuperTokens 세션이 필요한 단계별 가이드 |
| `/dashboard` | `Dashboard` | 사용자별 재료/레시피 현황 위젯 |
| `/register/spirits` | `SpiritsRegister` | 이미지 업로드 + 메타데이터 선택을 포함한 주류 등록 폼 |
| `/register/liqueur` | `LiqueurRegister` | 리큐르 등록 폼 |
| `/register/ingredient` | `IngredientRegister` | 비알코올 재료 등록 폼 |
| `/auth/*` | SuperTokens PreBuilt UI | 이메일/비밀번호 가입·로그인, 비밀번호 찾기 |

## 🚀 빠른 시작

### 사전 요구사항

- **Python 3.13+**
- **Node.js 18+**
- **UV** (Python 패키지 관리자)
- **PNPM** (Node.js 패키지 관리자)

### 설치

```bash
# 저장소 복제
git clone <repository-url>
cd cocktail-maker

# 백엔드 의존성 설치
uv sync

# 프론트엔드 의존성 설치
pnpm install

# 개발 환경 설정
uv run pre-commit install
```

### 개발

```bash
# 백엔드 서버 시작
uv run uvicorn app.main:cocktail_maker --reload --host 127.0.0.1 --port 8000

# 프론트엔드 개발 서버 시작 (새 터미널)
pnpm dev

# 문서 서버 시작 (선택사항)
uv run mkdocs serve
```

### 테스트 & 품질

```bash
# 커버리지 + HTML 리포트를 포함한 Python 테스트
TIMESTAMP=$(date +%Y%m%d-%H%M%S) && uv run pytest -s --cov=app --html=tests/results/test-${TIMESTAMP}.html --self-contained-html

# Python 품질 도구
uvx ruff check --fix app/
uvx pyrefly check app/

# 프론트엔드 정적 분석 & 단위 테스트
pnpm lint
pnpm exec vitest run --coverage
```

### 프로덕션 배포

```bash
# 프론트엔드 빌드
pnpm build

# Docker Compose로 실행
docker compose -f compose/docker-compose-full-example.yaml up
```

## ⚙️ 환경 변수 & 런타임 설정

FastAPI와 SuperTokens는 모두 `.env`(루트 혹은 `app/.env`)에서 아래 키를 참고합니다. 값이 없으면 애플리케이션이 부팅 도중 `KeyError`를 발생시킵니다.

| 이름 | 용도 | 정의 위치 | 예시 |
| --- | --- | --- | --- |
| `MONGODB_URL` | Motor가 연결할 MongoDB URI | `app/database/connector.py` | `mongodb://localhost:27017` |
| `SQLITE_PATH` | 메타데이터 테이블이 위치한 SQLite 파일 경로 | `app/database/connector.py`, `app/database/table.py` | `../db.sqlite3` |
| `SECRET_KEY` | (레거시) JWT 서명 키 | `app/auth/jwt.py` | 64‑byte hex 문자열 |
| `SECRET_ALGORITHM` | JWT 서명 알고리즘 | `app/auth/jwt.py` | `HS256` |
| `PUBLIC_API_MASTER_KEY` | API 키 파생용 마스터 키 | `app/auth/public_api.py` | 64‑byte hex |
| `PUBLIC_API_SALT` | API 키 파생용 고정 솔트 | `app/auth/public_api.py` | 64‑byte hex |
| `SUPERTOKEN_API_KEY` | SuperTokens Core에 전달될 API 키 | `app/main.py` | `dev-secret-key` |

> 위 값은 운영 환경에서 반드시 시크릿 매니저(Vault, SSM 등)나 Docker/Compose 환경 변수로 주입하세요.

```bash
# 예시: app/.env 생성
cat <<'EOF' > app/.env
MONGODB_URL=mongodb://localhost:27017
SQLITE_PATH=../db.sqlite3
SECRET_KEY=change-me
SECRET_ALGORITHM=HS256
PUBLIC_API_MASTER_KEY=hex-string-from-openssl-rand-hex-64
PUBLIC_API_SALT=hex-string-from-openssl-rand-hex-64
SUPERTOKEN_API_KEY=dev-key
EOF
# 필요 시: openssl rand -hex 64
```

### SuperTokens Core
- `app/main.py`와 `src/main.tsx` 모두 `http://localhost:3567`를 기본 Core 도메인으로 가정합니다.
- 로컬 개발 시 아래와 같이 Core를 먼저 띄우세요.

```bash
docker run --rm -p 3567:3567 -e SUPERTOKENS_DEFAULT_API_KEY=dev-key supertokens/supertokens-core:5
```

### 스토리지 & 로그 경로
- 모든 이미지 업로드는 `data/images/<collection>/<document_id>/<image>.png`에 저장되며 `app/query/query_child.py`가 디렉터리를 생성합니다.
- JSONL 기반 애플리케이션 로그는 `log/service.jsonl`에 적재되므로 실행 계정에 쓰기 권한이 필요합니다.

## DB

이 시스템은 데이터의 성격에 따라 두 개의 데이터베이스를 사용하는 듀얼 데이터베이스 아키텍처를 채택했습니다.

### 1. MongoDB (주요 데이터 저장소)

비정형적이고 유연한 구조의 데이터를 저장하기 위해 MongoDB를 사용합니다. 비동기 드라이버 `Motor`를 통해 FastAPI의 비동기 성능을 극대화합니다.

- **저장 데이터**:
  - **주류 (Spirits)**: 이름, 도수, 원산지, 맛, 향 등 복합적인 속성을 가진 주류 정보
  - **리큐르 (Liqueurs)**: 주류와 유사한 속성을 가지며, 브랜드, 주재료 등의 정보를 포함하는 리큐르 정보
  - **보조 재료 (Ingredients)**: 칵테일에 사용되는 비알코올성 재료 정보
  - **칵테일 (Cocktails)**: 여러 재료와 제조 단계를 포함하는 복잡한 구조의 레시피 정보
  - **사용자 (Users)**: 사용자 계정 정보 및 역할(Role)
- **선택 이유**:
  - **유연한 스키마**: 각기 다른 속성을 가진 주류, 리큐르, 재료 데이터를 별도의 스키마 수정 없이 쉽게 저장하고 확장할 수 있습니다.
  - **중첩 구조 지원**: 칵테일 레시피처럼 재료 목록, 제조 단계 등 중첩된 데이터를 직관적으로 모델링하고 저장하기 용이합니다.
  - **성능**: 비동기 드라이버를 지원하여 대량의 읽기/쓰기 작업에서 높은 처리량을 보장합니다.

### 2. SQLite (메타데이터 저장소)

데이터의 일관성과 정합성이 중요한 메타데이터는 관계형 데이터베이스인 SQLite에 저장합니다. `SQLAlchemy` ORM을 통해 관리됩니다.

- **저장 데이터**:
  - **메타데이터 (Metadata)**: 주류 및 리큐르의 '맛(Taste)', '향(Aroma)', '여운(Finish)'을 정의하는 표준 속성 값들. 예를 들어, '과일향', '스파이시', '부드러운 목넘김' 등의 값을 미리 정의해 둡니다.
- **선택 이유**:
  - **데이터 일관성**: 주류나 리큐르 정보를 등록할 때 사용될 수 있는 맛, 향, 여운의 값을 미리 정해진 목록으로 제한하여 데이터의 일관성을 유지합니다.
  - **데이터 무결성**: 관계형 모델을 사용하여 메타데이터 간의 관계를 명확히 하고, 잘못된 값이 입력되는 것을 방지합니다.
  - **검증**: 새로운 재료가 등록될 때 해당 재료의 맛, 향, 여운 속성이 SQLite에 저장된 유효한 값인지 검증하는 용도로 사용됩니다.

## 📦 Docker & Compose 실행 옵션
- **도커 이미지**: 루트 `Dockerfile`은 `uv` 캐시 마운트를 활용해 FastAPI 의존성을 미리 동결하고, `gunicorn main:cocktail_maker`를 기본 엔트리포인트로 설정합니다.
- **베이스 빌드**
  ```bash
  docker build -t cocktail-maker:dev .
  docker run --rm --env-file app/.env -p 8000:8000 cocktail-maker:dev
  ```
- **Compose 템플릿**
  - `compose/docker-compose-full-example.yaml`: Compose 기능을 총망라한 학습용 "kitchen-sink" 예시로, 실제 배포 전 필요한 설정을 골라서 사용할 수 있습니다.
  - `compose/cocktail-maker/docker-compose.yaml`: Swarm 배포용으로 `cocktail-maker` 서비스 3개와 HTTPS 종단(Nginx)을 구성하며, `/api/v1/health` 헬스체크를 통해 롤링 업데이트를 보조합니다.
  - `compose/cocktail-maker-background/docker-compose.yaml`: 개발용 인프라(로컬 MongoDB, SuperTokens Core, Postgres 18)를 한 번에 올리는 도우미 파일입니다.
- **환경 변수 전달**: Compose 파일에 `env_file: app/.env`를 추가하거나 `docker compose --env-file` 옵션을 사용해 앞서 정의한 시크릿을 주입하세요.

## 📚 문서화 (MkDocs)
- `mkdocs.yml`은 Material 테마 + `mkdocstrings`를 활성화하고 있어 Python docstring을 그대로 API 문서로 노출할 수 있습니다.
- `docs/` 디렉터리에서 콘텐츠를 수정하면 `site/`에 정적 사이트가 생성됩니다.

```bash
uv run mkdocs serve -a 127.0.0.1:9000  # FastAPI(8000)와 포트 충돌을 피하면서 프리뷰
uv run mkdocs build                    # site/ 에 정적 파일 생성
uv run mkdocs gh-deploy                # GitHub Pages에 배포 (필요 시)
```

## 📋 상세 기능

- **재료 관리 (Ingredient Management):** 주류, 리큐르, 기타 재료에 대한 완전한 CRUD 및 이미지 업로드 기능.
- **칵테일 레시피 관리 (Cocktail Recipe Management):** 칵테일 레시피 등록, 조회, 검색, 수정, 삭제 기능.
- **고급 검색 및 필터링 (Advanced Search & Filtering):** 재료 및 칵테일에 대한 다중 조건(이름, 도수, 원산지, 맛, 향 등) 검색, 페이지네이션, 정렬 기능.
- **한국어 초성 검색 (Korean Consonant Search):** 자음을 이용한 빠른 재료 검색.
- **메타데이터 시스템 (Metadata System):** 맛, 향, 여운 등 프로파일링을 위한 동적 속성 관리.
- **추천 시스템 (Recommendation System):** 보유한 재료를 기반으로 제조 가능한 칵테일 추천.
- **인증 및 권한 관리 (Authentication & Authorization):** JWT 토큰 기반 로그인, 역할(관리자, 사용자)에 따른 API 접근 제어, API 키 발급.
- **사용자 맞춤 기능 (User Personalization):** 즐겨찾기, 평점 및 리뷰, 나만의 레시피 컬렉션 관리.
- **커뮤니티 (Community):** 사용자들이 소통할 수 있는 게시판, 댓글, 좋아요 기능.
- **관리자 대시보드 (Admin Dashboard):** 사용자 및 시스템 통계, 콘텐츠 관리 기능.
- **성능 및 안정성 (Performance & Stability):** 비동기 처리, 결과 캐싱, API 요청 제한(Rate Limiting), 구조화된 로깅을 통한 고성능 및 안정적인 서비스 제공.

## 📝 백엔드 개발 로드맵

### 🚀 우선순위 높음 (핵심 기능)

#### 1. 칵테일 레시피 CRUD 완성

- [ ] **칵테일 레시피 상세 조회 API** (`GET /api/v1/cocktail/{name}`)
  - 칵테일 이름으로 단일 레시피 조회
  - 사용된 재료 정보와 연결하여 반환
  - 메타데이터(맛, 향, 여운) 정보 포함
- [ ] **칵테일 레시피 검색 API** (`GET /api/v1/cocktail/search`)
  - 칵테일명, 재료, 글래스 타입, 원산지별 검색
  - 페이지네이션 지원
  - 검색 결과 정렬 (관련성, 이름순)
- [ ] **칵테일 레시피 수정 API** (`PUT /api/v1/cocktail/{id}`)
  - 기존 레시피 정보 업데이트
  - 재료 목록 및 제조 단계 수정
  - 이미지 업로드 및 교체
- [ ] **칵테일 레시피 삭제 API** (`DELETE /api/v1/cocktail/{id}`)
  - 레시피 소프트 삭제 또는 하드 삭제 구현
  - 관련 이미지 파일 정리

#### 2. 한국어 자음 검색 기능

- [ ] **한국어 초성 검색 라이브러리 통합**
  - 주류/리큐르/재료명에 대한 초성 검색 지원
  - 예: "ㅂㅅㅋ" 입력 시 "보스턴 칵테일" 검색
- [ ] **자음 검색 API 엔드포인트 추가**
  - `/api/v1/spirits/search/consonant`
  - `/api/v1/liqueur/search/consonant`
  - `/api/v1/ingredient/search/consonant`
- [ ] **검색 성능 최적화**
  - MongoDB 인덱스 설정 (한글명 필드)
  - 자음 매핑 테이블 구축

#### 3. 재료-칵테일 관계 시스템

- [ ] **재료별 칵테일 목록 API** (`GET /api/v1/spirits/{id}/cocktails`)
  - 특정 주류/리큐르를 사용하는 칵테일 목록 반환
  - 주재료/부재료 구분 표시
- [ ] **칵테일별 재료 정보 확장**
  - 필수/선택 재료 구분
  - 대체 가능 재료 제안
  - 재료별 중요도/비율 정보
- [ ] **제조 가능한 칵테일 추천 API** (`POST /api/v1/cocktail/recommend`)
  - 보유 재료 목록을 전송하면 제조 가능한 칵테일 반환
  - 부족한 재료 개수별로 정렬
  - 대체 재료 제안 포함

### 📱 중간 우선순위 (사용자 경험)

#### 4. 이메일 인증 시스템

- [ ] **회원가입 시 이메일 중복 확인** (`POST /api/v1/auth/check-email`)
  - 실시간 이메일 중복 검사
  - 도메인 유효성 검증
- [ ] **이메일 인증 토큰 발송**
  - SMTP 서버 설정 (Gmail/SendGrid/AWS SES)
  - 인증 토큰 생성 및 만료 처리
  - 인증 이메일 템플릿 작성
- [ ] **이메일 인증 확인 API** (`POST /api/v1/auth/verify-email`)
  - 토큰 검증 후 계정 활성화
  - 인증 실패 시 재발송 기능

#### 5. 고급 검색 및 필터링

- [ ] **복합 검색 조건 지원**
  - 도수 범위 필터 (예: 20-40도)
  - 다중 카테고리 선택
  - 가격대별 필터링 (추가 필드 필요)
- [ ] **검색 결과 정렬 옵션**
  - 관련성, 이름순, 도수순, 평점순 정렬
  - 오름차순/내림차순 선택
- [ ] **검색 기록 및 인기 검색어**
  - 사용자별 최근 검색 기록 저장
  - 실시간 인기 검색어 집계

#### 6. 파일 업로드 시스템 개선

- [ ] **이미지 최적화 파이프라인**
  - 자동 리사이징 (썸네일, 중간, 원본)
  - WebP 형식 변환 지원
  - 이미지 메타데이터 추출
- [ ] **클라우드 스토리지 연동**
  - AWS S3/Google Cloud Storage 연동
  - CDN을 통한 이미지 서빙
  - 이미지 URL 관리

### 🌟 낮은 우선순위 (확장 기능)

#### 7. 커뮤니티 게시판 시스템

- [ ] **게시판 데이터 모델 설계**
  - 게시글, 댓글, 대댓글 스키마
  - 카테고리, 태그 시스템
  - 첨부파일 지원
- [ ] **게시글 CRUD API**
  - `/api/v1/board/posts` - 게시글 목록/작성
  - `/api/v1/board/posts/{id}` - 게시글 상세/수정/삭제
  - 마크다운 에디터 지원
- [ ] **댓글 시스템 API**
  - `/api/v1/board/posts/{id}/comments` - 댓글 CRUD
  - 대댓글(nested comments) 지원
  - 댓글 정렬 옵션 (최신순, 추천순)
- [ ] **좋아요/싫어요 시스템**
  - 게시글/댓글별 평가 기능
  - 중복 평가 방지 로직
  - 실시간 평가 수 집계
- [ ] **실시간 알림 시스템**
  - 댓글 작성 시 원글 작성자 알림
  - WebSocket 또는 Server-Sent Events 구현
  - 알림 설정 관리 API

#### 8. 사용자 개인화 기능

- [ ] **즐겨찾기 시스템**
  - 주류/칵테일 즐겨찾기 추가/제거
  - 개인 즐겨찾기 목록 조회
- [ ] **평점 및 리뷰 시스템**
  - 주류/칵테일별 평점 (1-5점)
  - 리뷰 작성 및 관리
  - 평점 기반 추천 알고리즘
- [ ] **개인 칵테일 레시피 컬렉션**
  - 사용자가 직접 작성한 레시피 관리
  - 공개/비공개 설정
  - 다른 사용자와 레시피 공유

#### 9. 관리자 기능 강화

- [ ] **관리자 대시보드 API**
  - 사용자 통계, 인기 검색어
  - 시스템 사용량 모니터링
- [ ] **컨텐츠 관리 기능**
  - 부적절한 게시글/댓글 신고 처리
  - 일괄 데이터 등록/수정 도구
  - 이미지 일괄 처리

#### 10. API 성능 및 안정성

- [ ] **캐싱 시스템 도입**
  - Redis를 이용한 검색 결과 캐싱
  - 메타데이터 캐싱으로 응답 속도 향상
- [ ] **API 속도 제한 (Rate Limiting)**
  - 사용자별/IP별 요청 제한
  - API 키별 차등 제한
- [ ] **로깅 및 모니터링 강화**
  - 구조화된 로그 형식 정립
  - 성능 메트릭 수집
  - 에러 추적 시스템

### 📋 개발 진행 가이드

#### 단계별 구현 순서

1. **1단계**: 칵테일 CRUD 완성 → 자음 검색 → 재료-칵테일 관계
2. **2단계**: 이메일 인증 → 고급 검색 → 파일 업로드 개선
3. **3단계**: 커뮤니티 기능 → 개인화 → 관리자 기능 → 성능 최적화

#### 각 기능 구현 시 체크리스트

- [ ] Pydantic 모델 정의 (`app/model/`)
- [ ] MongoDB 컬렉션 스키마 설계
- [ ] 쿼리 클래스 구현 (`app/query/`)
- [ ] API 엔드포인트 구현 (`app/main.py`)
- [ ] 에러 핸들링 및 로깅
- [ ] 단위 테스트 작성 (`tests/`)
- [ ] API 문서화 (FastAPI 자동 생성)
- [ ] 성능 테스트 (필요시)

## 🧪 테스트 커버리지

| 파일 | 목적 |
| --- | --- |
| `tests/test_health_check.py` | `/api/v1/health` 엔드포인트를 동기/비동기 TaskGroup으로 반복 호출하며 안정성을 검증 |
| `tests/test_error_response.py` | `problem_details_formatter`가 RFC 9457 스펙에 맞는 응답을 반환하는지 확인 |
| `tests/test_encryption.py` | `auth.encryption` 유틸이 동일 입력에 대해 동일 솔트를 재사용하고 예외를 던지는지 검사 |
| `tests/test_liqueur_delete.py` | `/api/v1/liqueur/{id}` 삭제 엔드포인트의 상태 코드, 유효성, TaskGroup 병렬 처리, `DeleteLiqueur` 호출 여부를 검증 |

```bash
# 백엔드 테스트 + HTML 리포트
TIMESTAMP=$(date +%Y%m%d-%H%M%S) && uv run pytest -s --cov=app --html=tests/results/test-${TIMESTAMP}.html --self-contained-html

# 프론트엔드 단위 테스트 / JSDOM 환경
pnpm exec vitest run --coverage
```

## 🤝 기여하기

1. **코드 품질**: 모든 코드는 린팅, 타입 검사, 테스트를 통과해야 합니다
2. **Pre-commit 훅**: `uv run pre-commit install`로 설치
3. **테스트**: 새로운 기능과 버그 수정에 대한 테스트 작성
4. **문서**: API 변경사항에 대한 문서 업데이트

### 개발 워크플로우

```bash
# 커밋하기 전에
uvx ruff check --fix app/
uvx ruff format app/
uvx pyrefly check app/
pnpm lint
pnpm format
uv run pytest tests/ --cov=app
```

## 📄 라이선스

이 프로젝트는 여러 오픈소스 의존성을 포함합니다. 자세한 정보는 아래 라이선스 표를 참조하세요.

## Licenses

| Name                       | Version     | License                                             |
| -------------------------- | ----------- | --------------------------------------------------- |
| Brotli                     | 1.1.0       | MIT License                                         |
| Deprecated                 | 1.2.18      | MIT License                                         |
| Jinja2                     | 3.1.6       | BSD License                                         |
| Markdown                   | 3.9         | UNKNOWN                                             |
| MarkupSafe                 | 3.0.2       | BSD License                                         |
| PyJWT                      | 2.10.1      | MIT License                                         |
| PyYAML                     | 6.0.2       | MIT License                                         |
| Pygments                   | 2.19.2      | BSD License                                         |
| SQLAlchemy                 | 2.0.43      | MIT                                                 |
| Secweb                     | 1.25.2      | UNKNOWN                                             |
| aiofiles                   | 24.1.0      | Apache Software License                             |
| aiohappyeyeballs           | 2.6.1       | Python Software Foundation License                  |
| aiohttp                    | 3.12.15     | Apache-2.0 AND MIT                                  |
| aiohttp-retry              | 2.9.1       | MIT License                                         |
| aiosignal                  | 1.4.0       | Apache Software License                             |
| aiosmtplib                 | 3.0.2       | MIT                                                 |
| annotated-types            | 0.7.0       | MIT License                                         |
| anyio                      | 4.10.0      | UNKNOWN                                             |
| asgiref                    | 3.9.1       | BSD License                                         |
| attrs                      | 25.3.0      | UNKNOWN                                             |
| babel                      | 2.17.0      | BSD License                                         |
| backrefs                   | 5.9         | MIT License                                         |
| certifi                    | 2025.8.3    | Mozilla Public License 2.0 (MPL 2.0)                |
| cffi                       | 2.0.0       | UNKNOWN                                             |
| cfgv                       | 3.4.0       | MIT License                                         |
| charset-normalizer         | 3.4.3       | MIT                                                 |
| click                      | 8.2.1       | UNKNOWN                                             |
| colorama                   | 0.4.6       | BSD License                                         |
| coverage                   | 7.10.6      | Apache-2.0                                          |
| cryptography               | 45.0.7      | Apache-2.0 OR BSD-3-Clause                          |
| distlib                    | 0.4.0       | Python Software Foundation License                  |
| dnspython                  | 2.8.0       | ISC License (ISCL)                                  |
| email-validator            | 2.3.0       | The Unlicense (Unlicense)                           |
| fastapi                    | 0.116.1     | MIT License                                         |
| fastapi-cli                | 0.0.11      | MIT License                                         |
| fastapi-cloud-cli          | 0.1.5       | MIT License                                         |
| filelock                   | 3.19.1      | The Unlicense (Unlicense)                           |
| frozenlist                 | 1.7.0       | Apache-2.0                                          |
| ghp-import                 | 2.1.0       | Apache Software License                             |
| griffe                     | 1.14.0      | UNKNOWN                                             |
| gunicorn                   | 23.0.0      | MIT License                                         |
| h11                        | 0.16.0      | MIT License                                         |
| httpcore                   | 1.0.9       | BSD License                                         |
| httptools                  | 0.6.4       | MIT License                                         |
| httpx                      | 0.28.1      | BSD License                                         |
| identify                   | 2.6.14      | MIT                                                 |
| idna                       | 3.10        | BSD License                                         |
| iniconfig                  | 2.1.0       | MIT License                                         |
| markdown-it-py             | 4.0.0       | MIT License                                         |
| mdurl                      | 0.1.2       | MIT License                                         |
| mergedeep                  | 1.3.4       | MIT License                                         |
| mkdocs                     | 1.6.1       | BSD License                                         |
| mkdocs-autorefs            | 1.4.3       | UNKNOWN                                             |
| mkdocs-get-deps            | 0.2.0       | MIT License                                         |
| mkdocs-material            | 9.6.19      | MIT License                                         |
| mkdocs-material-extensions | 1.3.1       | MIT License                                         |
| mkdocstrings               | 0.30.0      | UNKNOWN                                             |
| mkdocstrings-python        | 1.18.2      | UNKNOWN                                             |
| multidict                  | 6.6.4       | Apache License 2.0                                  |
| nodeenv                    | 1.9.1       | BSD License                                         |
| orjson                     | 3.11.3      | Apache Software License; MIT License                |
| packaging                  | 25.0        | Apache Software License; BSD License                |
| paginate                   | 0.5.7       | MIT License                                         |
| pathspec                   | 0.12.1      | Mozilla Public License 2.0 (MPL 2.0)                |
| phonenumbers               | 8.13.55     | Apache Software License                             |
| pillow                     | 11.3.0      | UNKNOWN                                             |
| pkce                       | 1.0.3       | MIT License                                         |
| platformdirs               | 4.4.0       | MIT License                                         |
| pluggy                     | 1.6.0       | MIT License                                         |
| pre_commit                 | 4.3.0       | MIT                                                 |
| propcache                  | 0.3.2       | Apache Software License                             |
| pycparser                  | 2.23        | BSD License                                         |
| pycryptodome               | 3.20.0      | Apache Software License; BSD License; Public Domain |
| pydantic                   | 2.11.7      | MIT License                                         |
| pydantic_core              | 2.33.2      | MIT License                                         |
| pyinstrument               | 5.1.1       | BSD License                                         |
| pymdown-extensions         | 10.16.1     | MIT License                                         |
| pymongo                    | 4.15.0      | Apache Software License                             |
| pyotp                      | 2.9.0       | MIT License                                         |
| pytest                     | 8.4.2       | MIT License                                         |
| pytest-asyncio             | 1.1.0       | UNKNOWN                                             |
| pytest-cov                 | 7.0.0       | MIT License                                         |
| pytest-dotenv              | 0.5.2       | MIT License                                         |
| pytest-html                | 4.1.1       | MIT License                                         |
| pytest-metadata            | 3.1.1       | Mozilla Public License 2.0 (MPL 2.0)                |
| python-dateutil            | 2.9.0.post0 | Apache Software License; BSD License                |
| python-dotenv              | 1.1.1       | BSD License                                         |
| python-multipart           | 0.0.20      | Apache Software License                             |
| pyyaml_env_tag             | 1.1         | UNKNOWN                                             |
| requests                   | 2.32.5      | Apache Software License                             |
| requests-file              | 2.1.0       | Apache Software License                             |
| rich                       | 14.1.0      | MIT License                                         |
| rich-toolkit               | 0.15.1      | MIT License                                         |
| rignore                    | 0.6.4       | MIT                                                 |
| sentry-sdk                 | 2.37.1      | BSD License                                         |
| setproctitle               | 1.3.7       | BSD License                                         |
| shellingham                | 1.5.4       | ISC License (ISCL)                                  |
| six                        | 1.17.0      | MIT License                                         |
| sniffio                    | 1.3.1       | Apache Software License; MIT License                |
| sqlmodel                   | 0.0.24      | MIT License                                         |
| starlette                  | 0.47.3      | BSD License                                         |
| starlette-compress         | 1.6.1       | Zero-Clause BSD (0BSD)                              |
| structlog                  | 25.4.0      | Apache Software License; MIT License                |
| supertokens_python         | 0.30.2      | Apache Software License                             |
| tldextract                 | 5.3.0       | BSD License                                         |
| twilio                     | 9.8.0       | MIT License                                         |
| typer                      | 0.17.4      | MIT License                                         |
| typing-inspection          | 0.4.1       | UNKNOWN                                             |
| typing_extensions          | 4.15.0      | UNKNOWN                                             |
| urllib3                    | 2.5.0       | UNKNOWN                                             |
| uvicorn                    | 0.35.0      | BSD License                                         |
| uvicorn-worker             | 0.3.0       | MIT License                                         |
| uvloop                     | 0.21.0      | Apache Software License; MIT License                |
| virtualenv                 | 20.34.0     | MIT License                                         |
| watchdog                   | 6.0.0       | Apache Software License                             |
| watchfiles                 | 1.1.0       | MIT License                                         |
| websockets                 | 15.0.1      | BSD License                                         |
| wrapt                      | 1.17.3      | BSD License                                         |
| yarl                       | 1.20.1      | Apache Software License                             |
| zstandard                  | 0.24.0      | BSD License                                         |
