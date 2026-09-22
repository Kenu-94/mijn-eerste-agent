"""Task data model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a task with description, completion status, and creation timestamp."""
    description: str
    completed: bool = False
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Set creation timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def mark_done(self) -> None:
        """Mark the task as completed."""
        self.completed = True
    
    def mark_undone(self) -> None:
        """Mark the task as not completed."""
        self.completed = False
    
    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.description} (created: {self.created_at.strftime('%Y-%m-%d %H:%M')})"