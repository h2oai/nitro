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

# ## Basic
# Call `box()` with `mode='table'` to show a table. A table can be a good substitute for a dropdown or dropdown list
# when each item has several details that are better displayed in grid form.
#
# The return value the value of selected row.
def table_basic(view: View):
    x = view(box(
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
    view(f'You chose {x}.')


# ## Primary Column
# By default, the first column's cells are clickable.
# To set a different column as clickable, set `primary=True` on its header.
def table_primary(view: View):
    x = view(box(
        mode='table',
        headers=[
            header('Flavor'),
            header('Super cheap!', primary=True),
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
    view(f'You chose {x}.')


# ## Multi-select
# Set `multiple=True` to allow multiple rows to be selected.
#
# The return value is a collection of the values of the selected rows.
def table_multiselect(view: View):
    x = view(box(
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
    view(f'You chose {x}.')


# ## Value
# Set `value=` to pre-select row.
def table_value(view: View):
    x = view(box(
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
    view(f'You chose {x}.')


# ## Selected
# Alternatively, set `selected=True` on the row to pre-select the row.
def table_selected(view: View):
    x = view(box(
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
    view(f'You chose {x}.')


# ## Grouped
# To group rows, use nested options.
def table_grouped(view: View):
    x = view(box(
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
    view(f'You chose {x}.')


# ## Multi-level
# Rows can be nested at multiple levels.
def table_grouped_multiple(view: View):
    x = view(box(
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
    view(f'You chose {x}.')
