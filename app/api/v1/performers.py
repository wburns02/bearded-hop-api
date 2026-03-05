from fastapi import APIRouter
from sqlalchemy import select
from uuid import UUID

from app.api.deps import DbSession, CurrentUser
from app.models.performer import Performer
from app.schemas.performers import PerformerCreate, PerformerUpdate, PerformerResponse
from app.exceptions import NotFoundError

router = APIRouter(prefix="/performers", tags=["performers"])


@router.get("/", response_model=list[PerformerResponse])
async def list_performers(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Performer))
    return result.scalars().all()


@router.get("/{id}", response_model=PerformerResponse)
async def get_performer(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Performer).where(Performer.id == id))
    performer = result.scalar_one_or_none()
    if not performer:
        raise NotFoundError("Performer")
    return performer


@router.post("/", response_model=PerformerResponse, status_code=201)
async def create_performer(body: PerformerCreate, db: DbSession, current_user: CurrentUser):
    performer = Performer(**body.model_dump())
    db.add(performer)
    await db.commit()
    await db.refresh(performer)
    return performer


@router.patch("/{id}", response_model=PerformerResponse)
async def update_performer(id: UUID, body: PerformerUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Performer).where(Performer.id == id))
    performer = result.scalar_one_or_none()
    if not performer:
        raise NotFoundError("Performer")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(performer, field, value)
    await db.commit()
    await db.refresh(performer)
    return performer


@router.delete("/{id}", status_code=204)
async def delete_performer(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Performer).where(Performer.id == id))
    performer = result.scalar_one_or_none()
    if not performer:
        raise NotFoundError("Performer")
    await db.delete(performer)
    await db.commit()
