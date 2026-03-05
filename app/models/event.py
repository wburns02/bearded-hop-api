import uuid
from sqlalchemy import Column, String, Float, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    date = Column(String, nullable=False)
    start_time = Column(String, nullable=True)
    end_time = Column(String, nullable=True)
    description = Column(String, default="")
    performer_id = Column(UUID(as_uuid=True), nullable=True)
    capacity = Column(Integer, default=0)
    tickets_sold = Column(Integer, default=0)
    ticket_price = Column(Float, default=0)
    is_ticketed = Column(Boolean, default=False)
    is_family_friendly = Column(Boolean, default=True)
    location = Column(String, default="taproom")
    status = Column(String, default="upcoming")
    revenue = Column(Float, default=0)
    special_beer = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
