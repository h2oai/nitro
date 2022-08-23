# ===
# About: 99 bottles of beer on a timer
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
# START python -m uvicorn __name__:app --reload --port 5000
# ===

from h2o_nitro import AsyncView as View
import asyncio


async def main(view: View):
    for i in range(99, 0, -1):  # Decrement from 99 to 1
        await view(
            f"""
            ## {i} bottles of beer

            {i} bottles of beer on the wall, {i} bottles of beer.

            Take one down, pass it around, {i - 1} bottles of beer on the wall...
            """,
            read=False,  # Don't read user input
            halt=True,  # Don't show Continue button
        )
        await asyncio.sleep(1)  # Wait for 1 second


nitro = View(main, title='Hello Nitro!', caption='v1.0')

# ┌─────────────── Uvicorn Boilerplate ───────────────┐

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse
from h2o_nitro_web import web_directory


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
