from fastapi import APIRouter
from sqlalchemy import select
from uuid import UUID

from app.api.deps import DbSession, CurrentUser
from app.models.event import Event
from app.schemas.events import EventCreate, EventUpdate, EventResponse
from app.exceptions import NotFoundError

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=list[EventResponse])
async def list_events(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Event))
    return result.scalars().all()


@router.get("/{id}", response_model=EventResponse)
async def get_event(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Event).where(Event.id == id))
    event = result.scalar_one_or_none()
    if not event:
        raise NotFoundError("Event")
    return event


@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(body: EventCreate, db: DbSession, current_user: CurrentUser):
    event = Event(**body.model_dump())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


@router.patch("/{id}", response_model=EventResponse)
async def update_event(id: UUID, body: EventUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Event).where(Event.id == id))
    event = result.scalar_one_or_none()
    if not event:
        raise NotFoundError("Event")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    await db.commit()
    await db.refresh(event)
    return event


@router.delete("/{id}", status_code=204)
async def delete_event(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Event).where(Event.id == id))
    event = result.scalar_one_or_none()
    if not event:
        raise NotFoundError("Event")
    await db.delete(event)
    await db.commit()
