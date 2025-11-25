from pydantic import BaseModel, Field
from enum import Enum


class StatusOption(str, Enum):
    ACTIVE = "active"
    HIDDEN = "hidden"
    DEPRECATED = "deprecated"


class Category(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    status: str
    created_at: str
    updated_at: str | None


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length = 3, max_length = 64)
    description: str | None = Field(max_length = 150)
    status: StatusOption = Field(...)


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length = 3, max_length = 64)
    description: str | None = Field(None, max_length = 150)
    status: StatusOption | None = None
