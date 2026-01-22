# common/crypto_utils.py
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from common.constants import FIXED_SALT

def derive_key(password: str) -> bytes:
    """
    Derives a 32-byte URL-safe base64-encoded key from a password.
    Uses PBKDF2HMAC with SHA256.
    """
    password_bytes = password.encode('utf-8')
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=FIXED_SALT,
        iterations=100_000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key