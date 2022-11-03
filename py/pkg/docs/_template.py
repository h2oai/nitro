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

# ===
# About: H2O Nitro Live Documentation
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://nitro.h2o.ai/docs.py
#
# Setup:
# FILE requirements.txt EOF
# flask
# simple-websocket
# h2o-nitro[web]
# EOF
# RUN python -m pip install -r requirements.txt
# ENV FLASK_APP docs.py
# ENV FLASK_RUN_PORT 4999
# START python -m flask --debug run
# ===

import json
import os
import datetime
import random
from pathlib import Path
from h2o_nitro import View, box, option, header, row, col, ContextSwitchError, lorem, Theme, \
    __version__ as version
import h2o_nitro.fake as fake
from h2o_nitro_web import web_directory
import simple_websocket
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

next_arrow = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="currentColor">
  <path d="m24 40-2.1-2.15L34.25 25.5H8v-3h26.25L21.9 10.15 24 8l16 16Z"/>
</svg>
'''
prev_arrow = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="currentColor">
  <path d="M24 40 8 24 24 8l2.1 2.1-12.4 12.4H40v3H13.7l12.4 12.4Z"/>
</svg>
'''

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
        option('https://nitro.h2o.ai', 'nitro.h2o.ai', icon='Globe')
    ],
    nav=[
        option(main, 'Contents'),
    ],
    routes=[
        # ROUTES
    ],
    help=dict(
        index='''
        ## Topics 
        
        - [Topic 1](#topic1)
        - [Topic 2](#topic2)
        - [Topic 3](#topic3)
        - [FAQ](#faq)
        
        ''',
        topic1='''
        ## Topic 1
        
        Describe the topic here.
        
        [Topics](#index)
        ''',
        topic2='''
        ## Topic 2
        
        Describe the topic here.
        
        [Topics](#index)
        ''',
        topic3='''
        ## Topic 3
        
        Describe the topic here.
        
        [Topics](#index)
        ''',
        faq='''
        ## FAQ
        
        ###  What's the answer to life, the universe, and everything?
        
        42.
        
        ### How many dishes does the Allen Telescope Array have?
        
        Also 42.
        
        [Topics](#index)
        ''',
    ),
    resources=dict(
        hi=dict(
            flavor_caption='एक स्वाद चुनें',
            flavor_hint='हमारे सभी स्वाद 100% प्राकृतिक हैं। कोई अतिरिक्त चीनी या रंग नहीं।',
            flavor_help='### स्वादिष्ट स्वाद\nहमारे सभी स्वाद 100% प्राकृतिक हैं। कोई अतिरिक्त चीनी या रंग नहीं।'
        )
    ),
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
