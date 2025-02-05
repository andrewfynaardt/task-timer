"""
__main__.py
Andrew Fynaardt <andrew.fynaardt@student.cune.edu>
2024-28-01
 
This file is the main file for the task-timer
"""

import click
import pickle
import time
import csv
from pathlib import Path

filepath = Path(__file__).parent / "tasks.pkl"
test_filepath = Path(__file__).parent / "test_tasks.pkl"

class Task:
    def __init__(self, name):
        self.name = name
        self.start_times = []
        self.end_times = []
        self.running = False
        self.total_time = 0

    def start(self):
        if not self.running:
            self.running = True
            self.start_times.append(time.time())
            click.echo("Task timing started.")
        else:
            click.echo("This tasks timer has already started.")

    def end(self):
        if self.running: 
            self.running = False
            self.end_times.append(time.time())
            click.echo("Task timing ended.")
        else:
            click.echo("This task's timer is not running.")

    def get_total_time(self):
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
        return self.name
    
    def set_name(self, name):
        self.name = name
        return
    
    def is_running(self):
        return self.running
    
    def get_start_times(self):
        return self.start_times
    
    def set_start_times(self, start_times):
        self.start_times = start_times
        return
    
    def get_end_times(self):
        return self.end_times
    
    def set_end_times(self, end_times):
        self.end_times = end_times
        return

@click.group()
def main():
    pass

@main.command()
@click.argument("task_name")
@click.option("--start", is_flag=True, help="Start timing the task.")
@click.option("--end", is_flag=True, help="End timing the task.")
def timer(task_name, start, end):
    string = "Task name: " + task_name
    click.echo(string)
    tasks = pickle.load(open(filepath, "rb"))
    if task_name not in tasks:
        task = Task(task_name)
        tasks[task_name] = task
    else:
        task = tasks[task_name]

    if start and not end:
        task.start()
    elif end and not start:
        task.end()
    else:
        click.echo("Please specify either --start or --end.")

    pickle.dump(tasks, open(filepath, "wb"))
    return

@main.command()
@click.option("-t", "--task", help="A specific task you want to view.")
@click.option("-r", "--running", is_flag=True, help="View only running tasks.")
def view(task_name, running):
    tasks = pickle.load(open(filepath, "rb"))
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
@click.option("-o", "--output", default="timesheet", help="The file you want to export to.")
def export(output):
    tasks = pickle.load(open(filepath, "rb"))
    with open(Path(__file__).parent / f"{output}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Task Name", "Total Time", "Start Times", "End Times"])
        for task in tasks.values():
            writer.writerow([task.get_name(), task.get_total_time(), task.get_start_times(), task.get_end_times()])
    return

@main.command()
@click.option("-t","--test", is_flag=True, help="Initialize with test data.")
def init(test):
    if test:
        tasks = pickle.load(open(test_filepath, "rb"))
    else:
        tasks = {}
    pickle.dump(tasks, open(filepath, "wb")) 
    return   