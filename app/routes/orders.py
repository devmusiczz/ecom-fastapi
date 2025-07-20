from fastapi import APIRouter
from app.models.order import OrderCreate
from app.database import db
from bson import ObjectId
import random

router = APIRouter()

def generate_unique_numeric_id():
    return str(random.randint(10**9, 10**10 - 1))  # 10-digit numeric ID

@router.post("/orders", status_code=201)
async def create_order(order: OrderCreate):
    order_data = order.dict()

    # Generate and check for unique ID
    while True:
        new_id = generate_unique_numeric_id()
        existing = await db.orders.find_one({"_id": new_id})
        if not existing:
            break

    order_data["_id"] = new_id
    await db.orders.insert_one(order_data)
    return {"id": new_id}

@router.get("/orders/{user_id}")
async def get_orders(user_id: str, limit: int = 0, offset: int = 0):
    cursor = db.orders.find({"userId": user_id}).skip(offset).limit(limit)
    orders = []

    async for order in cursor:
        enriched_items = []
        total = 0
        for item in order["items"]:
            product = await db.products.find_one({"_id": ObjectId(item["productId"])})
            if not product:
                continue  # skip if product not found

            item_total = item["qty"] * product["price"]
            total += item_total

            enriched_items.append({
                "productDetails": {
                    "name": product["name"],
                    "id": str(product["_id"])
                },
                "qty": item["qty"]
            })

        orders.append({
            "id": str(order["_id"]),
            "items": enriched_items,
            "total": total
        })

    return {
        "data": orders,
        "page": {
            "next": offset + limit,
            "limit": limit,
            "previous": max(offset - limit, 0)
        }
    }
