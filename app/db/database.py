from pymongo import AsyncMongoClient # Clase para crear un objeto de cliente
from app.core.config import settings # Configuración global
from gridfs import AsyncGridFSBucket

client = AsyncMongoClient(settings.MONGO_URI) # Cliente de conexión
db = client["Hikari"] # Base de datos
bucket = AsyncGridFSBucket(db) # Contenedor para almacenar archivos grandes

# Colecciones
users = db.Users
tags = db.Tags
categories = db.Categories