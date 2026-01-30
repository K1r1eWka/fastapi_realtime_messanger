from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from backend.core.config import security_settings

# context to hasing password and verify them 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
# plain_password - обычный пароль(незахешированный)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# create jwt token using sicret, and algorithm
def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=security_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, security_settings.JWT_SECRET, algorithm=security_settings.JWT_ALGORITHM)
    return encoded_jwt
