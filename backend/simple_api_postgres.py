"""
Simple API for Stefan's Kanban Board using PostgreSQL
This connects to your existing Render PostgreSQL database
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Stefan's Task API with PostgreSQL")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Allow all origins for now
        "https://stefan-tasks-db-1.onrender.com",  # Your frontend URL
        "http://localhost:3000",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    """Get connection to PostgreSQL database"""
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception("DATABASE_URL environment variable not set")
    
    # Render uses internal URL format, we might need to adjust
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    try:
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    except Exception as e:
        print(f"Database connection error: {e}")
        raise Exception(f"Database connection failed: {str(e)}")

# Task model
class Task(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: Optional[str] = None
    title: str
    category: str  # concrete, customer, crew, materials, internal, planning, personal
    priority: str = "normal"  # urgent, high, normal
    column: str = "backlog"  # backlog, this-week, in-progress, done
    metadata: Optional[Dict[str, Any]] = {}

# Initialize database table
def init_db():
    """Create tasks table if it doesn't exist"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS simple_tasks (
                id VARCHAR(255) PRIMARY KEY,
                title TEXT NOT NULL,
                category VARCHAR(50),
                priority VARCHAR(20),
                column_name VARCHAR(50),
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Initialize DB on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "Stefan's Task API", "status": "connected to PostgreSQL"}

@app.get("/tasks")
async def get_tasks():
    """Get all tasks"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, title, category, priority, column_name as column, metadata 
            FROM simple_tasks 
            ORDER BY created_at DESC
        """)
        
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert to list of dicts
        return [dict(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks")
async def create_task(task: Task):
    """Create a new task"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Generate ID if not provided
        if not task.id:
            task.id = str(uuid.uuid4())
        
        cur.execute("""
            INSERT INTO simple_tasks (id, title, category, priority, column_name, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, title, category, priority, column_name as column, metadata
        """, (
            task.id,
            task.title,
            task.category,
            task.priority,
            task.column,
            json.dumps(task.metadata)
        ))
        
        new_task = dict(cur.fetchone())
        conn.commit()
        cur.close()
        conn.close()
        
        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    """Update an existing task"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE simple_tasks 
            SET title = %s, category = %s, priority = %s, column_name = %s, 
                metadata = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, title, category, priority, column_name as column, metadata
        """, (
            task.title,
            task.category,
            task.priority,
            task.column,
            json.dumps(task.metadata),
            task_id
        ))
        
        updated_task = cur.fetchone()
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        conn.commit()
        cur.close()
        conn.close()
        
        return dict(updated_task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM simple_tasks WHERE id = %s RETURNING id", (task_id,))
        deleted = cur.fetchone()
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"message": "Task deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks")
async def delete_all_tasks():
    """Delete all tasks (for testing)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM simple_tasks")
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"message": "All tasks deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("simple_api_postgres:app", host="0.0.0.0", port=port, reload=False)