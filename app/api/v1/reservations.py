from fastapi import APIRouter
from sqlalchemy import select
from uuid import UUID

from app.api.deps import DbSession, CurrentUser
from app.models.reservation import Reservation
from app.schemas.reservations import ReservationCreate, ReservationUpdate, ReservationResponse
from app.exceptions import NotFoundError

router = APIRouter(prefix="/reservations", tags=["reservations"])

# Valid status values and allowed transitions
VALID_STATUSES = {"confirmed", "pending", "seated", "completed", "cancelled", "no-show"}


@router.get("/", response_model=list[ReservationResponse])
async def list_reservations(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Reservation))
    return result.scalars().all()


@router.get("/{id}", response_model=ReservationResponse)
async def get_reservation(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Reservation).where(Reservation.id == id))
    reservation = result.scalar_one_or_none()
    if not reservation:
        raise NotFoundError("Reservation")
    return reservation


@router.post("/", response_model=ReservationResponse, status_code=201)
async def create_reservation(body: ReservationCreate, db: DbSession, current_user: CurrentUser):
    reservation = Reservation(**body.model_dump())
    db.add(reservation)
    await db.commit()
    await db.refresh(reservation)
    return reservation


@router.patch("/{id}", response_model=ReservationResponse)
async def update_reservation(id: UUID, body: ReservationUpdate, db: DbSession, current_user: CurrentUser):
    """Update reservation fields. When status is included, validates it is a known status."""
    result = await db.execute(select(Reservation).where(Reservation.id == id))
    reservation = result.scalar_one_or_none()
    if not reservation:
        raise NotFoundError("Reservation")

    updates = body.model_dump(exclude_unset=True)

    if "status" in updates and updates["status"] not in VALID_STATUSES:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{updates['status']}'. Valid values: {sorted(VALID_STATUSES)}",
        )

    for field, value in updates.items():
        setattr(reservation, field, value)

    await db.commit()
    await db.refresh(reservation)
    return reservation


@router.delete("/{id}", status_code=204)
async def delete_reservation(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Reservation).where(Reservation.id == id))
    reservation = result.scalar_one_or_none()
    if not reservation:
        raise NotFoundError("Reservation")
    await db.delete(reservation)
    await db.commit()
