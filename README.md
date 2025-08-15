# Stefan's Task Management System

A simple, functional Kanban board for managing concrete painting operations, deployed and ready to use.

## Live Application

- **Frontend**: https://stefan-tasks-db-1.onrender.com
- **Backend API**: https://stefan-tasks-db.onrender.com

## Features

- ✅ Drag-and-drop Kanban board with 4 columns (Backlog, This Week, In Progress, Done)
- ✅ Task categories: Customer, Concrete, Crew, Materials, Internal, Planning, Personal
- ✅ Priority levels with visual indicators (Urgent/Today, High, Normal)
- ✅ Modal-based task editing (no more browser prompts!)
- ✅ Persistent PostgreSQL storage
- ✅ Real-time save on drag-and-drop
- ✅ Category filtering
- ✅ 25 pre-loaded real tasks from Stefan's operations

## Project Structure

```
/Kanban App/
├── frontend/
│   └── index.html          # Complete UI with inline styles and JS
├── backend/
│   ├── simple_api_postgres.py  # FastAPI backend (deployed)
│   ├── seed_data.py        # Load Stefan's real task data
│   └── requirements.txt    # Python dependencies
├── docs/
│   └── context.md          # Project context and history
└── README.md               # This file
```

## Tech Stack

- **Frontend**: Pure HTML/CSS/JavaScript (no build process needed)
- **Backend**: FastAPI + PostgreSQL
- **Hosting**: Render.com (both frontend and backend)
- **Database**: PostgreSQL on Render

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt

# Set environment variable for database
export DATABASE_URL="your_postgres_url"

# Run server
uvicorn simple_api_postgres:app --reload --port 8001
```

### Frontend
Simply open `frontend/index.html` in a browser, or serve it:
```bash
cd frontend
python -m http.server 8000
```

## Seeding Data

To load Stefan's 25 real tasks:
```bash
cd backend
python seed_data.py https://stefan-tasks-db.onrender.com
```

## Task Data Structure

```json
{
  "id": "uuid",
  "title": "Task description",
  "category": "customer|concrete|crew|materials|internal|planning|personal",
  "priority": "urgent|high|normal",
  "column": "backlog|this-week|in-progress|done",
  "metadata": {
    "client": "Client Name",
    "notes": "Additional notes",
    "due_date": "2025-01-15",
    "emoji": "📌",
    "auto_created": false
  }
}
```

## API Endpoints

- `GET /tasks` - Get all tasks
- `POST /tasks` - Create new task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `GET /health` - Health check

## Future Enhancements

The system is ready for future integrations:
- Gmail API for email-to-task conversion
- Monday.com two-way sync
- Twilio SMS notifications
- Google Calendar integration
- n8n automation workflows

## Deployment

Both frontend and backend are deployed on Render.com:
1. Backend uses PostgreSQL database (already configured)
2. Frontend served as static site
3. Automatic deploys from GitHub master branch

## Support

For issues or questions, contact the development team or check the project documentation in `docs/context.md`