from app.models.product import Product, Category
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest, ProductResponse
from app.schemas.category import CategoryCreateRequest, CategoryResponse
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from uuid import UUID
import json
from datetime import datetime
from typing import List

class ProductService():
    def get_values(body):       
        fields = []
        values = []

        if body.get("name") is not None:
            fields.append("name = %s")
            values.append(body["name"])

        if body.get("description") is not None:
            fields.append("description = %s")
            values.append(body["description"])

        if body.get("price") is not None:
            fields.append("price = %s")
            values.append(body["price"])

        if body.get("available") is not None:
            fields.append("available = %s")
            values.append(body["available"])

        if body.get("sku") is not None:
            fields.append("sku = %s")
            values.append(body["sku"])

        if "discount" in body:
            fields.append("discount = %s")
            values.append(body["discount"])

        if body.get("quantity") is not None:
            fields.append("quantity = %s")
            values.append(body["quantity"])

        if "image" in body:
            fields.append("image = %s")
            values.append(body["image"])

        if body.get("categories") is not None:
            categories_json = json.dumps(body["categories"])
            fields.append("categories = %s")
            values.append(categories_json)

        fields.append("updated_at = %s")
        values.append(datetime.now())
        return values, fields
