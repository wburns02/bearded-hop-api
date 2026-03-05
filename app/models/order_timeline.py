import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class OrderTimeline(Base):
    __tablename__ = "order_timelines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_id = Column(String, nullable=False)
    time = Column(String, nullable=False)
    action = Column(String, nullable=False)
    description = Column(String, default="")
