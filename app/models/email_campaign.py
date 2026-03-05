import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class EmailCampaign(Base):
    __tablename__ = "email_campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    subject = Column(String, default="")
    status = Column(String, default="draft")
    segment = Column(String, default="")
    sent_date = Column(String, nullable=True)
    scheduled_date = Column(String, nullable=True)
    recipients = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)
    unsubscribed = Column(Integer, default=0)
    type = Column(String, default="newsletter")
