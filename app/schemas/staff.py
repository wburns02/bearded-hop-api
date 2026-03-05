from __future__ import annotations

from datetime import date
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class StaffBase(BaseModel):
    first_name: str
    last_name: str
    role: str
    email: Optional[str] = None
    phone: Optional[str] = None
    hire_date: Optional[date] = None
    hourly_rate: float = 0
    status: str = "active"
    tabc_certified: bool = False
    tabc_expiry: Optional[date] = None
    food_handler_certified: bool = False
    food_handler_expiry: Optional[date] = None
    hours_this_week: float = 0
    sales_this_week: float = 0
    avatar: Optional[str] = None
    schedule: list[Any] = []


class StaffCreate(StaffBase):
    pass


class StaffUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    hire_date: Optional[date] = None
    hourly_rate: Optional[float] = None
    status: Optional[str] = None
    tabc_certified: Optional[bool] = None
    tabc_expiry: Optional[date] = None
    food_handler_certified: Optional[bool] = None
    food_handler_expiry: Optional[date] = None
    hours_this_week: Optional[float] = None
    sales_this_week: Optional[float] = None
    avatar: Optional[str] = None
    schedule: Optional[list[Any]] = None


class StaffResponse(StaffBase):
    id: UUID

    model_config = {"from_attributes": True}
