from sqlmodel import SQLModel, Field
from fastapi import UploadFile, File
from typing import Optional

class ProductRequest: 
    name: str
    price: float
    sku: str
    category_id: int
    quantity: int
    image: UploadFile = File(...)

class ProductBase(SQLModel):
    name: str
    price: float
    sku: str
    category_id: int
    quantity: int
    image: bytes = Field(sa_type="BYTEA")

class Category(SQLModel): 
    name: str
    description: str

class CategoryResponse(ProductCategoryBase):
    id: int

class Category(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: str
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    product: List["Product"] = Relationship(back_populates="category")

class Product(ProductBase, table=True): 
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    discount_id: int = Field(foreign_key="discount.id", ondelete="RESTRICT")
    discount: "Discount" = Relationship(back_populates="product")

    category_id: int = Field(foreign_key="category.id", ondelete="RESTRICT")
    category: "Category" = Relationship(back_populates="product")

class ProductResponse(ProductBase): 
    id: int
    discount_id: int


class DiscountBase(SQLModel): 
    name: str
    description: str
    discount_porcentage: float

class Discount(DiscountBase, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    product: List["Product"] = Relationship(back_populates="discount")
    
class DiscountResponse(DiscountBase):
    id: int



