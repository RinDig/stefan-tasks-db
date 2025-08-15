"""
Client schemas
"""
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any

class ClientBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    contact_info: Dict[str, Any] = {}

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID]
    
    class Config:
        from_attributes = True