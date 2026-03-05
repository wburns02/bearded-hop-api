import uuid
from sqlalchemy import Column, String, Integer, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    party_size = Column(Integer, default=1)
    table_id = Column(String, nullable=True)
    section = Column(String, default="taproom")
    status = Column(String, default="confirmed")
    notes = Column(String, default="")
    special_requests = Column(JSON, default=list)
    is_high_chair_needed = Column(Boolean, default=False)
