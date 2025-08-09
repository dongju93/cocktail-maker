# API Reference

이 문서는 칵테일 메이커 프로젝트의 주요 API 엔드포인트 및 데이터 모델에 대한 기술 참조 문서입니다.

코드를 직접 탐색하고 싶다면 `app/main.py` 파일에서 모든 라우트 정의를 확인할 수 있습니다.

## 인증 (Authentication)

인증 관련 엔드포인트는 `app/main.py`에 직접 정의되어 있으며, `supertokens-python` 라이브러리와 상호작용합니다.

::: app.main.sign_up
::: app.main.sign_in
::: app.main.refresh_token

## 주류 (Spirits)

주류 정보 관리 API입니다. CRUD 작업은 `app/query/query_parents.py`의 `CreateSpirits`, `RetrieveSpirits`, `UpdateSpirits`, `DeleteSpirits` 클래스에 구현되어 있습니다.

- **데이터 모델**: `app.model.spirits`
- **라우터**: `app.main.spirits_register`, `app.main.spirits_search`, `app.main.spirits_detail` 등

::: app.model.spirits.SpiritsDict
::: app.model.spirits.SpiritsRegisterForm
::: app.model.spirits.SpiritsSearch

## 리큐르 (Liqueur)

리큐르 정보 관리 API입니다. CRUD 작업은 `app/query/query_parents.py`의 `CreateLiqueur`, `RetrieveLiqueur`, `UpdateLiqueur`, `DeleteLiqueur` 클래스에 구현되어 있습니다.

- **데이터 모델**: `app.model.liqueur`
- **라우터**: `app.main.liqueur_register`, `app.main.liqueur_search`, `app.main.liqueur_detail` 등

::: app.model.liqueur.LiqueurDict
::: app.model.liqueur.LiqueurRegisterForm
::: app.model.liqueur.LiqueurSearchQuery

## 기타 재료 (Ingredient)

기타 재료 정보 관리 API입니다. CRUD 작업은 `app/query/query_child.py`의 `CreateIngredient`, `RetrieveIngredient`, `UpdateIngredient`, `DeleteIngredient` 클래스에 구현되어 있습니다.

- **데이터 모델**: `app.model.ingredients`
- **라우터**: `app.main.ingredient_register`, `app.main.ingredient_search`, `app.main.ingredient_detail` 등

::: app.model.ingredients.IngredientDict
::: app.model.ingredients.IngredientSearch

## 메타데이터 (Metadata)

맛, 향, 종류 등 검색 필터링에 사용되는 메타데이터 API입니다.

- **데이터 모델**: `app.model.etc`
- **라우터**: `app.main.metadata_register`, `app.main.metadata_details`

::: app.model.etc.MetadataRegister
