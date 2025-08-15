"""
Column model
"""
from sqlalchemy import Column, String, Integer, Boolean
from app.core.database import Base
from app.models.base import BaseModel

class Column(Base, BaseModel):
    __tablename__ = "columns"
    
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    color_code = Column(String(7), nullable=False)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)