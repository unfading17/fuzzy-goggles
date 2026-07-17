# To-Do List Application

A modern, feature-rich to-do list application with local storage functionality.

## Features

✅ **Task Management**
- Create, edit, and delete tasks
- Mark tasks as complete/incomplete
- Organize tasks by categories
- Set priorities (Low, Medium, High)
- Add due dates to tasks

💾 **Local Storage**
- All data saved to browser's local storage
- Persist tasks across sessions
- No backend required
- Works offline

🎨 **User Interface**
- Clean, modern design
- Dark/Light mode toggle
- Responsive design (mobile, tablet, desktop)
- Drag-and-drop reordering
- Real-time search and filtering

📊 **Statistics**
- Task completion percentage
- Total tasks overview
- Progress tracking

⚙️ **Advanced Features**
- Multiple categories
- Priority levels
- Due date reminders
- Export/Import tasks
- Task filtering and sorting

## Installation

1. Clone the repository
```bash
git clone https://github.com/unfading17/fuzzy-goggles.git
cd fuzzy-goggles/todo-app
```

2. Open `index.html` in your browser

That's it! No installation required.

## Usage

### Add a Task
1. Type your task in the input field
2. (Optional) Select a category
3. (Optional) Set priority and due date
4. Click "Add Task" or press Enter

### Manage Tasks
- **Complete**: Click the checkbox to mark as done
- **Edit**: Click on task text to edit
- **Delete**: Click the trash icon
- **Reorder**: Drag tasks to reorder

### Filter & Search
- Use the search bar to find tasks
- Filter by category or priority
- View only completed or incomplete tasks

### Export/Import
- Export tasks to JSON file
- Import previously exported tasks

## File Structure

```
todo-app/
├── index.html          # Main HTML file
├── css/
│   ├── styles.css      # Main styles
│   └── responsive.css  # Mobile responsive styles
├── js/
│   ├── app.js          # Main application logic
│   ├── storage.js      # Local storage handler
│   ├── ui.js           # UI management
│   └── utils.js        # Utility functions
└── README.md           # This file
```

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## Technology Stack

- HTML5
- CSS3 (with CSS Grid & Flexbox)
- Vanilla JavaScript (ES6+)
- Local Storage API

## License

MIT License - Free to use and modify
