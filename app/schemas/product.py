from fastapi import UploadFile, File
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class ProductCreateRequest(BaseModel):
    name: str
    description: str
    price: float
    sku: str
    category_id: Optional[List[int]] = None
    quantity: int
    available: bool
    image: Optional[UploadFile] = File(None)

class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    sku: Optional[str] = None
    category_id: Optional[List[UUID]] = None
    quantity: Optional[int] = None
    image: Optional[UploadFile] = File(None)

class ProductResponse(ProductCreateRequest):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PasswordRequest(BaseModel):
    current_password: str
    new_password: str 

class Message(BaseModel): 
    message: str

class CustomerChangePassword(BaseModel):
    password: str

class ListProductResponse(BaseModel): 
    data: List[ProductResponse]
    count: int


class CategoryCreateRequest(BaseModel): 
    name: str
    description: str

class CategoryResponse(CategoryCreateRequest):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CategoryUpdateRequest(BaseModel): 
    name: Optional[str]
    description: Optional[str]

class CategoryAsociation(BaseModel):
    category_id: UUID
    product_id: UUID