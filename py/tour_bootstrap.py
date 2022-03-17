from h2o_nitro import View, option
import simple_websocket
from flask import Flask, request

# EXAMPLES

topics = dict(
    # TOPIC_MAP
)

table_of_contents = '''
TOC
'''


def main(view: View):
    topic = view(table_of_contents)
    topics[topic](view)


nitro = View(
    main,
    title='Nitro',
    caption='v0.1',
    menu=[
        option(main, 'Contents', icon='Documentation'),
        # MENU
    ],
    nav=[
        option(main, 'Contents'),
    ],
)

app = Flask(__name__, static_folder='../web/build', static_url_path='')


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
