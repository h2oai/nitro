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

from h2o_nitro import View, box, row, col, option, lorem


# # Graphics
# Draw visualizations, microcharts, sparklines, and other data graphics.

# ## Line Y
# Set `mode='g line-y'` to draw line and area charts.
#
# For a single curve, set `data=` to a sequence of normalized y-coordinates.
#
# For dual curves, set `data=` to a sequence of normalized `[low, high]` y-coordinates.
def graphics_line_y(view: View):  # height 3
    view(row(
        # Single curve:
        col(
            # Stroke and fill:
            box(
                mode='g line-y',
                style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
                data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5] * 6,
            ),
            # Stroke only:
            box(
                mode='g line-y',
                style='w-48 h-8 fill-none stroke-indigo-700',
                data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5] * 6,
            ),
            # Fill only:
            box(
                mode='g line-y',
                style='w-48 h-8 fill-indigo-700 stroke-none',
                data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5] * 6,
            ),
        ),
        # Dual curve:
        col(
            # Stroke and fill:
            box(
                mode='g line-y',
                style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
                data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
            ),

            # Stroke only:
            box(
                mode='g line-y',
                style='w-48 h-8 fill-none stroke-indigo-700',
                data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
            ),
            # Fill only:
            box(
                mode='g line-y',
                style='w-48 h-8 fill-indigo-700 stroke-none',
                data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
            ),
        ),
    ))


# ## Curve Y
# Set `mode='g curve-y'` to draw line and area curves.
#
# For a single curve, set `data=` to a sequence of normalized y-coordinates.
#
# For dual curves, set `data=` to a sequence of normalized `[low, high]` y-coordinates.
def graphics_curve_y(view: View):  # height 3
    view(row(
        # Single curve:
        col(
            # Stroke and fill:
            box(
                mode='g curve-y',
                style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
                data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5],
            ),
            # Stroke only:
            box(
                mode='g curve-y',
                style='w-48 h-8 fill-none stroke-indigo-700',
                data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5],
            ),
            # Fill only:
            box(
                mode='g curve-y',
                style='w-48 h-8 fill-indigo-700 stroke-none',
                data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5],
            ),
        ),
        # Dual curve:
        col(
            # Stroke and fill:
            box(
                mode='g curve-y',
                style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
                data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
            ),

            # Stroke only:
            box(
                mode='g curve-y',
                style='w-48 h-8 fill-none stroke-indigo-700',
                data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
            ),
            # Fill only:
            box(
                mode='g curve-y',
                style='w-48 h-8 fill-indigo-700 stroke-none',
                data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
            ),
        ),
    ))


# ## Step Y
# Set `mode='g step-y'` to draw step charts. Step charts are similar to line charts, except that adjacent points are
# connected using discrete steps instead of line segments.
#
# For a single curve, set `data=` to a sequence of normalized y-coordinates.
#
# For dual curves, set `data=` to a sequence of normalized `[low, high]` y-coordinates.
def graphics_step_y(view: View):  # height 3
    view(row(
        # Single curve:
        col(
            # Stroke and fill:
            box(
                mode='g step-y',
                style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
                data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
            ),
            # Stroke only:
            box(
                mode='g step-y',
                style='w-48 h-8 fill-none stroke-indigo-700',
                data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
            ),
            # Fill only:
            box(
                mode='g step-y',
                style='w-48 h-8 fill-indigo-700 stroke-none',
                data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
            ),
        ),
        # Dual curve:
        col(
            # Stroke and fill:
            box(
                mode='g step-y',
                style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
                data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
            ),
            # Stroke only:
            box(
                mode='g step-y',
                style='w-48 h-8 fill-none stroke-indigo-700',
                data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
            ),
            # Fill only:
            box(
                mode='g step-y',
                style='w-48 h-8 fill-indigo-700 stroke-none',
                data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
            ),
        ),
    ))


# ## Bar Y
# Set `mode='g bar-y'` to draw bar/column charts.
#
# For simple bars, set `data=` to a sequence of normalized y-coordinates.
#
# For interval-valued bars, set `data=` to a sequence of normalized `[low, high]` y-coordinates.
def graphics_bar_y(view: View):  # height 3
    view(
        # "Column chart":
        box(
            mode='g bar-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
        ),
        # Interval-valued:
        box(
            mode='g bar-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
        ),
    )


# ## Stroke Y
# Set `mode='g stroke-y'` to draw a sequence of vertical strokes. The `stroke-y` mode is similar to the `bar-y`
# mode, except that you can control the thickness of the strokes (bars) when using `stroke-y`.
#
# For simple strokes, set `data=` to a sequence of normalized y-coordinates.
#
# For interval-valued strokes, set `data=` to a sequence of normalized `[low, high]` y-coordinates.
def graphics_stroke_y(view: View):  # height 3
    view(
        # Strokes:
        box(
            mode='g stroke-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
        ),
        # Thicker strokes:
        box(
            mode='g stroke-y',
            style='w-48 h-8 stroke-indigo-700 stroke-4',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
        ),
        # Interval-valued:
        box(
            mode='g stroke-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
        ),
    )


