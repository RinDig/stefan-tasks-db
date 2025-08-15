"""
User model
"""
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base
from app.models.base import BaseModel

class User(Base, BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    google_id = Column(String(255), unique=True)
    preferences = Column(JSONB, default={})