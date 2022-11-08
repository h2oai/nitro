# Copyright 2022 H2O.ai, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import random
import math

from h2o_nitro import View, box, row, col, option, lorem
import h2o_nitro.graphics


# # Graphics
# Draw visualizations, microcharts, sparklines, and other data graphics.


# ## Introduction
# Nitro includes graphics primitives that can be composited together to create custom visualizations and charts
# that aesthetically match the surrounding page layout.
#
# Graphics in Nitro are responsive, which means they resize automatically when the page size changes. Unlike SVG
# graphics, which resize physically, Nitro's graphics resize semantically (or logically). For example, if the points
# in a scatterplot are 10px wide in a visualization, they'll continue to be 10px wide when resized, so that the
# points do not appear distorted or skewed at different sizes.
#
# The graphical elements are styled using `style=`, similar to how you would style everything else in Nitro.
#
# Graphical primitives include lines, bars, points, guides, labels, and so on. Each of these are covered in detail
# in the following sections. Each primitive uses normalized
#
# To stack graphics, use the `relative` style on the parent box, and `absolute inset-0` on each child box.
# This makes the boxes render on top of each other instead of one below the other.
#
# Here's a rather complicated example that creates a custom time series chart from primitives. This example is just for
# demonstrating how compositing works.
# Most of the time, the graphics you create in Nitro would be much simpler than this.
def graphics_intro(view: View):  # height 4
    # Some pretty random data:
    n = 100
    data1 = h2o_nitro.graphics.random_walk(n)
    data2 = h2o_nitro.graphics.random_walk(n)
    # Select a few random points to highlight:
    highlighted = [random.randint(0, n - 1) for _ in range(4)]
    guides = [i / (n - 1) for i in highlighted]
    points1 = [(i / (n - 1), data1[i]) for i in highlighted]
    points2 = [(i / (n - 1), data2[i]) for i in highlighted]

    # Compose graphics:
    layer = box() / 'absolute inset-0'
    view(
        row(
            # Y-axis:
            box(
                mode='g-label',
                data=[
                    # All labels are right-justified
                    [1, 0 / 4, '0', 1, 0],  # first label, align top
                    [1, 1 / 4, '100', 1],
                    [1, 2 / 4, '200', 1],
                    [1, 3 / 4, '300', 1],
                    [1, 4 / 4, '400', 1, 1],  # last label, align bottom
                ],
            ) / 'w-8 h-48 text-xs text-slate-300',
            col(
                box(
                    # Month shading:
                    layer(mode='g-rect', data=[
                        [1 / 10, .5, 1 / 5, 1],
                        [5 / 10, .5, 1 / 5, 1],
                        [9 / 10, .5, 1 / 5, 1],
                    ]) / 'fill-slate-700 stroke-none',
                    # X-guides
                    layer(mode='g-guide-x', data=guides) / 'stroke-rose-500 fill-none',
                    # Y-guides
                    layer(mode='g-guide-y', data=[.25, .5, .75]) / 'stroke-slate-600 fill-none',
                    # Time-series
                    layer(mode='g-line-y', data=data1) / 'stroke-yellow-400 fill-none',
                    layer(mode='g-line-y', data=data2) / 'stroke-emerald-400 fill-none',
                    # Highlighted points:
                    layer(mode='g-point', data=points1) / 'stroke-yellow-400 fill-none',
                    layer(mode='g-point', data=points2) / 'stroke-emerald-400 fill-none',
                ) / 'relative w-full h-48',
                # X-axis:
                box(
                    mode='g-label',
                    data=[
                        [0 / 5, .5, 'Jul', 0],  # first label, left-justify
                        [1 / 5, .5, 'Aug'],
                        [2 / 5, .5, 'Sep'],
                        [3 / 5, .5, 'Oct'],
                        [4 / 5, .5, 'Nov'],
                        [5 / 5, .5, 'Dec', 1],  # last label, right-justify
                    ],
                ) / 'w-full h-8 text-xs text-slate-300',
            ) / 'w-full',
        ) / 'bg-slate-800 p-4',
    )


