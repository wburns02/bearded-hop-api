from __future__ import annotations
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class QualityCheckBase(BaseModel):
    batch_id: UUID
    check_type: str
    value: str
    checked_by: str = ""
    notes: str = ""
    pass_fail: str = "na"


class QualityCheckCreate(QualityCheckBase):
    pass


class QualityCheckResponse(QualityCheckBase):
    id: UUID
    checked_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
