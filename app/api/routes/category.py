from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status, Depends
from typing import List, Any
from app.services.category import CategoryService
from uuid import UUID, uuid4
from app.core.encrypt import encrypt_data
from app.core.db import get_db_conn
from datetime import datetime

app = FastAPI()
router = APIRouter(prefix="/category")
category_service = CategoryService()
    
@router.post("/", status_code=201)
async def create_category(
    id,
    request: Request,
    conn=Depends(get_db_conn)
) -> Any: 
    body = await request.json()
    cursor = conn.cursor()
    date_now = datetime.now()
    category_id = uuid4()

    query = """
        INSERT INTO category (id, name, description, neighborhood, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        uuid4(),
        body["name"],
        body["description"],
        body["neighborhood"],
        date_now, 
        date_now
    )
        
    body["id"] = category_id
    body["created_at"] = date_now
    body["updated_at"] = date_now
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    return body

@router.get("/{id}")
def get_address_by_id(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category WHERE category.id = '" + id + "'")
    category = cursor.fetchone()
    cursor.close()
    return {"category": category}

@router.get("/")
def get_categories(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    cursor.close()
    return {"category": categories}


@router.patch("/address/{id}/")
async def update_category(id, category: Request, conn=Depends(get_db_conn)):
    category = await category.json()
    cursor = conn.cursor()

    fields = []
    values = []

    if category.get("name"):
        fields.append("name = %s")
        values.append(category["name"])

    if category.get("description"):
        fields.append("description = %s")
        values.append(category["description"])

    fields.append("updated_at = %s")
    values.append(datetime.now())


    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(str(id))   

    query = f"UPDATE category SET {', '.join(fields)} WHERE id = %s"

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Category not found")

    cursor.close()
    return {"message": "Category updated successfully"}

@router.delete("/{id}/")
def delete_category(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM category WHERE id = = '" + id + "'")
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Category not found")

    cursor.close()
    return {"message": "Category deleted successfully"}
