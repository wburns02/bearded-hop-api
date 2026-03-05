import uuid
from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class MonthlyFinancial(Base):
    __tablename__ = "monthly_financials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    month = Column(String, unique=True, nullable=False)
    month_label = Column(String, default="")
    beer_revenue = Column(Float, default=0)
    food_revenue = Column(Float, default=0)
    na_revenue = Column(Float, default=0)
    merchandise_revenue = Column(Float, default=0)
    event_revenue = Column(Float, default=0)
    wholesale_revenue = Column(Float, default=0)
    total_revenue = Column(Float, default=0)
    cogs = Column(Float, default=0)
    labor_cost = Column(Float, default=0)
    rent = Column(Float, default=0)
    utilities = Column(Float, default=0)
    marketing = Column(Float, default=0)
    insurance = Column(Float, default=0)
    licenses = Column(Float, default=0)
    supplies = Column(Float, default=0)
    misc = Column(Float, default=0)
    total_expenses = Column(Float, default=0)
    net_profit = Column(Float, default=0)
    net_margin_pct = Column(Float, default=0)
