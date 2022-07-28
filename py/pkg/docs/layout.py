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
    view(
        box('Top', style='border p-2'),
        box('Middle', style='border p-2'),
        box('Bottom', style='border p-2'),
    )


# ## Horizontal layout
# Use `row()` to lay out multiple items horizontally, left to right.
def layout_row(view: View):  # height 2
    view(
        row(
            box('Left', style='border p-2'),
            box('Center', style='border p-2'),
            box('Right', style='border p-2'),
        )
    )


# `row(x, y, z)` is shorthand for `box(mode='row', items=[x, y, z], style='flex flex-row gap-2')`.
def layout_row_alt(view: View):
    view(box(
        mode='row',
        items=[
            box('Left', style='border p-2'),
            box('Center', style='border p-2'),
            box('Right', style='border p-2'),
        ],
        style='flex flex-row gap-2',
    ))


# ## Adjust items to fit
# Set the `grow` style to expand items to fit.
def layout_grow(view: View):  # height 2
    view(
        row(
            box('Left', style='border p-2 grow'),
            box('Center', style='border p-2 grow'),
            box('Right', style='border p-2 grow'),
        )
    )


# ## Adjust spacing
# Set a `gap` style to change the gap between items. The default gap is `gap-2`.
def layout_gap(view: View):  # height 2
    view(
        row(
            box('Left', style='border p-2 grow'),
            box('Center', style='border p-2 grow'),
            box('Right', style='border p-2 grow'),
            style='gap-8',
        )
    )


# ## Vertical layout
# Use `col()` to lay out multiple items vertically, top to bottom.
#
# The example shows one row split into three columns containing three rows each.
def layout_col(view: View):  # height 3
    style = 'border p-2'
    view(
        row(
            col(
                box('North-west', style=style),
                box('West', style=style),
                box('South-west', style=style),
            ),
            col(
                box('North', style=style),
                box('Center', style=style),
                box('South', style=style),
            ),
            col(
                box('North-east', style=style),
                box('East', style=style),
                box('South-east', style=style),
            ),
        ),
    )


# `col(x, y, z)` is shorthand for `box(mode='col', items=[x, y, z], style='flex flex-col gap-2')`.
def layout_col_alt2(view: View):
    box(
        mode='col',
        items=[
            box(value='North'),
            box(value='Center'),
            box(value='South'),
        ],
        style='flex flex-col gap-2',
    )


# ## Combine horizontal and vertical layouts
# Combine `row()` and `col()` to create simple grid-like layouts
#
# The example shows one row split into three columns containing three rows each.
def layout_row_col(view: View):  # height 3
    style = 'border p-2'
    view(
        row(
            col(
                box('North-west', style=style),
                box('West', style=style),
                box('South-west', style=style),
                style='grow gap-2'
            ),
            col(
                box('North', style=style),
                box('Center', style=style),
                box('South', style=style),
                style='grow gap-2'
            ),
            col(
                box('North-east', style=style),
                box('East', style=style),
                box('South-east', style=style),
                style='grow gap-2'
            ),
            style='gap-2'
        ),
    )


# ## Tabbed layout
# Set mode='tabs' on a box to lay out its items in tabs.
#
# The `text` of each child item is used as the tab's label.
def layout_tabs(view: View):  # height 5
    view(
        box(
            mode='tabs',
            items=[
                box(
                    'Profile',
                    items=[
                        box('First name', value='Boaty'),
                        box('Last name', value='McBoatface'),
                        box('Age', value=42)
                    ],
                ),
                box(
                    'Billing Address',
                    items=[
                        box('Billing address line 1', value=''),
                        box('Billing address line 2', value=''),
                        row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                    ],
                ),
                box(
                    'Shipping Address',
                    items=[
                        box('Shipping address line 1', value=''),
                        box('Shipping address line 2', value=''),
                        row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                    ],
                ),
            ]
        )
    )


# ## Accordion layout
# Set `mode='vertical tabs'` to lay out tabs one below the other, commonly known as an accordion.
def layout_tabs_vertical(view: View):  # height 5
    view(
        box(
            mode='vertical tabs',
            items=[
                box(
                    'Profile',
                    icon='Contact',
                    items=[
                        box('First name', value='Boaty'),
                        box('Last name', value='McBoatface'),
                        box('Age', value=42)
                    ],
                ),
                box(
                    'Billing Address',
                    icon='PaymentCard',
                    items=[
                        box('Billing address line 1', value=''),
                        box('Billing address line 2', value=''),
                        row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                    ],
                ),
                box(
                    'Shipping Address',
                    icon='DeliveryTruck',
                    items=[
                        box('Shipping address line 1', value=''),
                        box('Shipping address line 2', value=''),
                        row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                    ],
                ),
            ]
        )
    )


# ## Show icons on tabs
# Set `icon=` on each tab to show an icon on the tab.
def layout_tabs_icons(view: View):  # height 5
    view(
        box(
            mode='tabs',
            items=[
                box(
                    'Profile',
                    icon='Contact',
                    items=[
                        box('First name', value='Boaty'),
                        box('Last name', value='McBoatface'),
                        box('Age', value=42)
                    ],
                ),
                box(
                    'Billing Address',
                    icon='PaymentCard',
                    items=[
                        box('Billing address line 1', value=''),
                        box('Billing address line 2', value=''),
                        row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                    ],
                ),
                box(
                    'Shipping Address',
                    icon='DeliveryTruck',
                    items=[
                        box('Shipping address line 1', value=''),
                        box('Shipping address line 2', value=''),
                        row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                    ],
                ),
            ]
        )
    )


# ## Advanced layouts
# For explicit control over layouts, use `box(items=[...])` instead of `row(...)` or `col(...)`.
#
# The example below creates a 4-column grid layout using `style='grid'`.
def layout_grid(view: View):  # height 5
    view(
        box(
            items=[box(f'Box {i}', style='p-2 border') for i in range(1, 13)],
            style='grid grid-cols-4 gap-2',
        )
    )
