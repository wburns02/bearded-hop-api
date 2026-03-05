import uuid
from sqlalchemy import Column, String, Float, Integer, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class DetailedRecipe(Base):
    __tablename__ = "detailed_recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    beer_id = Column(UUID(as_uuid=True), nullable=True)
    name = Column(String, nullable=False)
    style = Column(String, nullable=False)
    category = Column(String, default="flagship")
    version = Column(Integer, default=1)
    batch_size = Column(Float, default=0)
    target_og = Column(Float, default=0)
    target_fg = Column(Float, default=0)
    target_abv = Column(Float, default=0)
    target_ibu = Column(Integer, default=0)
    target_srm = Column(Integer, default=0)
    boil_time = Column(Integer, default=60)
    mash_temp = Column(Integer, default=152)
    mash_time = Column(Integer, default=60)
    grain_bill = Column(JSON, default=list)
    hop_schedule = Column(JSON, default=list)
    yeast = Column(JSON, default=dict)
    water_profile = Column(JSON, default=dict)
    water_adjustments = Column(JSON, default=list)
    brew_day_steps = Column(JSON, default=list)
    total_cost = Column(Float, default=0)
    cost_per_barrel = Column(Float, default=0)
    cost_per_pint = Column(Float, default=0)
    last_brewed = Column(String, nullable=True)
    total_batches = Column(Integer, default=0)
    brew_history = Column(JSON, default=list)
    notes = Column(String, default="")
    created_date = Column(String, nullable=True)
