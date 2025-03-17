from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from src.database.models import Order, OrderCreate, OrderUpdate, OrderBase
from src.database.core import DbDependency
from src.orders.service import create_order, verify_user, take_order as take_order_service
from src.orders.service import get_my_taken_orders
from src.orders.schemas import OrderWithUserDetails

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order, status_code=201)
async def create_new_order(
    order_data: OrderBase,
    db: DbDependency, 
    payload=Depends(verify_user)  # Получаем пользователя из user-service
):
    return await create_order(db, order_data, payload)

@router.post("/{order_id}/take/", response_model=Order)
async def take_order(
    db: DbDependency,
    order_id: str,
    payload=Depends(verify_user)
):
    order = await take_order_service(db, order_id, payload['user_id'])
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
    

@router.get("/taken/", response_model=list[OrderWithUserDetails])
async def my_orders(
    db: DbDependency,
    payload=Depends(verify_user)
):
    orders = await get_my_taken_orders(db, payload['user_id'])
    user_ids = set()
    user_ids.add(order['executor_id'])
    for order in orders:
        user_ids.add(order['executor_id'])
    
    return orders
    

