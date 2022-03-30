import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.queues
from h2o_nitro import web_directory


# SAMPLE_ASYNC

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
