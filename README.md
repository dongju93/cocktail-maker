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

## Test
```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S) && uv run pytest -s --cov=app --html=../tests/results/test-${TIMESTAMP}.html --self-contained-html
```

## Licenses
| Name | Version | License | Description |
|---|---|---|---|
| Brotli | 1.1.0 | MIT License | A generic-purpose lossless compression algorithm. |
| Deprecated | 1.2.18 | MIT License | A library for marking functions and classes as deprecated. |
| Jinja2 | 3.1.6 | BSD License | A modern and designer-friendly templating engine for Python. |
| Markdown | 3.8.2 | UNKNOWN | A Python implementation of John Gruber's Markdown. |
| MarkupSafe | 3.0.2 | BSD License | A library for handling HTML and XML strings in a safe way. |
| PyJWT | 2.10.1 | MIT License | A Python implementation of JSON Web Tokens. |
| PyYAML | 6.0.2 | MIT License | A YAML parser and emitter for Python. |
| Pygments | 2.19.2 | BSD License | A generic syntax highlighter suitable for use in code hosting, forums, wikis or other applications that need to prettify source code. |
| SQLAlchemy | 2.0.41 | MIT | The Python SQL Toolkit and Object Relational Mapper. |
| Secweb | 1.18.1 | Mozilla Public License 2.0 (MPL 2.0) | A library for security scanning of web applications. |
| aiohappyeyeballs | 2.6.1 | Python Software Foundation License | An implementation of the Happy Eyeballs algorithm for asynchronous applications. |
| aiohttp | 3.12.13 | Apache-2.0 | An asynchronous HTTP client/server framework for asyncio and Python. |
| aiohttp-retry | 2.9.1 | MIT License | An asyncio http client/server framework retry library. |
| aiosignal | 1.3.2 | Apache Software License | A library for managing signals in asynchronous applications. |
| aiosmtplib | 3.0.2 | MIT | An asyncio SMTP client. |
| annotated-types | 0.7.0 | MIT License | A library for adding metadata to types. |
| anyio | 4.9.0 | MIT License | An asynchronous networking and concurrency library that works on top of either asyncio or trio. |
| asgiref | 3.8.1 | BSD License | A library that provides ASGI (Asynchronous Server Gateway Interface) utilities. |
| attrs | 25.3.0 | UNKNOWN | A library for creating classes without boilerplate. |
| babel | 2.17.0 | BSD License | A collection of tools for internationalizing Python applications. |
| backrefs | 5.9 | MIT License | A library for finding back-references to objects. |
| certifi | 2025.6.15 | Mozilla Public License 2.0 (MPL 2.0) | A curated collection of Root Certificates for validating the trustworthiness of SSL certificates while verifying the identity of TLS hosts. |
| cffi | 1.17.1 | MIT License | A library for calling C code from Python. |
| cfgv | 3.4.0 | MIT License | A library for validating configuration files. |
| charset-normalizer | 3.4.2 | MIT License | A library that helps you to normalize text. |
| click | 8.2.1 | UNKNOWN | A Python package for creating beautiful command line interfaces in a composable way with as little code as necessary. |
| colorama | 0.4.6 | BSD License | A library for producing colored terminal text and cursor positioning. |
| coverage | 7.9.1 | Apache-2.0 | A tool for measuring code coverage of Python programs. |
| cryptography | 45.0.4 | Apache-2.0 OR BSD-3-Clause | A package which provides cryptographic recipes and primitives to Python developers. |
| distlib | 0.3.9 | Python Software Foundation License | A library of functions for packaging and distribution of Python software. |
| dnspython | 2.7.0 | ISC License (ISCL) | A DNS toolkit for Python. |
| email_validator | 2.2.0 | The Unlicense (Unlicense) | A robust email syntax and deliverability validation library for Python. |
| fastapi | 0.115.14 | MIT License | A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. |
| fastapi-cli | 0.0.7 | MIT License | A command-line interface for FastAPI. |
| filelock | 3.18.0 | The Unlicense (Unlicense) | A platform independent file lock. |
| frozenlist | 1.7.0 | Apache-2.0 | A list-like structure which is immutable. |
| ghp-import | 2.1.0 | Apache Software License | A tool to import documentation to GitHub Pages. |
| griffe | 1.7.3 | UNKNOWN | A library for parsing Python source code and extracting docstrings. |
| gunicorn | 23.0.0 | MIT License | A Python WSGI HTTP Server for UNIX. |
| h11 | 0.16.0 | MIT License | A pure-Python, bring-your-own-I/O implementation of HTTP/1.1. |
| httpcore | 1.0.9 | BSD License | A minimal low-level HTTP client. |
| httptools | 0.6.4 | MIT License | A collection of Python utilities for HTTP. |
| httpx | 0.28.1 | BSD License | A fully featured HTTP client for Python 3. |
| identify | 2.6.12 | MIT | A library for identifying file types. |
| idna | 3.10 | BSD License | A library to support the Internationalized Domain Names in Applications (IDNA) protocol as specified in RFC 5891. |
| iniconfig | 2.1.0 | MIT License | A small and simple INI file parser. |
| markdown-it-py | 3.0.0 | MIT License | A Python port of markdown-it. |
| mdurl | 0.1.2 | MIT License | A library for parsing and manipulating URLs. |
| mergedeep | 1.3.4 | MIT License | A library for deep merging dictionaries. |
| mkdocs | 1.6.1 | BSD License | A fast, simple and downright gorgeous static site generator that's geared towards building project documentation. |
| mkdocs-autorefs | 1.4.2 | UNKNOWN | A MkDocs plugin for automatically creating cross-references. |
| mkdocs-get-deps | 0.2.0 | MIT License | A MkDocs plugin to get the dependencies of a MkDocs project. |
| mkdocs-material | 9.6.14 | MIT License | A Material Design theme for MkDocs. |
| mkdocs-material-extensions | 1.3.1 | MIT License | An extension for MkDocs Material theme. |
| mkdocstrings | 0.29.1 | UNKNOWN | A MkDocs plugin for automatically generating documentation from docstrings. |
| mkdocstrings-python | 1.16.12 | UNKNOWN | A Python handler for mkdocstrings. |
| motor | 3.7.1 | Apache Software License | An asynchronous Python driver for MongoDB. |
| multidict | 6.6.2 | Apache License 2.0 | A dictionary-like object that can have multiple values for the same key. |
| nodeenv | 1.9.1 | BSD License | A tool to create isolated node.js environments. |
| nodejs-wheel-binaries | 22.16.0 | MIT License | A wheel containing nodejs binaries. |
| orjson | 3.10.18 | Apache Software License; MIT License | A fast, correct JSON library for Python. |
| packaging | 25.0 | Apache Software License; BSD License | A library for parsing, comparing, and manipulating Python package versions. |
| paginate | 0.5.7 | MIT License | A library for paginating iterables. |
| pathspec | 0.12.1 | Mozilla Public License 2.0 (MPL 2.0) | A library for pattern matching of file paths. |
| phonenumbers | 8.13.55 | Apache Software License | A Python port of Google's libphonenumber library for parsing, formatting, and validating international phone numbers. |
| pillow | 11.2.1 | UNKNOWN | The Python Imaging Library adds image processing capabilities to your Python interpreter. |
| pkce | 1.0.3 | MIT License | A library for implementing PKCE (Proof Key for Code Exchange). |
| platformdirs | 4.3.8 | MIT License | A small Python module for determining appropriate platform-specific dirs, e.g. a "user data dir". |
| pluggy | 1.6.0 | MIT License | A minimalist production-ready plugin system. |
| pre_commit | 4.2.0 | MIT License | A framework for managing and maintaining multi-language pre-commit hooks. |
| propcache | 0.3.2 | Apache Software License | A library for caching properties. |
| pycparser | 2.22 | BSD License | A C parser in Python. |
| pycryptodome | 3.20.0 | Apache Software License; BSD License; Public Domain | A self-contained Python package of low-level cryptographic primitives. |
| pydantic | 2.11.7 | MIT License | Data validation and settings management using Python type annotations. |
| pydantic_core | 2.33.2 | MIT License | The core of pydantic, written in Rust. |
| pymdown-extensions | 10.16 | MIT License | A collection of extensions for Python-Markdown. |
| pymongo | 4.13.2 | Apache Software License | The Python driver for MongoDB. |
| pyotp | 2.9.0 | MIT License | A Python library for generating and verifying one-time passwords. |
| pyright | 1.1.402 | MIT | A static type checker for Python. |
| pytest | 8.4.1 | MIT License | A framework for writing small, readable tests. |
| pytest-asyncio | 1.0.0 | UNKNOWN | A pytest plugin for testing asyncio code. |
| pytest-cov | 6.2.1 | MIT | A pytest plugin for measuring code coverage. |
| pytest-dotenv | 0.5.2 | MIT License | A pytest plugin for loading environment variables from a .env file. |
| pytest-html | 4.1.1 | MIT License | A pytest plugin for generating HTML reports. |
| pytest-metadata | 3.1.1 | Mozilla Public License 2.0 (MPL 2.0) | A pytest plugin for adding metadata to test reports. |
| python-dateutil | 2.9.0.post0 | Apache Software License; BSD License | A library for parsing dates in almost any string format. |
| python-dotenv | 1.1.1 | BSD License | A library for reading key-value pairs from a .env file and setting them as environment variables. |
| python-multipart | 0.0.20 | Apache Software License | A streaming multipart parser for Python. |
| pyyaml_env_tag | 1.1 | UNKNOWN | A PyYAML tag for referencing environment variables. |
| requests | 2.32.4 | Apache Software License | A simple, yet elegant, HTTP library. |
| requests-file | 2.1.0 | Apache Software License | A requests transport adapter for local files. |
| rich | 14.0.0 | MIT License | A Python library for rich text and beautiful formatting in the terminal. |
| rich-toolkit | 0.14.7 | MIT License | A collection of tools for working with rich. |
| setproctitle | 1.3.6 | BSD License | A Python library to customize the process title. |
| shellingham | 1.5.4 | ISC License (ISCL) | A tool to detect the shell you are running in. |
| six | 1.17.0 | MIT License | A Python 2 and 3 compatibility library. |
| sniffio | 1.3.1 | Apache Software License; MIT License | A library for detecting which async library is being used. |
| sqlmodel | 0.0.24 | MIT License | A library for interacting with SQL databases from Python code, with Python objects. |
| starlette | 0.46.2 | BSD License | A lightweight ASGI framework/toolkit, which is ideal for building high performance asyncio services. |
| starlette-compress | 1.6.1 | Zero-Clause BSD (0BSD) | A compression middleware for Starlette. |
| structlog | 25.4.0 | Apache Software License; MIT License | A library for structured logging. |
| supertokens_python | 0.30.0 | Apache Software License | An open source user authentication solution. |
| tldextract | 5.3.0 | BSD License | A library for accurately separating the TLD from the registered domain and subdomain of a URL. |
| twilio | 9.6.3 | MIT License | A Python library for communicating with the Twilio API. |
| typer | 0.16.0 | MIT License | A library for building great Command Line Interfaces (CLIs). |
| typing-inspection | 0.4.1 | UNKNOWN | A library for inspecting type hints. |
| typing_extensions | 4.14.0 | UNKNOWN | A backport of the latest typing features to older Python versions. |
| urllib3 | 2.5.0 | UNKNOWN | A powerful, user-friendly HTTP client for Python. |
| uvicorn | 0.35.0 | BSD License | A lightning-fast ASGI server implementation, using uvloop and httptools. |
| uvicorn-worker | 0.3.0 | MIT License | A Gunicorn worker for Uvicorn. |
| uvloop | 0.21.0 | Apache Software License; MIT License | A fast, drop-in replacement for the default asyncio event loop. |
| virtualenv | 20.31.2 | MIT License | A tool to create isolated Python environments. |
| watchdog | 6.0.0 | Apache Software License | A Python API library and shell utilities to monitor file system events. |
| watchfiles | 1.1.0 | MIT License | A simple, modern and fast file watching library for Python. |
| websockets | 15.0.1 | BSD License | A library for building WebSocket servers and clients in Python. |
| wrapt | 1.17.2 | BSD License | A Python module for decorators, wrappers and monkey patching. |
| yarl | 1.20.1 | Apache Software License | A library for URL parsing and manipulation. |
| zstandard | 0.23.0 | BSD License | A Python binding to the Zstandard compression library. |

