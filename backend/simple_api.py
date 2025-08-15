"""
Simple API for Stefan's Kanban Board
This is a simplified version that works with the frontend without complex UUID relationships
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
import json
import os

# Create FastAPI app
app = FastAPI(title="Stefan's Simple Task API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage (using JSON file for simplicity)
DATA_FILE = "tasks_db.json"

# Task model
class Task(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: Optional[str] = None
    title: str
    category: str  # concrete, customer, crew, materials, internal, planning, personal
    priority: str = "normal"  # urgent, high, normal
    column: str = "backlog"  # backlog, this-week, in-progress, done
    metadata: Optional[Dict[str, Any]] = {}

# Load tasks from file
def load_tasks() -> List[Dict]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Save tasks to file
def save_tasks(tasks: List[Dict]):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

# Initialize with empty list if file doesn't exist
if not os.path.exists(DATA_FILE):
    save_tasks([])

@app.get("/")
async def root():
    return {"message": "Stefan's Simple Task API", "endpoints": ["/tasks"]}

@app.get("/tasks")
async def get_tasks():
    """Get all tasks"""
    return load_tasks()

@app.post("/tasks")
async def create_task(task: Task):
    """Create a new task"""
    tasks = load_tasks()
    
    # Generate ID if not provided
    if not task.id:
        task.id = str(uuid.uuid4())
    
    # Convert to dict and add
    task_dict = task.model_dump()
    tasks.append(task_dict)
    
    # Save to file
    save_tasks(tasks)
    
    return task_dict

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    """Update an existing task"""
    tasks = load_tasks()
    
    # Find the task
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            # Update the task
            task.id = task_id  # Preserve the ID
            tasks[i] = task.model_dump()
            save_tasks(tasks)
            return tasks[i]
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    tasks = load_tasks()
    
    # Filter out the task
    original_count = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) == original_count:
        raise HTTPException(status_code=404, detail="Task not found")
    
    save_tasks(tasks)
    return {"message": "Task deleted"}

@app.delete("/tasks")
async def delete_all_tasks():
    """Delete all tasks (for testing)"""
    save_tasks([])
    return {"message": "All tasks deleted"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("simple_api:app", host="0.0.0.0", port=port, reload=False)