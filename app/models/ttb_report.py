import uuid
from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class TTBReport(Base):
    __tablename__ = "ttb_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    month = Column(String, unique=True, nullable=False)
    beginning_inventory = Column(Float, default=0)
    produced = Column(Float, default=0)
    received = Column(Float, default=0)
    transferred_taproom = Column(Float, default=0)
    transferred_distribution = Column(Float, default=0)
    ending_inventory = Column(Float, default=0)
    losses = Column(Float, default=0)
    excise_tax = Column(Float, default=0)
