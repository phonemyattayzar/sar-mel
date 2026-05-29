from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List


class OrderItemCreate(BaseModel):
    menu_item_id: UUID
    quantity: int


class OrderCreate(BaseModel):
    restaurant_id: UUID
    delivery_address: str
    items: List[OrderItemCreate]



class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    menu_item_id: UUID
    quantity: int
    price_at_purchase: int


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    restaurant_id: UUID
    order_number: str
    order_status: str
    total_amount_mmk: int
    delivery_address: str
    created_at: datetime

    order_items: List[OrderItemOut]