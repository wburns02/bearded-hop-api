import uuid
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    current_stock = Column(Float, default=0)
    unit = Column(String, default="")
    par_level = Column(Float, default=0)
    reorder_point = Column(Float, default=0)
    cost_per_unit = Column(Float, default=0)
    supplier = Column(String, default="")
    last_ordered = Column(String, nullable=True)
    expiration_date = Column(String, nullable=True)
    location = Column(String, default="")
