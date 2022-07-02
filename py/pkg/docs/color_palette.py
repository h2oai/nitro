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


# # Color Palette
# Use a color palette to pick one color from a group of colors.

# ## Basic
# Set `options=` with `mode='color'` to show a color palette.
#
# The option's `value` must be a valid color in one of the formats described in the previous example.
#
# Unlike the Color Picker, the Color Palette returns the `value` of the chosen option, and not a `(r,g,b,a)` tuple.
def palette_basic(view: View):  # height 2
    color = view(box('Choose a color', mode='color', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue'),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(f'You chose {color}.')


# ## Set initial color
# Set `value=` to pre-select an option having that color value.
def palette_value(view: View):  # height 2
    color = view(box('Choose a color', mode='color', value='#0000ff', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue'),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(f'You chose {color}.')


# ## Mark colors as selected
# Alternatively, set `selected=True` to pre-select a color in the palette.
def palette_selected(view: View):  # height 2
    color = view(box('Choose a color', mode='color', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue', selected=True),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(f'You chose {color}.')
