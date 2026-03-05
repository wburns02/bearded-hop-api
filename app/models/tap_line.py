from sqlalchemy import Column, String, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class TapLine(Base):
    __tablename__ = "tap_lines"

    tap_number = Column(Integer, primary_key=True)
    beer_id = Column(UUID(as_uuid=True), nullable=True)
    beer_name = Column(String, nullable=True)
    style = Column(String, nullable=True)
    abv = Column(Float, nullable=True)
    ibu = Column(Integer, nullable=True)
    keg_level = Column(Float, default=100)
    keg_size = Column(String, default="1/2")
    tapped_date = Column(String, nullable=True)
    estimated_kick_date = Column(String, nullable=True)
    status = Column(String, default="active")  # active/empty/cleaning/reserved
    pour_sizes = Column(JSON, default=list)
    total_pours = Column(Integer, default=0)
    revenue_today = Column(Float, default=0)
