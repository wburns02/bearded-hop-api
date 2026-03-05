from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup
    from app.database import engine, Base
    # Import all models so Base.metadata knows about them
    from app.models import (  # noqa: F401
        user, beer, recipe, detailed_recipe, batch, gravity_reading,
        tap_line, keg, keg_event, customer, visit_record, customer_note,
        event, performer, reservation, open_tab, tab_item,
        pos_transaction, transaction_item, floor_table, service_alert,
        order_timeline, menu_item, inventory_item, purchase_order,
        staff_member, staff_certification, schedule_shift,
        wholesale_account, wholesale_order, mug_club_member,
        email_campaign, daily_sales, monthly_financial, ttb_report,
        compliance_item, social_metrics, content_calendar,
        customer_segment, business_settings,
        fermentation_vessel, brew_day_log, quality_check,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Bearded Hop API", version="1.0.0", lifespan=lifespan)

# CORS
origins = [settings.FRONTEND_URL]
if settings.ENVIRONMENT == "development":
    origins.extend(["http://localhost:5173", "http://localhost:4173", "http://localhost:3000"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/ping")
async def ping():
    return {"status": "ok", "service": "bearded-hop-api", "version": "1.0.0"}


# Import and include routers
from app.api.v1.auth import router as auth_router
app.include_router(auth_router, prefix="/api/v1")

from app.api.v1.customers import router as customers_router
app.include_router(customers_router, prefix="/api/v1")

from app.api.v1.beers import router as beers_router
app.include_router(beers_router, prefix="/api/v1")

from app.api.v1.recipes import router as recipes_router
app.include_router(recipes_router, prefix="/api/v1")

from app.api.v1.detailed_recipes import router as detailed_recipes_router
app.include_router(detailed_recipes_router, prefix="/api/v1")

from app.api.v1.batches import router as batches_router
app.include_router(batches_router, prefix="/api/v1")

from app.api.v1.tap_lines import router as tap_lines_router
app.include_router(tap_lines_router, prefix="/api/v1")

from app.api.v1.kegs import router as kegs_router
app.include_router(kegs_router, prefix="/api/v1")

from app.api.v1.events import router as events_router
app.include_router(events_router, prefix="/api/v1")

from app.api.v1.performers import router as performers_router
app.include_router(performers_router, prefix="/api/v1")

from app.api.v1.reservations import router as reservations_router
app.include_router(reservations_router, prefix="/api/v1")

from app.api.v1.menu_items import router as menu_items_router
app.include_router(menu_items_router, prefix="/api/v1")

from app.api.v1.inventory import router as inventory_router
app.include_router(inventory_router, prefix="/api/v1")

from app.api.v1.staff import router as staff_router
app.include_router(staff_router, prefix="/api/v1")

from app.api.v1.schedule import router as schedule_router
app.include_router(schedule_router, prefix="/api/v1")

from app.api.v1.distribution import router as distribution_router
app.include_router(distribution_router, prefix="/api/v1")

from app.api.v1.mug_club import router as mug_club_router
app.include_router(mug_club_router, prefix="/api/v1")

from app.api.v1.marketing import router as marketing_router
app.include_router(marketing_router, prefix="/api/v1")

from app.api.v1.financials import router as financials_router
app.include_router(financials_router, prefix="/api/v1")

from app.api.v1.pos import router as pos_router
app.include_router(pos_router, prefix="/api/v1")

from app.api.v1.floor_plan import router as floor_plan_router
app.include_router(floor_plan_router, prefix="/api/v1")

from app.api.v1.settings_routes import router as settings_router
app.include_router(settings_router, prefix="/api/v1")

from app.api.v1.dashboard import router as dashboard_router
app.include_router(dashboard_router, prefix="/api/v1")

from app.api.v1.reports import router as reports_router
app.include_router(reports_router, prefix="/api/v1")

from app.api.v1.vessels import router as vessels_router
app.include_router(vessels_router, prefix="/api/v1")

from app.api.v1.brew_days import router as brew_days_router
app.include_router(brew_days_router, prefix="/api/v1")

from app.api.v1.quality import router as quality_router
app.include_router(quality_router, prefix="/api/v1")

from app.api.v1.production import router as production_router
app.include_router(production_router, prefix="/api/v1")

from app.api.v1.seed import router as seed_router
app.include_router(seed_router, prefix="/api/v1")
