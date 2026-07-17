/**
 * Main Application
 */

class TodoApp {
    constructor() {
        this.tasks = storage.getAllTasks();
        this.filteredTasks = this.tasks;
        this.currentFilter = 'all';
        this.currentCategoryFilter = 'all';
        this.init();
    }

    /**
     * Initialize application
     */
    init() {
        this.setupEventListeners();
        ui.loadTheme();
        this.updateUI();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Add task
        ui.addTaskBtn.addEventListener('click', () => this.addTask());
        ui.taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTask();
        });

        // Search
        ui.searchInput.addEventListener('input', Utils.debounce(() => this.filterTasks(), 300));

        // Theme toggle
        ui.themeToggle.addEventListener('click', () => ui.toggleTheme());

        // Export/Import
        ui.exportBtn.addEventListener('click', () => this.exportTasks());
        ui.importBtn.addEventListener('click', () => ui.fileInput.click());
        ui.fileInput.addEventListener('change', (e) => this.importTasks(e));

        // Clear all
        ui.clearAllBtn.addEventListener('click', () => this.clearAllTasks());
    }

    /**
     * Add new task
     */
    addTask() {
        const text = ui.taskInput.value.trim();
        if (!text) {
            Utils.showToast('Please enter a task', 'error');
            return;
        }

        const task = {
            text,
            category: ui.categorySelect.value,
            priority: ui.prioritySelect.value,
            dueDate: ui.dueDateInput.value
        };

        storage.addTask(task);
        this.tasks = storage.getAllTasks();
        
        // Add category if new
        if (!storage.getCategories().includes(task.category)) {
            storage.addCategory(task.category);
            ui.updateCategories(storage.getCategories());
        }

        ui.clearInputs();
        this.updateUI();
        Utils.showToast('Task added successfully! ✅', 'success');
    }

    /**
     * Toggle task completion
     */
    toggleTask(taskId) {
        const task = storage.getTaskById(taskId);
        if (task) {
            storage.updateTask(taskId, { completed: !task.completed });
            this.tasks = storage.getAllTasks();
            this.updateUI();
        }
    }

    /**
     * Edit task
     */
    editTask(taskId) {
        const task = storage.getTaskById(taskId);
        if (!task) return;

        const newText = prompt('Edit task:', task.text);
        if (newText && newText.trim()) {
            storage.updateTask(taskId, { text: newText.trim() });
            this.tasks = storage.getAllTasks();
            this.updateUI();
            Utils.showToast('Task updated! ✏️', 'success');
        }
    }

    /**
     * Delete task
     */
    deleteTask(taskId) {
        if (ui.showConfirmDialog('Are you sure you want to delete this task?')) {
            storage.deleteTask(taskId);
            this.tasks = storage.getAllTasks();
            this.updateUI();
            Utils.showToast('Task deleted! 🗑️', 'success');
        }
    }

    /**
     * Filter by status (all, active, completed)
     */
    filterByStatus(status) {
        this.currentFilter = status;
        this.filterTasks();
        
        // Update filter button styles
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.filter === status) btn.classList.add('active');
        });
    }

    /**
     * Filter by category
     */
    filterByCategory(category) {
        this.currentCategoryFilter = category;
        this.filterTasks();
        
        // Update category button styles
        document.querySelectorAll('.category-tag').forEach(tag => {
            tag.classList.remove('active');
            if (tag.dataset.category === category) tag.classList.add('active');
        });
    }

    /**
     * Filter tasks based on current filters
     */
    filterTasks() {
        let filtered = [...this.tasks];
        const searchQuery = ui.searchInput.value.toLowerCase();

        // Status filter
        if (this.currentFilter === 'active') {
            filtered = filtered.filter(t => !t.completed);
        } else if (this.currentFilter === 'completed') {
            filtered = filtered.filter(t => t.completed);
        }

        // Category filter
        if (this.currentCategoryFilter !== 'all') {
            filtered = filtered.filter(t => t.category === this.currentCategoryFilter);
        }

        // Search filter
        if (searchQuery) {
            filtered = filtered.filter(t => 
                t.text.toLowerCase().includes(searchQuery) ||
                t.category.toLowerCase().includes(searchQuery)
            );
        }

        this.filteredTasks = filtered;
        ui.renderTasks(this.filteredTasks);
    }

    /**
     * Save task order after drag and drop
     */
    saveTaskOrder() {
        const taskIds = Array.from(document.querySelectorAll('.task-item'))
            .map(el => parseInt(el.dataset.id));
        
        const reordered = taskIds.map(id => 
            this.tasks.find(t => t.id === id)
        ).filter(t => t);
        
        storage.saveTasks(reordered);
        this.tasks = reordered;
    }

    /**
     * Clear all tasks
     */
    clearAllTasks() {
        if (ui.showConfirmDialog('Are you sure you want to delete ALL tasks? This cannot be undone!')) {
            storage.clearAllTasks();
            this.tasks = [];
            this.updateUI();
            Utils.showToast('All tasks deleted! 🗑️', 'success');
        }
    }

    /**
     * Export tasks to JSON file
     */
    exportTasks() {
        const jsonData = storage.exportTasks();
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `todo-export-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        URL.revokeObjectURL(url);
        Utils.showToast('Tasks exported successfully! ⬇️', 'success');
    }

    /**
     * Import tasks from JSON file
     */
    importTasks(e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            if (storage.importTasks(event.target.result)) {
                this.tasks = storage.getAllTasks();
                ui.updateCategories(storage.getCategories());
                this.updateUI();
                Utils.showToast('Tasks imported successfully! ⬆️', 'success');
            } else {
                Utils.showToast('Error importing tasks. Invalid file format.', 'error');
            }
        };
        reader.readAsText(file);
        ui.fileInput.value = ''; // Reset file input
    }

    /**
     * Update entire UI
     */
    updateUI() {
        ui.updateStats(this.tasks);
        ui.updateCategories(storage.getCategories());
        this.filterTasks();
    }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.app = new TodoApp();
    });
} else {
    window.app = new TodoApp();
}
