"""
Test Suite for CLI Task Manager
Run with: pytest test_task_manager.py -v
"""

import pytest
import json
from pathlib import Path
from datetime import datetime, timedelta
from task_manager import TaskManager, Priority


@pytest.fixture
def temp_task_file(tmp_path):
    """Create a temporary task file for testing."""
    test_file = tmp_path / "test_tasks.json"
    return str(test_file)


@pytest.fixture
def task_manager(temp_task_file):
    """Create a TaskManager instance with temporary file."""
    return TaskManager(filepath=temp_task_file)


@pytest.fixture
def task_manager_with_data(task_manager):
    """Create a TaskManager with sample data."""
    task_manager.add_task("Complete project", due_date="2026-02-01", priority="high")
    task_manager.add_task("Review code", priority="medium", category="development")
    task_manager.add_task("Write tests", due_date="2026-01-25", priority="low")
    return task_manager


class TestTaskManagerInitialization:
    """Test TaskManager initialization and file handling."""
    
    def test_creates_new_file_if_not_exists(self, temp_task_file):
        """Should create a new tasks file if it doesn't exist."""
        tm = TaskManager(filepath=temp_task_file)
        assert Path(temp_task_file).exists()
        assert tm.tasks == []
    
    def test_loads_existing_tasks(self, temp_task_file):
        """Should load tasks from existing file."""
        # Create file with sample data
        sample_tasks = [
            {"id": 1, "description": "Test task", "completed": False}
        ]
        with open(temp_task_file, 'w') as f:
            json.dump(sample_tasks, f)
        
        tm = TaskManager(filepath=temp_task_file)
        assert len(tm.tasks) == 1
        assert tm.tasks[0]["description"] == "Test task"
    
    def test_handles_corrupted_json(self, temp_task_file):
        """Should handle corrupted JSON gracefully."""
        # Write invalid JSON
        with open(temp_task_file, 'w') as f:
            f.write("{ invalid json }")
        
        tm = TaskManager(filepath=temp_task_file)
        assert tm.tasks == []


