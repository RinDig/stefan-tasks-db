# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Stefan's Task Management System - A simple, functional Kanban board for managing concrete painting operations. Currently deployed and operational with 25 real tasks from Stefan's business.

## Current Architecture

```
Frontend (HTML/JS) → FastAPI Backend → PostgreSQL
     ↓                      ↓              ↓
  Render.com          Render.com      Render.com
```

## Live URLs

- **Frontend**: https://stefan-tasks-db-1.onrender.com
- **Backend API**: https://stefan-tasks-db.onrender.com

## Project Structure

```
/Kanban App/
├── frontend/
│   └── index.html           # Complete UI with inline styles and JS
├── backend/
│   ├── simple_api_postgres.py   # FastAPI backend (deployed)
│   ├── seed_data.py         # Seeds Stefan's 25 real tasks
│   └── requirements.txt     # Python dependencies
├── docs/
│   └── context.md           # Project history and context
└── CLAUDE.md                # This file
```

## Development Commands

### Backend (FastAPI)
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server
uvicorn simple_api_postgres:app --reload --port 8001

# Seed Stefan's data
python seed_data.py https://stefan-tasks-db.onrender.com
```

### Frontend
```bash
# No build process needed - pure HTML/CSS/JS
# For local testing:
python -m http.server 8000
```

## Core Data Structure

Tasks follow this schema:
```json
{
  "id": "uuid",
  "title": "string",
  "category": "concrete|customer|crew|materials|internal|planning|personal",
  "priority": "urgent|high|normal",
  "column": "backlog|this-week|in-progress|done",
  "metadata": {
    "client": "string",
    "notes": "string",
    "due_date": "string",
    "emoji": "string",
    "auto_created": boolean
  }
}
```

## API Endpoints (Implemented)

- `GET /tasks` - Get all tasks
- `POST /tasks` - Create new task
- `PUT /tasks/{id}` - Update task (move columns, edit fields)
- `DELETE /tasks/{id}` - Delete task
- `GET /health` - Health check

## Key Features (Completed)

✅ **Phase 1 Complete**: Core MVP with Kanban functionality
- Drag-and-drop between columns
- Category filtering
- Priority indicators (Urgent/Today, High, Normal)
- Modal-based editing (no browser prompts)
- PostgreSQL persistence
- Real-time save on actions
- 25 pre-loaded real tasks

## Future Enhancements (Not Yet Implemented)

When implementing future features, use specialized sub-agents for planning:

### Integration Features
- **Gmail integration** → Use `gmail-monday-integration-planner` agent
- **Monday.com sync** → Use `gmail-monday-integration-planner` agent
- **SMS notifications** → Use `notification-system-architect` agent
- **n8n automations** → Use `n8n-workflow-designer` agent

### Technical Enhancements
- **Database changes** → Use `database-state-architect` agent
- **API expansions** → Use `fastapi-backend-architect` agent
- **AI/MCP features** → Use `mcp-server-architect` agent

## Implementation Notes

- Frontend uses pure HTML/CSS/JavaScript (no build process)
- All styles and scripts are inline in index.html for simplicity
- Backend is a single FastAPI file for easy deployment
- Database connection via environment variable DATABASE_URL
- CORS configured for production URLs

## Deployment

Both services deployed on Render.com:
1. Backend connects to Render PostgreSQL
2. Frontend served as static site
3. Auto-deploys from GitHub master branch

## Testing Locally

```bash
# Terminal 1: Backend
cd backend
export DATABASE_URL="your_postgres_url"
uvicorn simple_api_postgres:app --reload --port 8001

# Terminal 2: Frontend
cd frontend
python -m http.server 8000
# Open http://localhost:8000
```

## Security Considerations

- Database URL stored as environment variable
- CORS restricted to production frontend URL
- Input validation on all API endpoints
- No credentials in repository

## When Making Changes

1. Test locally first with both frontend and backend running
2. Ensure API_URL in frontend matches backend location
3. Run seed_data.py to populate test data
4. Commit and push to trigger auto-deployment

## Current State

The system is fully functional and deployed. Stefan can:
- View and manage all 25 real tasks
- Drag tasks between columns
- Add/edit/delete tasks with modal interface
- Filter by category
- See priority indicators and due dates

Focus is on stability and usability. Future integrations will be added incrementally.