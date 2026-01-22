# client/encryption.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cryptography.fernet import Fernet
from common.crypto_utils import derive_key

class EncryptionManager:
    def __init__(self, password):
        self.key = derive_key(password)
        self.cipher = Fernet(self.key)
    
    def encrypt_message(self, message: str) -> bytes:
        """Encrypts a string message into bytes"""
        return self.cipher.encrypt(message.encode())
    
    def decrypt_message(self, encrypted_bytes: bytes) -> str:
        """Decrypts bytes back into a string"""
        try:
            return self.cipher.decrypt(encrypted_bytes).decode()
        except Exception:
            return "[Decryption Failed: Wrong Password]"