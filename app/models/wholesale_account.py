import uuid
from sqlalchemy import Column, String, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class WholesaleAccount(Base):
    __tablename__ = "wholesale_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_name = Column(String, nullable=False)
    contact_name = Column(String, default="")
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, default="")
    type = Column(String, default="bar")
    status = Column(String, default="active")
    total_orders = Column(Integer, default=0)
    total_revenue = Column(Float, default=0)
    last_order = Column(String, nullable=True)
    kegs_out = Column(Integer, default=0)
    credit_limit = Column(Float, default=0)
    payment_terms = Column(String, default="Net 30")
    notes = Column(String, default="")
    taps_carrying = Column(JSON, default=list)
