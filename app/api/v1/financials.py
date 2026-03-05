from typing import Optional
from datetime import date, timedelta

from fastapi import APIRouter
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.monthly_financial import MonthlyFinancial
from app.models.daily_sales import DailySales
from app.models.ttb_report import TTBReport
from app.schemas.financials import (
    MonthlyFinancialResponse,
    DailySalesResponse,
    TTBReportResponse,
)

router = APIRouter(prefix="/financials", tags=["financials"])


@router.get("/monthly", response_model=list[MonthlyFinancialResponse])
async def list_monthly_financials(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(MonthlyFinancial))
    return result.scalars().all()


@router.get("/daily-sales", response_model=list[DailySalesResponse])
async def list_daily_sales(db: DbSession, current_user: CurrentUser, days: Optional[int] = None):
    stmt = select(DailySales)
    if days:
        cutoff = (date.today() - timedelta(days=days)).isoformat()
        stmt = stmt.where(DailySales.date >= cutoff)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/ttb-reports", response_model=list[TTBReportResponse])
async def list_ttb_reports(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(TTBReport))
    return result.scalars().all()
