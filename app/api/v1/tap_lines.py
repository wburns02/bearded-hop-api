from fastapi import APIRouter
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from app.api.deps import DbSession, CurrentUser
from app.models.tap_line import TapLine
from app.schemas.tap_lines import TapLineUpdate, TapLineBase
from app.exceptions import NotFoundError

router = APIRouter(prefix="/taps", tags=["taps"])


class PourRequest(BaseModel):
    pour_size_oz: float = 16.0  # ounces — used to calculate percentage of keg consumed


# TapLine uses tap_number (int) as its primary key, not a UUID.
# We return TapLineBase which omits the non-existent `id` field.


@router.get("/", response_model=list[TapLineBase])
async def list_tap_lines(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(TapLine))
    return result.scalars().all()


@router.get("/{tap_number}", response_model=TapLineBase)
async def get_tap_line(tap_number: int, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(TapLine).where(TapLine.tap_number == tap_number))
    tap = result.scalar_one_or_none()
    if not tap:
        raise NotFoundError("TapLine")
    return tap


@router.patch("/{tap_number}", response_model=TapLineBase)
async def update_tap_line(tap_number: int, body: TapLineUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(TapLine).where(TapLine.tap_number == tap_number))
    tap = result.scalar_one_or_none()
    if not tap:
        raise NotFoundError("TapLine")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(tap, field, value)
    await db.commit()
    await db.refresh(tap)
    return tap


@router.post("/{tap_number}/pour", response_model=TapLineBase)
async def record_pour(tap_number: int, body: PourRequest, db: DbSession, current_user: CurrentUser):
    """
    Decrement keg_level by a percentage based on pour size and increment total_pours.

    keg_level is stored as a percentage (0–100). We determine the percentage consumed
    based on the keg_size (standard volumes):
      1/2 barrel  = 1,984 oz
      1/4 barrel  = 992 oz
      slim-1/4    = 992 oz
      1/6 barrel  = 661 oz
    """
    result = await db.execute(select(TapLine).where(TapLine.tap_number == tap_number))
    tap = result.scalar_one_or_none()
    if not tap:
        raise NotFoundError("TapLine")

    keg_volumes_oz: dict[str, float] = {
        "1/2": 1984.0,
        "1/4": 992.0,
        "slim-1/4": 992.0,
        "1/6": 661.0,
    }
    total_oz = keg_volumes_oz.get(tap.keg_size or "1/2", 1984.0)
    pct_consumed = (body.pour_size_oz / total_oz) * 100.0

    tap.keg_level = max(0.0, (tap.keg_level or 100.0) - pct_consumed)
    tap.total_pours = (tap.total_pours or 0) + 1

    await db.commit()
    await db.refresh(tap)
    return tap
