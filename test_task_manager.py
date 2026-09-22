"""Tests for Task Manager CLI."""
import json
import os
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch, mock_open

from task import Task
from storage import TaskStorage
from task_manager import TaskManager


class TestTask(unittest.TestCase):
    """Test the Task data model."""
    
    def test_task_creation(self):
        """Test creating a task with default values."""
        task = Task("Test task")
        self.assertEqual(task.description, "Test task")
        self.assertFalse(task.completed)
        self.assertIsInstance(task.created_at, datetime)
    
    def test_task_creation_with_custom_timestamp(self):
        """Test creating a task with custom timestamp."""
        custom_time = datetime(2023, 1,机关的文档已更新，请问您需要继续查看哪个部分的内容呢？ 1, 12, 0, 0)
        task = Task("Test task", created_at=custom_time)
        self.assertEqual(task.created_at, custom_time)
    
    def test_mark_done(self):
        """Test marking a task as done."""
        task = Task("Test task")
        task.mark_done()
        self.assertTrue(task.completed)
    
    def test_mark_undone(self):
        """Test marking a task as undone."""
class TestTaskStorage(unittest.TestCase):
    """Test the TaskStorage class."""
    
    def setUp(self):
        """Set up test with temporary file."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.storage = TaskStorage(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary file."""
        os.unlink(self.temp_file.name)
    
    def test_load_tasks_empty_file(self):
        """Test loading tasks from empty/non-existent file."""
        tasks = self.storage.load_tasks()
        self.assertEqual(tasks, [])
    
    def test_save_and_load_tasks(self):
        """Test saving and loading tasks."""
        # Create test tasks
        task1 = Task("Task 1", created_at=datetime(2023, 1, 1, 12, 0, 0))
        task2 = Task("Task 2", completed=True, created_at=datetime(2023, 1, 2, 12, 0, 0))
        
        # Save tasks
        self.storage.save_tasks([task1, task2])
        
        # Load tasks back
        loaded_tasks = self.storage.load_tasks()
        
        # Verify loaded tasks
        self.assertEqual(len(loaded_tasks), 2)
        self.assertEqual(loaded_tasks[0].description, "Task 1")
        self.assertEqual(loaded_tasks[0].completed, False)
        self.assertEqual(loaded_tasks[0].created_at, datetime(2023, 1, 1, 12, 0, 0))
        
        self.assertEqual(loaded_tasks[1].description, "Task 2")
        self.assertEqual(loaded_tasks[1].completed, True)
        self.assertEqual(loaded_tasks[1].created_at, datetime(2023, 1, 2, 12, 0, 0))
    
    def test_load_tasks_corrupted_file(self):
        """Test loading tasks from corrupted JSON file."""
        # Write invalid JSON
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json content")
        
        tasks = self.storage.load_tasks()
        self.assertEqual(tasks, [])


