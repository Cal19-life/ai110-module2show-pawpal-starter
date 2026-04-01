import streamlit as st
from pawpal_system import Task, Pet, Owner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan") #TODO: change value="" to ensure text_input picks up user inputted name
pet_name = st.text_input("Pet name", value="Mochi") #TODO: change value="" to ensure text_input picks up user inputted name
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state and owner_name and owner_name.strip():
    st.session_state.owner = Owner(name=owner_name.strip())

if st.button("Add pet"):
    owner = st.session_state.get("owner")
    if owner is None:
        st.warning("Enter owner name first to create an owner, then add a pet.")
    elif owner.getPetByName(pet_name) is None:
        new_pet = Pet(
            name=pet_name,
            owner=owner,
            walkNeedLevel=1,
            feedingNeedLevel=1,
            medNeedLevel=1,
            groomingNeedLevel=1,
        )
        owner.addPet(new_pet)
        st.success(f"Added pet: {pet_name} ({species})")
    else:
        st.info(f"Pet '{pet_name}' already exists for owner '{owner.name}'.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

task_type_options = ["walk", "feeding", "medication", "enrichment", "grooming"]
priority_map = {"low": 1, "medium": 2, "high": 3}

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

task_type = st.selectbox("Task type", task_type_options, index=0)

if st.button("Add task"):
    if st.session_state.owner is None:
        st.warning("Add an owner/pet first before adding tasks.")
    else:
        pet = st.session_state.owner.getPetByName(pet_name)
        if pet is None:
            st.warning("Add the pet first before adding tasks.")
        else:
            task = Task(
                title=task_title,
                type=task_type,
                durationMin=int(duration),
                priority=priority_map[priority],
                notes="",
            )

            if task_type == "walk":
                task.isWalking = True
            elif task_type == "feeding":
                task.isFeeding = True
            elif task_type == "medication":
                task.isMedication = True
            elif task_type == "enrichment":
                task.isEnrichment = True
            elif task_type == "grooming":
                task.isGrooming = True

            pet.addTask(task)
            st.success(f"Added task '{task_title}' to {pet.name}.")

current_tasks = []
if st.session_state.owner is not None:
    selected_pet = st.session_state.owner.getPetByName(pet_name)
    if selected_pet is not None:
        current_tasks = [
            {
                "title": task.title,
                "type": task.type,
                "duration_minutes": task.durationMin,
                "priority": task.priority,
                "completed": task.completed,
            }
            for task in selected_pet.getTasks(includeCompleted=True)
        ]

if current_tasks:
    st.write(f"Current tasks for {pet_name}:")
    st.table(current_tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule") 
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    ) #TODO: implement UI-logic for connecting backend algo of generating schedule to button click
