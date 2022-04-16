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


# # Dropdown List

# ## Basic
# Set `mode='menu'` with `multiple=True` to show a dropdown menu that allows multiple options to be selected.
#
# `mode=` can be elided when there are more than 7 options.
def multi_dropdown_basic(view: View):
    choices = view(box(
        'Choose some colors',
        mode='menu',
        multiple=True,
        options=['green', 'yellow', 'orange', 'red']
    ))
    view(f'You chose {choices}.')


# ## Value
# Set `value=` to pre-select options having those values.
def multi_dropdown_value(view: View):
    choices = view(box(
        'Choose some colors',
        mode='menu',
        multiple=True,
        value=['yellow', 'red'],
        options=['green', 'yellow', 'orange', 'red']
    ))
    view(f'You chose {choices}.')


# ## Selected
# Alternatively, set `selected=True` to pre-select one or more options.
def multi_dropdown_selected(view: View):
    choices = view(box(
        'Choose some colors',
        mode='menu',
        multiple=True,
        options=[
            option('green', 'Green'),
            option('yellow', 'Yellow', selected=True),
            option('orange', 'Orange'),
            option('red', 'Red', selected=True),
        ]
    ))
    view(f'You chose {choices}.')
