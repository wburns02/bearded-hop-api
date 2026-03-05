import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class BusinessSettings(Base):
    __tablename__ = "business_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_name = Column(String, default="Bearded Hop Brewery")
    address = Column(String, default="")
    phone = Column(String, default="")
    email = Column(String, default="")
    tax_rate = Column(String, default="8.25%")
    timezone = Column(String, default="America/Chicago (CST)")
    currency = Column(String, default="USD")
