from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderStatusRDTO(BaseModel):
    id: int
    title: str
    value: str
    status: bool
    is_first: bool
    is_last: bool
    prev_id: Optional[int]
    next_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderStatusWithRelationRDTO(BaseModel):
    id: int
    title: str
    value: str
    status: bool
    is_first: bool
    is_last: bool
    prev_id: Optional[int]
    next_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    prev_status: Optional["OrderStatusRDTO"] = None
    next_status: Optional["OrderStatusRDTO"] = None

    class Config:
        from_attributes = True