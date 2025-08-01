from fastapi import APIRouter
from app.database import db
from app.models.product import Product
import random

router = APIRouter()

def generate_unique_numeric_id():
    return str(random.randint(10**9, 10**10 - 1))  # 10-digit numeric ID

@router.post("/products", status_code=201)
async def create_product(product: Product):
    product_data = product.model_dump()

    while True:
        new_id = generate_unique_numeric_id()
        exists = await db.products.find_one({"_id": new_id})
        if not exists:
            break

    product_data["_id"] = new_id
    await db.products.insert_one(product_data)
    return {"id": new_id}


@router.get("/products")
async def list_products(
    name: str = None,
    size: str = None,
    limit: int = 10,
    offset: int = 0
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size  # nested match for sizes

    cursor = db.products.find(query).sort("_id").skip(offset).limit(limit)
    products = []

    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        if "sizes" in doc:
            del doc["sizes"]  # ✅ remove sizes from output
        products.append(doc)

    return {
        "data": products,
        "page": {
            "next": offset + limit,
            "limit": len(products),  # actual returned count
            "previous": max(offset - limit, 0)
        }
    }
