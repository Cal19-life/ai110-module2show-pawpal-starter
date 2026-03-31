import pawpal_system
from datetime import time


def format_schedule(tasks: list[pawpal_system.Task]) -> str:
    """Return a readable terminal table for scheduled and unscheduled tasks.
    Included attributes of Task: title, type, preferredTimeWindow, scheduledTimeWindow, priority, completed
    Excluded attributes of Task: durationMin, notes, description, frequency, completedAt, isType boolean flags
    """
    day_names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    def sort_key(task: pawpal_system.Task):
        window = task.scheduledTimeWindow
        if window is None:
            return (1, 99, time.max)
        return (0, window.dayOfWeek, window.startTime)

    ordered_tasks = sorted(tasks, key=sort_key)
    lines = []
    header = f"{'day':<3}  {'time':<11}  {'task':<20}  {'pri':<3}  {'completed':<9}"
    lines.append(header)
    lines.append("-" * len(header))

    for task in ordered_tasks:
        window = task.scheduledTimeWindow
        if window is None:
            day_label = "NA"
            time_label = "NA"
        else:
            day_label = day_names[window.dayOfWeek] if 0 <= window.dayOfWeek < 7 else "NA"
            time_label = f"{window.startTime.strftime('%H:%M')}-{window.endTime.strftime('%H:%M')}"

        status = "done" if task.completed else "pending"
        lines.append(
            f"{day_label:<3}  {time_label:<11}  {task.title:<20}  {task.priority:<3}  {status}"
        )

    return "\n".join(lines)

test_owner_0 = pawpal_system.Owner(name="Sady")
test_pet_0 = pawpal_system.Pet(name="Buddy", owner=test_owner_0, walkNeedLevel=3, feedingNeedLevel=2, medNeedLevel=1, groomingNeedLevel=4)
test_pet_1 = pawpal_system.Pet(name="Benji", owner=test_owner_0, walkNeedLevel=3, feedingNeedLevel=3, medNeedLevel=0, groomingNeedLevel=1)

tasks_list = [
    pawpal_system.Task(
    preferredTimeWindow=pawpal_system.TimeWindow(
        dayOfWeek=0, startTime=time(8, 0), endTime=time(8, 30)
        ), 
    title="Morning Walk", type="walk", durationMin=30, 
    priority=1, notes="Take Buddy for a walk in the park.", 
    frequency=(1, 1), isWalking=True
    ), 
    pawpal_system.Task(
    preferredTimeWindow=pawpal_system.TimeWindow(
        dayOfWeek=1, startTime=time(12, 0), 
        endTime=time(12, 30)
        ), 
    title="Lunch Feeding", type="feeding", 
    durationMin=30, priority=2, notes="Feed Benji his lunch.", 
    frequency=(1, 1), isFeeding=True
    ), 
    pawpal_system.Task(
    preferredTimeWindow=pawpal_system.TimeWindow(
    dayOfWeek=2, startTime=time(18, 0), endTime=time(18, 30)
    ), 
    title="Evening Grooming", type="grooming", 
    durationMin=30, priority=3, notes="Groom Buddy before bed.", 
    frequency=(1, 1), isGrooming=True
    ), 
    pawpal_system.Task(
    preferredTimeWindow=pawpal_system.TimeWindow(
        dayOfWeek=3, startTime=time(9, 0), endTime=time(9, 30)
        ), 
    title="Medical Checkup", type="medical", durationMin=30, 
    priority=1, notes="Take Buddy to the vet for checkup.", 
    frequency=(1, 2), isMedication=True
    ), 
    pawpal_system.Task(
    preferredTimeWindow=pawpal_system.TimeWindow(
        dayOfWeek=4, startTime=time(14, 0), 
        endTime=time(14, 30)
        ), 
    title="Afternoon Walk", type="walk", 
    durationMin=30, priority=2, notes="Walk Benji in the neighborhood.", 
    frequency=(1, 1), isWalking=True
    ), 
    pawpal_system.Task(
    preferredTimeWindow=pawpal_system.TimeWindow(
    dayOfWeek=5, startTime=time(10, 0), endTime=time(10, 30)
    ), 
    title="Feeding Time", type="feeding", 
    durationMin=30, priority=2, notes="Feed Buddy breakfast.", 
    frequency=(1, 1), isFeeding=True
    )
]

scheduler = pawpal_system.Scheduler()

for task in tasks_list:
    scheduler.addScheduledTask(task, task.preferredTimeWindow) 

scheduler.generateDailyPlan(owner=test_owner_0)

print(f"Daily Plan for {test_owner_0.name}")
print(format_schedule(tasks_list))