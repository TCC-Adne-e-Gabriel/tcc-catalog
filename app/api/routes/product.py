from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status, Depends
from typing import List, Any
from app.services.product import ProductService
from app.services.category import CategoryService
from app.core.db import get_db_conn
from uuid import UUID, uuid4
from datetime import datetime
import json

app = FastAPI()
router = APIRouter(prefix="/product")
product_service = ProductService()
category_service = CategoryService()


@router.get("/{id}/")
def read_product_by_id(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE product.id = '"+ id + "'")
    product = cursor.fetchone()    
    cursor.close()
    return {"product": product}

@router.get("/")
def get_products(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    cursor.close()
    return {"category": products}


@router.post("/", status_code=201)
async def create_product(
    request: Request,
    conn=Depends(get_db_conn)
) -> Any: 
    body = await request.json()
    cursor = conn.cursor()
    date_now = datetime.now()
    product_id = uuid4()

    name = body.get("name")
    description = body.get("description")
    price = body.get("price")
    available = body.get("available", True)
    sku = body.get("sku")
    discount = body.get("discount", None)
    quantity = body.get("quantity", 0)
    image = body.get("image", None) 
    created_at = date_now
    updated_at = date_now

    categories = body.get("categories", None) 

    query = """
        INSERT INTO product (
            id, name, description, price, available, sku, discount, quantity, image, created_at, updated_at, categories
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    values = (
        product_id,
        name,
        description,
        price,
        available,
        sku,
        discount,
        quantity,
        image,
        created_at,
        updated_at,
        categories
    )

    cursor.execute(query, values)
    conn.commit()
    cursor.close()

    body["id"] = product_id
    body["created_at"] = created_at.isoformat()
    body["updated_at"] = updated_at.isoformat()

    body["discount"] = discount
    body["image"] = image
    body["categories"] = categories

    return body

@router.post('/associate-category')
async def associate_category(
    request: Request, 
    conn=Depends(get_db_conn)
):
    body = await request.json()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE product.id = '"+ id + "'")
    product = cursor.fetchone()    
    if(not product):
        raise HTTPException(
            status_code=400, 
            detail="There is no product with this ID"
        )
    cursor.execute("SELECT * FROM category WHERE category.id = '" + id + "'")
    category = cursor.fetchone()
    if(not category):
        raise HTTPException(
            status_code=400, 
            detail="There is no category with this ID"
        )
    
    cursor.execute("SELECT * FROM product_category pc WHERE pc.product_id = '" + id + "' AND pc.category_id")
    relationship = cursor.fetchone()

    if(relationship): 
        raise HTTPException(
            status_code=400, 
            detail="Category is already associated to this product"
        )
    
    query = f"INSERT INTO product_category (product_id, category_id) VALUES ('{body["product_id"]}', '{body["category_id"]}');"

    cursor.execute(query)
    conn.commit()
    return {"message": "New category added to product"}


@router.post('/desassociate-category')
async def desassociate_category(
    request: Request, 
    conn=Depends(get_db_conn)
):
    body = await request.json()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE product.id = '"+ id + "'")
    product = cursor.fetchone()    
    if(not product):
        raise HTTPException(
            status_code=400, 
            detail="There is no product with this ID"
        )
    cursor.execute("SELECT * FROM category WHERE category.id = '" + id + "'")
    category = cursor.fetchone()
    if(not category):
        raise HTTPException(
            status_code=400, 
            detail="There is no category with this ID"
        )
    
    cursor.execute("SELECT * FROM product_category pc WHERE pc.product_id = '" + id + "' AND pc.category_id")
    relationship = cursor.fetchone()

    if(not relationship): 
        raise HTTPException(
            status_code=400, 
            detail="Category is not associated to this product"
        )
    
    query =  f"DELETE FROM product_category WHERE product_id = '{body["product_id"]}' AND category_id = '{body["category_id"]}';"

    cursor.execute(query)
    conn.commit()
    return {"message": "Category removed of product"}


async def update_product(
    id: str,
    product: Request,
    conn=Depends(get_db_conn)
):
    body = await product.json()
    cursor = conn.cursor()
    values, fields = product_service.get_values(body)

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(id)

    query = f"UPDATE product SET {', '.join(fields)} WHERE id = %s"

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Product not found")

    cursor.close()
    return {"message": "Product updated successfully"}