from pymongo import AsyncMongoClient
from src.config import settings

client = AsyncMongoClient(settings.MONGO_URI) # Cliente de conexión
database = client["HikariBlog"] # Nombre de la base de datos

async def test_connection():
    """Prueba la conexión con la base de datos."""
    try:
        await client.admin.command('ping')
        print("Conexión exitosa a MongoDB.")
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection()) # python -m src.database.connection