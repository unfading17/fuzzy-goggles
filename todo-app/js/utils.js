/**
 * Utility Functions
 */

class Utils {
    /**
     * Format date to readable string
     */
    static formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    }

    /**
     * Check if date is overdue
     */
    static isOverdue(dateString) {
        if (!dateString) return false;
        const dueDate = new Date(dateString);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        return dueDate < today;
    }

    /**
     * Check if date is today
     */
    static isToday(dateString) {
        if (!dateString) return false;
        const dueDate = new Date(dateString);
        const today = new Date();
        return dueDate.toDateString() === today.toDateString();
    }

    /**
     * Check if date is tomorrow
     */
    static isTomorrow(dateString) {
        if (!dateString) return false;
        const dueDate = new Date(dateString);
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        return dueDate.toDateString() === tomorrow.toDateString();
    }

    /**
     * Get date label
     */
    static getDateLabel(dateString) {
        if (!dateString) return '';
        if (this.isToday(dateString)) return 'Today';
        if (this.isTomorrow(dateString)) return 'Tomorrow';
        if (this.isOverdue(dateString)) return `Overdue: ${this.formatDate(dateString)}`;
        return this.formatDate(dateString);
    }

    /**
     * Generate unique ID
     */
    static generateId() {
        return Date.now() + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Debounce function
     */
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Throttle function
     */
    static throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Deep clone object
     */
    static deepClone(obj) {
        return JSON.parse(JSON.stringify(obj));
    }

    /**
     * Escape HTML string
     */
    static escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Show toast notification
     */
    static showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 12px 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), duration);
    }
}
