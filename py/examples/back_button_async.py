# ===
# About: Back button and state handling demo
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/examples
# Keywords: [basic, tornado]
#
# Setup:
# FILE requirements.txt EOF
# tornado
# h2o-nitro[web]
# EOF
# RUN python -m pip install -r requirements.txt
# ECHO Access your app at http://localhost:5000
# START python back_button_async.py
# ===
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.queues
# ┌───────────────  Nitro app starts here ───────────────┐
from h2o_nitro import AsyncView as View, box, option
from h2o_nitro_web import web_directory


# For back-button support, the app's code needs to be structured a bit different:
# 1. Place each `view()` in a separate function.
# 2. To show the next view, call `view.jump(do_something)` instead of `do_something(view)`.
# 3. Pass these functions as routes when creating the root `View()`.

# Let's see how to do this step by step.

# This example demonstrate a 5-step wizard that collects personal details about the user's family members:
# 1. Introduction
# 2. User's details
# 3. Father's details
# 4. Mother's details
# 5. Summary

# First, we define a class to hold a person's details:

class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


# The app's state consists of details about three persons:

class State:
    def __init__(self):
        self.person = Person('Boaty', 'McBoatface')
        self.father = Person('Papa', 'McBoatface')
        self.mother = Person('Mama', 'McBoatface')


# The app starts by creating a new State instance, and showing the intro page.
# When the user clicks "Continue", control is passed on to the `ask_name()` function.

async def main(view: View):
    view.context['state'] = State()
    await view(
        '# Welcome to the wizard!',
        'Use the back button, Luke!'
    )
    await view.jump(ask_name)


# Ask for the user's details, then pass control to `ask_father_name()`.
# Note how we store the input values (first and last names) into the state instance:

async def ask_name(view: View):
    person: Person = view.context['state'].person
    person.first_name, person.last_name = await view(
        f"# Step 1",
        box('Your first name?', value=person.first_name),
        box('Your last name?', value=person.last_name)
    )
    await view.jump(ask_father_name)


# Same procedure here: ask for details, then pass control to the next function:

async def ask_father_name(view: View):
    father: Person = view.context['state'].father
    father.first_name, father.last_name = await view(
        f"# Step 2",
        box("Father's first name?", value=father.first_name),
        box("Father's last name?", value=father.last_name)
    )
    await view.jump(ask_mother_name)


# Same procedure here: ask for details, then pass control to the next function:

async def ask_mother_name(view: View):
    mother: Person = view.context['state'].mother
    mother.first_name, mother.last_name = await  view(
        f"# Step 3",
        box("Mother's first name?", value=mother.first_name),
        box("Mother's last name?", value=mother.last_name)
    )
    await view.jump(show_results)


# Finally, display the summmary:

async def show_results(view: View):
    state: State = view.context['state']
    await view(
        f"# Results",
        f"Your name: {state.person.first_name} {state.person.last_name}.",
        f"Your father's name: {state.father.first_name} {state.father.last_name}.",
        f"Your mother's name: {state.mother.first_name} {state.mother.last_name}.",
        halt=True,
    )


# Set up the Nitro view. Note how each function that can be "jumped to" is added to `routes=[...]`. Essentially,
# adding a functionn to the route list makes that function directly accessible by the front-end.

nitro = View(
    main,
    title='Hello Nitro!',
    caption='v1.0',
    routes=[
        option(ask_name),
        option(ask_father_name),
        option(ask_mother_name),
        option(show_results),
    ],
)


# └─────────────── Nitro app ends here ───────────────┘


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(f'{web_directory}/index.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = tornado.queues.Queue()

    async def open(self):
        async def send(message):  # Simple wrapper to always send binary messages.
            await self.write_message(message, binary=True)

        # Start listening to queued messages.
        tornado.ioloop.IOLoop.current().add_callback(nitro.serve, send, self.queue.get)

    async def on_message(self, message):
        await self.queue.put(message)  # Push to queue.

    def on_close(self):
        self.queue.put(None)  # Quit listening.


app = tornado.web.Application(
    [
        (r"/", RootHandler),
        (r"/nitro", WebSocketHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, dict(path=web_directory)),
    ],
    debug=True,
)

if __name__ == "__main__":
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
