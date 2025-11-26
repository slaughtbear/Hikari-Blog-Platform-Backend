import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
import sys


def setup_logging(logger_name: str = "hikari-logger", logger_level: int = logging.DEBUG) -> Logger:
    """
    Configura y devuelve un logger con handlers para consola y archivo.
    """
    logger = logging.getLogger(logger_name) # Instanciamiento del logger
    logger.setLevel(logger_level) # Nivel de logs

    # Formateo
    formatter = logging.Formatter(
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", # Datos
        datefmt = "%Y-%m-%d %H:%M:%S" # Formato
    )

    if not logger.handlers: # Prevención de handlers duplicados
        # Handler de Stream (envío de logs a consola)
        stream_handler = logging.StreamHandler(sys.stdout) # Creación del handler
        stream_handler.setFormatter(formatter) # Agregar formateador al handler
        stream_handler.setLevel(logging.INFO) # Definir nivel de logs para la consola
        logger.addHandler(stream_handler) # Agregar handler al logger

        # Handler de Files (envío de logs a archivos)
        file_handler = RotatingFileHandler( # Creación del handler
                "logs/app_activity.log", # Nombre del archivo
                maxBytes = 10 * 1024 * 1024, # Tamaño máximo (10MB)
                backupCount = 5, # Número máximo de archivos para rotación
                encoding = 'utf-8' # Codificación
            )

        file_handler.setFormatter(formatter) # Agregar formateador al handler
        logger.addHandler(file_handler) # Agregar handler al logger

    return logger