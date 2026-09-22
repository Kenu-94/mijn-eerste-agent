#!/usr/bin/env python3
"""Task Manager CLI."""
import argparse
import sys
from typing import List

from storage import TaskStorage
from task import Task


class TaskManager:
    """Main task manager class handling all CLI operations."""
    
    def __init__(self, storage: Optional[TaskStorage] = None):
        """Initialize task manager with storage.
        
        Args:
            storage: TaskStorage instance (defaults to TaskStorage())
        """
        self.storage = storage or TaskStorage()
    
    def create_task(self, description: str) -> Task:
        """Create a new task.
        
        Args:
            description: Description of the task
            
        Returns:
            Created Task object
        """
        task = Task(description=description)
        tasks = self.storage.load_tasks()
        tasks.append(task)
        self.storage.save_tasks(tasks)
        return task
    
    def list_tasks(self, show_all: bool = False) -> List[Task]:
        """List tasks.
        
        Args:
            show_all: If True, show all tasks. If False, show only pending tasks.
            
        Returns:
            List of Task objects
        """
        tasks = self.storage.load_tasks()
        if not show_all:
            tasks = [task for task in tasks if not task.completed]
        return tasks
    
    def mark_task_done(self, task_index: int) -> Optional[Task]:
        """Mark a task as done.
        
        Args:
            task_index: Index of the task to mark as done (1-based)
            
        Returns:
            Updated Task object or None if index is invalid
        """
        tasks = self.storage.load_tasks()
        
        # Validate index (convert from 1-based to 0-based)
        if task_index < 1 or task_index > len(tasks):
            return None
        
        task = tasks[task_index - 1]
        task.mark_done()
        self.storage.save_tasks(tasks)
        return task
    
    def delete_task(self, task_index: int) -> bool:
        """Delete a task.
        
        Args:
            task_index: Index of the task to delete (1-based)
            
        Returns:
            True if task was deleted, False if index is invalid
        """
        tasks = self.storage.load_tasks()
        
        # Validate index (convert from 1-based to 0-based)
        if task_index < 1 or task_index > len(tasks):
            return False
        
        del tasks[task_index - 1]
        self.storage.save_tasks(tasks)
        return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Task Manager CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create task command
    create_parser = subparsers.add_parser('create', help='Create a new task')
    create_parser.add_argument('description', help='Task description')
    
    # List tasks command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--all', action='store_true', 
                           help='Show all tasks including completed ones')
    
    # Mark task done command
    done_parser = subparsers.add_parser('done', help='Mark a task as done')
    done_parser.add_argument('task_index', type=int, 
                           help='Index of the task to mark as done')
    
    # Delete task command (bonus feature)
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_index', type=int, 
                             help='Index of the task to delete')
    
    args = parser.parse_args()
    manager = TaskManager()
    
    if args.command == 'create':
        task = manager.create_task(args.description)
        print(f"Task created: {task}")
    
    elif args.command == 'list':
        tasks = manager.list_tasks(show_all=args.all)
        if not tasks:
            print("No tasks found.")
        else:
            print(f"Tasks ({'all' if args.all else 'pending only'}):")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
    
    elif args.command == 'done':
        task = manager.mark_task_done(args.task_index)
        if task:
            print(f"Task marked as done: {task}")
        else:
            print(f"Error: Invalid task index {args.task_index}")
            sys.exit(1)
    
    elif args.command == 'delete':
        if manager.delete_task(args.task_index):
            print(f"Task {args.task_index} deleted")
        else:
            print(f"Error: Invalid task index {args.task_index}")
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()