# Quick Start Guide - Stefan's Task Manager

## 🚀 Start Everything (2 commands)

### Step 1: Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### Step 2: Start Frontend
```bash
cd frontend
python -m http.server 3000
```

### Step 3: Open Browser
Go to: **http://localhost:3000**

That's it! Your Kanban board is running!

---

## 📋 What You Can Do Now

### Create a Task
1. Click **"+ Add Task"** in any column
2. Fill in the form:
   - Title: "Call DACG about concrete"
   - Category: Concrete
   - Priority: Urgent
3. Click Save

### Move Tasks
- **Drag** any task card
- **Drop** it in another column
- Automatically saves!

### Filter by Category
- Click **Concrete** to see only concrete tasks
- Click **Customer** for customer tasks
- Click **All Tasks** to see everything

### View Statistics
Top bar shows:
- Total tasks
- Urgent items
- This Week count
- In Progress count

---

## 🔧 Troubleshooting

### "Failed to load board"
- Make sure backend is running (Step 1)
- Check: http://localhost:8000/docs

### Can't see columns
- Refresh the page
- Check browser console (F12)

### Tasks not saving
- Check backend is running
- Try refreshing the page

---

## 📱 Mobile Access

To access from your phone on the same network:
1. Find your computer's IP address
2. On phone, go to: `http://[YOUR-IP]:3000`

---

## 🛑 Stop Everything

### Stop Frontend
Press `Ctrl+C` in frontend terminal

### Stop Backend
Press `Ctrl+C` in backend terminal

---

## 📊 Database Access

Your data is stored in Render PostgreSQL.

To view raw data:
```bash
cd database
python test_database.py
```

---

## 🔑 Important Files

- **Backend API**: `backend/app/main.py`
- **Frontend**: `frontend/index.html`
- **Styles**: `frontend/styles.css`
- **JavaScript**: `frontend/app.js`
- **Config**: `.env` (DO NOT SHARE)

---

## 📝 Daily Workflow

### Morning
1. Start backend & frontend
2. Check urgent tasks
3. Move completed tasks to Done

### During Day
- Add tasks as they come in
- Drag tasks between columns
- Update priorities

### End of Day
- Review tomorrow's tasks
- Move tasks to "This Week"
- Clear completed items

---

## 🚀 Next Features Coming

1. **Gmail Integration** - Emails become tasks
2. **Monday.com Sync** - Two-way sync
3. **SMS Alerts** - Urgent notifications
4. **AI Categorization** - Auto-organize

---

**Need Help?**
- API Docs: http://localhost:8000/docs
- Check README.md for full details