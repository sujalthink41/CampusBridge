from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from campus_bridge.config.settings.app import app_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = app_settings.ALGORITHM
SECRET_KEY = app_settings.SECRET_KEY
EXPIRES_MINUTES = app_settings.EXPIRES_MINUTES
APP_NAME = app_settings.APP_NAME

def hash_password(password: str) -> str:
    """Hashing password"""
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify the actual password with the hashed password"""
    return pwd_context.verify(password, hashed_password)

def create_access_token(
    subject: str,
    role: str,
    college_id: str,
) -> str:
    """Creating access token for the verification"""
    expire = datetime.utcnow() + timedelta(minutes=EXPIRES_MINUTES)
    payload = {
        "sub": subject, 
        "exp": expire, 
        "role": role,
        "college_id": college_id,
        "iat": datetime.utcnow(),
        "iss": APP_NAME,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
