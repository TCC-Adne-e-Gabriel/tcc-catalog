from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status
from typing import List
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest, ProductResponse, UpdateQuantityRequest
from app.schemas.category import CategoryResponse, CategoryAsociation, CategoryCreateRequest
from app.services.product import ProductService
from app.services.category import CategoryService
from app.deps import SessionDep
from uuid import UUID
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
    product_request: ProductCreateRequest
): 
    product_sku = product_service.get_product_by_sku(session=session, sku=product_request.sku)
    if(product_sku): 
        raise HTTPException(
            status_code=400, 
            detail="Product with this sku already exists in the system"
        )
    product = product_service.create_product(session=session, product=product_request)
    try: 
        if product_request.category_id:
            for category_id in product_request.category_id: 
                category = category_service.get_category_by_id(session=session, id=category_id)
                if(not category):
                    raise HTTPException(
                        status_code=400, 
                        detail="Check the categories"
                    )
            
                product_service.associate_category(session=session, category=category, product=product)
    except: 
        raise HTTPException(
            status_code=400, 
            detail="Check if this category exists"
        )
    return product


@router.post("/category", response_model=CategoryResponse, status_code=201)
def create_category(
    session: SessionDep, 
    category: CategoryCreateRequest
): 
    category_name = category_service.get_category_by_name(session=session, name=category.name)
    if(category_name): 
        raise HTTPException(
            status_code=400, 
            detail="category with this name already exists in the system"
        )
    category = product_service.create_category(session=session, category=category)
    return category

@router.post('/associate-category')
def associate_category(
    session: SessionDep, 
    body: CategoryAsociation
):
    product = product_service.get_product_by_id(session=session, id=body.product_id)
    if(not product):
        raise HTTPException(
            status_code=400, 
            detail="There is no product with this ID"
        )
    category = category_service.get_category_by_id(session=session, id=body.category_id)
    if(not category):
        raise HTTPException(
            status_code=400, 
            detail="There is no category with this ID"
        )
    if(category in product.categories): 
        raise HTTPException(
            status_code=400, 
            detail="Category is already associated to this product"
        )
    return product_service.associate_category(session, product, category)


@router.post('/desassociate-category')
def desassociate_category(
    session: SessionDep, 
    body: CategoryAsociation
):
    product = product_service.get_product_by_id(session=session, id=body.product_id)
    if(not product):
        raise HTTPException(
            status_code=400, 
            detail="There is no product with this ID"
        )
    category = category_service.get_category_by_id(session=session, id=body.category_id)
    if(not category):
        raise HTTPException(
            status_code=400, 
            detail="There is no category with this ID"
        )
    if(category not in product.categories): 
        raise HTTPException(
            status_code=400, 
            detail="Category is not associated to this product"
        )
    return product_service.desassociate_category(session, product, category)

@router.delete('{id}', response_model=Message)
def delete_product(
    id: UUID,
    session: SessionDep, 
):
    try: 
        product_service.delete_product_by_id(session=session, id=id)
    except:
        raise HTTPException(
            status_code=400, 
            detail="Unable to delete product. Please check if the product still exists."
        )
    return Message(message="Product deleted successfully")


@router.patch("/{id}", response_model=ProductResponse)
def update_product(
    id: UUID,
    session: SessionDep, 
    product_request: UpdateQuantityRequest
): 
    product_by_id = product_service.get_product_by_id(session=session, id=id)
    if(not product_by_id):
        raise HTTPException(
            status_code=400, 
            detail="Product not found"
        )
    customer = product_service.update_product(session=session, product=product_request, current_product=product_by_id)
    return customer

@router.patch("/buy/{id}", response_model=ProductResponse)
def buy_product(
    id: UUID,
    session: SessionDep, 
    quantity_request: UpdateQuantityRequest
): 
    product_by_id = product_service.get_product_by_id(session=session, id=id)
    if(not product_by_id):
        raise HTTPException(
            status_code=400, 
            detail="Product not found"
        )
    product_update = ProductUpdateRequest(quantity=product_by_id.quantity - quantity_request.quantity)
    customer = product_service.update_product(session=session, product=product_update, current_product=product_by_id)
    return customer