# ## Tick Y
# Set `mode='g tick-y'` to draw a sequence of horizontal ticks.
#
# For simple ticks, set `data=` to a sequence of normalized y-coordinates.
#
# For interval-valued ticks, set `data=` to a sequence of normalized `[low, high]` y-coordinates.
def graphics_tick_y(view: View):  # height 3
    view(
        # Ticks:
        box(
            mode='g tick-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
        ),
        # Thicker ticks:
        box(
            mode='g tick-y',
            style='w-48 h-8 stroke-indigo-700 stroke-2',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
        ),
        # Interval-valued
        box(
            mode='g tick-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
        ),
    )


# ## Guide X
# Set `mode='g guide-x'` to draw a sequence of x-axis guide lines.
#
# Set `data=` to a sequence of normalized x-coordinates.
def graphics_guide_x(view: View):  # height 3
    view(
        box(
            mode='g guide-x',
            style='w-48 h-8 stroke-indigo-700',
            data=[0, 0.2, 0.4, 0.6, 0.8, 0.85, 0.9, 0.95, 0.975, 1],
        ),
    )


# ## Guide Y
# Set `mode='g guide-y'` to draw a sequence of y-axis guide lines.
#
# Set `data=` to a sequence of normalized y-coordinates.
def graphics_guide_y(view: View):  # height 3
    view(
        box(
            mode='g guide-y',
            style='w-8 h-48 stroke-indigo-700',
            data=[0, 0.2, 0.4, 0.6, 0.8, 0.85, 0.9, 0.95, 0.975, 1],
        ),
    )


# ## Gauge X
# Set `mode='g gauge-x'` to draw a horizontal gauge.
#
# Set `data=` to normalized `[start, end, size]` values.
# `size` defines the thickness of the bar relative to the rail, and defaults to 1 (bar is as thick as the rail).
def graphics_gauge_x(view: View):  # height 3
    style = 'w-48 h-4 fill-indigo-100 stroke-indigo-700'
    view(
        box(mode='g gauge-x', style=style, data=[0, 0.35]),
        box(mode='g gauge-x', style=style, data=[0.35, 1]),
        box(mode='g gauge-x', style=style, data=[0, 0.35, 0.5]),  # thinner bar
    )


# ## Gauge Y
# Set `mode='g gauge-y'` to draw a vertical gauge.
#
# Set `data=` to normalized `[start, end, size]` values.
# `size` defines the thickness of the bar relative to the rail, and defaults to 1 (bar is as thick as the rail).
def graphics_gauge_y(view: View):  # height 3
    style = 'w-4 h-48 fill-indigo-100 stroke-indigo-700'
    view(row(
        box(mode='g gauge-y', style=style, data=[0, 0.35]),
        box(mode='g gauge-y', style=style, data=[0.35, 1]),
        box(mode='g gauge-y', style=style, data=[0, 0.35, 0.5]),  # thinner bar
    ))


