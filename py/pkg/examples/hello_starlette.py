# ===
# About: Basic Hello World app using Starlette
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro/py/examples
# Keywords: [basic, uvicorn, starlette]
#
# Setup:
# FILE requirements.txt EOF
# uvicorn
# starlette
# websockets
# h2o-nitro[web]
# EOF
# RUN python -m pip install -r requirements.txt
# START python -m uvicorn hello_starlette:app --reload --port 5000
# ===
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse

# ┌───────────────  Nitro app starts here ───────────────┐

from h2o_nitro import AsyncView as View, box
from h2o_nitro_web import web_directory


async def main(view: View):
    name = await view(box('What is your name?', value='Boaty McBoatface'))
    feel = await view(box(f'How do you feel today, {name}?', value='intrigued'))
    await view(f'What a coincidence, {name}, I feel {feel}, too!')


nitro = View(main, title='Hello Nitro!', caption='v1.0')


# └─────────────── Nitro app ends here ───────────────┘

async def home_page(request):
    return FileResponse(f'{web_directory}/index.html')


async def socket(ws):
    await ws.accept()
    await nitro.serve(ws.send_bytes, ws.receive_bytes)
    await ws.close()


app = Starlette(debug=True, routes=[
    Route('/', home_page),
    WebSocketRoute('/nitro', socket),
    Mount('/', app=StaticFiles(directory=f'{web_directory}')),
])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
