from fastapi import APIRouter, Query
from sqlalchemy import select, func
from datetime import date, timedelta
from typing import Optional

from app.api.deps import DbSession, CurrentUser
from app.models.batch import Batch
from app.models.fermentation_vessel import FermentationVessel
from app.models.brew_day_log import BrewDayLog

router = APIRouter(prefix="/production", tags=["production"])

ACTIVE_STATUSES = ["mashing", "boiling", "fermenting", "conditioning", "carbonating"]
PHASE_ORDER = ["planned", "mashing", "boiling", "fermenting", "conditioning", "carbonating", "ready", "packaged"]
PHASE_DAYS = {
    "planned": 0, "mashing": 1, "boiling": 1, "fermenting": 14,
    "conditioning": 7, "carbonating": 5, "ready": 0, "packaged": 0,
}


@router.get("/overview")
async def production_overview(db: DbSession, current_user: CurrentUser):
    # Active batches
    result = await db.execute(select(Batch).where(Batch.status.in_(ACTIVE_STATUSES)))
    active_batches = result.scalars().all()

    # Vessels
    result = await db.execute(select(FermentationVessel))
    all_vessels = result.scalars().all()
    vessels_in_use = [v for v in all_vessels if v.status not in ("empty", "out_of_service")]
    vessels_available = [v for v in all_vessels if v.status == "empty"]

    # Upcoming brew days (next 14 days)
    today = date.today()
    result = await db.execute(
        select(BrewDayLog)
        .where(BrewDayLog.scheduled_date >= today)
        .where(BrewDayLog.scheduled_date <= today + timedelta(days=14))
        .order_by(BrewDayLog.scheduled_date)
    )
    upcoming_brew_days = result.scalars().all()

    # Ready to package
    result = await db.execute(select(Batch).where(Batch.status == "ready"))
    ready_batches = result.scalars().all()

    # Avg days in fermenter (estimate from brew_date for active fermenting batches)
    fermenting = [b for b in active_batches if b.status == "fermenting"]
    avg_days = 0
    if fermenting:
        total_days = 0
        count = 0
        for b in fermenting:
            if b.brew_date:
                try:
                    bd = date.fromisoformat(b.brew_date)
                    total_days += (today - bd).days
                    count += 1
                except ValueError:
                    pass
        avg_days = round(total_days / count) if count > 0 else 0

    # Production this month (BBL)
    month_start = today.replace(day=1).isoformat()
    result = await db.execute(
        select(Batch).where(Batch.brew_date >= month_start)
    )
    month_batches = result.scalars().all()
    production_bbl = sum(b.volume for b in month_batches if b.volume)

    # Build upcoming brew days response with batch info
    upcoming_list = []
    for bd_log in upcoming_brew_days:
        result = await db.execute(select(Batch).where(Batch.id == bd_log.batch_id))
        batch = result.scalar_one_or_none()
        upcoming_list.append({
            "id": str(bd_log.id),
            "scheduled_date": bd_log.scheduled_date.isoformat(),
            "status": bd_log.status,
            "brewer_name": bd_log.brewer_name,
            "batch_beer_name": batch.beer_name if batch else "",
            "batch_number": batch.batch_number if batch else "",
        })

    return {
        "active_batches_count": len(active_batches),
        "active_batches": [
            {
                "id": str(b.id),
                "batch_number": b.batch_number,
                "beer_name": b.beer_name,
                "style": b.style,
                "status": b.status,
                "brew_date": b.brew_date,
                "volume": b.volume,
                "tank_id": b.tank_id,
            }
            for b in active_batches
        ],
        "vessels_total": len(all_vessels),
        "vessels_in_use": len(vessels_in_use),
        "vessels_available": len(vessels_available),
        "upcoming_brew_days": upcoming_list,
        "next_brew_day": upcoming_list[0] if upcoming_list else None,
        "batches_ready_to_package": len(ready_batches),
        "avg_days_in_fermenter": avg_days,
        "production_this_month_bbl": production_bbl,
    }


