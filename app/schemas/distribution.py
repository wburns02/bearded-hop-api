from __future__ import annotations

# dates stored as strings
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Wholesale Account
# ---------------------------------------------------------------------------

class WholesaleAccountBase(BaseModel):
    business_name: str
    contact_name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    address: str = ""
    type: str = "bar"
    status: str = "active"
    total_orders: int = 0
    total_revenue: float = 0
    last_order: Optional[str] = None
    kegs_out: int = 0
    credit_limit: float = 0
    payment_terms: str = "Net 30"
    notes: str = ""
    taps_carrying: list[Any] = []


class WholesaleAccountCreate(WholesaleAccountBase):
    pass


class WholesaleAccountUpdate(BaseModel):
    business_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    total_orders: Optional[int] = None
    total_revenue: Optional[float] = None
    last_order: Optional[str] = None
    kegs_out: Optional[int] = None
    credit_limit: Optional[float] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    taps_carrying: Optional[list[Any]] = None


class WholesaleAccountResponse(WholesaleAccountBase):
    id: UUID

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Wholesale Order
# ---------------------------------------------------------------------------

class WholesaleOrderBase(BaseModel):
    order_number: str
    account_id: UUID
    account_name: str = ""
    items: list[Any] = []
    total: float = 0
    status: str = "pending"
    order_date: Optional[str] = None
    delivery_date: Optional[str] = None
    payment_status: str = "current"
    notes: Optional[str] = None


class WholesaleOrderCreate(WholesaleOrderBase):
    pass


class WholesaleOrderUpdate(BaseModel):
    order_number: Optional[str] = None
    account_id: Optional[UUID] = None
    account_name: Optional[str] = None
    items: Optional[list[Any]] = None
    total: Optional[float] = None
    status: Optional[str] = None
    order_date: Optional[str] = None
    delivery_date: Optional[str] = None
    payment_status: Optional[str] = None
    notes: Optional[str] = None


class WholesaleOrderResponse(WholesaleOrderBase):
    id: UUID

    model_config = {"from_attributes": True}
