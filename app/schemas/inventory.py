from __future__ import annotations

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class InventoryItemBase(BaseModel):
    name: str
    category: str
    current_stock: float = 0
    unit: str = ""
    par_level: float = 0
    reorder_point: float = 0
    cost_per_unit: float = 0
    supplier: str = ""
    last_ordered: Optional[date] = None
    expiration_date: Optional[date] = None
    location: str = ""


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    current_stock: Optional[float] = None
    unit: Optional[str] = None
    par_level: Optional[float] = None
    reorder_point: Optional[float] = None
    cost_per_unit: Optional[float] = None
    supplier: Optional[str] = None
    last_ordered: Optional[date] = None
    expiration_date: Optional[date] = None
    location: Optional[str] = None


class InventoryItemResponse(InventoryItemBase):
    id: UUID

    model_config = {"from_attributes": True}


class PurchaseOrderBase(BaseModel):
    po_number: str
    supplier: str
    items: list[dict] = []
    total_cost: float = 0
    status: str = "draft"
    order_date: Optional[date] = None
    eta: Optional[date] = None
    received_date: Optional[date] = None
    notes: Optional[str] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    pass


class PurchaseOrderUpdate(BaseModel):
    po_number: Optional[str] = None
    supplier: Optional[str] = None
    items: Optional[list[dict]] = None
    total_cost: Optional[float] = None
    status: Optional[str] = None
    order_date: Optional[date] = None
    eta: Optional[date] = None
    received_date: Optional[date] = None
    notes: Optional[str] = None


class PurchaseOrderResponse(PurchaseOrderBase):
    id: UUID

    model_config = {"from_attributes": True}
