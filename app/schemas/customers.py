from __future__ import annotations

# dates stored as strings
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    anniversary: Optional[str] = None
    first_visit: Optional[str] = None
    last_visit: Optional[str] = None
    total_visits: int = 0
    total_spent: float = 0
    avg_ticket: float = 0
    favorite_beers: list = []
    dietary_restrictions: list = []
    tags: list = []
    loyalty_points: int = 0
    loyalty_tier: str = "Bronze"
    mug_club_member: bool = False
    mug_club_tier: Optional[str] = None
    notes: Optional[str] = ""
    source: Optional[str] = ""
    family_members: list = []


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    anniversary: Optional[str] = None
    first_visit: Optional[str] = None
    last_visit: Optional[str] = None
    total_visits: Optional[int] = None
    total_spent: Optional[float] = None
    avg_ticket: Optional[float] = None
    favorite_beers: Optional[list] = None
    dietary_restrictions: Optional[list] = None
    tags: Optional[list] = None
    loyalty_points: Optional[int] = None
    loyalty_tier: Optional[str] = None
    mug_club_member: Optional[bool] = None
    mug_club_tier: Optional[str] = None
    notes: Optional[str] = None
    source: Optional[str] = None
    family_members: Optional[list] = None


class CustomerResponse(CustomerBase):
    id: UUID

    model_config = {"from_attributes": True}
