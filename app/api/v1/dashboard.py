from datetime import date, timedelta

from fastapi import APIRouter
from sqlalchemy import select, func

from app.api.deps import DbSession, CurrentUser
from app.models.customer import Customer
from app.models.tap_line import TapLine
from app.models.daily_sales import DailySales
from app.models.open_tab import OpenTab
from app.models.social_metrics import SocialMetrics

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/kpis")
async def get_kpis(db: DbSession, current_user: CurrentUser):
    # Total customers
    customer_result = await db.execute(select(func.count()).select_from(Customer))
    total_customers = customer_result.scalar() or 0

    # Total beers on tap (active tap lines)
    tap_result = await db.execute(
        select(func.count()).select_from(TapLine).where(TapLine.status == "active")
    )
    total_beers_on_tap = tap_result.scalar() or 0

    # Today's revenue
    today_str = date.today().isoformat()
    daily_result = await db.execute(
        select(DailySales).where(DailySales.date == today_str)
    )
    today_sales = daily_result.scalar_one_or_none()
    todays_revenue = today_sales.total_revenue if today_sales else 0.0

    # Active tabs count
    tabs_result = await db.execute(select(func.count()).select_from(OpenTab))
    active_tabs = tabs_result.scalar() or 0

    # Average rating (from most recent social metrics entry)
    metrics_result = await db.execute(
        select(SocialMetrics).order_by(SocialMetrics.date.desc()).limit(1)
    )
    latest_metrics = metrics_result.scalar_one_or_none()
    avg_rating = latest_metrics.google_rating if latest_metrics else 0.0

    return {
        "total_customers": total_customers,
        "total_beers_on_tap": total_beers_on_tap,
        "todays_revenue": todays_revenue,
        "active_tabs": active_tabs,
        "avg_rating": avg_rating,
    }


@router.get("/revenue-chart")
async def get_revenue_chart(db: DbSession, current_user: CurrentUser):
    cutoff = (date.today() - timedelta(days=30)).isoformat()
    result = await db.execute(
        select(DailySales)
        .where(DailySales.date >= cutoff)
        .order_by(DailySales.date.asc())
    )
    rows = result.scalars().all()
    return [
        {
            "date": row.date,
            "total_revenue": row.total_revenue,
            "beer_revenue": row.beer_revenue,
            "food_revenue": row.food_revenue,
            "customer_count": row.customer_count,
        }
        for row in rows
    ]
