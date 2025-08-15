## **Stefan's Operations Hub - Build Plan 🚀**

### **Architecture Overview:**
```
Stefan's Phone/Browser → Kanban UI → FastAPI Backend → MCP Server
                                           ↓
                                    Integration Layer
                                    ├── Gmail API
                                    ├── Monday.com
                                    ├── Google Calendar
                                    └── Twilio (SMS)
```

### **Phase 1: Core MVP (Week 1-2)**

**Tech Stack:**
- **Frontend:** React app (hosted on Vercel/GitHub Pages)
- **Backend:** FastAPI (Python) on Railway/Render
- **Database:** PostgreSQL (or SQLite for prototype)
- **MCP Server:** Claude MCP for agent brain

**Basic Features:**
```python
# Core task structure
{
  "id": "uuid",
  "title": "Contact DACG about Georgia",
  "category": "concrete",
  "priority": "urgent",
  "column": "this-week",
  "metadata": {
    "client": "DACG Concrete",
    "related_emails": [],
    "due_date": "today",
    "auto_created": false
  }
}
```

**Simple API endpoints:**
- `GET /tasks` - Load board state
- `POST /tasks` - Create task
- `PUT /tasks/{id}` - Update/move task
- `POST /agent/process` - Agent creates/updates tasks

### **Phase 2: Email Integration (Week 3)**

**Gmail Watcher + MCP Agent:**
```python
# Email processor pipeline
1. Gmail webhook/poll → 
2. MCP Agent analyzes →
3. Creates task card →
4. Categories: URGENT, SCHEDULE_REQUEST, MATERIAL_ORDER, FYI
```

**Smart Email Rules:**
- Keywords "start date", "pour date" → Create URGENT concrete task
- From: existing clients → Auto-tag with client name
- "delay", "pushed back" → Flag existing related tasks
- Materials/order confirmations → Create logistics task

### **Phase 3: Automation Layer (Week 4-5)**

**n8n Workflow Server** (or Zapier/Make for simpler):
```yaml
Workflows:
  - Email Triage:
      trigger: New email arrives
      action: Send to MCP → Create/update task
      
  - Daily Digest:
      trigger: 5:00 AM daily
      action: 
        - Get all 🔥 tasks
        - Get weather for job sites
        - Send SMS summary to Stefan
        
  - Task Completion:
      trigger: Task moved to "Done"
      action: 
        - If customer task → Draft completion email
        - If concrete coord → Update dependent tasks
```

### **Phase 4: Two-Way Sync (Week 6)**

**Monday.com Integration:**
- Webhooks for real-time updates
- Bi-directional sync (changes in either update both)
- Crew daily reports → Update task progress

**Google Calendar:**
- Task due dates → Calendar events
- Calendar changes → Update task dates

### **Implementation Path - SIMPLEST TO START:**

#### **Week 1: Static + Storage**
```javascript
// 1. Take existing HTML Kanban
// 2. Add localStorage for persistence
// 3. Add basic API calls to Python backend
// 4. Deploy on GitHub Pages + Railway

const api = {
  saveBoard: async (state) => {
    await fetch(`${API_URL}/board`, {
      method: 'POST',
      body: JSON.stringify(state)
    });
  },
  loadBoard: async () => {
    return await fetch(`${API_URL}/board`).then(r => r.json());
  }
};
```

#### **Week 2: MCP Agent Brain**
```python
# Simple MCP endpoint
@app.post("/agent/analyze")
async def analyze_input(text: str):
    # Send to Claude MCP
    analysis = await mcp_client.analyze(f"""
    Stefan said: {text}
    
    Extract:
    1. Task type (customer/concrete/crew/etc)
    2. Priority (urgent/high/normal)
    3. Client name
    4. Action needed
    5. Deadline
    
    Return as JSON
    """)
    
    # Create task from analysis
    return create_task_from_analysis(analysis)
```

#### **Week 3: Gmail Integration**
```python
# Using Google API Python client
def watch_gmail():
    service = build('gmail', 'v1', credentials=creds)
    
    # Get new messages
    messages = service.users().messages().list(
        userId='me',
        q='is:unread'
    ).execute()
    
    for msg in messages['messages']:
        # Send to MCP for analysis
        task = await analyze_email(msg)
        if task:
            create_task_card(task)
```

