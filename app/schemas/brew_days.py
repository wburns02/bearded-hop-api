from __future__ import annotations
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel


class BrewDayBase(BaseModel):
    batch_id: UUID
    scheduled_date: date
    brewer_id: Optional[UUID] = None
    brewer_name: str = ""
    mash_temp_f: Optional[float] = None
    mash_duration_min: Optional[int] = None
    boil_duration_min: int = 60
    pre_boil_gravity: Optional[float] = None
    original_gravity: Optional[float] = None
    post_boil_volume_gal: Optional[float] = None
    notes: str = ""
    status: str = "scheduled"


class BrewDayCreate(BrewDayBase):
    pass


class BrewDayUpdate(BaseModel):
    batch_id: Optional[UUID] = None
    scheduled_date: Optional[date] = None
    brewer_id: Optional[UUID] = None
    brewer_name: Optional[str] = None
    mash_temp_f: Optional[float] = None
    mash_duration_min: Optional[int] = None
    boil_duration_min: Optional[int] = None
    pre_boil_gravity: Optional[float] = None
    original_gravity: Optional[float] = None
    post_boil_volume_gal: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None


class BrewDayResponse(BrewDayBase):
    id: UUID
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    created_at: Optional[datetime] = None
    batch_beer_name: Optional[str] = None
    batch_number: Optional[str] = None

    model_config = {"from_attributes": True}
