"""
Category API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import Category
from app.schemas import CategoryResponse

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """Get all active categories"""
    categories = db.query(Category).filter(
        Category.is_active == True
    ).order_by(Category.sort_order).all()
    
    return categories