### **Stefan's Daily Experience (Once Built):**

**Morning (5am):**
- Gets SMS: "3 urgent tasks today: DACG callback, Boston delay notice, US Soccer response"
- Opens board: Everything organized, nothing forgotten

**Email arrives (10am):**
- "Can you move our start date to next Tuesday?"
- Agent creates card: "🔥 Lifetime requesting Tuesday start - conflicts with Kentucky"
- Stefan gets notification, drags to "In Progress"

**Completing task (2pm):**
- Drags "Contact DACG" to Done
- Agent drafts: "DACG confirmation email ready - [APPROVE] [EDIT]"
- Stefan taps approve, email sends

### **Tooling Recommendations:**

**EASIEST Path:**
- **Frontend:** Keep your HTML, add `fetch()` calls
- **Backend:** FastAPI (super simple, great with AI)
- **Automation:** n8n (self-hosted, visual, powerful)
- **MCP:** Claude MCP Python SDK
- **Deploy:** Vercel (frontend) + Railway (backend)

**AVOID:**
- Complex frameworks (Next.js, Django) - overkill
- Multiple databases - one PostgreSQL does all
- Building email server - use Gmail API
- Custom webhook handlers - use n8n

### **Budget Hosting:**
- **GitHub Pages:** Free (frontend)
- **Railway:** $5/month (backend + database)
- **n8n:** $20/month (or self-host free)
- **Total:** ~$25/month for production system

### **First Step RIGHT NOW:**
1. Take the HTML kanban
2. Add this to save state:
```javascript
// Add to existing HTML
function saveToAPI() {
  const tasks = Array.from(document.querySelectorAll('.task-card')).map(card => ({
    id: card.id,
    title: card.querySelector('.task-title').textContent,
    category: card.dataset.category,
    column: card.parentElement.id
  }));
  
  fetch('http://localhost:8000/tasks', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(tasks)
  });
}

// Call on every drag/drop and edit
```

3. Spin up basic FastAPI:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

tasks_db = []

@app.post("/tasks")
async def save_tasks(tasks: list):
    global tasks_db
    tasks_db = tasks
    return {"status": "saved"}

@app.get("/tasks")
async def get_tasks():
    return tasks_db
```
Looking at this Kanban board, I'll break down its structure into reusable components that can be adapted for any project or life management system:

## Core Structure Breakdown

### 1. **Page Layout Architecture**
```
Header Section
├── Main Title
├── Time Period Display
└── Summary Statistics Bar

Main Board Container
├── Filter Bar (category toggles)
├── Legend (visual category guide)
└── Column Grid (4 columns by default)
    ├── Backlog
    ├── This Week / To Do
    ├── In Progress
    └── Done
```

### 2. **Key Components**

#### **Header Statistics Dashboard**
- Dynamic counters that update based on card positions
- Modular stat cards showing:
  - Total items
  - Items in specific columns
  - Filtered views
  - Time allocations

#### **Filtering System**
- **Category Filters**: Buttons that show/hide cards based on data attributes
- **Visual Legend**: Clickable color-coded categories with metadata (like time estimates)
- Uses `data-filter` and `data-project` attributes for filtering logic

#### **Column Structure**
Each column contains:
- **Header**: Title + live count badge
- **Drop Zone**: `task-area` container for drag-and-drop
- **Add Button**: Creates new cards dynamically
- **Visual Indicator**: Top border color to distinguish columns

#### **Task Card Anatomy**
```html
<div class="task-card [category-class]" draggable="true" data-project="[category]">
    <span class="priority-[level]">Icon</span>
    <div class="task-header">
        <div class="task-project">Category Label</div>
    </div>
    <span class="task-emoji">Visual Icon</span>
    Main Task Text
    <div class="task-meta">
        <span class="task-hours">Time Estimate</span>
        <span class="task-deadline">Due Date</span>
    </div>
