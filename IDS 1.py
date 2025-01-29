import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Event class to store event details
class Event:
    def __init__(self, description, start_time, end_time):
        self.description = description
        self.start_time = datetime.strptime(start_time, "%H:%M")
        self.end_time = datetime.strptime(end_time, "%H:%M")

    def __str__(self):
        return f'"{self.description}", Start: "{self.start_time.strftime("%H:%M")}", End: "{self.end_time.strftime("%H:%M")}"'

# Function to check if two events conflict
def check_conflict(event1, event2):
    return not (event1.end_time <= event2.start_time or event2.end_time <= event1.start_time)

# Function to sort events by start time
def sort_events(events):
    return sorted(events, key=lambda x: x.start_time)

# Function to suggest an alternative time for a conflicting event
def suggest_alternative(events, event):
    # Check for conflicts and suggest a slot after the last event
    latest_end_time = max([e.end_time for e in events])
    new_start_time = latest_end_time + timedelta(minutes=30)  # add 30 minutes gap
    new_end_time = new_start_time + (event.end_time - event.start_time)
    return new_start_time.strftime("%H:%M"), new_end_time.strftime("%H:%M")

# Function to update the schedule and check for conflicts
def update_schedule(events):
    sorted_events = sort_events(events)
    conflict_list = []
    for i in range(len(sorted_events)):
        for j in range(i + 1, len(sorted_events)):
            if check_conflict(sorted_events[i], sorted_events[j]):
                conflict_list.append((sorted_events[i], sorted_events[j]))
    
    return sorted_events, conflict_list

# Function to add event and refresh the UI
def add_event():
    description = entry_description.get()
    start_time = entry_start_time.get()
    end_time = entry_end_time.get()
    
    if not description or not start_time or not end_time:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    event = Event(description, start_time, end_time)
    events.append(event)
    
    sorted_events, conflicts = update_schedule(events)
    
    # Clear existing display
    listbox_schedule.delete(0, tk.END)
    listbox_conflicts.delete(0, tk.END)
    
    # Display updated sorted schedule
    for e in sorted_events:
        listbox_schedule.insert(tk.END, str(e))
    
    # Display conflicts
    if conflicts:
        for conflict in conflicts:
            listbox_conflicts.insert(tk.END, f"Conflict: {conflict[0]} and {conflict[1]}")
            # Suggest alternative time for the second event
            alternative_start, alternative_end = suggest_alternative(events, conflict[1])
            listbox_conflicts.insert(tk.END, f"Suggested alternative for {conflict[1].description}: Start: {alternative_start}, End: {alternative_end}")
    else:
        listbox_conflicts.insert(tk.END, "No conflicts detected.")

# Create main window
root = tk.Tk()
root.title("Event Scheduler and Conflict Detector")

# Add input fields
tk.Label(root, text="Event Description:").pack()
entry_description = tk.Entry(root)
entry_description.pack()

tk.Label(root, text="Start Time (HH:MM):").pack()
entry_start_time = tk.Entry(root)
entry_start_time.pack()

tk.Label(root, text="End Time (HH:MM):").pack()
entry_end_time = tk.Entry(root)
entry_end_time.pack()

# Button to add event
button_add_event = tk.Button(root, text="Add Event", command=add_event)
button_add_event.pack()

# Create listboxes to display schedule and conflicts
tk.Label(root, text="Sorted Schedule:").pack()
listbox_schedule = tk.Listbox(root, width=50, height=10)
listbox_schedule.pack()

tk.Label(root, text="Conflicting Events:").pack()
listbox_conflicts = tk.Listbox(root, width=50, height=10)
listbox_conflicts.pack()

# List to store events
events = []

# Start the application
root.mainloop()
