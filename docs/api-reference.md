# API Reference

이 문서는 칵테일 메이커 프로젝트의 주요 API 엔드포인트 및 데이터 모델에 대한 기술 참조 문서입니다.

**Base URL**: `http://localhost:8000/api/v1`

## 📋 목차

- [인증 (Authentication)](#인증-authentication)
- [주류 (Spirits)](#주류-spirits)
- [리큐르 (Liqueur)](#리큐르-liqueur)
- [기타 재료 (Ingredient)](#기타-재료-ingredient)
- [메타데이터 (Metadata)](#메타데이터-metadata)
- [상태 확인 (Health Check)](#상태-확인-health-check)

## 인증 (Authentication)

### POST /signup
**요약**: 회원가입  
**인증**: 불필요

**요청 본문**:
```json
{
  "userId": "string",
  "password": "string"
}
```

**응답**: 
- `204 No Content`: 회원가입 성공, 자동 로그인 및 쿠키 설정
- `409 Conflict`: 이미 존재하는 사용자

### POST /signin
**요약**: 로그인  
**인증**: 불필요

**요청 본문**:
```json
{
  "userId": "string", 
  "password": "string"
}
```

**응답**:
- `204 No Content`: 로그인 성공, 인증 쿠키 설정
- `401 Unauthorized`: 잘못된 인증 정보

### POST /refresh-token
**요약**: 액세스 토큰 갱신  
**인증**: refreshToken 쿠키 필요

**응답**:
- `204 No Content`: 토큰 갱신 성공
- `401 Unauthorized`: 리프레시 토큰 누락 또는 만료

### GET /my-role
**요약**: 현재 사용자 권한 확인  
**인증**: 필요

**응답**:
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "roles": ["admin", "user"]
  },
  "message": "Successfully get user roles"
}
```

### POST /publish-api-key
**요약**: API 키 발급  
**인증**: 관리자 권한 필요

**요청 본문**:
```json
{
  "domain": "string"
}
```

**응답**:
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "api_key": "generated_api_key"
  },
  "message": "API key generated successfully"
}
```

## 주류 (Spirits)

### POST /spirits
**요약**: 주류 정보 등록  
**인증**: 필요  
**Content-Type**: `multipart/form-data`

**폼 필드**:
- `name` (string, 필수): 주류 이름
- `aroma` (array[string], 필수): 향 특성 목록
- `taste` (array[string], 필수): 맛 특성 목록
- `finish` (array[string], 필수): 여운 특성 목록
- `kind` (string, 필수): 주류 종류
- `subKind` (string, 필수): 세부 종류
- `amount` (float, 필수): 용량 (mL)
- `alcohol` (float, 필수): 알코올 도수 (%)
- `originNation` (string, 필수): 원산지 국가
- `originLocation` (string, 필수): 원산지 지역
- `description` (string, 필수): 설명
- `mainImage` (file, 필수): 대표 이미지 (최대 2MB)
- `subImage1-4` (file, 선택): 보조 이미지들

**응답**:
```json
{
  "status": "success",
  "code": 201,
  "data": "document_id", 
  "message": "Successfully register spirits"
}
```

### GET /spirits
**요약**: 주류 검색  
**인증**: 불필요

**쿼리 파라미터**:
- `name` (string): 이름 부분 일치 검색
- `aroma` (array[string]): 향 특성 정확 일치
- `taste` (array[string]): 맛 특성 정확 일치  
- `finish` (array[string]): 여운 특성 정확 일치
- `kind` (string): 주류 종류 정확 일치
- `subKind` (string): 세부 종류 정확 일치
- `minAlcohol` (float): 최소 알코올 도수
- `maxAlcohol` (float): 최대 알코올 도수
- `originNation` (string): 원산지 국가 정확 일치
- `originLocation` (string): 원산지 지역 부분 일치
- `pageNumber` (int, 기본값: 1): 페이지 번호
- `pageSize` (int, 기본값: 10, 최대: 100): 페이지 크기

**응답**:
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "items": [...],
    "total_count": 150,
    "page_number": 1,
    "page_size": 10,
    "total_pages": 15
  },
  "message": "Successfully search spirits"
}
```

### GET /spirits/{name}
**요약**: 단일 주류 조회  
**인증**: 불필요

**경로 파라미터**:
- `name` (string): 주류 이름 (정확한 일치)

**응답**:
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "name": "Tanqueray London Dry Gin",
    "aroma": ["juniper", "citrus"],
    "taste": ["dry", "botanical"],
    "finish": ["clean"],
    "kind": "Gin",
    "sub_kind": "London Dry",
    "amount": 750.0,
    "alcohol": 47.3,
    "origin_nation": "England",
    "origin_location": "London",
    "description": "Classic London Dry Gin",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "message": "Successfully get spirits"
}
```

### PUT /spirits/{document_id}
**요약**: 주류 정보 수정  
**인증**: 필요  
**Content-Type**: `multipart/form-data`

**경로 파라미터**:
- `document_id` (string): MongoDB 문서 ID

**폼 필드**: POST /spirits와 동일

**응답**:
- `204 No Content`: 수정 성공

### DELETE /spirits/{document_id}
**요약**: 주류 정보 삭제  
**인증**: 필요

**경로 파라미터**:
- `document_id` (string): MongoDB 문서 ID

**응답**:
```json
{
  "status": "success",
  "code": 200,
  "data": null,
  "message": "Successfully delete spirits"
}
```

## 리큐르 (Liqueur)

### POST /liqueur
**요약**: 리큐르 정보 등록  
**인증**: 필요  
**Content-Type**: `multipart/form-data`

**폼 필드**:
- `name` (string, 필수): 리큐르 이름
- `brand` (string, 필수): 브랜드
- `taste` (array[string], 필수): 맛 특성 목록
- `kind` (string, 필수): 리큐르 종류
- `subKind` (string, 필수): 세부 종류
- `mainIngredients` (array[string], 필수): 주재료 목록
- `volume` (float, 필수): 용량 (mL)
- `abv` (float, 필수): 알코올 도수 (%)
- `originNation` (string, 필수): 원산지 국가
- `description` (string, 필수): 설명
- `mainImage` (file, 필수): 대표 이미지

### GET /liqueur
**요약**: 리큐르 검색  
**인증**: 필요

**쿼리 파라미터**:
- `name` (string): 이름 부분 일치
- `brand` (string): 브랜드 정확 일치
- `taste` (array[string]): 맛 특성 정확 일치
- `kind` (string): 종류 정확 일치
- `subKind` (string): 세부 종류 정확 일치
- `mainIngredients` (array[string]): 주재료 정확 일치
- `minVolume` (float): 최소 용량
- `maxVolume` (float): 최대 용량
- `minAbv` (float): 최소 알코올 도수
- `maxAbv` (float): 최대 알코올 도수
- `originNation` (string): 원산지 국가 정확 일치
- `pageNumber` (int): 페이지 번호
- `pageSize` (int): 페이지 크기

### GET /liqueur/{name}
**요약**: 단일 리큐르 조회  
**인증**: 불필요

### PUT /liqueur/{document_id}
**요약**: 리큐르 정보 수정  
**인증**: 필요

### DELETE /liqueur/{document_id}
**요약**: 리큐르 정보 삭제  
**인증**: 필요

## 기타 재료 (Ingredient)

### POST /ingredient
**요약**: 기타 재료 등록  
**인증**: 필요  
**Content-Type**: `multipart/form-data`

**폼 필드**:
- `name` (string, 필수): 재료 이름
- `kind` (string, 필수): 재료 종류
- `description` (string, 필수): 설명
- `mainImage` (file, 필수): 대표 이미지
- `brand` (array[string], 선택): 브랜드 목록

### GET /ingredient
**요약**: 기타 재료 검색  
**인증**: 필요

**쿼리 파라미터**:
- `name` (string): 이름 부분 일치
- `brand` (array[string]): 브랜드 정확 일치
- `kind` (string): 종류 정확 일치
- `description` (string): 설명 부분 일치
- `pageNumber` (int): 페이지 번호
- `pageSize` (int): 페이지 크기

### GET /ingredient/{name}
**요약**: 단일 기타 재료 조회  
**인증**: 불필요

### PUT /ingredient/{document_id}
**요약**: 기타 재료 수정  
**인증**: 필요

### DELETE /ingredient/{document_id}
**요약**: 기타 재료 삭제  
**인증**: 필요

## 메타데이터 (Metadata)

### GET /metadata/{kind}/{category}
**요약**: 메타데이터 조회  
**인증**: 불필요

**경로 파라미터**:
- `kind`: `spirits`, `liqueur`, `ingredient`
- `category`: `taste`, `aroma`, `finish`, `kind`

**응답**:
```json
{
  "status": "success",
  "code": 200,
  "data": [
    {
      "id": 1,
      "value": "sweet"
    },
    {
      "id": 2, 
      "value": "dry"
    }
  ],
  "message": "Successfully get metadata"
}
```

### POST /metadata/{kind}/{category}
**요약**: 메타데이터 등록  
**인증**: 관리자 권한 필요

**요청 본문**:
```json
{
  "items": ["sweet", "dry", "fruity"]
}
```

### DELETE /metadata/{id}
**요약**: 메타데이터 삭제  
**인증**: 관리자 권한 필요

**경로 파라미터**:
- `id` (int): 메타데이터 ID

## 상태 확인 (Health Check)

### GET /health
**요약**: 서비스 상태 확인  
**인증**: 불필요

**응답**:
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "status": "ok"
  },
  "message": "Service is running"
}
```

## 🚨 공통 오류 응답

모든 엔드포인트는 오류 발생 시 RFC 9457 Problem Details 형식으로 응답합니다:

```json
{
  "type": "https://httpstatuses.com/400",
  "title": "Client Error 400",
  "detail": "Detailed error message",
  "status": 400
}
```

**주요 HTTP 상태 코드**:
- `200`: 성공
- `201`: 생성 성공
- `204`: 성공 (응답 본문 없음)
- `400`: 잘못된 요청
- `401`: 인증 필요
- `403`: 권한 없음
- `404`: 리소스 없음
- `409`: 중복 리소스
- `422`: 검증 오류
- `500`: 서버 오류

## 💡 추가 정보

코드를 직접 탐색하고 싶다면:
- **라우트 정의**: `app/main.py`
- **데이터 모델**: `app/model/`
- **CRUD 작업**: `app/query/`
- **인증 로직**: `app/auth/`

**상호작용 문서**: 
- Swagger UI: `/api/docs`
- ReDoc: `/api/redoc`
