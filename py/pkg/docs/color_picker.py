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


# # Color Picker
# Use a color picker to pick an arbitrary color.

# ## Basic
# Set `mode='color'` to show a color picker.
#
# The return value is a `(r, g, b, a)` tuple,
# where `r`, `g`, `b` are integers between 0-255,
# and `a` is an integer between 0-100%.
def color_basic(view: View):  # height 6
    color = view(box('Choose a color', mode='color'))
    r, g, b, a = color
    view(f'You chose the color `rgba({r}, {g}, {b}, {a}%)`.')


# ## Set initial color
# Set `value=` to set the initial color.
#
# A color value can be:
#
# - `#RRGGBB` e.g. `#ff0033`
# - `#RRGGBBAA` e.g. `#ff003388`
# - `#RGB` e.g. `#f03` (same as `#ff0033`)
# - `#RGBA` e.g. `#f038` (same as `#ff003388`)
# - `rgb(R,G,B)` e.g. `rgb(255, 0, 127)` or `rgb(100%, 0%, 50%)`
# - `rgba(R,G,B,A)` e.g. `rgb(255, 0, 127, 0.5)` or `rgb(100%, 0%, 50%, 50%)`
# - `hsl(H,S,L)` e.g. `hsl(348, 100%, 50%)`
# - `hsl(H,S,L,A)` e.g. `hsl(348, 100%, 50%, 0.5)` or `hsl(348, 100%, 50%, 50%)`
# - A [named color](https://drafts.csswg.org/css-color-3/#svg-color) e.g. `red`, `green`, `blue`, etc.
# - `transparent` (same as `rgba(0,0,0,0)`)
#
# The return value, as in the previous example, is a `(r, g, b, a)` tuple.
def color_value(view: View):  # height 6
    color = view(box('Choose a color', mode='color', value='#a241e8'))
    view(f'You chose {color}.')


# ## Handle changes immediately
# Add `live` to `mode` to handle changes immediately.
def color_live(view: View):  # height 6
    color = [162, 65, 232, 100]
    while True:
        color = view(
            box(
                'Choose a color',
                mode='live color',
                value=f'rgba({color[0]},{color[1]},{color[2]},{color[3]}%)',
            ),
            f'You chose {color}.'
        )
