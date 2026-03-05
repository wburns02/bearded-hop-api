import uuid
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("pos_transactions.id"), nullable=False)
    name = Column(String, nullable=False)
    size = Column(String, default="")
    price = Column(Float, default=0)
    qty = Column(Integer, default=1)
