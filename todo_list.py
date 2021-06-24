#Original app: https://github.com/ngshiheng/pywebio-todolist
#Forked and revised to save to-do data to a file

from pywebio import *
from pywebio.output import *
from pywebio.input import *

from functools import partial
import pickle

def complete_task(choice: str, task: str, tasks):
    if choice == 'Complete':
        tasks.remove(task)
        with open('__todo_list_tasks.ob', 'wb') as fp:
            pickle.dump(tasks, fp)
    clear('tasks')
    if tasks: display_task(tasks)
        
def add_task(tasks):
    task = input(
                type=TEXT,
                required=True,
                label='🏃 What are you going to do today?',
                placeholder='Add a task...',
                help_text='Try: "Write an article"',
            )
    tasks.append(task)
    with open('__todo_list_tasks.ob', 'wb') as fp:
        pickle.dump(tasks, fp)
    clear('tasks')
    display_task(tasks)

def display_task(tasks):
    put_table(
        tdata=[
            [
                task,
                put_buttons(['Complete'], onclick=partial(complete_task, task=task, tasks=tasks))
            ] for task in tasks
        ],
        header=[
            '🤩 Your Awesome Tasks',
            '✅ Have you completed your task?',
        ],
        scope='tasks',
    )
    
@platform.utils.seo('To-Do List', 'A to-do list made using PyWebIO.')
def main():
    'A todo list app built on pyweb.io'
    tasks = []
    with open ('__todo_list_tasks.ob', 'rb') as fp:
        tasks = pickle.load(fp)

    put_html(r"""<h1 align="center"><strong>📝 To-Do List</strong></h1>""")
    with use_scope('tasks'):
        if tasks: display_task(tasks)
        while True:
            add_task(tasks)
