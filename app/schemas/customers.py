from __future__ import annotations

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    anniversary: Optional[date] = None
    first_visit: Optional[date] = None
    last_visit: Optional[date] = None
    total_visits: int = 0
    total_spent: float = 0
    avg_ticket: float = 0
    favorite_beers: list[str] = []
    dietary_restrictions: list[str] = []
    tags: list[str] = []
    loyalty_points: int = 0
    loyalty_tier: str = "Bronze"
    mug_club_member: bool = False
    mug_club_tier: Optional[str] = None
    notes: str = ""
    source: str = ""
    family_members: list[str] = []


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    anniversary: Optional[date] = None
    first_visit: Optional[date] = None
    last_visit: Optional[date] = None
    total_visits: Optional[int] = None
    total_spent: Optional[float] = None
    avg_ticket: Optional[float] = None
    favorite_beers: Optional[list[str]] = None
    dietary_restrictions: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    loyalty_points: Optional[int] = None
    loyalty_tier: Optional[str] = None
    mug_club_member: Optional[bool] = None
    mug_club_tier: Optional[str] = None
    notes: Optional[str] = None
    source: Optional[str] = None
    family_members: Optional[list[str]] = None


class CustomerResponse(CustomerBase):
    id: UUID

    model_config = {"from_attributes": True}
