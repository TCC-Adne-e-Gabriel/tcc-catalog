from fastapi import APIRouter

from app.api.routes import product
from app.api.routes import category
from app.core.settings import settings

api_router = APIRouter()
api_router.include_router(product.router)
api_router.include_router(category.router)

