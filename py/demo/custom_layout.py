# ===
# About: Custom layouts
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/demo
# Keywords: [custom, layouts]
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

from h2o_nitro import View, box, option


def main(view: View):
    name = view(box('What is your name?', value='Boaty McBoatface'), ['Continue'])
    feel = view(box(f'How do you feel today, {name}?', value='intrigued'), ['Continue'])
    view(f'What a coincidence, {name}, I feel {feel}, too!')


layout = box(
    box(
        box(
            # nav
            box(
                box(
                    box(
                        box(
                            box(
                                # img
                                box() / 'block h-8 w-8',
                            ) / 'shrink-0',
                            box(
                                box(
                                    box('Overview') / 'bg-indigo-700 text-white rounded-md py-2 px-3 text-sm font-medium',
                                    box('Accounts') / 'text-white hover:bg-indigo-500/75 rounded-md py-2 px-3 text-sm font-medium',
                                    box('Transfer') / 'text-white hover:bg-indigo-500/75 rounded-md py-2 px-3 text-sm font-medium',
                                    box('Reports') / 'text-white hover:bg-indigo-500/75 rounded-md py-2 px-3 text-sm font-medium',
                                    box('Support') / 'text-white hover:bg-indigo-500/75 rounded-md py-2 px-3 text-sm font-medium',
                                ) / 'flex space-x-4',
                            ) / 'hidden lg:ml-10 lg:block',
                        ) / 'flex items-center px-2 lg:px-0',
                        box(
                            # button
                            box(
                                # span
                                box('Open main menu') / 'sr-only',
                                # svg
                                box("<svg class='block h-6 w-6' xmlns='http://www.w3.org/2000/svg' fill='none' viewbox='0 0 24 24' stroke-width='1.5' stroke='currentColor' aria-hidden='true' >\n    <path stroke-linecap='round' stroke-linejoin='round' d='M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5' />\n</svg>",
                                    mode='svg') / 'block h-6 w-6',
                                # svg
                                box("<svg class='hidden h-6 w-6' xmlns='http://www.w3.org/2000/svg' fill='none' viewbox='0 0 24 24' stroke-width='1.5' stroke='currentColor' aria-hidden='true' >\n    <path stroke-linecap='round' stroke-linejoin='round' d='M6 18L18 6M6 6l12 12' />\n</svg>",
                                    mode='svg') / 'hidden h-6 w-6',
                            ) / 'inline-flex items-center justify-center rounded-md bg-indigo-600 p-2 text-indigo-200 hover:bg-indigo-500/75 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-600',
                        ) / 'flex lg:hidden',
                        box(
                            box(
                                # button
                                box(
                                    # span
                                    box('View notifications') / 'sr-only',
                                    # svg
                                    box("<svg class='h-6 w-6' xmlns='http://www.w3.org/2000/svg' fill='none' viewbox='0 0 24 24' stroke-width='1.5' stroke='currentColor' aria-hidden='true' >\n    <path stroke-linecap='round' stroke-linejoin='round' d='M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0' />\n</svg>",
                                        mode='svg') / 'h-6 w-6',
                                ) / 'shrink-0 rounded-full bg-indigo-600 p-1 text-indigo-200 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-600',
                                box(
                                    box(
                                        # button
                                        box(
                                            # span
                                            box('Open user menu') / 'sr-only',
                                            box(
                                                box('B') / 'text-white text-lg font-light',
                                            ) / 'flex items-center justify-center h-8 w-8 rounded-full bg-pink-500',
                                        ) / 'flex rounded-full bg-indigo-600 text-sm text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-600',
                                    ),
                                    # Profile menu
                                    box(
                                        box('Profile') / 'block py-2 px-4 text-sm text-gray-700',
                                        box('Settings') / 'block py-2 px-4 text-sm text-gray-700',
                                        box('Sign out') / 'block py-2 px-4 text-sm text-gray-700',
                                    ) / 'absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black focus:outline-none',
                                ) / 'relative ml-3 shrink-0',
                            ) / 'flex items-center',
                        ) / 'hidden lg:ml-4 lg:block',
                    ) / 'relative flex h-16 items-center justify-between lg:border-b lg:border-indigo-400/25',
                ) / 'mx-auto max-w-7xl px-2 sm:px-4 lg:px-8',
                box(
                    box(
                        box('Overview') / 'bg-indigo-700 text-white block rounded-md py-2 px-3 text-base font-medium',
                        box('Accounts') / 'text-white hover:bg-indigo-500/75 block rounded-md py-2 px-3 text-base font-medium',
                        box('Transfer') / 'text-white hover:bg-indigo-500/75 block rounded-md py-2 px-3 text-base font-medium',
                        box('Reports') / 'text-white hover:bg-indigo-500/75 block rounded-md py-2 px-3 text-base font-medium',
                        box('Support') / 'text-white hover:bg-indigo-500/75 block rounded-md py-2 px-3 text-base font-medium',
                    ) / 'space-y-1 px-2 pt-2 pb-3',
                    box(
                        box(
                            box(
                                # img
                                box(
                                    box('B') / 'text-white text-xl font-light',
                                ) / 'flex items-center justify-center h-10 w-10 rounded-full bg-pink-500',
                            ) / 'shrink-0',
                            box(
                                box('Boaty McBoatface') / 'text-base font-medium text-white',
                                box('tom@example.com') / 'text-sm font-medium text-indigo-300',
                            ) / 'ml-3',
                            # button
                            box(
                                # span
                                box('View notifications') / 'sr-only',
                                # svg
                                box("<svg class='h-6 w-6' xmlns='http://www.w3.org/2000/svg' fill='none' viewbox='0 0 24 24' stroke-width='1.5' stroke='currentColor' aria-hidden='true' >\n    <path stroke-linecap='round' stroke-linejoin='round' d='M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0' />\n</svg>",
                                    mode='svg') / 'h-6 w-6',
                            ) / 'ml-auto shrink-0 rounded-full bg-indigo-600 p-1 text-indigo-200 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-600',
                        ) / 'flex items-center px-5',
                        box(
                            box('Profile') / 'block rounded-md py-2 px-3 text-base font-medium text-white hover:bg-indigo-500/75',
                            box('Settings') / 'block rounded-md py-2 px-3 text-base font-medium text-white hover:bg-indigo-500/75',
                            box('Sign out') / 'block rounded-md py-2 px-3 text-base font-medium text-white hover:bg-indigo-500/75',
                        ) / 'mt-3 space-y-1 px-2',
                    ) / 'border-t border-indigo-700 pt-4 pb-3',
                ) / 'lg:hidden',
            ) / 'border-b border-indigo-300/25 bg-indigo-600 lg:border-none',
            # header
            box(
                box(
                    # h1
                    box('Overview') / 'text-3xl font-bold tracking-tight text-white',
                ) / 'mx-auto max-w-7xl px-4 sm:px-6 lg:px-8',
            ) / 'py-10',
        ) / 'bg-indigo-600 pb-32',
        # main
        box(
            box(
                box(
                    # body container
                    box(mode='body') / 'h-96',
                ) / 'rounded-lg bg-white px-5 py-6 shadow sm:px-6',
            ) / 'mx-auto max-w-7xl px-4 pb-12 sm:px-6 lg:px-8',
        ) / '-mt-32',
    ) / 'min-h-full',
)

nitro = View(
    main,
    title='Hello Nitro!',
    caption='v1.0',
    layout=layout,
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
