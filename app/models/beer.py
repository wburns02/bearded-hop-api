import uuid
from sqlalchemy import Column, String, Float, Integer, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Beer(Base):
    __tablename__ = "beers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    style = Column(String, nullable=False)
    abv = Column(Float, nullable=False)
    ibu = Column(Integer, default=0)
    srm = Column(Integer, default=0)
    description = Column(String, default="")
    tasting_notes = Column(String, default="")
    food_pairings = Column(JSON, default=list)
    status = Column(String, nullable=False, default="planned")  # on-tap/fermenting/conditioning/planned/archived
    tap_number = Column(Integer, nullable=True)
    keg_level = Column(Float, nullable=True)
    batch_id = Column(String, nullable=True)
    rating = Column(Float, default=0)
    total_pours = Column(Integer, default=0)
    category = Column(String, default="flagship")  # flagship/seasonal/limited/experimental
    is_non_alcoholic = Column(Boolean, default=False)
