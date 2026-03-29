# PawPal+ Project Reflection

## 1. System Design

- Basic User Features (what user should be able to do):
    - Owner: Create owner, edit owner info
    - Pet: Create a Pet, edit pet info
    - Task: Create a task, edit task info(event-time, duration, priority)
    - Schedules: Create schedule, add tasks to schedule, reorganize tasks, edit task info, add constraints, edit constraints (time availabilities)
    - View the plan and rationale behind plan

- Basic Classes + Methods(actions to takes) + Attributes(info it needs):
    - Owner: methods -> create owner, edit owner info; attributes -> owner-info: name, time availabilities, misc owner preferences
    - Pet: attributes -> number of walks needed per day or week, number of times feeding is required per day or week, medications-- number of times per day/week/month, grooming-- number of times per week/month
    - Task: Create a general task, create tasks of following types-- walking, feeding, meds, enrichment, grooming
    - Scheduler: Create schedule, reorganize tasks in schedule, access and edit tasks within schedule

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design includes the Owner, Pet, Scheduler, and Task suggested classes, as well as one for a time-range and day (TimeWindow), the schedule for the day(DailyPlan), and subclasses of Task related to the common task-types(walking,feeding, medication, enrichment,grooming).

The Owner and Pet classes store information that the Scheduler can use to create a recommended schedule, such as Owner availabilities, Pet need level for a specific task. They also associate Pet(s) with an Owner. 

The Scheduler can generate a new plan, reschedule a Task, add/remove tasks, and explain the plan.

The TimeWindow class is for storing multiple attributes together-- day of the week and start/end times-- that are helpful to associate with a Task, and an Owner regarding their availabilities.

The DailyPlan class is simply for keeping the attributes of the final produced schedule organized together.

Finally, the Task class keeps the following attributes together-- task name, type, duration in minutes, priority, and additional notes. The Task can be created and edited.
 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.


    - Change: Replaced Task subclasses (WalkingTask, FeedingTask, etc.) with boolean task-type flags on Task. Rationale: For current scope, no additional characteristics(attributes, behavior) for each task-type. Flags act like label for task, in case Pet has to complete a specific task-type X number of times per day.
    
    - Change: Added Pet back-reference to Owner. Rationale: This makes relationship navigation two-way and allows Pet-object to use operations involving an Owner.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