@router.get("/calendar")
async def production_calendar(
    db: DbSession,
    current_user: CurrentUser,
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
):
    today = date.today()
    if not start:
        start = today - timedelta(days=today.weekday())
    if not end:
        end = start + timedelta(days=6)

    # Brew day logs in range
    result = await db.execute(
        select(BrewDayLog)
        .where(BrewDayLog.scheduled_date >= start)
        .where(BrewDayLog.scheduled_date <= end)
        .order_by(BrewDayLog.scheduled_date)
    )
    brew_days = result.scalars().all()

    events = []
    for bd in brew_days:
        result = await db.execute(select(Batch).where(Batch.id == bd.batch_id))
        batch = result.scalar_one_or_none()
        events.append({
            "id": str(bd.id),
            "type": "brew_day",
            "date": bd.scheduled_date.isoformat(),
            "status": bd.status,
            "brewer_name": bd.brewer_name,
            "batch_beer_name": batch.beer_name if batch else "",
            "batch_number": batch.batch_number if batch else "",
            "batch_status": batch.status if batch else "",
        })

    # Active batch phase windows
    result = await db.execute(select(Batch).where(Batch.status.in_(ACTIVE_STATUSES + ["ready"])))
    active_batches = result.scalars().all()
    for b in active_batches:
        if b.brew_date:
            try:
                brew_start = date.fromisoformat(b.brew_date)
                current_idx = PHASE_ORDER.index(b.status) if b.status in PHASE_ORDER else 0
                elapsed = sum(PHASE_DAYS[PHASE_ORDER[i]] for i in range(current_idx))
                phase_start = brew_start + timedelta(days=elapsed)
                phase_end = phase_start + timedelta(days=PHASE_DAYS.get(b.status, 7))
                if phase_end >= start and phase_start <= end:
                    events.append({
                        "id": str(b.id),
                        "type": "batch_phase",
                        "date": phase_start.isoformat(),
                        "end_date": phase_end.isoformat(),
                        "status": b.status,
                        "batch_beer_name": b.beer_name,
                        "batch_number": b.batch_number,
                    })
            except (ValueError, IndexError):
                pass

    return {"start": start.isoformat(), "end": end.isoformat(), "events": events}


@router.get("/timeline")
async def production_timeline(db: DbSession, current_user: CurrentUser):
    result = await db.execute(
        select(Batch).where(Batch.status.in_(ACTIVE_STATUSES + ["ready"]))
    )
    batches = result.scalars().all()

    # Get vessel assignments
    result = await db.execute(select(FermentationVessel))
    all_vessels = result.scalars().all()
    vessel_map = {str(v.current_batch_id): v.name for v in all_vessels if v.current_batch_id}

    timeline = []
    today = date.today()
    for b in batches:
        brew_start = None
        if b.brew_date:
            try:
                brew_start = date.fromisoformat(b.brew_date)
            except ValueError:
                pass

        current_idx = PHASE_ORDER.index(b.status) if b.status in PHASE_ORDER else 0
        elapsed_days = sum(PHASE_DAYS[PHASE_ORDER[i]] for i in range(current_idx))
        remaining_days = sum(PHASE_DAYS[PHASE_ORDER[i]] for i in range(current_idx, len(PHASE_ORDER)))
        total_days = elapsed_days + remaining_days

        estimated_completion = None
        if brew_start:
            estimated_completion = (brew_start + timedelta(days=total_days)).isoformat()
            days_in_current = (today - brew_start).days - sum(
                PHASE_DAYS[PHASE_ORDER[i]] for i in range(current_idx)
            )
        else:
            days_in_current = 0

        phase_total = PHASE_DAYS.get(b.status, 7)
        progress = min(100, round(elapsed_days / total_days * 100)) if total_days > 0 else 0

        timeline.append({
            "id": str(b.id),
            "batch_number": b.batch_number,
            "beer_name": b.beer_name,
            "style": b.style,
            "status": b.status,
            "brew_date": b.brew_date,
            "volume": b.volume,
            "vessel_name": vessel_map.get(str(b.id), b.tank_id or "Unassigned"),
            "progress_pct": progress,
            "days_in_current_phase": max(0, days_in_current),
            "estimated_phase_days": phase_total,
            "estimated_completion": estimated_completion,
        })

    timeline.sort(key=lambda x: x["estimated_completion"] or "9999")
    return timeline
