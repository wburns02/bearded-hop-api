import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class FermentationVessel(Base):
    __tablename__ = "fermentation_vessels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    vessel_type = Column(String, nullable=False, default="fermenter")
    capacity_bbl = Column(Float, nullable=False, default=7.0)
    current_batch_id = Column(UUID(as_uuid=True), ForeignKey("batches.id"), nullable=True)
    status = Column(String, nullable=False, default="empty")
    temperature_f = Column(Float, nullable=True)
    pressure_psi = Column(Float, nullable=True)
    notes = Column(String, default="")
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow())
