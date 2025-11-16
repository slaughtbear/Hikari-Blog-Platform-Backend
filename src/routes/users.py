from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from src.authentication.authentication import is_admin
from src.authentication.security import hash_password

from src.models.users import User, UserCreate, UserUpdate

from src.schemas.users import user_schema

from src.database.database import users
from src.database.queries import (
    create_document,
    read_documents,
    update_document,
    delete_document,
    search_document,
)


router = APIRouter()


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = User)
async def create_user(data: UserCreate, current_user: is_admin) -> User:
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
        response = await create_document(users, {
            "username": data.username,
            "full_name": data.full_name,
            "email": data.email,
            "role": "reader" if not data.role else data.role,
            "disabled": False,
            "password": hash_password(data.password)
        })

        return user_schema(response)
    
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
    return [user_schema(document) for document in await read_documents(users)]


@router.get("/{id}", response_model = User)
async def search_user(id: str, current_user: is_admin) -> User:
    """
    Búsca un usuario por la clave id.
    Args:
        id (str): ID de usuario.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.
    Returns:
        User: Información del usuario búscado.
    """
    response = await search_document(users, field="_id", key=ObjectId(id))

    if not response:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Usuario no encontrado..."
        )
    
    return user_schema(response)


@router.patch("/{id}", response_model = User)
async def update_user(id: str, data: UserUpdate, current_user: is_admin) -> User:
    """
    Actualiza información de un usuario.
    Args:
        id (str): ID del usuario.
        data (UserUpdate): Datos a actualizar.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.
    Returns:
        User: Documento con la información del usuario actualizada.
    """
    response = await update_document(users, id, data.model_dump())

    if not response:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No se encontro un usuario para actualizar..."
        )
    
    return user_schema(response)


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(id: str, current_user: is_admin):
    """
    Elimina a un usuario de la aplicación.

    Args:
        id (str): ID del usuario.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.
    """
    result = await delete_document(users, id)

    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No se encontro un usuario para eliminar..."
        )