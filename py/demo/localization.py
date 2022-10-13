# ===
# About: A simple multi-lingual application
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/demo
# Keywords: [flask, localization]
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

# This Nitro app automatically detects the end-user's locale settings and uses
# the corresponding translations dictionary to display a localized user interface.
#
# You can make the app use a different language by changing the "Location" dropdown in Chrome Dev Tool's "Sensors" tab.
# To display the "Sensors" tab, use the launcher (Ctrl+Shift+P) and type in "Show Sensors".

from h2o_nitro import View, box


def main(view: View):
    name = view(box('@ask_name', value='Boaty McBoatface'))
    feel = view(box('@ask_feeling', value='intrigued', data=dict(name=name)))
    view(box('@say_feeling', data=dict(name=name, feel=feel)))


# Language dictionary for en-US (English / US)
lang_english = dict(
    ask_name='What is your name?',
    ask_feeling='=How do you feel today, {name}?',
    say_feeling='=What a coincidence, {name}, I feel {feel}, too!',
)

# Language dictionary for hi-IN (Hindi / India)
lang_hindi = dict(
    ask_name='तुम्हारा नाम क्या हे?',
    ask_feeling='=तुम्हें आज कैसा लग रहा हा, {name}?',
    say_feeling='=क्या संयोग है, {name}, मुझे भी {feel} महसूस हो रहा है!',
)

nitro = View(
    main,
    title='Hello Nitro!',
    caption='v1.0',
    resources={
        'en-US': lang_english,
        'hi-IN': lang_hindi,
        # Add more language dictionaries here.
    },
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
