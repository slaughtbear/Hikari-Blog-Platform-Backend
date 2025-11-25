from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, Depends, status
from pymongo.errors import DuplicateKeyError

from app.authentication.tokens import get_current_user, is_admin

from app.db.database import categories

from app.models.categories import Category, CategoryCreate, CategoryUpdate
from app.models.users import User

from app.schemas.categories import category_schema

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


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = Category)
async def create_category(category: CategoryCreate, current_user: is_admin) -> Category:
    '''
    Crea y registra una nueva categoría.

    Args:
        category (CategoryCreate): Datos para crear la nueva categoría.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        Category: Categoría creada.
    '''
    try:
        response = await create_document(
            collection = categories,
            data = {
            "name": category.name,
            "slug": slugify(category.name),
            "description": category.description,
            "status": category.status,
            "created_at": CURRENT_DATE,
            "updated_at": None
        })

        return category_schema(response)
    
    except DuplicateKeyError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"El nombre de la etiqueta {category.name} ya está en uso."
        )
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.get("/", response_model = list[Category])
async def read_categories(current_user: User = Depends(get_current_user)) -> list[Category]:
    '''
    Retorna todas las categorías almacenadas en la base de datos.

    Args:
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        list (Category): Lista de categorías.
    '''
    try:
        return [category_schema(document) for document in await read_documents(categories)]
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.get("/{category_id}", response_model = Category)
async def search_category(category_id: str, current_user: User = Depends(get_current_user)) -> Category:
    '''
    Busca una categoría en la base de datos por su ID.

    Args:
        id (str): Id de la categoría a buscar.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        Category: Categoría buscada.
    '''
    try:
        response = await search_document(
            collection = categories,
            field = "_id",
            key = ObjectId(category_id)
        )

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró la categoría..."
            )
    
        return category_schema(response)
    
    except InvalidId:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "El ID enviado no corresponde a un objeto válido en MongoDB"
        )
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )
    

@router.patch("/{category_id}", response_model = Category)
async def update_category(
    category_id: str,
    category: CategoryUpdate,
    current_user: is_admin
) -> Category:
    """
    Actualiza información de una categoría.

    Args:
        category_id (str): Identificador único de la categoría.
        category (CategoryUpdate): Datos para actualizar una categoría.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.

    Returns:
        User: Categoría actualizada.
    """
    try:
        response = await update_document(
            collection = categories,
            id = category_id,
            data = {
            "name": category.name,
            "slug": slugify(category.name) if category.name else None,
            "status": category.status,
            "description": category.description,
            "updated_at": CURRENT_DATE
        })

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró la categoría..."
            )
        
        return category_schema(response)
    
    except InvalidId:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "El ID enviado no corresponde a un objeto válido en MongoDB"
        )
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )


@router.delete("/{category_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str, current_user: is_admin) -> None:
    """
    Elimina una categoría de la aplicación.

    Args:
        id (str): Identificador único de la categoría.
        current_user (User): Dependencia de FastAPI para validar que un usuario
                             autenticado está realizando la solicitud.
    """
    try:
        response = await delete_document(
            collection = categories,
            id = category_id
        )

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontro una categoría para eliminar..."
            )
    
    except InvalidId:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "El ID enviado no corresponde a un objeto válido en MongoDB"
        )
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor, inténtelo más tarde..."
        )