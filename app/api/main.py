from fastapi import APIRouter

from app.api.routes.internal import product
from app.api.routes.internal import category
from app.api.routes.public import product as product_public
from app.core.settings import settings

api_router = APIRouter()
api_router.include_router(product.router)
api_router.include_router(category.router)
api_router.include_router(product_public.router)
