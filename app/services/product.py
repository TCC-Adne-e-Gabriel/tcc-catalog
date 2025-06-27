from app.models.product import Product, Category
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest, ProductResponse
from app.services.category import CategoryService
from app.schemas.category import CategoryAsociation
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from uuid import UUID
from app.exceptions import ProductNotFoundException, CategoryNotFoundException, SameSkuException, DuplicatedCategoryException, UnlinkedCategoryException
from typing import List

class ProductService():
    def __init__(self): 
        self.category_service = CategoryService()

    def create_product(self, session: Session, product_request: ProductCreateRequest) -> ProductResponse:
        product_data = product_request.model_dump()
        product_sku = self.get_product_by_sku(session=session, sku=product_request.sku)
        if product_sku: 
            raise SameSkuException
        
        if product_request.category_id:
            categories = []
            for category_id in product_request.category_id: 
                category = self.category_service.get_category_by_id(session=session, id=category_id)
                if not category: 
                    continue
                categories.append(category)
            product_data["categories"] = categories

        db_product = Product(**product_data)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product

    def buy_product(self, session: Session, quantity: int, id: UUID) -> ProductResponse:
        current_product = self.get_product_by_id(session, id)
        if not current_product: 
            raise ProductNotFoundException
        product_request = ProductUpdateRequest(quantity=current_product.quantity - quantity)
        product_db = product_request.model_dump(exclude_none=True)
        current_product.sqlmodel_update(product_db)
        session.add(current_product)
        session.commit()
        session.refresh(current_product)
        return current_product
    
    def update_product(self, session: Session, product: ProductUpdateRequest, id: UUID) -> ProductResponse:
        current_product = self.get_product_by_id(session, id)
        if not current_product: 
            raise ProductNotFoundException
        product_db = product.model_dump(exclude_none=True)
        current_product.sqlmodel_update(product_db)
        session.add(current_product)
        session.commit()
        session.refresh(current_product)
        return current_product

    def get_product(self, session: Session, product_id: UUID) -> ProductResponse: 
        statement = select(Product).where(Product.id == product_id)
        product = session.exec(statement).first()
        if not product: 
            raise ProductNotFoundException
        return product

        if "discount" in body:
            fields.append("discount = %s")
            values.append(body["discount"])

    def get_product_by_sku(self, session: Session, sku: str) -> ProductResponse: 
        statement = select(Product).where(Product.sku == sku)
        result = session.exec(statement).first()
        return result
    
    def get_product_by_id(self, session: Session, id: UUID) -> Product: 
        statement = select(Product).where(Product.id == id).options(
            selectinload(Product.categories)
        )
        result = session.exec(statement).first()
        return result

    def associate_category(self, session: Session, category_link: CategoryAsociation) -> ProductResponse: 
        product = self.get_product_by_id(session=session, id=category_link.product_id)
        if not product:
            raise ProductNotFoundException
        category = self.category_service.get_category_by_id(session=session, id=category_link.category_id)
        if not category:
            raise CategoryNotFoundException
        if(category in product.categories): 
            raise DuplicatedCategoryException
        product.categories.append(category)
        session.commit()
        session.refresh(product)
        return product
    
    def desassociate_category(self, session: Session, category_unlink: CategoryAsociation) -> ProductResponse: 
        product = self.get_product_by_id(session=session, id=category_unlink.product_id)
        if not product: 
            raise ProductNotFoundException
        
        category = self.category_service.get_category_by_id(session=session, id=category_unlink.category_id)
        if not category: 
            raise CategoryNotFoundException
        
        if category not in product.categories:
            raise UnlinkedCategoryException

        product.categories.remove(category)
        session.commit()
        session.refresh(product)
        return product
    

    def delete_product_by_id(self, session: Session, id: UUID): 
        product = self.get_product_by_id(session=session, id=id)

        if not product: 
            raise ProductNotFoundException
        for category in product.categories:
            category.products.remove(product)
            session.commit()
        session.delete(product)
        session.commit()
