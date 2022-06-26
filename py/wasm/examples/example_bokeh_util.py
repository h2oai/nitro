import numpy as np
import pandas as pd
from bokeh.models import HoverTool
from bokeh.palettes import brewer
from bokeh.plotting import figure
from bokeh.sampledata.penguins import data
from bokeh.transform import factor_cmap, factor_mark


# Source: http://docs.bokeh.org/en/latest/docs/gallery/marker_map.html
def make_bokeh_scatterplot():
    SPECIES = sorted(data.species.unique())
    MARKERS = ['hex', 'circle_x', 'triangle']

    p = figure(title="Penguin size", background_fill_color="#fafafa")
    p.xaxis.axis_label = 'Flipper Length (mm)'
    p.yaxis.axis_label = 'Body Mass (g)'

    p.scatter("flipper_length_mm", "body_mass_g", source=data,
              legend_group="species", fill_alpha=0.4, size=12,
              marker=factor_mark('species', MARKERS, SPECIES),
              color=factor_cmap('species', 'Category10_3', SPECIES))

    p.legend.location = "top_left"
    p.legend.title = "Species"

    return p


# Source: http://docs.bokeh.org/en/latest/docs/gallery/hexbin.html
def make_bokeh_hexbin_plot():
    n = 500

    x = 2 + 2 * np.random.standard_normal(n)
    y = 2 + 2 * np.random.standard_normal(n)

    p = figure(title="Hexbin for 500 points", match_aspect=True,
               tools="wheel_zoom,reset", background_fill_color='#440154')
    p.grid.visible = False

    r, bins = p.hexbin(x, y, size=0.5, hover_color="pink", hover_alpha=0.8)

    p.circle(x, y, color="white", size=1)

    p.add_tools(HoverTool(
        tooltips=[("count", "@c"), ("(q,r)", "(@q, @r)")],
        mode="mouse", point_policy="follow_mouse", renderers=[r]
    ))

    return p


# Source: http://docs.bokeh.org/en/latest/docs/gallery/stacked_area.html
def make_bokeh_stacked_area():
    n = 10
    df = pd.DataFrame(np.random.randint(10, 100, size=(15, n))).add_prefix('y')

    p = figure(x_range=(0, len(df) - 1), y_range=(0, 800))
    p.grid.minor_grid_line_color = '#eeeeee'

    names = [f"y{i}" for i in range(n)]
    p.varea_stack(stackers=names, x='index', color=brewer['Spectral'][n], legend_label=names, source=df)

    p.legend.orientation = "horizontal"
    p.legend.background_fill_color = "#fafafa"

    return p


