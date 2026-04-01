"""
PawPal+ System Design
Classes and stubs for pet care task scheduling application
"""

from dataclasses import dataclass, field
from datetime import time
from typing import Dict, List, Optional, Tuple


@dataclass
class TimeWindow:
    """Represents a time window with day of week and start/end times."""
    dayOfWeek: int
    startTime: time
    endTime: time


@dataclass
class Task:
    """Base task class representing a pet care activity."""
    title: str
    type: str #TODO del later, redundant with isType boolean flags
    durationMin: int #TODO del later, redundant since saving scheduledTimeWindow
    priority: int
    notes: str
    description: Optional[str] = None
    preferredTimeWindow: Optional[TimeWindow] = None
    scheduledTimeWindow: Optional[TimeWindow] = None
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

    def updatePreferredTime(self, timeWindow: Optional[TimeWindow]) -> None:
        """Update the preferred time window for this task."""
        self.preferredTimeWindow = timeWindow

    def _updateScheduledTime(self, timeWindow: Optional[TimeWindow]) -> None:
        """Internal: Scheduler-owned mutation for scheduled task window."""
        self.scheduledTimeWindow = timeWindow

    def setPriority(self, priority: int) -> None:
        """Set task priority with basic validation."""
        if priority < 0:
            raise ValueError("priority must be >= 0")
        self.priority = priority

    def setDurationMin(self, minutes: int) -> None:
        """Set task duration in minutes with basic validation."""
        if minutes <= 0:
            raise ValueError("durationMin must be > 0")
        self.durationMin = minutes


@dataclass
class Pet:
    """Represents a pet with care needs."""
    name: str
    owner: "Owner"
    walkNeedLevel: int
    feedingNeedLevel: int
    medNeedLevel: int
    groomingNeedLevel: int
    tasks: List[Task] = field(default_factory=list)

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

    def getTasksByType(self, taskType: str, includeCompleted: bool = False) -> List[Task]:
        """Return tasks matching a task type, using flags first and type string as fallback."""
        normalizedType = taskType.strip().lower()

        flagByType = {
            "walk": "isWalking",
            "walking": "isWalking",
            "feed": "isFeeding",
            "feeding": "isFeeding",
            "med": "isMedication",
            "medication": "isMedication",
            "medicine": "isMedication",
            "enrichment": "isEnrichment",
            "groom": "isGrooming",
            "grooming": "isGrooming",
        }
        flagName = flagByType.get(normalizedType)

        candidateTasks = self.tasks if includeCompleted else [task for task in self.tasks if not task.completed]

        matched: List[Task] = []
        for task in candidateTasks:
            hasFlagMatch = flagName is not None and getattr(task, flagName, False)
            hasTypeFallbackMatch = task.type.strip().lower() == normalizedType
            if hasFlagMatch or hasTypeFallbackMatch:
                matched.append(task)

        return matched


@dataclass
class Owner:
    """Represents a pet owner with preferences and availability."""
    name: str
    preferences: List[str] = field(default_factory=list)
    availabilities: List[TimeWindow] = field(default_factory=list)
    notAvailable: List[TimeWindow] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

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

    def getPets(self) -> List[Pet]:
        """Return all pets associated with this owner."""
        return list(self.pets)

    def addPet(self, pet: Pet) -> None:
        """Add a pet to this owner if not already present."""
        if pet not in self.pets:
            self.pets.append(pet)
        pet.owner = self

    def removePet(self, petOrName: object) -> None:
        """Remove a pet by object or pet name."""
        if isinstance(petOrName, Pet):
            if petOrName in self.pets:
                self.pets.remove(petOrName)
            return

        if isinstance(petOrName, str):
            pet = self.getPetByName(petOrName)
            if pet is not None:
                self.pets.remove(pet)
            return

        raise TypeError("removePet expects a Pet instance or pet name string")

    def getPetByName(self, name: str) -> Optional[Pet]:
        """Return the first pet with a matching name, if any.
        Only looks for exact matches. Returns the first match found. 
        Returns None if no match is found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def addAvailability(self, timeWindow: TimeWindow) -> None:
        """Add an available time window for this owner."""
        self.availabilities.append(timeWindow)

    def addNotAvailable(self, timeWindow: TimeWindow) -> None:
        """Add an unavailable time window for this owner."""
        self.notAvailable.append(timeWindow)


class Scheduler:
    """Orchestrates mutable task scheduling for a single-day plan."""

    def __init__(self, scheduledTasks: List[Task] = None):
        self.scheduledTasks = scheduledTasks or []

    def generateDailyPlan(
        self, owner: Owner, date: Optional[str] = None
    ) -> Dict[Task, TimeWindow]:
        """Generate/update a daily schedule by retrieving cross-pet tasks from the owner."""
        pass

    def explainPlan(self, plan: Dict[Task, TimeWindow]) -> str:
        """Provide explanation/reasoning for the generated plan."""
        pass

    def addTasktoSchedule(self, task: Task, timewindow: TimeWindow) -> None:
        """Add a task to the schedule at a specific time window."""
        if task not in self.scheduledTasks:
            task._updateScheduledTime(timewindow) # so we don't update the timewindow if in scheduledTasks already
            self.scheduledTasks.append(task)

    def removeScheduledTask(self, task: Task) -> None:
        """Remove a task from the schedule."""
        if task in self.scheduledTasks:
            self.scheduledTasks.remove(task)
        task._updateScheduledTime(None)

    def rescheduleTaskTime(self, task: Task, timewindow: TimeWindow) -> None:
        """Reschedule a task to a new time window."""
        if task not in self.scheduledTasks:
            self.scheduledTasks.append(task)
        task._updateScheduledTime(timewindow)

    def getScheduledTasks(self) -> List[Task]:
        """Return currently scheduled tasks."""
        return list(self.scheduledTasks)
