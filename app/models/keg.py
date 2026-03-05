import uuid
from sqlalchemy import Column, String, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Keg(Base):
    __tablename__ = "kegs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keg_number = Column(String, unique=True, nullable=False)
    size = Column(String, nullable=False)  # 1/2, 1/4, 1/6, slim-1/4
    gallons = Column(Float, default=0)
    status = Column(String, default="clean-empty")
    current_beer_id = Column(UUID(as_uuid=True), nullable=True)
    current_beer_name = Column(String, nullable=True)
    batch_id = Column(UUID(as_uuid=True), nullable=True)
    location = Column(String, default="brewery-cold-room")
    deployed_to = Column(String, nullable=True)
    deployed_to_name = Column(String, nullable=True)
    deployed_date = Column(String, nullable=True)
    expected_return_date = Column(String, nullable=True)
    fill_date = Column(String, nullable=True)
    fill_count = Column(Integer, default=0)
    last_cleaned = Column(String, nullable=True)
    deposit = Column(Float, default=0)
    deposit_status = Column(String, default="not-applicable")
    purchase_date = Column(String, nullable=True)
    purchase_cost = Column(Float, default=0)
    notes = Column(String, default="")
    history = Column(JSON, default=list)
