from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    original_url: str = Field(description="The original URL to be shortened")

class URLRead(BaseModel):
    id: UUID
    original_url: str
    short_id: str
    expired_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        orm_mode = True