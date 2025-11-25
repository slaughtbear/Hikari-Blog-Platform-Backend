def slugify(text: str) -> str:
    """
    Genera una cadena de texto más amigable para una URL,
    generada a partir del título.
    Funciona como índice único para búsquedas rápidas.

    Args:
        text (str): Texto a convertir en slug.

    Returns:
        str: Texto convertido a slug.
    """
    return text.lower().replace(" ", "-")
