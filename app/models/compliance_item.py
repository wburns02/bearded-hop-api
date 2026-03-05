import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class ComplianceItem(Base):
    __tablename__ = "compliance_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="compliant")
    due_date = Column(String, nullable=True)
    last_completed = Column(String, nullable=True)
    notes = Column(String, default="")