# ## Line
# Set `mode='g-line-x'` or `mode='g-line-y'` to draw line and area charts.
#
# For a single line, set `data=` to a sequence of normalized values.
#
# For intervals (dual lines), set `data=` to a sequence of normalized `[low, high]` values.
def graphics_line_xy(view: View):  # height 3
    data = [.05, .24, .53, .61, .28, .45, .56, .68, .95, .72]
    intervals = [(.62, .9), (.57, 1), (.28, .66), (.34, .77), (.25, .48),
                 (0, .39), (.14, .65), (.18, .79), (.40, .78), (.61, 1)]

    view(row(
        # Single curve:
        col(
            # Stroke and fill:
            box(mode='g-line-y', style='w-32 h-8 fill-indigo-100 stroke-indigo-700', data=data),
            # Stroke only:
            box(mode='g-line-y', style='w-32 h-8 fill-none stroke-indigo-700', data=data),
            # Fill only:
            box(mode='g-line-y', style='w-32 h-8 fill-indigo-700 stroke-none', data=data),
        ),
        # Dual curve:
        col(
            # Stroke and fill:
            box(mode='g-line-y', style='w-32 h-8 fill-indigo-100 stroke-indigo-700', data=intervals),
            # Stroke only:
            box(mode='g-line-y', style='w-32 h-8 fill-none stroke-indigo-700', data=intervals),
            # Fill only:
            box(mode='g-line-y', style='w-32 h-8 fill-indigo-700 stroke-none', data=intervals),
        ),
        # Single curve:
        row(
            # Stroke and fill:
            box(mode='g-line-x', style='w-8 h-32 fill-indigo-100 stroke-indigo-700', data=data),
            # Stroke only:
            box(mode='g-line-x', style='w-8 h-32 fill-none stroke-indigo-700', data=data),
            # Fill only:
            box(mode='g-line-x', style='w-8 h-32 fill-indigo-700 stroke-none', data=data),
        ),
        # Dual curve:
        row(
            # Stroke and fill:
            box(mode='g-line-x', style='w-8 h-32 fill-indigo-100 stroke-indigo-700', data=intervals),
            # Stroke only:
            box(mode='g-line-x', style='w-8 h-32 fill-none stroke-indigo-700', data=intervals),
            # Fill only:
            box(mode='g-line-x', style='w-8 h-32 fill-indigo-700 stroke-none', data=intervals),
        ),
    ))


# ## Curve
# Set `mode='g-curve-x'` or `mode='g-curve-y'` to draw line and area curves.
#
# For a single curve, set `data=` to a sequence of normalized values.
#
# For intervals (dual curves), set `data=` to a sequence of normalized `[low, high]` values.
def graphics_curve_xy(view: View):  # height 3
    data = [.05, .24, .53, .61, .28, .45, .56, .68, .95, .72]
    intervals = [(.62, .9), (.57, 1), (.28, .66), (.34, .77), (.25, .48),
                 (0, .39), (.14, .65), (.18, .79), (.40, .78), (.61, 1)]
    view(row(
        # Single curve:
        col(
            # Stroke and fill:
            box(mode='g-curve-y', style='w-48 h-8 fill-indigo-100 stroke-indigo-700', data=data),
            # Stroke only:
            box(mode='g-curve-y', style='w-48 h-8 fill-none stroke-indigo-700', data=data),
            # Fill only:
            box(mode='g-curve-y', style='w-48 h-8 fill-indigo-700 stroke-none', data=data),
        ),
        # Dual curve:
        col(
            # Stroke and fill:
            box(mode='g-curve-y', style='w-48 h-8 fill-indigo-100 stroke-indigo-700', data=intervals),
            # Stroke only:
            box(mode='g-curve-y', style='w-48 h-8 fill-none stroke-indigo-700', data=intervals),
            # Fill only:
            box(mode='g-curve-y', style='w-48 h-8 fill-indigo-700 stroke-none', data=intervals),
        ),
    ))


