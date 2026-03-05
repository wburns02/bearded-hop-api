import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class CustomerNote(Base):
    __tablename__ = "customer_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    date = Column(String, nullable=False)
    author = Column(String, default="")
    type = Column(String, default="note")  # note/call/email/complaint/compliment/milestone
    content = Column(String, default="")
