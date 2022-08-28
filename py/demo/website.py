# ===
# About: A super simple website
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/demo
# Keywords: [flask, wizard]
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

from h2o_nitro import View, box, option, link, row, col, lorem


# Creates a sample page
def make_dummy_page(title):
    return f'''
    # {title}

    {lorem(3)}

    ## {lorem(1)}

    {lorem(5)}

    {lorem(8)}

    ## {lorem(1)}

    {lorem(5)}
    '''


# Initializes some dummy pages and blog posts for the website.
def init_dummy_content():
    # Make some pages
    pages = {k: make_dummy_page(k) for k in ['Home', 'Gallery', 'About', 'Contact']}

    # Make some blog posts
    posts = dict()  # Dictionary of posts
    post_links = []  # List of links to posts
    for id in range(1, 16):
        post_id = str(id)
        post_title = lorem(1)
        posts[post_id] = make_dummy_page(post_title)
        # The link() function creates a hyperlink that points to the post(view, id) function.
        post_links.append(f'### [{post_title}]({link(post, id=post_id)})')

    post_listing = '\n\n'.join(post_links)

    # Add post listing to a 'Blog' page
    pages['Blog'] = f"# Blog\n\n{post_listing}"

    return pages, posts


def home(view: View):
    view(dummy_pages['Home'])


def gallery(view: View):
    view(dummy_pages['Gallery'])


def blog(view: View):
    view(dummy_pages['Blog'])


def post(view: View, id: str):
    view(dummy_posts[id])


def about(view: View):
    view(dummy_pages['About'])


def contact(view: View):
    view(dummy_pages['Contact'])


# Initialize some dummy content
dummy_pages, dummy_posts = init_dummy_content()

nitro = View(
    home,
    # The app's title and caption, displayed at the top.
    title='Website',
    caption='Demo',
    # The main menu, displayed at the top left.
    menu=[
        option(home, 'Home', icon='Home', hotkey='Alt+H'),
        option(gallery, 'Gallery', icon='PhotoCollection', hotkey='Alt+G'),
        option(blog, 'Blog', icon='Blog', hotkey='Alt+B'),
        option(about, 'About', icon='Info', hotkey='Alt+A'),
        option(contact, 'Contact', icon='Mail', hotkey='Alt+C'),
        option('https://www.google.com', 'Search', icon='Search', hotkey='Alt+S'),
    ],
    # The navigation bar, displayed at the top right.
    nav=[
        option(home, 'Home'),
        option(gallery, 'Gallery'),
        option(blog, 'Blog'),
        option(about, 'About'),
        option(contact, 'Contact'),
    ],
    # Additional routes to expose
    routes=[
        option(post),
    ]
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