# ## Step
# Set `mode='g-step-x'` or `mode='g-step-y'` to draw step charts.
# Step charts are similar to line charts, except that adjacent points are
# connected using discrete steps instead of line segments.
#
# For a single curve, set `data=` to a sequence of normalized values.
#
# For intervals (dual curves), set `data=` to a sequence of normalized `[low, high]` values.
def graphics_step_xy(view: View):  # height 3
    data = [.05, .24, .53, .61, .28, .45, .56, .68, .95, .72]
    intervals = [(.62, .9), (.57, 1), (.28, .66), (.34, .77), (.25, .48),
                 (0, .39), (.14, .65), (.18, .79), (.40, .78), (.61, 1)]
    view(row(
        # Single curve:
        col(
            # Stroke and fill:
            box(mode='g-step-y', style='w-32 h-8 fill-indigo-100 stroke-indigo-700', data=data),
            # Stroke only:
            box(mode='g-step-y', style='w-32 h-8 fill-none stroke-indigo-700', data=data),
            # Fill only:
            box(mode='g-step-y', style='w-32 h-8 fill-indigo-700 stroke-none', data=data),
        ),
        # Dual curve:
        col(
            # Stroke and fill:
            box(mode='g-step-y', style='w-32 h-8 fill-indigo-100 stroke-indigo-700', data=intervals),
            # Stroke only:
            box(mode='g-step-y', style='w-32 h-8 fill-none stroke-indigo-700', data=intervals),
            # Fill only:
            box(mode='g-step-y', style='w-32 h-8 fill-indigo-700 stroke-none', data=intervals),
        ),
        # Single curve:
        row(
            # Stroke and fill:
            box(mode='g-step-x', style='w-8 h-32 fill-indigo-100 stroke-indigo-700', data=data),
            # Stroke only:
            box(mode='g-step-x', style='w-8 h-32 fill-none stroke-indigo-700', data=data),
            # Fill only:
            box(mode='g-step-x', style='w-8 h-32 fill-indigo-700 stroke-none', data=data),
        ),
        # Dual curve:
        row(
            # Stroke and fill:
            box(mode='g-step-x', style='w-8 h-32 fill-indigo-100 stroke-indigo-700', data=intervals),
            # Stroke only:
            box(mode='g-step-x', style='w-8 h-32 fill-none stroke-indigo-700', data=intervals),
            # Fill only:
            box(mode='g-step-x', style='w-8 h-32 fill-indigo-700 stroke-none', data=intervals),
        ),
    ))


# ## Bar
# Set `mode='g-bar-x'` or `mode='g-bar-y'` to draw bar/column charts.
#
# For simple bars, set `data=` to a sequence of normalized values.
#
# For interval-valued bars, set `data=` to a sequence of normalized `[low, high]` values.
def graphics_bar_xy(view: View):  # height 3
    data = [.05, .24, .53, .61, .28, .45, .56, .68, .95, .72]
    intervals = [(.62, .9), (.57, 1), (.28, .66), (.34, .77), (.25, .48),
                 (0, .39), (.14, .65), (.18, .79), (.40, .78), (.61, 1)]
    view(row(
        col(
            # "Column chart":
            box(mode='g-bar-y', style='w-32 h-16 stroke-indigo-700', data=data),
            # Interval-valued:
            box(mode='g-bar-y', style='w-32 h-16 stroke-indigo-700', data=intervals),
        ),
        row(
            # "Bar chart":
            box(mode='g-bar-x', style='w-16 h-32 stroke-indigo-700', data=data),
            # Interval-valued:
            box(mode='g-bar-x', style='w-16 h-32 stroke-indigo-700', data=intervals),
        )
    ))


