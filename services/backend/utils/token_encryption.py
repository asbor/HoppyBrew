"""
Token encryption utilities for secure API token storage.
"""

import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


def generate_salt() -> str:
    """Generate a cryptographically secure salt for token encryption."""
    return secrets.token_hex(32)


def derive_key_from_password(password: str, salt: bytes) -> bytes:
    """Derive encryption key from password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_token(token: str, salt: str = None) -> tuple[str, str]:
    """
    Encrypt an API token for secure storage.

    Args:
        token: The plaintext API token
        salt: Optional salt (will generate if not provided)

    Returns:
        Tuple of (encrypted_token, salt)
    """
    if not salt:
        salt = generate_salt()

    # Use environment variable or generate a master key
    master_key = os.getenv("DEVICE_TOKEN_KEY", "default-key-change-in-production")

    salt_bytes = bytes.fromhex(salt)
    key = derive_key_from_password(master_key, salt_bytes)

    fernet = Fernet(key)
    encrypted = fernet.encrypt(token.encode())

    return base64.urlsafe_b64encode(encrypted).decode(), salt


def decrypt_token(encrypted_token: str, salt: str) -> str:
    """
    Decrypt an API token for use.

    Args:
        encrypted_token: The base64 encoded encrypted token
        salt: The salt used for encryption

    Returns:
        The decrypted plaintext token
    """
    master_key = os.getenv("DEVICE_TOKEN_KEY", "default-key-change-in-production")

    salt_bytes = bytes.fromhex(salt)
    key = derive_key_from_password(master_key, salt_bytes)

    fernet = Fernet(key)
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_token.encode())

    return fernet.decrypt(encrypted_bytes).decode()


# Example usage:
# encrypted, salt = encrypt_token("my-secret-api-token")
# decrypted = decrypt_token(encrypted, salt)
