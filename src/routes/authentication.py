from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from src.models.users import User, UserSignUp
from src.models.tokens import Token
from src.schemas.users import user_schema

from src.authentication.jwt_auth import authenticate_user, create_access_token
from src.authentication.security import hash_password

from src.database.queries.users import add_user


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


@router.post("/signup", response_model=User)
async def signup(user_data: UserSignUp) -> JSONResponse:
    """Endpoint para registrar a un usuario.
    Args:
        user_data (UserSignUp): Datos necesarios para el registro.
    Returns:
        JSONResponse: Respuesta JSON personalizada.
    """
    # Hashing de contraseña
    user_data.password = hash_password(user_data.password)

    # Datos por defecto
    user_dict = user_data.model_dump() # copia de datos en diccionario
    user_dict["role"] = "commenter" # rol de usuario
    user_dict["disabled"] = False # cuenta activa

    # Operación de creación del usuario en la base de datos
    response = await add_user(user_dict)

    return JSONResponse(
        content={
            "status": "success",
            "message": f"{response["username"]} registrado correctamente"
        },
        status_code=status.HTTP_201_CREATED
    )