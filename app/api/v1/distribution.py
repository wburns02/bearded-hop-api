from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.wholesale_account import WholesaleAccount
from app.models.wholesale_order import WholesaleOrder
from app.schemas.distribution import (
    WholesaleAccountCreate,
    WholesaleAccountUpdate,
    WholesaleAccountResponse,
    WholesaleOrderCreate,
    WholesaleOrderUpdate,
    WholesaleOrderResponse,
)

router = APIRouter(prefix="/distribution", tags=["distribution"])


# ---------------------------------------------------------------------------
# Wholesale Accounts
# ---------------------------------------------------------------------------

@router.get("/accounts", response_model=list[WholesaleAccountResponse])
async def list_accounts(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(WholesaleAccount))
    return result.scalars().all()


@router.post("/accounts", response_model=WholesaleAccountResponse)
async def create_account(body: WholesaleAccountCreate, db: DbSession, current_user: CurrentUser):
    account = WholesaleAccount(**body.model_dump())
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


@router.get("/accounts/{id}", response_model=WholesaleAccountResponse)
async def get_account(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(WholesaleAccount).where(WholesaleAccount.id == id))
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Wholesale account not found")
    return account


@router.patch("/accounts/{id}", response_model=WholesaleAccountResponse)
async def update_account(id: UUID, body: WholesaleAccountUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(WholesaleAccount).where(WholesaleAccount.id == id))
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Wholesale account not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(account, field, value)
    await db.commit()
    await db.refresh(account)
    return account


# ---------------------------------------------------------------------------
# Wholesale Orders
# ---------------------------------------------------------------------------

@router.get("/orders", response_model=list[WholesaleOrderResponse])
async def list_orders(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(WholesaleOrder))
    return result.scalars().all()


@router.post("/orders", response_model=WholesaleOrderResponse)
async def create_order(body: WholesaleOrderCreate, db: DbSession, current_user: CurrentUser):
    data = body.model_dump()
    data["account_id"] = str(data["account_id"])
    order = WholesaleOrder(**data)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


@router.get("/orders/{id}", response_model=WholesaleOrderResponse)
async def get_order(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(WholesaleOrder).where(WholesaleOrder.id == id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Wholesale order not found")
    return order


@router.patch("/orders/{id}", response_model=WholesaleOrderResponse)
async def update_order(id: UUID, body: WholesaleOrderUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(WholesaleOrder).where(WholesaleOrder.id == id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Wholesale order not found")
    data = body.model_dump(exclude_unset=True)
    if "account_id" in data and data["account_id"] is not None:
        data["account_id"] = str(data["account_id"])
    for field, value in data.items():
        setattr(order, field, value)
    await db.commit()
    await db.refresh(order)
    return order
