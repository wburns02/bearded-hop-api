from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.menu_item import MenuItem
from app.schemas.menu_items import MenuItemCreate, MenuItemUpdate, MenuItemResponse

router = APIRouter(prefix="/menu-items", tags=["menu"])


@router.get("/", response_model=list[MenuItemResponse])
async def list_menu_items(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(MenuItem))
    return result.scalars().all()


@router.post("/", response_model=MenuItemResponse)
async def create_menu_item(body: MenuItemCreate, db: DbSession, current_user: CurrentUser):
    item = MenuItem(**body.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/{id}", response_model=MenuItemResponse)
async def get_menu_item(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(MenuItem).where(MenuItem.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@router.patch("/{id}", response_model=MenuItemResponse)
async def update_menu_item(id: UUID, body: MenuItemUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(MenuItem).where(MenuItem.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{id}")
async def delete_menu_item(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(MenuItem).where(MenuItem.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    await db.delete(item)
    await db.commit()
    return {"message": "Deleted"}


@router.patch("/{id}/availability", response_model=MenuItemResponse)
async def toggle_availability(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(MenuItem).where(MenuItem.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    item.is_available = not item.is_available
    await db.commit()
    await db.refresh(item)
    return item
