import uuid
from sqlalchemy import Column, String, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class WholesaleOrder(Base):
    __tablename__ = "wholesale_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String, unique=True, nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("wholesale_accounts.id"), nullable=False)
    account_name = Column(String, default="")
    items = Column(JSON, default=list)
    total = Column(Float, default=0)
    status = Column(String, default="pending")
    order_date = Column(String, nullable=True)
    delivery_date = Column(String, nullable=True)
    payment_status = Column(String, default="current")
    notes = Column(String, nullable=True)
