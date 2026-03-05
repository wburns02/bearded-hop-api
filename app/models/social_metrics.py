import uuid
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class SocialMetrics(Base):
    __tablename__ = "social_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(String, unique=True, nullable=False)
    instagram_followers = Column(Integer, default=0)
    facebook_likes = Column(Integer, default=0)
    untappd_checkins = Column(Integer, default=0)
    google_review_count = Column(Integer, default=0)
    google_rating = Column(Float, default=0)
    instagram_engagement = Column(Float, default=0)
    facebook_engagement = Column(Float, default=0)
