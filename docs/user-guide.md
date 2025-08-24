# 🧑‍💻 사용자 가이드

이 가이드는 **칵테일 주류 정보 API**를 사용하는 데 필요한 기본적인 정보를 제공합니다. 모든 API의 기본 URL은 `/api/v1` 입니다.

## 🔑 인증 (Authentication)

데이터 등록, 수정, 삭제 등 보호된 엔드포인트에 접근하려면 인증이 필요합니다. JWT 기반 쿠키 인증을 사용합니다.

### 회원가입
새 계정을 생성합니다.

- **Endpoint**: `POST /api/v1/signup`
- **Content-Type**: `application/json`

```json
{
  "userId": "your_user_id",
  "password": "your_password"
}
```

**응답**: 회원가입 성공 시 자동으로 로그인되며, 인증 쿠키가 설정됩니다.

### 로그인
기존 계정으로 로그인합니다.

- **Endpoint**: `POST /api/v1/signin`
- **Content-Type**: `application/json`

```json
{
  "userId": "your_user_id", 
  "password": "your_password"
}
```

**응답**: 로그인 성공 시 `accessToken`과 `refreshToken` 쿠키가 설정됩니다.

### 토큰 갱신
액세스 토큰이 만료되면 자동으로 갱신할 수 있습니다.

- **Endpoint**: `POST /api/v1/refresh-token`

쿠키의 `refreshToken`을 사용하여 자동으로 새로운 `accessToken`을 발급합니다.

### 내 권한 확인
현재 로그인된 사용자의 권한을 확인합니다.

- **Endpoint**: `GET /api/v1/my-role`
- **인증**: 필요

## 🥃 주류 (Spirits)

### 주류 등록
새로운 주류 정보를 등록합니다.

- **Endpoint**: `POST /api/v1/spirits`
- **Content-Type**: `multipart/form-data`
- **인증**: 필요

**필수 필드:**
- `name` (string): 주류 이름
- `aroma` (array): 향 특성 (메타데이터 값 사용)
- `taste` (array): 맛 특성 (메타데이터 값 사용)  
- `finish` (array): 여운 특성 (메타데이터 값 사용)
- `kind` (string): 주류 종류 (예: Gin, Whiskey, Rum)
- `subKind` (string): 세부 종류
- `amount` (float): 용량 (mL)
- `alcohol` (float): 알코올 도수 (%)
- `originNation` (string): 원산지 국가
- `originLocation` (string): 원산지 지역
- `description` (string): 설명
- `mainImage` (file): 대표 이미지 (최대 2MB)

**선택 필드:**
- `subImage1-4` (file): 보조 이미지들

```bash
curl -X POST "http://localhost:8000/api/v1/spirits" \
  -F "name=Tanqueray London Dry Gin" \
  -F "aroma=juniper" \
  -F "aroma=citrus" \
  -F "taste=dry" \
  -F "taste=botanical" \
  -F "finish=clean" \
  -F "kind=Gin" \
  -F "subKind=London Dry" \
  -F "amount=750" \
  -F "alcohol=47.3" \
  -F "originNation=England" \
  -F "originLocation=London" \
  -F "description=Classic London Dry Gin" \
  -F "mainImage=@tanqueray.jpg"
```

### 주류 검색
다양한 조건으로 주류를 검색합니다.

- **Endpoint**: `GET /api/v1/spirits`

**쿼리 파라미터:**
- `name` (string): 이름으로 부분 검색
- `aroma` (array): 향 특성으로 정확히 일치
- `taste` (array): 맛 특성으로 정확히 일치
- `finish` (array): 여운 특성으로 정확히 일치
- `kind` (string): 주류 종류로 정확히 일치
- `subKind` (string): 세부 종류로 정확히 일치
- `minAlcohol` (float): 최소 알코올 도수
- `maxAlcohol` (float): 최대 알코올 도수
- `originNation` (string): 원산지 국가로 정확히 일치
- `originLocation` (string): 원산지 지역으로 부분 일치
- `pageNumber` (int): 페이지 번호 (기본값: 1)
- `pageSize` (int): 페이지 크기 (기본값: 10, 최대: 100)

```bash
# 진 종류 검색
curl "http://localhost:8000/api/v1/spirits?kind=Gin&pageNumber=1&pageSize=5"

# 드라이하고 깔끔한 주류 검색
curl "http://localhost:8000/api/v1/spirits?taste=dry&finish=clean"

# 알코올 도수 40-50% 범위 검색
curl "http://localhost:8000/api/v1/spirits?minAlcohol=40&maxAlcohol=50"
```

### 단일 주류 조회
특정 주류의 상세 정보를 조회합니다.

- **Endpoint**: `GET /api/v1/spirits/{name}`

```bash
curl "http://localhost:8000/api/v1/spirits/Tanqueray%20London%20Dry%20Gin"
```

### 주류 수정
기존 주류 정보를 수정합니다.

- **Endpoint**: `PUT /api/v1/spirits/{document_id}`
- **Content-Type**: `multipart/form-data`
- **인증**: 필요

### 주류 삭제
주류 정보를 삭제합니다.

- **Endpoint**: `DELETE /api/v1/spirits/{document_id}`
- **인증**: 필요

