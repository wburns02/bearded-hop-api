import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class KegEvent(Base):
    __tablename__ = "keg_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keg_id = Column(UUID(as_uuid=True), ForeignKey("kegs.id"), nullable=False)
    date = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, default="")
    account_name = Column(String, nullable=True)
    beer_name = Column(String, nullable=True)
    performed_by = Column(String, nullable=True)
