from pymongo import AsyncMongoClient # Clase para crear un objeto de cliente
from src.config import settings # Configuración global

client = AsyncMongoClient(settings.MONGO_URI) # Cliente de conexión

db = client["Hikari"] # Base de datos

# Colecciones
users = db.Users
tags = db.Tags