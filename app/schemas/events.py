from __future__ import annotations

from datetime import date, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    type: str
    date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: str = ""
    performer_id: Optional[UUID] = None
    capacity: int = 0
    tickets_sold: int = 0
    ticket_price: float = 0
    is_ticketed: bool = False
    is_family_friendly: bool = True
    location: str = "taproom"
    status: str = "upcoming"
    revenue: float = 0
    special_beer: Optional[str] = None
    image_url: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: Optional[str] = None
    performer_id: Optional[UUID] = None
    capacity: Optional[int] = None
    tickets_sold: Optional[int] = None
    ticket_price: Optional[float] = None
    is_ticketed: Optional[bool] = None
    is_family_friendly: Optional[bool] = None
    location: Optional[str] = None
    status: Optional[str] = None
    revenue: Optional[float] = None
    special_beer: Optional[str] = None
    image_url: Optional[str] = None


class EventResponse(EventBase):
    id: UUID

    model_config = {"from_attributes": True}
