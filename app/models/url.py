from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.models.base import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(String, nullable=False)
    short_id = Column(String, nullable=False, unique=True, index=True)
    expired_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
