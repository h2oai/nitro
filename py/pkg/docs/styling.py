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


# # Styling
# Change how boxes look: colors, borders, sizing, margins, and padding.

# ## Set background color
# Set `background=` to apply a background color.
#
# The text color is automatically changed to a contrasting color if not specified.
# A padding is automatically applied if not specified.
def styling_background(view: View):
    text = lorem(3)
    view(
        box(text, background='#e63946'),
        box(text, background='#f1faee'),
        box(text, background='#a8dadc'),
        box(text, background='#457b9d'),
        box(text, background='#1d3557'),
    )
