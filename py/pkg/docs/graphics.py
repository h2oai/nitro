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
def graphics_line_y(view: View):  # height 3
    view(
        box(
            mode='g line-y',
            style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
        ),
        box(
            mode='g line-y',
            style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),
    )


# ## Step Y
def graphics_step_y(view: View):  # height 3
    view(
        box(
            mode='g step-y',
            style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
        ),
        box(
            mode='g step-y',
            style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),
    )


# ## Interval Y
def graphics_interval_y(view: View):  # height 3
    view(
        box(
            mode='g interval-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
        ),
        box(
            mode='g interval-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),
    )


# ## Stroke Y
def graphics_stroke_y(view: View):  # height 3
    view(
        box(
            mode='g stroke-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
        ),
        box(
            mode='g stroke-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),
    )


# ## Tick Y
def graphics_tick_y(view: View):  # height 3
    view(
        box(
            mode='g tick-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
        ),
        box(
            mode='g tick-y',
            style='w-48 h-8 stroke-indigo-700',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),
    )


# ## Guide X
def graphics_guide_x(view: View):  # height 3
    view(
        box(
            mode='g guide-x',
            style='h-8 stroke-indigo-700',
            data=[0, 0.2, 0.4, 0.6, 0.8, 0.85, 0.9, 0.95, 0.975, 1],
        ),
    )


# ## Guide Y
def graphics_guide_y(view: View):  # height 3
    view(
        box(
            mode='g guide-y',
            style='h-48 w-8 stroke-indigo-700',
            data=[0, 0.2, 0.4, 0.6, 0.8, 0.85, 0.9, 0.95, 0.975, 1],
        ),
    )


# ## Bar X
def graphics_bar_x(view: View):  # height 3
    style = 'w-48 h-2 fill-indigo-100 stroke-indigo-700'
    view(
        box(mode='g bar-x', style=style, data=[0, 0.35]),
        box(mode='g bar-x', style=style, data=[0.35, 1]),
    )


# ## Bar Y
def graphics_bar_y(view: View):  # height 3
    style = 'w-2 h-48 fill-indigo-100 stroke-indigo-700'
    view(row(
        box(mode='g bar-y', style=style, data=[0, 0.35]),
        box(mode='g bar-y', style=style, data=[0.35, 1]),
    ))


# ## Circle
def graphics_circle(view: View):  # height 3
    style = 'w-24 h-24 fill-indigo-100 stroke-indigo-700'
    view(row(
        box(mode='g circle', style=style, data=[0, 0.35]),
        box(mode='g circle', style=style, data=[0, 0.35, 0.5, 1]),
        box(mode='g circle', style=style, data=[0, 0.35, 0.5]),
        box(mode='g circle', style=style, data=[0, 0.35, 0.5, 0.75]),
        box(mode='g circle', style=style, data=[1, 0.35, 0.5, 1]),
    ))


# ## Arc
def graphics_arc(view: View):  # height 3
    style = 'w-24 h-12 fill-indigo-100 stroke-indigo-700'
    view(row(
        box(mode='g arc', style=style, data=[0, 0.35]),
        box(mode='g arc', style=style, data=[0, 0.35, 0.5, 1]),
        box(mode='g arc', style=style, data=[0, 0.35, 0.5]),
        box(mode='g arc', style=style, data=[0, 0.35, 0.5, 0.75]),
        box(mode='g arc', style=style, data=[1, 0.35, 0.5, 1]),
    ))
