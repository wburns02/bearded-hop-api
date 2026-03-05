import uuid
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class ScheduleShift(Base):
    __tablename__ = "schedule_shifts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff_members.id"), nullable=False)
    staff_name = Column(String, default="")
    role = Column(String, default="")
    date = Column(String, nullable=False)
    day_of_week = Column(String, default="")
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    hours = Column(Float, default=0)
    section = Column(String, default="taproom")
    status = Column(String, default="scheduled")
    notes = Column(String, nullable=True)
