from __future__ import annotations

from datetime import date
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class DetailedRecipeBase(BaseModel):
    beer_id: Optional[UUID] = None
    name: str
    style: str
    category: str = "flagship"
    version: int = 1
    batch_size: float = 0
    target_og: float = 0
    target_fg: float = 0
    target_abv: float = 0
    target_ibu: float = 0
    target_srm: float = 0
    boil_time: int = 60
    mash_temp: float = 152
    mash_time: int = 60
    grain_bill: list[Any] = []
    hop_schedule: list[Any] = []
    yeast: dict[str, Any] = {}
    water_profile: dict[str, Any] = {}
    water_adjustments: list[Any] = []
    brew_day_steps: list[Any] = []
    total_cost: float = 0
    cost_per_barrel: float = 0
    cost_per_pint: float = 0
    last_brewed: Optional[date] = None
    total_batches: int = 0
    brew_history: list[Any] = []
    notes: str = ""
    created_date: Optional[date] = None


class DetailedRecipeCreate(DetailedRecipeBase):
    pass


class DetailedRecipeUpdate(BaseModel):
    beer_id: Optional[UUID] = None
    name: Optional[str] = None
    style: Optional[str] = None
    category: Optional[str] = None
    version: Optional[int] = None
    batch_size: Optional[float] = None
    target_og: Optional[float] = None
    target_fg: Optional[float] = None
    target_abv: Optional[float] = None
    target_ibu: Optional[float] = None
    target_srm: Optional[float] = None
    boil_time: Optional[int] = None
    mash_temp: Optional[float] = None
    mash_time: Optional[int] = None
    grain_bill: Optional[list[Any]] = None
    hop_schedule: Optional[list[Any]] = None
    yeast: Optional[dict[str, Any]] = None
    water_profile: Optional[dict[str, Any]] = None
    water_adjustments: Optional[list[Any]] = None
    brew_day_steps: Optional[list[Any]] = None
    total_cost: Optional[float] = None
    cost_per_barrel: Optional[float] = None
    cost_per_pint: Optional[float] = None
    last_brewed: Optional[date] = None
    total_batches: Optional[int] = None
    brew_history: Optional[list[Any]] = None
    notes: Optional[str] = None
    created_date: Optional[date] = None


class DetailedRecipeResponse(DetailedRecipeBase):
    id: UUID

    model_config = {"from_attributes": True}
