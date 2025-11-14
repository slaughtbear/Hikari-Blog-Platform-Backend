from pydantic import BaseModel, Field

class Tag(BaseModel):
    id: str
    name: str
    slug: str
    created_by: str
    updated_by: str | None = None
    created_at: str
    updated_at: str | None = None

class TagCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=32)

class TagUpdate(BaseModel):
    name: str | None = Field(min_length=3, max_length=32)