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
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm.']),
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
        multiple=True,
        headers=[
            header('Flavor'),
            header('Super cheap!'),
            header('Extras'),
        ],
        options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm.']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ],
    ))
    view(f'You chose {x}.')
