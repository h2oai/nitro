from h2o_nitro import AsyncView as View
from h2o_nitro_bokeh import bokeh_plugin, bokeh_box
from example_bokeh_util import *


async def main(view: View):
    # Show plots one by one.
    await view(bokeh_box(make_bokeh_scatterplot()))
    await view(bokeh_box(make_bokeh_hexbin_plot()))
    await view(bokeh_box(make_bokeh_stacked_area()))


nitro = View(
    main,
    title='Nitro + Bokeh',
    caption='A minimal example',
    plugins=[bokeh_plugin()],  # Include the bokeh plugin
)