# ## Stroke
# Set `mode='g-stroke-x'` or `mode='g-stroke-y'` to draw a sequence of vertical strokes.
# The `stroke-` mode is similar to the `bar-` mode, except that you can control the thickness of the strokes (bars)
# when using the `stroke-` mode.
#
# For simple strokes, set `data=` to a sequence of normalized values.
#
# For interval-valued strokes, set `data=` to a sequence of normalized `[low, high]` values.
def graphics_stroke_xy(view: View):  # height 3
    data = [.05, .24, .53, .61, .28, .45, .56, .68, .95, .72] * 2
    intervals = [(.62, .9), (.57, 1), (.28, .66), (.34, .77), (.25, .48),
                 (0, .39), (.14, .65), (.18, .79), (.40, .78), (.61, 1)] * 2
    view(row(
        col(
            # Strokes:
            box(mode='g-stroke-y', style='w-32 h-8 stroke-indigo-700', data=data),
            # Thicker strokes:
            box(mode='g-stroke-y', style='w-32 h-8 stroke-indigo-700 stroke-4', data=data),
            # Interval-valued:
            box(mode='g-stroke-y', style='w-32 h-8 stroke-indigo-700', data=intervals),
        ),
        row(
            # Strokes:
            box(mode='g-stroke-x', style='w-8 h-32 stroke-indigo-700', data=data),
            # Thicker strokes:
            box(mode='g-stroke-x', style='w-8 h-32 stroke-indigo-700 stroke-4', data=data),
            # Interval-valued:
            box(mode='g-stroke-x', style='w-8 h-32 stroke-indigo-700', data=intervals),
        )
    ))


# ## Tick Y
# Set `mode='g-tick-y'` to draw a sequence of horizontal ticks.
#
# For simple ticks, set `data=` to a sequence of normalized y-coordinates.
#
# For interval-valued ticks, set `data=` to a sequence of normalized `[low, high]` y-coordinates.
def graphics_tick_y(view: View):  # height 3
    view(
        # Ticks:
        box(
            mode='g-tick-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
        ),
        # Thicker ticks:
        box(
            mode='g-tick-y',
            style='w-48 h-8 stroke-indigo-700 stroke-2',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
        ),
        # Interval-valued
        box(
            mode='g-tick-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
        ),
    )


# ## Guide X
# Set `mode='g-guide-x'` to draw a sequence of x-axis guide lines.
#
# Set `data=` to a sequence of normalized x-coordinates.
def graphics_guide_x(view: View):  # height 3
    view(
        box(
            mode='g-guide-x',
            style='w-48 h-8 stroke-indigo-700',
            data=[0, 0.2, 0.4, 0.6, 0.8, 0.85, 0.9, 0.95, 0.975, 1],
        ),
    )


# ## Guide Y
# Set `mode='g-guide-y'` to draw a sequence of y-axis guide lines.
#
# Set `data=` to a sequence of normalized y-coordinates.
def graphics_guide_y(view: View):  # height 3
    view(
        box(
            mode='g-guide-y',
            style='w-8 h-48 stroke-indigo-700',
            data=[0, 0.2, 0.4, 0.6, 0.8, 0.85, 0.9, 0.95, 0.975, 1],
        ),
    )


# ## Gauge X
# Set `mode='g-gauge-x'` to draw a horizontal gauge.
#
# Set `data=` to normalized `[length, width]` values.
# `width` defines the thickness of the bar relative to the track, and defaults to 1 (bar is as thick as the track).
def graphics_gauge_x(view: View):  # height 3
    style = 'w-48 h-4 fill-indigo-100 stroke-indigo-700'
    view(
        box(mode='g-gauge-x', style=style, data=[0.75]),
        box(mode='g-gauge-x', style=style, data=[0.75, 0.5]),  # thinner bar
    )


# ## Gauge Y
# Set `mode='g-gauge-y'` to draw a vertical gauge.
#
# Set `data=` to normalized `[length, width]` values.
# `width` defines the thickness of the bar relative to the track, and defaults to 1 (bar is as thick as the track).
def graphics_gauge_y(view: View):  # height 3
    style = 'w-4 h-48 fill-indigo-100 stroke-indigo-700'
    view(row(
        box(mode='g-gauge-y', style=style, data=[0.75]),
        box(mode='g-gauge-y', style=style, data=[0.75, 0.5]),  # thinner bar
    ))


