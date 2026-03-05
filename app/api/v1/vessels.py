from fastapi import APIRouter
from sqlalchemy import select
from uuid import UUID
from datetime import datetime

from app.api.deps import DbSession, CurrentUser
from app.models.fermentation_vessel import FermentationVessel
from app.models.batch import Batch
from app.models.quality_check import QualityCheck
from app.schemas.vessels import VesselCreate, VesselUpdate, VesselResponse, VesselReadingCreate
from app.exceptions import NotFoundError

router = APIRouter(prefix="/vessels", tags=["vessels"])


async def _enrich(vessel: FermentationVessel, db) -> dict:
    data = {c.key: getattr(vessel, c.key) for c in vessel.__table__.columns}
    if vessel.current_batch_id:
        result = await db.execute(select(Batch).where(Batch.id == vessel.current_batch_id))
        batch = result.scalar_one_or_none()
        if batch:
            data["batch_name"] = batch.batch_number
            data["batch_status"] = batch.status
            data["batch_beer_name"] = batch.beer_name
            data["batch_brew_date"] = batch.brew_date
            data["batch_style"] = batch.style
    return data


@router.get("/", response_model=list[VesselResponse])
async def list_vessels(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(FermentationVessel))
    vessels = result.scalars().all()
    return [await _enrich(v, db) for v in vessels]


@router.get("/{id}", response_model=VesselResponse)
async def get_vessel(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(FermentationVessel).where(FermentationVessel.id == id))
    vessel = result.scalar_one_or_none()
    if not vessel:
        raise NotFoundError("Vessel")
    return await _enrich(vessel, db)


@router.post("/", response_model=VesselResponse, status_code=201)
async def create_vessel(body: VesselCreate, db: DbSession, current_user: CurrentUser):
    vessel = FermentationVessel(**body.model_dump())
    db.add(vessel)
    await db.commit()
    await db.refresh(vessel)
    return await _enrich(vessel, db)


@router.patch("/{id}", response_model=VesselResponse)
async def update_vessel(id: UUID, body: VesselUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(FermentationVessel).where(FermentationVessel.id == id))
    vessel = result.scalar_one_or_none()
    if not vessel:
        raise NotFoundError("Vessel")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(vessel, field, value)
    vessel.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(vessel)
    return await _enrich(vessel, db)


@router.post("/{id}/reading", response_model=VesselResponse)
async def add_vessel_reading(id: UUID, body: VesselReadingCreate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(FermentationVessel).where(FermentationVessel.id == id))
    vessel = result.scalar_one_or_none()
    if not vessel:
        raise NotFoundError("Vessel")

    if body.temperature_f is not None:
        vessel.temperature_f = body.temperature_f
    if body.pressure_psi is not None:
        vessel.pressure_psi = body.pressure_psi

    if vessel.current_batch_id and body.gravity is not None:
        qc = QualityCheck(
            batch_id=vessel.current_batch_id,
            check_type="gravity",
            value=str(body.gravity),
            checked_by=body.checked_by,
            notes=body.notes,
            pass_fail="na",
        )
        db.add(qc)

    vessel.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(vessel)
    return await _enrich(vessel, db)
