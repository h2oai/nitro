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
