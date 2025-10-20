from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.models.users import User, UserCreate
from src.authentication.jwt_auth import authenticate_user, create_access_token
from src.authentication.security import hash_password
from src.database.queries.users import add_user
from src.schemas.users import user_schema
from src.models.tokens import Token

router = APIRouter()

@router.post("/signin", response_model=Token)
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": user["username"]})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=User)
async def signup(user_data: UserCreate) -> User:
    user_data.password = hash_password(user_data.password)
    response = await add_user(user_data.model_dump())
    return user_schema(response)