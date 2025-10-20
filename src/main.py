from fastapi import FastAPI
from src.routes import *

app = FastAPI(
    title="Hikari Blog Backend",
    version="1.0.0"
)

@app.get("/")
def read_root() -> dict:
    return {"message": "Welcome to Hikari Blog Backend"}

app.include_router(
    router=auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    router=users_router,
    prefix="/api/v1/users",
    tags=["Users"]
)