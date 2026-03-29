"""
PawPal+ System Design
Classes and stubs for pet care task scheduling application
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


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

    def createTask(self) -> None:
        """Create a new task."""
        pass

    def editTask(self) -> None:
        """Edit an existing task."""
        pass


@dataclass
class WalkingTask(Task):
    """Walking-specific task subclass."""
    pass


@dataclass
class FeedingTask(Task):
    """Feeding-specific task subclass."""
    pass


@dataclass
class MedicationTask(Task):
    """Medication-specific task subclass."""
    pass


@dataclass
class EnrichmentTask(Task):
    """Enrichment-specific task subclass."""
    pass


@dataclass
class GroomingTask(Task):
    """Grooming-specific task subclass."""
    pass


@dataclass
class Pet:
    """Represents a pet with care needs."""
    name: str
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


class DailyPlan:
    """Represents a daily schedule of tasks with assigned time windows."""

    def __init__(self, scheduledTasks: Dict[Task, TimeWindow] = None):
        self.scheduledTasks = scheduledTasks or {}

    def getDailyPlan(self) -> Dict[Task, TimeWindow]:
        """Retrieve the daily plan as a dictionary of tasks to time windows."""
        pass


class Scheduler:
    """Orchestrates daily plan generation and task scheduling."""

    def generateDailyPlan(
        self, owner: Owner, pets: List[Pet], tasks: List[Task]
    ) -> DailyPlan:
        """Generate a daily plan based on owner preferences, pet needs, and available tasks."""
        pass

    def explainPlan(self, plan: DailyPlan) -> str:
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