class TestTaskManager(unittest.TestCase):
    """Test the TaskManager class."""
    
    def setUp(self):
        """Set up test with temporary file storage."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        storage = TaskStorage(self.temp_file.name)
        self.manager = TaskManager(storage)
    
    def tearDown(self):
        """Clean up temporary file."""
        os.unlink(self.temp_file.name)
    
    def test_create_task(self):
        """Test creating a new task."""
        task = self.manager.create_task("New task")
        
        self.assertEqual(task.description, "New task")
        self.assertFalse(task.completed)
        
        # Verify it was saved
        tasks = self.manager.storage.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "New task")
    
    def test_list_tasks_empty(self):
        """Test listing tasks when empty."""
        tasks = self.manager.list_tasks()
        self.assertEqual(tasks, [])
    
    def test_list_tasks_with_data(self):
    def test_delete_task_valid(self):
        """Test deleting a valid task."""
        self.manager.create_task("Task 1")
        self.manager.create_task("Task 2")
        self.manager.create_task("Task 3")
        
        result = self.manager.delete_task(2)  # Delete middle task
        self.assertTrue(result)
        
        tasks = self.manager.storage.load_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].description, "Task 1")
        self.assertEqual(tasks[1].description, "Task 3")
    
    def test_delete_task_invalid(self):
        """Test deleting an invalid task."""
        self.manager.create_task("Task 1")
        
        # Test with index too low
        result = self.manager.delete_task(0)
        self.assertFalse(result)
        
        # Test with index too high
        result = self.manager.delete_task(2)
        self.assertFalse(result)


class TestCLI(unittest.TestCase):
    """Test the CLI interface."""
    
    @patch('builtins.print')
    def test_create_command(self, mock_print):
        """Test create command via CLI."""
        with patch('sys.argv', ['task_manager.py', 'create', 'Test task']):
            from task_manager import main
            main()
        
        # Check that something was printed
        self.assertTrue(mock_print.called)
        call_args = mock_print.call_args[0][0]
        self.assertIn("Task created", call_args)
        self.assertIn("Test task", call_args)
    
    @patch('builtins.print')
    def test_list_command_empty(self, mock_print):
        """Test list command when no tasks exist."""
        with patch('sys.argv', ['task_manager.py', 'list']):
            from task_manager import main
            main()
        
        call_args = mock_print.call_args[0][0]
        self.assertEqual("No tasks found.", call_args)
    
    @patch('builtins.print')
    def test_done_command_invalid(self, mock_print):
        """Test done command with invalid index."""
        with patch('sys.argv', ['task_manager.py', 'done', '1']), \
             patch('sys.exit') as mock_exit:
            from task_manager import main
            main()
        
        mock_exit.assert_called_with(1)
        call_args = mock_print.call_args[0][0]
        self.assertIn("Error: Invalid task index", call_args)


if __name__ == '__main__':
    unittest.main()
        """Test listing tasks with data."""
        # Create some tasks
        self.manager.create_task("Task 1")
        self.manager.create_task("Task 2")
        
        # List all tasks
        all_tasks = self.manager.list_tasks(show_all=True)
        self.assertEqual(len(all_tasks), 2)
        
        # List pending tasks only (default)
        pending_tasks = self.manager.list_tasks(show_all=False)
        self.assertEqual(len(pending_tasks), 2)
    
    def test_list_tasks_filter_completed(self):
        """Test listing tasks with completed tasks filtered out."""
        # Create tasks and mark one as done
        self.manager.create_task("Task 1")
        self.manager.create_task("Task 2")
        self.manager.mark_task_done(1)  # Mark first task as done
        
        # List all tasks
        all_tasks = self.manager.list_tasks(show_all=True)
        self.assertEqual(len(all_tasks), 2)
        
        # List pending tasks only
        pending_tasks = self.manager.list_tasks(show_all=False)
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0].description, "Task 2")
    
    def test_mark_task_done_valid(self):
        """Test marking a valid task as done."""
        self.manager.create_task("Task 1")
        self.manager.create_task("Task 2")
        
        task = self.manager.mark_task_done(1)
        self.assertIsNotNone(task)
        self.assertTrue(task.completed)
        self.assertEqual(task.description, "Task 1")
        
        # Verify only first task is completed
        tasks = self.manager.storage.load_tasks()
        self.assertTrue(tasks[0].completed)
        self.assertFalse(tasks[1].completed)
    
    def test_mark_task_done_invalid(self):
        """Test marking an invalid task as done."""
        self.manager.create_task("Task 1")
        
        # Test with index too low
        task = self.manager.mark_task_done(0)
        self.assertIsNone(task)
        
        # Test with index too high
        task = self.manager.mark_task_done(2)
        self.assertIsNone(task)
        task = Task("Test task", completed=True)
        task.mark_undone()
        self.assertFalse(task.completed)
    
    def test_string_representation(self):
        """Test string representation of task."""
        custom_time = datetime(2023, 1, 1, 12, 0, 0)
        task = Task("Test task", created_at=custom_time)
        
        # Test pending task
        self.assertIn("[✗] Test task (created: 2023-01-01 12:00)", str(task))
        
        # Test completed task
        task.mark_done()
        self.assertIn("[✓] Test task (created: 2023-01-01 12:00)", str(task))