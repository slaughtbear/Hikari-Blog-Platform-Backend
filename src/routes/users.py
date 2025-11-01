from fastapi import APIRouter, HTTPException, status

from src.authentication.jwt_auth import is_admin
from src.database.queries.users import *
from src.models.users import User, UserUpdate
from src.schemas.users import user_schema

router = APIRouter()

@router.get("/")
async def read_users(current_user: is_admin) -> list[User]:
    """
    Retorna la lista de usuarios en la app.
    Args:
        current_user (is_admin): Dependencia para validar el rol de admin.
    Returns:
        list (User): Lista de usuarios.
    """
    return await get_users()


@router.get("/{username}")
async def search_user(username: str, current_user: is_admin) -> User:
    """
    Búsca un usuario por la clave username.
    Args:
        username (str): Nombre de usuario.
        current_user (is_admin): Dependencia para validar el rol de admin.
    Returns:
        User: Información del usuario búscado.
    """
    response = await get_user(field="username", key=username)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_schema(response)


@router.patch("/{id}")
async def update_user(id: str, user_data: UserUpdate, current_user: is_admin) -> User:
    """
    Actualiza información de un usuario.
    Args:
        id (str): ID del usuario.
        user_data (UserUpdate): Datos a actualizar.
        current_user (is_admin): Dependencia para validar el rol de admin.
    Returns:
        User: Documento con la información del usuario actualizada.
    """
    response = await patch_user(id, user_data.model_dump())
    if not response:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user_schema(response)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str, current_user: is_admin):
    """
    Elimina a un usuario de la aplicación.
    Args:
        id (str): ID del usuario.
        current_user (is_admin): Dependencia para validar el rol de admin.
    """
    result = await del_user(id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )