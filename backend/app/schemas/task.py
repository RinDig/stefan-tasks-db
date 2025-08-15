"""
Task schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import date, datetime
from uuid import UUID

class TaskBase(BaseModel):
    title: str = Field(..., max_length=500)
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    column_id: Optional[UUID] = None
    client_id: Optional[UUID] = None
    priority: str = Field(default="normal", pattern="^(urgent|high|normal|low)$")
    status: str = Field(default="active", pattern="^(active|completed|cancelled)$")
    due_date: Optional[date] = None
    estimated_hours: Optional[int] = None
    task_metadata: Dict[str, Any] = Field(default_factory=dict)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    column_id: Optional[UUID] = None
    client_id: Optional[UUID] = None
    priority: Optional[str] = Field(None, pattern="^(urgent|high|normal|low)$")
    status: Optional[str] = Field(None, pattern="^(active|completed|cancelled)$")
    due_date: Optional[date] = None
    estimated_hours: Optional[int] = None
    actual_hours: Optional[int] = None
    task_metadata: Optional[Dict[str, Any]] = None
    version: Optional[int] = None  # For optimistic locking

class TaskResponse(TaskBase):
    id: UUID
    version: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    
    # Include related data
    category_name: Optional[str] = None
    column_name: Optional[str] = None
    client_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class TaskList(BaseModel):
    tasks: list[TaskResponse]
    total: int
    page: int = 1
    per_page: int = 100