import uuid
from sqlalchemy import Column, String, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class POSTransaction(Base):
    __tablename__ = "pos_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_name = Column(String, default="")
    items = Column(JSON, default=list)
    subtotal = Column(Float, default=0)
    tax = Column(Float, default=0)
    discount = Column(Float, nullable=True)
    discount_type = Column(String, nullable=True)
    total = Column(Float, default=0)
    payment_method = Column(String, default="card")
    server = Column(String, default="")
    closed_at = Column(String, nullable=False)
    tip_amount = Column(Float, nullable=True)
