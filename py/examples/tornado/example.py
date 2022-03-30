from h2o_nitro import AsyncView as View, box, web_directory


async def main(view: View):
    name = await view(box('What is your name?', value='Boaty McBoatface'))
    feel = await view(box(f'How do you feel today, {name}?', value='intrigued'))
    await view(f'What a coincidence, {name}, I feel {feel}, too!')


nitro = View(main, title='Hello Nitro!', caption='v1.0')

# ------------ How to integrate with Tornado ------------

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.queues


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
    ],
    static_path=f'{web_directory}/static',
)

if __name__ == "__main__":
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
