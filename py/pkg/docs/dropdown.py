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


# # Dropdown
# Use a dropdown to pick one option from a large number of options.

# ## Basic
# Set `mode='menu'` to show a dropdown menu.
#
# `mode=` can be elided when there are more than 7 options.
def dropdown_basic(view: View):  # height 2
    choice = view(box('Choose a color', mode='menu', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Set initial selection
# Set `value=` to pre-select an option having that value.
def dropdown_value(view: View):  # height 2
    choice = view(box('Choose a color', mode='menu', value='yellow', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Mark options as selected
# Set `selected=True` to pre-select an option.
def dropdown_selected(view: View):  # height 2
    choice = view(box('Choose a color', mode='menu', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Group options
# Options can have sub-options. This is useful for grouping options into categories.
#
# `mode=menu` is implied if options are grouped.
def dropdown_grouped(view: View):  # height 2
    choice = view(box('Choose a color', options=[
        option('primary', 'Primary Colors', options=[
            option('red', 'Red'),
            option('blue', 'Blue'),
            option('yellow', 'Yellow'),
        ]),
        option('secondary', 'Secondary Colors', options=[
            option('violet', 'Violet'),
            option('green', 'Green'),
            option('orange', 'Orange'),
        ]),
    ]))
    view(f'You chose {choice}.')


# ## Enable arbitrary input
# Set `editable=True` to allow arbitrary input in addition to the presented options.
#
# `mode=menu` is implied if `editable=True`.
def dropdown_editable(view: View):  # height 2
    choice = view(box('Choose a color', editable=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Handle changes immediately
# Set `live=True` to handle changes immediately.
def dropdown_live(view: View):  # height 3
    choice = 'yellow'
    while True:
        choice = view(
            box(
                'Choose a color',
                mode='menu',
                value=choice,
                live=True,
                options=['green', 'yellow', 'orange', 'red'],
            ),
            f'You chose {choice}.'
        )
