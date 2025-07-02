from fastapi import FastAPI
from fastapi import APIRouter, Depends
from typing import List
from app.schemas.product import ProductCreateRequest, ProductResponse, UpdateQuantityRequest
from app.schemas.category import CategoryAsociation
from app.services.product import ProductService
from app.services.category import CategoryService
from app.deps import SessionDep
from http import HTTPStatus
from uuid import UUID
from app.schemas.product import Message
from app import auth


app = FastAPI()
router = APIRouter(prefix="/product")
product_service = ProductService()
category_service = CategoryService()


@router.get("/{id}", response_model=ProductResponse)
def read_product_by_id(
    id: UUID, 
    session: SessionDep, 
) : 
    product = product_service.get_product(session=session, product_id=id)
    return product

@router.get("/", response_model=List[ProductResponse])
def read_products(
    session: SessionDep
) : 
    product = product_service.get_products(session=session)
    return product


@router.post("/", response_model=ProductResponse, status_code=201, dependencies=[Depends(auth.role_required(["admin"]))])
def create_product(
    session: SessionDep, 
    product_request: ProductCreateRequest
): 
    product = product_service.create_product(session=session, product_request=product_request)
    return product

@router.post('/associate-category/', response_model=ProductResponse, dependencies=[Depends(auth.role_required(["admin"]))])
def associate_category(
    session: SessionDep, 
    associate_request: CategoryAsociation
):
    return product_service.associate_category(session, associate_request)

@router.post('/desassociate-category/', dependencies=[Depends(auth.role_required(["admin"]))])
def desassociate_category(
    session: SessionDep, 
    body: CategoryAsociation
):
    return product_service.desassociate_category(session, body)

@router.delete('/{id}/', response_model=Message, dependencies=[Depends(auth.role_required(["admin"]))])
def delete_product(
    id: UUID,
    session: SessionDep, 
):
    product_service.delete_product_by_id(session=session, id=id)
    return Message(message="Product deleted successfully")

@router.patch("/{id}/", response_model=ProductResponse, dependencies=[Depends(auth.role_required(["admin"]))])
def update_product(
    id: UUID,
    session: SessionDep, 
    product_request: UpdateQuantityRequest
): 
    customer = product_service.update_product(session=session, product=product_request, id=id)
    return customer
    
@router.patch("/buy/{id}/", response_model=ProductResponse, dependencies=[Depends(auth.role_required(["admin", "service"]))])
def buy_product(
    id: UUID,
    session: SessionDep, 
    quantity_request: UpdateQuantityRequest
): 
    customer = product_service.buy_product(session=session, quantity=quantity_request.quantity, id=id)
    return customer