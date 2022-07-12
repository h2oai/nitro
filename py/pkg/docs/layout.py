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

# ## Basics
# By default each item passed to `view()` are laid out one below the other, with a `10px` gap.
def layout_basic(view: View):  # height 3
    view(
        box(value='Top'),
        box(value='Middle'),
        box(value='Bottom'),
    )


# ## Lay out horizontally
# Use `row()` to lay out multiple items horizontally, left to right.
#
# By default, items take up equal amounts of space, with a `10px` gap between the items.
def layout_row(view: View):  # height 2
    view(row(
        box(value='Left'),
        box(value='Center'),
        box(value='Right'),
    ))


# Setting `mode='row'` produces the same result as wrapping items with `row()`.
def layout_row_alt(view: View):
    view(
        box(value='Left'),
        box(value='Center'),
        box(value='Right'),
        mode='row',
    )


# ## Lay out vertically
# Use `col()` to lay out multiple items vertically, top to bottom.
#
# The example shows one row split into three columns containing three rows each.
def layout_col(view: View):  # height 3
    view(
        row(
            col(
                box(value='North-west'),
                box(value='West'),
                box(value='South-west'),
            ),
            col(
                box(value='North'),
                box(value='Center'),
                box(value='South'),
            ),
            col(
                box(value='North-east'),
                box(value='East'),
                box(value='South-east'),
            ),
        ),
    )


# ## Control scrolling
# Set `height=` or `width=` on a `row()` or `col()` to constrain size.
# Scrollbars automatically show up if their contents don't fit.
def layout_nest(view: View):  # height 13
    list1 = [box(lorem()) for _ in range(50)]
    list2 = [box(lorem()) for _ in range(50)]
    view(
        "### Scroll together",
        row(
            col(*list1),
            col(*list2),
            height='500px',
        ),
        "### Scroll independently",
        row(
            col(*list1, height='500px'),
            col(*list2, height='500px'),
        )
    )


# ## Control tiling
# Set `tile=` to control how items inside a view, row, or column are tiled along the main axis.
#
# - The main axis for a row is horizontal, starting at the left, and ending at the right.
# - The main axis for a column is vertical, starting at the top, and ending at the bottom
#
# `tile=` can be set to `start`, `center`, `end`, `between`, `around`, `evenly`, `stretch`, or `normal`.
def layout_tile(view: View):  # height 9
    boxes = [box(text=f'{i + 1}', background='#666', width=100) for i in range(3)]
    row_style = dict(background='#eee')
    view(
        "Start",
        # Pack items from the start.
        row(*boxes, tile='start', **row_style),

        "Center",
        # Pack items around the center.
        row(*boxes, tile='center', **row_style),

        "End",
        # Pack items towards the end.
        row(*boxes, tile='end', **row_style),

        "Between",
        # Distribute items evenly.
        # The first item is flush with the start,
        # the last is flush with the end.
        row(*boxes, tile='between', **row_style),

        "Around",
        # Distribute items evenly.
        # Items have a half-size space on either side.
        row(*boxes, tile='around', **row_style),

        "Evenly",
        # Distribute items evenly.
        # Items have equal space around them.
        row(*boxes, tile='evenly', **row_style),

        "Normal",
        # Default alignment.
        row(*boxes, tile='normal', **row_style),
    )


# ## Control cross tiling
# Set `cross_tile=` to control how items inside a view, row, or column are tiled along the cross axis.
#
# - The cross axis for a row is vertical. starting at the top, and ending at the bottom
# - The cross axis for a column is horizontal, starting at the left, and ending at the right.
#
# `cross_tile=` can be set to `start`, `center`, `end`, `stretch`, or `normal`.
def layout_cross_tile(view: View):  # height 9
    boxes = [box(text=f'{i + 1}', background='#666', width=100) for i in range(3)]
    row_style = dict(height=150, background='#eee')
    view(
        # Pack items from the start.
        row(*boxes, cross_tile='start', **row_style),

        # Pack items around the center.
        row(*boxes, cross_tile='center', **row_style),

        # Pack items towards the end.
        row(*boxes, cross_tile='end', **row_style),

        # Stretch items to fit.
        row(*boxes, cross_tile='stretch', **row_style),

        # Default alignment.
        row(*boxes, cross_tile='normal', **row_style),
    )


