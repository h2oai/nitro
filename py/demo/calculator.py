# ===
# About: macOS calculator clone
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/demo
# Keywords: [basic, flask]
#
# Setup:
# FILE requirements.txt EOF
# flask
# simple-websocket
# h2o-nitro[web]>=0.16
# EOF
# RUN python -m pip install -r requirements.txt
# ENV FLASK_APP __file__
# START python -m flask --debug run
# ===

from h2o_nitro import View, box, col

nums = {str(i) for i in range(0, 10)}  # Numbers, 0-9
ops = {'÷': '/', '×': '*', '+': '+', '-': '-'}  # Operators


def main(view: View):
    x, op, y, result = None, None, None, None
    while True:
        if result is None:
            result = y if y else x if x else '0'
        else:
            x, op, y = None, None, None
        k = view(
            col(
                output(result),
                box(
                    cue('AC'), cue('±'), cue('%'), sym('÷'),
                    num('7'), num('8'), num('9'), sym('×'),
                    num('4'), num('5'), num('6'), sym('-'),
                    num('1'), num('2'), num('3'), sym('+'),
                    num('0') / 'grow', num('.'), sym('='),
                    mode='control',
                ) / 'flex flex-wrap gap-0.5',
            ) / 'w-[394px] p-0.5 rounded-lg overflow-hidden shadow-2xl bg-zinc-800 text-white text-4xl font-light',
        )
        r = None
        if k in nums:
            y = y + k if y else k if k != '0' else None
        elif k == '.':
            y = y if y and k in y else y + k if y else '0.'
        elif k == '±':
            y = calc(y, '*', '-1') if y else None
        elif k in ops:
            x, op, y, r = calc(x or result, op, y), ops[k], None, None
        elif k == '%':
            r = calc(calc(x or result, op, y), '*', '100')
        elif k == '=':
            r = calc(x, op, y)
        elif k == 'AC':
            r = '0'
        result = r if r else None


def calc(x, op, y):  # Returns 'x op y', or 'E' on error.
    expr = x + op + y if x and op and y else x if x else y if y else '0'
    try:
        return str(eval(expr))
    except:
        return 'E'


def key(text):  # Calculator key
    return box(
        box(text, mode='box'), mode='tap', value=text,
    ) / 'flex justify-center items-center w-24 h-20 select-none cursor-pointer transition-colors'


def num(text):  # Number key (light zinc)
    return key(text) / 'bg-zinc-600 hover:bg-zinc-500'


def sym(text):  # Operator key (orange)
    return key(text) / 'bg-orange-400 text-5xl hover:bg-orange-300'


def cue(text):  # Misc key (dark zinc)
    return key(text) / 'bg-zinc-700 hover:bg-zinc-600'


def output(text):  # Result output display
    return box(text, name='result') / 'w-full p-4 text-right text-5xl font-extralight truncate'


nitro = View(main, title='Calculator', caption='v1.0')

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
