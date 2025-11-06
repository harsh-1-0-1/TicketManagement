# utils/security.py
from pwdlib import PasswordHash

# Initialize Argon2id context (recommended defaults)
pwd_context = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """
    Hashes a plain password using Argon2id.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    Returns True if valid, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
