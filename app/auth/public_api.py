from base64 import urlsafe_b64encode
from hashlib import sha256
from os import environ

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv

load_dotenv()

PUBLIC_API_MASTER_KEY: str = environ["PUBLIC_API_MASTER_KEY"]
PUBLIC_API_SALT: str = environ["PUBLIC_API_SALT"]


class ProductionAPIKeyGenerator:
    """
    생산 환경 API 키 생성기
    - 결정적 키 생성: 같은 입력은 같은 키 반환
    - 고정 솔트 사용: 키 생성 시마다 동일한 솔트 사용
    - OWASP 권장 PBKDF2HMAC 사용: SHA-512 해시 알고리즘, 64바이트 키, 210,000회 반복
    - URL-safe Base64 인코딩: API 키를 안전하게 전송 가능
    - sk-cm- 접두사: API 키 형식 통일
    """

    # // TODO: 누가, 언제, 왜 발급했는지 기록해야함
    # // TODO: API 키를 인증을 요청받으면 저장된 시간과 실제 요청한 도메인으로 키를 재생산하여 검증, API 키 자체를 저장하게되면 유출 시 악용 우려
    """
    1. API 요청 시 요청한 도메인을 데이터베이스에서 검색
    2. 저장된 시간과 도메인으로 API 키를 재생산
    3. 재생산된 API 키와 요청한 API 키를 비교하여 유효성 검증
    * 권한은..?
    """

    def __init__(self, master_key: bytes, persistent_salt: bytes) -> None:
        self.master_key: bytes = master_key
        self.salt: bytes = persistent_salt

    def generate_api_key(self, domain: str, timestamp: int) -> str:
        # 사용자별 고유 시드 생성
        seed: bytes = f"{domain}:{timestamp}".encode()
        deterministic_input: bytes = sha256(self.master_key + seed).digest()

        kdf = PBKDF2HMAC(  # Password-Based Key Derivation Function 2
            algorithm=SHA512(),  # SHA-512 해시 알고리즘 사용
            length=64,  # 64바이트 길이의 키 생성
            salt=self.salt,  # 고정 솔트 사용
            iterations=210000,  # OWASP 권장
            backend=default_backend(),  # 최적의 백엔드 사용
        )

        derived_key: bytes = kdf.derive(deterministic_input)  # 키 파생
        api_key: str = (
            urlsafe_b64encode(derived_key).decode().rstrip("=")
        )  # URL-safe Base64 인코딩

        return f"sk-cm-{api_key}"

    @classmethod
    def from_env(cls) -> "ProductionAPIKeyGenerator":
        master_key: bytes = bytes.fromhex(PUBLIC_API_MASTER_KEY)
        salt: bytes = bytes.fromhex(PUBLIC_API_SALT)
        return cls(master_key, salt)
