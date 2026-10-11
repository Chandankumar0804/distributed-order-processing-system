from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class OrderCreate(BaseModel):
    order_id: int | None = None
    customer_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    payment_status: str = "Pending"
    payment_type: str = "CASH"
    source: str


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    order_time: datetime
    payment_status: str
    payment_type: str
    source: str
    subtotal: Decimal
    discount_rate: Decimal
    discount_amount: Decimal
    final_amount: Decimal

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    payment_status: str
    reason: str | None = None
    