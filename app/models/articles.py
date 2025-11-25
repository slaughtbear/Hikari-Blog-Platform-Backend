from pydantic import BaseModel, Field
from app.models.tags import Tag
from app.models.categories import Category

class Article(BaseModel):
    id: str
    title: str
    slug: str
    user_id: str
    content: str
    tags: list[Tag]
    categories: list[Category]
    comments: list # TODO: Crear modelo Comment
    status: str
    created_at: str
    updated_at: str | None = None