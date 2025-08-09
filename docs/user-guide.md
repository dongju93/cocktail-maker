# 🧑‍💻 사용자 가이드

이 가이드는 **칵테일 주류 정보 API**를 사용하는 데 필요한 기본적인 정보를 제공합니다. 모든 API의 기본 URL은 `/api/v1` 입니다.

## 🔑 인증 (Authentication)

데이터 등록, 수정, 삭제 등 보호된 엔드포인트에 접근하려면 인증이 필요합니다. 저희 API는 **SuperTokens**를 이용한 쿠키 기반 세션 관리를 사용합니다.

1.  **회원 가입**: `/api/v1/signup` 엔드포인트에 `POST` 요청을 보내 새 계정을 생성합니다.

    **요청 본문 (Request Body):**

    ```json
    {
      "userId": "your_user_id",
      "password": "your_password"
    }
    ```

    회원가입 성공 시, 별도의 로그인 절차 없이 바로 로그인 처리되며, 응답 헤더에 인증용 쿠키(`accessToken`, `refreshToken`)가 설정됩니다.

2.  **로그인**: `/api/v1/signin` 엔드포인트에 `POST` 요청을 보내 로그인합니다.

    **요청 본문 (Request Body):**

    ```json
    {
      "userId": "your_user_id",
      "password": "your_password"
    }
    ```

    로그인 성공 시, 응답 헤더에 인증용 쿠키가 설정됩니다. 이후 모든 요청에 이 쿠키가 자동으로 포함되어야 합니다.

3.  **액세스 토큰 갱신**: `accessToken`이 만료되면 `/api/v1/refresh-token` 엔드포인트로 `POST` 요청을 보내 새로운 토큰을 발급받을 수 있습니다. 이 과정은 `refreshToken` 쿠키를 통해 자동으로 처리됩니다.

## 🥃 주류 (Spirits)

### 주류 정보 등록

새로운 주류 정보를 등록합니다. (인증 필요)

- **Endpoint**: `POST /api/v1/spirits`
- **Content-Type**: `multipart/form-data`

**요청 필드 (Form Data):**

- `name` (string): 이름
- `kind` (string): 종류 (예: Gin, Rum, Vodka)
- `aroma` (list[string]): 향 (메타데이터로 등록된 값)
- `taste` (list[string]): 맛 (메타데이터로 등록된 값)
- `finish` (list[string]): 끝맛 (메타데이터로 등록된 값)
- `main_image` (file): 대표 이미지 파일
- ... 기타 필드는 [API 레퍼런스](api-reference.md) 참고

### 주류 정보 검색

다양한 조건으로 주류 정보를 검색합니다.

- **Endpoint**: `GET /api/v1/spirits`

**쿼리 파라미터 (Query Parameters):**

- `name` (string): 이름으로 검색
- `kind` (string): 종류로 검색
- `taste` (string): 맛으로 검색
- `page` (int): 페이지 번호 (기본값: 1)
- `limit` (int): 페이지 당 항목 수 (기본값: 10)

**예시:**

```http
GET /api/v1/spirits?kind=Gin&taste=dry&page=1&limit=5
```

### 단일 주류 정보 조회

특정 주류의 상세 정보를 조회합니다.

- **Endpoint**: `GET /api/v1/spirits/{name}`

**예시:**

```http
GET /api/v1/spirits/Tanqueray%20London%20Dry%20Gin
```

## 🍹 리큐르 (Liqueur)

### 리큐르 정보 등록

새로운 리큐르 정보를 등록합니다. (인증 필요)

- **Endpoint**: `POST /api/v1/liqueur`
- **Content-Type**: `multipart/form-data`

**요청 필드 (Form Data):**

- `name` (string): 이름
- `brand` (string): 브랜드
- `kind` (string): 종류
- `taste` (list[string]): 맛 (메타데이터로 등록된 값)
- `main_image` (file): 대표 이미지 파일
- ... 기타 필드는 [API 레퍼런스](api-reference.md) 참고

### 리큐르 정보 검색

- **Endpoint**: `GET /api/v1/liqueur`

**쿼리 파라미터 (Query Parameters):**

- `name` (string): 이름으로 검색
- `kind` (string): 종류로 검색
- `page` (int): 페이지 번호
- `limit` (int): 페이지 당 항목 수

## 🌿 기타 재료 (Ingredient)

### 기타 재료 등록

주스, 시럽 등 기타 재료 정보를 등록합니다. (인증 필요)

- **Endpoint**: `POST /api/v1/ingredient`
- **Content-Type**: `multipart/form-data`

**요청 필드 (Form Data):**

- `name` (string): 이름
- `kind` (string): 종류 (예: Juice, Syrup)
- `description` (string): 설명
- `mainImage` (file): 대표 이미지 파일

### 기타 재료 검색

- **Endpoint**: `GET /api/v1/ingredient`

**쿼리 파라미터 (Query Parameters):**

- `name` (string): 이름으로 검색
- `kind` (string): 종류로 검색

## ⚙️ 메타데이터 (Metadata)

맛, 향, 종류 등 검색 및 등록에 사용될 메타데이터를 관리합니다.

### 메타데이터 조회

- **Endpoint**: `GET /api/v1/metadata/{kind}/{category}`
  - `{kind}`: `spirits`, `liqueur`, `ingredient` 중 하나
  - `{category}`: `taste`, `aroma`, `finish`, `kind` 등

**예시:**

```http
GET /api/v1/metadata/spirits/taste
```

### 메타데이터 등록

(관리자 권한 필요)

- **Endpoint**: `POST /api/v1/metadata/{kind}/{category}`

**요청 본문 (Request Body):**

```json
{
  "items": ["sweet", "dry", "fruity"]
}
```

---

더 자세한 엔드포인트 정보와 전체 요청/응답 스키마는 [API 레퍼런스](api-reference.md)를 참고하세요.
