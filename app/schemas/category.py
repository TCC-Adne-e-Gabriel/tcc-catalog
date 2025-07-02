from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

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
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryAsociation(BaseModel):
    category_id: UUID
    product_id: UUID