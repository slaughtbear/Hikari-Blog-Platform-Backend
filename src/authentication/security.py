import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt) 
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

if __name__ == "__main__":
    # Contraseña original
    password = "MiContraseñaSegura123"

    # Generar hash de la contraseña
    hashed = hash_password(password)
    print(f"Hash generado: {hashed}")

    # Verificar la contraseña
    is_valid = verify_password("MiContraseñaSegura123", hashed)
    print(f"¿La contraseña es segura?: {is_valid}")