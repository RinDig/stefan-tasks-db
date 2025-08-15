"""
Category schemas
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    color_code: str
    icon_emoji: str | None
    sort_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True