from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.product import ProductResponse
from app.services.product import ProductService
from app.services.category import CategoryService
from app.deps import SessionDep
from http import HTTPStatus
from uuid import UUID
from app.exceptions import (
    ProductNotFoundException
)


app = FastAPI()
router = APIRouter(prefix="/product")
product_service = ProductService()
category_service = CategoryService()


@router.get("/{id}/", response_model=ProductResponse)
def read_product_by_id(
    id: UUID, 
    session: SessionDep
) : 
    try:
        product = product_service.get_product(session=session, product_id=id)
        return product
    except ProductNotFoundException: 
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Product not found"
        )
    except Exception: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )
    
@router.get("/", response_model=List[ProductResponse])
def read_products(
    session: SessionDep
) : 
    try:
        product = product_service.get_products(session=session)
        return product
    except Exception: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )