from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PerformerBase(BaseModel):
    name: str
    genre: str = ""
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    fee: float = 0
    rating: float = 0
    past_performances: int = 0
    bio: str = ""
    social_links: list = []


class PerformerCreate(PerformerBase):
    pass


class PerformerUpdate(BaseModel):
    name: Optional[str] = None
    genre: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    fee: Optional[float] = None
    rating: Optional[float] = None
    past_performances: Optional[int] = None
    bio: Optional[str] = None
    social_links: Optional[list] = None


class PerformerResponse(PerformerBase):
    id: UUID

    model_config = {"from_attributes": True}