## 🍹 리큐르 (Liqueur)

### 리큐르 등록
새로운 리큐르 정보를 등록합니다.

- **Endpoint**: `POST /api/v1/liqueur`
- **Content-Type**: `multipart/form-data`
- **인증**: 필요

**필수 필드:**
- `name` (string): 리큐르 이름
- `brand` (string): 브랜드
- `taste` (array): 맛 특성
- `kind` (string): 리큐르 종류
- `subKind` (string): 세부 종류
- `mainIngredients` (array): 주재료 목록
- `volume` (float): 용량 (mL)
- `abv` (float): 알코올 도수 (%)
- `originNation` (string): 원산지 국가
- `description` (string): 설명
- `mainImage` (file): 대표 이미지

```bash
curl -X POST "http://localhost:8000/api/v1/liqueur" \
  -F "name=Cointreau" \
  -F "brand=Cointreau" \
  -F "taste=sweet" \
  -F "taste=citrus" \
  -F "kind=Triple Sec" \
  -F "subKind=Premium Triple Sec" \
  -F "mainIngredients=orange peel" \
  -F "volume=700" \
  -F "abv=40" \
  -F "originNation=France" \
  -F "description=Premium orange liqueur" \
  -F "mainImage=@cointreau.jpg"
```

### 리큐르 검색
- **Endpoint**: `GET /api/v1/liqueur`
- **인증**: 필요

**주요 쿼리 파라미터:**
- `name`, `brand`, `taste`, `kind`, `subKind`
- `mainIngredients`, `minVolume`, `maxVolume`
- `minAbv`, `maxAbv`, `originNation`
- `pageNumber`, `pageSize`

### 단일 리큐르 조회
- **Endpoint**: `GET /api/v1/liqueur/{name}`

### 리큐르 수정/삭제
- **수정**: `PUT /api/v1/liqueur/{document_id}` (인증 필요)
- **삭제**: `DELETE /api/v1/liqueur/{document_id}` (인증 필요)

## 🌿 기타 재료 (Ingredient)

### 기타 재료 등록
주스, 시럽 등 기타 재료를 등록합니다.

- **Endpoint**: `POST /api/v1/ingredient`
- **Content-Type**: `multipart/form-data`
- **인증**: 필요

**필수 필드:**
- `name` (string): 재료 이름
- `kind` (string): 재료 종류 (예: Juice, Syrup, Bitters)
- `description` (string): 설명
- `mainImage` (file): 대표 이미지

**선택 필드:**
- `brand` (array): 브랜드 목록

```bash
curl -X POST "http://localhost:8000/api/v1/ingredient" \
  -F "name=Simple Syrup" \
  -F "kind=Syrup" \
  -F "description=Basic sugar syrup for cocktails" \
  -F "mainImage=@simple_syrup.jpg"
```

### 기타 재료 검색
- **Endpoint**: `GET /api/v1/ingredient`
- **인증**: 필요

**쿼리 파라미터:**
- `name`, `brand`, `kind`, `description`
- `pageNumber`, `pageSize`

### 단일 기타 재료 조회
- **Endpoint**: `GET /api/v1/ingredient/{name}`

### 기타 재료 수정/삭제
- **수정**: `PUT /api/v1/ingredient/{document_id}` (인증 필요)
- **삭제**: `DELETE /api/v1/ingredient/{document_id}` (인증 필요)

## ⚙️ 메타데이터 (Metadata)

맛, 향, 종류 등 분류에 사용되는 메타데이터를 관리합니다.

### 메타데이터 조회
특정 종류와 카테고리의 메타데이터 목록을 조회합니다.

- **Endpoint**: `GET /api/v1/metadata/{kind}/{category}`
  - `{kind}`: `spirits`, `liqueur`, `ingredient`
  - `{category}`: `taste`, `aroma`, `finish`, `kind`

```bash
# 주류의 맛 메타데이터 조회
curl "http://localhost:8000/api/v1/metadata/spirits/taste"

# 리큐르의 향 메타데이터 조회  
curl "http://localhost:8000/api/v1/metadata/liqueur/aroma"
```

### 메타데이터 등록
새로운 메타데이터 항목을 등록합니다.

- **Endpoint**: `POST /api/v1/metadata/{kind}/{category}`
- **Content-Type**: `application/json`
- **인증**: 관리자 권한 필요

```json
{
  "items": ["sweet", "dry", "fruity", "spicy"]
}
```

### 메타데이터 삭제
메타데이터 항목을 삭제합니다.

- **Endpoint**: `DELETE /api/v1/metadata/{id}`
- **인증**: 관리자 권한 필요

## 📊 응답 형식

모든 API 응답은 다음과 같은 표준화된 형식을 따릅니다:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    // 실제 데이터
  },
  "message": "Successfully retrieved data"
}
```

**페이지네이션된 응답:**
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

## 🚨 오류 처리

오류 발생 시 RFC 9457 Problem Details 형식으로 응답합니다:

```json
{
  "type": "https://httpstatuses.com/400",
  "title": "Client Error 400",
  "detail": "Invalid input data",
  "status": 400
}
```

---

더 자세한 엔드포인트 정보와 전체 요청/응답 스키마는 [API 레퍼런스](api-reference.md)를 참고하세요.
