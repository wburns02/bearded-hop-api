import uuid
from sqlalchemy import Column, String, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class OpenTab(Base):
    __tablename__ = "open_tabs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_name = Column(String, nullable=False)
    customer_id = Column(UUID(as_uuid=True), nullable=True)
    items = Column(JSON, default=list)
    opened_at = Column(String, nullable=False)
    server = Column(String, default="")
    subtotal = Column(Float, default=0)
    table_number = Column(String, nullable=True)
