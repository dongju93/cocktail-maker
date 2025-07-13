from base64 import urlsafe_b64encode
from secrets import token_bytes

from cryptography.hazmat.primitives.hashes import SHA3_256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from model import PasswordAndSalt


class Encryption:
    SALT_LENGTH: int = 32
    ITERATIONS: int = 600_000

    @classmethod
    def _random_salt(cls) -> bytes:
        return token_bytes(cls.SALT_LENGTH)

    @classmethod
    def _hmac_sha3_256(cls, salt: bytes) -> PBKDF2HMAC:
        return PBKDF2HMAC(
            algorithm=SHA3_256(),
            length=cls.SALT_LENGTH,
            salt=salt,
            iterations=cls.ITERATIONS,
        )

    @staticmethod
    def _derive_key(kdf: PBKDF2HMAC, password: str) -> bytes:
        return kdf.derive(password.encode())

    @classmethod
    def passwords(cls, password: str, salt: bytes | None = None) -> PasswordAndSalt:
        if salt is None:
            salt = cls._random_salt()

        kdf: PBKDF2HMAC = cls._hmac_sha3_256(salt)
        encrypted_password: bytes = cls._derive_key(kdf, password)

        return PasswordAndSalt(
            encrypted_password=urlsafe_b64encode(encrypted_password).decode(),
            salt=urlsafe_b64encode(salt).decode(),
        )