# ## Circular Gauge
# Set `mode='g gauge-c'` to draw a circular gauge.
#
# Set `data=` to normalized `[start-angle, end-angle, inner-radius, outer-radius, size]` values.
#
# `inner-radius` and `outer-radius` are optional, and default to `0` and `1` respectively.
#
# `size` defines the size of the bar relative to the rail, and defaults to 1.
def graphics_gauge_c(view: View):  # height 4
    style = 'w-24 h-24 fill-indigo-100 stroke-indigo-700'
    view(
        row(
            box(mode='g gauge-c', style=style, data=[0, 0.35]),
            box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5, 1]),
            box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5]),  # end-radius defaults to 1.
            box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5, 1, 0.5]),  # thinner bar
            box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5, 0.75]),
            box(mode='g gauge-c', style=style, data=[0.25, 0.75, 0.5, 1]),
        ),
        row(
            # With label:
            box(
                box(mode='g gauge-c', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box('35%') / 'text-sm font-bold',
            ) / 'relative flex w-24 h-24 justify-center items-center',
            # Stacked:
            box(
                box(mode='g gauge-c', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box(mode='g gauge-c', data=[0.35, 0.65, 0.5]) / 'absolute inset-0 fill-none stroke-red-500',
                box(mode='g gauge-c', data=[0.65, 0.8, 0.5]) / 'absolute inset-0 fill-none stroke-red-300',
            ) / 'relative w-24 h-24',
            # Concentric:
            box(
                box(mode='g gauge-c', data=[0, 0.35, 0.8, 1]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box(mode='g gauge-c', data=[0, 0.65, 0.5, 0.7]) / 'absolute inset-0 fill-blue-100 stroke-blue-700',
                box(mode='g gauge-c', data=[0, 0.85, 0.2, 0.4]) / 'absolute inset-0 fill-green-100 stroke-green-700',
            ) / 'relative w-24 h-24',
        )
    )


# ## Semicircular Gauge
# Set `mode='g gauge-sc'` to draw a semicircular gauge.
#
# Set `data=` to normalized `[start-angle, end-angle, inner-radius, outer-radius, size]` values.
#
# `inner-radius` and `outer-radius` are optional, and default to `0` and `1` respectively.
#
# `size` defines the size of the bar relative to the rail, and defaults to 1.
def graphics_gauge_sc(view: View):  # height 3
    style = 'w-24 h-12 fill-indigo-100 stroke-indigo-700'
    view(
        row(
            box(mode='g gauge-sc', style=style, data=[0, 0.35]),
            box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5, 1]),
            box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5]),  # end-radius defaults to 1.
            box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5, 1, 0.5]),  # thinner bar
            box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5, 0.75]),
            box(mode='g gauge-sc', style=style, data=[0.25, 0.75, 0.5, 1]),
        ),
        row(
            # With label:
            box(
                box(mode='g gauge-sc', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box('35%') / 'text-xs font-medium',
            ) / 'relative flex w-24 h-12 justify-center items-end',
            # Stacked:
            box(
                box(mode='g gauge-sc', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box(mode='g gauge-sc', data=[0.35, 0.65, 0.5]) / 'absolute inset-0 fill-none stroke-red-500',
                box(mode='g gauge-sc', data=[0.65, 0.8, 0.5]) / 'absolute inset-0 fill-none stroke-red-300',
            ) / 'relative w-24 h-12',
            # Concentric:
            box(
                box(mode='g gauge-sc', data=[0, 0.35, 0.8, 1]) / 'absolute inset-0 fill-red-100 stroke-red-700',
                box(mode='g gauge-sc', data=[0, 0.65, 0.5, 0.7]) / 'absolute inset-0 fill-blue-100 stroke-blue-700',
                box(mode='g gauge-sc', data=[0, 0.85, 0.2, 0.4]) / 'absolute inset-0 fill-green-100 stroke-green-700',
            ) / 'relative w-24 h-12',
        ),
    )


# ## Label
# Set `mode='g-label'` to draw a sequence of labels.
#
# - Set `data=` to a sequence of normalized `[x, y, text, justify, align]` values.
# - Set `justify` to `0` (left), `1` (right), or omit to center (default).
# - Set `align` to `0` (top), `1` (bottom), or omit to center (default).
def graphics_annotation(view: View):  # height 3
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
# Set `data=` to a sequence of normalized `[x, y, diameter, size, start-angle, length]` values.
def graphics_arc(view: View):  # height 3
    view(row(
        box(
            mode='g-arc',
            style='w-32 h-32 fill-indigo-100 stroke-indigo-700',
            data=[
                [0.05, 0.5, 0.1],
                [0.25, 0.5, 0.3],
                [0.7, 0.5, 0.6, 0.5],  # donut
            ],
        ),
        box(
            mode='g-arc',
            style='w-32 h-32 fill-indigo-100 stroke-indigo-700',
            data=[
                [1 / 8, 0.5, 1 / 5, 1, 3 / 4, 1 / 2],
                [3 / 8, 0.5, 1 / 3, .5, 0, 3 / 4],
                [5 / 8, 0.5, 1 / 5, 1, 1 / 12, 4 / 12],
                [7 / 8, 0.5, 1 / 5, .75, 1 / 12, 3 / 4],
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
            box(mode='g bar-y', style='w-48 h-4 stroke-green-700', data=wins),
            box(mode='g bar-y', style='w-48 h-4 stroke-red-700', data=losses),
        )
    )


# ## Stacked bar
# Overlay multiple gauges to create a stacked bar.
def graphics_stacked_bar(view: View):  # height 3
    bar = box(mode='g gauge-x') / 'absolute inset-0 fill-none'
    view(
        box(
            bar(data=[0, 0.1]) / 'stroke-red-400',
            bar(data=[0.1, 0.3]) / 'stroke-orange-400',
            bar(data=[0.3, 0.7]) / 'stroke-amber-400',
            bar(data=[0.7, 0.8]) / 'stroke-lime-400',
            bar(data=[0.8, 1.0]) / 'stroke-green-400',
        ) / 'relative w-48 h-4',
    )


# ## Bullet graph
# Overlay multiple gauge and guide graphics to create a bullet graph.
def graphics_bullet_graph(view: View):  # height 3
    layer = box() / 'absolute inset-0 fill-none'
    bar = layer(mode='g gauge-x')
    view(
        box(
            bar(data=[0, 0.6]) / 'stroke-slate-400',  # band
            bar(data=[0.6, 0.8]) / 'stroke-slate-300',  # band
            bar(data=[0.8, 1]) / 'stroke-slate-200',  # band
            bar(data=[0, 0.7, 0.25]) / 'stroke-slate-900',  # measure
            layer(mode='g guide-x', data=[0.9]) / 'stroke-red-800',  # comparative measure
        ) / 'relative w-48 h-6',
    )
