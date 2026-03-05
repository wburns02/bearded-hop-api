from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BeerBase(BaseModel):
    name: str
    style: str
    abv: float
    ibu: int = 0
    srm: int = 0
    description: str = ""
    tasting_notes: str = ""
    food_pairings: list[str] = []
    status: str = "planned"
    tap_number: Optional[int] = None
    keg_level: Optional[float] = None
    batch_id: Optional[UUID] = None
    rating: float = 0
    total_pours: int = 0
    category: str = "flagship"
    is_non_alcoholic: bool = False


class BeerCreate(BeerBase):
    pass


class BeerUpdate(BaseModel):
    name: Optional[str] = None
    style: Optional[str] = None
    abv: Optional[float] = None
    ibu: Optional[int] = None
    srm: Optional[int] = None
    description: Optional[str] = None
    tasting_notes: Optional[str] = None
    food_pairings: Optional[list[str]] = None
    status: Optional[str] = None
    tap_number: Optional[int] = None
    keg_level: Optional[float] = None
    batch_id: Optional[UUID] = None
    rating: Optional[float] = None
    total_pours: Optional[int] = None
    category: Optional[str] = None
    is_non_alcoholic: Optional[bool] = None


class BeerResponse(BeerBase):
    id: UUID

    model_config = {"from_attributes": True}
