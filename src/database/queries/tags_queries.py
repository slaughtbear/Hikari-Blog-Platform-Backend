from typing import Any # Tipado de Python
from bson import ObjectId # Objeto ID de MongoDB
from src.database.database import db # Base de datos


tags_collection = db.Tags # Colección en la base de datos


async def add_tag(tag_data: dict) -> dict[str, Any]:
    '''
    Inserta un nuevo documento de etiqueta en la colección "Tags".

    Args:
        tag_data (dict): Diccionario con los datos de la etiqueta a insertar.

    Returns:
        dict (str, Any): Documento insertado.
    '''
    new_tag = await tags_collection.insert_one(tag_data)

    return await tags_collection.find_one({"_id": new_tag.inserted_id})


async def get_tags() -> list[dict]:
    '''
    Obtiene todos los documentos de etiqueta de la base de datos.

    Returns:
        list[dict]: Una lista de documentos de etiqueta.
    '''
    tags_documents = [] # lista para almacenar documentos
    cursor = tags_collection.find({}) # se obtienen los documentos

    async for document in cursor: # iteración sobre cada documento
        tags_documents.append(document) # se agrega a la lista

    return tags_documents


async def get_tag(field: str, key: Any) -> dict | None:
    '''
    Busca un único documento de etiqueta en la base de datos por un campo y valor.

    Args:
        field (str): Nombre del campo de MongoDB a buscar (ej. "_id", "name").
        key (Any): El valor a buscar en el campo especificado.

    Returns:
        dict | None: El documento de etiqueta encontrado o None si no se encuentra.
    '''
    return await tags_collection.find_one({field: key})


async def patch_tag(id: str, tag_data: dict) -> dict[str, Any] | None:
    '''
    Actualiza un documento de etiqueta existente en la base de datos por su ID.

    Solo se actualizan los campos presentes en "tag_data" cuyo valor NO sea None.
    Recupera y retorna el documento después de la actualización.

    Args:
        id (str): El ID de la etiqueta a actualizar, como cadena de texto.
        tag_data (dict): Los campos y valores a modificar (solo se usan los != None).

    Returns:
        dict[str, Any] | None: El documento de etiqueta actualizado,
                               o None si no se encontró la etiqueta con el ID dado.
    '''
    data = {k: v for k, v in tag_data.items() if v is not None}
    result = await tags_collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    if result.matched_count == 0:
        return None
    
    return await get_tag(field="_id", key=ObjectId(id))


async def del_tag(id: str) -> bool:
    '''
    Elimina un documento de etiqueta de la base de datos por su "_id".

    Args:
        id (str): El ID de la etiqueta a eliminar, como cadena de texto.

    Returns:
        bool: True si se eliminó exactamente un documento (eliminación exitosa),
              False en caso contrario.
    '''
    result = await tags_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count == 1