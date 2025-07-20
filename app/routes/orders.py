from fastapi import APIRouter
from app.models.order import OrderCreate
from app.database import db
from bson import ObjectId

router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(order: OrderCreate):
    order_dict = order.dict()
    result = await db.orders.insert_one(order_dict)
    return {"id": str(result.inserted_id)}

@router.get("/orders/{user_id}")
async def get_orders(user_id: str, limit: int = 0, offset: int = 0):
    cursor = db.orders.find({"userId": user_id}).skip(offset).limit(limit)
    orders = []
    async for order in cursor:
        enriched_items = []
        for item in order["items"]:
            product = await db.products.find_one({"_id": ObjectId(item["productId"])})
            item["productDetails"] = {
                "name": product["name"],
                "id": str(product["_id"])
            }
            del item["productId"]
            enriched_items.append(item)
        order_obj = {
            "id": str(order["_id"]),
            "items": enriched_items,
            "total": sum(item["qty"] * product["price"] for item in order["items"]),
        }
        orders.append(order_obj)

    return {
        "data": orders,
        "page": {
            "next": str(offset + limit),
            "limit": limit,
            "previous": offset - limit
        }
    }
