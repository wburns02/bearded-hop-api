import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class ContentCalendar(Base):
    __tablename__ = "content_calendar"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    caption = Column(String, default="")
    status = Column(String, default="planned")
    type = Column(String, default="photo")
