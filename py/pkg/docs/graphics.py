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
# Draw microcharts, sparklines, and other data graphics.

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
# Set `data=` to normalized `[start, end]` values.
def graphics_gauge_x(view: View):  # height 3
    style = 'w-48 h-2 fill-indigo-100 stroke-indigo-700'
    view(
        box(mode='g gauge-x', style=style, data=[0, 0.35]),
        box(mode='g gauge-x', style=style, data=[0.35, 1]),
    )


# ## Gauge Y
# Set `mode='g gauge-y'` to draw a vertical gauge.
#
# Set `data=` to normalized `[start, end]` values.
def graphics_gauge_y(view: View):  # height 3
    style = 'w-2 h-48 fill-indigo-100 stroke-indigo-700'
    view(row(
        box(mode='g gauge-y', style=style, data=[0, 0.35]),
        box(mode='g gauge-y', style=style, data=[0.35, 1]),
    ))


# ## Circular Gauge
# Set `mode='g gauge-c'` to draw a circular gauge.
#
# Set `data=` to normalized `[start-angle, end-angle, inner-radius, outer-radius]` values.
#
# `inner-radius` and `outer-radius` are optional, and default to `0` and `1` respectively.
def graphics_gauge_c(view: View):  # height 3
    style = 'w-24 h-24 fill-indigo-100 stroke-indigo-700'
    view(row(
        box(mode='g gauge-c', style=style, data=[0, 0.35]),
        box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5, 1]),
        box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5]),  # end-radius defaults to 1.
        box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5, 0.75]),
        box(mode='g gauge-c', style=style, data=[1, 0.35, 0.5, 1]),
    ))


# ## Semi-circular Gauge
# Set `mode='g gauge-sc'` to draw a semi-circular gauge.
#
# Set `data=` to normalized `[start-angle, end-angle, inner-radius, outer-radius]` values.
#
# `inner-radius` and `outer-radius` are optional, and default to `0` and `1` respectively.
def graphics_gauge_sc(view: View):  # height 3
    style = 'w-24 h-12 fill-indigo-100 stroke-indigo-700'
    view(row(
        box(mode='g gauge-sc', style=style, data=[0, 0.35]),
        box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5, 1]),
        box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5]),  # end-radius defaults to 1.
        box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5, 0.75]),
        box(mode='g gauge-sc', style=style, data=[1, 0.35, 0.5, 1]),
    ))
