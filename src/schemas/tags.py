def tag_schema(data: dict) -> dict:
    """
    Serializa los datos para enviarlos al cliente.

    Parámetros:
    - data(dict): Datos de la etiqueta.

    Retorna:
    - dict: Diccionario con los datos serializados.
    """
    return {
        "id": str(data["_id"]),
        "name": data["name"],
        "slug": data["slug"],
        "created_by": data["created_by"],
        "updated_by": data["updated_by"],
        "created_at": str(data["created_at"]),
        "updated_at": str(data["updated_at"]) if data["updated_at"] else None
    }