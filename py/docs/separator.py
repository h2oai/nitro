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
# Call `box()` with `mode='number'` to show a box with increment/decrement buttons.
# (also called a *spinbox*).
def separator_basic(view: View):
    view(box('Donuts', mode='separator'))


# ## Set text alignment
def separator_align(view: View):
    view(
        box('Left-aligned', mode='separator', align='left'),
        box(lorem(3)),
        box('Center-aligned', mode='separator'),
        box(lorem(3)),
        box('Right-aligned', mode='separator', align='right'),
        box(lorem(3)),
    )