from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.inventory_item import InventoryItem
from app.models.purchase_order import PurchaseOrder
from app.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemUpdate,
    InventoryItemResponse,
    PurchaseOrderCreate,
    PurchaseOrderUpdate,
    PurchaseOrderResponse,
)

router = APIRouter(prefix="/inventory", tags=["inventory"])


# ---------------------------------------------------------------------------
# Inventory Items
# ---------------------------------------------------------------------------

@router.get("/", response_model=list[InventoryItemResponse])
async def list_inventory_items(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(InventoryItem))
    return result.scalars().all()


@router.post("/", response_model=InventoryItemResponse)
async def create_inventory_item(body: InventoryItemCreate, db: DbSession, current_user: CurrentUser):
    item = InventoryItem(**body.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/reorder-alerts", response_model=list[InventoryItemResponse])
async def get_reorder_alerts(db: DbSession, current_user: CurrentUser):
    result = await db.execute(
        select(InventoryItem).where(InventoryItem.current_stock <= InventoryItem.reorder_point)
    )
    return result.scalars().all()


@router.get("/{id}", response_model=InventoryItemResponse)
async def get_inventory_item(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(InventoryItem).where(InventoryItem.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item


@router.patch("/{id}", response_model=InventoryItemResponse)
async def update_inventory_item(id: UUID, body: InventoryItemUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(InventoryItem).where(InventoryItem.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{id}")
async def delete_inventory_item(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(InventoryItem).where(InventoryItem.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    await db.delete(item)
    await db.commit()
    return {"message": "Deleted"}


# ---------------------------------------------------------------------------
# Purchase Orders
# ---------------------------------------------------------------------------

@router.get("/purchase-orders", response_model=list[PurchaseOrderResponse])
async def list_purchase_orders(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(PurchaseOrder))
    return result.scalars().all()


@router.post("/purchase-orders", response_model=PurchaseOrderResponse)
async def create_purchase_order(body: PurchaseOrderCreate, db: DbSession, current_user: CurrentUser):
    po = PurchaseOrder(**body.model_dump())
    db.add(po)
    await db.commit()
    await db.refresh(po)
    return po


@router.patch("/purchase-orders/{id}", response_model=PurchaseOrderResponse)
async def update_purchase_order(id: UUID, body: PurchaseOrderUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(PurchaseOrder).where(PurchaseOrder.id == id))
    po = result.scalar_one_or_none()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(po, field, value)
    await db.commit()
    await db.refresh(po)
    return po
