import uuid
from sqlalchemy import Column, String, Float, Integer, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)
    anniversary = Column(String, nullable=True)
    first_visit = Column(String, nullable=True)
    last_visit = Column(String, nullable=True)
    total_visits = Column(Integer, default=0)
    total_spent = Column(Float, default=0)
    avg_ticket = Column(Float, default=0)
    favorite_beers = Column(JSON, default=list)
    dietary_restrictions = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    loyalty_points = Column(Integer, default=0)
    loyalty_tier = Column(String, default="Bronze")
    mug_club_member = Column(Boolean, default=False)
    mug_club_tier = Column(String, nullable=True)
    notes = Column(String, default="")
    source = Column(String, default="")
    family_members = Column(JSON, default=list)
