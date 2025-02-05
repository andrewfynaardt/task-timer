"""
__main__.py
Andrew Fynaardt <andrew.fynaardt@student.cune.edu>
2024-28-01
 
This file is the main file for the task-timer
"""

import click
import pickle
import time
from pathlib import Path

filepath = Path(__file__).parent / "tasks.pkl"

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
    
    def is_running(self):
        return self.running

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
@click.option("--task_name", help="A specific task you want to view.")
@click.option("--all", is_flag=True, help="View all tasks.")
@click.option("--running", is_flag=True, help="View only running tasks.")
def view(task_name, all):
    tasks = pickle.load(open(filepath, "rb"))
    if task_name:
        string = "\"" + task_name + "\" has been worked on for " + str(tasks[task_name].get_total_time()) + " seconds."
        click.echo(tasks[task_name])
    elif all:
        for task in tasks.values():
            string = "\"" + task.get_name() + "\" has been worked on for " + str(task.get_total_time()) + " seconds."
            click.echo(string)
    else:
        for task in tasks.values():
            if task.is_running():
                string = "\"" + task.get_name() + "\" has been worked on for " + str(task.get_total_time()) + " seconds."
                click.echo(string)
    return 

@main.command()
def export():
    pass

@main.command()
def init():
    pickle.dump({}, open(filepath, "wb")) 
    return   