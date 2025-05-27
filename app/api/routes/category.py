from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status
from ...deps import SessionDep
from typing import List
from app.schemas.category import CategoryCreateRequest, CategoryResponse, CategoryUpdateRequest
from app.services.category import CategoryService
from app.deps import SessionDep
from app.schemas.product import Message
from uuid import UUID

app = FastAPI()
router = APIRouter(prefix="/category")
category_service = CategoryService()

@router.post("/", response_model=CategoryResponse, status_code=201)
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
    category = category_service.create_category(session=session, category=category)
    return category


@router.get("/", response_model=List[CategoryResponse])
def read_categories(
    session: SessionDep, 
    skip: int = 0, 
    limit: int = 100
) : 
    categories = category_service.get_categories(session=session)
    return categories

@router.delete('/{id}', response_model=Message)
def delete_category(
    id: UUID,
    session: SessionDep, 
):
    try: 
        category_service.delete_category_by_id(session=session, id=id)
    except:
        raise HTTPException(
            status_code=400, 
            detail="Unable to delete category. Please check if the product still exists."
        )
    return Message(message="Category deleted successfully")


@router.patch("/{id}", response_model=CategoryResponse)
def update_category(
    id: UUID,
    session: SessionDep, 
    category_request: CategoryUpdateRequest
): 
    category_by_id = category_service.get_category_by_id(session=session, id=id)
    if(not category_by_id):
        raise HTTPException(
            status_code=400, 
            detail="Category not found"
        )
    customer = category_service.update_category(session=session, category=category_request, current_category=category_by_id)
    return customer