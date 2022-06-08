# ===
# About: Basic Hello World app using Flask
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/examples
# Keywords: [basic, flask]
#
# Setup:
# FILE requirements.txt EOF
# flask
# simple-websocket
# h2o-nitro
# EOF
# RUN python -m pip install -r requirements.txt
# ENV FLASK_APP hello.py
# ENV FLASK_ENV development
# START python -m flask run
# ===
import simple_websocket
from flask import Flask, request, send_from_directory

# ┌───────────────  Nitro app starts here ───────────────┐

from h2o_nitro import View, box, web_directory


def main(view: View):
    name = view(box('What is your name?', value='Boaty McBoatface'))
    feel = view(box(f'How do you feel today, {name}?', value='intrigued'))
    view(f'What a coincidence, {name}, I feel {feel}, too!')


nitro = View(main, title='Hello Nitro!', caption='v1.0')

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
