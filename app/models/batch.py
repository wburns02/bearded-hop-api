import uuid
from sqlalchemy import Column, String, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Batch(Base):
    __tablename__ = "batches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_number = Column(String, nullable=False, unique=True)
    beer_id = Column(UUID(as_uuid=True), nullable=True)
    beer_name = Column(String, default="")
    style = Column(String, default="")
    recipe_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(String, nullable=False, default="planned")
    brew_date = Column(String, nullable=True)
    target_og = Column(Float, default=0)
    actual_og = Column(Float, nullable=True)
    target_fg = Column(Float, default=0)
    actual_fg = Column(Float, nullable=True)
    abv = Column(Float, nullable=True)
    tank_id = Column(String, default="")
    volume = Column(Float, default=0)
    notes = Column(String, default="")
    gravity_readings = Column(JSON, default=list)
    temperature_log = Column(JSON, default=list)
    quality_score = Column(Integer, nullable=True)
