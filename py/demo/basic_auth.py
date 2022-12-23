# ===
# About: Basic Auth using Flask
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/demo
# Keywords: [basic, auth, flask]
#
# Setup:
# FILE requirements.txt EOF
# flask
# Flask-HTTPAuth
# simple-websocket
# h2o-nitro[web]
# EOF
# RUN python -m pip install -r requirements.txt
# ENV FLASK_APP __file__
# START python -m flask --debug run
# ===

from h2o_nitro import View, box


def main(view: View):
    # Get the user from the context
    user = view['user']
    first_name = user.first_name

    view(f'Welcome, {first_name}!')
    feel = view(box(f'How do you feel today, {first_name}?', value='intrigued'))
    view(f'What a coincidence, {first_name}, I feel {feel}, too!')


nitro = View(main, title='Hello Nitro!', caption='v1.0')

# ┌─────────────── Flask Boilerplate ───────────────┐

import simple_websocket
from flask import Flask, request, send_from_directory
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from h2o_nitro_web import web_directory

app = Flask(__name__, static_folder=web_directory, static_url_path='')
auth = HTTPBasicAuth()


# The User class represents an application user.
class User:
    def __init__(self, username, password, first_name):
        self.name = username
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name


# A list of valid users
# For demonstration purposes only - don't do this in production!
# Typically, you'd look up users from the application's database or some SSO system.
users = {user.name: user for user in [
    # username, password, first name
    User('alice', 'wonderland', 'Alice'),
    User('bob', 'burger', 'Bob'),
]}


@auth.verify_password
def verify_password(username, password):
    user = users.get(username)
    if user and check_password_hash(user.password_hash, password):
        return user


@app.route('/')
@auth.login_required
def home_page():
    return send_from_directory(web_directory, 'index.html')


@app.route('/nitro', websocket=True)
@auth.login_required
def socket():
    ws = simple_websocket.Server(request.environ)
    try:
        # Pass the user to serve() using a context dictionary
        #   to make it accessible from all our view functions.
        nitro.serve(ws.send, ws.receive, context=dict(
            user=auth.current_user(),
        ))
    except simple_websocket.ConnectionClosed:
        pass
    return ''


if __name__ == '__main__':
    app.run()
