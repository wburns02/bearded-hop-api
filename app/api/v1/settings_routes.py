from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.business_settings import BusinessSettings
from app.models.compliance_item import ComplianceItem
from app.schemas.settings import (
    BusinessSettingsResponse,
    BusinessSettingsUpdate,
    ComplianceItemCreate,
    ComplianceItemUpdate,
    ComplianceItemResponse,
)

router = APIRouter(prefix="/settings", tags=["settings"])


# ---------------------------------------------------------------------------
# Business Settings (single-row)
# ---------------------------------------------------------------------------

@router.get("/", response_model=BusinessSettingsResponse)
async def get_settings(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(BusinessSettings))
    settings = result.scalar_one_or_none()
    if not settings:
        settings = BusinessSettings()
        db.add(settings)
        await db.commit()
        await db.refresh(settings)
    return settings


@router.patch("/", response_model=BusinessSettingsResponse)
async def update_settings(body: BusinessSettingsUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(BusinessSettings))
    settings = result.scalar_one_or_none()
    if not settings:
        settings = BusinessSettings()
        db.add(settings)
        await db.flush()
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(settings, field, value)
    await db.commit()
    await db.refresh(settings)
    return settings


# ---------------------------------------------------------------------------
# Compliance Items
# ---------------------------------------------------------------------------

@router.get("/compliance", response_model=list[ComplianceItemResponse])
async def list_compliance_items(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(ComplianceItem))
    return result.scalars().all()


@router.post("/compliance", response_model=ComplianceItemResponse)
async def create_compliance_item(body: ComplianceItemCreate, db: DbSession, current_user: CurrentUser):
    data = body.model_dump()
    if data.get("due_date") is not None:
        data["due_date"] = str(data["due_date"])
    if data.get("last_completed") is not None:
        data["last_completed"] = str(data["last_completed"])
    item = ComplianceItem(**data)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.patch("/compliance/{id}", response_model=ComplianceItemResponse)
async def update_compliance_item(id: UUID, body: ComplianceItemUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(ComplianceItem).where(ComplianceItem.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Compliance item not found")
    data = body.model_dump(exclude_unset=True)
    for field in ("due_date", "last_completed"):
        if field in data and data[field] is not None:
            data[field] = str(data[field])
    for field, value in data.items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item
