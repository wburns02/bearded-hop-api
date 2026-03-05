from __future__ import annotations
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class VesselBase(BaseModel):
    name: str
    vessel_type: str = "fermenter"
    capacity_bbl: float = 7.0
    current_batch_id: Optional[UUID] = None
    status: str = "empty"
    temperature_f: Optional[float] = None
    pressure_psi: Optional[float] = None
    notes: str = ""


class VesselCreate(VesselBase):
    pass


class VesselUpdate(BaseModel):
    name: Optional[str] = None
    vessel_type: Optional[str] = None
    capacity_bbl: Optional[float] = None
    current_batch_id: Optional[UUID] = None
    status: Optional[str] = None
    temperature_f: Optional[float] = None
    pressure_psi: Optional[float] = None
    notes: Optional[str] = None


class VesselResponse(VesselBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    batch_name: Optional[str] = None
    batch_status: Optional[str] = None
    batch_beer_name: Optional[str] = None
    batch_brew_date: Optional[str] = None
    batch_style: Optional[str] = None

    model_config = {"from_attributes": True}


class VesselReadingCreate(BaseModel):
    temperature_f: Optional[float] = None
    pressure_psi: Optional[float] = None
    gravity: Optional[float] = None
    checked_by: str = ""
    notes: str = ""
