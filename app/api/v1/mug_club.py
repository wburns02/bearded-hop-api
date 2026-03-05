from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.mug_club_member import MugClubMember
from app.schemas.mug_club import MugClubMemberCreate, MugClubMemberUpdate, MugClubMemberResponse

router = APIRouter(prefix="/mug-club", tags=["mug-club"])


@router.get("/", response_model=list[MugClubMemberResponse])
async def list_members(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(MugClubMember))
    return result.scalars().all()


@router.post("/", response_model=MugClubMemberResponse)
async def create_member(body: MugClubMemberCreate, db: DbSession, current_user: CurrentUser):
    data = body.model_dump()
    if data.get("customer_id"):
        data["customer_id"] = str(data["customer_id"])
    member = MugClubMember(**data)
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member


@router.get("/{id}", response_model=MugClubMemberResponse)
async def get_member(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(MugClubMember).where(MugClubMember.id == id))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Mug club member not found")
    return member


@router.patch("/{id}", response_model=MugClubMemberResponse)
async def update_member(id: UUID, body: MugClubMemberUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(MugClubMember).where(MugClubMember.id == id))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Mug club member not found")
    data = body.model_dump(exclude_unset=True)
    if "customer_id" in data and data["customer_id"] is not None:
        data["customer_id"] = str(data["customer_id"])
    for field, value in data.items():
        setattr(member, field, value)
    await db.commit()
    await db.refresh(member)
    return member


@router.delete("/{id}")
async def delete_member(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(MugClubMember).where(MugClubMember.id == id))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Mug club member not found")
    await db.delete(member)
    await db.commit()
    return {"message": "Deleted"}
