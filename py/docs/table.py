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


# # List

# ## Basic
# Call `box()` with `mode='list'` to show a list. A list can be a good substitute for a dropdown menu
# when each item has several details that are better displayed in tabular form.
def list_basic(view: View):
    choice = view(box(
        mode='list',
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
    view(f'You chose {choice}.')


# ## Multi-select
# Set `multiple=True` to allow multiple rows to be selected.
#
# The return value is a collection of the values of the selected rows.
def list_multiselect(view: View):
    choices = view(box(
        mode='list',
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


# ## Value
# Set `value=` to pre-select one or more rows.
def list_value(view: View):
    choices = view(box(
        mode='list',
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


# ## Selected
# Alternatively, set `selected=True` on a row to pre-select the row.
def list_selected(view: View):
    choices = view(box(
        mode='list',
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


# ## Grouped
# To group rows, use nested options.
def list_grouped(view: View):
    choice = view(box(
        mode='list',
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
    view(f'You chose {choice}.')


# ## Multi-level Grouped
# Rows can be nested at multiple levels.
def list_multilevel(view: View):
    choice = view(box(
        mode='list',
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
    view(f'You chose {choice}.')


# # Table

# ## Basic
# Call `box()` with `mode='table'` to show a table.
def table_basic(view: View):
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


# ## Clickable columns
# To make a column's cells clickable, set `mode='link'` on its header.
#
# If set, `view()` returns the `value` of the clicked row.
def table_primary(view: View):
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
