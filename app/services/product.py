from app.models.product import Product, Category
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest, ProductResponse
from app.schemas.category import CategoryCreateRequest, CategoryResponse
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List

class ProductService():
    def create_product(self, session: Session, product: ProductCreateRequest) -> ProductResponse:
        product_data = product.model_dump()
        db_product = Product(**product_data)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product
    

    def create_category(self, session: Session, category: CategoryCreateRequest) -> CategoryResponse:
        category_data = category.model_dump()
        db_category = Category(**category_data)
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return db_category


    def update_product(self, session: Session, product: ProductUpdateRequest, current_product: Product) -> ProductResponse:
        product_db = product.model_dump(exclude_none=True)
        current_product.sqlmodel_update(product_db)
        session.add(current_product)
        session.commit()
        session.refresh(current_product)
        return current_product


    def get_product(self, session: Session, product_id: UUID) -> Product: 
        statement = select(Product).where(Product.id == product_id)
        return session.exec(statement).first()

    def get_products(self, session: Session) -> List[ProductResponse]: 
        statement = select(Product).options(
            selectinload(Product.categories)
        )
        return session.exec(statement)

    def get_product_by_sku(self, session: Session, sku: str) -> Product: 
        statement = select(Product).where(Product.sku == sku)
        result = session.exec(statement).first()
        return result
    
    def get_product_by_id(self, session: Session, id: UUID) -> Product: 
        statement = select(Product).where(Product.id == id).options(
            selectinload(Product.categories)
        )
        result = session.exec(statement).first()
        return result
    
    def associate_category(self, session: Session, product: Product, category: Category) -> ProductResponse: 
        product.categories.append(category)
        session.commit()
        session.refresh(product)
        return product
    
    def desassociate_category(self, session: Session, product: Product, category: Category) -> ProductResponse: 
        product.categories.remove(category)
        session.commit()
        session.refresh(product)
        return product
    

    def delete_product_by_id(self, session: Session, id: UUID): 
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).first()

        for category in product.categories:
            category.products.remove(product)
            session.commit()
        session.delete(product)
        session.commit()
