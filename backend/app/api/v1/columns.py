"""
Column API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import Column
from app.schemas import ColumnResponse

router = APIRouter()

@router.get("/", response_model=List[ColumnResponse])
async def get_columns(db: Session = Depends(get_db)):
    """Get all active columns"""
    columns = db.query(Column).filter(
        Column.is_active == True
    ).order_by(Column.sort_order).all()
    
    return columns