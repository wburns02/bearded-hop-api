from __future__ import annotations

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Email Campaign
# ---------------------------------------------------------------------------

class EmailCampaignBase(BaseModel):
    name: str
    subject: str = ""
    status: str = "draft"
    segment: str = ""
    sent_date: Optional[date] = None
    scheduled_date: Optional[date] = None
    recipients: int = 0
    opened: int = 0
    clicked: int = 0
    unsubscribed: int = 0
    type: str = "newsletter"


class EmailCampaignCreate(EmailCampaignBase):
    pass


class EmailCampaignUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    status: Optional[str] = None
    segment: Optional[str] = None
    sent_date: Optional[date] = None
    scheduled_date: Optional[date] = None
    recipients: Optional[int] = None
    opened: Optional[int] = None
    clicked: Optional[int] = None
    unsubscribed: Optional[int] = None
    type: Optional[str] = None


class EmailCampaignResponse(EmailCampaignBase):
    id: UUID

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Social Metrics
# ---------------------------------------------------------------------------

class SocialMetricsResponse(BaseModel):
    id: UUID
    date: date
    instagram_followers: int = 0
    facebook_likes: int = 0
    untappd_checkins: int = 0
    google_review_count: int = 0
    google_rating: float = 0
    instagram_engagement: float = 0
    facebook_engagement: float = 0

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Content Calendar
# ---------------------------------------------------------------------------

class ContentCalendarBase(BaseModel):
    date: date
    platform: str
    caption: str = ""
    status: str = "planned"
    type: str = "photo"


class ContentCalendarCreate(ContentCalendarBase):
    pass


class ContentCalendarUpdate(BaseModel):
    date: Optional[date] = None
    platform: Optional[str] = None
    caption: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class ContentCalendarResponse(ContentCalendarBase):
    id: UUID

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Customer Segment
# ---------------------------------------------------------------------------

class CustomerSegmentResponse(BaseModel):
    id: UUID
    name: str
    count: int = 0
    avg_spend: float = 0
    visit_frequency: str = ""
    top_beer: str = ""
    suggested_campaign: str = ""
    color: str = ""

    model_config = {"from_attributes": True}
