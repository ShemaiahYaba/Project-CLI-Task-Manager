# CLI Task Manager 📋

A feature-rich command-line task management application built with Python. Manage your tasks efficiently from the terminal with full CRUD operations, filtering, search, and persistent storage.

**Week 1 Project** - Backend Engineering Fundamentals Bootcamp

---

## ✨ Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete tasks
- 💾 **JSON Persistence** - All tasks automatically saved to disk
- 🎯 **Priority Levels** - Low, Medium, High priority classification
- 📅 **Due Date Tracking** - Set deadlines and get overdue warnings
- 🏷️ **Categories** - Organize tasks by category
- 🔍 **Search Functionality** - Find tasks by description
- 🎨 **Rich CLI Output** - Beautiful formatted output with icons and colors
- 🔧 **Professional Argument Parsing** - Using argparse for robust CLI
- 🧪 **Comprehensive Test Suite** - 43+ unit and integration tests
- 📊 **Filtering Options** - Filter by status, priority, or category

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**

   ```bash
   git clone <your-repo-url>
   cd week1-cli-task-manager
   ```

2. **Install dependencies** (for testing)

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python task_manager.py --help
   ```

---

## 📖 Usage

### Basic Commands

#### Add a Task

```bash
# Simple task
python task_manager.py add "Complete Python project"

# Task with due date
python task_manager.py add "Submit assignment" --due 2026-01-30

# Task with priority and category
python task_manager.py add "Code review" --priority high --category development

# Full example
python task_manager.py add "Deploy to production" --due 2026-02-15 --priority high --category devops
```

#### List Tasks

```bash
# View all tasks
python task_manager.py list

# View only pending tasks
python task_manager.py list --pending-only

# Filter by priority
python task_manager.py list --priority high

# Filter by category
python task_manager.py list --category development

# Combine filters
python task_manager.py list --pending-only --priority high
```

#### Complete a Task

```bash
# Mark task #1 as complete
python task_manager.py complete 1
```

#### Delete a Task

```bash
# Delete task #2
python task_manager.py delete 2
```

#### Search Tasks

```bash
# Search for tasks containing "project"
python task_manager.py search "project"

# Case-insensitive search
python task_manager.py search "API"
```

### Get Help

```bash
# General help
python task_manager.py --help

# Help for specific command
python task_manager.py add --help
python task_manager.py list --help
```

---

## 📊 Example Workflow

```bash
# Add some tasks
python task_manager.py add "Build REST API" --due 2026-01-28 --priority high --category backend
python task_manager.py add "Write unit tests" --due 2026-01-29 --priority medium --category testing
python task_manager.py add "Update documentation" --priority low --category docs

# View all tasks
python task_manager.py list

# Complete the API task
python task_manager.py complete 1

# Search for testing tasks
python task_manager.py search "test"

# View only pending high-priority tasks
python task_manager.py list --pending-only --priority high
```

---

## 🎨 Output Examples

### Task List View

```markdown
============================================================
📌 PENDING TASKS
============================================================

○ Task #1
Build REST API
📅 2026-01-28 (Due in 8 days)
◆◆ Priority: HIGH
🏷 Category: backend

○ Task #2
Write unit tests
📅 2026-01-29 (Due in 9 days)
◆ Priority: MEDIUM
🏷 Category: testing

============================================================
✓ COMPLETED TASKS
============================================================

✓ Task #3
Update documentation
◇ Priority: LOW
🏷 Category: docs

---

## Total: 3 tasks (2 pending, 1 completed)
```

### Overdue Warning

```markdown
○ Task #5
Submit quarterly report
📅 2026-01-15 ⚠ OVERDUE by 5 days
◆◆ Priority: HIGH
```

---

## 🏗️ Project Structure

```markdown
week1-cli-task-manager/
│
├── task_manager.py # Main application code
├── test_task_manager.py # Comprehensive test suite
├── tasks.json # Task storage (auto-generated)
├── requirements.txt # Python dependencies
└── README.md # This file
```

---

## 🧪 Testing

The project includes a comprehensive test suite with 43+ tests covering:

- Task initialization and file handling
- CRUD operations
- Input validation
- Edge cases
- Integration scenarios

### Run Tests

```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run all tests
pytest test_task_manager.py -v

# Run with coverage report
pytest test_task_manager.py --cov=task_manager --cov-report=html

# Run specific test class
pytest test_task_manager.py::TestAddTask -v

