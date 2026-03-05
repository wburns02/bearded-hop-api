from fastapi import APIRouter
from app.api.deps import DbSession
from app.config import settings

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("/")
async def seed_database(db: DbSession):
    if settings.ENVIRONMENT == "production":
        return {"error": "Seeding not allowed in production"}
    from app.seed_data import run_seed
    try:
        await run_seed(db)
    except Exception as exc:
        return {"error": str(exc)}
    return {"message": "Database seeded successfully"}
