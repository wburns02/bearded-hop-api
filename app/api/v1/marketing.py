from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser
from app.models.email_campaign import EmailCampaign
from app.models.social_metrics import SocialMetrics
from app.models.content_calendar import ContentCalendar
from app.models.customer_segment import CustomerSegment
from app.schemas.marketing import (
    EmailCampaignCreate,
    EmailCampaignUpdate,
    EmailCampaignResponse,
    SocialMetricsResponse,
    ContentCalendarCreate,
    ContentCalendarUpdate,
    ContentCalendarResponse,
    CustomerSegmentResponse,
)

router = APIRouter(prefix="/marketing", tags=["marketing"])


# ---------------------------------------------------------------------------
# Email Campaigns
# ---------------------------------------------------------------------------

@router.get("/campaigns", response_model=list[EmailCampaignResponse])
async def list_campaigns(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(EmailCampaign))
    return result.scalars().all()


@router.post("/campaigns", response_model=EmailCampaignResponse)
async def create_campaign(body: EmailCampaignCreate, db: DbSession, current_user: CurrentUser):
    campaign = EmailCampaign(**body.model_dump())
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return campaign


@router.patch("/campaigns/{id}", response_model=EmailCampaignResponse)
async def update_campaign(id: UUID, body: EmailCampaignUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(EmailCampaign).where(EmailCampaign.id == id))
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Email campaign not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(campaign, field, value)
    await db.commit()
    await db.refresh(campaign)
    return campaign


# ---------------------------------------------------------------------------
# Social Metrics
# ---------------------------------------------------------------------------

@router.get("/social-metrics", response_model=list[SocialMetricsResponse])
async def list_social_metrics(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(SocialMetrics))
    return result.scalars().all()


# ---------------------------------------------------------------------------
# Content Calendar
# ---------------------------------------------------------------------------

@router.get("/content-calendar", response_model=list[ContentCalendarResponse])
async def list_content_calendar(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(ContentCalendar))
    return result.scalars().all()


@router.post("/content-calendar", response_model=ContentCalendarResponse)
async def create_content_entry(body: ContentCalendarCreate, db: DbSession, current_user: CurrentUser):
    data = body.model_dump()
    data["date"] = str(data["date"])
    entry = ContentCalendar(**data)
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


@router.patch("/content-calendar/{id}", response_model=ContentCalendarResponse)
async def update_content_entry(id: UUID, body: ContentCalendarUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(ContentCalendar).where(ContentCalendar.id == id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Content calendar entry not found")
    data = body.model_dump(exclude_unset=True)
    if "date" in data and data["date"] is not None:
        data["date"] = str(data["date"])
    for field, value in data.items():
        setattr(entry, field, value)
    await db.commit()
    await db.refresh(entry)
    return entry


# ---------------------------------------------------------------------------
# Customer Segments
# ---------------------------------------------------------------------------

@router.get("/segments", response_model=list[CustomerSegmentResponse])
async def list_segments(db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(CustomerSegment))
    return result.scalars().all()
