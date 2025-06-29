from base64 import urlsafe_b64encode
from secrets import token_bytes

from cryptography.hazmat.primitives.hashes import SHA3_256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from model import PasswordAndSalt


class Encryption:
    def __init__(self) -> None:
        self.SALT_LENGTH: int = 32
        self.ITERATIONS: int = 600_000

    def _random_salt(self) -> bytes:
        return token_bytes(self.SALT_LENGTH)

    def _hmac_sha3_256(self, salt: bytes) -> PBKDF2HMAC:
        return PBKDF2HMAC(
            algorithm=SHA3_256(),
            length=self.SALT_LENGTH,
            salt=salt,
            iterations=self.ITERATIONS,
        )

    def _derive_key(self, kdf: PBKDF2HMAC, password: str) -> bytes:
        return kdf.derive(password.encode())

    def passwords(self, password: str, salt: bytes | None = None) -> PasswordAndSalt:
        if salt is None:
            salt = self._random_salt()

        kdf: PBKDF2HMAC = self._hmac_sha3_256(salt)
        encrypted_password: bytes = self._derive_key(kdf, password)

        return PasswordAndSalt(
            encrypted_password=urlsafe_b64encode(encrypted_password).decode(),
            salt=urlsafe_b64encode(salt).decode(),
        )
