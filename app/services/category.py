from app.models.product import Category
from app.schemas.category import CategoryCreateRequest, CategoryResponse, CategoryUpdateRequest
from sqlmodel import Session, select
from uuid import UUID
from typing import List
from app.exceptions import CategoryNameAlreadyExists, CategoryNotFoundException
from app.catalog_logging import logger

class CategoryService():
  
    def create_category(self, session: Session, category: CategoryCreateRequest) -> CategoryResponse:
        category_name = self.get_category_by_name(session=session, name=category.name)
        if category_name: 
            raise CategoryNameAlreadyExists
        category_data = category.model_dump()
        db_category = Category(**category_data)
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        
        logger.audit(f"Category {db_category.id} created")
        return db_category

    def get_category_by_name(self, session: Session, name: str) -> Category: 
        statement = select(Category).where(Category.name == name)
        result = session.exec(statement).first()
        return result
    
    def get_category_by_id(self, session: Session, id: UUID) -> Category: 
        statement = select(Category).where(Category.id == id)
        result = session.exec(statement).first()
        return result
    
    def get_category(self, session: Session, id: UUID) -> CategoryResponse:
        category = self.get_category_by_id(session=session, id=id)
        if not category: 
            raise CategoryNotFoundException
        return category
        
    def get_categories(self, session: Session) -> List[CategoryResponse]: 
        statement = select(Category)
        return session.exec(statement)
    
    def delete_category_by_id(self, session: Session, id: UUID): 
        category = self.get_category_by_id(session=session, id=id)
        if not category: 
            raise CategoryNotFoundException
        for product in category.products:
            product.categories.remove(category)
            session.commit()
        session.delete(category)
        session.commit()
        logger.audit(f"Category {id} deleted")

    def update_category(self, session: Session, category: CategoryUpdateRequest, current_category: Category) -> CategoryResponse:
        category_db = category.model_dump(exclude_none=True)
        current_category.sqlmodel_update(category_db)
        session.add(current_category)
        session.commit()
        session.refresh(current_category)
        logger.audit(f"Category {current_category.id} updated")
        return current_category


