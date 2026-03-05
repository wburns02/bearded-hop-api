from fastapi import APIRouter, Query
from sqlalchemy import select
from uuid import UUID

from app.api.deps import DbSession, CurrentUser
from app.models.beer import Beer
from app.schemas.beers import BeerCreate, BeerUpdate, BeerResponse
from app.exceptions import NotFoundError

router = APIRouter(prefix="/beers", tags=["beers"])


@router.get("/", response_model=list[BeerResponse])
async def list_beers(
    db: DbSession,
    current_user: CurrentUser,
    status: str | None = Query(default=None),
    category: str | None = Query(default=None),
):
    stmt = select(Beer)
    if status:
        stmt = stmt.where(Beer.status == status)
    if category:
        stmt = stmt.where(Beer.category == category)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{id}", response_model=BeerResponse)
async def get_beer(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Beer).where(Beer.id == id))
    beer = result.scalar_one_or_none()
    if not beer:
        raise NotFoundError("Beer")
    return beer


@router.post("/", response_model=BeerResponse, status_code=201)
async def create_beer(body: BeerCreate, db: DbSession, current_user: CurrentUser):
    beer = Beer(**body.model_dump())
    db.add(beer)
    await db.commit()
    await db.refresh(beer)
    return beer


@router.patch("/{id}", response_model=BeerResponse)
async def update_beer(id: UUID, body: BeerUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Beer).where(Beer.id == id))
    beer = result.scalar_one_or_none()
    if not beer:
        raise NotFoundError("Beer")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(beer, field, value)
    await db.commit()
    await db.refresh(beer)
    return beer


@router.delete("/{id}", status_code=204)
async def delete_beer(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Beer).where(Beer.id == id))
    beer = result.scalar_one_or_none()
    if not beer:
        raise NotFoundError("Beer")
    await db.delete(beer)
    await db.commit()
