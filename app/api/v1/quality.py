from fastapi import APIRouter, Query
from sqlalchemy import select
from uuid import UUID
from typing import Optional

from app.api.deps import DbSession, CurrentUser
from app.models.quality_check import QualityCheck
from app.schemas.quality import QualityCheckCreate, QualityCheckResponse
from app.exceptions import NotFoundError

router = APIRouter(prefix="/quality", tags=["quality"])


@router.get("/", response_model=list[QualityCheckResponse])
async def list_quality_checks(
    db: DbSession,
    current_user: CurrentUser,
    batch_id: Optional[UUID] = Query(None),
):
    q = select(QualityCheck)
    if batch_id:
        q = q.where(QualityCheck.batch_id == batch_id)
    q = q.order_by(QualityCheck.checked_at.desc())
    result = await db.execute(q)
    return result.scalars().all()


@router.post("/", response_model=QualityCheckResponse, status_code=201)
async def create_quality_check(body: QualityCheckCreate, db: DbSession, current_user: CurrentUser):
    qc = QualityCheck(**body.model_dump())
    db.add(qc)
    await db.commit()
    await db.refresh(qc)
    return qc


@router.get("/batch/{batch_id}/report")
async def batch_quality_report(batch_id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(
        select(QualityCheck).where(QualityCheck.batch_id == batch_id).order_by(QualityCheck.checked_at)
    )
    checks = result.scalars().all()
    total = len(checks)
    passed = sum(1 for c in checks if c.pass_fail == "pass")
    failed = sum(1 for c in checks if c.pass_fail == "fail")
    warnings = sum(1 for c in checks if c.pass_fail == "warning")

    return {
        "batch_id": str(batch_id),
        "total_checks": total,
        "passed": passed,
        "failed": failed,
        "warnings": warnings,
        "pass_rate": round(passed / total * 100, 1) if total > 0 else 0,
        "checks": [
            {
                "id": str(c.id),
                "check_type": c.check_type,
                "value": c.value,
                "checked_by": c.checked_by,
                "checked_at": c.checked_at.isoformat() if c.checked_at else None,
                "notes": c.notes,
                "pass_fail": c.pass_fail,
            }
            for c in checks
        ],
    }
