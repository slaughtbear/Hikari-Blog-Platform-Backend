def user_schema(data: dict) -> dict:
    """
    Convierte el ID del usuario en MongoDB a str.

    Parámetros:
    - data(dict): Datos del usuario.

    Retorna:
    - dict: Diccionario con los datos listos para utilizar.
    """
    return {
        "id": str(data["_id"]),
        "username": data["username"],
        "full_name": data["full_name"],
        "email": data["email"],
        "role": data["role"],
        "disabled": data["disabled"]
    }