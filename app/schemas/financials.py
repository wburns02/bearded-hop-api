from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel


class DailySalesResponse(BaseModel):
    id: UUID
    date: date
    beer_revenue: float = 0
    food_revenue: float = 0
    na_revenue: float = 0
    merchandise_revenue: float = 0
    event_revenue: float = 0
    total_revenue: float = 0
    customer_count: int = 0
    avg_ticket: float = 0

    model_config = {"from_attributes": True}


class MonthlyFinancialResponse(BaseModel):
    id: UUID
    month: str
    month_label: str = ""
    beer_revenue: float = 0
    food_revenue: float = 0
    na_revenue: float = 0
    merchandise_revenue: float = 0
    event_revenue: float = 0
    wholesale_revenue: float = 0
    total_revenue: float = 0
    cogs: float = 0
    labor_cost: float = 0
    rent: float = 0
    utilities: float = 0
    marketing: float = 0
    insurance: float = 0
    licenses: float = 0
    supplies: float = 0
    misc: float = 0
    total_expenses: float = 0
    net_profit: float = 0
    net_margin_pct: float = 0

    model_config = {"from_attributes": True}


class TTBReportResponse(BaseModel):
    id: UUID
    month: str
    beginning_inventory: float = 0
    produced: float = 0
    received: float = 0
    transferred_taproom: float = 0
    transferred_distribution: float = 0
    ending_inventory: float = 0
    losses: float = 0
    excise_tax: float = 0

    model_config = {"from_attributes": True}
