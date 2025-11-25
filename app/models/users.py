from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
    role: str
    disabled: bool


class UserInDB(User):
    password: str


class UserCreate(BaseModel):
    username: str = Field(..., min_length=5, max_length=15)
    full_name: str = Field(..., min_length=6, max_length=128)
    email: EmailStr = Field(..., min_length=6, max_length=254)
    role: str | None = None
    password: str = Field(...)


class UserSignUp(BaseModel):
    username: str = Field(..., min_length=5, max_length=15)
    full_name: str = Field(..., min_length=6, max_length=128)
    email: EmailStr = Field(..., min_length=6, max_length=254)
    password: str = Field(...)


class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=5, max_length=15)
    full_name: str | None = Field(None, min_length=6, max_length=128)
    email: EmailStr | None = Field(None, min_length=6, max_length=254)
    role: str | None = Field(None, min_length=6, max_length=32)
    password: str | None = None
    disabled: bool | None = None