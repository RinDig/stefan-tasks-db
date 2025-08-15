"""
Task API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from uuid import UUID
from app.core.database import get_db
from app.models import Task, Category, Column, Client
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskList

router = APIRouter()

@router.get("/", response_model=TaskList)
async def get_tasks(
    column_id: Optional[UUID] = Query(None),
    category_id: Optional[UUID] = Query(None),
    priority: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all tasks with optional filtering"""
    query = db.query(Task).filter(Task.is_deleted == False)
    
    # Apply filters
    if column_id:
        query = query.filter(Task.column_id == column_id)
    if category_id:
        query = query.filter(Task.category_id == category_id)
    if priority:
        query = query.filter(Task.priority == priority)
    
    # Get total count
    total = query.count()
    
    # Pagination
    offset = (page - 1) * per_page
    tasks = query.options(
        joinedload(Task.category),
        joinedload(Task.column),
        joinedload(Task.client)
    ).order_by(Task.created_at.desc()).offset(offset).limit(per_page).all()
    
    # Enrich response with related data
    task_responses = []
    for task in tasks:
        task_dict = task.__dict__.copy()
        task_dict['category_name'] = task.category.name if task.category else None
        task_dict['column_name'] = task.column.name if task.column else None
        task_dict['client_name'] = task.client.name if task.client else None
        task_responses.append(TaskResponse(**task_dict))
    
    return TaskList(
        tasks=task_responses,
        total=total,
        page=page,
        per_page=per_page
    )

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    task = db.query(Task).options(
        joinedload(Task.category),
        joinedload(Task.column),
        joinedload(Task.client)
    ).filter(Task.id == task_id, Task.is_deleted == False).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_dict = task.__dict__.copy()
    task_dict['category_name'] = task.category.name if task.category else None
    task_dict['column_name'] = task.column.name if task.column else None
    task_dict['client_name'] = task.client.name if task.client else None
    
    return TaskResponse(**task_dict)

@router.post("/", response_model=TaskResponse)
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    # Get the default user (Stefan) for now
    user = db.query(User).filter(User.email == "stefan@paintingbusiness.com").first()
    
    task = Task(**task_data.dict())
    if user:
        task.created_by = user.id
        task.updated_by = user.id
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Load relationships
    task = db.query(Task).options(
        joinedload(Task.category),
        joinedload(Task.column),
        joinedload(Task.client)
    ).filter(Task.id == task.id).first()
    
    task_dict = task.__dict__.copy()
    task_dict['category_name'] = task.category.name if task.category else None
    task_dict['column_name'] = task.column.name if task.column else None
    task_dict['client_name'] = task.client.name if task.client else None
    
    return TaskResponse(**task_dict)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update a task with optimistic locking"""
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check version for conflict detection
    if task_data.version and task.version != task_data.version:
        raise HTTPException(
            status_code=409,
            detail="Conflict detected. Task has been modified by another user."
        )
    
    # Update fields
    update_data = task_data.dict(exclude_unset=True, exclude={'version'})
    for field, value in update_data.items():
        setattr(task, field, value)
    
    # Increment version
    task.version += 1
    
    # Get the default user for updated_by
    user = db.query(User).filter(User.email == "stefan@paintingbusiness.com").first()
    if user:
        task.updated_by = user.id
    
    db.commit()
    db.refresh(task)
    
    # Load relationships
    task = db.query(Task).options(
        joinedload(Task.category),
        joinedload(Task.column),
        joinedload(Task.client)
    ).filter(Task.id == task.id).first()
    
    task_dict = task.__dict__.copy()
    task_dict['category_name'] = task.category.name if task.category else None
    task_dict['column_name'] = task.column.name if task.column else None
    task_dict['client_name'] = task.client.name if task.client else None
    
    return TaskResponse(**task_dict)

@router.delete("/{task_id}")
async def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    """Soft delete a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.is_deleted = True
    db.commit()
    
    return {"message": "Task deleted successfully"}

@router.post("/{task_id}/move")
async def move_task(
    task_id: UUID,
    column_id: UUID,
    db: Session = Depends(get_db)
):
    """Move a task to a different column"""
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Verify column exists
    column = db.query(Column).filter(Column.id == column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    
    task.column_id = column_id
    task.version += 1
    
    db.commit()
    
    return {"message": "Task moved successfully", "new_column": column.name}

# Import User model at the end to avoid circular imports
from app.models import User