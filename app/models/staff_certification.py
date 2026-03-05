import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class StaffCertification(Base):
    __tablename__ = "staff_certifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff_members.id"), nullable=False)
    staff_name = Column(String, default="")
    type = Column(String, nullable=False)
    status = Column(String, default="active")
    issue_date = Column(String, nullable=True)
    expiry_date = Column(String, nullable=True)
    days_until_expiry = Column(Integer, default=0)
