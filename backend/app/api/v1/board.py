"""
Board API - Get complete board state
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.models import Task, Category, Column, Client
from typing import Dict, List, Any

router = APIRouter()

@router.get("/")
async def get_board_state(db: Session = Depends(get_db)):
    """Get complete board state with all tasks organized by columns"""
    
    # Get all columns
    columns = db.query(Column).filter(
        Column.is_active == True
    ).order_by(Column.sort_order).all()
    
    # Get all categories
    categories = db.query(Category).filter(
        Category.is_active == True
    ).order_by(Category.sort_order).all()
    
    # Get all tasks with relationships
    tasks = db.query(Task).options(
        joinedload(Task.category),
        joinedload(Task.column),
        joinedload(Task.client)
    ).filter(Task.is_deleted == False).all()
    
    # Organize tasks by column
    board_data = {
        "columns": [],
        "categories": [
            {
                "id": str(cat.id),
                "name": cat.name,
                "slug": cat.slug,
                "color_code": cat.color_code,
                "icon_emoji": cat.icon_emoji
            } for cat in categories
        ],
        "statistics": {
            "total_tasks": len(tasks),
            "urgent_tasks": len([t for t in tasks if t.priority == "urgent"]),
            "high_priority": len([t for t in tasks if t.priority == "high"]),
            "completed_tasks": len([t for t in tasks if t.status == "completed"])
        }
    }
    
    for column in columns:
        column_tasks = [t for t in tasks if t.column_id == column.id]
        
        board_data["columns"].append({
            "id": str(column.id),
            "name": column.name,
            "slug": column.slug,
            "color_code": column.color_code,
            "task_count": len(column_tasks),
            "tasks": [
                {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "category_id": str(task.category_id) if task.category_id else None,
                    "category_name": task.category.name if task.category else None,
                    "category_color": task.category.color_code if task.category else None,
                    "client_name": task.client.name if task.client else None,
                    "priority": task.priority,
                    "status": task.status,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "version": task.version
                } for task in column_tasks
            ]
        })
    
    return board_data