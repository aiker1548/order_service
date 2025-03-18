from datetime import datetime
from bson import ObjectId

from fastapi import HTTPException
import httpx
from starlette.requests import Request

from src.database.models import OrderStatus, Order, OrderCreate
from src.auth import verify_access_token

# Проверка пользователя через HTTP

# async def verify_user(request: Request):
#     token = request.headers.get("Authorization")
#     if not token:
#         raise HTTPException(status_code=401, detail="Authorization token is missing")

#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             "http://localhost:8000/users/me/",
#             headers={"Authorization": token}
#         )

#     if response.status_code == 200:
#         return response.json()
#     elif response.status_code == 404:
#         raise HTTPException(status_code=404, detail="User not found")
#     else:
#         raise HTTPException(status_code=500, detail="Error verifying user")

def verify_user(request: Request):
    token = request.headers.get("Authorization")
    if token and token.startswith('Bearer'):
            token = token.split("Bearer ")[-1].strip()
            payload = verify_access_token(token)
    else:
        raise HTTPException(status_code=401, detail="Authorization token is missing")

    return payload

# Создание заказа
async def create_order(db, order_data: Order, current_user) -> Order:
    # Проверяем, существует ли создатель заказа
    # Формируем документ для MongoDB
    new_order = OrderCreate(
        title=order_data.title,
        price=order_data.price,
        creator_id=current_user['user_id'],
        details=order_data.details,
        status=OrderStatus.OPEN,  
        created_at=datetime.utcnow(),
    )
    result = await db.orders.insert_one(new_order.dict())
    return Order(id=str(result.inserted_id), **new_order.dict())

# Получение списка открытых заказов
async def get_open_orders(db) -> list[Order]:
    cursor = db.orders.find({"status": OrderStatus.OPEN})
    orders = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        orders.append(Order(**doc))
    return orders

# Взятие заказа на выполнение
async def take_order(db, order_id: str, executor_id: str) -> Order:

    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order["status"] != OrderStatus.OPEN:
        raise HTTPException(status_code=400, detail="Order is not open")

    updated_order = {
        **order,
        "executor_id": executor_id,
        "status": OrderStatus.IN_PROGRESS,
        "updated_at": datetime.utcnow()
    }
    await db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": updated_order})

    updated_order["id"] = str(order_id)
    return Order(**updated_order)

# Завершение заказа
async def complete_order(db, order_id: str, executor_id: str) -> Order:
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order["status"] != OrderStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Order is not in progress")
    if order["executor_id"] != executor_id:
        raise HTTPException(status_code=403, detail="You are not the executor of this order")

    updated_order = {
        **order,
        "status": OrderStatus.COMPLETED,
        "updated_at": datetime.utcnow()
    }
    await db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": updated_order})

    updated_order["id"] = str(order_id)
    return Order(**updated_order)

async def get_my_taken_orders(db, executor_id: int) -> list[Order]:
    orders = await db.orders.find({"executor_id": executor_id}).to_list(length=100)
    if not orders:
        return []
    # Преобразуем _id в id, если оно присутствует
    for order in orders:
        order["id"] = str(order["_id"])  # Здесь мы просто переводим _id в строку и сохраняем в id
        del order["_id"]  # Удаляем старое поле _id
        
    return [Order(**order) for order in orders]