# Copyright 2022 H2O.ai, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
from pathlib import Path
from h2o_nitro import web_directory, View, box, option, header, row, col, ContextSwitchError, lorem, Theme, \
    __version__ as version
import simple_websocket
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

# EXAMPLES

topics = dict(
    # TOPIC_MAP
)

table_of_contents = '''
# Welcome to Nitro!

Nitro is the simplest way to build interactive web apps using Python.
No front-end experience required.

This application is a collection of live, annotated examples for how to use
Nitro. It acts as a reference for how to do various things using Nitro, 
but can also be used as a guide to learn about many of the features Nitro provides.

You can always view an online version of these docs at [https://nitro.h2o.ai](https://nitro.h2o.ai).

TOC
'''


def view_output(view: View, docs, *args, **kwargs):
    if len(args) == 0:
        # example has no output
        return view(*docs)

    if 'popup' in kwargs:
        # show as-is
        return view(*args, **kwargs)

    # show with docs
    return view(*docs, col(*args, name='output', padding=20, border='$accent', **kwargs))


def main(view: View):
    topic = view(table_of_contents)
    topics[topic](view)


nitro = View(
    main,
    title='Nitro',
    caption=f'v{version}',
    menu=[
        option(main, 'Contents', icon='Documentation'),
        # MENU
    ],
    nav=[
        option(main, 'Contents', name='contents'),
    ],
)

app = Flask(__name__, static_folder=web_directory, static_url_path='')
UPLOAD_DIR = './file_uploads'
Path(UPLOAD_DIR).mkdir(exist_ok=True)


@app.route('/')
def home_page():
    return send_from_directory(web_directory, 'index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Missing files part', 400
    files = request.files.getlist('file')
    filenames = []
    for file in files:
        if file.filename == '':
            return 'Empty file', 400
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_DIR, filename))
            filenames.append(filename)
    return json.dumps(dict(files=filenames))


@app.route('/nitro', websocket=True)
def socket():
    ws = simple_websocket.Server(request.environ)
    try:
        nitro.serve(ws.send, ws.receive)
    except simple_websocket.ConnectionClosed:
        pass
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999)
