from datetime import time
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pawpal_system


def make_window(day: int = 0, start_hour: int = 8, end_hour: int = 9) -> pawpal_system.TimeWindow:
	return pawpal_system.TimeWindow(
		dayOfWeek=day,
		startTime=time(start_hour, 0),
		endTime=time(end_hour, 0),
	)


def make_task(
	title: str = "Task",
	task_type: str = "walk",
	frequency: tuple[int, int] = (1, 1),
	completed: bool = False,
	priority: int = 1,
	is_walking: bool = False,
	is_feeding: bool = False,
	is_medication: bool = False,
	is_enrichment: bool = False,
	is_grooming: bool = False,
) -> pawpal_system.Task:
	task = pawpal_system.Task(
		title=title,
		type=task_type,
		durationMin=30,
		priority=priority,
		notes="sample",
		preferredTimeWindow=make_window(),
		frequency=frequency,
		isWalking=is_walking,
		isFeeding=is_feeding,
		isMedication=is_medication,
		isEnrichment=is_enrichment,
		isGrooming=is_grooming,
	)
	if completed:
		task.markComplete()
	return task


def make_owner_and_pet(
	owner_name: str = "Sady", pet_name: str = "Buddy"
) -> tuple[pawpal_system.Owner, pawpal_system.Pet]:
	owner = pawpal_system.Owner(name=owner_name)
	pet = pawpal_system.Pet(
		name=pet_name,
		owner=owner,
		walkNeedLevel=3,
		feedingNeedLevel=2,
		medNeedLevel=1,
		groomingNeedLevel=2,
	)
	owner.addPet(pet)
	return owner, pet


def test_task_frequency_rejects_negative_count() -> None:
	with pytest.raises(ValueError):
		make_task(frequency=(-1, 1))


def test_task_frequency_rejects_non_positive_days() -> None:
	with pytest.raises(ValueError):
		make_task(frequency=(1, 0))


def test_task_mark_complete_and_mark_incomplete() -> None:
	task = make_task()

	task.markComplete("2026-03-31T08:30")
	assert task.completed is True
	assert task.completedAt == "2026-03-31T08:30"

	task.markIncomplete()
	assert task.completed is False
	assert task.completedAt is None


def test_task_update_preferred_time_window() -> None:
	task = make_task()
	preferred = make_window(day=2, start_hour=10, end_hour=11)

	task.updatePreferredTime(preferred)

	assert task.preferredTimeWindow == preferred


def test_task_set_priority_validates_negative_values() -> None:
	task = make_task(priority=1)
	task.setPriority(5)
	assert task.priority == 5

	with pytest.raises(ValueError):
		task.setPriority(-1)


def test_task_set_duration_validates_non_positive_values() -> None:
	task = make_task()
	task.setDurationMin(45)
	assert task.durationMin == 45

	with pytest.raises(ValueError):
		task.setDurationMin(0)


def test_pet_add_remove_and_get_tasks_filters_completed() -> None:
	_, pet = make_owner_and_pet()
	walk = make_task(title="Walk", task_type="walk")
	feed = make_task(title="Feed", task_type="feeding", completed=True)

	pet.addTask(walk)
	pet.addTask(feed)

	assert pet.getTasks() == [walk]
	assert pet.getTasks(includeCompleted=True) == [walk, feed]

	pet.removeTask(walk)
	assert pet.tasks == [feed]


def test_pet_remove_missing_task_is_noop() -> None:
	_, pet = make_owner_and_pet()
	missing = make_task(title="Not Added")

	pet.removeTask(missing)
	assert pet.tasks == []


def test_pet_get_tasks_by_type_uses_flag_matches() -> None:
	_, pet = make_owner_and_pet()
	walk = make_task(title="Morning Walk", task_type="xyz", is_walking=True)
	feed = make_task(title="Breakfast", task_type="feeding", is_feeding=True)
	pet.addTask(walk)
	pet.addTask(feed)

	result = pet.getTasksByType("walk")

	assert result == [walk]


