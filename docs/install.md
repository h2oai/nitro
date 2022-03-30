# Getting started

## Installation

```
pip3 install h2o-nitro
```


[Download](https://raw.githubusercontent.com/h2oai/nitro/main/py/tour.py) and run the interactive tour.

``` 
python3 tour.py
```

You'll also want to install a Python framework like Flask, Starlette, or Tornado, explained later.

## Flask

```
pip3 install flask simple_websocket
```

### Example

```py
from h2o_nitro import View, box, web_directory


def main(view: View):
    name = view(box('What is your name?', value='Boaty McBoatface'))
    feel = view(box(f'How do you feel today, {name}?', value='intrigued'))
    view(f'What a coincidence, {name}, I feel {feel}, too!')


nitro = View(main, title='Hello Nitro!', caption='v1.0')

# ------------ How to integrate with Flask ------------

import simple_websocket
from flask import Flask, request, send_from_directory

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
```

[Download this file](https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/flask/example.py).

### Run

```
$ python3 example.py
```

Access the example at [http://localhost:5000/](http://localhost:5000/).

## Starlette / FastAPI

```
pip3 install uvicorn starlette websockets
```

### Example

```py

from h2o_nitro import AsyncView as View, box, web_directory


async def main(view: View):
    name = await view(box('What is your name?', value='Boaty McBoatface'))
    feel = await view(box(f'How do you feel today, {name}?', value='intrigued'))
    await view(f'What a coincidence, {name}, I feel {feel}, too!')


nitro = View(main, title='Hello Nitro!', caption='v1.0')

# ------------ How to integrate with Starlette ------------

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse

app = Starlette(debug=True, routes=[
    Mount('/static', app=StaticFiles(directory=f'{web_directory}/static')),
])


@app.route('/')
async def home_page(request):
    return FileResponse(f'{web_directory}/index.html')


@app.websocket_route('/nitro')
async def socket(ws):
    await ws.accept()
    await nitro.serve(ws.send_bytes, ws.receive_bytes)
    await ws.close()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
```

[Download this file](https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/starlette/example.py).

### Run

```
$ python3 example.py
```

Access the example at [http://localhost:5000/](http://localhost:5000/).

## Tornado

```
pip3 install tornado
```

### Example

```py
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
```

[Download this file](https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/tornado/example.py).

### Run

```
$ python3 example.py
```

Access the example at [http://localhost:5000/](http://localhost:5000/).
