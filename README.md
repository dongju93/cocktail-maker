# 칵테일 메이커

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
  - [ ] 리큐르 정보 수정 - ID
  - [ ] 리큐르 정보 삭제 - ID
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

## Test
```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S) && uv run pytest -s --cov=app --html=../tests/results/test-${TIMESTAMP}.html --self-contained-html
```
