# 칵테일 메이커

FastAPI와 React로 구축된 현대적인 한국어 칵테일 재료 데이터베이스 및 레시피 관리 시스템

## 🚀 개요

이 풀스택 웹 애플리케이션은 칵테일 재료, 레시피, 메타데이터를 관리하기 위한 종합 플랫폼을 제공합니다. 시스템은 주류, 리큐르, 보조 재료를 지원하며 상세한 속성 관리 및 검색 기능을 제공합니다.

### ✨ 주요 기능

- **🍸 재료 관리**: 주류, 리큐르, 재료에 대한 완전한 CRUD 작업
- **🔍 고급 검색**: 모든 속성에 대한 전체 텍스트 검색 및 페이지네이션
- **🏷️ 메타데이터 시스템**: 맛 프로필을 위한 카테고리별 설명 속성
- **📸 이미지 지원**: 제품 이미지를 위한 파일 업로드 검증 및 저장
- **🔐 인증**: JWT 기반 역할별 접근 제어
- **📱 반응형 디자인**: TailwindCSS를 사용한 현대적인 React 프론트엔드
- **⚡ 성능**: MongoDB와 SQLite를 사용한 비동기 우선 Python 백엔드

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
- **[Pyright](https://github.com/microsoft/pyright)** - Python 정적 타입 검사기
- **[Biome](https://biomejs.dev/)** - 빠른 TypeScript/React 린터 및 포맷터
- **[MkDocs](https://www.mkdocs.org/)** - 문서 생성기

## 🏗️ 아키텍처

### 애플리케이션 구조

```
cocktail-maker/
├── app/                    # FastAPI 백엔드
│   ├── auth/              # JWT 인증 및 권한 부여
│   ├── database/          # MongoDB 및 SQLite 연결
│   ├── model/             # Pydantic 데이터 모델
│   ├── query/             # 데이터베이스 쿼리 레이어
│   ├── utils/             # 유틸리티 (로깅, 포맷팅)
│   └── main.py            # FastAPI 애플리케이션 진입점
├── src/                   # React 프론트엔드
├── tests/                 # 테스트 스위트
├── docs/                  # MkDocs 문서
└── compose/               # Docker 구성
```

### 주요 구성 요소

#### 인증 레이어 (`app/auth/`)

- 액세스/리프레시 패턴을 사용한 JWT 토큰 관리
- 역할 기반 권한 부여 미들웨어
- 프로덕션 API 키 생성
- 데이터 암호화 유틸리티

#### 데이터베이스 레이어 (`app/database/`)

- **MongoDB**: 주 데이터를 위한 Motor를 통한 비동기 작업
- **SQLite**: ORM 기반 메타데이터 저장
- 연결 풀링 및 트랜잭션 관리

#### API 레이어 (`app/model/` & `app/query/`)

- **Pydantic 모델**: 요청/응답 검증
- **쿼리 추상화**: 검색을 포함한 CRUD 작업
- **표준화된 응답**: 일관된 JSON API 형식

### 응답 형식

모든 API 엔드포인트는 표준화된 JSON 응답을 반환합니다:

```json
{
  "status": "success|error",
  "code": 200,
  "data": {
    /* response payload */
  },
  "message": "Operation description"
}
```

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

### 테스트

```bash
# 커버리지를 포함한 Python 테스트 실행
TIMESTAMP=$(date +%Y%m%d-%H%M%S) && uv run pytest -s --cov=app --html=../tests/results/test-${TIMESTAMP}.html --self-contained-html

# 코드 품질 검사 실행
uvx ruff check --fix app/
uvx pyright app/
pnpm lint
```

### 프로덕션 배포

```bash
# 프론트엔드 빌드
pnpm build

# Docker Compose로 실행
docker compose -f compose/docker-compose-full-example.yaml up
```

## DB

### 주류 및 리큐르

속성

- 주류별 ID, 명칭, 향, 맛, 여운, 종류, 용량, 도수, 국가, 지역, 설명, 사진

### 보조 재료

속성

- 보조별 ID, 명칭, 종류, 설명, 사진

### 메타데이터

속성

- 메타 ID, 명칭, 설명, 사진

## 기능

1. 주류, 리큐르, 보조 재료 검색

- 선택한 속성에 대한 Full Text 검색
- 결과와 가장 일치하는 항목을 검색 결과 상위에 노출
- 결과 Pagination
- 결과 클릭 시 상세 페이지로 이동

2. 주류, 리큐르, 보조 재료 상세 페이지

- 설명에 기재된 내용 중 메타데이터에 존재하는 단어 오른쪽 상단에 작은 기호 아이콘 표기
- 해당하는 단어 클릭 시 메타데이터 정보 팝오버

3. 메타데이터 메뉴

- 명칭 기준 가나다 나열
- 클릭 시 상세 페이지로 이동

## 추가 예정

- 칵테일 레시피 DB
- 재료와 칵테일 레시피간 관계 구축
- 칵테일 레시피 혹은 재료별 상세 페이지에 해당하는 레시피 혹은 재료 링크
- 재료 검색 시 제조 가능한 칵테일 레시피 표기
- 칵테일 레시피에 권장 재료 및 대체 가능 재료 표기

### (new) 커뮤니티 게시판

- 게시글, 댓글 CRUD
- 댓글 알림
- 좋아요, 싫어요

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

## Dev

### Features tracking

#### Auth

- [x] 회원가입 (ID, Password, Role, ETC) -> Replace supertokens
- [ ] 회원가입 시 ID, Email 중복확인 -> Replace supertokens
- [ ] 회원가입 시 Email 인증 후 가입 승인 -> Replace supertokens
- [x] 로그인 시 Access JWT 발급 -> Replace supertokens
- [x] Refresh Token 으로 JWT 재발급 -> Replace supertokens
- [x] API 엔드포인트별 사용자 Role 검증 -> Replace supertokens

#### Key

- [x] 메타데이터 다수 등록
- [x] 메타데이터 전체 조회 - Category
- [x] 메타데이터 삭제 - ID
- [x] 주류 정보 단일 등록
- [x] 주류 정보 단일 조회 - Name
- [x] 주류 정보 검색 - All attributes
- [ ] 주류 정보 자음 검색 - Name
- [x] 주류 정보 수정 - ID
- [x] 주류 정보 삭제 - ID
- [x] 리큐르 정보 단일 등록
- [x] 리큐르 정보 단일 조회 - Name
- [x] 리큐르 정보 검색 - All attributes
- [ ] 리큐르 정보 자음 검색 - Name
- [x] 리큐르 정보 수정 - ID
- [x] 리큐르 정보 삭제 - ID
- [x] 기타 재료 정보 단일 등록
- [x] 기타 재료 정보 검색 - All attributes
- [x] 기타 재료 정보 단일 조회 - Name
- [ ] 기타 재료 자음 검색 - Name
- [x] 기타 재료 정보 수정 - ID
- [x] 기타 재료 정보 삭제 - ID
- [ ] 주류, 리큐르(Optional), 기타 재료(Optional)로 칵테일 제조 정보 등록
- [ ] 칵테일 제조 정보 단일 조회 - Name
- [ ] 칵테일 제조 정보 수정 - ID
- [ ] 칵테일 제조 정보 삭제 - ID

#### ETC

- [x] 서비스 버전 정보 조회
- [x] 모든 응답에 규격화된 JSON 적용
- [x] 이벤트 로거
- [x] 상태 체크

## 🧪 테스트

커버리지 리포트와 함께 전체 테스트 스위트를 실행합니다:

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S) && uv run pytest -s --cov=app --html=../tests/results/test-${TIMESTAMP}.html --self-contained-html
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
uvx pyright app/
pnpm lint
pnpm format
uv run pytest tests/ --cov=app
```

## 📄 라이선스

이 프로젝트는 여러 오픈소스 의존성을 포함합니다. 자세한 정보는 아래 라이선스 표를 참조하세요.

## Licenses

| Name                       | Version     | License                                             | Description                                                                                                                                 |
| -------------------------- | ----------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Brotli                     | 1.1.0       | MIT License                                         | A generic-purpose lossless compression algorithm.                                                                                           |
| Deprecated                 | 1.2.18      | MIT License                                         | A library for marking functions and classes as deprecated.                                                                                  |
| Jinja2                     | 3.1.6       | BSD License                                         | A modern and designer-friendly templating engine for Python.                                                                                |
| Markdown                   | 3.8.2       | UNKNOWN                                             | A Python implementation of John Gruber's Markdown.                                                                                          |
| MarkupSafe                 | 3.0.2       | BSD License                                         | A library for handling HTML and XML strings in a safe way.                                                                                  |
| PyJWT                      | 2.10.1      | MIT License                                         | A Python implementation of JSON Web Tokens.                                                                                                 |
| PyYAML                     | 6.0.2       | MIT License                                         | A YAML parser and emitter for Python.                                                                                                       |
| Pygments                   | 2.19.2      | BSD License                                         | A generic syntax highlighter suitable for use in code hosting, forums, wikis or other applications that need to prettify source code.       |
| SQLAlchemy                 | 2.0.41      | MIT                                                 | The Python SQL Toolkit and Object Relational Mapper.                                                                                        |
| Secweb                     | 1.18.1      | Mozilla Public License 2.0 (MPL 2.0)                | A library for security scanning of web applications.                                                                                        |
| aiohappyeyeballs           | 2.6.1       | Python Software Foundation License                  | An implementation of the Happy Eyeballs algorithm for asynchronous applications.                                                            |
| aiohttp                    | 3.12.13     | Apache-2.0                                          | An asynchronous HTTP client/server framework for asyncio and Python.                                                                        |
| aiohttp-retry              | 2.9.1       | MIT License                                         | An asyncio http client/server framework retry library.                                                                                      |
| aiosignal                  | 1.3.2       | Apache Software License                             | A library for managing signals in asynchronous applications.                                                                                |
| aiosmtplib                 | 3.0.2       | MIT                                                 | An asyncio SMTP client.                                                                                                                     |
| annotated-types            | 0.7.0       | MIT License                                         | A library for adding metadata to types.                                                                                                     |
| anyio                      | 4.9.0       | MIT License                                         | An asynchronous networking and concurrency library that works on top of either asyncio or trio.                                             |
| asgiref                    | 3.8.1       | BSD License                                         | A library that provides ASGI (Asynchronous Server Gateway Interface) utilities.                                                             |
| attrs                      | 25.3.0      | UNKNOWN                                             | A library for creating classes without boilerplate.                                                                                         |
| babel                      | 2.17.0      | BSD License                                         | A collection of tools for internationalizing Python applications.                                                                           |
| backrefs                   | 5.9         | MIT License                                         | A library for finding back-references to objects.                                                                                           |
| certifi                    | 2025.6.15   | Mozilla Public License 2.0 (MPL 2.0)                | A curated collection of Root Certificates for validating the trustworthiness of SSL certificates while verifying the identity of TLS hosts. |
| cffi                       | 1.17.1      | MIT License                                         | A library for calling C code from Python.                                                                                                   |
| cfgv                       | 3.4.0       | MIT License                                         | A library for validating configuration files.                                                                                               |
| charset-normalizer         | 3.4.2       | MIT License                                         | A library that helps you to normalize text.                                                                                                 |
| click                      | 8.2.1       | UNKNOWN                                             | A Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.                       |
| colorama                   | 0.4.6       | BSD License                                         | A library for producing colored terminal text and cursor positioning.                                                                       |
| coverage                   | 7.9.1       | Apache-2.0                                          | A tool for measuring code coverage of Python programs.                                                                                      |
| cryptography               | 45.0.4      | Apache-2.0 OR BSD-3-Clause                          | A package which provides cryptographic recipes and primitives to Python developers.                                                         |
| distlib                    | 0.3.9       | Python Software Foundation License                  | A library of functions for packaging and distribution of Python software.                                                                   |
| dnspython                  | 2.7.0       | ISC License (ISCL)                                  | A DNS toolkit for Python.                                                                                                                   |
| email_validator            | 2.2.0       | The Unlicense (Unlicense)                           | A robust email syntax and deliverability validation library for Python.                                                                     |
| fastapi                    | 0.115.14    | MIT License                                         | A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.                    |
| fastapi-cli                | 0.0.7       | MIT License                                         | A command-line interface for FastAPI.                                                                                                       |
| filelock                   | 3.18.0      | The Unlicense (Unlicense)                           | A platform independent file lock.                                                                                                           |
| frozenlist                 | 1.7.0       | Apache-2.0                                          | A list-like structure which is immutable.                                                                                                   |
| ghp-import                 | 2.1.0       | Apache Software License                             | A tool to import documentation to GitHub Pages.                                                                                             |
| griffe                     | 1.7.3       | UNKNOWN                                             | A library for parsing Python source code and extracting docstrings.                                                                         |
| gunicorn                   | 23.0.0      | MIT License                                         | A Python WSGI HTTP Server for UNIX.                                                                                                         |
| h11                        | 0.16.0      | MIT License                                         | A pure-Python, bring-your-own-I/O implementation of HTTP/1.1.                                                                               |
| httpcore                   | 1.0.9       | BSD License                                         | A minimal low-level HTTP client.                                                                                                            |
| httptools                  | 0.6.4       | MIT License                                         | A collection of Python utilities for HTTP.                                                                                                  |
| httpx                      | 0.28.1      | BSD License                                         | A fully featured HTTP client for Python 3.                                                                                                  |
| identify                   | 2.6.12      | MIT                                                 | A library for identifying file types.                                                                                                       |
| idna                       | 3.10        | BSD License                                         | A library to support the Internationalized Domain Names in Applications (IDNA) protocol as specified in RFC 5891.                           |
| iniconfig                  | 2.1.0       | MIT License                                         | A small and simple INI file parser.                                                                                                         |
| markdown-it-py             | 3.0.0       | MIT License                                         | A Python port of markdown-it.                                                                                                               |
| mdurl                      | 0.1.2       | MIT License                                         | A library for parsing and manipulating URLs.                                                                                                |
| mergedeep                  | 1.3.4       | MIT License                                         | A library for deep merging dictionaries.                                                                                                    |
| mkdocs                     | 1.6.1       | BSD License                                         | A fast, simple and downright gorgeous static site generator that's geared towards building project documentation.                           |
| mkdocs-autorefs            | 1.4.2       | UNKNOWN                                             | A MkDocs plugin for automatically creating cross-references.                                                                                |
| mkdocs-get-deps            | 0.2.0       | MIT License                                         | A MkDocs plugin to get the dependencies of a MkDocs project.                                                                                |
| mkdocs-material            | 9.6.14      | MIT License                                         | A Material Design theme for MkDocs.                                                                                                         |
| mkdocs-material-extensions | 1.3.1       | MIT License                                         | An extension for MkDocs Material theme.                                                                                                     |
| mkdocstrings               | 0.29.1      | UNKNOWN                                             | A MkDocs plugin for automatically generating documentation from docstrings.                                                                 |
| mkdocstrings-python        | 1.16.12     | UNKNOWN                                             | A Python handler for mkdocstrings.                                                                                                          |
| motor                      | 3.7.1       | Apache Software License                             | An asynchronous Python driver for MongoDB.                                                                                                  |
| multidict                  | 6.6.2       | Apache License 2.0                                  | A dictionary-like object that can have multiple values for the same key.                                                                    |
| nodeenv                    | 1.9.1       | BSD License                                         | A tool to create isolated node.js environments.                                                                                             |
| nodejs-wheel-binaries      | 22.16.0     | MIT License                                         | A wheel containing nodejs binaries.                                                                                                         |
| orjson                     | 3.10.18     | Apache Software License; MIT License                | A fast, correct JSON library for Python.                                                                                                    |
| packaging                  | 25.0        | Apache Software License; BSD License                | A library for parsing, comparing, and manipulating Python package versions.                                                                 |
| paginate                   | 0.5.7       | MIT License                                         | A library for paginating iterables.                                                                                                         |
| pathspec                   | 0.12.1      | Mozilla Public License 2.0 (MPL 2.0)                | A library for pattern matching of file paths.                                                                                               |
| phonenumbers               | 8.13.55     | Apache Software License                             | A Python port of Google's libphonenumber library for parsing, formatting, and validating international phone numbers.                       |
| pillow                     | 11.2.1      | UNKNOWN                                             | The Python Imaging Library adds image processing capabilities to your Python interpreter.                                                   |
| pkce                       | 1.0.3       | MIT License                                         | A library for implementing PKCE (Proof Key for Code Exchange).                                                                              |
| platformdirs               | 4.3.8       | MIT License                                         | A small Python module for determining appropriate platform-specific dirs, e.g. a "user data dir".                                           |
| pluggy                     | 1.6.0       | MIT License                                         | A minimalist production-ready plugin system.                                                                                                |
| pre_commit                 | 4.2.0       | MIT License                                         | A framework for managing and maintaining multi-language pre-commit hooks.                                                                   |
| propcache                  | 0.3.2       | Apache Software License                             | A library for caching properties.                                                                                                           |
| pycparser                  | 2.22        | BSD License                                         | A C parser in Python.                                                                                                                       |
| pycryptodome               | 3.20.0      | Apache Software License; BSD License; Public Domain | A self-contained Python package of low-level cryptographic primitives.                                                                      |
| pydantic                   | 2.11.7      | MIT License                                         | Data validation and settings management using Python type annotations.                                                                      |
| pydantic_core              | 2.33.2      | MIT License                                         | The core of pydantic, written in Rust.                                                                                                      |
| pymdown-extensions         | 10.16       | MIT License                                         | A collection of extensions for Python-Markdown.                                                                                             |
| pymongo                    | 4.13.2      | Apache Software License                             | The Python driver for MongoDB.                                                                                                              |
| pyotp                      | 2.9.0       | MIT License                                         | A Python library for generating and verifying one-time passwords.                                                                           |
| pyright                    | 1.1.402     | MIT                                                 | A static type checker for Python.                                                                                                           |
| pytest                     | 8.4.1       | MIT License                                         | A framework for writing small, readable tests.                                                                                              |
| pytest-asyncio             | 1.0.0       | UNKNOWN                                             | A pytest plugin for testing asyncio code.                                                                                                   |
| pytest-cov                 | 6.2.1       | MIT                                                 | A pytest plugin for measuring code coverage.                                                                                                |
| pytest-dotenv              | 0.5.2       | MIT License                                         | A pytest plugin for loading environment variables from a .env file.                                                                         |
| pytest-html                | 4.1.1       | MIT License                                         | A pytest plugin for generating HTML reports.                                                                                                |
| pytest-metadata            | 3.1.1       | Mozilla Public License 2.0 (MPL 2.0)                | A pytest plugin for adding metadata to test reports.                                                                                        |
| python-dateutil            | 2.9.0.post0 | Apache Software License; BSD License                | A library for parsing dates in almost any string format.                                                                                    |
| python-dotenv              | 1.1.1       | BSD License                                         | A library for reading key-value pairs from a .env file and setting them as environment variables.                                           |
| python-multipart           | 0.0.20      | Apache Software License                             | A streaming multipart parser for Python.                                                                                                    |
| pyyaml_env_tag             | 1.1         | UNKNOWN                                             | A PyYAML tag for referencing environment variables.                                                                                         |
| requests                   | 2.32.4      | Apache Software License                             | A simple, yet elegant, HTTP library.                                                                                                        |
| requests-file              | 2.1.0       | Apache Software License                             | A requests transport adapter for local files.                                                                                               |
| rich                       | 14.0.0      | MIT License                                         | A Python library for rich text and beautiful formatting in the terminal.                                                                    |
| rich-toolkit               | 0.14.7      | MIT License                                         | A collection of tools for working with rich.                                                                                                |
| setproctitle               | 1.3.6       | BSD License                                         | A Python library to customize the process title.                                                                                            |
| shellingham                | 1.5.4       | ISC License (ISCL)                                  | A tool to detect the shell you are running in.                                                                                              |
| six                        | 1.17.0      | MIT License                                         | A Python 2 and 3 compatibility library.                                                                                                     |
| sniffio                    | 1.3.1       | Apache Software License; MIT License                | A library for detecting which async library is being used.                                                                                  |
| sqlmodel                   | 0.0.24      | MIT License                                         | A library for interacting with SQL databases from Python code, with Python objects.                                                         |
| starlette                  | 0.46.2      | BSD License                                         | A lightweight ASGI framework/toolkit, which is ideal for building high performance asyncio services.                                        |
| starlette-compress         | 1.6.1       | Zero-Clause BSD (0BSD)                              | A compression middleware for Starlette.                                                                                                     |
| structlog                  | 25.4.0      | Apache Software License; MIT License                | A library for structured logging.                                                                                                           |
| supertokens_python         | 0.30.0      | Apache Software License                             | An open source user authentication solution.                                                                                                |
| tldextract                 | 5.3.0       | BSD License                                         | A library for accurately separating the TLD from the registered domain and subdomain of a URL.                                              |
| twilio                     | 9.6.3       | MIT License                                         | A Python library for communicating with the Twilio API.                                                                                     |
| typer                      | 0.16.0      | MIT License                                         | A library for building great Command Line Interfaces (CLIs).                                                                                |
| typing-inspection          | 0.4.1       | UNKNOWN                                             | A library for inspecting type hints.                                                                                                        |
| typing_extensions          | 4.14.0      | UNKNOWN                                             | A backport of the latest typing features to older Python versions.                                                                          |
| urllib3                    | 2.5.0       | UNKNOWN                                             | A powerful, user-friendly HTTP client for Python.                                                                                           |
| uvicorn                    | 0.35.0      | BSD License                                         | A lightning-fast ASGI server implementation, using uvloop and httptools.                                                                    |
| uvicorn-worker             | 0.3.0       | MIT License                                         | A Gunicorn worker for Uvicorn.                                                                                                              |
| uvloop                     | 0.21.0      | Apache Software License; MIT License                | A fast, drop-in replacement for the default asyncio event loop.                                                                             |
| virtualenv                 | 20.31.2     | MIT License                                         | A tool to create isolated Python environments.                                                                                              |
| watchdog                   | 6.0.0       | Apache Software License                             | A Python API library and shell utilities to monitor file system events.                                                                     |
| watchfiles                 | 1.1.0       | MIT License                                         | A simple, modern and fast file watching library for Python.                                                                                 |
| websockets                 | 15.0.1      | BSD License                                         | A library for building WebSocket servers and clients in Python.                                                                             |
| wrapt                      | 1.17.2      | BSD License                                         | A Python module for decorators, wrappers and monkey patching.                                                                               |
| yarl                       | 1.20.1      | Apache Software License                             | A library for URL parsing and manipulation.                                                                                                 |
| zstandard                  | 0.23.0      | BSD License                                         | A Python binding to the Zstandard compression library.                                                                                      |
