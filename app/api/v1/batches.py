from fastapi import APIRouter
from sqlalchemy import select
from uuid import UUID
from pydantic import BaseModel
from datetime import date

from app.api.deps import DbSession, CurrentUser
from app.models.batch import Batch
from app.schemas.batches import BatchCreate, BatchUpdate, BatchResponse, GravityReadingCreate
from app.exceptions import NotFoundError

router = APIRouter(prefix="/batches", tags=["batches"])

# Ordered status progression for batches
STATUS_PROGRESSION = [
    "planned",
    "mashing",
    "boiling",
    "fermenting",
    "conditioning",
    "carbonating",
    "ready",
    "packaged",
]


@router.get("/", response_model=list[BatchResponse])
async def list_batches(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Batch))
    return result.scalars().all()


@router.get("/{id}", response_model=BatchResponse)
async def get_batch(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Batch).where(Batch.id == id))
    batch = result.scalar_one_or_none()
    if not batch:
        raise NotFoundError("Batch")
    return batch


@router.post("/", response_model=BatchResponse, status_code=201)
async def create_batch(body: BatchCreate, db: DbSession, current_user: CurrentUser):
    batch = Batch(**body.model_dump())
    db.add(batch)
    await db.commit()
    await db.refresh(batch)
    return batch


@router.patch("/{id}", response_model=BatchResponse)
async def update_batch(id: UUID, body: BatchUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Batch).where(Batch.id == id))
    batch = result.scalar_one_or_none()
    if not batch:
        raise NotFoundError("Batch")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(batch, field, value)
    await db.commit()
    await db.refresh(batch)
    return batch


@router.delete("/{id}", status_code=204)
async def delete_batch(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Batch).where(Batch.id == id))
    batch = result.scalar_one_or_none()
    if not batch:
        raise NotFoundError("Batch")
    await db.delete(batch)
    await db.commit()


@router.post("/{id}/advance-status", response_model=BatchResponse)
async def advance_batch_status(id: UUID, db: DbSession, current_user: CurrentUser):
    """Advance the batch through the standard status progression."""
    result = await db.execute(select(Batch).where(Batch.id == id))
    batch = result.scalar_one_or_none()
    if not batch:
        raise NotFoundError("Batch")

    current_status = batch.status
    if current_status not in STATUS_PROGRESSION:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail=f"Unknown status '{current_status}'. Cannot advance.",
        )

    current_index = STATUS_PROGRESSION.index(current_status)
    if current_index >= len(STATUS_PROGRESSION) - 1:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail=f"Batch is already at the final status '{current_status}'.",
        )

    batch.status = STATUS_PROGRESSION[current_index + 1]
    await db.commit()
    await db.refresh(batch)
    return batch


@router.post("/{id}/gravity-readings", response_model=BatchResponse, status_code=201)
async def add_gravity_reading(
    id: UUID,
    body: GravityReadingCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Append a gravity reading to the batch's gravity_readings JSON array."""
    result = await db.execute(select(Batch).where(Batch.id == id))
    batch = result.scalar_one_or_none()
    if not batch:
        raise NotFoundError("Batch")

    readings = list(batch.gravity_readings or [])
    readings.append(body.model_dump(mode="json"))
    batch.gravity_readings = readings
    await db.commit()
    await db.refresh(batch)
    return batch
