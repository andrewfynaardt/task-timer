"""
__main__.py
Andrew Fynaardt <andrew.fynaardt@student.cune.edu>
2024-09-02
 
This file is the main file for the task-timer. It contains all the commands for the task-timer.
The timesheet data is stored in a pickle file and unpickled when a command is run.

Commands:
start <task_name> - Create and start timing a task with the given name. If the task already exists, resume it.
stop <task_name> - Stop timing a task with the given name. If the task does not exist or is not running, print an error message.
undo <task_name> - Undo the last start or end time of a task with the given name. If the task does not exist, print an error message.
rename <task_name> <new_name> - Rename a task with the given name to the new name. If the task does not exist, print an error message.
delete <task_name> - Delete a task with the given name. If the task does not exist, print an error message.
view - View all tasks or a specific task.
export - Export all tasks to a CSV file.

Copilot was used to help document the code. It was also used to generate some repetitive code like the try/except blocks.
"""

import click
import pickle
import time
import csv
from pathlib import Path

filepath = Path(__file__).parent / "tasks.pkl"
test_filepath = Path(__file__).parent / "test_tasks.pkl"

class Task:
    """A class to represent a task. Has attributes for its name, arrays of start times and end times, and a boolean for if it is running or not.
       Has methods for logging start and end times, getting the total time the task has been worked, and getting and setting the name and times.
    """
    def __init__(self, name):
        """Create and name a new task with empty start and end times."""
        self.name = name
        self.start_times = []
        self.end_times = []
        self.running = False
        self.total_time = 0

    def start(self):
        """Log the start time of the task set it to running."""
        if not self.running:
            self.running = True
            self.start_times.append(time.time())

    def end(self):
        """Log the end time of the task and set it to not running."""
        if self.running: 
            self.running = False
            self.end_times.append(time.time())

    def get_total_time(self):
        """Sum the total time the task has been worked on."""
        self.total_time = 0
        if self.running:
            for i in range(len(self.start_times-1)):
                self.total_time += self.end_times[i] - self.start_times[i]
            self.total_time += self.start_times[-1]
        else:
            for i in range(len(self.start_times)):
                self.total_time += self.end_times[i] - self.start_times[i]
        return self.total_time

    def get_name(self):
        """Return the name of the task."""
        return self.name
    
    def set_name(self, name):
        """Set the name of the task."""
        self.name = name
        return
    
    def is_running(self):
        """Return if the task is running or not."""
        return self.running
    
    def get_start_times(self):
        """Return the start times of the task."""
        return self.start_times
    
    def set_start_times(self, start_times):
        """Set the start times of the task."""
        self.start_times = start_times
        return
    
    def get_end_times(self):
        """Return the end times of the task."""
        return self.end_times
    
    def set_end_times(self, end_times):
        """Set the end times of the task."""
        self.end_times = end_times
        return

@click.group()
def main():
    pass

@main.command()
@click.argument("task_name")
def start(task_name):
    """Create and start timing a task with the given name. If the task already exists, resume it."""
    try:
        tasks = pickle.load(open(filepath, "rb"))
    except:
        init()
        tasks = pickle.load(open(filepath, "rb"))

    if task_name not in tasks:
        task = Task(task_name)
        tasks[task_name] = task
        click.echo(f"Created \"{task_name}\".")
    else:
        task = tasks[task_name]
        click.echo(f"Resuming \"{task_name}\".")

    task.start()

    pickle.dump(tasks, open(filepath, "wb"))
    return

@main.command()
@click.argument("task_name")
def stop(task_name):
    """Stop timing a task with the given name. If the task does not exist or is not running, print an error message."""
    tasks = pickle.load(open(filepath, "rb"))
    if task_name not in tasks:
        click.echo(f"\"{task_name}\" does not exist.")
        return
    task = tasks[task_name]
    if not task.is_running():
        click.echo(f"\"{task_name}\" is not running.")
        return
    task.end()
    click.echo(f"Stopped timing \"{task_name}\".")

    pickle.dump(tasks, open(filepath, "wb"))
    return