</div>
```

### 3. **Interactive Features**

#### **Drag & Drop System**
- Uses HTML5 drag events
- Visual feedback (opacity change, rotation on drag)
- Column highlighting on hover
- Maintains card in last dropped position

#### **Dynamic Editing**
- Double-click cards to edit inline
- Add new cards via button in each column
- Prompt-based creation system

#### **Live Statistics**
- Updates automatically when cards move
- Respects current filter state
- Column-specific counting

### 4. **Styling Strategy**

#### **Color Coding System**
Create category classes with:
- Background color
- Left border accent
- Consistent color variables

```css
.category-1 { background: #ColorA; border-left: 4px solid #DarkerColorA; }
.category-2 { background: #ColorB; border-left: 4px solid #DarkerColorB; }
```

#### **Visual Hierarchy**
- Priority indicators (🔥 high, ⚡ medium)
- Status through column position
- Category through color
- Metadata in subdued styling

### 5. **Responsive Design**
- Desktop: 4 columns
- Tablet: 2 columns  
- Mobile: 1 column
- Uses CSS Grid with media queries

## How to Make It Reusable

### 1. **Genericize the Categories**
Replace specific projects with:
```javascript
const categories = [
    { id: 'personal', name: 'Personal', emoji: '👤', color: '#FFE5B4', hours: '5h' },
    { id: 'work', name: 'Work', emoji: '💼', color: '#E6E6FA', hours: '8h' },
    { id: 'health', name: 'Health', emoji: '❤️', color: '#E0F2E9', hours: '2h' }
];
```

### 2. **Configurable Columns**
Make columns customizable:
```javascript
const columns = [
    { id: 'backlog', title: 'Ideas', icon: '💡', color: '#6c757d' },
    { id: 'todo', title: 'To Do', icon: '📋', color: '#ffc107' },
    { id: 'doing', title: 'Doing', icon: '⚡', color: '#17a2b8' },
    { id: 'done', title: 'Done', icon: '✅', color: '#28a745' }
];
```

### 3. **Template Task Structure**
```javascript
const taskTemplate = {
    id: generateId(),
    category: 'work',
    title: 'Task description',
    priority: 'medium', // high, medium, low
    estimate: '2h',
    deadline: 'Fri',
    emoji: '📌'
};
```

### 4. **localStorage Persistence**
Add data persistence:
```javascript
function saveBoard() {
    const boardState = {
        tasks: getAllTasks(),
        columns: getColumnStates()
    };
    localStorage.setItem('kanbanBoard', JSON.stringify(boardState));
}

function loadBoard() {
    const saved = localStorage.getItem('kanbanBoard');
    if (saved) {
        const boardState = JSON.parse(saved);
        restoreBoard(boardState);
    }
}
```

### 5. **Make It Data-Driven**
Instead of hardcoded HTML, generate cards from data:
```javascript
function createTaskCard(task) {
    const card = document.createElement('div');
    card.className = `task-card ${task.category}`;
    card.draggable = true;
    card.dataset.project = task.category;
    card.dataset.taskId = task.id;
    
    card.innerHTML = `
        ${task.priority === 'high' ? '<span class="priority-high">🔥</span>' : ''}
        <div class="task-header">
            <div class="task-project">${getCategoryName(task.category)}</div>
        </div>
        <span class="task-emoji">${task.emoji}</span>
        ${task.title}
        <div class="task-meta">
            ${task.estimate ? `<span class="task-hours">${task.estimate}</span>` : ''}
            ${task.deadline ? `<span class="task-deadline">${task.deadline}</span>` : ''}
        </div>
    `;
    
    return card;
}
```

## Universal Use Cases

This structure works for:
- **Personal**: Goals, habits, chores, appointments
- **Team Projects**: Sprints, features, bugs, releases  
- **Content Creation**: Ideas, drafts, editing, published
- **Learning**: Topics, studying, practicing, mastered
- **Sales Pipeline**: Leads, contacted, negotiating, closed
- **Home Renovation**: Planning, shopping, in-progress, completed

The key is keeping the structure while swapping out categories, columns, and metadata fields based on your specific needs.