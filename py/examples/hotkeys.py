# ===
# About: Basic Hello World app using Flask
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/demo
# Keywords: [basic, flask]
#
# Setup:
# FILE requirements.txt EOF
# flask
# simple-websocket
# h2o-nitro[web]
# EOF
# RUN python -m pip install -r requirements.txt
# ENV FLASK_APP __file__
# START python -m flask --debug run
# ===

from h2o_nitro import View, option


# Hotkey handler for Cut (ctrl+x)
def cut(view: View):
    view('# You tried to cut!')


# Hotkey handler for Copy (ctrl+c)
def copy(view: View):
    view('# You tried to copy!')


# Hotkey handler for Paste (ctrl+v)
def paste(view: View):
    view('# You tried to paste!')


def main(view: View):
    view('''
    # Copypasta!
    
    This is a simple demo of how to use hotkeys.
    
    - Press `ctrl+x` to cut.
    - Press `ctrl+c` to copy.
    - Press `ctrl+v` to paste.
    ''')


nitro = View(
    main,
    title='Hotkeys Demo',
    caption='v1.0',
    # Bind hotkey combinations to functions.
    hotkeys=[
        option(cut, 'ctrl+x'),
        option(copy, 'ctrl+c'),
        option(paste, 'ctrl+v'),
    ],
)

# ┌─────────────── Flask Boilerplate ───────────────┐

import simple_websocket
from flask import Flask, request, send_from_directory
from h2o_nitro_web import web_directory

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
