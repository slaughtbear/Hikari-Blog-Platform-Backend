from pydantic import BaseModel, Field
from app.utils.utils import CURRENT_DATE

class Profile(BaseModel):
    id: str
    id_user: str
    bio: str | None
    birth_date: str | None
    profile_photo_id: str | None

class ProfileCreate(BaseModel):
    bio: str | None = Field(None, max_length = 150)
    birth_date: str | None = Field(None, lt=CURRENT_DATE)
