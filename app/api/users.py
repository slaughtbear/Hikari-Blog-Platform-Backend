from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.authentication.tokens import is_admin
from app.authentication.security import hash_password

from app.db.database import users

from app.models.users import User, UserCreate, UserUpdate

from app.schemas.users import user_schema

from app.services.services import (
    create_document,
    read_documents,
    update_document,
    delete_document,
    search_document,
)


router = APIRouter()


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = User)
async def create_user(user_data: UserCreate, current_user: is_admin) -> User:
    '''
    Crea y registra un nuevo usuario.

    Args:
        data (UserCreate): Datos para crear el usuario.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        User: Usuario creado.
    '''
    try:    
        response = await create_document(
            collection = users,
            data = {
                "username": user_data.username,
                "full_name": user_data.full_name,
                "email": user_data.email,
                "role": "reader" if not user_data.role else user_data.role,
                "disabled": False,
                "password": hash_password(user_data.password)
            }
        )

        return user_schema(response)
    
    except DuplicateKeyError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "El nombre de usuario o correo electrónico ya están en uso."
        )
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.get("/", response_model = list[User])
async def read_users(current_user: is_admin) -> list[User]:
    """
    Retorna la lista de usuarios en la app.

    Args:
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.
    Returns:
        list (User): Lista de usuarios.
    """
    try:
        return [user_schema(document) for document in await read_documents(users)]
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.get("/{user_id}", response_model = User)
async def search_user(user_id: str, current_user: is_admin) -> User:
    """
    Búsca un usuario por la clave user_id.
    Args:
        user_id (str): ID de usuario.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.
    Returns:
        User: Información del usuario búscado.
    """
    try:
        response = await search_document(users, field="_id", key=ObjectId(user_id))

        if not response:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Usuario no encontrado..."
            )
        
        return user_schema(response)
    
    except InvalidId:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "El ID enviado no corresponde a un objeto válido en MongoDB"
        )
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.patch("/{user_id}", response_model = User)
async def update_user(user_id: str, user_data: UserUpdate, current_user: is_admin) -> User:
    """
    Actualiza información de un usuario.

    Args:
        user_id (str): ID del usuario.
        user_data (UserUpdate): Datos a actualizar.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        User: Documento con la información del usuario actualizada.
    """
    try:
        response = await update_document(
            collection = users,
            id = user_id,
            data = user_data.model_dump()
        )

        if not response:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "No se encontro un usuario para actualizar..."
            )
        
        return user_schema(response)
    
    except InvalidId:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "El ID enviado no corresponde a un objeto válido en MongoDB"
        )
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(id: str, current_user: is_admin):
    """
    Elimina a un usuario de la aplicación.

    Args:
        id (str): ID del usuario.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.
    """
    try:
        result = await delete_document(users, id)

        if not result:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "No se encontro un usuario para eliminar..."
            )
    
    except InvalidId:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "El ID enviado no corresponde a un objeto válido en MongoDB"
        )    

    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )