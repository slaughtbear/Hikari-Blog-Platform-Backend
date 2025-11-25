import logging
from logging.handlers import RotatingFileHandler
import sys

LOG_FILE = "app_activity.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def configure_logger(logger_name: str = 'fastapi-app', level=logging.DEBUG):
    """
    Configura y devuelve un logger con handlers para consola y archivo.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Definir el formateador
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # Si ya tiene handlers, no añadir de nuevo (evita duplicados)
    if not logger.handlers:
        # Handler para consola (salida estándar)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Handler para archivo (con rotación)
        # Rotará el archivo cuando alcance 10MB, manteniendo 5 archivos de respaldo.
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=10 * 1024 * 1024, # 10MB
            backupCount=5,
            encoding='utf-8'
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger