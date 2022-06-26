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

# ## Basic
# Call `box()` with `mode='separator'` to show a separator.
def separator_basic(view: View):  # height 2
    view(box('Donuts', mode='separator'))


# ## Set text alignment
# A separator's label is centered by default.
# Set `align=` to left- or right-align the label.
def separator_align(view: View):  # height 4
    view(
        box('Left-aligned', mode='separator', align='left'),
        box(lorem(3)),
        box('Center-aligned', mode='separator'),
        box(lorem(3)),
        box('Right-aligned', mode='separator', align='right'),
        box(lorem(3)),
    )
