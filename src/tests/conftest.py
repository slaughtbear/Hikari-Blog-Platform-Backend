import os # Manipulación de archivos
import pytest # Líbreria para pruebas unitarias
from dotenv import load_dotenv # Interacción con variables de entorno

load_dotenv()

@pytest.fixture(scope="session")
def mongo_uri() -> str:
    """Proporciona la cadena de conexión de MongoDB."""
    return os.getenv("MONGO_URI")