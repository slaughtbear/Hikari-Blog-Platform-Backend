from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.authentication.authentication import authenticate_user, create_access_token
from src.authentication.security import hash_password

from src.database.database import users
from src.database.queries import create_document

from src.models.users import User, UserSignUp
from src.models.tokens import Token

from src.schemas.users import user_schema


router = APIRouter()


@router.post("/signin", response_model = Token)
async def signin(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """
    Endpoint para el inicio de sesión de usuarios.

    Recibe el nombre de usuario y la contraseña a través del formulario 
    estándar de OAuth2 (OAuth2PasswordRequestForm). Si las credenciales 
    son válidas, genera un token de acceso JWT y lo retorna.

    Args:
        form_data: Objeto OAuth2PasswordRequestForm inyectado por dependencia 
                   que contiene los campos username y password del usuario.

    Returns:
        dict (str, str): Token de acceso.
    """
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrecta..."
        )
    
    access_token = create_access_token(data={"sub": user["username"]})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/signup", status_code = status.HTTP_201_CREATED, response_model = User)
async def signup(data: UserSignUp) -> User:
    """
    Endpoint para el registro de nuevos usuarios en el sistema.

    Recibe los datos del nuevo usuario a través del modelo UserSignUp. 
    La contraseña se hashea antes de almacenarse en la base de datos. 
    Por defecto, el nuevo usuario se registra con el rol de reader.

    Args:
        data (UserSignUp): Objeto UserSignUp que contiene los 
              datos de registro.

    Returns:
        User: El objeto de usuario recién creado.
    """
    response = await create_document(users, {
        "username": data.username,
        "full_name": data.full_name,
        "email": data.email,
        "role": "reader",
        "disabled": False,
        "password": hash_password(data.password)
    })

    return user_schema(response)