# ## Control spacing
# Set `gap=` to control the spacing between items. The default gap is `10` or `'10px'`.
def layout_gap(view: View):  # height 3
    view(
        box(value='Top'),
        box(value='Middle'),
        box(value='Bottom'),
        gap=25,
    )


# ## Control wrapping
# Set `wrap=` to control how items are wrapped inside a view, row, or column.
#
# `wrap=` can be set to `start`, `center`, `end`, `between`, `around`, `evenly`, `stretch`, or `normal`.
def layout_wrap(view: View):  # height 23
    boxes = [box(text=f'{i + 1}', background='#666', width=150, height=50) for i in range(9)]
    row_style = dict(height=300, background='#eee')
    view(
        # Pack items from the start.
        row(*boxes, wrap='start', **row_style),

        # Pack items around the center.
        row(*boxes, wrap='center', **row_style),

        # Pack items towards the end.
        row(*boxes, wrap='end', **row_style),

        # Distribute items evenly.
        # The first item is flush with the start,
        # the last is flush with the end.
        row(*boxes, wrap='between', **row_style),

        # Distribute items evenly.
        # Items have a half-size space on either side.
        row(*boxes, wrap='around', **row_style),

        # Distribute items evenly.
        # Items have equal space around them.
        row(*boxes, wrap='evenly', **row_style),

        # Default alignment.
        row(*boxes, wrap='normal', **row_style),
    )


# ## Grow or shrink some items
# Set `grow=` or `shrink=` to specify what amount of the available space the item should take up
# inside a view, row, or column.
#
# Setting `grow=` expands the item. Setting `shrink=` contracts the item. Both are proportions.
#
# By default, items are grown or shrunk based on their initial size. To resize them on a different basis,
# set `basis=` to the value you want.
#
# - `basis=0` means "distribute available space assuming that the initial size is zero".
# - `basis='20px'` means "distribute available space assuming that the initial size is 20px".
# - The default behavior (if `basis=` is not set) is to assume that the initial size is the size of the item's content.
def layout_grow_shrink(view: View):  # height 7
    box_style = dict(background='#666')
    row_style = dict(background='#eee')
    view(
        '1:?:?',
        row(
            # Take up all available space.
            box('a', grow=1, **box_style),
            box('b', width=50, **box_style),
            box('c', width=50, **box_style),
            **row_style,
        ),
        '1:1:?',
        row(
            # Take up one part of available space = 1 / (1 + 1).
            box('a', grow=1, **box_style),
            # Take up one part of available space = 1 / (1 + 1).
            box('b', grow=1, **box_style),
            box('c', width=50, **box_style),
            **row_style,
        ),
        '2:1:?',
        row(
            # Take up two parts of available space = 2 / (2 + 1).
            box('a', grow=2, **box_style),
            # Take up one part of available space = 1 / (2 + 1).
            box('b', grow=1, **box_style),
            box('c', width=50, **box_style),
            **row_style,
        ),
        '1:2:3:?',
        row(
            # Take up one part of available space = 1 / (1 + 2 + 3).
            box('a', grow=1, **box_style),
            # Take up two parts of available space = 2 / (1 + 2 + 3).
            box('b', grow=2, **box_style),
            # Take up three parts of available space = 3 / (1 + 2 + 3).
            box('c', grow=3, **box_style),
            box('d', width=50, **box_style),
            **row_style,
        ),
        '1:1:1:1',
        row(
            # Divide available space equally.
            box('a', grow=1, **box_style),
            box('b', grow=1, **box_style),
            box('c', grow=1, **box_style),
            box('d', grow=1, **box_style),
            **row_style,
        ),
    )


# ## Center content vertically
# Use `tile='center'` to center content vertically inside a box.
#
# The following example centers content both horizontally and vertically.
def layout_vertical_alignment(view: View):  # height 5
    view(
        box(
            '# Donuts',
            tile='center', cross_tile='center',
            height='300px', background='$foreground', color='$background',
        )
    )
