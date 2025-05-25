# 🧑‍💻 사용자 가이드

이 가이드는 **칵테일 주류 정보 API**를 사용하는 데 필요한 기본적인 정보를 제공합니다.

## 🔑 인증 (Authentication)

저장 및 관리 기능은 JWT(JSON Web Token) 기반의 인증 시스템을 통해
보호됩니다. API를 사용하기 전에 먼저 사용자 계정을 생성하고 로그인하여
액세스 토큰을 발급받아야 합니다.

1.  **회원 가입**: `/auth/register` 엔드포인트를 사용하여 새 계정을 생성합니다.
    (예시)
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
2.  **로그인**: `/auth/login` 엔드포인트를 사용하여 로그인하고 JWT 토큰을 발급받습니다.
    로그인 성공 시 `access_token`을 응답으로 받게 됩니다.
    (예시)
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
    **응답 예시:**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1Ni...",
      "token_type": "bearer"
    }
    ```
3.  **API 요청**: 발급받은 `access_token`을 모든 보호된 API 요청의
    `Authorization` 헤더에 `Bearer <token>` 형식으로 포함해야 합니다.

    ```http
    GET /api/liquors HTTP/1.1
    Host: your-api-domain.com
    Authorization: Bearer eyJhbGciOiJIUzI1Ni...
    ```

## 🔍 주류 정보 검색

로그인 없이도 주류 정보를 검색할 수 있습니다.

*   **모든 주류 조회**:
    ```http
    GET /api/liquors
    ```
*   **특정 주류 ID로 조회**:
    ```http
    GET /api/liquors/{liquor_id}
    ```
*   **주류 이름으로 검색**:
    ```http
    GET /api/liquors?name=gin
    ```
*   **특성(향, 맛 등)으로 검색**:
    ```http
    GET /api/liquors?aroma=citrus&taste=dry
    ```

## ➕ 주류 정보 추가 (관리자 권한 필요)

인증된 사용자(특히 관리자 권한)는 새로운 주류 정보를 추가할 수 있습니다.

```http
POST /api/liquors HTTP/1.1
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1Ni...

{
  "name": "Tanqueray London Dry Gin",
  "type": "Gin",
  "abv": 47.3,
  "country": "England",
  "aroma": ["juniper", "citrus", "coriander"],
  "taste": ["dry", "botanical", "crisp"],
  "finish": ["clean", "peppery"],
  "description": "클래식 런던 드라이 진의 정수.",
  "image_url": "https://example.com/tanqueray.jpg"
}
```

## ✏️ 주류 정보 업데이트 및 삭제 (관리자 권한 필요)

기존 주류 정보의 업데이트와 삭제도 인증된 사용자를 통해 가능합니다.

*   **업데이트**: `PUT /api/liquors/{liquor_id}`
*   **삭제**: `DELETE /api/liquors/{liquor_id}`

더 자세한 엔드포인트 정보는 [API 레퍼런스](api-reference.md)를 참고하세요.