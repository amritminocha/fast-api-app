from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID

# --- Base Schema (Shared) ---
class UserBase(BaseModel):
    username: str = Field(min_length=10, max_length=80, description="Username must be between 10 and 80 characters")
    email: EmailStr = Field(description="Email must be a valid email address")


# --- Request Body: POST /users ---
class UserCreate(UserBase):
    password: str = Field(min_length=6, description="Password must be at least 6 characters long")


# --- Optional fields for PATCH ---
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=10, max_length=80)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


# --- Response Schema ---
class UserRead(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
