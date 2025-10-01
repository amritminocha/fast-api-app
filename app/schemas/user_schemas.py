from pydantic import BaseModel, Field, EmailStr
from pydantic import ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    username: str = Field(min_length=10, max_length=80, description="Username must be between 10 and 80 characters")
    email: EmailStr = Field(description="Email must be a valid email address")

class UserCreate(UserBase):
    password: str = Field(min_length=6, description="Password must be at least 6 characters long")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=10, max_length=80)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

class UserRead(UserBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)