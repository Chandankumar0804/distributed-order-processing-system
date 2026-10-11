from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrderLogCreate(BaseModel):
    order_id: int
    status: str
    reason: Optional[str] = None


class OrderLogResponse(BaseModel):
    log_id: int
    order_id: int
    status: str
    reason: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True