from __future__ import annotations

# dates stored as strings
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TapLineBase(BaseModel):
    tap_number: int
    beer_id: Optional[UUID] = None
    beer_name: Optional[str] = None
    style: Optional[str] = None
    abv: Optional[float] = None
    ibu: Optional[int] = None
    keg_level: float = 100
    keg_size: str = "1/2"
    tapped_date: Optional[str] = None
    estimated_kick_date: Optional[str] = None
    status: str = "active"
    pour_sizes: list[dict] = []
    total_pours: int = 0
    revenue_today: float = 0


class TapLineUpdate(BaseModel):
    tap_number: Optional[int] = None
    beer_id: Optional[UUID] = None
    beer_name: Optional[str] = None
    style: Optional[str] = None
    abv: Optional[float] = None
    ibu: Optional[int] = None
    keg_level: Optional[float] = None
    keg_size: Optional[str] = None
    tapped_date: Optional[str] = None
    estimated_kick_date: Optional[str] = None
    status: Optional[str] = None
    pour_sizes: Optional[list[dict]] = None
    total_pours: Optional[int] = None
    revenue_today: Optional[float] = None


class TapLineResponse(TapLineBase):
    model_config = {"from_attributes": True}
