"""
Client model
"""
from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base
from app.models.base import BaseModel

class Client(Base, BaseModel):
    __tablename__ = "clients"
    
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    notes = Column(Text)
    contact_info = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))