import pytest # Líbreria para pruebas unitarias
from pymongo import AsyncMongoClient # Clase para crear un objeto de cliente
from pymongo.errors import (
    ConnectionFailure, # Servidor apagado, host/puerto incorrecto.
    OperationFailure # Autenticación (usuario/contraseña incorrectos).
) 

@pytest.mark.asyncio
async def test_connection_success(mongo_uri: str):
    '''
    Verifica si la aplicación puede conectarse correctamente
    al servidor de MongoDB.

    Ejecuta un comando "ping", si es éxitoso la prueba pasa.

    Args:
        mongo_uri (str): Cadena de conexión de MongoDB.
    '''
    client = None

    try:
        client = AsyncMongoClient(mongo_uri)
        await client.admin.command('ping')

    except (ConnectionFailure, OperationFailure) as e:
        pytest.fail(f"Error en la conexión: {e}") # Prueba fallida

    finally: 
        if client:
            await client.close() # Cierre de conexión