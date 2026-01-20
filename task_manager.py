"""
CLI Task Manager - Week 1 Project
A command-line task management application with full CRUD operations,
JSON persistence, and best practices implementation.
"""

import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from enum import Enum


class Priority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskManager:
    """
    Manages tasks with CRUD operations and JSON persistence.
    
    Attributes:
        filepath (Path): Path to the JSON file storing tasks
        tasks (List[Dict]): List of task dictionaries
    """
    
    def __init__(self, filepath: str = "tasks.json"):
        """
        Initialize the TaskManager.
        
        Args:
            filepath: Path to the JSON file for task storage
        """
        self.filepath = Path(filepath)
        self.tasks: List[Dict] = []
        self.load_tasks()
    
    def load_tasks(self) -> None:
        """Load tasks from JSON file. Creates file if it doesn't exist."""
        try:
            if self.filepath.exists():
                with open(self.filepath, 'r') as f:
                    self.tasks = json.load(f)
                print(f"✓ Loaded {len(self.tasks)} tasks from {self.filepath}")
            else:
                self.tasks = []
                self.save_tasks()
                print(f"✓ Created new task file: {self.filepath}")
        except json.JSONDecodeError:
            print(f"⚠ Error reading {self.filepath}. Starting with empty task list.")
            self.tasks = []
        except Exception as e:
            print(f"⚠ Unexpected error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self) -> None:
        """Save tasks to JSON file."""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f"✗ Error saving tasks: {e}")
    
    def add_task(
        self, 
        description: str, 
        due_date: Optional[str] = None,
        priority: str = "medium",
        category: Optional[str] = None
    ) -> Dict:
        """
        Add a new task.
        
        Args:
            description: Task description
            due_date: Due date in YYYY-MM-DD format
            priority: Task priority (low, medium, high)
            category: Optional task category
            
        Returns:
            The created task dictionary
            
        Raises:
            ValueError: If due_date format is invalid
        """
        if not description.strip():
            raise ValueError("Task description cannot be empty")
        
        # Validate due date if provided
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format")
        
        # Validate priority
        try:
            Priority(priority.lower())
        except ValueError:
            raise ValueError(f"Priority must be one of: {', '.join([p.value for p in Priority])}")
        
        task_id = max([t.get('id', 0) for t in self.tasks], default=0) + 1
        
        task = {
            'id': task_id,
            'description': description.strip(),
            'due_date': due_date,
            'priority': priority.lower(),
            'category': category,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Task #{task_id} added successfully!")
        return task
    
    def view_tasks(
        self, 
        show_completed: bool = True,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        completed_only: bool = False
    ) -> None:
        """
        Display all tasks with optional filtering.
        
        Args:
            show_completed: Whether to show completed tasks
            category: Filter by category
            priority: Filter by priority
        """
        if not self.tasks:
            print("\n📋 No tasks yet. Add one to get started!")
            return
        
        # Filter tasks
        filtered_tasks = self.tasks
        
        if completed_only:
            filtered_tasks = [t for t in filtered_tasks if t['completed']]
        elif not show_completed:
            filtered_tasks = [t for t in filtered_tasks if not t['completed']]
        
        if category:
            filtered_tasks = [t for t in filtered_tasks if t.get('category') == category]
        
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.get('priority') == priority.lower()]
        
        if not filtered_tasks:
            print("\n📋 No tasks match your filters.")
            return
        
        # Separate and sort tasks
        pending = [t for t in filtered_tasks if not t['completed']]
        completed = [t for t in filtered_tasks if t['completed']]
        
        # Display pending tasks
        if pending:
            print("\n" + "="*60)
            print("📌 PENDING TASKS")
            print("="*60)
            for task in sorted(pending, key=lambda x: x.get('due_date') or '9999-99-99'):
                self._print_task(task)
        
        # Display completed tasks
        if completed and show_completed:
            print("\n" + "="*60)
            print("✓ COMPLETED TASKS")
            print("="*60)
            for task in completed:
                self._print_task(task)
        
        # Summary
        print("\n" + "-"*60)
        print(f"Total: {len(filtered_tasks)} tasks ({len(pending)} pending, {len(completed)} completed)")
        print("-"*60 + "\n")
    
    def _print_task(self, task: Dict) -> None:
        """Helper method to print a single task."""
        status = "✓" if task['completed'] else "○"
        priority_icon = {"low": "◇", "medium": "◆", "high": "◆◆"}
        
        print(f"\n{status} Task #{task['id']}")
        print(f"  {task['description']}")
        
        if task.get('due_date'):
            due = datetime.strptime(task['due_date'], "%Y-%m-%d")
            days_until = (due - datetime.now()).days
            
            if days_until < 0:
                due_text = f"⚠ OVERDUE by {abs(days_until)} days"
            elif days_until == 0:
                due_text = "⚠ DUE TODAY"
            else:
                due_text = f"Due in {days_until} days"
            
            print(f"  📅 {task['due_date']} ({due_text})")
        
        if task.get('priority'):
            icon = priority_icon.get(task['priority'], "◇")
            print(f"  {icon} Priority: {task['priority'].upper()}")
        
        if task.get('category'):
            print(f"  🏷  Category: {task['category']}")
    
    def complete_task(self, task_id: int) -> None:
        """
        Mark a task as complete.
        
        Args:
            task_id: ID of the task to complete
            
        Raises:
            ValueError: If task_id is not found
        """
        task = self._find_task(task_id)
        
        if task['completed']:
            print(f"⚠ Task #{task_id} is already completed!")
            return
        
        task['completed'] = True
        task['completed_at'] = datetime.now().isoformat()
        self.save_tasks()
        print(f"✓ Task #{task_id} marked as complete!")
    
    def delete_task(self, task_id: int) -> None:
        """
        Delete a task.
        
        Args:
            task_id: ID of the task to delete
            
        Raises:
            ValueError: If task_id is not found
        """
        task = self._find_task(task_id)
        self.tasks.remove(task)
        self.save_tasks()
        print(f"✓ Task #{task_id} deleted successfully!")
    
    def search_tasks(self, query: str) -> None:
        """
        Search tasks by description.
        
        Args:
            query: Search term
        """
        query_lower = query.lower()
        results = [t for t in self.tasks if query_lower in t['description'].lower()]
        
        if not results:
            print(f"\n🔍 No tasks found matching '{query}'")
            return
        
        print(f"\n🔍 Found {len(results)} task(s) matching '{query}':")
        print("="*60)
        for task in results:
            self._print_task(task)
        print()
    
    def _find_task(self, task_id: int) -> Dict:
        """
        Find a task by ID.
        
        Args:
            task_id: ID of the task to find
            
        Returns:
            Task dictionary
            
        Raises:
            ValueError: If task is not found
        """
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        raise ValueError(f"Task #{task_id} not found")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CLI Task Manager - Manage your tasks from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add "Complete Python project" --due 2026-01-25 --priority high
  %(prog)s list
  %(prog)s list --pending-only --priority high
  %(prog)s list --completed-only
  %(prog)s complete 1
  %(prog)s search "Python"
  %(prog)s delete 1
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')
    add_parser.add_argument('--due', help='Due date (YYYY-MM-DD)')
    add_parser.add_argument('--priority', choices=['low', 'medium', 'high'], 
                           default='medium', help='Task priority')
    add_parser.add_argument('--category', help='Task category')
    
    # List command
    list_parser = subparsers.add_parser('list', help='View all tasks')
    list_parser.add_argument('--pending-only', action='store_true', 
                            help='Show only pending tasks')
    list_parser.add_argument('--completed-only', action='store_true', 
                            help='Show only completed tasks')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--priority', choices=['low', 'medium', 'high'],
                            help='Filter by priority')
    
    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Mark task as complete')
    complete_parser.add_argument('task_id', type=int, help='Task ID to complete')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='Task ID to delete')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search tasks')
    search_parser.add_argument('query', help='Search term')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize task manager
    tm = TaskManager()
    
    try:
        if args.command == 'add':
            tm.add_task(
                args.description,
                due_date=args.due,
                priority=args.priority,
                category=args.category
            )
        
        elif args.command == 'list':
            if args.completed_only:
                tm.view_tasks(
                    show_completed=True,
                    category=args.category,
                    priority=args.priority,
                    completed_only=True
                )
            else:
                tm.view_tasks(
                    show_completed=not args.pending_only,
                    category=args.category,
                    priority=args.priority
                )
        
        elif args.command == 'complete':
            tm.complete_task(args.task_id)
        
        elif args.command == 'delete':
            tm.delete_task(args.task_id)
        
        elif args.command == 'search':
            tm.search_tasks(args.query)
    
    except ValueError as e:
        print(f"✗ Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()