def test_pet_get_tasks_by_type_uses_type_fallback_and_completion_filter() -> None:
	_, pet = make_owner_and_pet()
	med_done = make_task(title="Med", task_type="medication", completed=True)
	med_due = make_task(title="Med 2", task_type="medication", completed=False)
	pet.addTask(med_done)
	pet.addTask(med_due)

	due_only = pet.getTasksByType("medication")
	all_matching = pet.getTasksByType("medication", includeCompleted=True)

	assert due_only == [med_due]
	assert all_matching == [med_done, med_due]


def test_owner_task_aggregation_across_multiple_pets() -> None:
	owner = pawpal_system.Owner(name="Sady")
	pet1 = pawpal_system.Pet("Buddy", owner, 3, 2, 1, 2)
	pet2 = pawpal_system.Pet("Benji", owner, 3, 3, 0, 1)
	owner.addPet(pet1)
	owner.addPet(pet2)

	t1 = make_task(title="Walk Buddy")
	t2 = make_task(title="Feed Benji", completed=True)
	pet1.addTask(t1)
	pet2.addTask(t2)

	assert owner.getAllTasks(includeCompleted=True) == [t1, t2]
	assert owner.getDueTasks() == [t1]


def test_owner_pet_management_methods() -> None:
	owner = pawpal_system.Owner(name="Sady")
	pet = pawpal_system.Pet("Buddy", owner, 3, 2, 1, 2)

	owner.addPet(pet)
	owner.addPet(pet)
	assert owner.getPets() == [pet]
	assert owner.getPetByName("Buddy") == pet
	assert owner.getPetByName("Missing") is None

	owner.removePet("Buddy")
	assert owner.getPets() == []


def test_owner_remove_pet_invalid_type_raises() -> None:
	owner = pawpal_system.Owner(name="Sady")

	with pytest.raises(TypeError):
		owner.removePet(123)


def test_owner_availability_lists_append_entries() -> None:
	owner = pawpal_system.Owner(name="Sady")
	available = make_window(day=1, start_hour=9, end_hour=10)
	blocked = make_window(day=1, start_hour=11, end_hour=12)

	owner.addAvailability(available)
	owner.addNotAvailable(blocked)

	assert owner.availabilities == [available]
	assert owner.notAvailable == [blocked]


def test_scheduler_add_remove_reschedule_and_get_scheduled_tasks() -> None:
	scheduler = pawpal_system.Scheduler()
	task = make_task(title="Morning Walk")
	slot_a = make_window(day=0, start_hour=7, end_hour=8)
	slot_b = make_window(day=0, start_hour=10, end_hour=11)

	scheduler.addScheduledTask(task, slot_a)
	assert scheduler.getScheduledTasks() == [task]
	assert task.scheduledTimeWindow == slot_a

	scheduler.rescheduleTaskTime(task, slot_b)
	assert scheduler.getScheduledTasks() == [task]
	assert task.scheduledTimeWindow == slot_b

	scheduler.removeScheduledTask(task)
	assert scheduler.getScheduledTasks() == []
	assert task.scheduledTimeWindow is None


def test_scheduler_add_does_not_overwrite_existing_scheduled_time() -> None:
	scheduler = pawpal_system.Scheduler()
	task = make_task(title="Repeat Add")
	slot_a = make_window(day=0, start_hour=8, end_hour=9)
	slot_b = make_window(day=0, start_hour=9, end_hour=10)

	scheduler.addScheduledTask(task, slot_a)
	scheduler.addScheduledTask(task, slot_b)

	assert scheduler.getScheduledTasks() == [task]
	assert task.scheduledTimeWindow == slot_a


def test_scheduler_remove_unscheduled_task_with_stale_window_clears_it() -> None:
	scheduler = pawpal_system.Scheduler()
	task = make_task(title="Loose Task")
	task._updateScheduledTime(make_window(day=4, start_hour=15, end_hour=16))

	scheduler.removeScheduledTask(task)

	assert scheduler.getScheduledTasks() == []
	assert task.scheduledTimeWindow is None


def test_scheduler_remove_unscheduled_task_with_no_window_is_safe() -> None:
	scheduler = pawpal_system.Scheduler()
	task = make_task(title="Already Clear")

	scheduler.removeScheduledTask(task)

	assert scheduler.getScheduledTasks() == []
	assert task.scheduledTimeWindow is None
