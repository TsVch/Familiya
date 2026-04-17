from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
import hashlib


SECRET_KEY = "change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# 🔐 Хеширование пароля (SHA256 для MVP)
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


# 🔐 Проверка пароля
def verify_password(plain_password: str, password_hash: str) -> bool:
    return hashlib.sha256(plain_password.encode()).hexdigest() == password_hash


# 🔑 Создание JWT токена
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 🔍 Декодирование токена
def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None