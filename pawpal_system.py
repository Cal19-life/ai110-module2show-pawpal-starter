"""
PawPal+ System Design
Classes and stubs for pet care task scheduling application
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


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
    completed: bool = False
    completedAt: Optional[str] = None
    isWalking: bool = False
    isFeeding: bool = False
    isMedication: bool = False
    isEnrichment: bool = False
    isGrooming: bool = False

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

    def updatePetInfo(self) -> None:
        """Update pet information."""
        pass


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


class Scheduler:
    """Orchestrates mutable task scheduling for a single-day plan."""

    def __init__(self, scheduledTasks: Dict[Task, TimeWindow] = None):
        self.scheduledTasks = scheduledTasks or {}

    def generateDailyPlan(
        self, owner: Owner, pets: List[Pet], tasks: List[Task]
    ) -> Dict[Task, TimeWindow]:
        """Generate/update a daily schedule based on owner preferences, pet needs, and tasks."""
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
