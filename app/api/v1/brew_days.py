from fastapi import APIRouter, Query
from sqlalchemy import select
from uuid import UUID
from datetime import date
from typing import Optional

from app.api.deps import DbSession, CurrentUser
from app.models.brew_day_log import BrewDayLog
from app.models.batch import Batch
from app.schemas.brew_days import BrewDayCreate, BrewDayUpdate, BrewDayResponse
from app.exceptions import NotFoundError

router = APIRouter(prefix="/brew-days", tags=["brew-days"])


async def _enrich(log: BrewDayLog, db) -> dict:
    data = {c.key: getattr(log, c.key) for c in log.__table__.columns}
    result = await db.execute(select(Batch).where(Batch.id == log.batch_id))
    batch = result.scalar_one_or_none()
    if batch:
        data["batch_beer_name"] = batch.beer_name
        data["batch_number"] = batch.batch_number
    return data


@router.get("/", response_model=list[BrewDayResponse])
async def list_brew_days(
    db: DbSession,
    current_user: CurrentUser,
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
):
    q = select(BrewDayLog)
    if start:
        q = q.where(BrewDayLog.scheduled_date >= start)
    if end:
        q = q.where(BrewDayLog.scheduled_date <= end)
    q = q.order_by(BrewDayLog.scheduled_date)
    result = await db.execute(q)
    logs = result.scalars().all()
    return [await _enrich(log, db) for log in logs]


@router.get("/{id}", response_model=BrewDayResponse)
async def get_brew_day(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(BrewDayLog).where(BrewDayLog.id == id))
    log = result.scalar_one_or_none()
    if not log:
        raise NotFoundError("BrewDayLog")
    return await _enrich(log, db)


@router.post("/", response_model=BrewDayResponse, status_code=201)
async def create_brew_day(body: BrewDayCreate, db: DbSession, current_user: CurrentUser):
    log = BrewDayLog(**body.model_dump())
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return await _enrich(log, db)


@router.patch("/{id}", response_model=BrewDayResponse)
async def update_brew_day(id: UUID, body: BrewDayUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(BrewDayLog).where(BrewDayLog.id == id))
    log = result.scalar_one_or_none()
    if not log:
        raise NotFoundError("BrewDayLog")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(log, field, value)
    await db.commit()
    await db.refresh(log)
    return await _enrich(log, db)


@router.delete("/{id}", status_code=204)
async def delete_brew_day(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(BrewDayLog).where(BrewDayLog.id == id))
    log = result.scalar_one_or_none()
    if not log:
        raise NotFoundError("BrewDayLog")
    await db.delete(log)
    await db.commit()
