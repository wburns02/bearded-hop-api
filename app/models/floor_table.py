import uuid
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class FloorTable(Base):
    __tablename__ = "floor_tables"

    id = Column(String, primary_key=True)  # e.g. "T-1"
    zone = Column(String, nullable=False)
    label = Column(String, nullable=False)
    seats = Column(Integer, default=4)
    x = Column(Float, default=0)
    y = Column(Float, default=0)
    shape = Column(String, default="rect")
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    radius = Column(Float, nullable=True)
    status = Column(String, default="available")
    current_tab_id = Column(String, nullable=True)
    current_customer_name = Column(String, nullable=True)
    current_customer_id = Column(String, nullable=True)
    party_size = Column(Integer, nullable=True)
    server_id = Column(String, nullable=True)
    server_name = Column(String, nullable=True)
    seated_at = Column(String, nullable=True)
    reservation_id = Column(String, nullable=True)
