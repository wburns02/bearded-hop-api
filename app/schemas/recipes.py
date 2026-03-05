from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class RecipeBase(BaseModel):
    name: str
    style: str
    batch_size: float = 0
    og: float = 0
    fg: float = 0
    abv: float = 0
    ibu: int = 0
    srm: int = 0
    grains: list[dict] = []
    hops: list[dict] = []
    yeast: str = ""
    water_profile: str = ""
    mash_temp: float = 0
    mash_time: int = 0
    boil_time: int = 0
    notes: str = ""
    versions: int = 1


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    style: Optional[str] = None
    batch_size: Optional[float] = None
    og: Optional[float] = None
    fg: Optional[float] = None
    abv: Optional[float] = None
    ibu: Optional[int] = None
    srm: Optional[int] = None
    grains: Optional[list[dict]] = None
    hops: Optional[list[dict]] = None
    yeast: Optional[str] = None
    water_profile: Optional[str] = None
    mash_temp: Optional[float] = None
    mash_time: Optional[int] = None
    boil_time: Optional[int] = None
    notes: Optional[str] = None
    versions: Optional[int] = None


class RecipeResponse(RecipeBase):
    id: UUID

    model_config = {"from_attributes": True}
