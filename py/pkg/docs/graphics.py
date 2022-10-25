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
        box(mode='g line-y', style='h-8 fill-indigo-100 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5]),
    )


# ## Step Y
def graphics_step_y(view: View):  # height 3
    view(
        box(mode='g step-y', style='h-8 fill-indigo-100 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5]),
    )


# ## Bar Y
def graphics_bar_y(view: View):  # height 3
    view(
        box(mode='g bar-y', style='h-8 fill-indigo-100 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5]),
    )


# ## Stroke Y
def graphics_stroke_y(view: View):  # height 3
    view(
        box(mode='g stroke-y', style='h-8 stroke-indigo-700', data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5]),
    )


# ## Tick Y
def graphics_tick_y(view: View):  # height 3
    view(
        box(mode='g tick-y', style='h-8 stroke-indigo-700', data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5]),
    )
