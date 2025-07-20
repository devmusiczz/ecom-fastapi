from fastapi import APIRouter, Query
from app.database import db
from app.models.product import Product
from bson import ObjectId

router = APIRouter()

@router.post("/products", status_code=201)
async def create_product(product: Product):
    result = await db.products.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

@router.get("/products")
async def list_products(
    name: str = None,
    size: str = None,
    limit: int = 0,
    offset: int = 0
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["size"] = size

    cursor = db.products.find(query).skip(offset).limit(limit)
    products = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        products.append(doc)

    return {"data": products, "page": {"next": str(offset + limit), "limit": limit, "previous": offset - limit}}
