from __future__ import annotations

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Business Settings
# ---------------------------------------------------------------------------

class BusinessSettingsBase(BaseModel):
    business_name: str = "Bearded Hop Brewery"
    address: str = ""
    phone: str = ""
    email: str = ""
    tax_rate: str = "8.25%"
    timezone: str = "America/Chicago (CST)"
    currency: str = "USD"


class BusinessSettingsUpdate(BaseModel):
    business_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_rate: Optional[str] = None
    timezone: Optional[str] = None
    currency: Optional[str] = None


class BusinessSettingsResponse(BusinessSettingsBase):
    id: UUID

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Compliance Item
# ---------------------------------------------------------------------------

class ComplianceItemBase(BaseModel):
    type: str
    name: str
    status: str = "compliant"
    due_date: Optional[date] = None
    last_completed: Optional[date] = None
    notes: str = ""


class ComplianceItemCreate(ComplianceItemBase):
    pass


class ComplianceItemUpdate(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None
    last_completed: Optional[date] = None
    notes: Optional[str] = None


class ComplianceItemResponse(ComplianceItemBase):
    id: UUID

    model_config = {"from_attributes": True}
