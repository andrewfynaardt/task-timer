"""
__main__.py
Andrew Fynaardt <andrew.fynaardt@student.cune.edu>
2024-28-01
 
This file is the main file for the task-timer
"""

import click

@click.command()

@click.command()
@click.argument("task_name", task_name="Task name", help="The task you want to time.")
@click.option("--start", task_name="Your name", help="Start timing the task.")
@click.option("--end", task_name="Your name", help="End timing the task.")
def time(task_name):
    pass

@click.command()
@click.option("--task_name", task_name="Task name", help="A specific task you want to view.")
def view(task_name):
    pass



def main():
    """This is my main cli."""

    click.echo("Hello from task-timer!")

if __name__ == "__main__":
    main()