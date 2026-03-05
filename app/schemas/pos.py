from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class TabItemSchema(BaseModel):
    name: str
    size: str = ""
    price: float = 0
    qty: int = 1


class OpenTabBase(BaseModel):
    customer_name: str
    customer_id: Optional[UUID] = None
    items: list[TabItemSchema] = []
    opened_at: datetime
    server: str = ""
    subtotal: float = 0
    table_number: Optional[str] = None


class OpenTabCreate(OpenTabBase):
    pass


class OpenTabResponse(OpenTabBase):
    id: UUID

    model_config = {"from_attributes": True}


class CloseTabRequest(BaseModel):
    tab_id: UUID
    payment_method: str = "card"
    discount: float = 0
    discount_type: Optional[str] = None
    tip_amount: float = 0


class POSTransactionResponse(BaseModel):
    id: UUID
    customer_name: str
    items: list[Any]
    subtotal: float
    tax: float
    discount: Optional[float] = None
    discount_type: Optional[str] = None
    total: float
    payment_method: str
    server: str
    closed_at: datetime
    tip_amount: Optional[float] = None

    model_config = {"from_attributes": True}
