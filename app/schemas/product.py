from fastapi import UploadFile, File
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from .category import CategoryResponse

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    sku: str
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

class ProductCreateRequest(ProductBase): 
    category_id: Optional[List[UUID]] = None

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    categories: List[CategoryResponse]

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

class UpdateQuantityRequest(BaseModel): 
    quantity: int