# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Stefan's Operations Hub - a Kanban-based task management system designed for concrete coordination and client management. The system will integrate with Gmail, Monday.com, Google Calendar, and Twilio for automated task creation and notifications.

## Architecture

The planned architecture follows this flow:
```
User Interface (React) → FastAPI Backend → MCP Server → External Services
                              ↓
                        PostgreSQL DB
                              ↓
                     Integration Layer:
                     - Gmail API
                     - Monday.com
                     - Google Calendar  
                     - Twilio SMS
```

## Development Commands

Since the project is in initial development, use these commands as implementation progresses:

### Frontend (React)
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests (when implemented)
npm test
```

### Backend (FastAPI)
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests (when implemented)
pytest
```

## Core Data Structure

Tasks follow this schema:
```json
{
  "id": "uuid",
  "title": "string",
  "category": "concrete|customer|crew|personal",
  "priority": "urgent|high|normal",
  "column": "backlog|this-week|in-progress|done",
  "metadata": {
    "client": "string",
    "related_emails": [],
    "due_date": "string",
    "auto_created": boolean
  }
}
```

## API Endpoints

Core endpoints to implement:
- `GET /tasks` - Load board state
- `POST /tasks` - Create task
- `PUT /tasks/{id}` - Update/move task
- `DELETE /tasks/{id}` - Delete task
- `POST /agent/process` - MCP agent task processing
- `POST /agent/analyze` - Analyze email/text for task creation

## Development Phases

The project follows this implementation roadmap:

1. **Phase 1**: Core MVP with basic Kanban functionality
2. **Phase 2**: Email integration via Gmail API
3. **Phase 3**: Automation layer with n8n workflows
4. **Phase 4**: Two-way sync with Monday.com and Google Calendar

## Key Implementation Notes

- Start with localStorage for persistence, then migrate to PostgreSQL
- Use FastAPI middleware for CORS handling
- Implement drag-and-drop using HTML5 drag events
- Category colors and filters should be data-driven for reusability
- MCP integration uses Claude MCP Python SDK for intelligent task processing

## Testing Approach

When implementing tests:
- Frontend: Use Jest and React Testing Library
- Backend: Use pytest with FastAPI TestClient
- Integration: Test MCP agent responses with mock data
- E2E: Consider Playwright for critical user flows

## Deployment

Planned deployment stack:
- Frontend: Vercel or GitHub Pages
- Backend: Railway or Render
- Database: PostgreSQL (Railway addon or separate)
- Automation: n8n (self-hosted or cloud)

## Available Sub-Agents

This project has specialized sub-agents available. You MUST use them for planning before implementation:

1. **gmail-monday-integration-planner** - Research and design Gmail/Monday.com integrations
2. **database-state-architect** - Design database schemas and state management
3. **mcp-server-architect** - Plan MCP server architecture for AI features
4. **notification-system-architect** - Design notification and alert systems
5. **n8n-workflow-designer** - Create automation workflow plans
6. **fastapi-backend-architect** - Design FastAPI backend architecture

## CRITICAL: Sub-Agent Delegation Rules

### When to Delegate (MANDATORY)
Before implementing ANY of these features, delegate to the appropriate sub-agent:
- Gmail/email integration → gmail-monday-integration-planner
- Database setup → database-state-architect
- AI/Claude features → mcp-server-architect
- SMS/notifications → notification-system-architect
- Automation workflows → n8n-workflow-designer
- API endpoints/backend → fastapi-backend-architect

### How to Delegate
When a feature requires planning:
1. Use the Task tool with the appropriate subagent_type
2. Provide clear context about Stefan's task management system
3. Wait for the agent's plan
4. ONLY THEN proceed with implementation based on their research

### Implementation Workflow
1. Receive feature request
2. Identify which sub-agent(s) needed
3. Delegate research/planning to sub-agent(s)
4. Review generated plans
5. Create implementation checklist from plans
6. Implement following the researched approach
7. Update this file with implementation decisions

### Feature-to-Agent Mapping
| Feature | Required Sub-Agent | Purpose |
|---------|-------------------|---------|
| Gmail integration | gmail-monday-integration-planner | Integration strategy and API planning |
| Monday.com sync | gmail-monday-integration-planner | Webhook and sync architecture |
| Database schema | database-state-architect | Schema design and migrations |
| Offline support | database-state-architect | State sync and conflict resolution |
| API structure | fastapi-backend-architect | Endpoint design and middleware |
| WebSocket real-time | fastapi-backend-architect | Real-time communication planning |
| MCP agent brain | mcp-server-architect | Tool schemas and context management |
| Email notifications | notification-system-architect | Email template and delivery strategy |
| SMS alerts | notification-system-architect | Twilio integration and alert logic |
| Daily digests | n8n-workflow-designer | Automated summary workflows |
| Task automation | n8n-workflow-designer | Trigger-based automations |

## Context Management

### Project Context File
Maintain project context in: `docs/context.md`
- Update after EVERY major decision or implementation
- Include architecture decisions, completed features, and integration details

### Documentation Structure
```
/Kanban App/
├── docs/
│   ├── context.md           # Living project context
│   ├── architecture/        # Sub-agent architecture plans
│   └── implementation/      # Implementation notes
├── frontend/                # React/HTML frontend
├── backend/                 # FastAPI backend
└── automations/            # n8n workflows
```

## Anti-Patterns to AVOID
- ❌ Implementing features without consulting sub-agents
- ❌ Ignoring sub-agent research/plans
- ❌ Starting coding before reading all relevant plans
- ❌ Not documenting implementation decisions

## Security Considerations

- Never commit API keys or credentials
- Use environment variables for all sensitive configuration
- Implement proper authentication before production deployment
- Validate all user inputs on both frontend and backend
- Use HTTPS for all API communications