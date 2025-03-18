from datetime import datetime
import time

from fastapi import APIRouter, Depends, HTTPException

from src.database.models import Order, OrderCreate, OrderUpdate, OrderBase
from src.database.core import DbDependency
from src.orders.service import create_order, verify_user, take_order as take_order_service
from src.orders.service import get_my_taken_orders
from src.orders.schemas import OrderWithUserDetails
from src.kafka.producer import send_user_ids_to_kafka
from src.kafka.consumer import consume_kafka_messages_for_users
from src.orders.schemas import User

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
    user_ids = {order.creator_id for order in orders} | {payload['user_id']}
    
    start = time.time()
    correlation_id = await send_user_ids_to_kafka(list(user_ids))
    users_data = await consume_kafka_messages_for_users(correlation_id, user_ids)
    print(f"Kafka time: {time.time() - start:.3f} sec")
    
    orders_with_users = []
    for order in orders:
        creator_user = users_data.get(order.creator_id)
        executor_user = users_data.get(order.executor_id)
        orders_with_users.append(OrderWithUserDetails(
            id=order.id,
            creator=User(username=creator_user['username']) if creator_user else None,
            executor=User(username=executor_user['username']) if executor_user else None,
            title=order.title,
            price=order.price,
            details=order.details,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            executor_id=order.executor_id,
            creator_id=order.creator_id
        ))

    return orders_with_users

