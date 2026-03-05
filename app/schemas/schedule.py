from __future__ import annotations

# dates stored as strings
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ShiftBase(BaseModel):
    staff_id: UUID
    staff_name: str = ""
    role: str = ""
    date: str
    day_of_week: str = ""
    start_time: str
    end_time: str
    hours: float = 0
    section: str = "taproom"
    status: str = "scheduled"
    notes: Optional[str] = None


class ShiftCreate(ShiftBase):
    pass


class ShiftUpdate(BaseModel):
    staff_id: Optional[UUID] = None
    staff_name: Optional[str] = None
    role: Optional[str] = None
    date: Optional[str] = None
    day_of_week: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    hours: Optional[float] = None
    section: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class ShiftResponse(ShiftBase):
    id: UUID

    model_config = {"from_attributes": True}
