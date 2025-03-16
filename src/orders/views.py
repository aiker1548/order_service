from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from src.database.models import Order, OrderCreate, OrderUpdate, OrderBase
from src.database.core import DbDependency
from src.orders.service import create_order, verify_user


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order, status_code=201)
async def create_new_order(
    order_data: OrderBase,
    db: DbDependency, 
    current_user=Depends(verify_user)  # Получаем пользователя из user-service
):
    return await create_order(db, order_data, current_user)


# @router.get("/{order_id}", response_model=Order)
# async def read_order(order_id: str):
#     order = await get_order(order_id)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order

# @router.get("/my/", response_model=list[Order])
# async def read_user_orders(current_user: dict = Depends(get_current_user)):
#     return await get_orders_by_user(current_user['id'])

# @router.put("/{order_id}", response_model=Order)
# async def update_existing_order(order_id: str, order_update: OrderUpdate):
#     order = await update_order(order_id, order_update)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order

# @router.delete("/{order_id}", status_code=204)
# async def delete_existing_order(order_id: str):
#     if not await delete_order(order_id):
#         raise HTTPException(status_code=404, detail="Order not found")
    
# @router.post("/orders/", response_model=Order, status_code=201)
# async def create_order(db: DbDependency, order: OrderCreate):
#     collection = db.orders
#     order_dict = order.dict()
#     result = await collection.insert_one(order_dict)
#     order_dict["_id"] = str(result.inserted_id)
#     return Order(**order_dict)