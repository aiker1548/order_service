from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class OrderStatus(str, Enum):
    PENDING = "pending"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"


class OrderBase(BaseModel):
    title: str  
    price: str  
    details: Optional[Dict[str, Any]] = None  


class OrderCreate(OrderBase):
    creator_id: int  
    status: OrderStatus  
    created_at: datetime  


class OrderUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    status: Optional[OrderStatus] = None


class Order(OrderBase):
    id: str
    creator_id: int
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    executor_id: Optional[int] = None  # ID исполнителя