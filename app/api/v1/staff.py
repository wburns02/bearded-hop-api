from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.staff_member import StaffMember
from app.models.staff_certification import StaffCertification
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse

router = APIRouter(prefix="/staff", tags=["staff"])


@router.get("/", response_model=list[StaffResponse])
async def list_staff(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(StaffMember))
    return result.scalars().all()


@router.post("/", response_model=StaffResponse)
async def create_staff_member(body: StaffCreate, db: DbSession, current_user: CurrentUser):
    member = StaffMember(**body.model_dump())
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member


@router.get("/certifications")
async def list_certifications(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(StaffCertification))
    certs = result.scalars().all()
    return [
        {
            "id": str(c.id),
            "staff_id": str(c.staff_id),
            "staff_name": c.staff_name,
            "type": c.type,
            "status": c.status,
            "issue_date": c.issue_date,
            "expiry_date": c.expiry_date,
            "days_until_expiry": c.days_until_expiry,
        }
        for c in certs
    ]


@router.get("/{id}", response_model=StaffResponse)
async def get_staff_member(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(StaffMember).where(StaffMember.id == id))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return member


@router.patch("/{id}", response_model=StaffResponse)
async def update_staff_member(id: UUID, body: StaffUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(StaffMember).where(StaffMember.id == id))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    await db.commit()
    await db.refresh(member)
    return member


@router.delete("/{id}")
async def delete_staff_member(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(StaffMember).where(StaffMember.id == id))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    await db.delete(member)
    await db.commit()
    return {"message": "Deleted"}
