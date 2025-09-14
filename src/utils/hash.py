from cryptography.fernet import Fernet
from config import settings

def hashToken(token: str) -> str:
    cipher_suite = Fernet(settings.ENCRYPTION_KEY)
    return cipher_suite.encrypt(token.encode()).decode()

def unencryptToken(hashed_token: str) -> str:
    cipher_suite = Fernet(settings.ENCRYPTION_KEY)
    return cipher_suite.decrypt(hashed_token.encode()).decode()