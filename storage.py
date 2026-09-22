"""Task storage module for persistence."""
import json
import os
from datetime import datetime
from typing import List, Optional

from task import Task


class TaskStorage:
    """Handles storage and retrieval of tasks using JSON file."""
    
    def __init__(self, file_path: str = "tasks.json"):
        """Initialize storage with file path.
        
        Args:
            file_path: Path to the JSON file for storing tasks
        """
        self.file_path = file_path
    
    def load_tasks(self) -> List[Task]:
        """Load tasks from the storage file.
        
        Returns:
            List of Task objects
        """
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            
            tasks = []
            for task_data in data:
                # Convert string datetime back to datetime object
                created_at = datetime.fromisoformat(task_data['created_at'])
                task = Task(
                    description=task_data['description'],
                    completed=task_data['completed'],
                    created_at=created_at
                )
                tasks.append(task)
            return tasks
        except (json.JSONDecodeError, KeyError, ValueError):
            # If file is corrupted, return empty list
            return []
    
    def save_tasks(self, tasks: List[Task]) -> None:
        """Save tasks to the storage file.
        
        Args:
            tasks: List of Task objects to save
        """
        # Convert tasks to serializable format
        data = []
        for task in tasks:
            task_data = {
                'description': task.description,
                'completed': task.completed,
                'created_at': task.created_at.isoformat()
            }
            data.append(task_data)
        
        # Save to file
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)