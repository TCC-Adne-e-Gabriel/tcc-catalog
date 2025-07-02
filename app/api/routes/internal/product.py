from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status
from typing import List
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest, ProductResponse, UpdateQuantityRequest
from app.schemas.category import CategoryResponse, CategoryAsociation, CategoryCreateRequest
from app.services.product import ProductService
from app.services.category import CategoryService
from app.deps import SessionDep
from http import HTTPStatus
from uuid import UUID
from app.exceptions import (
    ProductNotFoundException, 
    CategoryNotFoundException, 
    SameSkuException, 
    DuplicatedCategoryException, 
    UnlinkedCategoryException
)
from app.schemas.product import Message


app = FastAPI()
router = APIRouter(prefix="/internal/product")
product_service = ProductService()
category_service = CategoryService()


@router.get("/{id}", response_model=ProductResponse)
def read_product_by_id(
    id: UUID, 
    session: SessionDep, 
    skip: int = 0, 
    limit: int = 100
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
    

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    session: SessionDep, 
    product_request: ProductCreateRequest
): 
    try: 
        product = product_service.create_product(session=session, product=product_request)
        return product
    except SameSkuException: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="Product with this sku already exists"
        )
    except Exception: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )

@router.post('/associate-category/', response_model=ProductResponse)
def associate_category(
    session: SessionDep, 
    associate_request: CategoryAsociation
):
    try:
        return product_service.associate_category(session, associate_request)
    except ProductNotFoundException:
        raise HTTPException(
            status_code=400, 
            detail="There is no product with this ID"
        )
    except CategoryNotFoundException:
        raise HTTPException(
            status_code=400, 
            detail="There is no category with this ID"
        )
    except DuplicatedCategoryException:
        raise HTTPException(
            status_code=400, 
            detail="Category is already associated to this product"
        )


@router.post('/desassociate-category/')
def desassociate_category(
    session: SessionDep, 
    body: CategoryAsociation
):
    try: 
        return product_service.desassociate_category(session, body)
    except ProductNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Product not found"
        )
    except CategoryNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="Category not found"
        )
    except UnlinkedCategoryException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="Category is not associated to this product"
        )
    except Exception: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST
        )

@router.delete('/{id}/', response_model=Message)
def delete_product(
    id: UUID,
    session: SessionDep, 
):
    try: 
        product_service.delete_product_by_id(session=session, id=id)
        return Message(message="Product deleted successfully")
    except ProductNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Product not found."
        )
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST
        )


@router.patch("/{id}/", response_model=ProductResponse)
def update_product(
    id: UUID,
    session: SessionDep, 
    product_request: UpdateQuantityRequest
): 
    try: 
        customer = product_service.update_product(session=session, product=product_request, id=id)
        return customer
    except ProductNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Product not found."
        )
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST
        )
    
@router.patch("/buy/{id}/", response_model=ProductResponse)
def buy_product(
    id: UUID,
    session: SessionDep, 
    quantity_request: UpdateQuantityRequest
): 
    try:
        customer = product_service.buy_product(session=session, quantity=quantity_request.quantity, id=id)
        return customer
    except ProductNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Product not found"
        )
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST
        )