from fastapi import APIRouter, HTTPException, Depends, FastAPI
from typing import List
from app.schemas.category import CategoryCreateRequest, CategoryResponse, CategoryUpdateRequest
from app.services.category import CategoryService
from app.deps import SessionDep
from app.schemas.product import Message
from uuid import UUID
from app import auth
from app.context import user_id_context

app = FastAPI()
router = APIRouter(prefix="/category")
category_service = CategoryService()


@router.get("/{id}/", response_model=CategoryResponse)
def read_product_by_id(
    id: UUID, 
    session: SessionDep
) : 
    product = category_service.get_category(session=session, id=id)
    return product

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    session: SessionDep, 
    category: CategoryCreateRequest,
    decoded_token = Depends(auth.role_required(["admin"]))
): 
    user_id_context.set(decoded_token.id)
    category = category_service.create_category(session=session, category=category)
    return category

@router.get("/", response_model=List[CategoryResponse])
def read_categories(
    session: SessionDep, 
) : 
    categories = category_service.get_categories(session=session)
    return categories
    
@router.delete('/{id}', response_model=Message)
def delete_category(
    id: UUID,
    session: SessionDep, 
    decoded_token = Depends(auth.role_required(["admin"]))
):
    user_id_context.set(decoded_token.id)
    category_service.delete_category_by_id(session=session, id=id)
    return Message(message="Category deleted successfully")

@router.patch("/{id}", response_model=CategoryResponse)
def update_category(
    id: UUID,
    session: SessionDep, 
    category_request: CategoryUpdateRequest,
    decoded_token = Depends(auth.role_required(["admin"]))
): 
    user_id_context.set(decoded_token.id)
    customer = category_service.update_category(session=session, category=category_request, id=id)
    return customer
