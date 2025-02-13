from typing import Union
from app.models import ProductPublic, Product
from fastapi import FastAPI

app = FastAPI()

@router.get("/products", response_model=ProductPublic)
def get_products(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100
) -> Any:
    statement = select(Product)
    count_statement = select(func.count()).select_from(Product)
    statement = statement.offset(skip).limit(limit)
    products = session.exec(statement).all()
    count = session.exec(count_statement).one()

    return DevicesPublic(data=devices, count=count)


@router.get("/sales-products", response_model=DevicesPublic):
    pass


@router.get
def get_sales_products(
    session: SessionDep,

): 
    

@router.get('create/sales-products')
async def create_sales_products(
    session: SessionDep, 
    discount: DiscountCreate, 
    product_ids: List[int]
):

    new_discount = Discount.model_validate(productRequest)
    session.add(new_discount)
    session.refresh(new_discount)
    
    return new_discount

@app.post("/products/", response_model=ProductPublic)
async def create_product(
    *,
    session: SessionDep,
    productRequest: ProductRequest
):
    image_data = await image.read()

    product = Product.model_validate(productRequest)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product