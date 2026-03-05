from __future__ import annotations

# dates stored as strings
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Floor Table
# ---------------------------------------------------------------------------

class FloorTableBase(BaseModel):
    zone: str
    label: str
    seats: int = 4
    x: float = 0
    y: float = 0
    shape: str = "rect"
    width: Optional[float] = None
    height: Optional[float] = None
    radius: Optional[float] = None
    status: str = "available"
    current_tab_id: Optional[UUID] = None
    current_customer_name: Optional[str] = None
    current_customer_id: Optional[UUID] = None
    party_size: Optional[int] = None
    server_id: Optional[UUID] = None
    server_name: Optional[str] = None
    seated_at: Optional[str] = None
    reservation_id: Optional[UUID] = None


class FloorTableUpdate(BaseModel):
    zone: Optional[str] = None
    label: Optional[str] = None
    seats: Optional[int] = None
    x: Optional[float] = None
    y: Optional[float] = None
    shape: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    radius: Optional[float] = None
    status: Optional[str] = None
    current_tab_id: Optional[UUID] = None
    current_customer_name: Optional[str] = None
    current_customer_id: Optional[UUID] = None
    party_size: Optional[int] = None
    server_id: Optional[UUID] = None
    server_name: Optional[str] = None
    seated_at: Optional[str] = None
    reservation_id: Optional[UUID] = None


class FloorTableResponse(FloorTableBase):
    id: str

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Seat Guests Request
# ---------------------------------------------------------------------------

class SeatGuestsRequest(BaseModel):
    customer_name: str
    party_size: int = 1
    server_id: Optional[UUID] = None
    server_name: Optional[str] = None
    customer_id: Optional[UUID] = None


# ---------------------------------------------------------------------------
# Service Alert
# ---------------------------------------------------------------------------

class ServiceAlertBase(BaseModel):
    table_id: str
    type: str
    message: str = ""
    priority: str = "medium"
    created_at: Optional[str] = None


class ServiceAlertCreate(ServiceAlertBase):
    pass


class ServiceAlertResponse(ServiceAlertBase):
    id: UUID

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Order Timeline
# ---------------------------------------------------------------------------

class OrderTimelineResponse(BaseModel):
    id: UUID
    table_id: str
    time: str
    action: str
    description: str = ""

    model_config = {"from_attributes": True}
