import uuid
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    count = Column(Integer, default=0)
    avg_spend = Column(Float, default=0)
    visit_frequency = Column(String, default="")
    top_beer = Column(String, default="")
    suggested_campaign = Column(String, default="")
    color = Column(String, default="#000000")
