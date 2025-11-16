from typing import Any # Tipado de Python
from bson import ObjectId # Objeto ID de MongoDB
from pymongo.asynchronous.collection import AsyncCollection # Colección asíncrona en Mongo


async def create_document(collection: AsyncCollection, data: dict) -> dict[str, Any]:
    '''
    Guarda un nuevo documento (registro) en la base de datos.

    Args:
        collection (AsyncCollection): Colección asíncrona en Mongo.
        data (dict): Diccionario con los datos a insertar en BD.

    Returns:
        dict (str, Any): El documento creado en la base de datos.
    '''
    document = await collection.insert_one(data)
    return await collection.find_one({"_id": document.inserted_id})


async def read_documents(collection: AsyncCollection) -> list[dict]:
    '''
    Recupera y devuelve TODOS los documentos (registros) que se encuentran
    en una colección de MongoDB.

    Args:
        collection (AsyncCollection): Colección asíncrona en Mongo.

    Returns:
        list (dict): Lista de diccionarios, donde cada diccionario representa un
        documento completo en la base de datos.
    '''
    documents = []
    cursor = collection.find({})

    async for document in cursor:
        documents.append(document) 

    return documents


async def update_document(collection: AsyncCollection, id: str, data: dict) -> dict[str, Any] | None:
    '''
    Actualiza un documento (registro) existente en la base de datos de MongoDB
    utilizando su ID único.

    Args:
        collection (AsyncCollection): Colección asíncrona en Mongo.

        id (str): ID único del documento que se desea actualizar.
        data (dict): Diccionario con los campos y sus nuevos valores a modificar.

    Returns:
        dict (str, Any): El documento completo después de haber sido actualizado.

        None: Si la función no encontró ningún documento con el 'id'
        proporcionado para actualizar.
    '''
    data = {k: v for k, v in data.items() if v is not None}
    result = await collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    if result.matched_count == 0:
        return None
    
    return await search_document(collection=collection, field="_id", key=ObjectId(id))


async def delete_document(collection: AsyncCollection, id: str) -> bool:
    '''
    Elimina un único documento (registro) de la colección de MongoDB
    utilizando su ID único.

    Args:
        collection (AsyncCollection) Colección asíncrona en Mongo.
        id (str): ID único del documento a eliminar.

    Returns:
        True: Si la eliminación fue exitosa.
        False: Si no se encontró o no se eliminó ningún documento con ese ID.
    '''
    result = await collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count == 1


async def search_document(collection: AsyncCollection, field: str, key: Any) -> dict[str, Any] | None:
    '''
    Busca y devuelve el primer documento (registro) que coincida con
    un valor específico ('key') en un campo determinado ('field') dentro
    de la colección de MongoDB.

    Args:
        collection (AsyncCollection): La tabla colección asíncrona de MongoDB donde se
                    realizará la búsqueda.
        field (str): El nombre exacto del campo en el que se buscará.
        key (Any): El valor que debe coincidir con el campo especificado.

    Returns:
        dict (str, Any): Documento encontrado.
        None: Si la función no encontró ningún documento que coincidiera
              con la búsqueda.
    '''
    try:
        response = await collection.find_one({field: key})
        return response
    
    except Exception as error:
        print(f"Ha ocurrido un error al intentar buscar el documento...\n{error}")