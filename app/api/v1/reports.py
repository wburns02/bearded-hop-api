from fastapi import APIRouter
from sqlalchemy import select, func

from app.api.deps import DbSession, CurrentUser
from app.models.beer import Beer
from app.models.customer import Customer
from app.models.daily_sales import DailySales
from app.models.monthly_financial import MonthlyFinancial
from app.models.mug_club_member import MugClubMember
from app.models.open_tab import OpenTab

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/taproom-analytics")
async def get_taproom_analytics(db: DbSession, current_user: CurrentUser):
    # Top beers by total_pours
    result = await db.execute(
        select(Beer)
        .where(Beer.total_pours > 0)
        .order_by(Beer.total_pours.desc())
        .limit(20)
    )
    beers = result.scalars().all()
    return {
        "top_beers": [
            {
                "id": str(b.id),
                "name": b.name,
                "style": b.style,
                "abv": b.abv,
                "total_pours": b.total_pours,
                "rating": b.rating,
                "status": b.status,
                "tap_number": b.tap_number,
            }
            for b in beers
        ]
    }


@router.get("/summary")
async def get_summary(db: DbSession, current_user: CurrentUser):
    # Total customers
    customer_count_result = await db.execute(select(func.count()).select_from(Customer))
    total_customers = customer_count_result.scalar() or 0

    # Mug club members
    mug_count_result = await db.execute(
        select(func.count()).select_from(MugClubMember).where(MugClubMember.status == "active")
    )
    active_mug_members = mug_count_result.scalar() or 0

    # Open tabs
    tabs_result = await db.execute(select(func.count()).select_from(OpenTab))
    open_tabs = tabs_result.scalar() or 0

    # Total revenue from all monthly financials
    monthly_result = await db.execute(select(MonthlyFinancial))
    monthly_rows = monthly_result.scalars().all()
    total_revenue_all_time = sum(r.total_revenue for r in monthly_rows)
    total_expenses_all_time = sum(r.total_expenses for r in monthly_rows)
    net_profit_all_time = sum(r.net_profit for r in monthly_rows)

    # Daily sales count
    daily_count_result = await db.execute(select(func.count()).select_from(DailySales))
    days_recorded = daily_count_result.scalar() or 0

    return {
        "total_customers": total_customers,
        "active_mug_club_members": active_mug_members,
        "open_tabs": open_tabs,
        "total_revenue_all_time": round(total_revenue_all_time, 2),
        "total_expenses_all_time": round(total_expenses_all_time, 2),
        "net_profit_all_time": round(net_profit_all_time, 2),
        "days_recorded": days_recorded,
    }
