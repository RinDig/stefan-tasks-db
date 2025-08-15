"""
User schemas
"""
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Dict, Any

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    google_id: str | None
    preferences: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True