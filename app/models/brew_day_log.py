import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class BrewDayLog(Base):
    __tablename__ = "brew_day_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id = Column(UUID(as_uuid=True), ForeignKey("batches.id"), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    brewer_id = Column(UUID(as_uuid=True), ForeignKey("staff_members.id"), nullable=True)
    brewer_name = Column(String, default="")
    mash_temp_f = Column(Float, nullable=True)
    mash_duration_min = Column(Integer, nullable=True)
    boil_duration_min = Column(Integer, default=60)
    pre_boil_gravity = Column(Float, nullable=True)
    original_gravity = Column(Float, nullable=True)
    post_boil_volume_gal = Column(Float, nullable=True)
    notes = Column(String, default="")
    status = Column(String, nullable=False, default="scheduled")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
