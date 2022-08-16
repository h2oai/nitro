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


# # Layout
# Compose and arrange boxes to lay out content and control flow.

# ## Basic
# By default, items passed to `view()` are laid out one below the other.
def layout_basic(view: View):  # height 3
    block = box() / 'p-2 rounded bg-accent-500 text-white'
    view(
        block('Top'),
        block('Middle'),
        block('Bottom'),
        style='bg-stripes-accent',
    )


# ## Rows
# Use `row()` to lay out multiple items horizontally, left to right.
def layout_row(view: View):  # height 2
    block = box() / 'p-2 rounded bg-accent-500 text-white'
    view(
        row(
            block('Left'),
            block('Center'),
            block('Right'),
        ) / 'bg-stripes-accent'
    )


# `row(x, y, z)` is in fact shorthand for `box(x, y, z, mode='row', style='flex flex-row gap-2')`.
# The following code produces the same results.
def layout_row_alt(view: View):
    block = box() / 'p-2 rounded bg-accent-500 text-white'
    view(
        box(
            block('Left'),
            block('Center'),
            block('Right'),
            mode='row',
        ) / 'flex flex-row gap-2 bg-stripes-accent',
    )


# ## Fit
# Set the `grow` style to expand items to fit.
def layout_grow(view: View):  # height 2
    block = box() / 'p-2 rounded bg-accent-500 text-white grow'
    view(
        row(
            block('Left'),
            block('Center'),
            block('Right'),
        ) / 'bg-stripes-accent'
    )


# ## Columns
# Use `col()` to lay out multiple items vertically, top to bottom.
#
# The example shows one row split into three columns containing three rows each.
def layout_col(view: View):  # height 3
    block = box() / 'p-2 rounded bg-accent-500 text-white'
    view(
        col(
            block('North'),
            block('Center'),
            block('South'),
        ) / 'bg-stripes-accent',
    )


# `col(x, y, z)` is shorthand for `box(x, y, z, mode='col', style='flex flex-col gap-2')`.
def layout_col_alt2(view: View):
    box(
        box('North'),
        box('Center'),
        box('South'),
        mode='col',
    ) / 'flex flex-col gap-2'


# ## Combine rows and columns
# Combine `row()` and `col()` to create simple grid-like layouts
#
# The example shows one row split into three columns containing three rows each.
def layout_row_col(view: View):  # height 3
    block = box() / 'p-2 rounded bg-accent-500 text-white'
    grow = col() / 'grow'  # a column stretched horizontally
    view(
        row(
            grow(block('North-west'), block('West'), block('South-west')),
            grow(block('North'), block('Center'), block('South')),
            grow(block('North-east'), block('East'), block('South-east')),
        ) / 'bg-stripes-accent',
    )


# ## Grids
# A simple way to lay out items in a grid is use the `grid` style.
#
# The example below lays out 12 boxes in a 4-column grid.
def layout_grid(view: View):  # height 3
    style = 'p-2 rounded bg-accent-500 text-white'

    # Create some boxes.
    boxes = [box(f'Box {i}') / style for i in range(1, 13)]

    # Place the boxes in a 4-column grid.
    view(box(*boxes) / 'grid grid-cols-4 gap-2 bg-stripes-accent')


# ## Groups
# Add `mode='group'` or set `title=` to create a group. A group can be expanded or collapsed by the user.
#
# A group is collapsed by default. Add `open` to `mode` to expand it.
def layout_group(view: View):  # height 4
    view(
        '## Menu',
        box(lorem(3), title='Donuts', mode='open'),
        box(lorem(3), title='Coffee'),
        box(lorem(3), title='Ice Cream'),
    )


# ## Tabs
# Put groups in a row to display a tabbed layout.
def layout_tabs(view: View):  # height 3
    view(
        row(
            box(lorem(3), title='Donuts'),
            box(lorem(3), title='Coffee'),
            box(lorem(3), title='Ice Cream'),
        )
    )


# ## Vertical Tabs
# Put groups in a column to display a vertical tabbed layout.
def layout_tabs_vertical(view: View):  # height 3
    view(
        col(
            box(lorem(3), title='Donuts'),
            box(lorem(3), title='Coffee'),
            box(lorem(3), title='Ice Cream'),
        )
    )


# ## Tabs with icons
# Set `icon=` on each group to show an icon on its tab.
def layout_tabs_icons(view: View):  # height 4
    view(
        row(
            box(lorem(3), title='Profile', icon='Contact'),
            box(lorem(3), title='Billing Address', icon='PaymentCard'),
            box(lorem(3), title='Shipping Address', icon='DeliveryTruck'),
        ),
    )


# ## Vertical Tabs with icons
# Set `icon=` on each group to show an icon on its tab.
def layout_tabs_vertical_icons(view: View):  # height 4
    view(
        col(
            box(lorem(3), title='Profile', icon='Contact'),
            box(lorem(3), title='Billing Address', icon='PaymentCard'),
            box(lorem(3), title='Shipping Address', icon='DeliveryTruck'),
        )
    )


# ## Select tab
# Set a tab's `mode` to `open` to open that tab instead of the first tab in the set.
def layout_tab_select(view: View):  # height 4
    view(
        row(
            box(lorem(3), title='Donuts'),
            box(lorem(3), title='Coffee', mode='open'),
            box(lorem(3), title='Ice Cream'),
        )
    )


# ## Select vertical tab
# Set a tab's `mode` to `open` to open that tab instead of the first tab in the set.
def layout_tab_vertical_select(view: View):  # height 4
    view(
        col(
            box(lorem(3), title='Donuts'),
            box(lorem(3), title='Coffee', mode='open'),
            box(lorem(3), title='Ice Cream'),
        )
    )
