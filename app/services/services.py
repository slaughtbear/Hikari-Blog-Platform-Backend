from typing import Any # Tipado de Python

from bson import ObjectId # Objeto ID de MongoDB
from bson.errors import InvalidId # Excepciones de BSON
from fastapi import UploadFile # Clase para subir archivos
from pymongo.errors import DuplicateKeyError # Excepciones de MongoDB
from pymongo.asynchronous.collection import AsyncCollection # Colección asíncrona en Mongo

from app.db.database import bucket # Almacenamiento de archivos en MongoDB
from app.utils.constants import CHUNK_SIZE_BYTES # Constantes


async def create_document(collection: AsyncCollection, data: dict) -> dict[str, Any]:
    '''
    Inserta un nuevo documento en la base de datos.

    Args:
        collection (AsyncCollection): Colección asíncrona en MongoDB.
        data (dict): Diccionario con los datos a insertar en la base de datos.

    Returns:
        dict (str, Any): Documento insertado en la base de datos.
    '''
    try:
        document = await collection.insert_one(data)
        return await collection.find_one({"_id": document.inserted_id})

    except DuplicateKeyError:
        raise


async def read_documents(collection: AsyncCollection) -> list[dict]:
    '''
    Recupera y devuelve todos los documentos que se encuentran
    en una colección en MongoDB.

    Args:
        collection (AsyncCollection): Colección asíncrona en MongoDB.

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
    try:
        data = {k: v for k, v in data.items() if v is not None}
        result = await collection.update_one({"_id": ObjectId(id)}, {"$set": data})

        if result.matched_count == 0:
            return None
        
        return await search_document(collection=collection, field="_id", key=ObjectId(id))
    
    except InvalidId:
        raise 


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
    try:
        result = await collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count == 1
    
    except InvalidId:
        raise


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
    
    except InvalidId:
        raise


async def process_file(file: UploadFile) -> ObjectId | bool:
    """
    Procesa y almacena un archivo subido en MongoDB utilizando 
    la especificación GridFS de manera asíncrona.
    
    Args:
        file (UploadFile): Archivo que será procesado y subido.

    Returns:
        grid_in._id (ObjectId): Identificador único (ID) del archivo.
        False: Si la operación no es éxitosa.
    """
    try:
        # 1. Abrir stream de carga: preparación para recibir el archivo
        async with bucket.open_upload_stream(
            file.filename, # Nombre del archivo
            chunk_size_bytes = CHUNK_SIZE_BYTES, # Tamaño de fragmentos a dividir
            metadata = {
                "contentType": file.content_type,
            }
        ) as grid_in: # 2. Transferencia de datos
            while content := await file.read(CHUNK_SIZE_BYTES): # Lectura por fragmentos
                await grid_in.write(content) # Escritura en GridFS mientras se lee el archivo

        return grid_in._id # Identificador único (ID) del archivo

    except Exception as e:
        print(f"Error al subir archivo a GridFS...\n{e}")
        return False
    
    finally:
        await file.close() # Cerrar archivo subido