class TestAddTask:
    """Test task addition functionality."""
    
    def test_add_basic_task(self, task_manager):
        """Should add a basic task successfully."""
        task = task_manager.add_task("Test task")
        
        assert task["id"] == 1
        assert task["description"] == "Test task"
        assert task["completed"] is False
        assert "created_at" in task
        assert len(task_manager.tasks) == 1
    
    def test_add_task_with_all_fields(self, task_manager):
        """Should add task with all optional fields."""
        task = task_manager.add_task(
            "Complex task",
            due_date="2026-02-15",
            priority="high",
            category="work"
        )
        
        assert task["description"] == "Complex task"
        assert task["due_date"] == "2026-02-15"
        assert task["priority"] == "high"
        assert task["category"] == "work"
    
    def test_increments_task_ids(self, task_manager):
        """Should increment task IDs correctly."""
        task1 = task_manager.add_task("First task")
        task2 = task_manager.add_task("Second task")
        task3 = task_manager.add_task("Third task")
        
        assert task1["id"] == 1
        assert task2["id"] == 2
        assert task3["id"] == 3
    
    def test_strips_whitespace_from_description(self, task_manager):
        """Should strip leading/trailing whitespace."""
        task = task_manager.add_task("  Task with spaces  ")
        assert task["description"] == "Task with spaces"
    
    def test_rejects_empty_description(self, task_manager):
        """Should reject empty or whitespace-only descriptions."""
        with pytest.raises(ValueError, match="cannot be empty"):
            task_manager.add_task("")
        
        with pytest.raises(ValueError, match="cannot be empty"):
            task_manager.add_task("   ")
    
    def test_validates_due_date_format(self, task_manager):
        """Should validate due date format."""
        with pytest.raises(ValueError, match="YYYY-MM-DD format"):
            task_manager.add_task("Task", due_date="2026/01/25")
        
        with pytest.raises(ValueError, match="YYYY-MM-DD format"):
            task_manager.add_task("Task", due_date="25-01-2026")
        
        with pytest.raises(ValueError, match="YYYY-MM-DD format"):
            task_manager.add_task("Task", due_date="invalid")
    
    def test_validates_priority(self, task_manager):
        """Should validate priority values."""
        with pytest.raises(ValueError, match="Priority must be one of"):
            task_manager.add_task("Task", priority="urgent")
        
        # Should accept valid priorities (case-insensitive)
        task = task_manager.add_task("Task", priority="HIGH")
        assert task["priority"] == "high"
    
    def test_persists_to_file(self, task_manager, temp_task_file):
        """Should save task to JSON file."""
        task_manager.add_task("Persistent task")
        
        with open(temp_task_file, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 1
        assert data[0]["description"] == "Persistent task"


class TestCompleteTask:
    """Test task completion functionality."""
    
    def test_complete_task(self, task_manager_with_data):
        """Should mark task as complete."""
        task_manager_with_data.complete_task(1)
        
        task = task_manager_with_data._find_task(1)
        assert task["completed"] is True
        assert "completed_at" in task
    
    def test_complete_already_completed_task(self, task_manager_with_data, capsys):
        """Should handle already completed tasks gracefully."""
        task_manager_with_data.complete_task(1)
        task_manager_with_data.complete_task(1)  # Try again
        
        captured = capsys.readouterr()
        assert "already completed" in captured.out
    
    def test_complete_nonexistent_task(self, task_manager_with_data):
        """Should raise error for nonexistent task."""
        with pytest.raises(ValueError, match="not found"):
            task_manager_with_data.complete_task(999)
    
    def test_persists_completion(self, task_manager_with_data, temp_task_file):
        """Should persist completion status to file."""
        task_manager_with_data.complete_task(1)
        
        # Reload from file
        tm_new = TaskManager(filepath=temp_task_file)
        task = tm_new._find_task(1)
        assert task["completed"] is True


class TestDeleteTask:
    """Test task deletion functionality."""
    
    def test_delete_task(self, task_manager_with_data):
        """Should delete task successfully."""
        initial_count = len(task_manager_with_data.tasks)
        task_manager_with_data.delete_task(1)
        
        assert len(task_manager_with_data.tasks) == initial_count - 1
        
        with pytest.raises(ValueError, match="not found"):
            task_manager_with_data._find_task(1)
    
    def test_delete_nonexistent_task(self, task_manager_with_data):
        """Should raise error when deleting nonexistent task."""
        with pytest.raises(ValueError, match="not found"):
            task_manager_with_data.delete_task(999)
    
    def test_persists_deletion(self, task_manager_with_data, temp_task_file):
        """Should persist deletion to file."""
        task_manager_with_data.delete_task(2)
        
        # Reload from file
        tm_new = TaskManager(filepath=temp_task_file)
        assert len(tm_new.tasks) == 2
        
        with pytest.raises(ValueError):
            tm_new._find_task(2)


class TestViewTasks:
    """Test task viewing and filtering."""
    
    def test_view_all_tasks(self, task_manager_with_data, capsys):
        """Should display all tasks."""
        task_manager_with_data.view_tasks()
        
        captured = capsys.readouterr()
        assert "Complete project" in captured.out
        assert "Review code" in captured.out
        assert "Write tests" in captured.out
    
    def test_view_pending_only(self, task_manager_with_data, capsys):
        """Should show only pending tasks."""
        task_manager_with_data.complete_task(1)
        task_manager_with_data.view_tasks(show_completed=False)
        
        captured = capsys.readouterr()
        assert "PENDING TASKS" in captured.out
        assert "COMPLETED TASKS" not in captured.out
    
    def test_filter_by_category(self, task_manager_with_data, capsys):
        """Should filter tasks by category."""
        task_manager_with_data.view_tasks(category="development")
        
        captured = capsys.readouterr()
        assert "Review code" in captured.out
        assert "Complete project" not in captured.out
    
    def test_filter_by_priority(self, task_manager_with_data, capsys):
        """Should filter tasks by priority."""
        task_manager_with_data.view_tasks(priority="high")
        
        captured = capsys.readouterr()
        assert "Complete project" in captured.out
        assert "Review code" not in captured.out
    
    def test_empty_task_list(self, task_manager, capsys):
        """Should handle empty task list gracefully."""
        task_manager.view_tasks()
        
        captured = capsys.readouterr()
        assert "No tasks yet" in captured.out
    
    def test_shows_overdue_warning(self, task_manager, capsys):
        """Should show overdue warning for past dates."""
        past_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        task_manager.add_task("Overdue task", due_date=past_date)
        task_manager.view_tasks()
        
        captured = capsys.readouterr()
        assert "OVERDUE" in captured.out


class TestSearchTasks:
    """Test task search functionality."""
    
    def test_search_finds_matching_tasks(self, task_manager_with_data, capsys):
        """Should find tasks matching search query."""
        task_manager_with_data.search_tasks("code")
        
        captured = capsys.readouterr()
        assert "Review code" in captured.out
        assert "Complete project" not in captured.out
    
    def test_search_case_insensitive(self, task_manager_with_data, capsys):
        """Should perform case-insensitive search."""
        task_manager_with_data.search_tasks("CODE")
        
        captured = capsys.readouterr()
        assert "Review code" in captured.out
    
    def test_search_no_results(self, task_manager_with_data, capsys):
        """Should handle no search results."""
        task_manager_with_data.search_tasks("nonexistent")
        
        captured = capsys.readouterr()
        assert "No tasks found" in captured.out
    
    def test_search_partial_match(self, task_manager_with_data, capsys):
        """Should find partial matches."""
        task_manager_with_data.search_tasks("test")
        
        captured = capsys.readouterr()
        assert "Write tests" in captured.out


class TestFindTask:
    """Test internal task finding helper."""
    
    def test_find_existing_task(self, task_manager_with_data):
        """Should find task by ID."""
        task = task_manager_with_data._find_task(1)
        assert task["id"] == 1
        assert task["description"] == "Complete project"
    
    def test_find_nonexistent_task(self, task_manager_with_data):
        """Should raise error for nonexistent task."""
        with pytest.raises(ValueError, match="Task #999 not found"):
            task_manager_with_data._find_task(999)


class TestPriorityEnum:
    """Test Priority enum."""
    
    def test_priority_values(self):
        """Should have correct priority values."""
        assert Priority.LOW.value == "low"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.HIGH.value == "high"
    
    def test_priority_from_string(self):
        """Should create Priority from string."""
        assert Priority("low") == Priority.LOW
        assert Priority("medium") == Priority.MEDIUM
        assert Priority("high") == Priority.HIGH


class TestEdgeCases:
    """Test edge cases and error scenarios."""
    
    def test_handles_file_permission_error(self, tmp_path, monkeypatch):
        """Should handle file permission errors gracefully."""
        test_file = tmp_path / "readonly.json"
        test_file.write_text("[]")
        test_file.chmod(0o444)  # Read-only
        
        tm = TaskManager(filepath=str(test_file))
        # Should not crash when trying to save
        # (will print error but continue)
    
    def test_multiple_tasks_same_due_date(self, task_manager):
        """Should handle multiple tasks with same due date."""
        task_manager.add_task("Task 1", due_date="2026-02-01")
        task_manager.add_task("Task 2", due_date="2026-02-01")
        task_manager.add_task("Task 3", due_date="2026-02-01")
        
        assert len(task_manager.tasks) == 3
    
    def test_unicode_in_description(self, task_manager):
        """Should handle unicode characters in descriptions."""
        task = task_manager.add_task("Task with emoji 🚀 and unicode: café")
        assert "🚀" in task["description"]
        assert "café" in task["description"]
    
    def test_very_long_description(self, task_manager):
        """Should handle very long descriptions."""
        long_desc = "A" * 1000
        task = task_manager.add_task(long_desc)
        assert len(task["description"]) == 1000


# Integration Tests
class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_complete_workflow(self, task_manager):
        """Test complete task lifecycle."""
        # Add multiple tasks
        task1 = task_manager.add_task("Task 1", priority="high")
        task2 = task_manager.add_task("Task 2", due_date="2026-02-01")
        task3 = task_manager.add_task("Task 3", category="work")
        
        # Complete one task
        task_manager.complete_task(task1["id"])
        
        # Delete one task
        task_manager.delete_task(task2["id"])
        
        # Verify final state
        assert len(task_manager.tasks) == 2
        assert task_manager._find_task(task1["id"])["completed"] is True
        
        with pytest.raises(ValueError):
            task_manager._find_task(task2["id"])
    
    def test_persistence_across_instances(self, temp_task_file):
        """Test data persistence across different instances."""
        # Create and populate first instance
        tm1 = TaskManager(filepath=temp_task_file)
        tm1.add_task("Persistent task", priority="high")
        task_id = tm1.tasks[0]["id"]
        
        # Create second instance and verify data persisted
        tm2 = TaskManager(filepath=temp_task_file)
        assert len(tm2.tasks) == 1
        assert tm2.tasks[0]["description"] == "Persistent task"
        
        # Modify in second instance
        tm2.complete_task(task_id)
        
        # Verify in third instance
        tm3 = TaskManager(filepath=temp_task_file)
        assert tm3._find_task(task_id)["completed"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])