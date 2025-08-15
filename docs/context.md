# Stefan's Task Management System - Project Context

## Current Status
- Project initialized: 2025-08-15
- Stage: **MVP COMPLETE & WORKING**
- Backend: Running on port 8000
- Frontend: Running on port 3000
- Database: Live on Render PostgreSQL
- Next milestone: Gmail & Monday.com integration

## Project Goal
Build a Kanban-based task management system for Stefan's painting business that automatically processes emails, syncs with Monday.com, sends SMS alerts, and uses AI to intelligently organize tasks.

## Architecture Decisions
*To be updated as sub-agents provide research and decisions are made*

### Technology Stack (Planned)
- **Frontend**: React (or vanilla HTML/JS for MVP)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **AI Brain**: Claude MCP Server
- **Automation**: n8n workflows
- **Hosting**: Vercel (frontend) + Railway (backend)

## Completed Research
*Links to sub-agent architecture plans will be added here*

- [x] Gmail integration plan - `/docs/architecture/integration-plan.md`
- [x] Monday.com sync architecture - `/docs/architecture/integration-plan.md`
- [ ] Database schema design
- [ ] MCP server architecture
- [ ] Notification system design
- [ ] Automation workflow plans
- [ ] FastAPI backend structure

## Implementation Progress

### Phase 1: Core MVP
- [x] Basic HTML/JavaScript Kanban board
- [x] API-based persistence
- [x] Drag and drop functionality
- [x] Category filtering
- [x] Column management (Backlog, This Week, In Progress, Done)

### Phase 2: Backend & Database
- [x] FastAPI server setup
- [x] PostgreSQL database on Render
- [x] Task CRUD endpoints
- [x] Data persistence layer
- [x] CORS configuration

### Phase 3: Email Integration
- [ ] Gmail API authentication
- [ ] Email polling/webhook setup
- [ ] MCP agent for email analysis
- [ ] Auto-task creation from emails
- [ ] Email categorization logic

### Phase 4: External Integrations
- [ ] Monday.com two-way sync
- [ ] Google Calendar integration
- [ ] Twilio SMS notifications
- [ ] Daily digest automation

### Phase 5: Automation & Intelligence
- [ ] n8n workflow server
- [ ] MCP agent brain
- [ ] Smart task prioritization
- [ ] Automated responses
- [ ] Weather-based alerts

## Key Technical Choices
*Updated as implementation proceeds*

### Data Model
- Task schema defined in CLAUDE.md
- Categories: concrete, customer, crew, personal
- Priority levels: urgent, high, normal
- Columns: backlog, this-week, in-progress, done

### Integration Points
*Documented as built*

- Gmail API: Push notifications via Cloud Pub/Sub with OAuth 2.0 (see integration-plan.md)
- Monday.com: Bidirectional GraphQL sync with webhooks (see integration-plan.md)
- Twilio: [SMS gateway configuration TBD]
- MCP Server: [Tool schemas TBD]

## Known Constraints
- Budget: ~$25/month for hosting
- Mobile-first UI requirement
- Real-time sync needed
- Offline capability desired
- Must handle 100+ tasks efficiently

## Development Notes
*Add important discoveries and decisions here*

### Key Architectural Decisions (2025-08-15)
- **Gmail Integration**: Push notifications recommended over polling for real-time processing
- **Monday.com Sync**: Bidirectional sync with last-writer-wins conflict resolution
- **Rate Limiting**: Exponential backoff with circuit breakers for both APIs
- **Data Flow**: Kanban database as primary source of truth
- **Estimated Timeline**: 12 weeks implementation in 4 phases

## Testing Strategy
*To be defined based on sub-agent recommendations*

## Deployment Pipeline
*To be configured based on architecture decisions*