from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.product import ProductResponse
from app.services.product import ProductService
from app.services.category import CategoryService
from app.deps import SessionDep
from uuid import UUID


app = FastAPI()
router = APIRouter(prefix="/product")
product_service = ProductService()
category_service = CategoryService()


@router.get("/{id}", response_model=ProductResponse)
def read_product_by_id(
    id: UUID, 
    session: SessionDep, 
    skip: int = 0, 
    limit: int = 100
) : 
    product = product_service.get_product(session=session, product_id=id)
    if(not product): 
        raise HTTPException(
            status_code=400, 
            detail="Product with this id doesnt exist"
        )
    return product


@router.get("/", response_model=List[ProductResponse])
def read_products(
    session: SessionDep, 
    skip: int = 0, 
    limit: int = 100
) : 
    product = product_service.get_products(session=session)
    return product
