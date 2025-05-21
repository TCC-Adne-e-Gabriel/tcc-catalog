from app.models.product import Product, Category
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest, ProductResponse, CategoryCreateRequest, CategoryResponse
from sqlmodel import Session, select
from uuid import UUID
from typing import List

class CategoryService():
  
    def create_category(self, session: Session, category: CategoryCreateRequest) -> CategoryResponse:
        category_data = category.model_dump()
        db_category = Category(**category_data)
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return db_category

    def get_category_by_name(self, session: Session, name: str) -> Category: 
        statement = select(Category).where(Category.name == name)
        result = session.exec(statement).first()
        return result
    
    def get_category_by_name(self, session: Session, id: UUID) -> Category: 
        statement = select(Category).where(Category.id == id)
        result = session.exec(statement).first()
        return result
    
    def get_categories(self, session: Session) -> List[CategoryResponse]: 
        statement = select(Category)
        return session.exec(statement)
