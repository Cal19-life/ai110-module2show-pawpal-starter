"""
PawPal+ System Design
Classes and stubs for pet care task scheduling application
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class TimeWindow:
    """Represents a time window with day of week and start/end times."""
    dayOfWeek: int
    startTime: str
    endTime: str


@dataclass
class Task:
    """Base task class representing a pet care activity."""
    title: str
    type: str
    durationMin: int
    priority: int
    notes: str
    description: Optional[str] = None
    preferredTimeWindow: Optional[TimeWindow] = None
    frequency: Tuple[int, int] = (1, 1)
    completed: bool = False
    completedAt: Optional[str] = None
    isWalking: bool = False
    isFeeding: bool = False
    isMedication: bool = False
    isEnrichment: bool = False
    isGrooming: bool = False

    def __post_init__(self) -> None:
        """Validate frequency tuple on task initialization."""
        count, days = self.frequency
        if count < 0 or days <= 0:
            raise ValueError(f"frequency must be (count >= 0, days > 0), got {self.frequency}")

    def editTask(self) -> None:
        """Edit an existing task."""
        pass

    def markComplete(self, completedAt: Optional[str] = None) -> None:
        """Mark a task as completed, optionally with a completion timestamp."""
        self.completed = True
        self.completedAt = completedAt

    def markIncomplete(self) -> None:
        """Mark a task as not completed and clear completion metadata."""
        self.completed = False
        self.completedAt = None


@dataclass
class Pet:
    """Represents a pet with care needs."""
    name: str
    owner: "Owner"
    walkNeedLevel: int
    feedingNeedLevel: int
    medNeedLevel: int
    groomingNeedLevel: int
    tasks: List[Task] = None

    def __post_init__(self) -> None:
        """Ensure each pet has its own task list by default."""
        if self.tasks is None:
            self.tasks = []

    def updatePetInfo(self) -> None:
        """Update pet information."""
        pass

    def addTask(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def removeTask(self, task: Task) -> None:
        """Remove a task from this pet's task list if present."""
        if task in self.tasks:
            self.tasks.remove(task)

    def getTasks(self, includeCompleted: bool = False) -> List[Task]: #Unsure why I'd need to return tasks, but still helpful boilerplate code to write if I do 
        """Return this pet's tasks, optionally including completed tasks."""
        if includeCompleted:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]


class Owner:
    """Represents a pet owner with preferences and availability."""

    def __init__(
        self,
        name: str,
        preferences: List[str] = None,
        availabilities: List[TimeWindow] = None,
        notAvailable: List[TimeWindow] = None,
        pets: List[Pet] = None,
    ):
        self.name = name
        self.preferences = preferences or []
        self.availabilities = availabilities or []
        self.notAvailable = notAvailable or []
        self.pets = pets or []

    def createOwner(self) -> None:
        """Create a new owner record."""
        pass

    def editOwnerInfo(self) -> None:
        """Edit owner information."""
        pass

    def getAllTasks(self, includeCompleted: bool = False) -> List[Task]:
        """Return tasks across all pets owned by this owner."""
        allTasks: List[Task] = []
        for pet in self.pets:
            allTasks.extend(pet.getTasks(includeCompleted=includeCompleted))
        return allTasks

    def getDueTasks(self) -> List[Task]:
        """Return due tasks across all pets (currently modeled as incomplete tasks)."""
        return self.getAllTasks(includeCompleted=False)


class Scheduler:
    """Orchestrates mutable task scheduling for a single-day plan."""

    def __init__(self, scheduledTasks: Dict[Task, TimeWindow] = None):
        self.scheduledTasks = scheduledTasks or {}

    def generateDailyPlan(
        self, owner: Owner, date: Optional[str] = None
    ) -> Dict[Task, TimeWindow]:
        """Generate/update a daily schedule by retrieving cross-pet tasks from the owner."""
        pass

    def explainPlan(self, plan: Dict[Task, TimeWindow]) -> str:
        """Provide explanation/reasoning for the generated plan."""
        pass

    def addScheduledTask(self, task: Task, timewindow: TimeWindow) -> None:
        """Add a task to the schedule at a specific time window."""
        pass

    def removeScheduledTask(self, task: Task) -> None:
        """Remove a task from the schedule."""
        pass

    def rescheduleTaskTime(self, task: Task, timewindow: TimeWindow) -> None:
        """Reschedule a task to a new time window."""
        pass
