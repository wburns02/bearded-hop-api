import uuid
from sqlalchemy import Column, String, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    style = Column(String, nullable=False)
    batch_size = Column(Float, default=0)
    og = Column(Float, default=0)
    fg = Column(Float, default=0)
    abv = Column(Float, default=0)
    ibu = Column(Integer, default=0)
    srm = Column(Integer, default=0)
    grains = Column(JSON, default=list)
    hops = Column(JSON, default=list)
    yeast = Column(String, default="")
    water_profile = Column(String, default="")
    mash_temp = Column(Integer, default=0)
    mash_time = Column(Integer, default=0)
    boil_time = Column(Integer, default=0)
    notes = Column(String, default="")
    versions = Column(Integer, default=1)
