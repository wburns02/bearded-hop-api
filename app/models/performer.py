import uuid
from sqlalchemy import Column, String, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Performer(Base):
    __tablename__ = "performers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    genre = Column(String, default="")
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    fee = Column(Float, default=0)
    rating = Column(Float, default=0)
    past_performances = Column(Integer, default=0)
    bio = Column(String, default="")
    social_links = Column(JSON, default=list)
