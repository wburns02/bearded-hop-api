import uuid
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class DailySales(Base):
    __tablename__ = "daily_sales"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(String, unique=True, nullable=False)
    beer_revenue = Column(Float, default=0)
    food_revenue = Column(Float, default=0)
    na_revenue = Column(Float, default=0)
    merchandise_revenue = Column(Float, default=0)
    event_revenue = Column(Float, default=0)
    total_revenue = Column(Float, default=0)
    customer_count = Column(Integer, default=0)
    avg_ticket = Column(Float, default=0)
