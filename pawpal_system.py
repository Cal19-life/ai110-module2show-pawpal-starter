"""
PawPal+ System Design
Classes and stubs for pet care task scheduling application
"""

from dataclasses import dataclass, field
from datetime import date, time, timedelta
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
    recurrenceStartDate: date = field(default_factory=date.today)
    completedCountInCycle: int = 0
    completionDayNumbers: List[int] = field(default_factory=list)
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
        if not isinstance(self.recurrenceStartDate, date):
            raise ValueError("recurrenceStartDate must be a datetime.date")

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

    def __init__(self, scheduledTasks: Optional[List[Task]] = None, recurringTasks: Optional[List[Task]] = None):
        """Initialize scheduler task lists for scheduled instances and recurring templates."""
        self.scheduledTasks = scheduledTasks or []
        self.recurringTasks = recurringTasks or []

    def registerRecurringTask(self, task: Task) -> None:
        """Register a task as recurrence-managed by the scheduler."""
        if task not in self.recurringTasks:
            self.recurringTasks.append(task)

    def unregisterRecurringTask(self, task: Task) -> None:
        """Remove a task from recurrence management."""
        if task in self.recurringTasks:
            self.recurringTasks.remove(task)

    def _dayNumberForDate(self, onDate: date) -> int:
        """Return absolute day-number representation for a date."""
        return onDate.toordinal()



    def _syncTaskCycle(self, task: Task, onDate: date) -> None:
        """Reset completion counters and snap anchor when crossing a cycle boundary."""
        if onDate < task.recurrenceStartDate:
            task.completedCountInCycle = 0
            task.completionDayNumbers.clear()
            task.markIncomplete()
            return

        cycleDays = task.frequency[1]
        elapsedDays = (onDate - task.recurrenceStartDate).days

        # If we've entered a new cycle, snap the anchor forward and reset
        if elapsedDays >= cycleDays:
            completedCycles = elapsedDays // cycleDays
            task.recurrenceStartDate = task.recurrenceStartDate + timedelta(days=completedCycles * cycleDays)
            task.completedCountInCycle = 0
            task.completionDayNumbers.clear()
            task.markIncomplete()

    def _matchesTaskWeekday(self, task: Task, dayOfWeek: int) -> bool:
        """Return True if a task is allowed to run on the provided weekday."""
        if task.preferredTimeWindow is None:
            return True
        return task.preferredTimeWindow.dayOfWeek == dayOfWeek

    def canScheduleTaskOnDate(self, task: Task, onDate: date) -> bool:
        """Check recurrence and weekday constraints for a task on a specific date."""
        requiredCount, _ = task.frequency
        if requiredCount <= 0:
            return False
        if onDate < task.recurrenceStartDate:
            return False

        self._syncTaskCycle(task, onDate)

        dayOfWeek = onDate.weekday()
        if not self._matchesTaskWeekday(task, dayOfWeek):
            return False

        return task.completedCountInCycle < requiredCount

    def markTaskCompleteForDate(self, task: Task, onDate: date, completedAt: Optional[str] = None) -> None:
        """Record one completion event and increment cycle counters safely."""
        if not self.canScheduleTaskOnDate(task, onDate):
            return

        requiredCount, _ = task.frequency
        if task.completedCountInCycle >= requiredCount:
            return

        dayNumber = self._dayNumberForDate(onDate)
        if dayNumber in task.completionDayNumbers:
            return

        task.completedCountInCycle += 1
        task.completionDayNumbers.append(dayNumber)
        task.markComplete(completedAt)

    def autoAddRecurringTasksForDate(self, owner: Owner, onDate: date) -> List[Task]:
        """Auto-add all due recurring owner tasks to scheduledTasks for the given date."""
        sourceTasks = owner.getAllTasks(includeCompleted=True)
        dueTasks: List[Task] = []
        dayOfWeek = onDate.weekday()

        for task in sourceTasks:
            if task not in self.recurringTasks:
                self.registerRecurringTask(task)

            if not self.canScheduleTaskOnDate(task, onDate):
                continue

            preferredWindow = task.preferredTimeWindow
            if preferredWindow is not None:
                if task.scheduledTimeWindow is None or task.scheduledTimeWindow.dayOfWeek != dayOfWeek:
                    self.rescheduleTaskTime(task, preferredWindow)

            if task not in self.scheduledTasks:
                self.scheduledTasks.append(task)

            dueTasks.append(task)

        return dueTasks

    def canScheduleTaskOnDay(self, task: Task, dayNumber: int, dayOfWeek: int) -> bool:
        """Compatibility wrapper for day-number based callers."""
        onDate = date.fromordinal(dayNumber)
        return self.canScheduleTaskOnDate(task, onDate)

    def markTaskCompleteForDay(self, task: Task, dayNumber: int, dayOfWeek: int, completedAt: Optional[str] = None) -> None:
        """Compatibility wrapper for day-number based callers."""
        onDate = date.fromordinal(dayNumber)
        self.markTaskCompleteForDate(task, onDate, completedAt)

    def autoAddRecurringTasksForDay(self, owner: Owner, dayNumber: int, dayOfWeek: int) -> List[Task]:
        """Compatibility wrapper for day-number based callers."""
        onDate = date.fromordinal(dayNumber)
        return self.autoAddRecurringTasksForDate(owner, onDate)

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