@main.command()
@click.argument("task_name")
def undo(task_name):
    """Undo the last start or end time of a task with the given name. If the task does not exist, print an error message."""
    try:
        tasks = pickle.load(open(filepath, "rb"))
    except:
        click.echo("No timesheet found.")
        return
    if task_name not in tasks:
        click.echo(f"\"{task_name}\" does not exist.")
        return
    task = tasks[task_name]
    task.end()
    task.set_start_times(task.get_start_times()[:-1])
    task.set_end_times(task.get_end_times()[:-1])

    pickle.dump(tasks, open(filepath, "wb"))
    return

@main.command()
@click.argument("task_name")
@click.argument("new_name")
def rename(task_name, new_name):
    """Rename a task with the given name to the new name. If the task does not exist, print an error message."""
    try:
        tasks = pickle.load(open(filepath, "rb"))
    except:
        click.echo("No timesheet found.")
        return
    if task_name not in tasks:
        click.echo(f"\"{task_name}\" does not exist.")
        return
    task = tasks[task_name]
    task.set_name(new_name)
    tasks[new_name] = task
    del tasks[task_name]
    click.echo(f"Renamed \"{task_name}\" to \"{new_name}\".")

    pickle.dump(tasks, open(filepath, "wb"))
    return

@main.command()
@click.argument("task_name")
@click.option("-a", "--all_", is_flag=True, help="Delete all tasks.")
def delete(task_name, all_):
    """Delete a task with the given name. If the task does not exist, print an error message."""
    try:
        tasks = pickle.load(open(filepath, "rb"))
    except:
        click.echo("No timesheet found.")
        return
    if all_:
        init()
        click.echo("Deleted all tasks.")
        return
    if task_name not in tasks:
        click.echo(f"\"{task_name}\" does not exist.")
        return
    del tasks[task_name]
    click.echo(f"Deleted \"{task_name}\".")

    pickle.dump(tasks, open(filepath, "wb"))
    return

@main.command()
@click.option("-t", "--task_name", help="A specific task you want to view.")
@click.option("-r", "--running", is_flag=True, help="View only running tasks.")
def view(task_name, running):
    """View all tasks or a specific task."""
    try:
        tasks = pickle.load(open(filepath, "rb"))
    except:
        click.echo("No timesheet found.")
        return
    if task_name:
        string = "\"" + task_name + "\" has been worked on for " + str(tasks[task_name].get_total_time()) + " seconds."
        click.echo(tasks[task_name])
    elif running:
        for task in tasks.values():
            if task.is_running():
                string = "\"" + task.get_name() + "\" has been worked on for " + str(task.get_total_time()) + " seconds."
                click.echo(string)
    else:
        for task in tasks.values():
            string = "\"" + task.get_name() + "\" has been worked on for " + str(task.get_total_time()) + " seconds."
            click.echo(string)
    return 

@main.command()
@click.option("-o", "--out", default="timesheet", help="The file you want to export to.")
def export(out):
    """Export all tasks to a CSV file."""
    try:
        tasks = pickle.load(open(filepath, "rb"))
    except:
        click.echo("No timesheet found.")
        return
    with open(Path(__file__).parent / f"{out}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Task Name", "Total Time", "Start Times", "End Times"])
        for task in tasks.values():
            task.end()
            writer.writerow([task.get_name(), task.get_total_time(), task.get_start_times(), task.get_end_times()])
    return

@main.command()
@click.option("-t", "--test", is_flag=True, help="Initialize with test data.")
def init(test):
    """Initialize the task-timer with a new timesheet. Use the test timesheet if --test is specified."""
    if test:
        tasks = pickle.load(open(test_filepath, "rb"))
    else:
        tasks = {}
    pickle.dump(tasks, open(filepath, "wb")) 
    return