// Stefan's Task Manager - Main Application
const API_BASE = 'http://localhost:8000/api/v1';

// Global state
let boardData = {
    columns: [],
    categories: [],
    tasks: []
};
let currentFilter = 'all';
let selectedColumnId = null;
let draggedTask = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing Stefan\'s Task Manager...');
    loadBoard();
    setupEventListeners();
});

// Load board data from API
async function loadBoard() {
    try {
        const response = await fetch(`${API_BASE}/board/`);
        if (!response.ok) throw new Error('Failed to load board');
        
        boardData = await response.json();
        renderBoard();
        updateStatistics();
    } catch (error) {
        console.error('Error loading board:', error);
        showError('Failed to load board. Please check if the backend is running.');
    }
}

// Render the entire board
function renderBoard() {
    const boardElement = document.getElementById('kanban-board');
    boardElement.innerHTML = '';
    
    if (!boardData.columns || boardData.columns.length === 0) {
        boardElement.innerHTML = '<div class="loading">No columns found. Please check database.</div>';
        return;
    }
    
    boardData.columns.forEach(column => {
        const columnElement = createColumnElement(column);
        boardElement.appendChild(columnElement);
    });
}

// Create column element
function createColumnElement(column) {
    const columnDiv = document.createElement('div');
    columnDiv.className = 'kanban-column';
    columnDiv.dataset.columnId = column.id;
    
    columnDiv.innerHTML = `
        <div class="column-header" style="border-bottom-color: ${column.color_code}">
            <h2>${column.name}</h2>
            <span class="task-count">${column.task_count || 0}</span>
        </div>
        <div class="task-area" id="column-${column.id}" data-column-id="${column.id}">
            ${column.tasks.map(task => createTaskHTML(task)).join('')}
        </div>
        <button class="add-task-btn" data-column-id="${column.id}">+ Add Task</button>
    `;
    
    // Setup drag and drop for task area
    const taskArea = columnDiv.querySelector('.task-area');
    setupDropZone(taskArea);
    
    // Setup add task button
    const addBtn = columnDiv.querySelector('.add-task-btn');
    addBtn.addEventListener('click', () => openAddTaskModal(column.id));
    
    return columnDiv;
}

// Create task HTML
function createTaskHTML(task) {
    const categoryClass = getCategorySlug(task.category_name);
    const priorityIcon = task.priority === 'urgent' ? '<span class="priority-urgent">🔥</span>' : 
                         task.priority === 'high' ? '<span class="priority-high">⚡</span>' : '';
    
    return `
        <div class="task-card ${categoryClass}" 
             draggable="true" 
             data-task-id="${task.id}"
             data-category="${categoryClass}">
            ${priorityIcon}
            <div class="task-header">
                <div class="task-category">${task.category_name || 'Uncategorized'}</div>
            </div>
            <div class="task-title">${task.title}</div>
            <div class="task-meta">
                ${task.client_name ? `<span>Client: ${task.client_name}</span>` : ''}
                ${task.due_date ? `<span>Due: ${formatDate(task.due_date)}</span>` : ''}
            </div>
        </div>
    `;
}

// Setup drag and drop for a task area
function setupDropZone(taskArea) {
    taskArea.addEventListener('dragover', handleDragOver);
    taskArea.addEventListener('drop', handleDrop);
    taskArea.addEventListener('dragleave', handleDragLeave);
    
    // Setup drag events for existing tasks
    const tasks = taskArea.querySelectorAll('.task-card');
    tasks.forEach(task => {
        task.addEventListener('dragstart', handleDragStart);
        task.addEventListener('dragend', handleDragEnd);
    });
}

// Drag and drop handlers
function handleDragStart(e) {
    draggedTask = e.target;
    e.target.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', e.target.innerHTML);
}

function handleDragEnd(e) {
    e.target.classList.remove('dragging');
    draggedTask = null;
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    e.currentTarget.classList.add('drag-over');
    return false;
}

function handleDragLeave(e) {
    e.currentTarget.classList.remove('drag-over');
}

