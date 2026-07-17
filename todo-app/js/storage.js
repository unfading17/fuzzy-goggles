/**
 * Storage Module
 * Handles local storage operations for tasks
 */

class StorageManager {
    constructor() {
        this.storageKey = 'todoList_tasks';
        this.categoriesKey = 'todoList_categories';
        this.settingsKey = 'todoList_settings';
    }

    /**
     * Get all tasks from local storage
     */
    getAllTasks() {
        try {
            const tasks = localStorage.getItem(this.storageKey);
            return tasks ? JSON.parse(tasks) : [];
        } catch (error) {
            console.error('Error reading tasks:', error);
            return [];
        }
    }

    /**
     * Save all tasks to local storage
     */
    saveTasks(tasks) {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(tasks));
            return true;
        } catch (error) {
            console.error('Error saving tasks:', error);
            return false;
        }
    }

    /**
     * Add a new task
     */
    addTask(task) {
        const tasks = this.getAllTasks();
        task.id = Date.now();
        task.createdAt = new Date().toISOString();
        task.completed = false;
        tasks.push(task);
        this.saveTasks(tasks);
        return task;
    }

    /**
     * Update an existing task
     */
    updateTask(taskId, updatedTask) {
        const tasks = this.getAllTasks();
        const index = tasks.findIndex(t => t.id === taskId);
        if (index !== -1) {
            tasks[index] = { ...tasks[index], ...updatedTask, updatedAt: new Date().toISOString() };
            this.saveTasks(tasks);
            return tasks[index];
        }
        return null;
    }

    /**
     * Delete a task
     */
    deleteTask(taskId) {
        const tasks = this.getAllTasks();
        const filtered = tasks.filter(t => t.id !== taskId);
        this.saveTasks(filtered);
        return filtered;
    }

    /**
     * Get a single task by ID
     */
    getTaskById(taskId) {
        const tasks = this.getAllTasks();
        return tasks.find(t => t.id === taskId);
    }

    /**
     * Clear all tasks
     */
    clearAllTasks() {
        localStorage.setItem(this.storageKey, JSON.stringify([]));
    }

    /**
     * Get all categories
     */
    getCategories() {
        try {
            const categories = localStorage.getItem(this.categoriesKey);
            return categories ? JSON.parse(categories) : ['General', 'Work', 'Personal', 'Shopping', 'Health'];
        } catch (error) {
            console.error('Error reading categories:', error);
            return ['General', 'Work', 'Personal', 'Shopping', 'Health'];
        }
    }

    /**
     * Save categories
     */
    saveCategories(categories) {
        try {
            localStorage.setItem(this.categoriesKey, JSON.stringify(categories));
            return true;
        } catch (error) {
            console.error('Error saving categories:', error);
            return false;
        }
    }

    /**
     * Add a new category
     */
    addCategory(category) {
        const categories = this.getCategories();
        if (!categories.includes(category)) {
            categories.push(category);
            this.saveCategories(categories);
        }
        return categories;
    }

    /**
     * Get settings
     */
    getSettings() {
        try {
            const settings = localStorage.getItem(this.settingsKey);
            return settings ? JSON.parse(settings) : { darkMode: false };
        } catch (error) {
            console.error('Error reading settings:', error);
            return { darkMode: false };
        }
    }

    /**
     * Save settings
     */
    saveSettings(settings) {
        try {
            localStorage.setItem(this.settingsKey, JSON.stringify(settings));
            return true;
        } catch (error) {
            console.error('Error saving settings:', error);
            return false;
        }
    }

    /**
     * Export tasks to JSON
     */
    exportTasks() {
        const tasks = this.getAllTasks();
        const categories = this.getCategories();
        const exportData = {
            version: '1.0',
            exportDate: new Date().toISOString(),
            tasks,
            categories
        };
        return JSON.stringify(exportData, null, 2);
    }

    /**
     * Import tasks from JSON
     */
    importTasks(jsonData) {
        try {
            const data = JSON.parse(jsonData);
            if (data.tasks && Array.isArray(data.tasks)) {
                this.saveTasks(data.tasks);
                if (data.categories && Array.isArray(data.categories)) {
                    this.saveCategories(data.categories);
                }
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error importing tasks:', error);
            return false;
        }
    }
}

// Create global instance
const storage = new StorageManager();
