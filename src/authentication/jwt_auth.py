from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta, timezone

from src.config import settings
from src.models.users import User
from src.authentication.security import verify_password
from src.database.queries.users import get_user
from src.schemas.users import user_schema

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

async def authenticate_user(username: str, password: str):
    user = await get_user(field="username", key=username)
    if not user or not verify_password(password, user["password"]):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Please try again"
        )
    
    user_data = await get_user(field="username", key=username)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return User(**user_schema(user_data))

def check_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions"
        )
    
    return user
    
is_admin = Annotated[User, Depends(check_admin)] # Dependencia

if __name__ == "__main__":
    user_data = {"sub": "slaughtbear"}
    token = create_access_token(user_data)
    print(f"Token generado:\n{token}\n")

    try:
        decoded = decode_token(token)
        print(f"Token decodificado:\n{decoded}\n")
    except Exception as e:
        print(str(e))