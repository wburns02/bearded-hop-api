from fastapi import APIRouter
from sqlalchemy import select
from uuid import UUID

from app.api.deps import DbSession, CurrentUser
from app.models.recipe import Recipe
from app.schemas.recipes import RecipeCreate, RecipeUpdate, RecipeResponse
from app.exceptions import NotFoundError

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=list[RecipeResponse])
async def list_recipes(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Recipe))
    return result.scalars().all()


@router.get("/{id}", response_model=RecipeResponse)
async def get_recipe(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Recipe).where(Recipe.id == id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise NotFoundError("Recipe")
    return recipe


@router.post("/", response_model=RecipeResponse, status_code=201)
async def create_recipe(body: RecipeCreate, db: DbSession, current_user: CurrentUser):
    recipe = Recipe(**body.model_dump())
    db.add(recipe)
    await db.commit()
    await db.refresh(recipe)
    return recipe


@router.patch("/{id}", response_model=RecipeResponse)
async def update_recipe(id: UUID, body: RecipeUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Recipe).where(Recipe.id == id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise NotFoundError("Recipe")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(recipe, field, value)
    await db.commit()
    await db.refresh(recipe)
    return recipe


@router.delete("/{id}", status_code=204)
async def delete_recipe(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Recipe).where(Recipe.id == id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise NotFoundError("Recipe")
    await db.delete(recipe)
    await db.commit()