# ## Circular Gauge
# Set `mode='g-gauge-c'` to draw a circular gauge.
#
# Set `data=` to normalized `[start-angle, end-angle, inner-radius, outer-radius, size]` values.
#
# Set `data=` to normalized `[length, width, track-length, track-width, rotation]` values.
#
# `inner-radius` and `outer-radius` are optional, and default to `0` and `1` respectively.
#
# `size` defines the size of the bar relative to the track, and defaults to 1.
def graphics_gauge_c(view: View):  # height 4
    style = 'w-24 h-24 fill-indigo-100 stroke-indigo-700'
    view(
        row(
            box(mode='g-gauge-c', style=style, data=[0, 0.35]),
            box(mode='g-gauge-c', style=style, data=[0, 0.35, 0.5, 1]),
            box(mode='g-gauge-c', style=style, data=[0, 0.35, 0.5]),  # end-radius defaults to 1.
            box(mode='g-gauge-c', style=style, data=[0, 0.35, 0.5, 1, 0.5]),  # thinner bar
            box(mode='g-gauge-c', style=style, data=[0, 0.35, 0.5, 0.75]),
            box(mode='g-gauge-c', style=style, data=[0.25, 0.75, 0.5, 1]),
        ),
        row(
            # With label:
            box(
                box(mode='g-gauge-c', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box('35%') / 'text-sm font-bold',
            ) / 'relative flex w-24 h-24 justify-center items-center',
            # Stacked:
            box(
                box(mode='g-gauge-c', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box(mode='g-gauge-c', data=[0.35, 0.65, 0.5]) / 'absolute inset-0 fill-none stroke-red-500',
                box(mode='g-gauge-c', data=[0.65, 0.8, 0.5]) / 'absolute inset-0 fill-none stroke-red-300',
            ) / 'relative w-24 h-24',
            # Concentric:
            box(
                box(mode='g-gauge-c', data=[0, 0.35, 0.8, 1]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box(mode='g-gauge-c', data=[0, 0.65, 0.5, 0.7]) / 'absolute inset-0 fill-blue-100 stroke-blue-700',
                box(mode='g-gauge-c', data=[0, 0.85, 0.2, 0.4]) / 'absolute inset-0 fill-green-100 stroke-green-700',
            ) / 'relative w-24 h-24',
        )
    )


# ## Semicircular Gauge
# Set `mode='g-gauge-sc'` to draw a semicircular gauge.
#
# Set `data=` to normalized `[start-angle, end-angle, inner-radius, outer-radius, size]` values.
#
# `inner-radius` and `outer-radius` are optional, and default to `0` and `1` respectively.
#
# `size` defines the size of the bar relative to the track, and defaults to 1.
def graphics_gauge_sc(view: View):  # height 3
    style = 'w-24 h-12 fill-indigo-100 stroke-indigo-700'
    view(
        row(
            box(mode='g-gauge-sc', style=style, data=[0, 0.35]),
            box(mode='g-gauge-sc', style=style, data=[0, 0.35, 0.5, 1]),
            box(mode='g-gauge-sc', style=style, data=[0, 0.35, 0.5]),  # end-radius defaults to 1.
            box(mode='g-gauge-sc', style=style, data=[0, 0.35, 0.5, 1, 0.5]),  # thinner bar
            box(mode='g-gauge-sc', style=style, data=[0, 0.35, 0.5, 0.75]),
            box(mode='g-gauge-sc', style=style, data=[0.25, 0.75, 0.5, 1]),
        ),
        row(
            # With label:
            box(
                box(mode='g-gauge-sc', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box('35%') / 'text-xs font-medium',
            ) / 'relative flex w-24 h-12 justify-center items-end',
            # Stacked:
            box(
                box(mode='g-gauge-sc', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box(mode='g-gauge-sc', data=[0.35, 0.65, 0.5]) / 'absolute inset-0 fill-none stroke-red-500',
                box(mode='g-gauge-sc', data=[0.65, 0.8, 0.5]) / 'absolute inset-0 fill-none stroke-red-300',
            ) / 'relative w-24 h-12',
            # Concentric:
            box(
                box(mode='g-gauge-sc', data=[0, 0.35, 0.8, 1]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box(mode='g-gauge-sc', data=[0, 0.65, 0.5, 0.7]) / 'absolute inset-0 fill-blue-100 stroke-blue-700',
                box(mode='g-gauge-sc', data=[0, 0.85, 0.2, 0.4]) / 'absolute inset-0 fill-green-100 stroke-green-700',
            ) / 'relative w-24 h-12',
        ),
    )


# ## Label
# Set `mode='g-label'` to draw a sequence of labels.
#
# - Set `data=` to a sequence of normalized `[x, y, text, justify, align]` values.
# - Set `justify` to `0` (left), `1` (right), or omit to center (default).
# - Set `align` to `0` (top), `1` (bottom), or omit to center (default).
def graphics_label(view: View):  # height 3
    view(
        box(
            mode='g-label',
            style='w-48 h-8 text-xs bg-slate-100',
            data=[
                [0, 0.5, '0', 0],  # first label, left-justify
                [0.25, 0.5, '100'],
                [0.5, 0.5, '200'],
                [0.75, 0.5, '300'],
                [1, 0.5, '400', 1],  # last label, right-justify
            ],
        ),
        box(
            mode='g-label',
            style='w-8 h-48 text-xs bg-slate-100',
            data=[
                # All labels are right-justified
                [1, 0, '0', 1, 0],  # first label, align top
                [1, 0.25, '100', 1],
                [1, 0.5, '200', 1],
                [1, 0.75, '300', 1],
                [1, 1, '400', 1, 1],  # last label, align bottom
            ],
        ),
    )


# ## Point
# Set `mode='g-point'` to draw shapes at multiple points.
#
# Set `data=` to a sequence of normalized `[x, y, size, shape]` values, where:
#
# - `(x, y)` is the anchor point of the shape.
# - `size` determines the size of the shape, in pixels (note that this is a fixed size, not normalized).
# - `shape` is one of `c` (circle, default), `s` (square), `d` (diamond),
#   `tu` (triangle-up), `tr` (triangle-right), `td` (triangle-down), `tl` (triangle-left),
#   `h` (horizontal bar), `v` (vertical bar), `p` (plus),`x` (cross),
#   `au` (arrow-up), `ar` (arrow-right), `al` (arrow-left), `ad` (arrow-down).
def graphics_point(view: View):  # height 3
    view(
        box(
            mode='g-point',
            style='w-64 h-8 fill-none stroke-indigo-700',
            data=[
                [1 / 16, .5, 10, 'c'],  # circle
                [2 / 16, .5, 10, 's'],  # square
                [3 / 16, .5, 10, 'd'],  # diamond
                [4 / 16, .5, 10, 'tu'],  # triangle-up
                [5 / 16, .5, 10, 'tr'],  # triangle-right
                [6 / 16, .5, 10, 'td'],  # triangle-down
                [7 / 16, .5, 10, 'tl'],  # triangle-left
                [8 / 16, .5, 10, 'h'],  # horizontal bar
                [9 / 16, .5, 10, 'v'],  # vertical bar
                [10 / 16, .5, 10, 'p'],  # plus
                [11 / 16, .5, 10, 'x'],  # cross
                [12 / 16, .5, 10, 'au'],  # arrow-up
                [13 / 16, .5, 10, 'ar'],  # arrow-right
                [14 / 16, .5, 10, 'ad'],  # arrow-down
                [15 / 16, .5, 10, 'al'],  # arrow-left
            ],
        )
    )


# ## Rectangle
# Set `mode='g-rect'` to draw multiple rectangles.
def graphics_rect(view: View):  # height 3
    view(
        box(
            mode='g-rect',
            style='w-32 h-16 fill-indigo-100 stroke-indigo-700',
            data=[
                [0.25, 0.5, 0.2, 0.9],
                [0.5, 0.5, 0.2, 0.5],
                [0.75, 0.5, 0.2, 0.9, 10],
            ],
        ),
    )


# ## Arc
# Set `mode='g-arc'` to draw multiple arcs or circles.
#
# Set `data=` to a sequence of normalized `[x, y, diameter, length, width, rotation]` values.
def graphics_arc(view: View):  # height 3
    view(row(
        box(
            mode='g-arc',
            style='w-32 h-32 fill-indigo-100 stroke-indigo-700',
            data=[
                [0.05, 0.5, 0.1],
                [0.25, 0.5, 0.3],
                [0.7, 0.5, 0.6, 1, 0.5],  # donut
            ],
        ),
        box(
            mode='g-arc',
            style='w-32 h-32 fill-indigo-100 stroke-indigo-700',
            data=[
                [1 / 8, 0.5, 1 / 5, 1 / 2, 1, 3 / 4],
                [3 / 8, 0.5, 1 / 3, 3 / 4, .5, 0],
                [5 / 8, 0.5, 1 / 5, 4 / 12, 1, 1 / 12],
                [7 / 8, 0.5, 1 / 5, 3 / 4, .75, 1 / 12],
            ],
        ),
    ))


# ## Polyline
# Set `mode='g-polyline'` to draw multiple polylines.
def graphics_polyline(view: View):  # height 3
    view(
        box(
            mode='g-polyline',
            style='w-32 h-8 fill-none stroke-indigo-700',
            data=[
                [
                    0.1, 0.1, 0.1, 0.9,
                    0.2, 0.1, 0.2, 0.9,
                    0.3, 0.1, 0.3, 0.9,
                    0.4, 0.1, 0.4, 0.9,
                    0.5, 0.1, 0.5, 0.9,
                ],
                [
                    0.6, 0.1, 0.9, 0.1,
                    0.6, 0.3, 0.9, 0.3,
                    0.6, 0.5, 0.9, 0.5,
                    0.6, 0.7, 0.9, 0.7,
                    0.6, 0.9, 0.9, 0.9,
                ],
            ],
        ),
    )


# ## Polygon
# Set `mode='g-polygon'` to draw multiple polygon.
def graphics_polygon(view: View):  # height 3
    view(
        box(
            mode='g-polygon',
            style='w-32 h-8 fill-indigo-100 stroke-indigo-700',
            data=[
                [
                    0.1, 0.05, 0.1, 0.9,
                    0.2, 0.1, 0.2, 0.9,
                    0.3, 0.1, 0.3, 0.9,
                    0.4, 0.1, 0.4, 0.9,
                    0.5, 0.05
                ],
                [
                    0.55, 0.1, 0.9, 0.1,
                    0.6, 0.3, 0.9, 0.3,
                    0.6, 0.5, 0.9, 0.5,
                    0.6, 0.7, 0.9, 0.7,
                    0.55, 0.9
                ],
            ],
        ),
    )


# ## Link X
# Set `mode='g-link-x'` to draw connecting lines between pairs of points.
#
# Set `data=` to a sequence of normalized `[x1, y1, x2, y2, t1, t2]` values, where:
#
# - `(x1, y1)` is the start point.
# - `(x2, y2)` is the end point.
# - `t1` (optional) is the start thickness. If omitted, the stroke thickness can be controlled using `style=`.
# - `t2` (optional) is the end thickness. Defaults to `t1` if omitted.
def graphics_link_x(view: View):  # height 3
    view(row(
        box(
            mode='g-link-x',
            style='h-32 w-32 fill-none stroke-indigo-700',
            data=[
                [0.1, 0.75, 0.9, 0.95],
                [0.1, 0.5, 0.9, 0.5],
                [0.1, 0.25, 0.9, 0.05],
            ],
        ),
        box(
            mode='g-link-x',
            style='h-32 w-32 fill-indigo-700 stroke-none',
            data=[
                [0.1, 0.75, 0.9, 0.75, 0.05],  # add thickness
                [0.1, 0.5, 0.9, 0.5, 0.1],  # more thickness
                [0.1, 0.25, 0.9, 0.25, 0.25],  # even more thickness
            ],
        ),
        box(
            mode='g-link-x',
            style='h-32 w-32 fill-indigo-700 stroke-none',
            data=[
                [0.1, 0.75, 0.9, 0.75, 0.1, 0.2],  # start thin, end thick
                [0.1, 0.5, 0.9, 0.5, 0.2, 0.1],  # start thick, end thin
                [0.1, 0.25, 0.9, 0.25, 0.1, 0.1],  # uniform thickness
            ],
        ),
    ))


# ## Spline X
# Set `mode='g-spline-x'` to draw connecting splines (curves) between pairs of points.
#
# Set `data=` to a sequence of normalized `[x1, y1, x2, y2, t1, t2]` values, where:
#
# - `(x1, y1)` is the start point.
# - `(x2, y2)` is the end point.
# - `t1` (optional) is the start thickness. If omitted, the stroke thickness can be controlled using `style=`.
# - `t2` (optional) is the end thickness. Defaults to `t1` if omitted.
def graphics_spline_x(view: View):  # height 3
    view(row(
        box(
            mode='g-spline-x',
            style='h-32 w-32 fill-none stroke-indigo-700',
            data=[
                [0.1, 0.75, 0.9, 0.95],
                [0.1, 0.5, 0.9, 0.5],
                [0.1, 0.25, 0.9, 0.05],
            ],
        ),
        box(
            mode='g-spline-x',
            style='h-32 w-32 fill-indigo-700 stroke-none',
            data=[
                [0.1, 0.75, 0.9, 0.75, 0.05],  # add thickness
                [0.1, 0.5, 0.9, 0.5, 0.1],  # more thickness
                [0.1, 0.25, 0.9, 0.25, 0.25],  # even more thickness
            ],
        ),
        box(
            mode='g-spline-x',
            style='h-32 w-32 fill-indigo-700 stroke-none',
            data=[
                [0.1, 0.8, 0.9, 0.65, 0.2, 0.3],  # variable thickness
                [0.1, 0.5, 0.9, 0.3, 0.2, 0.3],  # variable thickness
                [0.1, 0.25, 0.9, 0.05, 0.1, 0.1],  # uniform thickness
            ],
        ),
    ))


# ## Win Loss
# Stack two bar graphics vertically to create a win-loss graphic.
def graphics_win_loss(view: View):  # height 3
    wins = [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] * 2
    losses = [(x + 1) % 2 for x in wins]  # invert wins
    view(
        box(
            box(mode='g-bar-y', style='w-48 h-4 stroke-green-700', data=wins),
            box(mode='g-bar-y', style='w-48 h-4 stroke-red-700', data=losses),
        )
    )


# ## Stacked bar
# Overlay multiple gauges to create a stacked bar.
def graphics_stacked_bar(view: View):  # height 3
    bar = box(mode='g-gauge-x') / 'absolute inset-0 fill-none'
    view(
        box(
            bar(data=[1.0]) / 'stroke-green-400',
            bar(data=[0.8]) / 'stroke-lime-400',
            bar(data=[0.7]) / 'stroke-amber-400',
            bar(data=[0.3]) / 'stroke-orange-400',
            bar(data=[0.1]) / 'stroke-red-400',
        ) / 'relative w-48 h-4',
    )


# ## Bullet graph
# Overlay multiple gauge and guide graphics to create a bullet graph.
def graphics_bullet_graph(view: View):  # height 3
    layer = box() / 'absolute inset-0 fill-none'
    bar = layer(mode='g-gauge-x')
    view(
        box(
            bar(data=[1]) / 'stroke-slate-200',  # band
            bar(data=[0.8]) / 'stroke-slate-300',  # band
            bar(data=[0.6]) / 'stroke-slate-400',  # band
            bar(data=[0.7, 0.25]) / 'stroke-slate-900',  # measure
            layer(mode='g-guide-x', data=[0.9]) / 'stroke-red-800',  # comparative measure
        ) / 'relative w-48 h-6',
    )


# ## Network graph
# Overlay point and link graphics to create a network graph (node-link diagram).
def graphics_network_graph(view: View):  # height 4
    n = 100
    nodes = [(random.uniform(.05, .95), random.uniform(.05, .95)) for _ in range(n)]
    edges = []
    for x1, y1 in nodes:
        for x2, y2 in random.choices(nodes, k=random.randint(1, 4)):
            edges.append((x1, y1, x2, y2))

    layer = box() / 'absolute inset-0'
    view(
        box(
            layer(mode='g-link-x', data=edges) / 'stroke-indigo-300 fill-none',
            layer(mode='g-point', data=nodes) / 'stroke-indigo-700 fill-none',
        ) / 'relative w-64 h-64',
    )
