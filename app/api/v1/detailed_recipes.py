from datetime import datetime, timezone
from fastapi import APIRouter
from sqlalchemy import select, func
from uuid import UUID
from typing import Optional, Any
from pydantic import BaseModel

from app.api.deps import DbSession, CurrentUser
from app.models.detailed_recipe import DetailedRecipe
from app.models.batch import Batch
from app.schemas.batches import BatchResponse
from app.exceptions import NotFoundError

router = APIRouter(prefix="/detailed-recipes", tags=["recipes"])


# ── Inline schemas (no dedicated schema file exists for DetailedRecipe) ──────

class DetailedRecipeBase(BaseModel):
    beer_id: Optional[UUID] = None
    name: str
    style: str
    category: str = "flagship"
    version: int = 1
    batch_size: float = 0
    target_og: float = 0
    target_fg: float = 0
    target_abv: float = 0
    target_ibu: int = 0
    target_srm: int = 0
    boil_time: int = 60
    mash_temp: int = 152
    mash_time: int = 60
    grain_bill: list[dict] = []
    hop_schedule: list[dict] = []
    yeast: dict = {}
    water_profile: dict = {}
    water_adjustments: list[dict] = []
    brew_day_steps: list[dict] = []
    total_cost: float = 0
    cost_per_barrel: float = 0
    cost_per_pint: float = 0
    last_brewed: Optional[str] = None
    total_batches: int = 0
    brew_history: list[dict] = []
    notes: str = ""
    created_date: Optional[str] = None


class DetailedRecipeCreate(DetailedRecipeBase):
    pass


class DetailedRecipeUpdate(BaseModel):
    beer_id: Optional[UUID] = None
    name: Optional[str] = None
    style: Optional[str] = None
    category: Optional[str] = None
    version: Optional[int] = None
    batch_size: Optional[float] = None
    target_og: Optional[float] = None
    target_fg: Optional[float] = None
    target_abv: Optional[float] = None
    target_ibu: Optional[int] = None
    target_srm: Optional[int] = None
    boil_time: Optional[int] = None
    mash_temp: Optional[int] = None
    mash_time: Optional[int] = None
    grain_bill: Optional[list[dict]] = None
    hop_schedule: Optional[list[dict]] = None
    yeast: Optional[dict] = None
    water_profile: Optional[dict] = None
    water_adjustments: Optional[list[dict]] = None
    brew_day_steps: Optional[list[dict]] = None
    total_cost: Optional[float] = None
    cost_per_barrel: Optional[float] = None
    cost_per_pint: Optional[float] = None
    last_brewed: Optional[str] = None
    total_batches: Optional[int] = None
    brew_history: Optional[list[dict]] = None
    notes: Optional[str] = None
    created_date: Optional[str] = None


class DetailedRecipeResponse(DetailedRecipeBase):
    id: UUID

    model_config = {"from_attributes": True}


# ── Routes ───────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[DetailedRecipeResponse])
async def list_detailed_recipes(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(DetailedRecipe))
    return result.scalars().all()


@router.get("/{id}", response_model=DetailedRecipeResponse)
async def get_detailed_recipe(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(DetailedRecipe).where(DetailedRecipe.id == id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise NotFoundError("DetailedRecipe")
    return recipe


@router.post("/", response_model=DetailedRecipeResponse, status_code=201)
async def create_detailed_recipe(body: DetailedRecipeCreate, db: DbSession, current_user: CurrentUser):
    recipe = DetailedRecipe(**body.model_dump())
    db.add(recipe)
    await db.commit()
    await db.refresh(recipe)
    return recipe


@router.patch("/{id}", response_model=DetailedRecipeResponse)
async def update_detailed_recipe(id: UUID, body: DetailedRecipeUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(DetailedRecipe).where(DetailedRecipe.id == id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise NotFoundError("DetailedRecipe")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(recipe, field, value)
    await db.commit()
    await db.refresh(recipe)
    return recipe


@router.delete("/{id}", status_code=204)
async def delete_detailed_recipe(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(DetailedRecipe).where(DetailedRecipe.id == id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise NotFoundError("DetailedRecipe")
    await db.delete(recipe)
    await db.commit()


@router.post("/{id}/brew", response_model=BatchResponse, status_code=201)
async def brew_from_recipe(id: UUID, db: DbSession, current_user: CurrentUser):
    """Create a new Batch from this detailed recipe."""
    result = await db.execute(select(DetailedRecipe).where(DetailedRecipe.id == id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise NotFoundError("DetailedRecipe")

    year = datetime.now(timezone.utc).year

    # Count existing batches for this year to build a sequential batch number
    count_result = await db.execute(
        select(func.count()).select_from(Batch).where(
            Batch.batch_number.like(f"BH-{year}-%")
        )
    )
    existing_count = count_result.scalar() or 0
    batch_number = f"BH-{year}-{existing_count + 1:03d}"

    batch = Batch(
        batch_number=batch_number,
        beer_id=recipe.beer_id,
        beer_name=recipe.name,
        style=recipe.style,
        recipe_id=recipe.id,
        status="planned",
        target_og=recipe.target_og,
        target_fg=recipe.target_fg,
        volume=recipe.batch_size,
    )
    db.add(batch)
    await db.commit()
    await db.refresh(batch)
    return batch
