def category_schema(data: dict) -> dict:
    """
    Serializa los datos para enviarlos al cliente.

    Parámetros:
    - data(dict): Datos de la categoría.

    Retorna:
    - dict: Diccionario con los datos serializados.
    """
    return {
        "id": str(data["_id"]),
        "name": data["name"],
        "slug": data["slug"],
        "description": data["description"],
        "status": data["status"],
        "created_at": str(data["created_at"]),
        "updated_at": str(data["updated_at"]) if data["updated_at"] else None
    }