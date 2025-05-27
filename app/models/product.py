from fastapi import UploadFile, File
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import LargeBinary, String
from sqlmodel import Field, Relationship, SQLModel, DateTime, func, Column
from uuid import UUID, uuid4
from decimal import Decimal

class ProductCategory(SQLModel, table=True):
    product_id: UUID = Field(foreign_key="product.id", primary_key=True)
    categoria_id: UUID = Field(foreign_key="category.id", primary_key=True)

class Category(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        )
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
        )
    )   
    products: List["Product"] = Relationship(
        back_populates="categories",
        link_model=ProductCategory
    )


class Product(SQLModel, table=True): 
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    price: Decimal
    available: bool
    sku: str = Field(
        unique=True, 
        index=True
    )
    discount: Optional[Decimal] = 0
    quantity: int
    image: Optional[bytes] = Field(
        default=None,
        sa_column=Column(LargeBinary, nullable=True)  
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    
    categories: List[Category] = Relationship(
        back_populates="products",
        link_model=ProductCategory
    )





