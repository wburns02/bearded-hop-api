from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.floor_table import FloorTable
from app.models.open_tab import OpenTab
from app.models.service_alert import ServiceAlert
from app.models.order_timeline import OrderTimeline
from app.schemas.floor_plan import (
    FloorTableResponse,
    FloorTableUpdate,
    SeatGuestsRequest,
    ServiceAlertCreate,
    ServiceAlertResponse,
    OrderTimelineResponse,
)

router = APIRouter(prefix="/floor-plan", tags=["floor-plan"])


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------

@router.get("/tables", response_model=list[FloorTableResponse])
async def list_tables(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(FloorTable))
    return result.scalars().all()


@router.patch("/tables/{id}", response_model=FloorTableResponse)
async def update_table(id: str, body: FloorTableUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(FloorTable).where(FloorTable.id == id))
    table = result.scalar_one_or_none()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        if value is not None and hasattr(value, '__str__') and field in (
            "current_tab_id", "current_customer_id", "server_id", "reservation_id"
        ):
            value = str(value)
        elif field == "seated_at" and value is not None:
            value = str(value)
        setattr(table, field, value)
    await db.commit()
    await db.refresh(table)
    return table


@router.post("/tables/{id}/seat", response_model=FloorTableResponse)
async def seat_guests(id: str, body: SeatGuestsRequest, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(FloorTable).where(FloorTable.id == id))
    table = result.scalar_one_or_none()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Create a new open tab for this table
    now = datetime.now(timezone.utc)
    tab = OpenTab(
        customer_name=body.customer_name,
        customer_id=body.customer_id,
        items=[],
        opened_at=now.isoformat(),
        server=body.server_name or "",
        subtotal=0.0,
        table_number=id,
    )
    db.add(tab)
    await db.flush()  # get tab.id before commit

    # Update table fields
    table.status = "occupied"
    table.current_customer_name = body.customer_name
    table.current_customer_id = str(body.customer_id) if body.customer_id else None
    table.party_size = body.party_size
    table.server_id = str(body.server_id) if body.server_id else None
    table.server_name = body.server_name
    table.seated_at = now.isoformat()
    table.current_tab_id = str(tab.id)

    await db.commit()
    await db.refresh(table)
    return table


@router.post("/tables/{id}/clear", response_model=FloorTableResponse)
async def clear_table(id: str, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(FloorTable).where(FloorTable.id == id))
    table = result.scalar_one_or_none()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Delete linked tab if present
    if table.current_tab_id:
        tab_result = await db.execute(
            select(OpenTab).where(OpenTab.table_number == id)
        )
        tab = tab_result.scalar_one_or_none()
        if tab:
            await db.delete(tab)

    table.status = "available"
    table.current_tab_id = None
    table.current_customer_name = None
    table.current_customer_id = None
    table.party_size = None
    table.server_id = None
    table.server_name = None
    table.seated_at = None

    await db.commit()
    await db.refresh(table)
    return table


# ---------------------------------------------------------------------------
# Service Alerts
# ---------------------------------------------------------------------------

@router.get("/alerts", response_model=list[ServiceAlertResponse])
async def list_alerts(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(ServiceAlert))
    return result.scalars().all()


@router.post("/alerts", response_model=ServiceAlertResponse)
async def create_alert(body: ServiceAlertCreate, db: DbSession, current_user: CurrentUser):
    data = body.model_dump()
    if data.get("created_at") is not None:
        data["created_at"] = str(data["created_at"])
    else:
        data["created_at"] = datetime.now(timezone.utc).isoformat()
    alert = ServiceAlert(**data)
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert


@router.delete("/alerts/{id}")
async def dismiss_alert(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(ServiceAlert).where(ServiceAlert.id == id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    await db.delete(alert)
    await db.commit()
    return {"message": "Alert dismissed"}


# ---------------------------------------------------------------------------
# Order Timeline
# ---------------------------------------------------------------------------

@router.get("/timeline/{table_id}", response_model=list[OrderTimelineResponse])
async def get_table_timeline(table_id: str, db: DbSession, current_user: CurrentUser):
    result = await db.execute(
        select(OrderTimeline).where(OrderTimeline.table_id == table_id)
    )
    return result.scalars().all()
