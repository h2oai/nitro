import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.queues

# --- Nitro ---

from h2o_nitro import View, box


def main(view: View):
    name = view(box('What is your name?', value='Boaty McBoatface'))
    feel = view(box(f'How do you feel today, {name}?', value='intrigued'))
    view(f'What a coincidence, {name}, I feel {feel}, too!')


nitro = View(main, title='Hello Nitro!', caption='v1.0')


# --- Tornado ---
class AsyncView:
    def __init__(self, send, recv):
        self._send = send
        self._recv = recv

    async def serve(self):
        while True:
            msg = await self._recv()
            if msg is None:
                break
            await self._send(f'echo: {msg}')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class NitroSocket(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = tornado.queues.Queue()
        self.view = None

    async def open(self):
        self.view = AsyncView(self.write_message, self.queue.get)
        tornado.ioloop.IOLoop.current().add_callback(self.view.serve)

    async def on_message(self, message):
        await self.queue.put(message)

    def on_close(self):
        self.queue.put(None)


app = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r"/nitro", NitroSocket),
    ],
    static_path='static',
    debug=True,
)

if __name__ == "__main__":
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
