from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class MenuItemBase(BaseModel):
    name: str
    description: str = ""
    category: str
    price: float = 0
    cost: float = 0
    is_available: bool = True
    allergens: list[str] = []
    dietary_tags: list[str] = []
    is_kids_friendly: bool = False
    popularity: int = 0
    image_url: Optional[str] = None


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    is_available: Optional[bool] = None
    allergens: Optional[list[str]] = None
    dietary_tags: Optional[list[str]] = None
    is_kids_friendly: Optional[bool] = None
    popularity: Optional[int] = None
    image_url: Optional[str] = None


class MenuItemResponse(MenuItemBase):
    id: UUID

    model_config = {"from_attributes": True}
