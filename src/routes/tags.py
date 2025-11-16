from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, status

from src.authentication.authentication import get_current_user, is_admin

from src.models.users import User
from src.models.tags import Tag, TagUpdate, TagCreate

from src.schemas.tags import tag_schema

from src.database.database import tags
from src.database.queries import (
    create_document,
    read_documents,
    update_document,
    delete_document,
    search_document,
)


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
        response = await create_document(tags, {
            "name": data.name,
            "slug": data.name.lower().replace(" ", "-"),
            "created_by": current_user.username,
            "updated_by": None,
            "created_at": datetime.now(),
            "updated_at": None
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
        return [tag_schema(document) for document in await read_documents(tags)]
    
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
    response = await search_document(collection=tags, field="_id", key=ObjectId(id))

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró la etiqueta..."
        )
        
    return tag_schema(response)


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
        response = await update_document(tags, id, {
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
    
    except Exception as error:
        print(error)
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
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.
    """
    response = await delete_document(tags, id)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro una etiqueta para eliminar..."
        )