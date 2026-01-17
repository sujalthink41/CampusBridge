from datetime import datetime
from jose import jwt
from passlib.context import CryptContext

from campus_bridge.config.settings.app import app_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = app_settings.ALGORITHM

def hash_password(password: str) -> str:
    """Hashing password"""
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify the actual password with the hashed password"""
    return pwd_context.verify(password, hashed_password)

def create_access_token(
    subject: str,
    secret_key: str,
    expires_minutes: int,
) -> str:
    """Creating access token for the verification"""
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, secret_key, algorithm=ALGORITHM)