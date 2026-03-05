from __future__ import annotations

from datetime import date
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class MugClubMemberBase(BaseModel):
    customer_id: Optional[UUID] = None
    customer_name: str = ""
    tier: str = "Standard"
    member_since: Optional[date] = None
    renewal_date: Optional[date] = None
    mug_number: int = 0
    mug_location: str = ""
    total_saved: float = 0
    visits_as_member: int = 0
    referrals: int = 0
    status: str = "active"
    benefits: list[Any] = []


class MugClubMemberCreate(MugClubMemberBase):
    pass


class MugClubMemberUpdate(BaseModel):
    customer_id: Optional[UUID] = None
    customer_name: Optional[str] = None
    tier: Optional[str] = None
    member_since: Optional[date] = None
    renewal_date: Optional[date] = None
    mug_number: Optional[int] = None
    mug_location: Optional[str] = None
    total_saved: Optional[float] = None
    visits_as_member: Optional[int] = None
    referrals: Optional[int] = None
    status: Optional[str] = None
    benefits: Optional[list[Any]] = None


class MugClubMemberResponse(MugClubMemberBase):
    id: UUID

    model_config = {"from_attributes": True}
