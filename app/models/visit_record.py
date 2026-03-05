import uuid
from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class VisitRecord(Base):
    __tablename__ = "visit_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    date = Column(String, nullable=False)
    day_of_week = Column(String, nullable=True)
    arrival_time = Column(String, nullable=True)
    party_size = Column(Integer, default=1)
    total_spent = Column(Float, default=0)
    beers_ordered = Column(JSON, default=list)
    food_ordered = Column(JSON, default=list)
    tab_closed_by = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
