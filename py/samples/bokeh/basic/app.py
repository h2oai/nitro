import simple_websocket
from flask import Flask, request, send_from_directory
from h2o_nitro import View, box, web_directory, Plugin, Script

from bokeh.plotting import figure
from bokeh.embed import json_item
from bokeh.model import Model
import json

# A little Javascript for embedding the Bokeh plot.
# See: http://docs.bokeh.org/en/latest/docs/user_guide/embed.html#json-items
bokeh_embed_js = '''
exports.embed = (context, element, data) => {
    Bokeh.embed.embed_item(JSON.parse(data.model), element.id);
};
'''


# Creates a Nitro box from a Bokeh model (plots, widgets, etc.)
def bokeh_box(model: Model):
    return box(mode='plugin:bokeh.embed', data=dict(model=json.dumps(json_item(model))))


# Our app's entry point
def main(view: View):
    # Create a Bokeh plot
    plot = figure()
    plot.circle([1, 2], [3, 4])

    # Show the Bokeh plot
    view(bokeh_box(plot))


nitro = View(
    main,
    title='Nitro + Bokeh',
    caption='A minimal example',
    plugins=[
        Plugin(name='bokeh', scripts=[
            Script(source='https://cdn.bokeh.org/bokeh/release/bokeh-2.4.0.min.js', cross_origin='anonymous'),
            Script(source=bokeh_embed_js, type='inline'),
        ]),
    ],
)

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
