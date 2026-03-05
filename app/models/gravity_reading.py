import uuid
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class GravityReading(Base):
    __tablename__ = "gravity_readings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id = Column(UUID(as_uuid=True), ForeignKey("batches.id"), nullable=False)
    date = Column(String, nullable=False)
    gravity = Column(Float, nullable=False)
    temp = Column(Float, nullable=False)
