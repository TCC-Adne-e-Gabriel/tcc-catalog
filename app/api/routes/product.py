from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status
from ...deps import SessionDep
from typing import List
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest, ProductResponse, CategoryCreateRequest, CategoryResponse, CategoryAsociation
from app.services.product import ProductService
from app.services.category import CategoryService
from app.deps import SessionDep
from uuid import UUID
from app.schemas.product import Message


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

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    session: SessionDep, 
    product: ProductCreateRequest
): 
    product_sku = product_service.get_product_by_sku(session=session, sku=product.sku)
    if(product_sku): 
        raise HTTPException(
            status_code=400, 
            detail="Product with this sku already exists in the system"
        )
    product = product_service.create_product(session=session, product=product)
    return product


@router.post("/category", response_model=CategoryResponse, status_code=201)
def create_category(
    session: SessionDep, 
    category: CategoryCreateRequest
): 
    category_name = product_service.get_category_by_name(session=session, name=category.name)
    if(category_name): 
        raise HTTPException(
            status_code=400, 
            detail="category with this name already exists in the system"
        )
    category = product_service.create_category(session=session, category=category)
    return category

@router.get("/", response_model=List[ProductResponse])
def read_products(
    session: SessionDep, 
    skip: int = 0, 
    limit: int = 100
) : 
    product = product_service.get_products(session=session)
    return product

@router.get("/category", response_model=List[CategoryResponse])
def read_categories(
    session: SessionDep, 
    skip: int = 0, 
    limit: int = 100
) : 
    categories = product_service.get_categories(session=session)
    print(categories)
    return categories

@router.post('')
def associate_category(
    session: SessionDep, 
    body: CategoryAsociation
):
    product = product_service.get_product_by_id()
    if(not product):
        raise HTTPException(
            status_code=400, 
            detail="There is no product with this ID"
        )
    category = category_service.get_category_by_id()
    if(not category):
        raise HTTPException(
            status_code=400, 
            detail="There is no category with this ID"
        )
    
    if(category in product.category): 
        raise HTTPException(
            status_code=400, 
            detail="Category is already associated to this product"
        )
    return product_service.associate_category(session, product, category)