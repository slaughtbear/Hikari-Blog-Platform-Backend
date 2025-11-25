from .users import router as users_router
from .authentication import router as auth_router
from .tags import router as tags_router
from .categories import router as categories_router

__all__ = [
    "users_router",
    "auth_router",
    "tags_router",
    "categories_router"
]