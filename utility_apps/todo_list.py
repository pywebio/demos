#Original app: https://github.com/ngshiheng/pywebio-todolist
#Forked and revised to save to-do data to a file

from pywebio import *
from pywebio.output import *
from pywebio.input import *

from functools import partial
import pickle

todo_data_file = '__todo_list_tasks.ob'

def complete_task(choice: str, task: str, tasks):
    global todo_data_file
    if choice == 'Complete':
        tasks.remove(task)
        with open(todo_data_file, 'wb') as fp:
            pickle.dump(tasks, fp)
    clear('tasks')
    if tasks: display_task(tasks)
        
def add_task(tasks):
    global todo_data_file
    task = input(
                type=TEXT,
                required=True,
                label='🏃 What are you going to do today?',
                placeholder='Add a task...',
                help_text='Try: "Write an article"',
            )
    tasks.append(task)
    with open(todo_data_file, 'wb') as fp:
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
    
def main():
    'A todo list app built on pyweb.io'
    global todo_data_file
    
    #Read file to load previous todo items. It handles edge cases like missing file and empty file.
    try:
        with open (todo_data_file, 'rb') as fp:
            try: 
                tasks = pickle.load(fp)
            except EOFError:
                tasks = []
    except IOError:
        with open(todo_data_file, 'w') as fp:
            tasks = []


    put_html(r"""<h1 align="center"><strong>📝 To-Do List</strong></h1>""")
    with use_scope('tasks'):
        if tasks: display_task(tasks)
        while True:
            add_task(tasks)


if __name__ == '__main__':
    start_server(main, debug=True, port=9999)