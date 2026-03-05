from fastapi import APIRouter
from sqlalchemy import select
from uuid import UUID
from typing import Optional
from pydantic import BaseModel

from app.api.deps import DbSession, CurrentUser
from app.models.keg import Keg
from app.models.keg_event import KegEvent
from app.exceptions import NotFoundError

router = APIRouter(prefix="/kegs", tags=["kegs"])


# ── Inline schemas (no dedicated keg schema file exists) ─────────────────────

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
    history: list[dict] = []


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
    history: Optional[list[dict]] = None


class KegResponse(KegBase):
    id: UUID

    model_config = {"from_attributes": True}


class KegEventBase(BaseModel):
    date: str
    type: str
    description: str = ""
    account_name: Optional[str] = None
    beer_name: Optional[str] = None
    performed_by: Optional[str] = None


class KegEventCreate(KegEventBase):
    pass


class KegEventResponse(KegEventBase):
    id: UUID
    keg_id: UUID

    model_config = {"from_attributes": True}


# ── Routes ───────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[KegResponse])
async def list_kegs(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Keg))
    return result.scalars().all()


@router.get("/{id}", response_model=KegResponse)
async def get_keg(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Keg).where(Keg.id == id))
    keg = result.scalar_one_or_none()
    if not keg:
        raise NotFoundError("Keg")
    return keg


@router.post("/", response_model=KegResponse, status_code=201)
async def create_keg(body: KegCreate, db: DbSession, current_user: CurrentUser):
    keg = Keg(**body.model_dump())
    db.add(keg)
    await db.commit()
    await db.refresh(keg)
    return keg


@router.patch("/{id}", response_model=KegResponse)
async def update_keg(id: UUID, body: KegUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Keg).where(Keg.id == id))
    keg = result.scalar_one_or_none()
    if not keg:
        raise NotFoundError("Keg")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(keg, field, value)
    await db.commit()
    await db.refresh(keg)
    return keg


@router.delete("/{id}", status_code=204)
async def delete_keg(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Keg).where(Keg.id == id))
    keg = result.scalar_one_or_none()
    if not keg:
        raise NotFoundError("Keg")
    await db.delete(keg)
    await db.commit()


@router.post("/{id}/events", response_model=KegEventResponse, status_code=201)
async def add_keg_event(id: UUID, body: KegEventCreate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Keg).where(Keg.id == id))
    if not result.scalar_one_or_none():
        raise NotFoundError("Keg")
    event = KegEvent(keg_id=id, **body.model_dump())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


@router.get("/{id}/events", response_model=list[KegEventResponse])
async def list_keg_events(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Keg).where(Keg.id == id))
    if not result.scalar_one_or_none():
        raise NotFoundError("Keg")
    events_result = await db.execute(select(KegEvent).where(KegEvent.keg_id == id))
    return events_result.scalars().all()
