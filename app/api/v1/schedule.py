from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.schedule_shift import ScheduleShift
from app.models.staff_member import StaffMember
from app.schemas.schedule import ShiftCreate, ShiftUpdate, ShiftResponse

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("/", response_model=list[ShiftResponse])
async def list_shifts(db: DbSession, current_user: CurrentUser, date: Optional[str] = None):
    stmt = select(ScheduleShift)
    if date:
        stmt = stmt.where(ScheduleShift.date == date)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/", response_model=ShiftResponse)
async def create_shift(body: ShiftCreate, db: DbSession, current_user: CurrentUser):
    data = body.model_dump()
    # Convert date/time objects to strings for storage
    data["date"] = str(data["date"])
    data["start_time"] = str(data["start_time"])
    data["end_time"] = str(data["end_time"])
    shift = ScheduleShift(**data)
    db.add(shift)
    await db.commit()
    await db.refresh(shift)
    return shift


@router.get("/labor-costs")
async def get_labor_costs(db: DbSession, current_user: CurrentUser):
    shifts_result = await db.execute(select(ScheduleShift))
    shifts = shifts_result.scalars().all()

    staff_result = await db.execute(select(StaffMember))
    staff_list = staff_result.scalars().all()
    staff_map = {str(s.id): s for s in staff_list}

    output = []
    for shift in shifts:
        staff = staff_map.get(str(shift.staff_id))
        hourly_rate = staff.hourly_rate if staff else 0
        labor_cost = shift.hours * hourly_rate
        output.append(
            {
                "id": str(shift.id),
                "staff_id": str(shift.staff_id),
                "staff_name": shift.staff_name,
                "role": shift.role,
                "date": shift.date,
                "start_time": shift.start_time,
                "end_time": shift.end_time,
                "hours": shift.hours,
                "hourly_rate": hourly_rate,
                "labor_cost": labor_cost,
                "section": shift.section,
                "status": shift.status,
            }
        )
    return output


@router.get("/{id}", response_model=ShiftResponse)
async def get_shift(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(ScheduleShift).where(ScheduleShift.id == id))
    shift = result.scalar_one_or_none()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift


@router.patch("/{id}", response_model=ShiftResponse)
async def update_shift(id: UUID, body: ShiftUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(ScheduleShift).where(ScheduleShift.id == id))
    shift = result.scalar_one_or_none()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    data = body.model_dump(exclude_unset=True)
    for field, value in data.items():
        if field in ("date", "start_time", "end_time") and value is not None:
            value = str(value)
        setattr(shift, field, value)
    await db.commit()
    await db.refresh(shift)
    return shift


@router.delete("/{id}")
async def delete_shift(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(ScheduleShift).where(ScheduleShift.id == id))
    shift = result.scalar_one_or_none()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    await db.delete(shift)
    await db.commit()
    return {"message": "Deleted"}