async function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    e.preventDefault();
    
    const dropZone = e.currentTarget;
    dropZone.classList.remove('drag-over');
    
    if (draggedTask && dropZone !== draggedTask.parentElement) {
        const taskId = draggedTask.dataset.taskId;
        const newColumnId = dropZone.dataset.columnId;
        
        // Move task visually
        dropZone.appendChild(draggedTask);
        
        // Update backend
        try {
            const response = await fetch(`${API_BASE}/tasks/${taskId}/move`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ column_id: newColumnId })
            });
            
            if (!response.ok) throw new Error('Failed to move task');
            
            // Reload board to sync
            loadBoard();
        } catch (error) {
            console.error('Error moving task:', error);
            showError('Failed to move task. Please try again.');
            loadBoard(); // Reload to restore correct state
        }
    }
    
    return false;
}

// Open add task modal
function openAddTaskModal(columnId) {
    selectedColumnId = columnId;
    const modal = document.getElementById('task-modal');
    modal.classList.add('show');
    
    // Reset form
    document.getElementById('task-form').reset();
    
    // Populate categories dropdown
    const categorySelect = document.getElementById('task-category');
    categorySelect.innerHTML = boardData.categories.map(cat => 
        `<option value="${cat.id}">${cat.name}</option>`
    ).join('');
}

// Close modal
function closeModal() {
    const modal = document.getElementById('task-modal');
    modal.classList.remove('show');
    selectedColumnId = null;
}

// Setup event listeners
function setupEventListeners() {
    // Modal close button
    const closeBtn = document.querySelector('.close-modal');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
    
    // Cancel button
    const cancelBtn = document.querySelector('.btn-cancel');
    if (cancelBtn) {
        cancelBtn.addEventListener('click', closeModal);
    }
    
    // Task form submit
    const taskForm = document.getElementById('task-form');
    if (taskForm) {
        taskForm.addEventListener('submit', handleTaskSubmit);
    }
    
    // Filter buttons
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Apply filter
            currentFilter = btn.dataset.filter;
            applyFilter();
        });
    });
    
    // Click outside modal to close
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('task-modal');
        if (e.target === modal) {
            closeModal();
        }
    });
}

// Handle task form submission
async function handleTaskSubmit(e) {
    e.preventDefault();
    
    const formData = {
        title: document.getElementById('task-title').value,
        category_id: document.getElementById('task-category').value,
        column_id: selectedColumnId,
        priority: document.getElementById('task-priority').value,
        client_name: document.getElementById('task-client').value || null,
        due_date: document.getElementById('task-due').value || null
    };
    
    try {
        const response = await fetch(`${API_BASE}/tasks/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) throw new Error('Failed to create task');
        
        closeModal();
        loadBoard(); // Reload to show new task
        showSuccess('Task created successfully!');
    } catch (error) {
        console.error('Error creating task:', error);
        showError('Failed to create task. Please try again.');
    }
}

// Apply category filter
function applyFilter() {
    const allTasks = document.querySelectorAll('.task-card');
    
    allTasks.forEach(task => {
        if (currentFilter === 'all') {
            task.style.display = 'block';
        } else {
            const taskCategory = task.dataset.category;
            task.style.display = taskCategory === currentFilter ? 'block' : 'none';
        }
    });
    
    updateStatistics();
}

// Update statistics
function updateStatistics() {
    if (!boardData.statistics) return;
    
    document.getElementById('total-tasks').textContent = boardData.statistics.total_tasks || 0;
    document.getElementById('urgent-tasks').textContent = boardData.statistics.urgent_tasks || 0;
    
    // Count tasks in specific columns
    const thisWeekColumn = boardData.columns.find(c => c.slug === 'this-week');
    const inProgressColumn = boardData.columns.find(c => c.slug === 'in-progress');
    
    document.getElementById('this-week-tasks').textContent = thisWeekColumn ? thisWeekColumn.task_count : 0;
    document.getElementById('in-progress-tasks').textContent = inProgressColumn ? inProgressColumn.task_count : 0;
}

// Utility functions
function getCategorySlug(categoryName) {
    if (!categoryName) return '';
    return categoryName.toLowerCase().replace(/\s+/g, '-');
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'error-message';
    successDiv.style.background = '#28a745';
    successDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// Auto-refresh every 30 seconds
setInterval(() => {
    loadBoard();
}, 30000);