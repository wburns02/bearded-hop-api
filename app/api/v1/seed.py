from fastapi import APIRouter, Query
from app.api.deps import DbSession
from app.config import settings

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("/")
async def seed_database(db: DbSession, force: str = Query(default="")):
    if settings.ENVIRONMENT == "production" and force != "bearded-hop-2026":
        return {"error": "Seeding not allowed in production"}
    from app.seed_data import run_seed
    try:
        await run_seed(db)
    except Exception as exc:
        return {"error": str(exc)}
    return {"message": "Database seeded successfully"}
