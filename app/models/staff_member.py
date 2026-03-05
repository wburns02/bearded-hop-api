import uuid
from sqlalchemy import Column, String, Float, Integer, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class StaffMember(Base):
    __tablename__ = "staff_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    hire_date = Column(String, nullable=True)
    hourly_rate = Column(Float, default=0)
    status = Column(String, default="active")
    tabc_certified = Column(Boolean, default=False)
    tabc_expiry = Column(String, nullable=True)
    food_handler_certified = Column(Boolean, default=False)
    food_handler_expiry = Column(String, nullable=True)
    hours_this_week = Column(Float, default=0)
    sales_this_week = Column(Float, default=0)
    avatar = Column(String, nullable=True)
    schedule = Column(JSON, default=list)
