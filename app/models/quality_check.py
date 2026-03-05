import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class QualityCheck(Base):
    __tablename__ = "quality_checks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id = Column(UUID(as_uuid=True), ForeignKey("batches.id"), nullable=False)
    check_type = Column(String, nullable=False)
    value = Column(String, nullable=False)
    checked_by = Column(String, default="")
    checked_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, default="")
    pass_fail = Column(String, default="na")
