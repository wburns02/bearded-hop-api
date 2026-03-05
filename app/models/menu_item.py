import uuid
from sqlalchemy import Column, String, Float, Boolean, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    category = Column(String, nullable=False)
    price = Column(Float, default=0)
    cost = Column(Float, default=0)
    is_available = Column(Boolean, default=True)
    allergens = Column(JSON, default=list)
    dietary_tags = Column(JSON, default=list)
    is_kids_friendly = Column(Boolean, default=False)
    popularity = Column(Integer, default=0)
    image_url = Column(String, nullable=True)
