# utils/security.py
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Any

from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from dotenv import load_dotenv
from fastapi import HTTPException, status

from pwdlib import PasswordHash

# -----------------------
# Load config / secrets
# -----------------------
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-do-not-use-in-prod")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "5"))

# -----------------------
# Password hashing (pwdlib)
# -----------------------
pwd_context = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

# -----------------------
# JWT helpers
# -----------------------
def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

def _expiry_timestamp(minutes: int) -> int:
    return int((_now_utc() + timedelta(minutes=minutes)).timestamp())

def create_access_token(data: Dict[str, Any], expires_minutes: Optional[int] = None) -> str:
    """
    Create a signed JWT token containing `data` and an expiry (exp as unix timestamp).
    `data` should NOT already contain an 'exp' claim (this function sets it).
    """
    to_encode = data.copy()
    minutes = expires_minutes if expires_minutes is not None else ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode.update({"exp": _expiry_timestamp(minutes)})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token. Returns payload dict on success.
    Raises HTTPException with 401 on failure for FastAPI compatibility.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_subject_from_token(token: str) -> str:
    """
    Extracts 'sub' or falls back to 'username' or 'user_id' (as string) from payload.
    Raises HTTPException if missing or token invalid.
    """
    payload = verify_access_token(token)
    sub = payload.get("sub") or payload.get("username") or payload.get("user_id")
    if sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token payload missing subject")
    return str(sub)

# Convenience: create token for a user (adds standard 'sub' claim)
def create_user_token(user_id: int, username: str, role: str = "user", expires_minutes: Optional[int] = None) -> str:
    payload = {"sub": username, "user_id": user_id, "username": username, "role": role}
    return create_access_token(payload, expires_minutes=expires_minutes)
