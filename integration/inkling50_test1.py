import flet as ft
import asyncio
import time

# Global variables to manage timers and state
inactivity_timeout = 8  # seconds for idle timeout
flet_timer_duration = 5  # seconds for the document deletion timer after inactivity
last_input_time = 0  # Last time the user typed
flet_timer_running = False  # Whether the flet timer is running
document_deleted = False  # Whether the document has been deleted

# Timer callbacks
async def countdown_flet_timer(page: ft.Page):
    global flet_timer_duration
    while flet_timer_duration > 0:
        flet_timer_duration -= 1
        flet_timer_label.value = f"Flet Timer: {flet_timer_duration}s"
        page.update()
        await asyncio.sleep(1)

    # Once the timer runs out, delete the document
    global document_deleted
    document_deleted = True
    page.add(ft.Text("Document deleted due to inactivity!"))
    page.update()

async def reset_flet_timer(page: ft.Page):
    global flet_timer_running, flet_timer_duration
    flet_timer_running = False
    flet_timer_duration = 5  # Reset flet timer duration
    flet_timer_label.value = f"Flet Timer: {flet_timer_duration}s"
    page.update()

# Function to handle typing input and inactivity timer
def on_input_change(e):
    global last_input_time, flet_timer_running, document_deleted

    # Reset the inactivity timer on input
    last_input_time = time.time()

    # If the flet timer is running, reset it
    if flet_timer_running:
        reset_flet_timer(page)
        print("Flet timer reset due to user input.")

    if document_deleted:
        # If the document has been deleted, prevent further input or actions
        user_input.disabled = True
        page.update()

    # Reset the idle timer and update the UI
    idle_timer_label.value = f"Idle Timer: 8s (reset on input)"
    page.update()

# Function to handle the idle timer (checking if the user has been idle)
async def handle_inactivity(page: ft.Page):
    global last_input_time, inactivity_timeout, flet_timer_running

    while True:
        current_time = time.time()

        # If the user has been inactive for more than 8 seconds, start the flet timer
        if current_time - last_input_time > inactivity_timeout and not flet_timer_running:
            flet_timer_running = True
            page.add(ft.Text("Flet Timer started due to inactivity!"))
            page.update()
            # Start the flet timer countdown
            await countdown_flet_timer(page)

        await asyncio.sleep(1)  # Check inactivity every second

# UI elements
def main(page: ft.Page):
    global last_input_time

    # Label for showing timers
    global flet_timer_label, idle_timer_label
    flet_timer_label = ft.Text("Flet Timer: 5s")
    idle_timer_label = ft.Text("Idle Timer: 8s (reset on input)")

    # Textfield for user input
    user_input = ft.TextField(
        label="Enter text",
        on_change=on_input_change,
    )

    # Add elements to the page
    page.add(flet_timer_label, idle_timer_label, user_input)

    # Run the inactivity check every second using asyncio
    asyncio.create_task(handle_inactivity(page))

# Run the app
ft.app(target=main)
