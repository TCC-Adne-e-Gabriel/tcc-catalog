from fastapi import UploadFile, File
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import LargeBinary
from sqlmodel import Field, Relationship, SQLModel, DateTime, func, Column
from uuid import UUID, uuid4
from decimal import Decimal

class ProductCategory():
    product_id: UUID
    categoria_id: UUID

class Category():
    id: UUID
    name: str
    description: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    products: List["Product"]

class Product(): 
    id: UUID
    name: str
    description: str
    price: Decimal
    available: bool
    sku: str
    discount: Optional[Decimal] = 0
    quantity: int
    image: Optional[bytes]
    created_at: datetime
    updated_at: datetime
    categories: List[Category]




