from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.category import CategoryCreateRequest, CategoryResponse, CategoryUpdateRequest
from app.services.category import CategoryService
from app.deps import SessionDep
from app.exceptions import CategoryNameAlreadyExists, CategoryNotFoundException
from app.schemas.product import Message
from uuid import UUID
from http import HTTPStatus

app = FastAPI()
router = APIRouter(prefix="/internal/category")
category_service = CategoryService()


@router.get("/{id}/", response_model=CategoryResponse)
def read_product_by_id(
    id: UUID, 
    session: SessionDep
) : 
    try:
        product = category_service.get_category(session=session, id=id)
        return product
    except CategoryNotFoundException: 
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Category not found"
        )
    except Exception: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )
    
@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    session: SessionDep, 
    category: CategoryCreateRequest
): 
    try: 
        category = category_service.create_category(session=session, category=category)
        return category
    except CategoryNameAlreadyExists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="Category name already exists"
        )
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    
@router.get("/", response_model=List[CategoryResponse])
def read_categories(
    session: SessionDep, 
) : 
    try: 
        categories = category_service.get_categories(session=session)
        return categories
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

@router.delete('/{id}', response_model=Message)
def delete_category(
    id: UUID,
    session: SessionDep, 
):
    try: 
        category_service.delete_category_by_id(session=session, id=id)
        return Message(message="Category deleted successfully")
    except CategoryNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Category not found"
        )


@router.patch("/{id}", response_model=CategoryResponse)
def update_category(
    id: UUID,
    session: SessionDep, 
    category_request: CategoryUpdateRequest
): 
    try: 
        customer = category_service.update_category(session=session, category=category_request, id=id)
        return customer
    except CategoryNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Category not found"
        )
    except Exception:        
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND
        )