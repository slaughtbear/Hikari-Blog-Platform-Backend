from datetime import datetime # Librería para trabajar con fechas y horas

from fastapi import APIRouter, HTTPException, Depends, status # FastAPI

from src.models.users import User # Modelo de usuario
from src.models.tags import Tag, TagUpdate, TagCreate # Modelos de etiquetas

from src.authentication.jwt_auth import get_current_user, is_admin # Dependencia validadora del rol admin

from src.database.queries.tags_queries import * # Operaciones a la base de datos

from src.schemas.tags import tag_schema # Serializador de datos


router = APIRouter()


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = Tag)
async def create_tag(data: TagCreate, current_user: is_admin) -> Tag:
    '''
    Crea y registra una nueva etiqueta.

    Args:
        data (TagCreate): Datos para crear la etiqueta nueva.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        Tag: Etiqueta creada.
    '''
    try:
        response = await add_tag({
            "name": data.name, # Nombre
            "slug": data.name.lower().replace(" ", "-"), # Slug
            "created_by": current_user.username, # Creado por
            "updated_by": None, # Actualizado por 
            "created_at": datetime.now(), # Fecha de creación
            "updated_at": None # Fecha de actualización por defecto
        })

        return tag_schema(response)
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.get("/", response_model = list[Tag])
async def read_tags(current_user: User = Depends(get_current_user)) -> list[Tag]:
    '''
    Retorna todas las etiquetas almacenadas en la base de datos.

    Args:
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        list (Tag): Lista de etiquetas.
    '''
    try:
        return [tag_schema(document) for document in await get_tags()]
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.get("/{id}", response_model = Tag)
async def search_tag(id: str, current_user: User = Depends(get_current_user)) -> Tag:
    '''
    Busca una etiqueta en la base de datos por su ID.

    Args:
        id (str): Id de la etiqueta a buscar.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        Tag: Etiqueta buscada.
    '''
    try:
        response = await get_tag(field="_id", key=id)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró la etiqueta..."
            )
        
        return tag_schema(response)
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.patch("/{id}", response_model = Tag)
async def update_tag(id: str, data: TagUpdate, current_user: is_admin) -> Tag:
    """
    Actualiza información de una etiqueta.

    Args:
        id (str): ID de la etiqueta.
        data (TagUpdate): Datos a actualizar.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        User: Etiqueta actualizada.
    """
    try:
        response = await patch_tag(id, {
            "name": data.name,
            "slug": data.name.lower().replace(" ", "-"),
            "updated_by": current_user.username,
            "updated_at": datetime.now()
        })

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró la etiqueta..."
            )
        
        return tag_schema(response)
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_tag(id: str, current_user: is_admin) -> None:
    """
    Elimina una etiqueta de la app.

    Args:
        id (str): ID de la etiqueta.
        current_user (is_admin): Dependencia para validar el rol de admin.
    """
    response = await del_tag(id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro una etiqueta para eliminar..."
        )