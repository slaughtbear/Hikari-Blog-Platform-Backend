from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, Depends, status
from pymongo.errors import DuplicateKeyError

from app.authentication.tokens import get_current_user, is_admin

from app.db.database import tags

from app.models.users import User
from app.models.tags import Tag, TagUpdate, TagCreate

from app.schemas.tags import tag_schema

from app.services.services import (
    create_document,
    read_documents,
    update_document,
    delete_document,
    search_document,
)

from app.utils.constants import CURRENT_DATE
from app.utils.utils import slugify


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
        response = await create_document(
            collection = tags,
            data = {
                "name": data.name,
                "slug": slugify(data.name),
                "created_at": CURRENT_DATE,
                "created_by": current_user.username,
                "updated_at": None,
                "updated_by": None
            }
        )

        return tag_schema(response)
    
    except DuplicateKeyError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"El nombre de la etiqueta {data.name} ya está en uso."
        )
    
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


@router.get("/{tag_id}", response_model = Tag)
async def search_tag(tag_id: str, current_user: User = Depends(get_current_user)) -> Tag:
    '''
    Busca una etiqueta en la base de datos por su ID.

    Args:
        tag_id (str): Id de la etiqueta a buscar.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        Tag: Etiqueta buscada.
    '''
    try:
        response = await search_document(collection=tags, field="_id", key=ObjectId(tag_id))

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró la etiqueta..."
            )
            
        return tag_schema(response)
    
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


@router.patch("/{tag_id}", response_model = Tag)
async def update_tag(tag_id: str, data: TagUpdate, current_user: is_admin) -> Tag:
    """
    Actualiza información de una etiqueta.

    Args:
        tag_id (str): ID de la etiqueta.
        data (TagUpdate): Datos a actualizar.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        User: Etiqueta actualizada.
    """
    try:
        response = await update_document(
            collection = tags,
            id = tag_id,
            data = {
                "name": data.name,
                "slug": slugify(data.name),
                "updated_by": current_user.username,
                "updated_at": CURRENT_DATE
            }
        )

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró la etiqueta..."
            )
        
        return tag_schema(response)
    
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


@router.delete("/{tag_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: str, current_user: is_admin) -> None:
    """
    Elimina una etiqueta de la app.

    Args:
        tag_id (str): ID de la etiqueta.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.
    """
    try:
        response = await delete_document(tags, tag_id)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontro una etiqueta para eliminar..."
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