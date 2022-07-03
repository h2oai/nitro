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

from h2o_nitro import View, box, row, col, option, header, lorem


# # Table
# Use tables to display detailed information in the form of a grid.
# Tables can be thought of as pickers that allow one or more rows to be selected.
# They are a good replacement for dropdowns and dropdown lists when each option has several displayable attributes.

# ## Basic
# Call `box()` with `mode='table'` to show a table.
def table_basic(view: View):  # height 4
    view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!'),
            header('Extras'),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ],
    ))


# ## Make rows clickable
# To make rows clickable, set `mode='link'` on a header.
#
# If set, `view()` returns the `value` of the clicked row.
def table_clickable(view: View):  # height 4
    choice = view(box(
        mode='table',
        headers=[
            header('Flavor', mode='link'),
            header('Super cheap!'),
            header('Extras'),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ],
    ))
    view(f'You chose {choice}.')


# ## Use markdown in cells
# By default, cells are interpreted as plain text. To interpret them as markdown, set `mode='md'` on the header.
def table_markdown(view: View):  # height 4
    choice = view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!'),
            header('Extras', mode='md'),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', '*Sugar and spice*']),
            option('sugar', options=['Powdered Sugar', '$1.99', '**Served warm**']),
            option('vanilla',
                   options=['Vanilla', '$2.99', 'With [cookie](https://en.wikipedia.org/wiki/Cookie) crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With ~real~ blueberry']),
        ],
    ))
    view(f'You chose {choice}.')


# ## Enable multi-select
# Set `multiple=True` to allow rows to be selected. This effectively allow a table to be used in place of a
# dropdown menu, especially useful when each item has multiple attributes.
#
# The return value is a collection of the values of the selected rows.
def table_multiselect(view: View):  # height 4
    choices = view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!'),
            header('Extras'),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ],
        multiple=True,
    ))
    view(f'You chose {choices}.')


# ## Enable single select
# Set `multiple=False` to allow at most one row to be selected.
#
# The return value is the `value` of the selected row.
def table_singleselect(view: View):  # height 4
    choice = view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!'),
            header('Extras'),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ],
        multiple=False,
    ))
    view(f'You chose {choice}.')


# ## Set initial selection
# Set `value=` to pre-select one or more rows.
def table_value(view: View):  # height 4
    choices = view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!'),
            header('Extras'),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ],
        multiple=True,
        value=['vanilla', 'blueberry'],
    ))
    view(f'You chose {choices}.')


# ## Mark rows as selected
# Alternatively, set `selected=True` on a row to pre-select the row.
def table_selected(view: View):  # height 4
    choices = view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!'),
            header('Extras'),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles'], selected=True),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry'], selected=True),
        ],
        multiple=True,
    ))
    view(f'You chose {choices}.')


# ## Group rows
# To group rows, use nested options.
def table_grouped(view: View):  # height 7
    choice = view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!'),
            header('Extras'),
        ],
        options=[
            option('donuts', text='Donuts', options=[
                option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
                option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
                option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
                option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
                option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
            ]),
            option('coffee', text='Coffee', options=[
                option('blonde', options=['Blonde Roast', '$1.49', 'Light and creamy']),
                option('medium', options=['Medium Roast', '$1.49', 'House favorite']),
                option('dark', options=['Dark Roast', '$1.49', 'Bold and sassy']),
            ]),
        ],
    ))


# ## Group rows at multiple levels
# Rows can be nested at multiple levels.
def table_multilevel(view: View):  # height 8
    choice = view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!'),
            header('Extras'),
        ],
        options=[
            option('donuts', text='Donuts', options=[
                option('popular', text='Popular', options=[
                    option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
                    option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
                ]),
                option('specialty', text='Specialty', options=[
                    option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
                    option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
                    option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
                ]),
            ]),
            option('coffee', text='Coffee', options=[
                option('blonde', options=['Blonde Roast', '$1.49', 'Light and creamy']),
                option('medium', options=['Medium Roast', '$1.49', 'House favorite']),
                option('dark', options=['Dark Roast', '$1.49', 'Bold and sassy']),
            ]),
        ],
    ))


# ## Set column width
# Set `width=` to set the minimum width of the column.
#
# To set both minimum and maximum widths, set `width=` to a `(min, max)` tuple.
def table_column_width(view: View):  # height 4
    view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!', width=100),
            header('Extras', width=(200, 300)),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ],
    ))


# ## Set header icon
# Set `icon=` to display an icon in the header instead of text.
def table_header_icon(view: View):  # height 4
    view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!', icon='Money'),
            header('Extras'),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ],
    ))


# ## Disable column resizing
# Set `resizable=False` to prevent a column from being resized.
def table_header_resizable(view: View):  # height 4
    view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!', resizable=False),
            header('Extras'),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ],
    ))


# ## Enable multiline cells
# Set `Multiline=True` to allow multiline text in a column's cells
def table_column_multiline(view: View):  # height 4
    view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!'),
            header('Extras', multiline=True),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ],
    ))
