from fastapi import APIRouter
from app.api.v1 import tasks, categories, columns, board, health

api_router = APIRouter()

# Include all routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
api_router.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
api_router.include_router(columns.router, prefix="/api/v1/columns", tags=["columns"])
api_router.include_router(board.router, prefix="/api/v1/board", tags=["board"])