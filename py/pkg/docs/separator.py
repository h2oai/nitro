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
# A separator's text is centered by default. Add `left`, `right`, `top`, `middle`, or `bottom` to `mode` to change the
# orientation and text alignment.
def separator_align(view: View):  # height 4
    content = box(lorem(1), style='p-2 bg-stripes-accent')
    view(
        row(
            col(
                content,
                box('Left', mode='left separator'),
                content,
            ),
            col(
                content,
                box('Center', mode='separator'),
                content,
            ),
            col(
                content,
                box('Right', mode='right separator'),
                content,
            ),
        ),
        row(
            content,
            box('Top', mode='top separator'),
            content,
            box('Middle', mode='middle separator'),
            content,
            box('Bottom', mode='bottom separator'),
            content,
        ),
    )
