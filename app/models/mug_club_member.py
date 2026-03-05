import uuid
from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class MugClubMember(Base):
    __tablename__ = "mug_club_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    customer_name = Column(String, default="")
    tier = Column(String, default="Standard")
    member_since = Column(String, nullable=True)
    renewal_date = Column(String, nullable=True)
    mug_number = Column(Integer, default=0)
    mug_location = Column(String, default="")
    total_saved = Column(Float, default=0)
    visits_as_member = Column(Integer, default=0)
    referrals = Column(Integer, default=0)
    status = Column(String, default="active")
    benefits = Column(JSON, default=list)
