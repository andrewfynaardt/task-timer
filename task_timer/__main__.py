"""
__main__.py
Andrew Fynaardt <andrew.fynaardt@student.cune.edu>
2024-28-01
 
This file is the main file for the task-timer
"""

import click
import pickle
import time

class Task:
    def __init__(self, name):
        self.name = name
        self.start_times = []
        self.end_times = []
        self.running = False

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

    def total_time(self):
        if self.running:
            total = 0
            for i in range(len(self.start_times-1)):
                total_time += self.end_times[i] - self.start_times[i]
            total_time += self.start_times[-1]
            return total_time
        else:
            total = 0
            for i in range(len(self.start_times)):
                total += self.end_times[i] - self.start_times[i]
            return total_time

    def __str__(self):
        return f"{self.name} has been worked on for {self.total_time()} seconds."

@click.group()
def main():
    pass

@main.command()
@click.argument("task_name")
@click.option("--start", is_flag=True, help="Start timing the task.")
@click.option("--end", is_flag=True, help="End timing the task.")
def time(task_name, start, end):
    print("time")
    pass

@main.command()
@click.option("--task_name", help="A specific task you want to view.")
@click.option("--all", is_flag=True, help="View all tasks.")
def view(task_name, all):
    print("view")
    pass

if __name__ == "__main__":
    main()