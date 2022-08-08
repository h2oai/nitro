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


# # Separator
# Use a separator to visually separate form inputs into sections.

# ## Basic
# Call `box()` with `mode='separator'` to show a separator.
def separator_basic(view: View):  # height 2
    view(box('Donuts', mode='separator'))


# ## Set text alignment
# A separator's text is centered by default.
#
# - Set `text-start` to show text at the start of the separator.
# - Set `text-end` to show text at the end of the separator.
def separator_align(view: View):  # height 4
    view(
        box('Left-aligned', mode='separator text-start'),
        box(lorem(3)),
        box('Center-aligned', mode='separator'),
        box(lorem(3)),
        box('Right-aligned', mode='separator text-end'),
        box(lorem(3)),
    )


# ## Vertical
# Set `vertical` to show a vertical separator
def separator_vertical(view: View):  # height 4
    view(
        row(
            box('Top-aligned', mode='vertical separator text-start'),
            box(lorem(3)),
            box('Center-aligned', mode='vertical separator'),
            box(lorem(3)),
            box('Bottom-aligned', mode='vertical separator text-end'),
            box(lorem(3)),
        )
    )
