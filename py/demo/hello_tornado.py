# ===
# About: Basic Hello World app using Tornado
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/demo
# Keywords: [basic, tornado]
#
# Setup:
# FILE requirements.txt EOF
# tornado
# h2o-nitro[web]
# EOF
# RUN python -m pip install -r requirements.txt
# ECHO Access your app at http://localhost:5000
# START python __file__
# ===

from h2o_nitro import AsyncView as View, box


async def main(view: View):
    name = await view(box('What is your name?', value='Boaty McBoatface'))
    feel = await view(box(f'How do you feel today, {name}?', value='intrigued'))
    await view(f'What a coincidence, {name}, I feel {feel}, too!')


nitro = View(main, title='Hello Nitro!', caption='v1.0')

# ┌─────────────── Tornado Boilerplate ───────────────┐

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.queues
from h2o_nitro_web import web_directory


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
