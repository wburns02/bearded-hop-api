import uuid
from sqlalchemy import Column, String, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    po_number = Column(String, unique=True, nullable=False)
    supplier = Column(String, nullable=False)
    items = Column(JSON, default=list)
    total_cost = Column(Float, default=0)
    status = Column(String, default="draft")
    order_date = Column(String, nullable=True)
    eta = Column(String, nullable=True)
    received_date = Column(String, nullable=True)
    notes = Column(String, nullable=True)
