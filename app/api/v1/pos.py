from typing import Optional
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.open_tab import OpenTab
from app.models.pos_transaction import POSTransaction
from app.schemas.pos import (
    OpenTabCreate,
    OpenTabResponse,
    CloseTabRequest,
    POSTransactionResponse,
    TabItemSchema,
)

router = APIRouter(prefix="/pos", tags=["pos"])


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------

@router.get("/tabs", response_model=list[OpenTabResponse])
async def list_open_tabs(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(OpenTab))
    return result.scalars().all()


@router.post("/tabs", response_model=OpenTabResponse)
async def create_tab(body: OpenTabCreate, db: DbSession, current_user: CurrentUser):
    data = body.model_dump()
    if data.get("customer_id"):
        data["customer_id"] = str(data["customer_id"])
    data["opened_at"] = str(data["opened_at"])
    tab = OpenTab(**data)
    db.add(tab)
    await db.commit()
    await db.refresh(tab)
    return tab


@router.post("/tabs/{id}/items", response_model=OpenTabResponse)
async def add_item_to_tab(id: UUID, item: TabItemSchema, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(OpenTab).where(OpenTab.id == id))
    tab = result.scalar_one_or_none()
    if not tab:
        raise HTTPException(status_code=404, detail="Tab not found")

    current_items = list(tab.items) if tab.items else []
    current_items.append(item.model_dump())
    tab.items = current_items
    tab.subtotal = sum(i["price"] * i.get("qty", 1) for i in current_items)

    await db.commit()
    await db.refresh(tab)
    return tab


@router.post("/tabs/{id}/close", response_model=POSTransactionResponse)
async def close_tab(id: UUID, body: CloseTabRequest, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(OpenTab).where(OpenTab.id == id))
    tab = result.scalar_one_or_none()
    if not tab:
        raise HTTPException(status_code=404, detail="Tab not found")

    subtotal = tab.subtotal or 0.0
    discount = body.discount or 0.0
    discounted_subtotal = subtotal - discount
    tax = round(discounted_subtotal * 0.0825, 2)
    total = round(discounted_subtotal + tax + (body.tip_amount or 0.0), 2)

    transaction = POSTransaction(
        customer_name=tab.customer_name,
        items=tab.items,
        subtotal=subtotal,
        tax=tax,
        discount=discount if discount else None,
        discount_type=body.discount_type,
        total=total,
        payment_method=body.payment_method,
        server=tab.server,
        closed_at=datetime.now(timezone.utc).isoformat(),
        tip_amount=body.tip_amount if body.tip_amount else None,
    )
    db.add(transaction)
    await db.delete(tab)
    await db.commit()
    await db.refresh(transaction)
    return transaction


# ---------------------------------------------------------------------------
# Transactions
# ---------------------------------------------------------------------------

@router.get("/transactions", response_model=list[POSTransactionResponse])
async def list_transactions(db: DbSession, current_user: CurrentUser, limit: Optional[int] = 20):
    stmt = select(POSTransaction).order_by(POSTransaction.closed_at.desc())
    if limit:
        stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
