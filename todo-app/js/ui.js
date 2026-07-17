/**
 * UI Manager
 * Handles all UI rendering and DOM manipulation
 */

class UIManager {
    constructor() {
        this.tasksList = document.getElementById('tasksList');
        this.taskInput = document.getElementById('taskInput');
        this.categorySelect = document.getElementById('categorySelect');
        this.prioritySelect = document.getElementById('prioritySelect');
        this.dueDateInput = document.getElementById('dueDateInput');
        this.searchInput = document.getElementById('searchInput');
        this.categoriesList = document.getElementById('categoriesList');
        this.themeToggle = document.getElementById('themeToggle');
        this.addTaskBtn = document.getElementById('addTaskBtn');
        this.exportBtn = document.getElementById('exportBtn');
        this.importBtn = document.getElementById('importBtn');
        this.clearAllBtn = document.getElementById('clearAllBtn');
        this.fileInput = document.getElementById('fileInput');
    }

    /**
     * Render tasks list
     */
    renderTasks(tasks) {
        if (tasks.length === 0) {
            this.tasksList.innerHTML = '<div class="empty-state"><p>📭 No tasks yet. Add one to get started!</p></div>';
            return;
        }

        this.tasksList.innerHTML = tasks.map(task => this.createTaskElement(task)).join('');
        this.attachTaskEventListeners();
    }

    /**
     * Create task element HTML
     */
    createTaskElement(task) {
        const priorityClass = `${task.priority ? task.priority.toLowerCase() : 'medium'}-priority`;
        const overduClass = task.dueDate && Utils.isOverdue(task.dueDate) ? 'overdue' : '';
        const completedClass = task.completed ? 'completed' : '';

        return `
            <div class="task-item ${priorityClass} ${completedClass}" data-id="${task.id}" draggable="true">
                <input 
                    type="checkbox" 
                    class="task-checkbox" 
                    ${task.completed ? 'checked' : ''}
                    onchange="app.toggleTask(${task.id})"
                >
                <div class="task-content">
                    <div class="task-text">${Utils.escapeHtml(task.text)}</div>
                    <div class="task-meta">
                        <span class="task-category">${task.category || 'General'}</span>
                        <span class="task-priority priority-${task.priority ? task.priority.toLowerCase() : 'medium'}">
                            ${task.priority || 'Medium'}
                        </span>
                        ${task.dueDate ? `<span class="task-due-date ${overduClass}">📅 ${Utils.getDateLabel(task.dueDate)}</span>` : ''}
                    </div>
                </div>
                <div class="task-actions">
                    <button class="btn-task-action btn-task-edit" onclick="app.editTask(${task.id})" title="Edit">
                        ✏️
                    </button>
                    <button class="btn-task-action btn-task-delete" onclick="app.deleteTask(${task.id})" title="Delete">
                        🗑️
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Attach event listeners to tasks
     */
    attachTaskEventListeners() {
        const tasks = this.tasksList.querySelectorAll('.task-item');
        tasks.forEach(task => {
            task.addEventListener('dragstart', (e) => this.handleDragStart(e));
            task.addEventListener('dragend', (e) => this.handleDragEnd(e));
            task.addEventListener('dragover', (e) => this.handleDragOver(e));
            task.addEventListener('drop', (e) => this.handleDrop(e));
        });
    }

    /**
     * Update statistics
     */
    updateStats(tasks) {
        const total = tasks.length;
        const completed = tasks.filter(t => t.completed).length;
        const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

        document.getElementById('totalTasks').textContent = total;
        document.getElementById('completedTasks').textContent = completed;
        document.getElementById('completionPercentage').textContent = percentage + '%';
    }

    /**
     * Update categories list
     */
    updateCategories(categories) {
        let html = '<button class="category-tag active" data-category="all" onclick="app.filterByCategory(\'all\')">All Tasks</button>';
        categories.forEach(category => {
            html += `<button class="category-tag" data-category="${category}" onclick="app.filterByCategory('${category}')">${category}</button>`;
        });
        this.categoriesList.innerHTML = html;
    }

    /**
     * Clear input fields
     */
    clearInputs() {
        this.taskInput.value = '';
        this.prioritySelect.value = 'Medium';
        this.dueDateInput.value = '';
        this.taskInput.focus();
    }

    /**
     * Toggle theme
     */
    toggleTheme() {
        document.body.classList.toggle('dark-mode');
        const isDarkMode = document.body.classList.contains('dark-mode');
        this.themeToggle.textContent = isDarkMode ? '☀️' : '🌙';
        storage.saveSettings({ darkMode: isDarkMode });
    }

    /**
     * Load theme from settings
     */
    loadTheme() {
        const settings = storage.getSettings();
        if (settings.darkMode) {
            document.body.classList.add('dark-mode');
            this.themeToggle.textContent = '☀️';
        }
    }

    /**
     * Drag and drop handlers
     */
    handleDragStart(e) {
        e.dataTransfer.effectAllowed = 'move';
        e.target.style.opacity = '0.5';
    }

    handleDragEnd(e) {
        e.target.style.opacity = '1';
    }

    handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        e.target.closest('.task-item')?.style.borderTop = '2px solid #2563eb';
    }

    handleDrop(e) {
        e.preventDefault();
        const draggedElement = document.querySelector('.task-item[style*="opacity"]');
        const targetElement = e.target.closest('.task-item');
        
        if (draggedElement && targetElement && draggedElement !== targetElement) {
            targetElement.parentNode.insertBefore(draggedElement, targetElement);
            app.saveTaskOrder();
        }
    }

    /**
     * Show confirmation dialog
     */
    showConfirmDialog(message) {
        return confirm(message);
    }
}

// Create global instance
const ui = new UIManager();
