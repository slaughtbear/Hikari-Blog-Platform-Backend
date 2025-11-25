from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

from app.authentication.security import verify_password
from app.db.database import users
from app.core.config import settings
from app.models.users import User
from app.schemas.users import user_schema
from app.services.services import search_document


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/api/v1/auth/signin")


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Crea un token de acceso JWT (JSON Web Token).

    El token se codifica con los datos proporcionados y una marca de tiempo 
    de expiración.

    Args:
        data (dict): Los datos que se incluirán en el payload del token. .
        expires_delta (timedelta): Objeto opcional que define la duración 
                       antes de que el token expire. Si es None, el token 
                       expirará en 15 minutos por defecto.

    Returns:
        str: El token de acceso codificado.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """
    Decodifica y valida un token de acceso JWT.

    Verifica la firma, si la decodificación falla (por token inválido, expirado, etc.), 
    lanza una excepción HTTPException 401.

    Args:
        token: La cadena de texto del token de acceso JWT a decodificar.

    Returns:
        dict: El payload del token decodificado como un diccionario, 
              si la validación es exitosa.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "El token es inválido o ha expirado..."
        )


async def authenticate_user(username: str, password: str) -> dict[str, Any] | None:
    """
    Intenta autenticar a un usuario buscando su nombre de usuario 
    y verificando la contraseña proporcionada.

    Args:
        username (string): El nombre de usuario con el que se intenta iniciar sesión.
        password (string): La contraseña proporcionada por el usuario.

    Returns:
        dict (str, Any): El diccionario con los datos del usuario, 
                      si la autenticación es exitosa. Retorna None si el usuario 
        None: Si no se encuentra el usuario o la contraseña no es válida.
    """
    user = await search_document(users, field="username", key=username)
    if not user or not verify_password(password, user["password"]):
        return None
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Obtiene el usuario actual a partir del token JWT proporcionado 
    en el encabezado de la solicitud (Header 'Authorization: Bearer <token>').

    Esta función actúa como una dependencia que:
    1. Extrae el token usando el esquema OAuth2.
    2. Decodifica el token para obtener el 'subject' (nombre de usuario).
    3. Busca el documento del usuario en la base de datos.
    4. Retorna los datos del usuario si todo es válido.

    Args:
        token (str): La cadena de texto del token JWT, inyectada automáticamente 
               por la dependencia 'oauth2_scheme' de FastAPI.

    Returns:
        User: Datos del usuario correspondiente al token.
    """
    payload = decode_token(token)
    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas. Inténtalo de nuevo"
        )
    
    user_data = await search_document(users, field="username", key=username)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado..."
        )
    
    return User(**user_schema(user_data))


def check_admin(user: User = Depends(get_current_user)):
    """
    Verifica que el usuario autenticado actual tenga el rol de admin.

    Esta función se utiliza como una dependencia de ruta en endpoints 
    que solo deben ser accesibles por administradores. Primero, obtiene 
    el objeto User a través de la dependencia get_current_user. 
    Luego, comprueba el atributo role.

    Args:
        user (User): El objeto de usuario inyectado 
              automáticamente por la dependencia get_current_user.

    Returns:
        User: Datos del usuario si el rol es admin.
    """
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes suficientes permisos..."
        )
    
    return user

# Dependencias
is_admin = Annotated[User, Depends(check_admin)] 