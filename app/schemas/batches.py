from __future__ import annotations

# dates stored as strings
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GravityReadingCreate(BaseModel):
    date: str
    gravity: float
    temp: float


class BatchBase(BaseModel):
    batch_number: str
    beer_id: Optional[UUID] = None
    beer_name: str = ""
    style: str = ""
    recipe_id: Optional[UUID] = None
    status: str = "planned"
    brew_date: Optional[str] = None
    target_og: float = 0
    actual_og: Optional[float] = None
    target_fg: float = 0
    actual_fg: Optional[float] = None
    abv: Optional[float] = None
    tank_id: str = ""
    volume: float = 0
    notes: str = ""
    gravity_readings: list[dict] = []
    temperature_log: list[dict] = []
    quality_score: Optional[float] = None


class BatchCreate(BatchBase):
    pass


class BatchUpdate(BaseModel):
    batch_number: Optional[str] = None
    beer_id: Optional[UUID] = None
    beer_name: Optional[str] = None
    style: Optional[str] = None
    recipe_id: Optional[UUID] = None
    status: Optional[str] = None
    brew_date: Optional[str] = None
    target_og: Optional[float] = None
    actual_og: Optional[float] = None
    target_fg: Optional[float] = None
    actual_fg: Optional[float] = None
    abv: Optional[float] = None
    tank_id: Optional[str] = None
    volume: Optional[float] = None
    notes: Optional[str] = None
    gravity_readings: Optional[list[dict]] = None
    temperature_log: Optional[list[dict]] = None
    quality_score: Optional[float] = None


class BatchResponse(BatchBase):
    id: UUID

    model_config = {"from_attributes": True}
