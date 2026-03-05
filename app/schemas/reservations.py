from __future__ import annotations

from datetime import date, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class ReservationBase(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    date: date
    time: time
    party_size: int = 1
    table_id: Optional[str] = None
    section: str = "taproom"
    status: str = "confirmed"
    notes: str = ""
    special_requests: list[str] = []
    is_high_chair_needed: bool = False


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    date: Optional[date] = None
    time: Optional[time] = None
    party_size: Optional[int] = None
    table_id: Optional[str] = None
    section: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    special_requests: Optional[list[str]] = None
    is_high_chair_needed: Optional[bool] = None


class ReservationResponse(ReservationBase):
    id: UUID

    model_config = {"from_attributes": True}
