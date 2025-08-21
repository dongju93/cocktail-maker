from base64 import urlsafe_b64decode

import pytest

from auth.encryption import Encryption  # type: ignore[import]


class TestEncryption:
    def test_passwords_without_salt_generates_random_salt(self):
        """Test that passwords() generates a random salt when none is provided."""
        password = "test_password"
        result = Encryption.passwords(password)

        assert "encrypted_password" in result
        assert "salt" in result

        # Verify salt is base64 encoded and has correct length when decoded
        decoded_salt = urlsafe_b64decode(result["salt"])
        assert len(decoded_salt) == Encryption.SALT_LENGTH

    def test_passwords_with_provided_salt(self):
        """Test that passwords() uses the provided salt."""
        password = "test_password"
        salt = b"a" * Encryption.SALT_LENGTH

        result = Encryption.passwords(password, salt)

        assert "encrypted_password" in result
        assert "salt" in result

        # Verify the provided salt is used
        decoded_salt = urlsafe_b64decode(result["salt"])
        assert decoded_salt == salt

    def test_passwords_deterministic_with_same_salt(self):
        """Test that the same password and salt always produce the same result."""
        password = "test_password"
        salt = b"b" * Encryption.SALT_LENGTH

        result1 = Encryption.passwords(password, salt)
        result2 = Encryption.passwords(password, salt)

        assert result1["encrypted_password"] == result2["encrypted_password"]
        assert result1["salt"] == result2["salt"]

    def test_passwords_different_with_different_salts(self):
        """Test that the same password with different salts produces different results."""
        password = "test_password"
        salt1 = b"c" * Encryption.SALT_LENGTH
        salt2 = b"d" * Encryption.SALT_LENGTH

        result1 = Encryption.passwords(password, salt1)
        result2 = Encryption.passwords(password, salt2)

        assert result1["encrypted_password"] != result2["encrypted_password"]
        assert result1["salt"] != result2["salt"]

    def test_passwords_different_passwords_different_results(self):
        """Test that different passwords produce different encrypted results."""
        salt = b"e" * Encryption.SALT_LENGTH

        result1 = Encryption.passwords("password1", salt)
        result2 = Encryption.passwords("password2", salt)

        assert result1["encrypted_password"] != result2["encrypted_password"]
        assert result1["salt"] == result2["salt"]  # Same salt

    def test_passwords_random_salts_are_different(self):
        """Test that multiple calls without salt generate different salts."""
        password = "test_password"

        result1 = Encryption.passwords(password)
        result2 = Encryption.passwords(password)

        assert result1["salt"] != result2["salt"]
        assert result1["encrypted_password"] != result2["encrypted_password"]

    def test_passwords_empty_password(self):
        """Test encryption with empty password."""
        password = ""
        salt = b"f" * Encryption.SALT_LENGTH

        result = Encryption.passwords(password, salt)

        assert "encrypted_password" in result
        assert "salt" in result

    def test_passwords_unicode_password(self):
        """Test encryption with unicode characters."""
        password = "🔐테스트密码"
        salt = b"g" * Encryption.SALT_LENGTH

        result = Encryption.passwords(password, salt)

        assert "encrypted_password" in result
        assert "salt" in result

    def test_passwords_long_password(self):
        """Test encryption with a very long password."""
        password = "a" * 1000
        salt = b"h" * Encryption.SALT_LENGTH

        result = Encryption.passwords(password, salt)

        assert "encrypted_password" in result
        assert "salt" in result

    def test_passwords_output_format(self):
        """Test that the output is properly base64 encoded."""
        password = "test_password"
        salt = b"i" * Encryption.SALT_LENGTH

        result = Encryption.passwords(password, salt)

        # Should not raise exceptions when decoding
        urlsafe_b64decode(result["encrypted_password"])
        urlsafe_b64decode(result["salt"])

        # Verify encrypted password length
        decoded_password = urlsafe_b64decode(result["encrypted_password"])
        assert len(decoded_password) == Encryption.SALT_LENGTH

    def test_encryption_constants(self):
        """Test that encryption constants have expected values."""
        assert Encryption.SALT_LENGTH == 32
        assert Encryption.ITERATIONS == 600_000

    def test_random_salt_length(self):
        """Test that _random_salt generates correct length salt."""
        salt = Encryption._random_salt()
        assert len(salt) == Encryption.SALT_LENGTH
        assert isinstance(salt, bytes)

    def test_random_salt_uniqueness(self):
        """Test that _random_salt generates unique salts."""
        salt1 = Encryption._random_salt()
        salt2 = Encryption._random_salt()
        assert salt1 != salt2

    def test_passwords_with_invalid_password_type(self):
        """Test passwords with non-string password."""
        with pytest.raises(AttributeError):
            Encryption.passwords(12345)

    def test_passwords_with_invalid_salt_type(self):
        """Test passwords with non-bytes salt."""
        with pytest.raises(TypeError):
            Encryption.passwords("test_password", "not_bytes")
