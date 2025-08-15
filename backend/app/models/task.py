"""
Task model
"""
from sqlalchemy import Column, String, Text, ForeignKey, Boolean, Integer, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModel

class Task(Base, BaseModel):
    __tablename__ = "tasks"
    
    title = Column(String(500), nullable=False)
    description = Column(Text)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    column_id = Column(UUID(as_uuid=True), ForeignKey("columns.id"))
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"))
    priority = Column(String(20), default="normal")
    status = Column(String(20), default="active")
    due_date = Column(Date)
    estimated_hours = Column(Integer)
    actual_hours = Column(Integer)
    task_metadata = Column("metadata", JSONB, default={})  # Renamed to avoid conflict
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    monday_com_id = Column(String(100))
    google_calendar_id = Column(String(255))
    version = Column(Integer, default=1)
    is_deleted = Column(Boolean, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    category = relationship("Category", backref="tasks")
    column = relationship("Column", backref="tasks")
    client = relationship("Client", backref="tasks")