# Run specific test
pytest test_task_manager.py::TestAddTask::test_add_basic_task -v
```

### Test Coverage

- ✅ Initialization & file handling (3 tests)
- ✅ Add task operations (9 tests)
- ✅ Complete task operations (4 tests)
- ✅ Delete task operations (3 tests)
- ✅ View & filter tasks (6 tests)
- ✅ Search functionality (4 tests)
- ✅ Edge cases & error handling (4 tests)
- ✅ Integration workflows (2 tests)

---

## 🔧 Technical Implementation

### Key Features

- **Type Hints**: Full type annotations for better code quality
- **Enums**: Type-safe priority levels using Python's Enum
- **Pathlib**: Modern file path handling
- **Datetime**: Proper date parsing and overdue calculations
- **Argparse**: Professional CLI argument parsing
- **Error Handling**: Comprehensive exception handling with user-friendly messages
- **Single Responsibility**: Each method does one thing well
- **Docstrings**: Google-style documentation for all functions

### Dependencies

```python
# Standard Library Only (No external dependencies for main app)
import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from enum import Enum

# Testing Dependencies
pytest>=7.4.0
pytest-cov>=4.1.0
```

---

## 🎯 Learning Objectives Achieved

### Week 1 Bootcamp Requirements

✅ **Python Fundamentals**

- Variables, data types, and type hints
- Lists, dictionaries, and data structures
- Control flow (if/elif/else, loops)
- Functions with parameters and return values

✅ **File Handling**

- Reading and writing JSON files
- Error handling for file operations
- Path management with pathlib

✅ **Exception Handling**

- Try-except blocks
- Custom error messages
- Graceful error recovery

✅ **Best Practices**

- Single Responsibility Principle
- Input validation
- Type hints throughout
- Comprehensive docstrings
- Professional code organization

✅ **Testing**

- Unit tests with pytest
- Fixtures and test organization
- Edge case coverage
- Integration testing

---

## 📝 Command Reference

| Command    | Description       | Example                                  |
| ---------- | ----------------- | ---------------------------------------- |
| `add`      | Add a new task    | `task_manager.py add "Task description"` |
| `list`     | View all tasks    | `task_manager.py list`                   |
| `complete` | Mark task as done | `task_manager.py complete 1`             |
| `delete`   | Remove a task     | `task_manager.py delete 2`               |
| `search`   | Find tasks        | `task_manager.py search "keyword"`       |

### Optional Flags

| Flag             | Options           | Description                |
| ---------------- | ----------------- | -------------------------- |
| `--due`          | YYYY-MM-DD        | Set due date               |
| `--priority`     | low, medium, high | Set priority level         |
| `--category`     | any string        | Assign category            |
| `--pending-only` | -                 | Show only incomplete tasks |

---

## 🐛 Troubleshooting

### Common Issues

#### **Q: "Permission denied" error when saving tasks**

- Check that you have write permissions in the current directory
- Try running from a directory where you have write access

#### **Q: Tasks not persisting between sessions**

- Ensure `tasks.json` is being created in the same directory
- Check for any error messages when the program exits

#### **Q: Invalid date format error**

- Dates must be in `YYYY-MM-DD` format
- Example: `2026-01-30` (not `01/30/2026` or `30-01-2026`)

#### **Q: Task ID not found**

- Run `list` command to see all available task IDs
- IDs are assigned sequentially starting from 1

---

## 🚀 Future Enhancements

Potential features for future iterations:

- [ ] Task tags (multiple tags per task)
- [ ] Recurring tasks
- [ ] Task notes and attachments
- [ ] Subtasks and task dependencies
- [ ] Time tracking
- [ ] Export to CSV/PDF
- [ ] Task reminders
- [ ] Color-coded priorities in terminal
- [ ] Undo/redo functionality
- [ ] Task templates

---

## 📚 Resources Used

- [Python Official Documentation](https://docs.python.org/3/)
- [Argparse Tutorial](https://docs.python.org/3/howto/argparse.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Real Python - Python Basics](https://realpython.com/)

---

## 👨‍💻 Author

### **Your Name**

- Bootcamp: Backend Engineering Fundamentals
- Week: 1 - Python Fundamentals & Backend Basics
- Project: CLI Task Manager

---

## 📄 License

This project is part of a learning bootcamp and is free to use for educational purposes.

---

## 🙏 Acknowledgments

- Built as part of the Backend Engineering Fundamentals - 6 Week Intensive Course
- Week 1 Project: CLI Task Manager
- Thanks to the bootcamp instructors and community

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the example workflows
3. Run tests to verify installation: `pytest test_task_manager.py -v`
4. Check command help: `python task_manager.py --help`

---

## **Happy Task Managing! 🎉**
