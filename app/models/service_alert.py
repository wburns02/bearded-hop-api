import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class ServiceAlert(Base):
    __tablename__ = "service_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    message = Column(String, default="")
    priority = Column(String, default="medium")
    created_at = Column(String, nullable=True)
