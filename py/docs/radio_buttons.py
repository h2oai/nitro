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


# # Radio Buttons

# ## Basic
# Set `mode='radio'` to show radio buttons.
#
# `mode=` can be elided when there are 4-7 options.
def radio_basic(view: View):
    choice = view(box('Choose a color', mode='radio', options=[
        'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Value
# Set `value=` to pre-select an option having that value.
def radio_value(view: View):
    choice = view(box('Choose a color', mode='radio', value='yellow', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Selected
# Set `selected=True` to pre-select an option.
def radio_selected(view: View):
    choice = view(box('Choose a color', mode='radio', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Icons
# Set `icon=` to show graphical options.
def radio_icon(view: View):
    choice = view(box('Choose a chart type', mode='radio', options=[
        option('area', 'Area', icon='AreaChart', selected=True),
        option('bar', 'Bar', icon='BarChartHorizontal'),
        option('column', 'Column', icon='BarChartVertical'),
        option('line', 'Line', icon='LineChart'),
        option('scatter', 'Scatter', icon='ScatterChart'),
        option('donut', 'Donut', icon='DonutChart'),
    ]))
    view(f'You chose {choice}.')


