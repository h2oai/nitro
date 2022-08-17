# ===
# About: To Do List
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/examples
# Keywords: [todo, flask]
#
# Setup:
# FILE requirements.txt EOF
# flask
# simple-websocket
# h2o-nitro[web]
# EOF
# RUN python -m pip install -r requirements.txt
# ENV FLASK_APP todo.py
# ENV FLASK_ENV development
# START python -m flask run
# ===
import simple_websocket
from flask import Flask, request, send_from_directory

# ┌───────────────  Nitro app starts here ───────────────┐

from typing import Dict
from h2o_nitro import View, box, row, option
from h2o_nitro_web import web_directory

_task_key = 0


class Task:
    def __init__(self, text):
        global _task_key
        _task_key += 1
        self.key = str(_task_key)
        self.text = text
        self.done = False


tasks: Dict[str, Task] = {}


def task_to_option(task: Task):
    return option(task.key, task.text, selected=task.done)


def main(view: View):
    while True:
        text, add, not_done, done = view(
            row(box('Add a task', value='', lines=4) / 'grow', ['Add']),
            box('To do', mode='live check', options=[
                task_to_option(task) for task in tasks.values() if not task.done
            ]),
            box('Done', mode='live check', options=[
                task_to_option(task) for task in tasks.values() if task.done
            ]),
        )
        if add:
            task = Task(text)
            tasks[task.key] = task
        else:
            checked = set(not_done + done)
            for task in tasks.values():
                task.done = task.key in checked


nitro = View(main, title='To Do List', caption='Made with Nitro')

# └─────────────── Nitro app ends here ───────────────┘

app = Flask(__name__, static_folder=web_directory, static_url_path='')


@app.route('/')
def home_page():
    return send_from_directory(web_directory, 'index.html')


@app.route('/nitro', websocket=True)
def socket():
    ws = simple_websocket.Server(request.environ)
    try:
        nitro.serve(ws.send, ws.receive)
    except simple_websocket.ConnectionClosed:
        pass
    return ''


if __name__ == '__main__':
    app.run()
