from __future__ import annotations

# dates stored as strings
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class KegBase(BaseModel):
    keg_number: str
    size: str
    gallons: float = 0
    status: str = "clean-empty"
    current_beer_id: Optional[UUID] = None
    current_beer_name: Optional[str] = None
    batch_id: Optional[UUID] = None
    location: str = "brewery-cold-room"
    deployed_to: Optional[str] = None
    deployed_to_name: Optional[str] = None
    deployed_date: Optional[str] = None
    expected_return_date: Optional[str] = None
    fill_date: Optional[str] = None
    fill_count: int = 0
    last_cleaned: Optional[str] = None
    deposit: float = 0
    deposit_status: str = "not-applicable"
    purchase_date: Optional[str] = None
    purchase_cost: float = 0
    notes: str = ""
    history: list[Any] = []


class KegCreate(KegBase):
    pass


class KegUpdate(BaseModel):
    keg_number: Optional[str] = None
    size: Optional[str] = None
    gallons: Optional[float] = None
    status: Optional[str] = None
    current_beer_id: Optional[UUID] = None
    current_beer_name: Optional[str] = None
    batch_id: Optional[UUID] = None
    location: Optional[str] = None
    deployed_to: Optional[str] = None
    deployed_to_name: Optional[str] = None
    deployed_date: Optional[str] = None
    expected_return_date: Optional[str] = None
    fill_date: Optional[str] = None
    fill_count: Optional[int] = None
    last_cleaned: Optional[str] = None
    deposit: Optional[float] = None
    deposit_status: Optional[str] = None
    purchase_date: Optional[str] = None
    purchase_cost: Optional[float] = None
    notes: Optional[str] = None
    history: Optional[list[Any]] = None


class KegResponse(KegBase):
    id: UUID

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Keg Event
# ---------------------------------------------------------------------------

class KegEventCreate(BaseModel):
    date: str
    type: str
    description: str = ""
    account_name: Optional[str] = None
    beer_name: Optional[str] = None
    performed_by: Optional[str] = None


class KegEventResponse(BaseModel):
    id: UUID
    keg_id: UUID
    date: str
    type: str
    description: str
    account_name: Optional[str] = None
    beer_name: Optional[str] = None
    performed_by: Optional[str] = None

    model_config = {"from_attributes": True}
