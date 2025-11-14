from pymongo import AsyncMongoClient # Clase para crear un objeto de cliente
from src.config import settings # Configuración global

client = AsyncMongoClient(settings.MONGO_ATLAS) # Cliente de conexión

db = client["Hikari"] # Base de datos para Producción